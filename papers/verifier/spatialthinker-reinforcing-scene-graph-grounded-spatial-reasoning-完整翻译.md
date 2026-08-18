# SpatialThinker: Reinforcing Scene Graph-Grounded Spatial Reasoning via Dense Rewards

> **SpatialThinker：通过稠密奖励强化基于场景图的空间推理**（完整中文翻译）
>
> - 作者：Hunar Batra¹、Haoqin Tu²、Hardy Chen²、Yuanze Lin¹、Cihang Xie²、Ronald Clark¹
> - 机构：¹University of Oxford（牛津大学）、²University of California, Santa Cruz（加州大学圣克鲁兹分校）
> - arXiv:2511.07403v2 [cs.CV]，2026 年 7 月 2 日
> - 对应 PDF：`spatialthinker-reinforcing-scene-graph-grounded-spatial-reasoning.pdf`

---

## 摘要

多模态大语言模型（MLLMs）在视觉-语言任务上取得了显著进展，但在空间推理方面仍然吃力。现有的空间 MLLMs 依赖大规模数据集、显式 3D 输入、架构特定修改，或提供不足指导的稀疏强化学习（RL）方法。我们提出 **SpatialThinker**。据我们所知，它是第一个通过在线 RL 将场景图生成（Scene Graph Generation, SGG）与视觉推理统一在单次前向过程中的 MLLM。该模型通过构建由任务相关对象和关系组成的"心理场景图"来模拟类人的空间感知，并借助稠密空间奖励推理出答案。我们的贡献有三点：

1. **基于 SGG 的接地推理**：将 SGG 直接集成到推理链中，而不是作为独立的预处理步骤；
2. **STVQA-7K**：通过可扩展的合成管线构建的高质量空间 VQA 训练数据集；
3. **稠密空间奖励设计**：在 RL 过程中强制结构化接地，并能泛化以改善广泛的视觉感知。

SpatialThinker-7B 相比 SFT 取得 **3.6 倍**的性能增益，相比稀疏 RL 在分布内与分布外泛化上提升 **1.7 倍**。仅用 7K 样本训练，SpatialThinker-7B 即可匹敌 GPT-5 并超越 GPT-4o；SpatialThinker-30B 在 14 个空间与真实世界基准上的平均值超越 GPT-5 和 Claude 4 Sonnet。这证明：**结构化的空间接地 + 奖励对齐的推理，能用有限数据带来稳健的空间理解**。

---

## 1 引言

空间推理是人类智能的核心，它使我们能够在复杂环境中感知、定位和操纵物体——这一能力对具身 AI 任务至关重要，如机器人操作（Intelligence et al., 2025; Gao et al., 2023; Nasiriany et al., 2024）、导航（Huang et al., 2022）和增强现实（Konenkov et al., 2024），这些场景中精确的空间意识是真实部署的前提（Driess et al., 2023; Team et al., 2025）。

虽然 MLLM 在视觉-语言任务上快速进步（Hurst et al., 2024; Lin et al., 2024; Deitke et al., 2025; Bai et al., 2025b; Du et al., 2025; Liu et al., 2023; Google, 2025），但它们在空间理解上仍然困难，尤其是在 3D 空间——这需要捕捉超越 2D 投影的几何、结构和关系（Chen et al., 2024a; Tong et al., 2024b; Kamath et al., 2023; Yang et al., 2025a; Tong et al., 2024a; Ma et al., 2024b）。

**现有方法及其不足。** 现有方法通过以下途径应对：从 3D 场景图大规模合成数据（Chen et al., 2024a; Ma et al., 2025b; Daxberger et al., 2025; Cheng et al., 2024）、辅助空间 token 或架构修改（Hong et al., 2023b; Ma et al., 2025b）、或显式 3D 输入如深度图和点云（Hong et al., 2023c; Cheng et al., 2024; Cai et al., 2024）。一个常见模式是把场景图当作**离线数据整理的预处理工具**：SpatialRGPT 从点云构建 3D 场景图生成 700K 训练样本（Cheng et al., 2024），SpatialVLM 与 SpatialLLM 分别依赖场景图派生的标注在 2B 与 1M 样本上监督训练（Chen et al., 2024a; Ma et al., 2025b）。这导致数据密集型的管线，要么需要海量规模，要么需要架构特定修改。

最近，RLVR（基于可验证奖励的强化学习）通过学习多样化推理策略而非静态模式，展现出优于 SFT 的泛化能力（DeepSeek-AI et al., 2025; Shen et al., 2025b; Gandhi et al., 2025）。然而，现有用于空间推理的 RLVR 方法采用**仅基于正确率的简单奖励**，无法为视觉接地推理提供足够指导（Shen et al., 2025a; Xiao et al., 2025; Ma et al., 2025a; Wang & Ling, 2025; Xia et al., 2025; Zhu et al., 2025）。与此同时，场景图能为视觉推理提供天然的结构指导（Hildebrandt et al., 2020; Wald et al., 2020），但现有方法要么把它当作外部预处理管线用于数据整理（Kim et al., 2024; Chen et al., 2023; Li et al., 2024c），要么当作与下游推理脱节的孤立生成目标（Chen et al., 2025c; Li et al., 2025），从未将其端到端集成进推理过程本身。

**我们的方案。** 我们提出 **SpatialThinker**——据我们所知，第一个通过在线 RL 统一场景图生成（SGG）与视觉推理的 MLLM。它不是把 SGG 当作脱节的预处理步骤，而是将场景图构建直接集成进推理链：构造**感兴趣区域场景图（region-of-interest scene graphs）**，捕捉任务相关的对象、空间关系与局部化坐标，并基于这些结构化表示推理出答案。

训练采用**带词典序门控（lexicographic ordering）的多目标奖励**：
- **格式奖励**强制结构化推理；
- **数量惩罚**（count penalties）调节区域聚焦；
- **正确率奖励**优先保证答案正确；
- **空间奖励**鼓励精确定位。

这促进类人的推理过程：**观察（observe）→ 定位（localize）→ 思考（think）→ 作答（answer）**。其中 2D 接地告诉模型"物体在哪里"，3D 关系谓词告诉模型"物体在世界上如何摆放"，映照了人类感知场景时形成的心理草图。

**主要结果。** SpatialThinker-7B 仅用合成数据集 STVQA-7K 中的 7K 样本训练，在 14 个基准上超越 SFT（+5.5%）与常规 RL 基线（+3.2%），超越 GPT-4o（平均 +4.7%）、Claude 3.5 Sonnet（+9.6%）与 Claude 4 Sonnet（+1.8%），同时匹敌 GPT-5（平均 −0.9%）。纯稀疏 RL 只将基座模型提升 +4.4%，而我们的稠密空间奖励达到 +7.7%——**将近翻倍（×1.7）了 RL 的收益**。关键的是，稀疏 RL 在 OOD 真实世界 VQA 上只是追平 SFT（+2.7% vs. +2.9%），而 SpatialThinker 达到 +5.2%，证实仅靠正确率奖励无法改善对通用视觉感知任务的泛化。将同一配方扩展到 30B，SpatialThinker-30B 取得最佳整体平均，超越 GPT-5（+3.0%）和 Claude 4 Sonnet（+5.8%），并在 CV-Bench 3D 上达到 93.6%（比 GPT-5 高 +3.3%）。

**主要贡献：**

- 提出 **SpatialThinker**——据我们所知第一个通过在线 RL 在单次前向中统一 SGG 与视觉推理生成的 MLLM，使模型能同时感知空间结构并推理；仅用 7K 训练样本就达到强性能，而现有空间 MLLM 使用数十万到数十亿样本。
- 引入 **STVQA-7K**——基于场景图标注的高质量空间 VQA 训练数据集，配套可扩展的数据生成管线（可扩展到 108K 样本），并用**双 LLM 校验**保证质量。
- 设计**稠密的、词典序门控的多目标奖励**，指导区域聚焦的空间推理，并泛化到空间任务之外改善广泛视觉感知；在空间、通用 VQA 与真实世界基准上取得更优的分布内/分布外泛化，超越常规 RL 与 SFT 基线、开源通用与空间 MLLM 以及闭源模型。我们发布 3B、7B、30B 三个规模的 SpatialThinker，其中 SpatialThinker-30B 在 14 个基准上平均超越 GPT-5 与 Claude 4 Sonnet 等 SOTA 闭源模型。

---

## 2 预备知识

### 场景图生成（SGG）

场景图将图像 I 表示为有向图 G = (V, E) 的结构化表示。每个节点 $v_i \in V$ 表示一个对象，带有类别标签 $c_i$ 和 2D 边界框 $b_i = (x_1, y_1, x_2, y_2)$；每条边 $e_{ij} \in E$ 是一个关系三元组 $\langle v_i, r_{ij}, v_j \rangle$，由主语 $v_i$、谓词 $r_{ij}$ 和宾语 $v_j$ 组成，捕捉空间或交互关系（如 left of、on、under）（Hildebrandt et al., 2020; Wald et al., 2020）。

经典 SGG 将预测分解为对象检测与关系识别（Carion et al., 2020; Cong et al., 2023），开放词表方法则利用语言或视觉先验超越固定本体泛化（Chen et al., 2024b; Li et al., 2023）。我们把**面向问题的场景子图**记为 $G_q = (V_q, E_q) \subseteq G$，只保留与给定查询 q 相关的对象和关系。

### MLLM 中的推理

MLLM 旨在解决定义在多模态实例数据集 D 上的推理任务 $(x_{img}, x_{text}, y^*)$，其中 $x_{img}$ 是视觉输入，$x_{text}$ 是自然语言查询，$y^*$ 是标准答案。我们将 MLLM 建模为自回归策略 $\pi_\theta$，输出轨迹 $y = (s_1, \dots, s_T, a)$，由推理步骤 $s_t$ 和最终答案 a 组成。策略分解为：

$$
\pi_\theta(y | x_{img}, x_{text}) = \left( \prod_{t=1}^{T} \pi_\theta(s_t | x_{img}, x_{text}, s_{<t}) \right) \cdot \pi_\theta(a | x_{img}, x_{text}, s_{\le T}) \tag{1}
$$

监督微调（SFT）能模仿参考推理轨迹，但常在分布外（OOD）泛化上挣扎。强化学习（RL）则用显式奖励信号优化推理轨迹，提升鲁棒性（Gandhi et al., 2025; DeepSeek-AI et al., 2025; Huang et al., 2025）。RL 目标为：

$$
\max_\theta \mathbb{E}_{(x_{img}, x_{text}, y^*) \sim D,\ y \sim \pi_\theta} [R(y)]
$$

其中 $R(y)$ 基于格式符合度、对象数量、答案正确性与空间定位来评估轨迹。

---

## 3 SpatialThinker：基于场景图接地的空间推理 MLLM

### 3.0 任务定义

我们将 MLLM 中的空间推理定义为：为查询 Q = {x_img, x_text} 生成视觉接地响应 y。与通用推理不同，我们的公式**明确要求构建面向问题的场景子图 $G_q$**，并基于对象、边界框与关系进行推理。策略 $\pi_\theta$ 在 STVQA-7K（§3.3）的空间接地 VQA 样本上训练，使用我们的多目标空间奖励设计 R（§3.1），奖励的校验基于数据集中的标准场景图。这强制了结构有效性、数量保真、答案准确性与精确空间接地。

### 3.1 多目标奖励设计

与先前仅用稀疏最终答案奖励的 RLVR 方法不同（Peng et al., 2025; Zhu et al., 2025; Shen et al., 2025b），我们的稠密奖励设计将**词典序门控**与四个分量结合：**格式、数量、正确率与空间奖励**。奖励设计过程（含消融与动机）详见附录 C。

**格式奖励（Format Reward）。** 强制视觉接地且结构化的推理模板：`<observe>` 用于场景描述、`<scene>` 用于包含对象/边界框/关系的区域场景图、`<think>` 用于显式推理、`<answer>` 用于最终输出。除标签存在性外，格式奖励还验证 `<scene>` 内的 JSON：(1) 可解析；(2) 每个对象包含必填字段（ID 与边界框）；(3) 所有关系是有效的主语-谓词-宾语三元组。这鼓励顺序接地：感知 → 定位 → 推理 → 作答。奖励 $R_f \in \{0, 1\}$，权重 $w_{format} = 0.1$。

**正确率奖励（Accuracy Reward）。** 为优先任务表现，定义二元正确率奖励 $R_a$：模型预测答案与标准答案**精确字符串匹配**（依托多选题格式）。该分量权重最高（$w_{accuracy} = 0.5$），直接激励正确的最终预测，其余奖励则塑造模型"如何"得出正确答案。

**数量奖励（Count Reward）。** 鼓励模型预测与查询相关的恰当数量的对象与关系，同时惩罚欠生成与过生成，基于两者预测数量与标准数量的偏差：

$$
R_{count} = w_{count} \cdot \left[ \lambda_{obj} \cdot \max\left(0, 1 - \frac{|N^{pred}_{obj} - N^{gt}_{obj}|}{\max(N^{gt}_{obj}, 1)}\right) + \lambda_{rel} \cdot \max\left(0, 1 - \frac{|N^{pred}_{rel} - N^{gt}_{rel}|}{\max(N^{gt}_{rel}, 1)}\right) \right]
$$

其中 $N^{pred}$ 与 $N^{gt}$ 分别表示预测与标准数量，$w_{count} = 0.2$ 是整体数量奖励权重，$\lambda_{obj} = 0.7$、$\lambda_{rel} = 0.3$。这引导模型聚焦于与问题相关的区域。没有它，我们发现模型会**通过生成过量对象和关系来最大化随机匹配，从而博弈空间奖励——这是一种 reward hacking**。

**空间奖励（Spatial Reward）。** 为监督对象定位，空间奖励**只在最终答案正确时计算**。预测与标准对象用匈牙利算法（Hungarian algorithm）做二分匹配，代价函数结合 Complete IoU（CIoU）与语义相似度：

$$
C(o^{pred}_i, o^{gt}_j) = \lambda_{spatial} (1 - \text{IoU}(b_i, b_j)) + \lambda_{semantic} (1 - \text{sim}(l_i, l_j)) \tag{2}
$$

其中 b 与 l 分别表示边界框与标签，$\lambda_{spatial} = 1.0$，$\lambda_{semantic} = 2.0$。奖励为匹配对上的平均 CIoU：

$$
R_{spatial} = w_{spatial} \cdot \left( \frac{1}{|M|} \sum_{(i,j) \in M} \text{CIoU}(b^{pred}_i, b^{gt}_j) \right)
$$

其中 $w_{spatial} = 0.2$。CIoU 相比 IoU 提供更稠密的监督：即使框不重叠，它也通过中心距离与长宽比项给出非零梯度（Zheng et al., 2020）。虽然是在 2D 中计算，这些接地信号与 3D 关联的关系结合，促进了 3D 一致的空间推理。

**词典序门控（Lexicographic Gating）。** 应用带条件门控的词典序（Skalse et al., 2022），优先级为 **format ≻ {count, accuracy} ≻ spatial**。模型必须先满足格式，然后联合优化数量与正确率，且只有答案正确时才获得空间奖励。这确保空间接地强化有效推理，并使模型对不完美的中间场景图保持鲁棒。没有正确率门控，模型会**过度优化中间空间奖励而牺牲最终答案正确性**。最终奖励如下（$I[\cdot]$ 为指示函数）：

$$
R_{total} = I[R_{format} = 1] \cdot \left( w_{format} R_f + w_{count} R_c + w_{accuracy} R_a I[R_{accuracy} = 1] w_{spatial} R_s \right) \tag{3}
$$

### 3.2 在线 RL 策略优化

采用 **Group-Relative Policy Optimization（GRPO）**（DeepSeek-AI et al., 2025; Shao et al., 2024）训练——一种无需 critic 网络、通过组内比较估计优势的在线 RL 方法。给定输入 x，从当前策略 $\pi_{\theta_{old}}$ 采样 N 条轨迹 $\{y^{(1)}, \dots, y^{(N)}\}$。每条响应用我们的稠密空间奖励函数（§3.1）打分，优势用组归一化分数计算：

$$
A^{(i)} = \frac{r^{(i)} - \mu}{\sigma + \varepsilon}
$$

其中 $\mu$、$\sigma$ 为组均值与标准差，$\varepsilon = 10^{-6}$。然后使用带 KL 正则的 PPO 式裁剪损失更新策略：

$$
\mathcal{L}_{RL}(\theta) = -\frac{1}{G} \sum_{i=1}^{G} \frac{1}{|y^{(i)}|} \sum_{t=1}^{|y^{(i)}|} \left[ \min\left(r_{i,t} A^{(i)}, \text{clip}(r_{i,t}, 1 - \epsilon_l, 1 + \epsilon_h) A^{(i)}\right) - \beta D^{KL}_{i,t} \right] \tag{4}
$$

其中 $r_{i,t} = \frac{\pi_\theta(y^{(i)}_t | x, y^{(i)}_{<t})}{\pi_{\theta_{old}}(y^{(i)}_t | x, y^{(i)}_{<t})}$ 是新旧策略的重要性比率，$D^{KL}_{i,t}$ 是相对参考模型的 token 级 KL 散度。超参数 $\epsilon_l = 0.2$、$\epsilon_h = 0.3$、$\beta = 10^{-2}$。该目标在从稠密空间奖励学习的同时约束策略发散，保证稳定与泛化。

### 3.3 STVQA-7K：数据集构建

为支持奖励对齐的空间推理，我们构建 **STVQA-7K**——基于 Visual Genome（Krishna et al., 2017）人工标注场景图合成的视觉问答（VQA）数据集。STVQA-7K 包含 **7,587 个空间接地的多选题 VQA 对**，覆盖 2D 与 3D 空间理解，涵盖九类核心推理：关系、大小、朝向、距离、深度、可达性、位置、数量与存在性。

我们在原 VG150 谓词集（50 个标准谓词）基础上**新增 34 个空间关系谓词**——覆盖距离（如 near、far）、大小（如 bigger、taller）、朝向（如 facing away）与包含（如 inside、beneath）——丰富关系词汇。从这些场景图生成 3D 推理 VQA，例如深度："哪个离相机更近？"、朝向："从这个人视角看，狗在哪个方向？"

**问题生成。** 每个 QA 对由 Claude Sonnet 4（Anthropic, 2025）从场景图生成，并评定难度与质量（满分 10 分）。

**双 LLM 质量过滤。** 为缓解 LLM 生成问题的潜在偏差，应用**基于一致性的双 LLM 过滤管线**：Claude Sonnet 4 生成 QA 对，GPT-4o（Hurst et al., 2024）用 pass@2 一致性校验。跨模型校验带来 **+13% 的准确率提升**（表 5），确认双 LLM 校验保留了高质量样本。从最初 **56,224 个问题**中，按评分、难度与校验保留**前 7,587 个**样本（训练 6,895 / 验证 692，约 75% 保留率）。

**场景图适配（区域对齐）。** 为使推理区域特定化，通过**词形还原的关键词匹配**提取每问相关对象与关系，构建与问题对齐的场景子图作为局部监督。这帮助模型学习在复杂场景中"聚焦哪里"。边界框坐标保留**绝对像素空间**以保持真实尺度，供 CIoU 奖励训练使用。

**可扩展性。** 管线可扩展到约 **108K 样本**（Visual Genome 上限），支持未来大规模后训练或 RL 微调。

### 3.4 训练细节

- **基座模型**：Qwen2.5-VL-3B、Qwen2.5-VL-7B（Bai et al., 2025b）、Qwen3-VL-30B（Bai et al., 2025a）；**RL 前不做 SFT**。
- **RL 算法**：GRPO，每查询采样 **8 条轨迹**（rollout size 8），采样温度 1.0。
- **上下文长度**：最大 16,384 token。
- **批量大小**：rollout batch 512，global batch 128。
- **训练步数**：75 步（约 5 个 episode），4 × NVIDIA H100 80GB；3B 约 **13 小时**、7B 约 **15 小时**。
- **30B 缩放**：Qwen3-VL-30B-A3B-Instruct 基座，经 Tinker API 用 **LoRA（rank 64）** 训练同一稠密奖励 GRPO 目标。
- **图像输入**：512×512 至 2048×2048 高分辨率，保留细粒度空间信息。
- **优化器**：AdamW，bf16，学习率 $1 \times 10^{-6}$，权重衰减 $1 \times 10^{-2}$，KL 惩罚系数 $10^{-2}$。
- **数据划分**：STVQA-7K 按 90/10 划分训练/验证。
- **全部参数（含视觉编码器）参与更新**。

**推理开销。** 由于生成面向问题的场景子图而非穷举场景描述（由数量惩罚与 RoI 过滤监督强制），结构化推理仅带来**平均约 120 个额外 token** 的适度开销。

---

## 4 实验

在 14 个多样化基准上评估（8 个空间 + 6 个真实世界/通用 VQA，覆盖 2D 与 3D 推理），围绕两个核心问题：
- **(Q1)** 空间 VQA 生成管线 + 稠密奖励 RL 能否提升 MLLM 的通用空间与视觉推理？
- **(Q2)** MLLM 能否仅从 7K 合成样本学到强空间能力？与多几个数量级数据训练的模型相比如何？

**基准。** 8 个空间基准：CV-Bench 2D/3D（Tong et al., 2024a）、BLINK Spatial Relations 与 Relative Depth（Fu et al., 2024）、3DSRBench（Ma et al., 2024b）、MMVP（Tong et al., 2024b）、SpatialBench（Cai et al., 2024）、SpatialReasonerEval（Ma et al., 2025a）、多视图 MindCube-tiny（Wang et al., 2026）、以及发布 STVQA-7K 测试集的留出验证划分（九类空间推理）。6 个真实世界/通用基准：VStarBench、RealWorldQA、MME-RealWorld（RoboSpatial-Home 仅用 Configuration 与 Compatibility 子集）、MM-Star、HallusionBench。

**基线。** 闭源：GPT-5（gpt-5-0807）、GPT-4o（gpt-4o-0513）、Claude 4 Sonnet、Claude 3.5 Sonnet。开源通用：Qwen2.5-VL、Qwen3-VL-30B、LLaVA-NeXT、Cambrian-1、VLAA-Thinker。开源空间专用：SpaceLLaVA、SpatialRGPT、RoboPoint、SpaceThinker、SpaceOm、SpatialReasoner、SpatialBot、Visionary-R1、SATORI-R1（Shen et al., 2025a）。消融变体：STVQA-7K 上训练的 SFT 基线、稀疏奖励 RL 基线（仅格式 + 正确率，各 0.5 权重），用于隔离稠密空间奖励的效果。

**评测设置。** 全部 zero-shot、贪心解码（temp = 0.0，max_new_tokens = 2048）。SpatialRGPT 用深度输入，其余模型只用 RGB。Accuracy 为主指标。

### 4.1 结果

**空间基准表现（表 1、表 2）。** 所有空间任务上表现强且一致：SpatialThinker-30B 几乎在每个基准上最佳，SpatialThinker-7B 是最强的小型开源模型。

- CV-Bench：ST-7B 在 2D/3D 上平均 78.2%，逼近 GPT-4o 的 79.4%，领先所有同级开源模型；ST-30B 达 87.0%，超越 GPT-5（85.86%）与 Claude 4 Sonnet（78.73%）；3D 分项上 ST-30B 达 **93.6%**（+3.3% vs GPT-5）。
- 3DSRBench（需朝向与多对象推理）：ST-7B 56.4%（超 GPT-4o +12.1%），ST-30B 62.1%。
- BLINK 空间关系与相对深度：ST-7B 86.0% 与 72.6%（平均 79.3%，逼近 GPT-4o 的 80.4%）；ST-30B 平均 84.0%，超越用深度输入 + 700K 样本的 Spatial-RGPT-7B（69.0%）。
- 附加空间基准（表 2）：ST-30B 在 MMVP（79.7%）、SpatialReasonerEval（92.6%）、SpatialBench（69.5%）上均超过 GPT-5 与 Claude 4 Sonnet；ST-7B 在 MMVP 上 78.0%，超过包括 GPT-5（61.7%）在内的所有基线。

尽管只用 7K 合成样本 + RGB 输入，ST-7B 稳定超越训练数据多几个数量级的开源基线（VLAA-Thinker-7B、Cambrian-1-8B、Spatial-RGPT、SpaceLLaVA、RoboPoint-13B）。**值得注意的是：即使只用 RGB 与 2D 奖励训练，关系场景图监督编码了与深度和朝向相关的线索，RL 目标训练模型保持几何-关系一致性，涌现出 3D 推理能力。**

**真实世界与通用 VQA 基准表现（表 3）。** 相比基座，ST-7B 在 MM-Star 65.9%（+2.0%）、VStarBench 81.7%（+5.8% vs 基座，+15.7% vs GPT-4o）、RoboSpatial-Home 76.3%（+5.7% vs 基座，+7.9% vs GPT-4o）上超越所有开源与闭源基线；幻觉敏感与真实世界基准上：HallusionBench 66.4%（+13.5% vs 基座，+11.4% vs GPT-4o）、RealWorldQA 69.2%、MME-RealWorld-Lite 48.3%（+4.2%）。这些结果证明稠密空间奖励改善的是**广泛视觉感知**，而不只是空间理解。我们把收益归因于空间接地迫使模型关注特定图像区域及其几何属性：锚定视觉证据减少幻觉（HallusionBench +13.5%）、锐化细粒度视觉区分（VStarBench +5.8%）、改善具身场景理解（RoboSpatial-Home +5.7%）。ST-30B 进一步扩展：在 MM-Star（66.9%）、VStarBench（85.9%）、RoboSpatial-Home（78.1%）、HallusionBench（75.2%，超过 GPT-5 的 73.82%）上取得所有模型最优。

**稠密奖励 RL 带来更优泛化（表 4）。** ST-7B 在全部 14 基准平均 70.5%，比 SFT 增益多 +5.5%、比稀疏 GRPO 变体多 +3.2%，基本匹敌 GPT-5（−0.9% 平均）并超过 GPT-4o、Claude 4 Sonnet 及所有开源基线。ST-30B 达 74.5%，超越 GPT-5（+3.0%）与 Claude 4 Sonnet（+5.8%）。3B 规模同样一致：ST-3B 分别超越 SFT 与 GRPO 对应版本 +5.2% 与 +3.9%。**Vanilla GRPO 相对基座仅 +4.4%（7B）/ +5.2%（3B），而稠密空间奖励将其提升到 +7.7% 与 +9.1%（约 1.7 倍）**——强调了数量与空间目标及词典序门控提供的互补学习信号。

**奖励设计消融（表 5，STVQA-7Kval）。**

| 奖励分量 | STVQA-7Kval |
|---|---|
| Format + Accuracy | 74.9 |
| + Spatial | 23.7 |
| + Count | 61.7 |
| + Lexicographic Gating & RoI Filtering | 76.3 |
| + Filtered Dataset (pass@2) | 87.9（+13.0）|

**朴素加空间奖励会引发 reward hacking（掉到 23.7%）**——模型过生成杂乱的框以利用 CIoU 奖励。引入数量奖励缓解（相对提升 38%），将场景图内对象与关系数量正则到标准数量。但奖励所有场景对象会使模型偏向穷举描述；改为**只奖励与问题相关实体对应的 RoI 的局部监督** + **词典序门控**（答案正确才给空间奖励），恢复并略超基线（76.3%）；再经 GPT-4o pass@2 校验的数据过滤（保留 7K 高质量样本），进一步提升到 **87.9%**。这种分阶段奖励塑形对稳定优化、把学习锚定在可验证的空间推理上至关重要。

**OOD 泛化：稠密奖励带来更强迁移（表 6，13 个留出基准）。** 稀疏奖励 GRPO 相对基座在空间上有实打实增益（3B +4.4%、7B +5.9%），但在真实世界基准上提升微弱（+4.9% / +1.9%），几乎追平或低于 SFT（+4.6% / +2.8%）。相比之下，SpatialThinker 在 OOD 上显著更强：3B +7.6%、7B +5.3%，两个规模都超过基线；ST-7B 的真实世界增益是稀疏 GRPO 的**近 3 倍**（+5.3% vs +1.9%）。结构化推理格式 + 词典序门控奖励鼓励模型内化空间先验与组合模式，有效迁移到 OOD 任务。附录 F 还展示了抽象与多视图推理任务的泛化。

### 表 1：2D 与 3D 空间理解基准（完整数据）

| 模型 | 3DSRBench | CV-Bench 2D | CV-Bench 3D | CV-Bench Avg. | BLINK Spatial Relation | BLINK Relative Depth | BLINK Avg. |
|---|---|---|---|---|---|---|---|
| **闭源模型** | | | | | | | |
| GPT-5-0807 | 68.2 | 81.4 | 90.3 | 85.8 | 90.9 | 81.4 | 86.1 |
| GPT-4o-0513 | 44.3 | 75.8 | 83.0 | 79.4 | 82.5 | 78.2 | 80.4 |
| Claude-4-Sonnet-0514 | 61.9 | 73.3 | 84.2 | 78.7 | 79.0 | 78.2 | 78.6 |
| Claude-3.5-Sonnet-0620 | 48.2 | 60.2 | 71.5 | 65.9 | 58.7 | 67.7 | 63.2 |
| **开源通用 MLLM** | | | | | | | |
| Qwen2.5-VL-3B | 44.0 | 59.9 | 60.2 | 60.0 | 66.4 | 54.0 | 60.2 |
| Qwen2.5-VL-7B | 48.4 | 69.1 | 68.0 | 68.6 | 84.0 | 52.4 | 68.2 |
| Qwen3-VL-30B | 60.4 | 79.0 | 89.6 | 84.3 | 86.0 | 75.8 | 80.9 |
| VLAA-Thinker-Qwen2.5-VL-7B | 52.2 | 60.8 | 60.3 | 60.6 | 81.2 | 71.0 | 76.1 |
| LLaVA-NeXT-8B | 48.4 | 62.2 | 65.3 | 63.8 | – | – | – |
| Cambrian-1-8B | 42.2 | 72.3 | 72.0 | 72.2 | 69.9 | 73.4 | 71.7 |
| **开源空间 MLLM** | | | | | | | |
| RoboPoint-13B | – | – | 61.2 | – | 60.8 | 61.3 | 61.1 |
| SpatialBot-3B | 41.1 | – | 69.1 | – | 67.8 | 67.7 | 67.8 |
| SpaceLLaVA-13B | 42.0 | – | 68.5 | – | 72.7 | 62.9 | 67.8 |
| SATORI-R1 | 48.0 | 54.6 | 69.4 | 62.0 | 77.0 | 58.9 | 68.0 |
| Spatial-RGPT-7B w/ depth | 48.4 | – | 60.7 | – | 65.7 | 72.3 | 69.0 |
| SpaceThinker | 51.1 | 65.1 | 65.9 | 65.5 | 73.4 | 59.9 | 66.7 |
| SpaceOm | 52.2 | 72.1 | 69.3 | 70.7 | 81.1 | 65.3 | 73.2 |
| **方法对比（STVQA-7K 训练）** | | | | | | | |
| Qwen2.5-VL-3B + SFT | 50.8 | 53.9 | 68.4 | 61.1 | 65.0 | 66.9 | 66.0 |
| Qwen2.5-VL-3B + Vanilla GRPO | 50.1 | 70.6 | 66.6 | 68.6 | 73.4 | 55.6 | 64.5 |
| **SpatialThinker-3B** | **52.9** | **71.0** | **76.3** | **73.6** | **81.8** | **66.9** | **74.4** |
| Qwen2.5-VL-7B + SFT | 53.6 | 56.1 | 71.3 | 63.7 | 75.5 | 64.5 | 70.0 |
| Qwen2.5-VL-7B + Vanilla GRPO | 54.7 | 68.9 | 76.5 | 72.7 | 80.4 | 75.0 | 77.7 |
| **SpatialThinker-7B** | **56.4** | **77.7** | **78.7** | **78.2** | **86.0** | **72.6** | **79.3** |
| **SpatialThinker-30B** | **62.1** | **80.3** | **93.6** | **87.0** | **88.1** | **79.8** | **84.0** |

### 表 2：附加空间基准（完整数据）

| 模型 | MMVP | SpatialReasonerEval | SpatialBench | STVQA-7Kval | MindCube-tiny |
|---|---|---|---|---|---|
| **闭源模型** | | | | | |
| GPT-5-0807 | 61.7 | 90.5 | 62.6 | 89.7 | 42.5 |
| GPT-4o-0513 | 70.7 | 85.8 | 67.0 | 77.0 | 34.9 |
| Claude-4-Sonnet-0514 | 71.3 | 85.7 | 60.9 | 80.5 | 44.8 |
| Claude-3.5-Sonnet-0620 | 71.3 | 84.1 | 63.2 | – | – |
| **开源通用与空间 MLLM** | | | | | |
| Qwen2.5-VL-3B | 67.0 | 68.0 | 49.9 | 74.3 | 36.4 |
| Qwen2.5-VL-7B | 72.3 | 70.6 | 62.5 | 77.5 | 35.3 |
| Qwen3-VL-30B | 77.9 | 88.2 | 68.1 | 83.7 | 39.0 |
| VLAA-Thinker-7B | 75.3 | 61.2 | 66.2 | 76.2 | 36.7 |
| SpaceThinker | 63.0 | 69.6 | 57.9 | 75.4 | 36.0 |
| SpaceOm | 66.3 | 68.9 | 58.6 | 66.0 | 33.5 |
| SpatialReasoner | 64.0 | 76.4 | 59.2 | 74.0 | 34.6 |
| SATORI-R1 | 67.7 | 70.5 | 60.3 | 51.2 | 36.0 |
| Visionary-R1 | 70.3 | 72.9 | 59.8 | 74.4 | 36.0 |
| **方法对比（STVQA-7K 训练）** | | | | | |
| Qwen2.5-VL-3B + SFT | 62.7 | 67.5 | 56.3 | 85.6 | 35.9 |
| Qwen2.5-VL-3B + Vanilla GRPO | 68.3 | 69.3 | 56.9 | 86.7 | 38.8 |
| **SpatialThinker-3B** | **69.0** | **76.5** | **61.5** | **92.5** | **40.5** |
| Qwen2.5-VL-7B + SFT | 68.3 | 70.8 | 63.5 | 84.5 | 42.2 |
| Qwen2.5-VL-7B + Vanilla GRPO | 74.3 | 79.6 | 64.2 | 87.1 | 44.0 |
| **SpatialThinker-7B** | **78.0** | **82.7** | **66.4** | **92.8** | **45.1** |
| **SpatialThinker-30B** | **79.7** | **92.6** | **69.5** | **93.0** | **45.4** |

### 表 3：VQA 与真实世界基准（完整数据）

| 模型 | MM-Star | VStarBench | RealWorldQA | MME-RealWorld-Lite | RoboSpatial-Home | HallusionBench |
|---|---|---|---|---|---|---|
| **闭源与开源 MLLM** | | | | | | |
| GPT-5-0807 | 58.9 | 73.3 | 78.7 | 57.0 | 71.5 | 73.8 |
| GPT-4o-0513 | 64.7 | 66.0 | 75.4 | 51.6 | 68.4 | 55.0 |
| Claude-4-Sonnet-0514 | 64.4 | 60.7 | 64.0 | 46.9 | 69.7 | 71.2 |
| Claude-3.5-Sonnet-0620 | 65.1 | 51.8 | 60.1 | 45.2 | 57.0 | 55.5 |
| Qwen2.5-VL-3B | 55.9 | 74.9 | 58.2 | 41.9 | 58.7 | 46.3 |
| Qwen2.5-VL-7B | 63.9 | 75.9 | 68.4 | 44.1 | 70.6 | 52.9 |
| Qwen3-VL-30B | 64.3 | 81.2 | 64.8 | 45.8 | 53.1 | 61.5 |
| VLAA-Thinker-7B | 63.8 | 58.1 | 66.4 | 44.6 | 68.9 | 68.9 |
| SpaceThinker | 54.5 | 56.5 | 61.6 | – | 52.6 | 65.4 |
| SpaceOm | 57.7 | 56.5 | 53.3 | – | 68.9 | 62.9 |
| **方法对比（STVQA-7K 训练）** | | | | | | |
| Qwen2.5-VL-3B + SFT | 53.9 | 73.3 | 64.8 | 43.0 | 69.8 | 58.9 |
| Qwen2.5-VL-3B + Vanilla GRPO | 56.7 | 74.3 | 64.4 | 46.7 | 64.0 | 59.0 |
| **SpatialThinker-3B** | **57.6** | **78.0** | **66.3** | **46.5** | **70.6** | **62.5** |
| Qwen2.5-VL-7B + SFT | 63.2 | 78.0 | 65.4 | 47.4 | 72.4 | 66.2 |
| Qwen2.5-VL-7B + Vanilla GRPO | 63.4 | 73.9 | 66.6 | 46.3 | 76.2 | 60.7 |
| **SpatialThinker-7B** | **65.9** | **81.7** | **69.2** | **48.3** | **76.3** | **66.4** |
| **SpatialThinker-30B** | **66.9** | **85.9** | **74.9** | **49.2** | **78.1** | **75.2** |

### 表 4：14 个基准平均准确率与相对增益

| 模型 | Avg. Acc. (14) | ΔBase | ΔGPT-5 | ΔGPT-4o | ΔClaude 4 |
|---|---|---|---|---|---|
| **闭源与基座 MLLM** | | | | | |
| GPT-5-0807 | 71.5 | – | – | – | – |
| GPT-4o-0513 | 65.8 | – | – | – | – |
| Claude-4-Sonnet-0514 | 68.7 | – | – | – | – |
| Claude-3.5-Sonnet-0620 | 60.9 | – | – | – | – |
| Qwen2.5-VL-3B | 56.8 | – | – | – | – |
| Qwen2.5-VL-7B | 62.8 | – | – | – | – |
| Qwen3-VL-30B | 68.1 | – | – | – | – |
| **方法对比（STVQA-7K 训练）** | | | | | |
| Qwen2.5-VL-3B + SFT | 60.7 | +3.9 | −10.8 | −5.1 | −8.0 |
| Qwen2.5-VL-3B + Vanilla GRPO | 62.0 | +5.2 | −9.5 | −3.8 | −6.7 |
| **SpatialThinker-3B** | **65.9** | **+9.1** | **−5.6** | **+0.1** | **−2.8** |
| Qwen2.5-VL-7B + SFT | 64.9 | +2.1 | −6.6 | −0.9 | −3.8 |
| Qwen2.5-VL-7B + Vanilla GRPO | 67.2 | +4.4 | −4.3 | +1.4 | −1.5 |
| **SpatialThinker-7B** | **70.5** | **+7.7** | **−1.0** | **+4.7** | **+1.8** |
| **SpatialThinker-30B** | **74.5** | **+6.4** | **+3.0** | **+8.7** | **+5.8** |

### 表 6：13 个留出基准上的平均增益（除 STVQA-7Kval 外的全部）

| 模型变体 | 空间 VQA ΔBase | 真实世界 VQA ΔBase |
|---|---|---|
| Qwen2.5-VL-3B + SFT | +2.1 | +4.6 |
| Qwen2.5-VL-3B + GRPO | +4.4 | +4.9 |
| **SpatialThinker-3B** | **+9.0** | **+7.6** |
| Qwen2.5-VL-7B + SFT | +0.9 | +2.8 |
| Qwen2.5-VL-7B + GRPO | +5.9 | +1.9 |
| **SpatialThinker-7B** | **+8.6** | **+5.3** |

---

## 5 相关工作

**MLLM 中的 3D 空间推理。** 近期工作通过点云或多视图重建集成 3D 信号（Hong et al., 2023c;a）、或带物理先验的世界模型（Wang et al., 2023; 2024）。SpatialVLM、SpatialPIN、SpatialBot、SpatialRGPT 等大规模工作使用数百万 3D 增强样本或 RGB-D 场景图；MM-Spatial、SpatialLLM、SpaRE 同样规模化合成或重建 3D 数据。但这些方法数据密集、依赖专用输入或在结构化关系建模上不足。SpatialThinker 仅用 7K VQA 样本 + 稠密空间奖励 RL 就获得稳健的关系与区域推理。

**MLLM 中的结构化视觉接地。** 场景图长期支持视觉推理（Hildebrandt et al., 2020; Wald et al., 2020; Gu et al., 2023; Carion et al., 2020; Cong et al., 2023）。LLM4SGG、GPT4SGG 从描述提取结构化图（Kim et al., 2024; Chen et al., 2023），开放词表 SGG 用 MLLM 超越固定本体（Chen et al., 2024b; Li et al., 2023）。RL 训练的 SGG 模型如 R1-SGG 通过稠密结构或认知奖励直接生成场景图（Chen et al., 2025c）。区域感知 MLLM（KOSMOS-2、GLaMM、Ferret）通过边界框与区域-文本对齐增强空间接地。SpatialThinker 扩展了这些想法：将推理接地在问题感兴趣区域聚焦的场景子图上，把结构化理解与奖励引导的空间推理结合。

**多模态强化学习。** RL 已被越来越多地用于增强 MLLM 推理：数学（Yang et al., 2025b; Meng et al., 2025）、分类与接地（Liu et al., 2025b）、语义分割（Liu et al., 2025a）、区域理解（Shen et al., 2025a）、开放词表检测/指代表达理解（Pinto et al., 2023; Shen et al., 2025b）。空间 RL 也已出现（Wang & Ling, 2025; Shen et al., 2025b; Ma et al., 2025a），但局限于最终正确率或粗略位置线索等稀疏信号，对细粒度空间推理支持有限。SpatialThinker 引入覆盖区域子图构建、对象定位、关系接地、对象计数与最终正确性的**稠密多目标奖励框架**。

---

## 6 结论

我们提出 SpatialThinker——通过 RL 将场景图接地与空间奖励结合、实现强空间推理的 MLLM。仅用 7K 样本训练，它就在空间、真实世界与通用 VQA 基准上超越闭源与开源 MLLM，并具有更优的 OOD 泛化，胜过训练数据多几个数量级的模型：SpatialThinker-7B 平均匹敌 GPT-5、超越 GPT-4o；SpatialThinker-30B 同时超越 GPT-5 与 Claude 4 Sonnet。稠密空间奖励将标准 GRPO RL 的收益近乎翻倍，凸显了丰富监督信号的价值。我们的结果表明：**2D 接地 + 3D 关联的关系监督足以诱导稳健的 3D 空间先验**。

局限与未来工作：方法依赖显式场景图；未来可探索潜表示中的隐式空间推理、将奖励设计扩展到时空与真实世界任务（如网页导航）、开发跨视觉推理域的统一多目标策略与环境。

---

## 附录

### 附录 A：STVQA-7K 数据集构建细节

**动机。** 高质量空间 VQA 数据集稀缺：现有基准要么缺乏接地场景图标注（对象与关系的显式空间坐标），要么不能全面覆盖 2D 与 3D 空间推理类别。Visual Genome 提供稠密人工标注的场景图，在统一表示框架内严格接地问题生成与答案校验。

**谓词扩展。** 原 VG150 谓词集仅 50 个关系，缺少位置关系（left、right、beside）、距离关系（near、far、next to）、比较大小（smaller、taller、bigger）、朝向（facing towards/away）、包含（inside、beneath）等关键类别。新增 34 个谓词弥补，覆盖更丰富的 2D/3D 空间。边界框保留**绝对像素坐标**（非归一化），保持真实尺度与空间对齐，支撑 CIoU 监督。

**三阶段管线。** (1) 从标准场景图合成问题；(2) 外部校验自动质量过滤；(3) 场景图适配实现区域对齐。

- **合成问题生成**：Visual Genome 场景图（150,000+ 图像的对象类别、边界框、关系三元组）作地基真值；Claude Sonnet 4 合成多选题 QA 对，覆盖九类空间推理（空间关系、物理可达与交互、比较大小、特定视角朝向、图像帧内实例位置、相对相机的深度排序、到参考对象的距离比较、对象计数、存在性验证）。每个 QA 附 10 分制评分与难度。为促进稳健感知，还包含场景中部分可见或被遮挡对象的问题。也纳入干扰项（distractors）以强化推理。
- **质量过滤与校验**：Claude Sonnet 4 生成 → GPT-4o 以 pass@2 一致性校验标准答案标签；未通过者用两个补充模型响应再评估，四个响应全部与生成标签不一致的样本判为可能错误/有歧义而丢弃。跨模型校验 +13% 准确率。56,224 个初始问题 → 选评分最高的 10,000 个 → 一致性过滤后保留 6,895 训练 + 692 验证样本（约 75%）。最终集合 50% 来自关系类别，其余 50% 分布在另外八类。为防止位置偏差，答案在 A/B/C/D 选项间均匀分布。
- **场景图适配**：对每个问题，tokenize + 词形还原提取内容词（单复数形式），过滤场景图仅保留标签出现在问题词汇中的对象节点；主语与宾语都被保留且谓词出现在问题上下文中的关系三元组予以保留。生成的聚焦场景图表示训练模型输出与问题对齐的 RoI 子图，学会在复杂视觉场景中定位注意力。

### 附录 B：实验设置细节

**B.1 实现细节。** 与 §3.4 相同：Qwen2.5-VL-3B/7B 基座、无 SFT、GRPO（rollout 8、温度 1.0）、上下文 16,384、rollout batch 512、global batch 128、75 步、4×H100、3B 约 13 小时 / 7B 约 15 小时、512²–2048² 高分辨率输入、全参数（含视觉编码器）更新、AdamW + bf16、LR 1e-6、权重衰减 1e-2、KL 10⁻²、90/10 划分。30B：Qwen3-VL-30B-A3B-Instruct + LoRA（rank 64）经 Tinker API，completion 长度上限 2048 token。

**B.2 实验设置。** 基准细节：CV-Bench 测 2D 空间关系、对象计数、深度排序与距离推理；BLINK 测方向/位置理解与细粒度点级深度感知（SpatialThinker 训练时无显式点级监督，尤其有挑战）；3DSRBench 通过关系与多对象比较评估自我中心 3D 空间推理；MMVP 检查朝向、位置关系、存在性、视角、大小等视觉模式识别；SpatialBench 评估计数、存在性、位置关系、物理交互（reach）、大小比较；SpatialReasonerEval 强调 3D 空间任务中的深度与距离推理；MindCube-tiny 是跨场景多图推理的自我中心基准；STVQA-7Kval 覆盖九类域内空间掌握。闭源基线用默认 medium reasoning effort 查询 GPT-5。评估管线基于 OpenVLThinker 的评估框架改造。

**B.3 提示格式。** 结构化四阶段提示：先在 `<observe>` 中观察图像，再在 `<scene>` 中可视化相关场景图，然后在 `<think>` 中作内部独白式推理，最后在 `<answer>` 中给出最终答案（只返回带正确选项与答案的最终选择，如 `<answer> (C) The red cube is left of the green sphere </answer>`）。提示还包含 `Image size: {Width} × {Height}`（动态替换为实际值），帮助模型把预测边界框坐标约束在图像边界内，实现更好的空间定位，并直接用于 CIoU 等 IoU 类空间奖励评估。

**B.4 SFT 训练细节。** 基座模型与数据集同 RL；LLaMA-Factory 框架 + LoRA（rank 8，应用于全部可用模块）；3 epoch 共 645 步；上下文 2048 token；BF16；LR 1e-4，cosine 调度 + 0.1 warmup。直接训练 QA 对、无中间推理轨迹（生成标准推理轨迹需额外数据处理/标注/API 预算）。SFT 基线用于证明稠密空间奖励 RL 相比同数据集监督学习的泛化优势。

**B.5 RL 训练细节。** 基于 EasyR1 框架；基座模型不做任何先验 SFT，隔离奖励驱动学习的效应。Vanilla GRPO 基线只用正确率（w=0.5）+ 格式（w=0.5）奖励，输出推理轨迹 + 最终答案（标准 CoT GRPO 设置）。注意：由于算力瓶颈，30B 不训练 SFT 与基线 RL，只用最终空间奖励设计。

**B.5.1 RL 训练曲线。** 四个奖励分量（格式、正确率、数量、空间）全程一致且可解释地提升：格式奖励早期快速收敛（学会结构有效输出）；正确率稳步上升；数量奖励持续上升（学会只预测与问题相关的对象与关系）；空间奖励渐进改善（预测框与标准框对齐）。响应长度先降后升，出现 **"aha moment"**（DeepSeek-AI et al., 2025; Zhou et al., 2025）——模型开始产生更深思熟虑的推理轨迹，在回答前花更多"思考时间"，与其空间推理过程中自我反思与结构化规划的出现一致。

### 附录 C：奖励设计过程

**C.1 奖励设计消融（表 5 的完整叙述）。** 无生成约束地朴素加空间奖励 → 性能崩溃超 50%（74.9% → 23.7%）：模型生成杂乱边界框博弈 CIoU。引入数量奖励：相对提升 38%（→ 61.7%），约束过生成、迫使聚焦问题相关元素。但奖励所有场景对象的空间对齐仍使模型偏向穷举全局描述 → 从**全局**转向**局部**空间监督（只奖励问题相关对象与关系派生的 RoI）；词典序门控进一步确保只有答案正确才给空间奖励。这些干预恢复并略超原性能（76.3%）。最后 pass@2 数据过滤放大效果，达到最佳验证准确率 **87.9%**。

**C.2 数量奖励权重消融（表 7）。** 固定高层权重 $(w_f, w_c, w_a, w_s) = (0.1, 0.2, 0.5, 0.2)$ 与其余管线（SpatialThinker-3B、词典序门控、KL 0.01、75 步、STVQA-7K），消融对象/关系数量拆分 $(\lambda_{obj}, \lambda_{rel})$：

| λ_obj | λ_rel | Acc. | Format | Count | Spatial |
|---|---|---|---|---|---|
| **0.7** | **0.3** | **76.02** | 99.90 | 75.35 | 49.48 |
| 0.8 | 0.2 | 75.24 | 99.90 | 74.98 | 48.61 |
| 1.0 | 0.0 | 74.85 | 99.90 | 71.97 | 48.53 |
| 0.5 | 0.5 | 74.85 | 99.71 | 77.65 | 48.54 |

对象数量是更干净的信号（关系受对象约束），对象数量惩罚先抑制对象过生成，关系数量惩罚再精修剩余关系集。两个极端都次优：1.0/0.0 完全去掉关系修正，0.5/0.5 低估了主导的对象信号。

**C.3 设计动机。**

- **缓解空间奖励 hacking**：初始直接奖励定位质量的公式导致模型生成大量不同坐标的边界框；匈牙利匹配下即使随机预测偶尔也有高 CIoU。数量奖励起双重作用：(1) 约束生成空间防 hacking；(2) 鼓励聚焦问题相关元素而非穷举整图。线性惩罚与标准 RoI 数量的相对偏差成正比，归一化防止被多对象场景主导。
- **场景图过滤**：用完整 Visual Genome 场景图训练时模型会记忆穷举场景描述（含无关背景对象），泛化差；过滤为仅保留与问题相关的对象与关系，把监督聚焦到任务关键信息。
- **空间奖励用 CIoU 而非 IoU**：IoU 在框不重叠时为零梯度，CIoU 通过中心距离、长宽比与重叠提供有意义梯度，监督更稠密更稳健。
- **监督与探索的平衡**：模型学简单奖励函数显著快于复杂函数；过度细致、监督每一方面的奖励函数反而降性能（模型过拟合微小奖励分量、收敛到模板式答案）。最终设计：格式检查、数量约束、正确率奖励提供软信号，空间定位奖励只在答案正确时激活，维持指导与探索的微妙平衡。
- **词典序门控的顺序优化**：严格层级 format ≻ {count, accuracy} ≻ spatial，公式同式 (3)：

$$
R_{total} = I[R_{format} = 1] \cdot \left( w_{format} R_f + w_{count} R_c + w_{accuracy} R_a + I[R_{accuracy} = 1] \cdot w_{spatial} R_s \right)
$$

权重 $w_{format}=0.1, w_{count}=0.2, w_{accuracy}=0.5, w_{spatial}=0.2$。

### 附录 D：场景图错误传播影响

SpatialThinker 把面向问题的场景图作为推理链的中间步骤，此阶段错误原则上可能传播到最终答案。在 STVQA-7K 留出验证划分（n=692，SpatialThinker-7B）上量化场景图质量与答案正确性的耦合。对每个样本解析 `<scene>` 中的预测场景图，与标准计算两个互补集合相似度：对象 Jaccard $J_{obj}$（归一化对象类集合，剥离数字 ID 如 mountain.1→mountain）与三元组 Jaccard $J_{trip}$（同一归一化下的 (subject, predicate, object) 关系集合）：

$$
J_{obj} = \frac{|O^{pred} \cap O^{gt}|}{|O^{pred} \cup O^{gt}|}, \quad J_{trip} = \frac{|T^{pred} \cap T^{gt}|}{|T^{pred} \cup T^{gt}|}
$$

对象识别饱和（$\bar{J}_{obj} = 0.957$，663/692 样本 $J_{obj} \ge 0.5$），作为下游准确率预测器无信息量（ϕ = −0.009）；关系级项承载判别信号，故以 $J_{trip} \ge 0.5$ 定义 "SGG correct"。

表 8（SGG 正确性 × 最终答案正确性，n=692）：

| | 答案 ✓ | 答案 ✗ | 行合计 |
|---|---|---|---|
| SGG ✓（J_trip ≥ 0.5） | 221（95.26%） | 11（4.74%） | 232 |
| SGG ✗（J_trip < 0.5） | 365（79.35%） | 95（20.65%） | 460 |
| 列合计 | 586（84.68%） | 106（15.32%） | 692 |

三元组级场景图恢复困难（$\bar{J}_{trip} = 0.319$，仅 232/692 = 33.5% 样本 $J_{trip} \ge 0.5$），但两个结果呈现互补效应：场景图正确时条件答案准确率升至 95.26%；不正确时仍有 79.35%，差距 +15.91 pp（Phi 系数 ϕ = +0.209；连续 J_trip 上 Spearman ρ = +0.221，p < 10⁻⁸）。不同三元组截断阈值下信号一致（Δ ∈ [+15.9, +17.2] pp）。**结论：场景图错误的下游影响可测量但有限**——正确的场景图可靠提升最终答案；训练好的推理策略能在不完美的中间表示上继续推理（作为"部分脚手架"而非严格依赖）。场景图生成是有用但不承重的脚手架：准确时把答案正确率提升约 16 pp，不准确时模型仍能在约 80% 样本上答对。持续投入中间表示（更长 RL 训练、更强场景图监督、更丰富标注）是把三元组级恢复提升转化为更高答案准确率的有前景方向。

### 附录 E：散度约束消融（表 9，CV-Bench，SpatialThinker-3B）

DAPO（Yu et al., 2025; Vassoyan et al., 2025）等近期工作认为 KL 正则不必要地约束策略更新，建议完全移除 KL 惩罚以允许更自由探索；Huang et al. (2024) 则提出用卡方（chi-squared）惩罚更好控制过度优化。三种变体对比：

| 变体 | Count | Relation | Depth | Distance | CV-Bench 2D | CV-Bench 3D | CV-Bench Avg. |
|---|---|---|---|---|---|---|---|
| + No KL Penalty | 65.5 | 76.8 | 74.8 | 70.2 | 71.2 | 72.5 | 71.9 |
| + Chi2 (0.01) | 64.5 | 73.7 | 71.2 | 66.2 | 69.1 | 68.7 | 68.9 |
| **+ KL (0.01)** | **68.5** | **73.5** | **79.7** | **72.8** | **71.0** | **76.3** | **73.7** |

移除 KL 惩罚导致明显性能下降（尤其 3D 任务）；卡方惩罚在多个子任务（尤其深度与距离推理）上劣于无惩罚与 KL 变体；KL 正则化模型整体最佳（CV-Bench 平均 73.7%）。**结论：适度的 KL 惩罚稳定策略更新、防止奖励过度优化——在需要稳定与连贯空间接地的多模态推理任务中保留小 KL 项仍是有益的**，尽管纯语言对齐工作主张移除散度约束。

### 附录 F：抽象推理补充结果（表 10）

在训练分布之外的两个抽象推理基准上验证泛化：Lego Puzzles（测试组合对象推理与多步空间推理）与 BLINK Multi-View（跨多个视点整合空间线索，含视觉-空间理解与视角理解）。SpatialThinker-7B 在两项上取得最高开源性能：Lego Puzzles 37.7%、BLINK Multi-View 52.6%，后者逼近 GPT-4o（54.1%）并超越 Claude 3.5 Sonnet（51.9%）。有趣的是，vanilla GRPO 在 BLINK Multi-View 上有竞争力但在 Lego Puzzles 上表现不佳，表明稠密空间奖励提供支持组合推理的互补信号。

### 附录 G：CV-Bench 详细结果（表 11）

CV-Bench 四子任务（Count/Relation/Depth/Distance）+ 2D/3D 分项的完整对比，原文 Table 11。关键数字：SpatialThinker-30B 各子任务 67.4 / 93.2 / 96.1 / 91.1（2D 80.3、3D 93.6、平均 87.0）；SpatialThinker-7B 68.7 / 86.7 / 81.2 / 76.2（平均 78.2）；对比 GPT-5（68.3 / 94.5 / 92.2 / 88.6，平均 85.9）。完整逐模型数据见原文表 11。

### 附录 H：3DSRBench 详细结果（表 12）

四子任务（Height/Location/Orientation/Multi-Object）。SpatialThinker-30B：62.6 / 74.9 / 50.5 / 54.3（平均 62.1）；SpatialThinker-7B：52.0 / 70.3 / 45.5 / 50.9（平均 56.4）；GPT-5：72.9 / 79.5 / 59.0 / 60.6（平均 68.2）。完整逐模型数据见原文表 12。

### 附录 I：STVQA-7Kval 分类别结果（表 13）

九类空间推理（Relation/Reach/Size/Orient./Location/Depth/Distance/Count/Existence）的逐类准确率。SpatialThinker 系列在几乎所有类别上领先，关系、大小与存在性推理上增益最大：ST-7B 总体 92.8%（Relation 93.2、Location 97.9、Existence 93.6），ST-30B 总体 93.0%（Orientation 98.5、Location 99.2）；对比 GPT-5 总体 89.7、GPT-4o 77.0。完整逐模型数据见原文表 13。

### 附录 J：更多定性结果（图 8）

GPT-5-0807 在细粒度空间关系上经常犯错（如把"behind"判成"in front of"、把"in front of"判成"beside"），SpatialThinker 则通过 `<observe>` → `<scene>`（含精确边界框与关系三元组）→ `<think>` → `<answer>` 的完整链条给出正确且接地充分的回答，准确识别 GPT-5 常混淆的 3D 关系。定性示例原文图 4、图 8。

---

## 翻译说明

- 本翻译覆盖论文全部正文（摘要、引言、预备知识、方法、实验、相关工作、结论）与附录 A–J 的全部内容。
- 正文表 1–6 数据完整保留；附录 G/H/I 的详细表格（表 11–13）为控制篇幅以文字概括关键结果，完整逐模型数据请见原文对应表格。
- 公式编号与原文一致；专有名词、数据集名、模型名、基准名保留英文原文。
