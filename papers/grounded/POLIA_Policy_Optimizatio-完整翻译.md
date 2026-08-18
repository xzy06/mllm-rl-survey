# POLIA: Policy Optimization with Visual-Object-Level Intrinsic Advantage for Multimodal Reasoning

> **POLIA：面向多模态推理的视觉物体级内在优势策略优化**（完整中文翻译）
>
> - 作者：Yiran Zeng、Da Chen、Hangyu Mao、Yuanxing Zhang、Pengfei Wan、Mengchen Zhao
> - 机构：华南理工大学（中国广州）、快手科技（中国北京）
> - 来源/发表信息：Proceedings of the 43rd International Conference on Machine Learning (ICML 2026), Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s).
> - 对应 PDF：`POLIA_Policy_Optimizatio.pdf`

---

## 摘要

基于分组强化学习（RL）的最新进展极大地提升了 LLM 在文本推理方面的能力。然而，这些方法缺乏对多模态信息的充分建模，导致了显著的推理幻觉（reasoning hallucination）。在本文中，我们提出 POLIA——一种面向多模态推理、具有视觉物体级内在优势（visual-object-level intrinsic advantage）的新型分组 RL 方法。POLIA 分别在候选答案和视觉物体两个层面上引入了两个优势计算阶段。答案级外在优势（answer-level extrinsic advantages）基于一组候选答案的外在奖励计算得到。此外，我们基于每个视觉物体的置信度分数及其与最终答案的引用关系，为每个视觉物体计算内在优势。直观地说，物体的内在优势反映了它对正确答案的潜在贡献。这种两阶段优势计算机制确保了在包含多个视觉物体的多模态推理序列上进行准确的信用分配（credit assignment）。在多样化多模态推理基准上的实验结果表明，POLIA 显著优于开源 MLLM 和强基线方法。代码可在 https://github.com/dudu115/POLIAcode 获取。

## 1. 引言

强化学习（RL）已被证明是增强大语言模型（LLM）推理能力的有效工具（Zhou et al., 2025; Wang et al., 2025c）。对于多模态大语言模型（MLLM）而言，推理需要综合并分析来自不同模态的信息（Yin et al., 2024）。现有的 RL 方法，例如 GRPO（Shao et al., 2024b），无法区分不同模态，导致训练后的模型出现显著的推理幻觉（Zhang et al., 2025a; Tu et al., 2025）。例如，模型可能在推理过程中忽略视觉信息，或生成看似正确但违背视觉事实的答案（Guo et al., 2025）。这些问题迫切要求新的 RL 方法大幅提升 MLLM 的推理能力（Huang et al., 2025; Shen et al., 2025; Yang et al., 2025）。

使用 RL 提升 MLLM 的推理能力面临三大挑战。第一，缺乏对视觉证据显式且结构化的建模，视觉证据在多模态推理中通常被含糊地称为"与视觉相关的信息"（Fan et al., 2025; Zhou et al., 2025）。如果没有对视觉证据的明确强调，MLLM 往往难以从输入图像中提取最有用的视觉信息。第二，很难构建有效的奖励信号来引导推理过程（Bai et al., 2024），因为现有数据集仅提供最终答案作为评判模型输出的参考（Wu et al., 2025b）。因此，模型可能会通过奖励作弊（reward hacking）被诱导去获得虚假的高奖励。第三，现有 RL 方法缺乏对视觉证据的显式信用分配机制。如果没有清晰合理的信用分配机制，模型很容易忽略对最终答案贡献最大的关键视觉证据（Zhang et al., 2025c）。

先前的工作已证明了 RL 在多模态推理中的有效性，但其改进仍然有限。早期工作通过简单地将视觉 token 与文本 token 混合，将面向 LLM 的 RL 扩展到 MLLM（Yang et al., 2025; Huang et al., 2025）。这些方法严重依赖基础 MLLM 区分关键视觉证据的能力，导致学习效率低下。近期工作通过鼓励模型在生成答案时引用视觉 token 来优化推理过程（Zheng et al., 2025b; Zhang et al., 2025d; Cao et al., 2025; Fan et al., 2025; Wang et al., 2025a）。尽管这些方法改善了推理过程中对视觉信息的利用，但模型可能会得出对视觉证据完全错误的引用。换言之，由于缺乏推理过程奖励和显式的信用分配，模型无法学会如何利用视觉证据进行推理。

![Figure 1](file://c:/Users/Lenovo/Desktop/study/essay/mllm-rl-survey/figures/fig1_reward_signal_evolution.png)

**图 1.** GRPO 与 POLIA 在多模态推理上的对比。左侧：传统 GRPO 仅在答案层面计算优势。右侧：POLIA 将答案级外在优势（A_ext）与视觉物体级内在优势（A_int）相结合进行多模态策略优化，实现了对视觉物体的显式信用分配以及对视觉证据更有效的利用。

在本文中，我们提出 POLIA——一种面向多模态推理、具有视觉物体级内在优势的新型分组 RL 方法。POLIA 在 GRPO 的基础上引入了额外的内在优势，显著提高了视觉证据上信用分配的准确性。图 1 展示了这一对比。总体而言，POLIA 的优势计算可分为两个阶段。首先，将 MLLM 生成的候选答案（包括相关的推理链）视为一个大的分组，我们通过将每个候选答案与数据集中的参考真实答案进行比较，为每个候选答案计算外在奖励。由此，我们遵循 GRPO 为每个候选答案计算外在优势。其次，由于每个候选答案引用一组独特的视觉物体，我们识别出若干组视觉物体作为视觉证据 ¹。在每个视觉物体组中，我们将答案级外在奖励广播到每个视觉物体，并根据其置信度进行校正。然后，通过比较同一视觉物体组内校正后的物体级奖励，为每个视觉物体计算内在优势。直观地说，物体的内在优势反映了它对正确答案的潜在贡献。我们称之为内在优势，因为它是训练过程中在自然形成的视觉物体组内计算得到的。上述两阶段优势计算实现了更准确、更细粒度的信用分配机制，这对于缓解多模态推理中的幻觉和奖励作弊至关重要。

我们的主要贡献总结如下：

- 受人类读图方式的启发，我们提出了一种新的多模态推理范式，将视觉证据形式化为一组视觉物体。通过这种方式，MLLM 可以专注于学习视觉物体之间的高层推理逻辑。
- 我们扩展了 GRPO，引入了一个新颖的内在优势计算模块，该模块在物体层面提供细粒度的奖励信号，有效引导推理过程的学习。
- 我们在七个广泛使用的多模态推理数据集上评估了 POLIA，涵盖复杂物体计数、空间关系理解、带视觉上下文的数学推理及相关任务。实验结果表明，POLIA 显著提升了 MLLM 的推理能力。

> ¹ 注意，我们将视觉证据形式化为一组视觉物体，因为人类通常以物体级别来阅读图片。

## 2. 相关工作

### 2.1. LLM 推理的强化学习

RL 很早就通过基于人类反馈的强化学习（RLHF）被用于 LLM，RLHF 利用人类偏好信号指导模型更新（Ziegler et al., 2019; Stiennon et al., 2020; Ouyang et al., 2022; Gu et al., 2024）。随后，用于增强推理的 RL 方法从 PPO（Schulman et al., 2017）和 DPO（Rafailov et al., 2023）演化为以 GRPO（Shao et al., 2024b）为代表的无评论家（critic-free）、基于分组（group-based）的算法。这种形式化为同一查询采样多个候选答案，并在分组内估计优势，无需训练价值函数，从而降低了训练成本，便于应用于 LLM。后续工作，如 Dr. GRPO（Liu et al., 2025a）、DAPO（Yu et al., 2025b）、GSPO（Zheng et al., 2025a）、GMPO（Zhao et al., 2025）和 GFPO（Shrivastava et al., 2025），在多个方面进一步改进了 GRPO。这些方法与 LLM 具有天然契合性：候选答案共享共同的文本上下文，使得答案级奖励能够公平地比较推理质量。对于 MLLM 而言，不同的答案可能依赖不同的视觉证据，导致答案级奖励无法公平地比较推理质量。因此，将面向 LLM 的 RL 方法适配到多模态推理，需要显式地考虑视觉接地（visual grounding）。

### 2.2. MLLM 推理的视觉信息建模

先前的工作通过在推理过程中引入更显式、更结构化的视觉信息建模来改进多模态推理。早期工作主要依赖提示（prompting）策略来鼓励模型整合视觉信息，例如多模态思维链（chain-of-thought）形式（Zhang et al., 2023; Shao et al., 2024a; Li et al., 2025）。后续方法引入了显式的视觉证据表示，使模型能够将推理与相应的图像区域关联起来（Peng et al., 2023）。更新的方法通过支持与图像的逐步交互，进一步丰富了视觉信息建模（Qi et al., 2024）。此外，RL 已被应用于学习多模态推理轨迹，无需在推理过程中提供中间监督（Fan et al., 2025; Cao et al., 2025）。尽管取得了这些进展，现有方法仍难以将视觉证据显式地结构化为有意义的物体并对其关系进行推理，这使得学习准确多模态理解所需的高层推理逻辑变得困难。

### 2.3. MLLM 推理的强化学习

在分组 RL 于 LLM 推理中取得成功的基础上，近期工作将无评论家策略优化应用于 MLLM（Meng et al., 2025; Shen et al., 2025; Peng et al., 2025; Wang et al., 2025b; Yang et al., 2025）。尽管这些方法证明了 RL 可以增强多模态推理，但主要基于最终答案定义的奖励信号对推理过程和视觉信息利用提供的指导有限。为解决这一局限，一些研究通过引入对推理行为的额外约束来细化奖励信号（Zhang et al., 2025b; Xia et al., 2025; Xu et al., 2025; Liu et al., 2025b; Wu et al., 2025a）。与此同时，其他工作侧重于通过引入显式视觉证据来提高视觉可靠性（Wang et al., 2025d; Zhang et al., 2025a; Yu et al., 2025a; Fan et al., 2025; Sarch et al., 2025）。然而，现有 RL 方法仍然依赖最终答案监督，为引用不同视觉证据的候选答案分配单一的标量奖励。因此，这些奖励信号无法对视觉证据提供精确的信用分配，导致对多模态推理的指导较为粗糙。

## 3. 预备知识

**分组 RL（Group-based RL）。** 分组 RL 已被广泛用于训练 LLM，无需学习显式的价值函数。给定输入 $x$，策略 $\pi_{\theta_{old}}$ 采样一组 $N$ 个候选答案 $\{y_1, \ldots, y_N\}$，每个候选答案对应一个完整的推理过程和最终答案。每个候选答案 $y_i$ 根据生成结果的总体质量被赋予一个标量奖励 $r_i = R(x, y_i)$。分组 RL 通过比较同一组候选答案内的奖励来计算优势。具体而言，每个答案的优势通过对其奖励进行组内归一化得到：

$$A_i = \text{GroupNorm}\left(\{r_j\}_{j=1}^{N}\right)$$

GRPO 是一种具有代表性的分组 RL 方法，它遵循这一原则，使用组的均值和方差对奖励进行归一化。这种无评论家设计简化了训练，非常适合大规模策略优化。

**问题设定。** 在多模态推理中，每个输入 $x = (I, Q)$ 由一张图像 $I$ 和一个查询 $Q$ 组成，每个候选答案 $y_i$ 同时包含推理链和最终答案。不同的候选答案可能依赖不同的视觉证据，我们将视觉证据表示为一组视觉物体 $S_i = g(x, y_i)$。然而，标准分组 RL 在整个组内归一化奖励，隐含地将所有候选答案视为可直接比较。当 $S_i \neq S_j$ 时，这种归一化无法对视觉证据提供精确的信用分配，导致对多模态推理的指导较为粗糙。因此，多模态场景下的分组 RL 需要对视觉证据进行更精确的处理，以支持可靠的多模态推理。

## 4. 方法

**动机。** 现有的多模态推理 RL 方法在最终答案层面优化奖励，尽管候选答案可能依赖不同的视觉证据。这限制了视觉证据上的信用分配，并加剧了幻觉和奖励作弊。我们通过两阶段计算优势来解决这一问题：一个来自最终答案监督的答案级外在优势，以及一个在引用相同视觉证据的答案的视觉物体组内计算的物体级内在优势。

**概述。** 如图 2 所示，我们提出 POLIA——一种用于多模态推理的视觉物体级内在优势策略优化方法。POLIA 采用两阶段优势形式化，同时在答案层面和视觉物体层面运作。通过在视觉物体上引入内在优势，POLIA 对视觉证据提供了更显式的信用分配。该设计使得在最终答案监督下进行更可靠的优化成为可能。

**图 2.** POLIA 概览。给定图像-查询输入，POLIA 采样一组候选答案（C），并根据外在奖励（R）计算答案级外在优势（A_ext）。然后，候选答案按照它们引用的视觉物体（o）进行分组，相同颜色表示同一个视觉物体。对于每个答案，R 由物体置信度（s）校正得到 r。视觉物体级内在优势（A_int）在每组视觉物体组内根据 r 计算。策略通过结合 A_ext 和 A_int 进行优化。

### 4.1. 答案级外在优势计算

给定图像-查询输入 $x = (I, Q)$，我们从当前策略 $\pi_\theta$ 采样一组 $N$ 个候选答案：$\{c_1, \ldots, c_N\} \sim \pi_\theta(\cdot \mid x)$。然后，我们为每个候选答案 $c_i$ 计算答案级外在奖励 $R(c_i)$：

$$R(c_i) = \lambda_{ans} R_{ans}(c_i) + \lambda_{fmt} R_{fmt}(c_i)$$

在实践中，$R(c_i)$ 由以下两部分组成：(i) 答案正确性项 $R_{ans}(c_i)$，衡量最终答案与真实答案之间的匹配程度。它提供主要的监督信号，直接与评估指标对齐；(ii) 格式有效性项 $R_{fmt}(c_i)$，强制执行推理链中视觉证据说明所需的坐标格式，这对于后续的视觉物体组构建是必要的。$\lambda_{ans}$、$\lambda_{fmt}$ 在整体目标中平衡这些组成部分。

遵循 GRPO，我们通过在组内对 $R(c_i)$ 进行归一化来计算外在优势 $A^{ext}_i$：

$$A^{ext}_i = \frac{R(c_i) - \frac{1}{N}\sum_{j=1}^{N} R(c_j)}{\text{std}\left(\{R(c_j)\}_{j=1}^{N}\right) + \delta}$$

其中 $\delta$ 是为数值稳定性设置的小常数。这种组内相对比较保留了无评论家策略优化的效率，并提供了稳定的答案级训练信号。然而，如上文所讨论的，当候选答案依赖不同的视觉证据时，答案级奖励变得不足，这促使我们进行显式且结构化的视觉证据建模。

### 4.2. 视觉证据建模

为了解决缺乏对视觉证据显式且结构化建模的问题，我们将每个候选答案所引用的视觉证据表示为一组视觉物体。这一设计受到人类图像解读习惯的启发，为在多模态推理中强调和比较视觉证据提供了显式的手段。具体而言，每个候选答案 $c_i$ 可能包含以预测边界框形式呈现的显式视觉引用。我们使用预定义的匹配规则，将每个预测框匹配到真实物体框，并将匹配到的物体身份表示为一个与顺序无关的集合：

$$S_i = \{o_{i,1}, \ldots, o_{i,m_i}\}$$

我们将 $S_i$ 视为 $c_i$ 所使用的视觉证据。在这种形式化下，只有两个候选答案诱发相同的物体集合时，才认为它们依赖相同的视觉证据。与将视觉信息保留为定义含糊的"视觉相关信息"相比，这种表示提供了对视觉证据显式且结构化的建模，并为在一致证据条件下的后续视觉物体组构建奠定了基础。

### 4.3. 视觉物体级内在优势计算

**视觉物体分组。** 给定每个候选答案 $c_i$ 所引用的视觉证据 $S_i$，我们根据候选答案依赖的视觉物体对其进行分组。具体而言，对于每个视觉证据 $S$，我们构建一个视觉物体组：

$$G_S = \{c_i \mid S_i = S\}$$

同一组内的候选答案依赖完全相同的视觉证据，因此在一致证据条件下被视为逻辑上可比较的。这种分组为组内比较和后续的奖励传播提供了结构化基础。

**基于置信度的视觉物体级奖励校正。** 对于候选答案 $c_i \in G_S$，我们考虑其引用的每个视觉物体 $o \in S_i$，并计算物体置信度分数 $s_{i,o} \in [0, 1]$，衡量 $c_i$ 引用 $o$ 的可靠程度。在我们的实现中，$s_{i,o}$ 由 $c_i$ 中预测边界框与物体 $o$ 的真实框之间的匹配质量推导而来，计算为 IoU 与归一化 L1 距离的加权组合，随后进行裁剪。我们定义每个视觉物体的校正后物体级奖励为：

$$r_{i,o} = R(c_i) \cdot s_{i,o}$$

**视觉物体级内在优势计算。** 我们通过比较同一视觉物体组内的 $r_{i,o}$，为每个物体计算内在优势 $A^{int}_{i,o}$。具体而言，对于每个视觉物体组 $G_S$ 和每个物体 $o \in S$，我们对 $\{r_{i,o}\}_{c_i \in G_S}$ 进行如下归一化：

$$A^{int}_{i,o} = \frac{r_{i,o} - \text{mean}_{j \in G_S}[r_{j,o}]}{\text{std}_{j \in G_S}[r_{j,o}] + \delta}, \quad c_i \in G_S, \ o \in S$$

其中 $\delta$ 是为数值稳定性设置的小常数。根据构造，$A^{int}_{i,o}$ 在引用相同视觉证据的自然形成的视觉物体组内计算。这种组内归一化建立了对每一条视觉证据的显式信用分配机制。因此，内在优势量化了每个视觉物体对最终答案的相对贡献，为策略优化提供物体级信号，并鼓励策略强调有效的视觉证据。

### 4.4. 整体策略优化

我们将答案级外在优势与物体级内在优势整合到统一的策略优化步骤中。具体而言，$A^{ext}_i$ 应用于推理链中的所有 token，包括文本 token 和坐标 token，而 $A^{int}_{i,o}$ 仅应用于与每个被引用的视觉物体 $o \in S_i$ 相对应的坐标 token，从而通过组内比较实现物体级更新。我们记 $\pi_{\theta_{old}}$ 为采样策略，$\pi_\theta$ 为更新后的策略。每个候选答案写成一个 token 序列 $c_i = (c_{i,1}, \ldots, c_{i,T_i})$（包括其推理链）。对于每个位置 $t$，前缀上下文为 $c_{i,1:t-1}$，由前 $t-1$ 个 token 组成。重要性比率定义为：

$$\rho_{i,t}(\theta) = \frac{\pi_\theta(c_{i,t} \mid x, c_{i,1:t-1})}{\pi_{\theta_{old}}(c_{i,t} \mid x, c_{i,1:t-1})}$$

我们采用带超参数 $\epsilon$ 的标准裁剪代理目标（clipped surrogate objective）以促进稳定的策略更新：

$$g(\rho, A) = \min\left(\rho A, \ \text{clip}(\rho, 1 - \epsilon, 1 + \epsilon)A\right)$$

**算法 1** POLIA 整体策略优化

**输入：** 初始策略 $\pi_{\theta_{old}}$，任务分布 $p(X)$，生成数量 $N$，KL 正则化系数 $\beta$，裁剪参数 $\epsilon$，外在奖励函数权重 $\{w_i\}$，内在优势权重 $\omega$

1. **for** 每个训练迭代 **do**
2. 更新旧策略：$\theta_{old} \leftarrow \theta$；
3. 采样输入批次 $x \sim p(X)$；
4. 生成 $N$ 个答案 $\{c_1, \ldots, c_N\} \sim \pi_\theta(\cdot \mid x)$；
5. 处理 grounding 信息并提取预测的边界框；
6. 计算加权外在奖励 $\{R(c_i)\}$；
7. 归一化奖励以计算外在优势 $\{A^{ext}_i\}$；
8. 将引用相同视觉物体组 $\{S_i\}$ 的候选答案 $c_i$ 分组为视觉物体组 $\{G_S\}$；
9. 使用视觉物体组 $\{G_S\}$ 内的物体置信度分数 $s_{i,o}$ 计算物体级内在优势 $\{A^{int}_i\}$；
10. 合并优势：$A_i \leftarrow A^{ext}_i + \omega A^{int}_i$；
11. 根据公式 (1) 更新策略 $\theta$；
12. **end for**

整体训练目标为：

$$\mathcal{L}(\theta) = -\mathbb{E}_x\left[\frac{1}{N}\sum_{i=1}^{N}\sum_{t \in T^{all}_i} g\left(\rho_{i,t}(\theta), \ A^{ext}_i + \omega\sum_{o \in S_i} \mathbb{I}\{t \in T^{box}_{i,o}\} A^{int}_{i,o}\right)\right] + \beta \, \text{KL}\left(\pi_{\theta_{old}} \| \pi_\theta\right) \tag{1}$$

其中 $T^{all}_i$ 表示 $c_i$ 的完整推理链 token 集合，$T^{box}_{i,o}$ 表示 $c_i$ 中引用物体 $o$ 的坐标 token，$\omega$ 是内在优势权重。我们在算法 1 中给出了伪代码。更多实现细节见附录 A.1。通过这种方式，外在优势在最终答案监督下鼓励高奖励答案，而内在优势通过视觉物体组内比较，为视觉证据提供显式的信用分配信号。这种统一更新保留了分组 RL 的效率，并增强了提取和利用有效视觉证据的学习信号。

## 5. 实验

在本节中，我们在广泛使用的多模态推理基准上评估 POLIA，重点关注以下研究问题（RQ）。

- **RQ1：** 在多模态推理基准上，POLIA 与代表性基线相比表现如何？
- **RQ2：** 外在优势和内在优势如何影响 POLIA 的学习动态？
- **RQ3：** 在训练过程中，POLIA 是否促使视觉物体组变得更加稳定和一致？
- **RQ4：** 与 GRPO 相比，POLIA 带来了多少额外的计算开销？

**表 1.** POLIA 与具有代表性的闭源和开源 MLLM 在答案准确率（ACC，%）上的性能对比。最佳得分以粗体表示，次佳得分以下划线表示。平均提升（Average Improvements）表示 POLIA 与相同参数规模的基线模型之间的平均相对性能差异。带 + 的分数取自相应模型的官方报告。

| 模型 | VSR | TallyQA | GQA | MathVista | MathVision | LogicVista | MME |
|---|---|---|---|---|---|---|---|
| **闭源模型** | | | | | | | |
| GPT-4o | 62.3 | 38.9 | 52.2 | 60.6 | 30.4+ | 52.3 | 83.5 |
| Gemini2.5-pro | 64.0 | 49.8 | 60.5 | 54.1 | 73.3+ | 73.8+ | 92.9 |
| **开源模型（7B）** | | | | | | | |
| Qwen2.5-VL | 41.3 | 48.0 | 33.9 | 48.8 | 25.1 | 44.5 | 92.9 |
| Qwen2.5-VL+DAPO | 60.7 | 52.8 | 58.8 | 61.9+ | 27.3+ | 47.5+ | 92.2 |
| Qwen2.5-VL+GRPO | 59.0 | 48.0 | 58.2 | 65.5+ | 26.3+ | 47.1+ | 92.6 |
| **POLIA** | **81.3** | **56.7** | **69.5** | **74.8** | **29.4** | **48.7** | **93.3** |
| 平均提升 | 27.6 ↑ | 7.1 ↑ | 19.2 ↑ | 16.1 ↑ | 3.2 ↑ | 2.3 ↑ | 0.7 ↑ |
| **开源模型（≤3B）** | | | | | | | |
| InternVL3-2B | 52.9+ | 15.5+ | 29.4+ | 43.0+ | 21.7+ | 36.9+ | 40.0+ |
| Qwen2.5-VL-3B | 49.5 | 40.8 | 20.1 | 56.0 | 9.8 | 28.5 | 88.6 |
| Chain-of-Thought-3B | 37.5+ | 33.2+ | 39.5+ | 33.0+ | 20.0 | 38.1 | 41.3+ |
| One-shot ICL-3B | 13.2+ | 36.3+ | 20.4+ | 29.1+ | 12.2 | 18.3 | 24.7+ |
| Few-shot fine-tuning-3B | 59.7+ | 44.5+ | 64.6+ | 45.0+ | 12.8 | 17.0 | 68.3+ |
| GRIT-3B | 61.2 | 43.6 | 57.9 | 56.2 | 12.3 | 39.4 | 85.4 |
| Qwen2.5-VL+DAPO-3B | 53.9 | 43.4 | 54.9 | 61.5 | 22.3 | 39.3 | 88.4 |
| Qwen2.5-VL+GRPO-3B | 53.5 | 41.6 | 57.1 | 62.4 | 24.4 | 38.5+ | 88.3 |
| **POLIA-3B** | **71.9** | **48.8** | **60.2** | **63.9** | **24.5** | **40.4** | **89.2** |
| 平均提升 | 24.2 ↑ | 11.4 ↑ | 17.2 ↑ | 15.6 ↑ | 7.6 ↑ | 8.4 ↑ | 23.6 ↑ |

### 5.1. 实验设置

**数据集。** 我们在七个广泛使用的多模态推理基准上评估 POLIA：VSR（Liu et al., 2023）、TallyQA（Acharya et al., 2019）、GQA（Hudson & Manning, 2019）、MathVista（Lu et al., 2023）、MathVision（Wang et al., 2024）、LogicVista（Xiao et al., 2024）和 MME（Fu et al., 2025）。这些基准既涵盖物理感知（例如复杂物体计数和空间关系理解），也涵盖视觉数学推理（例如数学与逻辑推理）。数据预处理的更多细节见附录 B。

**基线。** 我们将 POLIA 与覆盖 MLLM 常见训练策略的代表性基线进行比较。对于 7B 设置，我们采用 Qwen2.5-VL-7B-Instruct 作为基础模型，并纳入 GRPO 风格的 RL 基线（Qwen2.5-VL+GRPO、Qwen2.5-VL+DAPO）以进行公平比较。对于 3B 设置，我们将基线分为两类：(i) 非 RL 基线，包括 InternVL3-2B、Qwen2.5-VL-3B-Instruct、one-shot ICL、chain-of-thought 和 few-shot fine-tuning；(ii) RL 基线，包括 Qwen2.5-VL+GRPO-3B、Qwen2.5-VL+DAPO-3B，以及强调在优化过程中使用视觉证据的 GRIT-3B。我们还报告了强大的闭源模型（GPT-4o、Gemini2.5-pro）作为参考点。

**评估指标。** 遵循先前的工作，我们使用基于 GPT 的评判器来评估答案准确率（Fan et al., 2025）。由于模型输出是自由形式的自然语言，可能包含改写，自动字符串匹配是不够的；因此，我们采用 GPT-as-a-judge 协议，侧重于语义正确性而非精确字符串匹配。具体而言，我们使用 GPT-4o 将生成的答案与基准参考答案进行比较，并产生一个在 [0, 1] 范围内的答案准确率分数，其中 0 表示答案不正确，1 表示答案完全正确。我们在每个基准上报告平均分数作为主要评估指标。相关细节见附录 C.2。

### 5.2. 与基线的性能比较（RQ1）

表 1 显示了比较结果。闭源模型仍然强大，而开源基础模型落后，凸显了在仅结果监督下进行多模态推理的难度。值得注意的是，在需要精确视觉接地的基准（VSR、GQA、TallyQA）上，POLIA-7B 同时优于 GPT-4o 和 Gemini2.5-pro，反映了它在有效利用视觉证据方面的优势。

GRPO 风格的分组 RL（GRPO/DAPO）相比基础模型带来了明显的提升，但其答案级优化对视觉证据的信用分配仍然有限。相比之下，POLIA 在各个基准上始终超越 GRPO/DAPO，尤其是在需要精确视觉证据的任务上。具体而言，在 7B 设置下，POLIA 相比 GRPO 将 VSR 提升了 +22.3%，TallyQA 提升了 +8.7%，GQA 提升了 +11.3%，同时还将 MathVista 提升了 +9.3%。对于较小模型，POLIA-3B 同样优于 RL 基线（例如 VSR +18.4%；TallyQA +7.2%），而 SFT 在 GQA 上略高，反映了直接答案监督在该数据集上的优势。此外，值得注意的是，POLIA 仅在 VSR 和 TallyQA 上以有限的监督进行训练，却表现出强劲的性能，详见附录 A.2。尽管如此，在广泛评估任务上观察到的改进表明，POLIA 在训练基准之外展现出一定程度的泛化能力。

总体而言，这些结果表明，在策略优化过程中强化视觉证据的信用分配，能够在以感知为中心和以推理为中心的基准上（如 MME 所反映的）带来稳健的提升。

### 5.3. 两种优势的消融研究（RQ2）

为了考察外在优势和内在优势如何影响 POLIA 的训练动态，我们进行了消融研究，并在 VSR 和 TallyQA 上追踪一个结合了答案正确性与推理格式有效性的归一化训练奖励随训练迭代的变化。如图 3 所示，两个数据集上观察到一致的趋势：去除外在优势（w/o A_ext）导致最低的奖励和最慢的提升，表明外在优势对于稳定优化至关重要；去除内在优势（w/o A_int）产生的动态显著优于去除外在优势的情况，但在收敛速度和最终奖励平台两方面仍落后于完整方法。这表明，虽然外在优势驱动有效的全局优化，但内在优势通过在每个视觉物体组内提供物体级指导来补充它，改善了视觉证据上的信用分配。

总体而言，这些结果表明，POLIA 通过将稳定的全局学习与改进的视觉证据信用分配相结合，产生了最有效的训练动态。

### 5.4. 视觉物体组数量的收敛分析（RQ3）

我们设计了这一系列实验，以考察 POLIA 是否促使视觉物体组在训练过程中变得更加一致，以及这种收敛是否与准确率共同演化。在这里，采样的候选答案按照它们依赖的视觉物体集合进行分组。视觉物体组的数量被计为采样答案中出现的不同视觉物体集合的数量；数值越小，表明越多的答案依赖一致的视觉证据。我们从物体数量较多的 TallyQA 中随机采样，在训练初期，那里的视觉证据选择更可能不一致，使视觉物体组的变化更容易被观察到。我们追踪不同生成数量 $N \in \{8, 16, 24\}$ 下，训练迭代 $\{0, 25, 50, 75, 100\}$ 中平均视觉物体组数量和答案准确率的演化。我们进一步报告各样本间视觉物体组数量的标准差，以衡量视觉证据选择的稳定性。

**图 3.** 消融研究的训练曲线。y 轴显示用于训练的归一化奖励。曲线在多次运行上取平均，并报告 95% 置信区间。(a) VSR 上的消融结果；(b) TallyQA 上的消融结果。

**图 4.** 不同生成数量（N）下，视觉物体组平均数量（左轴）与答案准确率（右轴）随训练迭代的演化。

**视觉物体组数量与准确率之间的关系。** 如图 4 所示，在第 0 次迭代时，视觉物体组的数量很高，表明候选答案在引用哪些物体作为视觉证据方面存在显著分歧。随着训练的进行，视觉物体组的数量持续减少，在第 50 次迭代之前迅速下降，随后趋于稳定，表明优化将许多看似合理但不一致的视觉证据压缩为更小的一组一致证据。这种行为表明，优化逐步消解了视觉证据选择中的歧义，将多个看似合理但相互冲突的证据选择过滤为被大多数候选答案采用的更小且更一致的集合。

与此同时，ACC 上升并在较晚阶段趋于饱和，表明视觉物体组的收敛与答案正确性的提升共同演化。改变生成数量进一步凸显了探索-利用的权衡：$N = 8$ 产生的 ACC 明显低于 $N \in \{16, 24\}$，而 $N \in \{16, 24\}$ 的结果相近，表明探索不足会限制性能，但一旦候选答案的多样性充分，收益就会递减。

**图 5.** 视觉证据选择的稳定性。阴影区域表示不同生成数量（N）下，各样本间视觉物体组数量的标准差（左轴）随训练迭代的变化，准确率在右轴报告。(a) N = 8；(b) N = 16；(c) N = 24。

**视觉证据选择的稳定性。** 如图 5 所示，在所有 N 下，视觉物体组数量的标准差都随着其均值一起下降，表明证据分歧在不同样本间的波动变小，证据选择更加可预测和稳健。标准差的减小在训练早期阶段更大，后期逐渐放缓，这与两阶段优化过程一致：在早期阶段，模型快速抑制导致分歧推理行为的高度不一致证据；在后期阶段，随着视觉物体组数量趋于稳定，训练主要集中于解决剩余的模糊情况，随着接近收敛，变化变得更小。最后，通过在 $N = 8$ 时去除内在优势，我们观察到视觉物体组的数量与完整方法相比增加了 50%，这表明内在优势在促进视觉物体组收敛和稳定证据选择方面发挥着重要作用。

### 5.5. 计算成本分析（RQ4）

为了展示 POLIA 的效率，我们将训练过程分解为几个部分。我们的方法建立在 GRPO 框架之上，保持无评论家架构，但引入了两个额外的步骤：分组（Grouping）和 $A^{int}$ 的计算（详见第 4.3 节）。我们对 POLIA-3B 的每次迭代训练时间进行了基准测试。如图 6 所示，Rollout 阶段是主要的瓶颈，消耗总时间的 536.25 秒（97.24%）。这种高延迟主要归因于思考过程，模型必须生成 2D 边界框。相比之下，新引入的组件带来的开销可忽略不计：$A^{int}$ 的计算仅占 0.002 秒，而分组几乎瞬时完成。这些结果表明，我们的方法在几乎不影响训练效率的情况下大幅提升了模型性能。

**图 6.** POLIA 的每迭代训练时间分解。黄色条表示与 GRPO 基线共享的组件，红色条代表 POLIA 特有的新增部分（A_int 和 Grouping）。y 轴使用两个断开的刻度以适应小数值。

## 6. 结论

多模态推理的目标是使模型能够通过利用视觉证据进行正确推理。然而，现有的分组 RL 方法主要优化答案级外在奖励，缺乏对视觉物体的显式信用分配，这限制了它们调节推理过程中视觉证据使用方式的能力。在本文中，我们旨在通过改进多模态 RL 中对视觉物体的信用分配来解决这一局限。我们提出 POLIA，一种在视觉物体上定义内在优势的分组 RL 方法。在多样化多模态推理基准上的实验证明了其有效性。我们相信多模态 RL 中仍有大量尚未探索的空间。

## 致谢

本工作受广东省基础与应用基础研究基金（No. 2025A1515010247）、CCF-快手大模型探索者基金（No. CCF-KuaiShou 2025004）以及国家自然科学基金（No. 62506133）资助。

## 影响声明

本文所呈现的工作旨在推动机器学习领域的发展，特别是在多模态推理和强化学习方面。虽然多模态推理的进展可能具有更广泛的社会影响，例如提升视觉-语言系统的性能，但我们预计除机器学习研究通常伴随的影响外，本工作不会产生任何直接的伦理问题或负面社会影响。

## 参考文献

Acharya, M., Kafle, K., and Kanan, C. Tallyqa: Answering complex counting questions. In Proceedings of the AAAI conference on artificial intelligence, volume 33, pp. 8076–8084, 2019.

Bai, Z., Wang, P., Xiao, T., He, T., Han, Z., Zhang, Z., and Shou, M. Z. Hallucination of multimodal large language models: A survey. arXiv preprint arXiv:2404.18930, 2024.

Cao, M., Zhao, H., Zhang, C., Chang, X., Reid, I., and Liang, X. Ground-r1: Incentivizing grounded visual reasoning via reinforcement learning. arXiv preprint arXiv:2505.20272, 2025.

Fan, Y., He, X., Yang, D., Zheng, K., Kuo, C.-C., Zheng, Y., Narayanaraju, S. J., Guan, X., and Wang, X. E. Grit: Teaching mllms to think with images. arXiv preprint arXiv:2505.15879, 2025.

Fu, C., Chen, P., Shen, Y., Qin, Y., Zhang, M., Lin, X., Yang, J., Zheng, X., Li, K., Sun, X., et al. Mme: A comprehensive evaluation benchmark for multimodal large language models. In The Thirty-ninth Annual Conference on Neural Information Processing Systems Datasets and Benchmarks Track, 2025.

Gu, J., Jiang, X., Shi, Z., Tan, H., Zhai, X., Xu, C., Li, W., Shen, Y., Ma, S., Liu, H., et al. A survey on llm-as-a-judge. The Innovation, 2024.

Guo, P., Wang, J., Qiang, W., Zhou, J., Zheng, C., and Hua, G. Copo: Causal-oriented policy optimization for hallucinations of mllms. arXiv preprint arXiv:2508.04182, 2025.

Huang, W., Jia, B., Zhai, Z., Cao, S., Ye, Z., Zhao, F., Xu, Z., Hu, Y., and Lin, S. Vision-r1: Incentivizing reasoning capability in multimodal large language models. arXiv preprint arXiv:2503.06749, 2025.

Hudson, D. A. and Manning, C. D. Gqa: A new dataset for real-world visual reasoning and compositional question answering. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pp. 6700–6709, 2019.

Li, Z., Luo, R., Zhang, J., Qiu, M., Huang, X.-J., and Wei, Z. Vocot: Unleashing visually grounded multi-step reasoning in large multi-modal models. In Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), pp. 3769–3798, 2025.

Liu, F., Emerson, G., and Collier, N. Visual spatial reasoning. Transactions of the Association for Computational Linguistics, 11:635–651, 2023.

Liu, Z., Chen, C., Li, W., Qi, P., Pang, T., Du, C., Lee, W. S., and Lin, M. Understanding r1-zero-like training: A critical perspective. arXiv preprint arXiv:2503.20783, 2025a.

Liu, Z., Sun, Z., Zang, Y., Dong, X., Cao, Y., Duan, H., Lin, D., and Wang, J. Visual-rft: Visual reinforcement fine-tuning. arXiv preprint arXiv:2503.01785, 2025b.

Lu, P., Bansal, H., Xia, T., Liu, J., Li, C., Hajishirzi, H., Cheng, H., Chang, K.-W., Galley, M., and Gao, J. Mathvista: Evaluating mathematical reasoning of foundation models in visual contexts. arXiv preprint arXiv:2310.02255, 2023.

Meng, F., Du, L., Liu, Z., Zhou, Z., Lu, Q., Fu, D., Han, T., Shi, B., Wang, W., He, J., et al. Mm-eureka: Exploring the frontiers of multimodal reasoning with rule-based reinforcement learning. arXiv preprint arXiv:2503.07365, 2025.

Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C., Mishkin, P., Zhang, C., Agarwal, S., Slama, K., Ray, A., et al. Training language models to follow instructions with human feedback. Advances in neural information processing systems, 35:27730–27744, 2022.

Peng, Y., Wang, P., Wang, X., Wei, Y., Pei, J., Qiu, W., Jian, A., Hao, Y., Pan, J., Xie, T., et al. Skywork r1v: Pioneering multimodal reasoning with chain-of-thought. arXiv preprint arXiv:2504.05599, 2025.

Peng, Z., Wang, W., Dong, L., Hao, Y., Huang, S., Ma, S., and Wei, F. Kosmos-2: Grounding multimodal large language models to the world. arXiv preprint arXiv:2306.14824, 2023.

Qi, J., Ding, M., Wang, W., Bai, Y., Lv, Q., Hong, W., Xu, B., Hou, L., Li, J., Dong, Y., et al. Cogcom: A visual language model with chain-of-manipulations reasoning. arXiv preprint arXiv:2402.04236, 2024.

Rafailov, R., Sharma, A., Mitchell, E., Manning, C. D., Ermon, S., and Finn, C. Direct preference optimization: Your language model is secretly a reward model. Advances in neural information processing systems, 36:53728–53741, 2023.

Sarch, G., Saha, S., Khandelwal, N., Jain, A., Tarr, M. J., Kumar, A., and Fragkiadaki, K. Grounded reinforcement learning for visual reasoning. arXiv preprint arXiv:2505.23678, 2025.

Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and Klimov, O. Proximal policy optimization algorithms. arXiv preprint arXiv:1707.06347, 2017.

Shao, H., Qian, S., Xiao, H., Song, G., Zong, Z., Wang, L., Liu, Y., and Li, H. Visual cot: Advancing multimodal language models with a comprehensive dataset and benchmark for chain-of-thought reasoning. Advances in Neural Information Processing Systems, 37:8612–8642, 2024a.

Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang, H., Zhang, M., Li, Y., Wu, Y., et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300, 2024b.

Shen, H., Liu, P., Li, J., Fang, C., Ma, Y., Liao, J., Shen, Q., Zhang, Z., Zhao, K., Zhang, Q., et al. Vlm-r1: A stable and generalizable r1-style large vision-language model. arXiv preprint arXiv:2504.07615, 2025.

Shrivastava, V., Awadallah, A., Balachandran, V., Garg, S., Behl, H., and Papailiopoulos, D. Sample more to think less: Group filtered policy optimization for concise reasoning. arXiv preprint arXiv:2508.09726, 2025.

Stiennon, N., Ouyang, L., Wu, J., Ziegler, D., Lowe, R., Voss, C., Radford, A., Amodei, D., and Christiano, P. F. Learning to summarize with human feedback. Advances in neural information processing systems, 33:3008–3021, 2020.

Tu, S., Zhang, Q., Sun, J., Fu, Y., Li, L., Lan, X., Jiang, D., Wang, Y., and Zhao, D. Perception-consistency multimodal large language models reasoning via caption-regularized policy optimization. arXiv preprint arXiv:2509.21854, 2025.

Wang, H., Su, A., Ren, W., Lin, F., and Chen, W. Pixel reasoner: Incentivizing pixel-space reasoning with curiosity-driven reinforcement learning. arXiv preprint arXiv:2505.15966, 2025a.

Wang, K., Pan, J., Shi, W., Lu, Z., Ren, H., Zhou, A., Zhan, M., and Li, H. Measuring multimodal mathematical reasoning with math-vision dataset. Advances in Neural Information Processing Systems, 37:95095–95169, 2024.

Wang, P., Wei, Y., Peng, Y., Wang, X., Qiu, W., Shen, W., Xie, T., Pei, J., Zhang, J., Hao, Y., et al. Skywork r1v2: Multimodal hybrid reinforcement learning for reasoning. arXiv preprint arXiv:2504.16656, 2025b.

Wang, Y., Yang, Q., Zeng, Z., Ren, L., Liu, L., Peng, B., Cheng, H., He, X., Wang, K., Gao, J., et al. Reinforcement learning for reasoning in large language models with one training example. arXiv preprint arXiv:2504.20571, 2025c.

Wang, Z., Guo, X., Stoica, S., Xu, H., Wang, H., Ha, H., Chen, X., Chen, Y., Yan, M., Huang, F., et al. Perception-aware policy optimization for multimodal reasoning. arXiv preprint arXiv:2507.06448, 2025d.

Wu, M., Yang, J., Jiang, J., Li, M., Yan, K., Yu, H., Zhang, M., Zhai, C., and Nahrstedt, K. Vtool-r1: Vlms learn to think with images via reinforcement learning on multimodal tool use. arXiv preprint arXiv:2505.19255, 2025a.

Wu, W., Gao, C., Chen, J., Lin, K. Q., Meng, Q., Zhang, Y., Qiu, Y., Zhou, H., and Shou, M. Z. Reinforcement learning for large model: A survey. arXiv preprint arXiv:2508.08189, 2025b.

Xia, J., Zang, Y., Gao, P., Li, S., and Zhou, K. Visionary-r1: Mitigating shortcuts in visual reasoning with reinforcement learning. arXiv preprint arXiv:2505.14677, 2025.

Xiao, Y., Sun, E., Liu, T., and Wang, W. Logicvista: Multimodal llm logical reasoning benchmark in visual contexts. arXiv preprint arXiv:2407.04973, 2024.

Xu, S., Li, Y., Yang, R., Zhang, T., Sun, Y., Chow, W., Li, L., Song, H., Xu, Q., Tong, Y., et al. Mixed-r1: Unified reward perspective for reasoning capability in multimodal large language models. arXiv preprint arXiv:2505.24164, 2025.

Yang, Y., He, X., Pan, H., Jiang, X., Deng, Y., Yang, X., Lu, H., Yin, D., Rao, F., Zhu, M., et al. R1-onevision: Advancing generalized multimodal reasoning through cross-modal formalization. arXiv preprint arXiv:2503.10615, 2025.

Yin, S., Fu, C., Zhao, S., Li, K., Sun, X., Xu, T., and Chen, E. A survey on multimodal large language models. National Science Review, 11(12):nwae403, 2024.

Yu, E., Lin, K., Zhao, L., Yin, J., Wei, Y., Peng, Y., Wei, H., Sun, J., Han, C., Ge, Z., et al. Perception-r1: Pioneering perception policy with reinforcement learning. arXiv preprint arXiv:2504.07954, 2025a.

Yu, Q., Zhang, Z., Zhu, R., Yuan, Y., Zuo, X., Yue, Y., Dai, W., Fan, T., Liu, G., Liu, L., et al. Dapo: An open-source llm reinforcement learning system at scale. arXiv preprint arXiv:2503.14476, 2025b.

Zhang, C., Qiu, H., Zhang, Q., Xu, Y., Zeng, Z., Yang, S., Shi, P., Ma, L., and Zhang, J. Perceptual-evidence anchored reinforced learning for multimodal reasoning. arXiv preprint arXiv:2511.18437, 2025a.

Zhang, J., Huang, J., Yao, H., Liu, S., Zhang, X., Lu, S., and Tao, D. R1-vl: Learning to reason with multimodal large language models via step-wise group relative policy optimization. arXiv preprint arXiv:2503.12937, 2025b.

Zhang, K., Zuo, Y., He, B., Sun, Y., Liu, R., Jiang, C., Fan, Y., Tian, K., Jia, G., Li, P., et al. A survey of reinforcement learning for large reasoning models. arXiv preprint arXiv:2509.08827, 2025c.

Zhang, X., Gao, Z., Zhang, B., Li, P., Zhang, X., Liu, Y., Yuan, T., Wu, Y., Jia, Y., Zhu, S.-C., et al. Chain-of-focus: Adaptive visual search and zooming for multimodal reasoning via rl. arXiv preprint arXiv:2505.15436, 2025d.

Zhang, Z., Zhang, A., Li, M., Zhao, H., Karypis, G., and Smola, A. Multimodal chain-of-thought reasoning in language models. arXiv preprint arXiv:2302.00923, 2023.

Zhao, Y., Liu, Y., Liu, J., Chen, J., Wu, X., Hao, Y., Lv, T., Huang, S., Cui, L., Ye, Q., et al. Geometric-mean policy optimization. arXiv preprint arXiv:2507.20673, 2025.

Zheng, C., Liu, S., Li, M., Chen, X.-H., Yu, B., Gao, C., Dang, K., Liu, Y., Men, R., Yang, A., et al. Group sequence policy optimization. arXiv preprint arXiv:2507.18071, 2025a.

Zheng, Z., Yang, M., Hong, J., Zhao, C., Xu, G., Yang, L., Shen, C., and Yu, X. Deepeyes: Incentivizing" thinking with images" via reinforcement learning. arXiv preprint arXiv:2505.14362, 2025b.

Zhou, G., Qiu, P., Chen, C., Wang, J., Yang, Z., Xu, J., and Qiu, M. Reinforced mllm: A survey on rl-based reasoning in multimodal large language models. arXiv preprint arXiv:2504.21277, 2025.

Zhu, J., Wang, W., Chen, Z., Liu, Z., Ye, S., Gu, L., Tian, H., Duan, Y., Su, W., Shao, J., et al. Internvl3: Exploring advanced training and test-time recipes for open-source multimodal models. arXiv preprint arXiv:2504.10479, 2025.

Ziegler, D. M., Stiennon, N., Wu, J., Brown, T. B., Radford, A., Amodei, D., Christiano, P., and Irving, G. Fine-tuning language models from human preferences. arXiv preprint arXiv:1909.08593, 2019.

## A. 实验细节

### A.1. 实验设置

我们使用带学习率调度器的 AdamW 优化器，并将学习率设置为 $2 \times 10^{-6}$。实验在 NVIDIA A100 GPU（40GB）上进行。对于 POLIA-3B，训练使用每设备批大小为 8，梯度累积步数为 4。对于每个输入，我们采样一组 $N = 16$ 个候选答案。对于 POLIA-7B，训练使用每设备批大小为 3，梯度累积步数为 2。对于每个输入，我们采样一组 $N = 9$ 个候选答案。为了计算内在优势，当预测边界框的交并比（IoU）超过 0.5 时，该边界框被视为成功。奖励信号定义为加权和，其中 IoU 项的权重为 0.7，L1 项的权重为 0.3。对于最终的优势估计，子图集优势（sub-graph set advantage）和基于 GPT 的评分的系数分别设置为 1.0 和 1.5，而所有其他奖励分量使用默认权重 1.0。

### A.2. 数据使用

我们进一步说明用于训练 POLIA 的监督设置。在我们的实验中，POLIA 在受限的物体级监督设置下训练，而非依赖大规模标注数据。尽管训练设置受限，POLIA 在多样化的多模态推理基准上仍展现出持续的性能提升。虽然我们不旨在对数据效率提出强力主张，但这一观察表明，POLIA 的学习行为并不严重依赖大量的物体级标注。

## B. 数据集细节

### B.1. VSR

VSR（Liu et al., 2023）包含空间关系验证任务。我们的训练和评估数据来自 Visual CoT 基准（Shao et al., 2024a）的 VSR 子集。VSR 子集位于关系推理（Relation Reasoning）类别中，与我们的工作特别相关。它聚焦于空间关系验证这一基础任务，要求模型评估场景中物体之间空间关系（例如"在…左边"、"在…里面"、"在…下面"）的有效性。对于每个 VSR 三元组（问题-图像-答案），数据集提供了所涉及实体的精确真实边界框。这确保模型必须展示准确的视觉接地——识别物体的精确位置——之后才能执行高层的空间推理。该任务挑战模型解决多样化真实世界图像中复杂且往往微妙的空间布局。

为了提高训练质量，我们对数据集进行了若干手动调整。我们首先过滤掉包含模糊或主观答案的样本，以确保确定性的训练信号。此外，我们略微调整了训练集中边界框的尺寸。这一修改有助于模型更好地捕捉目标物体，从而在训练过程中增强其视觉接地性能。在评估阶段，模型仅被提供问题-图像-答案三元组。推理期间没有可用的边界框信息。这种设置迫使模型完全依赖其学习到的接地和推理能力来验证空间关系，而无需任何外部视觉线索。如表 1 所示，我们使用了源自某篇论文（Fan et al., 2025）的一小部分数据。

**图 7.** 来自 VSR 数据集的示例。

### B.2. TallyQA

TallyQA（Acharya et al., 2019）是一个旨在评估视觉问答（VQA）背景下开放式计数能力的基准。与主要依赖基本物体检测的标准计数任务不同，TallyQA 区分简单和复杂计数问题。复杂类别是我们研究特别感兴趣的，它要求模型推理物体之间错综复杂的关系、识别特定的视觉属性并整合上下文信息（例如，水槽左侧有多少个条纹容器？）。通过利用来自 Visual Genome 和 VQA v2.0 的多样化图像，该基准为评估模型在真实世界场景中执行高层数值推理和细粒度视觉接地的能力提供了严格的环境。

与我们对 VSR 的处理方式一致，我们对 TallyQA 数据集应用相同的处理方法来增强模型的接地和推理能力，同时减少标签噪声。对于训练集，我们手动过滤掉模糊样本并调整边界框尺寸，以更好地监督模型的注意力。在评估阶段，我们仅使用问题-图像-答案三元组，要求模型在无边界框信息辅助的情况下验证数值关系。如表 1 所示，我们使用了源自某篇论文（Fan et al., 2025）的一小部分数据。

**图 8.** 来自 TallyQA 数据集的示例。

### B.3. GQA

GQA（Hudson & Manning, 2019）是一个为真实世界视觉推理和组合式问答设计的大规模基准。与传统的 VQA 数据集不同，GQA 利用 Visual Genome 的结构化场景图来创建具有复杂逻辑依赖关系的问题。这些问题要求模型执行多步推理，包括物体定位、属性识别以及对错综复杂空间关系的理解。该数据集的优势在于它能够评估模型是否真正能够对场景进行推理，而不是依赖统计偏差。

经过简单的手动优化，我们过滤掉模糊样本以保持数据质量。在评估期间，模型仅被提供图像和问题。如表 1 所示，我们使用了源自某篇论文（Fan et al., 2025）的一小部分数据。

**图 9.** 来自 GQA 数据集的示例。

### B.4. MathVista

MathVista（Lu et al., 2023）是一个专门用于评估视觉背景下数学推理的综合性基准。它整合了 28 个现有的多模态数据集并引入了三个新的专门数据集（IQTest、FunctionQA 和 PaperQA），共包含 6,141 个示例。该基准覆盖广泛的数学领域，包括基础算术、几何、代数推理和统计分析，全部通过图表、示意图和几何形状等多样化的视觉形式呈现。与标准 VQA 任务不同，MathVista 要求模型执行细粒度视觉感知与多步组合推理的结合，这对当前 MLLM 构成了重大挑战。

我们仅将 MathVista 用于测试目的，不涉及任何训练。通过仅保留必要的视觉和文本组件（图像、问题和答案），我们挑战模型独立解决复杂的数学任务。评估在不使用外部提示或空间提示的情况下进行，以确保结果反映模型真实的推理深度。如表 1 所示，我们使用了源自某些论文（Fan et al., 2025; Wang et al., 2025d）的一小部分数据。

**图 10.** 来自 MathVista 数据集的示例。

### B.5. MathVision

MathVision（Wang et al., 2024）是一个精心整理的视觉数学基准，包含从真实世界数学竞赛中收集的 3,040 个高质量问题。该数据集涵盖 16 个不同的逻辑学科——包括平面与立体几何、函数变换和组合数学——并划分为五个难度级别。与先前的基准不同，MathVision 强调复杂数学理论与多样化视觉表示的整合。每个问题都要求模型准确感知错综复杂的几何结构或数学符号，并执行多步逻辑推理以得出解决方案，为现代 MLLM 的数学推理能力提供了严格的测试。

对于 MathVision，我们的实验仅限于评估阶段。数据集被简化为其最基本的形式——图像、查询和真实答案的三元组，以消除来自元数据的任何潜在信息泄漏。因此，模型必须自主完成推理过程，在推理期间无法访问边界框或补充提示。如表 1 所示，我们使用了源自某些论文（Wang et al., 2024; 2025d; Zhu et al., 2025）的一小部分数据。

**图 11.** 来自 MathVision 数据集的示例。

### B.6. LogicVista

LogicVista（Xiao et al., 2024）是一个专注于视觉背景下多模态大语言模型逻辑推理能力的评估基准。它包含 448 个高质量的选择题，涵盖 5 项核心逻辑推理任务和 9 种不同的能力，例如演绎推理、数值逻辑和空间谜题。该数据集被独特地设计用于评估模型如何将视觉感知与复杂的认知任务（如导航和谜题求解）相结合。每个条目都经过精心标注，带有人类书写的推理链，为评估 MLLM 在具有挑战性的真实世界场景中的准确性和逻辑一致性提供了严格的标准。

LogicVista 仅被用作盲测集。我们将输入简化为基本的图像-问题对，以评估模型的逻辑一致性。为了维持公平且具有挑战性的环境，禁止模型使用任何边界框辅助，要求其完全独立地解读视觉上下文和逻辑约束。如表 1 所示，我们使用了源自某些论文（Wang et al., 2025d; Zhu et al., 2025）的一小部分数据。

**图 12.** 来自 LogicVista 数据集的示例。

### B.7. MME

MME（Fu et al., 2025）是一个旨在评估多模态大语言模型（MLLM）多方面能力的综合性基准。它共涵盖 14 个子任务，系统性地分为两个维度：感知和认知。感知维度评估模型识别物体、计数和空间位置的能力，而认知维度则以常识推理、数值计算和代码识别等更高层次的任务挑战模型。MME 的一个显著特点是所有指令-答案对都是人工设计的，而非直接取自公共数据集，这有效防止了数据泄漏，并确保对模型真实泛化能力进行更严格的评估。

在我们的研究中，MME 仅用于评估。我们手动过滤数据集，以确保所有测试样本提供清晰且确定的信号。在评估阶段，模型仅被提供图像和问题。它必须完全依靠自身的感知和推理能力来生成答案，不借助边界框或任何额外的视觉线索。如表 1 所示，我们使用了源自某篇论文（Fan et al., 2025）的一小部分数据。

**图 13.** 来自 MME 数据集的示例。

## C. 提示词

### C.1. 生成边界框的提示词

如图 14 所示，我们设计了一个专门的提示词以促进边界框的生成，从而有效整合模型的接地与推理能力。具体而言，我们加入明确的指令"2D 边界框"以引导模型生成空间坐标。此外，通过提供格式模板 [x min, y min, x max, y max]，我们确保模型遵循正确的输出规则，并更准确地捕捉图像中的物体。这种提示策略在训练和测试阶段均一致采用。

**图 14.** 该模板指示模型首先在 ⟨think⟩ 标签内以特定的 JSON 格式 [x min, y min, x max, y max] 生成 2D 边界框。随后，模型被引导基于这些空间坐标重新审视其逻辑，再在答案标签后给出简洁的最终 ⟨answer⟩。

### C.2. 评分提示词

通过 GPT-4o 进行的评估如下所述。为了确保稳健且客观的评估，我们利用 GPT-4o 作为自动评估器对模型性能进行评分。具体而言，我们采用 GRIT（Fan et al., 2025）中的评估提示词，它有助于在模型的输出与真实答案之间进行比较。详细的评分模板和标准如图 15 所示。这种方法可以对模型的推理准确性进行一致且细粒度的分析。

## D. 更多示例

**图 15.** 基于 GPT-4o 的评估评分提示词。遵循 GRIT（Fan et al., 2025）中的协议，该提示词指示 GPT-4o 扮演公正的评判者。它评估模型预测与真实答案之间的对齐程度，并根据推理的正确性和完整性分配 0.0 到 1.0 之间的分数。

**图 16.** 在思考（Think）阶段，模型生成物体检测边界框以识别相关组件。在重新思考（Rethink）阶段，它综合这些空间信息形成逻辑结论，最终产生最终答案。

**图 17.** 视觉空间推理的案例研究。该示例说明了模型如何在执行逻辑演绎以验证空间关系之前，利用边界框对物体进行接地，展示了定位与推理的整合。

**图 18.** 该图说明了模型如何利用 2D 边界框聚焦关键实体，并利用其推理标签（⟨think⟩、⟨rethink⟩）在动态上下文中解决男人与滑板之间的关系。
