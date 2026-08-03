# MLLM 组合推理 RL 增强方法 — 背景文献调研

> 调研目的：为综述论文《MLLM 组合推理中 RL 增强方法》补齐 Background 层文献
> 调研日期：2026-08-03
> 核心论点：RL 在 MLLM 组合推理中的发展，本质上是奖励信号从结果验证向视觉语义结构和推理过程对齐的演进过程

---

## 一、RLHF/RLAIF 在 MLLM 上的经典工作

### 1.1 LLaVA-RLHF

- **论文**：Aligning Large Multimodal Models with Factually Augmented RLHF（arXiv:2309.14525，引用 757+）
- **核心做法**：提出 **Factually Augmented RLHF（Fact-RLHF）**——在训练 reward model 时，额外注入图像描述（image captions）等事实信息，使奖励信号具有事实依据，从而校准模型输出、减少奖励篡改（reward hacking）和幻觉。

**奖励信号设计**：
- 类型：人类偏好（RLHF），结果级（outcome-level）
- 粒度：对完整回答整体打分，通过 PPO 优化策略
- 关键改进：reward model 的输入不再只有"问题+回答"，而是"问题+回答+图像事实描述"，让奖励判断有据可依

**在组合推理上的局限**：
- 奖励信号仍是**整体质量**的判断——"这个回答是否与图像一致"，而非"模型的组合理解是否正确"
- 事实增强（图像描述）是粗粒度的——描述本身可能已丢失组合细节（如"左边发霉的橙子"可能被描述为"两个橙子"）
- 该工作主要针对幻觉（hallucination）问题，组合推理（compositional reasoning）不是其直接目标

### 1.2 RLHF-V

- **论文**：RLHF-V: Towards Trustworthy MLLMs via Behavior Alignment from Fine-grained Correctional Human Feedback（arXiv:2312.00849，CVPR 2024，引用 590+）
- **核心做法**：提出**细粒度纠错人类反馈（fine-grained correctional human feedback）**——标注员不仅判断回答好坏，还直接**纠正模型输出中幻觉的具体片段**，然后用 dense DPO 学习这些细粒度反馈。

**奖励信号设计**：
- 类型：人类反馈 + 纠错（比 LLaVA-RLHF 更细粒度），使用 DPO 而非 PPO（无需单独训练 reward model）
- 粒度：**片段级（segment-level）**——奖励/惩罚细化为回答中的具体句子或片段
- 数据规模：1.4K 细粒度密集反馈样本

**在组合推理上的局限**：
- 反馈粒度已细化到片段级，但片段仍是"语言单元"，不是"视觉-语义组合单元"
- 人类标注员纠正的是"描述与图像不符"的片段，但组合错误往往表现为"描述看似合理但与图像的绑定错误"——例如"左边的橙子是发霉的"被纠正为"橙子是发霉的"（丢失空间绑定）时，需要标注员主动识别这种绑定错误，成本极高
- DPO 不经过 RL 循环，严格来说不是"RL 增强"，但常作为对比基线

### 1.3 Silkie

- **论文**：Aligning Large Vision-Language Models with AI Feedback（arXiv:2410.09421）
- **核心做法**：用 **GPT-4V 作为 AI 标注员**生成偏好数据（VLFeedback 数据集），对 Qwen-VL-Chat 做 DPO 训练。属于 **RLAIF（AI 反馈强化学习）** 路线的代表。

**奖励信号设计**：
- 类型：AI 反馈（GPT-4V 生成偏好对），使用 DPO
- 粒度：结果级——GPT-4V 对两个回答比较排序
- 规模：VLFeedback 包含约 8 万条多模态指令及 GPT-4V 标注的偏好

**在组合推理上的局限**：
- AI 标注员（GPT-4V）自身在组合推理上就有系统性弱点（属性绑定、空间关系错误），AI 反馈会**传播同样的盲区**——"以盲导盲"
- 偏好比较是整体的（哪个回答更好），无法定位到具体组合错误的环节
- 这与论文 thesis 直接相关：**AI 反馈的可靠性取决于标注模型自身的组合理解能力，形成闭环盲区**

### 小结：奖励信号在组合推理上的局限

| 方法 | 反馈来源 | 粒度 | 组合推理覆盖 |
|------|---------|------|-------------|
| LLaVA-RLHF | 人类偏好 | 结果级 | 无（聚焦幻觉） |
| RLHF-V | 人类纠错 | 片段级 | 弱（语言片段，非视觉-语义组合） |
| Silkie | GPT-4V | 结果级 | 无（且 AI 标注自身有组合盲区） |

**关键观察**：这一阶段的共同特征是**奖励信号来自"人对回答的评判"，而非"对组合正确性的验证"**。无论反馈来自人类还是 AI，奖励粒度都停留在"回答好不好"，没有触及"组合绑定对不对"。这正是论文 thesis 中"结果验证"阶段的含义。

---

## 二、MLLM 组合推理评测基准

### 2.1 VALSE

- **论文**：VALSE: A Task-Independent Benchmark for Vision and Language Models Centered on Linguistic Phenomena（arXiv:2112.07566，ACL 2022 Main，引用 172+）
- **定位**：任务无关（task-independent）的视觉-语言结构化评测基准，围绕**语言现象**（linguistic phenomena）测试通用预训练 V&L 模型的视觉-语言 grounding 能力。核心方法是构造**伪造实例（foiled instances）**——对正确描述做最小修改使其与图像不符，测试模型能否识别。

**评测的六项测试**（语言现象）：
1. 存在性（Existence）：图中是否有该物体
2. 复数（Plurality）：单复数等数量表达的理解
3. 计数（Counting）
4. 空间关系（Spatial Relations）："左边/右边/上面"等
5. 动作（Actions）
6. **实体共指（Entity Coreference）**：代词等是否指向正确的实体

**评测方式**：给模型一个"真实描述或伪造描述"（foil），判断描述与图像是否匹配（真/假判断），需要模型对语言结构敏感。论文评估了 5 个广泛使用的 V&L 模型，发现模型在存在性上表现较好、计数尚可，但在复数、空间关系、共指和动作上挣扎。

### 2.2 SugarCrepe

- **论文**：SugarCrepe: Fixing Hackable Benchmarks for Vision-Language Compositionality（arXiv:2306.14610，NeurIPS 2023，引用 296+）
- **核心贡献**：指出现有组合评测基准（ARO、CREPE 等）存在**可被 hack 的漏洞**——程序化生成的 hard negatives 往往不合逻辑或不流畅，模型可以靠语言先验（而非真正的组合理解）分辨正负样本。SugarCrepe 用 **LLM 生成语义合理的 hard negatives**，消除这些 artifact。

**评测结构**（基于 COCO 图文对）：
- **Replace 形式**（替换原子概念）：Replace-Obj（物体）、Replace-Att（属性）、Replace-Rel（关系）
- **Swap 形式**（交换两个同类别概念）：Swap-Obj、Swap-Att
- **Add 形式**（添加新概念）：Add-Obj、Add-Att
- 共 7512 个测试样本，每个样本为"图像 + 正描述 + 硬负描述"的二选一检索任务（随机基线 50%）

**关键发现**（对论文极有价值）：
1. **现有模型是物体中心的（object-centric）**：模型在物体组合上接近人类水平，但在**属性和关系**组合上显著落后（Replace-Att 掉 15%，Replace-Rel 掉 29%）
2. **Swap 形式最难**：所有模型在 Swap 上表现最差（与人类差距达 27%-50%），因为 Swap 不引入新概念，纯粹考验"正确绑定"——正是你定义的核心能力
3. **模型性能与 ImageNet zero-shot 准确率正相关**（r>0.8），暗示组合推理能力与整体视觉理解能力耦合

### 2.3 CREPE

- **论文**：CREPE: Can Vision-Language Foundation Models Reason Compositionally?（arXiv:2212.07796，CVPR 2023，引用 287+）
- **定位**：大规模组合评测基准，评测认知科学中组合性的两个核心方面：
  - **系统性（Systematicity）**：理解"见过的基本单元的新组合"的能力
  - **生产力（Productivity）**：理解"从未见过的单元组合"的能力

**规模与评测方式**：
- **系统性（Systematicity）**：37 万+ 图文对，三个 seen-unseen splits（分别针对 CC-12M、YFCC-15M、LAION-400M 训练数据设计），含 32.5 万/31.6 万/30.9 万 hard negative 描述。发现：新组合占主导时模型性能一致下降，Recall@1 最多降 12%
- **生产力（Productivity）**：1.7 万图文对、九种不同复杂度，含 18.3 万 hard negatives（atomic、swapping、negation 三种 foil 类型）。发现：检索成功率随复杂度增加而衰减，高复杂度时接近随机水平
- 数据来源：复用 Visual Genome 场景图和区域描述，用人工模板和 GPT-3 生成
- 结论：7 种架构 × 4 种训练算法，无论模型和训练数据规模大小，都表现出组合性缺陷

**与 SugarCrepe 的关系**：SugarCrepe 指出 CREPE 等程序化生成基准存在可 hack 漏洞，其 hard negatives 可通过语言先验分辨；但 SugarCrepe 的评测结果与 CREPE 高度一致（物体>属性>关系），交叉验证了失败模式的真实性。

### 2.4 ARO

- **论文**：When and why vision-language models behave like bags-of-words, and what to do about it?（arXiv:2210.01936，ICLR 2023 Oral（前 5%），引用 797+）
- **定位**：系统评测 VLM 对三种组合结构的理解，规模为**5 万+ 测试用例**（比此前组合评测基准大几个数量级），由三个子集构成：
  - **Visual Genome Attribution（属性）**：测试物体属性绑定（"红色杯子" vs 图中有多个物体时属性是否绑对）
  - **Visual Genome Relation（关系）**：测试物体间关系理解（"猫在狗上面" vs "狗在猫上面"）
  - **COCO & Flickr30k-Order（顺序）**：测试词序敏感性（"人骑大象" vs "大象骑人"）
- **核心发现**：VLM 类似 **bag-of-words（词袋模型）**——对词序和组合结构不敏感。论文进一步证明：**在现有检索基准上不利用组合/顺序信息也能表现良好**（因为对比预训练优化的检索任务存在 shortcut），这解释了为什么模型不需要学习组合表示
- **提出的解决方案**：composition-aware hard negative mining（组合感知的困难负样本挖掘），简单修改对比学习即可显著提升顺序和组合性任务表现

### 小结：组合推理的评测维度与失败模式

| 基准 | 子任务维度 | 评测方式 | 关键发现 |
|------|-----------|---------|---------|
| VALSE | 存在性/复数/计数/空间关系/动作/实体共指 | 真假判断（foiled instances） | 复数、空间关系、共指、动作上挣扎 |
| SugarCrepe | 物体/属性/关系 × Replace/Swap/Add | 二选一检索 | 属性关系弱于物体；Swap 最难 |
| CREPE | 系统性/生产力 | 检索（seen-unseen splits + 复杂度梯度） | 新组合主导时 Recall@1 降 12%；高复杂度接近随机 |
| ARO | 属性/关系/顺序 | 检索（5 万+ 用例） | VLM 是词袋模型；不利用组合信息也能通过现有基准 |

**对论文的启示**：
1. **组合推理可操作化为三个子问题**：属性绑定（attribute binding）、空间/逻辑关系（relation）、词序/结构（order）——你的论文分析可以沿此展开
2. **评测方式的差异本身是论文 Discussion 的素材**：不同论文用不同基准（VALSE/SugarCrepe/CREPE/ARO），结果难以直接对比——这就是"benchmark 碎片化"问题
3. **Swap 任务 = 纯绑定测试**：SugarCrepe 的 Swap 形式（同类别概念交换）是最纯粹的"组合正确性"测试，可用来评估"奖励信号是否触及组合理解"

---

## 三、GRPO 算法与多模态应用

### 3.1 GRPO 核心原理

- **原始论文**：DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models（arXiv:2402.03300，引用 7475+）
- **定位**：PPO 的变体，DeepSeek-R1 的训练核心，RLVR（RL with Verifiable Rewards）路线的代表算法

**核心思想**：
- 对同一个问题采样 **G 个回答**（一组），用**组内相对优势**代替 PPO 的 value network
- 优势计算：\(a_i = (r_i - \bar{r}) / \sigma_r\)——该回答的奖励相对于组内均值的归一化偏离
- **去掉了 critic/value network**，大幅降低内存和训练复杂度
- 奖励通常来自**确定性规则验证器**（如数学答案比对），不需要训练 reward model

**GRPO vs PPO 关键区别**：

| 维度 | PPO | GRPO |
|------|-----|------|
| 基线 | 需要单独训练的 value network（critic） | 无 critic，用组内均值做基线 |
| 奖励来源 | reward model（通常需训练） | 规则/验证器（可确定性计算） |
| 内存 | 高（policy + value 两个模型） | 低（只有 policy） |
| 奖励信号类型 | 可以是任何分数 | 最适合可验证奖励（verifiable rewards） |

### 3.2 GRPO 在多模态场景的适配

GRPO 直接迁移到多模态会遇到问题（这也是你论文中 H-GRPO、Ground-R1 等工作的动机）：
- **文本偏置（Text-bias）**：MLLM 可能忽略真实图像，仅凭文本提示"脑补"答案——GRPO 的结果级规则奖励无法察觉这一点（H-GRPO 专门解决此问题）
- **视觉 grounding 缺失**：奖励只验证最终答案，不验证"模型是否真的看了图、看了正确的区域"（Ground-R1 的动机）
- **奖励可验证性下降**：数学有确定答案，但组合推理的"正确性"没有唯一标准答案——这是 GRPO 应用于组合推理的最大障碍

### 3.3 "GRPO is Secretly a PRM" 理论分析

- **论文**：GRPO is Secretly a Process Reward Model（arXiv:2509.21154，Sullivan & Koller, 2025）
- **核心理论结果**：在 token 级 policy gradient + 单次更新（μ=1）的设定下，**标准 GRPO 目标函数与一个 PRM-aware 目标函数数学等价**。

**证明要点**：
1. 组内 G 个轨迹（trajectories）的**共享前缀**自然定义了"过程步骤"（process sets）
2. 对共享前缀内每个 token 赋予该前缀下所有轨迹的平均奖励 \(r_{mean}(\lambda)\)，可构造出 PRM-aware loss
3. 该 loss 与标准 GRPO loss **逐项数学相等**——GRPO 一直在隐式地做细粒度 credit assignment

**经验验证**：
- 在 Qwen 数学推理微调中，随着训练推进，组内共享前缀结构越来越丰富（组大小 36 时几乎 100% 的组存在非平凡过程结构）
- 模型收敛后倾向于为同一问题生成相似的高质量前缀——隐式 PRM 真实存在且活跃

**暴露的缺陷（Process Step Frequency Flaw）**：
- 标准 GRPO 中，某个过程步骤对梯度的贡献与其频率 \(|\lambda|\) 成正比
- **抑制探索**：高频前缀有微正优势时被放大强化，模型可能过早收敛到次优路径
- **阻碍利用**：有价值轨迹若与低奖励轨迹共享前缀，平均优势可能为负，被连带惩罚
- 修复方案：**λ-GRPO**——用逆频率 \(|\lambda|^{-1}\) 缩放每个 token 的贡献，平衡过程步骤影响力。实验显示 λ-GRPO 在 75% 的基准上优于标准 GRPO，平均提升约 10%，且收敛更快

### 小结：对奖励信号演进的启示

1. **GRPO 与 PRM 不是两条独立路线，而是同一谱系**——GRPO 隐式地做过程级 credit assignment。这支持你论文的 thesis：奖励信号演进是一个连续谱，不是离散类别
2. **但 GRPO 的隐式 PRM 是基于"答案正确性的共享前缀"，不是基于"视觉语义结构"**——在组合推理场景中，共享前缀可能来自文本模式而非真正的视觉组合理解，这可能是 GRPO 在多模态组合推理上需要显式视觉对齐奖励（Ground-R1、GRIT、POLIA）的原因
3. **奖励的可验证性是核心约束**：数学→可自动验证；组合推理→难以自动验证，这是"结果验证→结构验证→视觉对齐→过程对齐"演进的驱动力

---

## 附：本次调研涉及的核心文献清单

| # | 论文 | arXiv ID | 类别 |
|---|------|----------|------|
| 1 | Aligning Large Multimodal Models with Factually Augmented RLHF (LLaVA-RLHF) | 2309.14525 | RLHF |
| 2 | RLHF-V: Towards Trustworthy MLLMs via Behavior Alignment from Fine-grained Correctional Human Feedback | 2312.00849 | RLHF/DPO |
| 3 | Aligning Large Vision-Language Models with AI Feedback (Silkie) | 2410.09421 | RLAIF |
| 4 | VALSE: A Task-Independent Benchmark for Vision and Language Models | 2112.07566 | Benchmark |
| 5 | SugarCrepe: Fixing Hackable Benchmarks for Vision-Language Compositionality | 2306.14610 | Benchmark |
| 6 | CREPE: Can Vision-Language Foundation Models Reason Compositionally? | 2212.07796 | Benchmark |
| 7 | When and why vision-language models behave like bags-of-words (ARO) | 2210.01936 | Benchmark |
| 8 | DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models (GRPO) | 2402.03300 | RL 算法 |
| 9 | GRPO is Secretly a Process Reward Model | 2509.21154 | RL 理论 |
