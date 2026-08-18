# Ground-R1: Thinking with Images via Scale Relative Policy Optimization

> Ground-R1：用"尺度相对策略优化"（SRPO）让模型真正看着图思考（MBZUAI + 北大 + 中科大 + 中山大学，arXiv v3 2026-02）
>
> 注意：本文概括基于 arXiv 最新版（v3，2026-02-03，标题与方法均已改版），早期版本（v1）使用两阶段 GRPO，与本文内容不同。

## 这篇论文到底在解决什么问题？

**大视觉语言模型（LVLM）的答案不可靠、也不可解释。** 模型经常靠预训练数据里的虚假相关（spurious correlation）猜答案，而不是真正去看图里相关的证据区域——你说"图片里哪辆车离相机更近"，它可能瞥一眼大片的显著区域就猜一个答案，根本没定位到关键的小细节。

为此，"thinking with images"（带着图像思考）范式要求模型显式地把推理锚定到图像证据区域（输出 `<think>` 推理 + `<box>` 证据框 + `<answer>` 答案）。**但论文用实验诊断出一个系统性的缺陷——尺度驱动偏差（scale-driven bias）**：

- **大区域主导训练奖励**：论文跟踪训练中不同尺度证据区域的奖励轨迹（小/中/大区域按相对面积 <10%、10%~30%、>30% 划分），发现大区域一直拿更高奖励，小但语义关键的证据获得持续负优势，梯度被抑制甚至被裁剪。
- **根因在 vanilla GRPO 的归一化方式**：GRPO 在全体 rollout 上做全局优势归一化，大框天然得到更高奖励（"框得越大越容易蒙对"），小框即使关键也被压低。训练越久，策略越偏好大而显著的框，产生**探索崩溃（exploration collapse）**——不再去看小但可能关键的区域。
- 结果就是：推理时模型偏好视觉显著的大物体，忽略小却关键的证据，grounding 是虚假的。

**这篇论文想干什么？** 提出 Ground-R1：用一个新的优化目标 **SRPO（Scale Relative Policy Optimization，尺度相对策略优化）** 替换标准 GRPO，按证据区域尺度重校准奖励分配，让模型学会聚焦小但关键的证据。全程只靠"问题-答案对"监督，不需要额外的框标注来训练 grounding（框是模型自己输出的）。

## 他们怎么做的？

**核心 idea：保留"找证据→放大看图→作答"的两阶段 rollout 结构，但把 GRPO 的全局归一化改成"按区域尺度分箱（bin）的尺度感知归一化"——同一尺度桶内比较（intra-bin），再跨桶做判别（inter-bin），消除大区域对奖励的垄断。** 技术流派：GRPO 的尺度感知变体（SRPO）+ 两阶段 rollout 的 thinking-with-images 范式。

### 第一步：两阶段 rollout（Grounding + Answer）

给定问题 q 和图像 v，模型先从当前策略 π_θold 采样 G1=4 条 grounding rollouts，每条输出一个证据框 b_i ∈ ℝ⁴（轴对齐 bbox，左上/右下角坐标）：

$$ \boldsymbol{b} = \{\boldsymbol{b}_i\}_{i=1}^{G_1} \sim \pi_{\theta_{\text{old}}}(\cdot \mid \boldsymbol{q}, \boldsymbol{v}), \quad G_1 = 4 $$

提示词要求模型把推理写在 `<think>` 标签里、bbox 坐标以 `[x1,y1,x2,y2]` 格式写在 `<box>` 标签里（可多轮细化）。把每个证据框 b_i 裁剪出局部图像区域 e_i，与原图 + 问题一起送回模型，采样 G2=2 条 answer rollouts：

$$ \boldsymbol{o}_i = \{\boldsymbol{o}_{i,j}\}_{j=1}^{G_2} \sim \pi_{\theta_{\text{old}}}(\cdot \mid \boldsymbol{q}, \boldsymbol{v}, \boldsymbol{e}_i), \quad G_2 = 2 $$

每个证据框产出 2 条答案轨迹，共 G1·G2 = 8 条推理轨迹。

### 第二步：SRPO 核心（关键机制，分四步）

**① 证据区域离散化（Evidence Region Discretization）。** 按证据区域的相对面积 a_i（区域面积/图像面积）把所有 rollout 分成 K=3 个等大小桶（scale bins）：

$$ s(i) = \min(\lfloor K a_i \rfloor + 1, K) \in \{1, \ldots, K\} $$

s(i) 是第 i 条证据区域的桶号。这样大框、中框、小框各归各桶，不再混在一起比。

**② 奖励打分：intra-bin + inter-bin 两个分量。**

- **Intra-bin reward（桶内奖励）**：与普通奖励相同，由格式奖励（`<think>`/`<box>`/`<answer>` 标签合规）+ 答案奖励组成。答案奖励按题型自适应：多选题 → 精确匹配（二元 0/1）；开放题 → 与 GT 的 ROUGE-1/2/L 平均分（词法对齐）。每个桶 S_k 单独计算自身奖励的均值 µ_k 和标准差 σ_k。
- **Inter-bin reward（桶间奖励）**：只有平均奖励最高的桶（argmax_k µ_k）内的 rollout 得 1，其余桶得 0：

$$ r^{\text{inter}}_{i,j} = \begin{cases} 1, & \text{if } s(i) = \arg\max_{k \in \{1,\ldots,K\}} \mu_k \\ 0, & \text{otherwise} \end{cases} $$

这逼模型跨尺度做判别性比较——只有当某个尺度的证据真的最有效（平均奖励最高）时，它才拿桶间奖励。

**③ 尺度感知优势估计（Scale-aware Advantage Estimation）。** 这是 SRPO 的核心公式：

$$ A_{i,j} = \underbrace{\frac{r^{\text{intra}}_{i,j} - \mu_{s(i)}}{\sigma_{s(i)}}}_{\text{桶内归一化}} + \underbrace{\frac{r^{\text{inter}}_{i,j} - \text{mean}(r^{\text{inter}})}{\text{std}(r^{\text{inter}})}}_{\text{全局归一化}} $$

- 第一项：桶内归一化——用自己的桶的 µ_k/σ_k 归一化，保证同尺度内公平比较（小框在小框里比，不再被大框碾压）；
- 第二项：桶间奖励的全局归一化——保留跨尺度的判别信号。

对比标准 GRPO 的全局归一化（所有 rollout 一起归一化，大框天然占优），SRPO 让每个尺度的证据都有机会拿到正优势。

**④ 优化目标**：标准 PPO 式 clip 目标 + KL 散度惩罚：

$$ J(\theta) = \mathbb{E}\left[ \frac{1}{G_1 G_2} \sum_{i,j} \min\left(\rho_{i,j}(\theta) A_{i,j},\ \text{clip}(\rho_{i,j}(\theta), 1-\varepsilon, 1+\varepsilon) A_{i,j}\right) \right] - \beta D_{KL}(\pi_\theta \| \pi_{\text{ref}}) $$

### 第三步：训练配置

- **数据**：DeepEyes 引入的 RL 训练数据（fine-grained visual search、arXivQA、ThinkLite-VL 等），**无 SFT 冷启动**（刻意不用 curated SFT 数据，避免改变基座模型的 grounding 行为）；
- **基座**：Qwen2.5-VL-7B-Instruct；
- **训练**：1000 步、batch size 8、学习率 1e-6、采样温度 1、最大输出 512 tokens、K=3；
- **算力**：8×H100，约 12 小时。

### 与同类方法的区别

和 Vision-R1 / LMM-R1 等 R1 系列相比，Ground-R1 的 grounding 证据框是显式的（两阶段 rollout + 放大看图），且优化目标不是 vanilla GRPO 而是 SRPO——**这是第一篇诊断并修复"大区域主导奖励"偏差的工作**；和 DeepEyes / Mini-o3 等 thinking-with-images 方法相比，它们都建在 vanilla GRPO 上，同样受 scale-driven bias 影响。

## 效果怎么样？

### 对基座的提升（Qwen2.5-VL-7B → Ground-R1）

- 通用基准全面超越：MME +83.4、MME-RealWorld-Lite +17.1%、RealWorldQA +2.9%、POPE +6.2%、MM-Vet +2.7%、SEED-Bench +1.3%；
- 高分辨率基准（小物体多、最吃 grounding）：V* +11.9%、HR-4K +6.8%、HR-8K +8.4%——高分辨率场景收益最大，因为关键证据往往只占很小空间范围；
- 视觉 grounding：RefCOCO val 达 93.1%，接近专用 grounding 模型（Grounding DINO），缩小了通用模型与专用模型的差距。

### SRPO vs 标准 GRPO（核心对比）

- **SRPO 带来稳定增益**：V* +2.1%、HR-4K +1.2%、HR-8K +1.8%；
- **grounding 质量显著更高**：训练中 grounding IoU 曲线明显高于 GRPO，差距在约 600 步后拉大——GRPO 出现探索崩溃（策略锁定在大而显著的框上），SRPO 持续改进；
- **定性对比**：GRPO 版 Ground-R1 会把证据框放在包含多栋房子的大片显著区域上然后给不确定/错误答案；SRPO 版聚焦银车所在的小区域，利用相对大小线索正确判断"哪辆车离相机更近"。

### 消融结论

- **RL > SFT**（V* 上 +14.1% 绝对提升）；
- **grounding-then-answering > 直接作答**（去掉 grounding 阶段的 Vanilla-R1 全面落后）；
- **intra-bin 和 inter-bin 缺一不可**：只用 intra-bin（Ground-R1-Intra）退化最明显——桶内归一化不足以区分跨尺度的证据；只用 inter-bin（Ground-R1-Inter）也低于完整版。

**局限性**：① 依赖 region proposals 的质量——遮挡或视觉模糊的对象，证据框仍可能定位不准；② 评测限于既有基准，开放世界、长尾、域偏移场景下的表现与 grounding 保真度尚未探索。

## 对谁有用？

- 做 **grounded reasoning、thinking-with-images、减少幻觉** 的研究者——"尺度感知奖励归一化"是修复 RL 系统性偏差的完整案例；
- 做 **RLVR 奖励设计** 的人——它揭示了一个被忽视的陷阱：GRPO 的全局归一化天然偏袒"大而显著"的中间产物，任何有结构化中间输出的 RL 都可能踩坑，SRPO 的分箱归一化思路可以迁移；
- 写综述时它是"视觉对齐奖励"方向的重要一环：对齐对象从"答案"变成了"证据区域"，且对齐的公平性（不同尺度证据）第一次被显式处理。

## 原文信息

- 来源：arXiv
- 链接：https://arxiv.org/abs/2505.20272
- 作者：Meng Cao, Haoze Zhao, Can Zhang, Xiaojun Chang, Ian Reid, Xiaodan Liang
- 发表时间：2025 年 5 月首版；本文基于 2026 年 2 月 3 日 v3 版（arXiv:2505.20272v3）
- 对应 PDF：papers/grounded/ground-r1-incentivizing-grounded-visual-reasoning.pdf
