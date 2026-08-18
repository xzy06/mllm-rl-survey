# MM-CondChain: A Programmatically Verified Benchmark for Visually Grounded Deep Compositional Reasoning
> **[MM-CondChain：面向视觉锚定的深度组合推理的程序化验证基准]**
>
> - 作者：Haozhan Shen¹,²∗、Shilin Yan¹†、Hongwei Xue¹‡、Shuaiqi Lu¹、Xiaojun Tang¹、Guannan Zhang¹、Tiancheng Zhao³‡、Jianwei Yin²
> - 机构：¹Accio Team, Alibaba Group（阿里巴巴集团 Accio 团队）；²Zhejiang University（浙江大学）；³ZJU-BJ
> - 来源/发表信息：arXiv:2603.12266v1 [cs.CV]，2026年3月12日
> - 对应 PDF：`mm-condchain-programmatically-verified-benchmark.pdf`
---

∗ 本工作是在阿里巴巴集团 Accio 团队实习期间完成的。
† 项目负责人；‡ 通讯作者。

## 摘要

多模态大语言模型（Multimodal Large Language Models, MLLMs）正越来越多地被用于执行视觉工作流，例如导航 GUI，这类任务中的下一步操作取决于经过验证的视觉组合条件（例如，“如果出现权限对话框且界面颜色为绿色，则点击 Allow”），并且流程可能发生分支或提前终止。然而，这一能力仍未被充分评估：现有基准侧重于浅层组合（shallow-composition）或独立约束（independent-constraint），而非深度链式组合条件（deeply chained compositional conditionals）。本文中，我们提出 MM-CondChain，一个面向视觉锚定的深度组合推理基准。每个基准实例被组织为多层推理链，每一层包含一个以视觉证据为锚定、由多个对象、属性或关系构建的非平凡组合条件。要正确作答，MLLM 必须细致地感知图像、在每一步对多个视觉元素进行推理，并沿着由此产生的执行路径最终得出结果。为了可扩展地构建此类工作流式数据，我们提出一种智能体式合成流水线（agentic synthesis pipeline）：由规划器（Planner）逐层编排组合条件的生成，同时一个可验证的程序化中间表示（Verifiable Programmatic Intermediate Representation, VPIR）确保每一层的条件都可以机械地验证。随后，组合器（Composer）将这些经过验证的层组装为完整指令。利用该流水线，我们在三个视觉域上构建了基准：自然图像、数据图表和 GUI 轨迹。在多种 MLLM 上的实验表明，即使最强的模型也仅达到 53.33 的 Path F1，且在困难负样本上以及当深度或谓词复杂度增长时性能急剧下降，这证实了深度组合推理仍是一个根本性挑战。

- 项目主页：https://accio-lab.github.io/MM-CondChain
- GitHub 仓库：https://github.com/Accio-Lab/MM-CondChain
- HuggingFace：https://huggingface.co/datasets/Accio-Lab/MM-CondChain

---

## 1 引言

随着大语言模型（LLMs）[Abdin et al., 2024; Achiam et al., 2023; Anthropic; Yang et al., 2025a; Jiang et al., 2025; Qwen Team, 2026; Google DeepMind, d; Li et al., 2025; Grattafiori et al., 2024; Liu et al., 2024] 和多模态大语言模型（MLLMs）[Achiam et al., 2023; OpenAI; Google DeepMind, d,c,b,a; Qwen Team, 2026; Bai et al., 2025; Yan et al., 2025; Anthropic; Hong et al., 2025] 的能力日益增强，它们被期望超越简单的视觉问答，去处理复杂的视觉工作流——在这些工作流中，正确的动作取决于一系列视觉检查（例如，如果出现对话框，验证它是否请求位置权限；若如此且应用可信，则点击 Allow；否则……）。这类任务要求视觉锚定的深度组合推理（visually grounded deep compositional reasoning）：在每一步，模型必须验证一个多因素的视觉条件，然后决定工作流是继续还是提前终止。因此，一个自然的问题随之而来：当前先进 MLLM 能否可靠地遵循需要在每一步都对照视觉输入进行验证的深度组合条件指令？

回答这一问题需要一个系统性地探测此类能力的基准。然而，现有基准在两个关键方面有所欠缺。第一，在组合深度方面。先前的视觉推理基准 [Hsieh et al., 2023; Johnson et al., 2017; Hudson and Manning, 2019; Hua et al., 2024] 通常评估单层组合（例如，“这个物体是红色且大的吗？”），而指令遵循基准 [Zhou et al., 2023; Jiang et al., 2024b; Qian et al.; Wen et al., 2024; Pyatkin et al., 2025; Ding et al., 2025] 侧重于独立约束。两者都不要求模型跨层进行深度组合推理。在这些任务中，模型必须在每一步验证多因素视觉条件，而每一步的结果又决定后续的推理路径。第二，在困难负样本的难度方面。一些先前基准包含用于组合理解的对比对 [Thrush et al., 2022; Yuksekgonul et al., 2023; Zhao et al., 2022a,b]，但这些通常局限于单层变化，例如替换一个属性或关系。

为了填补这些空白，我们提出 MM-CondChain，一个面向 MLLM 视觉锚定深度组合推理的基准。与测试浅层组合或独立约束的先前基准不同，MM-CondChain 要求模型遵循多层控制流，其中每个决策都由一个必须对照视觉输入进行验证的组合条件所门控，且执行过程可能分支或提前终止。

**表 1：与现有基准的比较。** Compose：层内多属性组合；Nested：跨层链式条件；Visual：条件锚定于视觉输入；Hard Neg.：带最小扰动的对比对；Prog. Verif.：通过代码执行验证真值；Determ.：无需 LLM-as-judge 的确定性评估；Auto.：自动化数据构建。

| 基准 | Compose | Nested | Visual | Hard Neg. | Prog. Verif. | Determ. | Auto. |
|---|---|---|---|---|---|---|---|
| **视觉推理 (Visual Reasoning)** | | | | | | | |
| SugarCrepe [Hsieh et al., 2023] | ✓ | ✗ | ✓ | ✓ | ✗ | ✓ | ✓ |
| Winoground [Thrush et al., 2022] | ✓ | ✗ | ✓ | ✓ | ✗ | ✓ | ✗ |
| ARO [Yuksekgonul et al., 2023] | ✓ | ✗ | ✓ | ✓ | ✗ | ✓ | ✗ |
| MMComposition [Hua et al., 2024] | ✓ | ✗ | ✓ | ✗ | ✗ | ✓ | ✗ |
| **指令遵循 (Instruction Following)** | | | | | | | |
| IFEval [Zhou et al., 2023] | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✗ |
| FollowBench [Jiang et al., 2024b] | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| MIA-Bench [Qian et al.] | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| ComplexBench [Wen et al., 2024] | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| MM-IFEval [Ding et al., 2025] | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✓ |
| **MM-CondChain** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

然而，规模化构建此类基准颇具挑战。如果我们直接让一个 MLLM 智能体生成长而多层的视觉推理链，结果往往包含逻辑冲突、模糊的视觉指代，或无法从视觉输入中可靠确定的陈述。为解决这一问题，我们通过所提出的可验证程序化中间表示（VPIR）将逻辑构建与自然语言书写解耦。我们并非直接生成最终指令，而是先将每一层表示为一个可执行的、类 Python 的谓词，并针对结构化视觉事实机械地验证其为真或为假，然后才将验证过的逻辑翻译为自然语言。这使得基准构建过程可靠、可控，且锚定于可验证的视觉证据。

在 VPIR 的基础上，我们进一步开发了一个智能体式合成流水线，逐步构建每个基准实例，如图 1 所示。在每一层，流水线生成一个视觉锚定的组合条件，对照结构化视觉事实机械地验证它，然后才扩展推理链。VPIR 在每一层显式地表示已验证条件及其最小扰动的反事实（counterfactual），这自然地实现了链式困难负样本。如图 1 所示，翻转单个谓词可以改变执行路径，同时保持整体指令几乎不变，从而迫使模型在整条链路上精确地验证每一个条件。与主要测试浅层组合或独立约束的先前基准相比，我们的基准以带链式困难负样本的深层多层推理为目标。表 1 总结了 MM-CondChain 与现有基准之间的差异。

利用该流水线，我们在三个视觉域上实例化 MM-CondChain：自然图像、数据图表和 GUI 轨迹。在多种最先进 MLLM 上的实验表明，视觉锚定的深度组合推理仍然极具挑战性：即使最强的模型也仅达到 53.33 的平均 Path F1，在假路径困难负样本上性能急剧下降，并且随着推理深度和谓词复杂度的增加，准确率进一步降低。

我们的贡献总结如下：

- 我们提出 MM-CondChain，这是首个面向视觉锚定深度组合推理的基准，具有带链式困难负样本的多层控制流。
- 我们提出一个基于 VPIR 的智能体式合成流水线，将逻辑构建与语言渲染解耦，从而实现具有机械可验证性的可扩展基准构建。
- 我们在三个视觉域上实例化该框架并评估了十个 MLLM，表明即使最先进的模型也难以对组合视觉条件进行细粒度验证，尤其是在困难负样本实例上以及更大深度或谓词复杂度下。

**图 1：MM-CondChain 的目标是超越先前基准的视觉锚定深度条件推理。** 上图：现有基准通常要么评估浅层单层视觉组合，要么评估独立指令约束。左下：MM-CondChain 引入嵌套的跨层条件链，并带有丰富的层内组合谓词，其中被最小扰动的条件可以产生一个改变执行路径并导致提前终止的困难负样本。右下：实验表明，即使是先进 MLLM 在该基准上也仅取得有限性能，凸显了视觉锚定深度组合推理是一项根本性挑战。

图 1 顶部展示了一个示例指令链（英文原文）：

> If the man in the center holding a folded paper either has brown hair and is wearing a t-shirt, or he is partially blocked by another object, while he also carries a mobile phone and is not sitting down, then continue; otherwise answer [Based on the foliage visible in the background, which season is depicted?] (A1. Summer  A2. Spring  A3. Winter  A4. Autumn);
>
> Given the preceding conditions hold, if his upper garment is either a blue t-shirt or is currently folded, and it is also completely unobstructed with a white printed design on the center chest, then continue; otherwise answer [What type of bag is the man in the center wearing?] (B1. A messenger bag  B2. A backpack  B3. A duffel bag  B4. A tote bag);
>
> Given the preceding conditions hold, if the woman with a ponytail is either positioned on the right side of the image facing left or stands alone, and she is not wearing a hat while either wearing plastic sunglasses or sitting down, then continue; otherwise answer [What type of event does the equipment in the background indicate?] (C1. ...);
>
> Given the preceding conditions hold, if her glasses are either brown and currently worn or they are lying on a table, while also featuring tinted lenses and not being positioned anywhere other than on the face, then continue; otherwise answer [What does the clothing of the three individuals in the foreground indicate about their relationship?] (D1. ...);
>
> Given the preceding conditions hold, if the electronic device associated with the man in the center is either a single silver object or is cylindrical in shape, and it is fully visible while being either held or positioned on the table, then continue; otherwise answer [What is the likely functional purpose of the yellow canopy structure in the background?] (E1. ...);
>
> Given all preceding conditions hold, please answer [Considering the folded map or guide held in the man's other hand, for what functional purpose is this device likely being used?] (F1. Watching a streaming movie  F2. Assisting with navigation or coordinating a location-based activity  F3. ...)

该示例展示了三种特性：① 层内组合复杂度（Intra-layer Compositional Complexity）；② 跨层深度嵌套条件（Inter-layer Deep Nested Condition）；③ 整条链中的困难负样本（Hard Negative in the Whole Chain）。假路径（False Path）：某个条件被替换为一个最小扰动的反事实，MLLM 应在此层提前退出并回答辅助问题；真路径（True Path）：所有条件成立，MLLM 应走完条件链并回答最终问题。对比而言，其他基准通常只问诸如“有人穿蓝色上衣并且拿着手机吗？”（MMComposition、Winoground 等单层属性组合）、“左边的人穿蓝色上衣吗？/ 左边的人穿棕色上衣吗？”（MIA-Bench 等独立约束）、或“图中正在发生什么？用恰好两句话描述，必须提及背景中的自行车和前景中人们拿着的手机，使用现在时。”（单层困难负样本替换，VL-CheckList、ARO 等）。图 1 右下角柱状图显示各模型性能（Perplexity ↑ / Performance ↓）：Qwen3.5-397B-A17B 为 45.90，Qwen3-VL-235B-A22B-Thinking 为 46.83，GPT-4o-1120 为 20.06，GPT-5-0807 为 50.34，Gemini-3-Flash 为 48.31，Gemini-3-Pro 为 53.33，Kimi-K2.5 为 45.25。

---

## 2 相关工作

### 程序化可验证评估（Programmatically Verifiable Evaluation）

IFEval [Zhou et al., 2023] 提出了可验证指令，其符合性可由简单的 Python 函数检查，侧重于表面级约束。IFBENCH [Pyatkin et al., 2025] 以域外约束对其进行了扩展，并将程序化验证用作强化学习奖励。在这两种情况下，验证都发生在事后（post-hoc）：代码检查模型输出是否满足规定的格式规则。我们的方法在根本上有所不同：我们在基准构建期间而非评估期间应用程序化验证。我们并非检查输出格式，而是通过针对提取的视觉事实执行谓词来验证所生成条件的语义正确性。这确保了基准数据在逻辑上由设计保证是可靠的，消除了 LLM 直接生成复杂指令时出现的矛盾。简言之，先前工作用代码来评判输出；我们用代码来保证数据质量。

### 组合与逻辑视觉推理（Compositional and Logical Visual Reasoning）

近期的进展通过针对组合关系、空间智能和逻辑 [Zerroug et al., 2022; Zhang et al., 2019; Jiang et al., 2024a; Yang et al., 2026] 来评估 MLLM 超出基础感知的能力。诸如 VisuLogic [Xu et al., 2025b]、VER-Bench [Qiang et al., 2025] 和 LogicVista [Xiao et al., 2024] 之类的框架以视觉中心的谜题挑战模型，要求进行细粒度证据提取以排除纯文本捷径。与此同时，多步能力和严谨的分析演绎则通过顺序推理任务来评估 [Lu et al., 2024; Masry et al., 2022; Zhang et al., 2024b; Qian et al., 2025]。我们的方法在结构上有所不同：现有框架主要评估单层组合、孤立的视觉关系或没有已验证分支的顺序推理，而 MM-CondChain 以多层控制流下的视觉锚定深度组合推理为目标。在每一步，模型必须验证一个组合视觉条件，而一步的结果决定下一步的推理路径。

### 复杂视觉指令遵循（Complex Visual Instruction Following）

指令遵循的评估近来已从纯文本约束转向多模态和跨上下文环境。诸如 MIA-Bench [Qian et al.]、VC-IFEval [He et al., 2026] 和 MC-Bench [Xu et al., 2025a] 之类的基准测试 MLLM 对分层、视觉中心指令的严格遵守。为驾驭这些复杂任务，模型越来越多地利用结构化推理范式，例如视觉思维链（Visual Chain-of-Thought, VCoT）、视觉交错 CoT 和逐步课程学习 [Chen et al.; Thawakar et al., 2025; Shao et al., 2024; Wu et al., 2025]。我们的方法在结构上有所不同：先前的视觉指令数据集通常呈现扁平、加性的约束，遗漏一个视觉细节主要只是降低整体符合性分数。相比之下，MM-CondChain 将指令组织为组合视觉条件的多层链，因此未能满足一个条件会改变下游的执行路径。此外，VPIR 使我们能够将每条已验证的链与一个最小扰动的反事实配对，从而产生措辞几乎相同但执行结果不同的机械验证困难负样本。

---

## 3 基于 VPIR 的智能体式基准构建

### 3.1 概述

直接提示 MLLM 智能体生成长而多层的组合推理链，往往会导致逻辑不一致和不可验证的声明。为解决这一问题，我们提出一个基于 VPIR 的智能体式基准构建流水线，将逻辑构建与语言渲染解耦。核心思想是首先构建可验证程序化中间表示（VPIR），即可执行的类 Python 谓词，其真值可以对照视觉事实进行机械验证。然后我们将验证过的逻辑渲染为自然语言。图 2 展示了整个流水线。

给定一个多模态输入（例如，自然图像、图表或 GUI 轨迹），流水线迭代地构建多层推理链。在每一层，它选择一个视觉锚定的主题（subject），提取结构化事实，生成可执行的 VPIR 谓词，并将验证过的谓词渲染为自然语言（第 3.2 节）。每一层必须通过验证，链条才能进一步扩展。

为协调链的构建，规划器（Planner，第 3.4 节）决定是扩展、终止还是回滚链条，并与执行质量控制的验证器（Verifier，第 3.3 节）协同工作。最后，组合器（Composer，第 3.5 节）将每条已验证的链编译为成对的基准实例：所有条件都成立的真路径（True-path），以及某个条件被替换为最小扰动反事实的假路径（False-path）。这种近同构（near-isomorphic）设计产生了既需要精确视觉锚定又需要深度组合推理的困难负样本。

**图 2：MM-CondChain 智能体式合成流水线概览。** 给定多模态输入，规划器迭代地扩展条件链：在每一层，提取结构化事实，生成并经代码执行验证一个 VPIR 谓词对，然后将逻辑渲染为自然语言。随后组合器将验证过的链编译为用于评估的成对真路径与假路径实例。

### 3.2 逐层 VPIR 合成：事实、策略与程序化逻辑

我们迭代地构建一个深度控制流链，其中每一层都依赖于其前驱层的成功验证。在每一层 $t$，流水线通过一个四阶段工作流合成可验证的层逻辑：(1) 选择一个约束主题转移的关系策略 $r_t$；(2) 提取以视觉证据为锚定的结构化事实 $F_t$；(3) 生成程序化谓词对 $(p_t, \tilde{p}_t)$；(4) 将可执行逻辑渲染为自然语言。这种逻辑形成与语言渲染的解耦确保了在任何语言表达之前真值都是机械可计算的。

#### 3.2.1 第 1 步：关系策略与主题选择

在每一层 $t$，我们选择一个关系策略 $r_t \in \mathcal{R}$，其中 $\mathcal{R}$ 是跨层关系的离散分类体系（例如，深化（Deepening）与转移（Transition））。直观地，Deepening 通过放大到主题的部件或新的属性维度来继续对同一主题进行推理，而 Transition 则通过空间/语义关系转移到不同但相关的实体。

给定输入样本 $x$ 和按执行顺序排列的链历史 $H_{t-1}$，我们将 $r_t$ 实例化为主题过滤器，并构建视觉锚定候选的可行集合：

$$\Omega_t \triangleq \Omega(x, H_{t-1}, r_t). \tag{1}$$

我们使用 $\Omega_t$ 约束第 2 步中的抽取器，后者联合选择主题并提取事实。这里 $H_{t-1}$ 按执行顺序总结了先前各层，包括它们所选的主题和验证结果，因为控制流是沿着链顺序求值的。

#### 3.2.2 第 2 步：结构化事实提取

为防止逻辑合成过程中的幻觉，流水线将生成锚定在结构化、与域无关的事实表示上。在 $r_t$（进而 $\Omega_t$）和历史 $H_{t-1}$ 的条件下，抽取器联合选择一个锚定主题 $S_t \in \Omega_t$ 并产生主题-事实对：

$$(S_t, F_t) = \mathcal{E}(x, r_t, H_{t-1}). \tag{2}$$

对于种子层（$t = 1$），$H_0 = \emptyset$，$r_1$ 是基础种子策略。提取的事实 $F_t$ 构成一个类型化的键值映射 $\{(k, v_k)\}$²，其中每个键 $k$ 表示一个视觉属性维度（例如，color、spatial_relation、count、gui_state），$v_k$ 是一个类型化的观测值（例如，red、left-of、50、list-layout）。

我们强制执行两个关键设计原则：

- **以对象为中心的锚定（Object-Centric Grounding）**：主题 $S_t$ 必须在视觉输入中可唯一定位，确保条件根植于视觉证据。
- **结构优先表示（Structure-First Representation）**：通过将 $F_t$ 表示为 JSON 字典（而非自由形式文本），我们定义了一个程序化命名空间 $\mathcal{V}_t \triangleq \text{keys}(F_t)$，从而能够通过可执行语义进行机械验证。

#### 3.2.3 第 3 步：VPIR 生成

在确立事实空间 $F_t$ 和变量命名空间 $\mathcal{V}_t$ 之后，流水线合成可验证程序化中间表示（VPIR）。我们将第 $t$ 层的 VPIR 定义为一对可执行谓词程序：真逻辑 $p_t$ 和反事实假逻辑 $\tilde{p}_t$。

为正式验证这些谓词，我们在沙箱化执行环境 $\text{Env}(F_t)$ 中求值 VPIR。该环境仅暴露白名单内置运算符 $\mathcal{B}$（例如，len、set、all、any），并将每个事实键 $k \in \mathcal{V}_t$ 绑定到其提取值 $F_t[k]$。VPIR 谓词的语义随后由其确定性布尔输出定义：

$$\llbracket p \rrbracket (F_t) \triangleq \text{Exec}(p; \text{Env}(F_t)) \in \{0, 1\}. \tag{3}$$

这种程序化形式保证了绝对的确定性可验证性——生成的谓词只有通过对 $F_t$ 的机械执行才被接受：

$$\llbracket p_t \rrbracket (F_t) = 1, \quad \llbracket \tilde{p}_t \rrbracket (F_t) = 0. \tag{4}$$

此外，通过基于提示的约束，我们鼓励 (i) 非平凡的谓词复杂度（例如，具有嵌套结构和多个事实键的多子句布尔组合）以及 (ii) $\tilde{p}_t$ 相对于 $p_t$ 的最小反事实扰动，从而使真/假实例在表面形式上保持近同构，无法通过浅层文本线索区分。

#### 3.2.4 第 4 步：逻辑渲染

一旦 VPIR 谓词对 $(p_t, \tilde{p}_t)$ 通过程序化验证，基于 LLM 的转换器（Translator）就将可执行逻辑渲染为自然语言：真实条件文本 $c_t$ 和反事实条件文本 $\tilde{c}_t$（由 $\tilde{p}_t$ 渲染）。这里 $\tilde{c}_t$ 被保留用于下游的配对路径编译（第 3.5 节），在其中它将被替换到单个层以触发假路径实例中的提前终止。

至关重要的是，真值锚定在代码执行中；语言仅仅是用于评估的表面渲染。然后我们应用表达式级验证（第 3.3 节），以确保渲染流畅、无歧义且忠实于已验证的 VPIR 语义。

**微型示例（Tiny Example）。** 考虑一辆停在蓝色卡车左侧的红色汽车。在第 $t$ 层，规划器选择 $r_t = \text{Transition}$；抽取器产生 $S_t$ = “the car（那辆车）”，$F_t$ = {color: "red", position: "left"}；流水线生成 $p_t$: `color == "red" and position == "left"` 及其最小扰动 $\tilde{p}_t$: `color == "blue" and ...`；最后，转换器渲染 $c_t$ = “the car is red and on the left（那辆车是红色的且在左侧）”。机械执行确认 $\llbracket p_t \rrbracket = 1$，$\llbracket \tilde{p}_t \rrbracket = 0$。

> ²“类型化”指 $F_t$ 中的值使用 JSON 兼容类型（例如，str/int/float/bool、list/dict），并作为变量暴露给 VPIR 执行。VPIR 仅在这些类型上允许白名单原语（例如，len、any/all、min/max/sum），从而确保确定性可验证性。

### 3.3 专用验证器（Dedicated Verifier）

我们在整个链构建过程中采用一个专用的基于 MLLM 的验证器（Verifier）进行集中式质量控制。

在第 $t$ 层，候选是一个束（bundle）$B_t = (S_t, F_t, p_t, \tilde{p}_t, c_t, \tilde{c}_t)$。验证器返回结构化判定 $v = \{\text{passed}, \text{reasons}, \text{fix\_hint}\}$。验证分两个阶段进行：

**阶段 I：事实与主题验证（Fact and Subject Verification）。** 阶段 I 在任何语言渲染发生之前验证锚定材料 $(S_t, F_t)$。它检查：

- **视觉锚定（Visual Grounded）**：$S_t$ 必须在输入 $x$ 中可唯一定位；
- **不重复（Non-Repetition）**：主题和提取的事实不得与 $H_{t-1}$ 中的重复；
- **关系符合性（Relational Compliance）**：选择必须满足所选策略 $r_t$；
- **模式与一致性（Schema & Consistency）**：$F_t$ 必须符合域模式，且跨属性值保持一致。

**阶段 II：语言实现验证（Language Realization Verification）。** 阶段 II 对照已验证的 VPIR 谓词 $(p_t, \tilde{p}_t)$ 验证渲染后的自然语言条件 $(c_t, \tilde{c}_t)$。它检查：

- **语义保真（Semantic Fidelity）**：自然语言必须保留 VPIR 逻辑，不残留代码痕迹；
- **无歧义指代（Unambiguous Reference）**：每个子句必须显式命名其主题，避免共指歧义；
- **反事实质量（Counterfactual Quality）**：$\tilde{c}_t$ 必须忠实地反映 $\tilde{p}_t$，同时相对于 $c_t$ 保持最小扰动。

**反馈驱动的重新生成（Feedback-Driven Regeneration）。** 验证是阶段感知的：阶段 I 的失败触发 $(S_t, F_t)$ 的重新生成，而阶段 II 的失败则保留已验证的 $(S_t, F_t, p_t, \tilde{p}_t)$，仅重新渲染 $(c_t, \tilde{c}_t)$。

### 3.4 规划器：验证感知的链控制

我们引入一个验证感知的规划器（Planner）来治理链级控制流。基于 MLLM 的规划器与验证器之间的这种动态交互构成了我们流水线的智能体核心：规划器提出动作，验证器提供反馈，规划器相应地调整。

在每一层 $t$，规划器输出一个决策 $(a_t, r_t) = \pi(H_{t-1})$，其中 $a_t$ 是动作，$r_t \in \mathcal{R}$ 是关系策略（第 3.2 节第 1 步）。动作空间包含三个选项：

- **EXTEND**：在所提策略 $r_t$ 下合成新的一层；
- **FINISH**：终止链条并进入组合阶段；
- **ROLLBACK**：丢弃最近的非种子层，并从已验证的前缀恢复。

#### 3.4.1 混合深度控制（Hybrid Depth Control）

规划器将硬编码规则与 MLLM 驱动的策略相结合。给定目标深度区间 $[d_{\min}, d_{\max}]$：

- 若 $\text{depth}(H_{t-1}) < d_{\min}$：强制 $a_t = \text{EXTEND}$；
- 若 $\text{depth}(H_{t-1}) \geq d_{\max}$：强制 $a_t = \text{FINISH}$；
- 否则：委托给 $a_t = \pi_{\text{MLLM}}(H_{t-1})$，即一个基于 MLLM 的策略，根据链的一致性和剩余合成潜力进行决策。

#### 3.4.2 验证感知的回溯（Verification-Aware Backtracking）

规划器与验证器（第 3.3 节）紧密耦合。当当前前沿（frontier）反复出现验证失败时（例如，持续的主题重复或不可满足的关系约束），规划器触发 ROLLBACK，剪除失败层并从最后一个已验证前缀恢复合成。该反馈回路防止流水线卡在不可恢复的状态中。

一旦规划器发出 FINISH，链条即被定稿并转发给组合器（第 3.5 节）。

### 3.5 组合：配对路径指令编译

在规划器发出 FINISH 之后，我们得到一个由 $T$ 层组成的已验证控制流骨架，其中每一层 $t$ 提供一个锚定主题 $S_t$ 及其真/反事实条件 $(c_t, \tilde{c}_t)$。由于控制流可以在任何一层终止，我们为每个可能的出口点附加一个问题：为终端层附加最终问题 $q_{\text{fin}}$，为每个中间层附加辅助问题 $q^{\text{aux}}_t$。所有问题均为具有确定性答案的选择题。与先前依赖 LLM-as-judge 进行开放式评估的复杂指令基准 [Zhang et al., 2025; Yang et al., 2025b; Deshpande et al., 2025; Zou et al., 2025; Yao et al., 2023; Wen et al., 2024; Qian et al.] 不同，我们的设计实现了完全可复现、客观的评分。组合器通过两个步骤将该骨架编译为可用于评估的实例。

**第 1 步：主题去泄漏（Subject De-leakage）。** 主题描述可能无意中泄露其关联的条件。例如，如果某个条件测试“汽车是否为红色”，将主题描述为“红色的汽车”就会泄露答案。为防止这一点，基于 MLLM 的重写器将每个 $S_t$ 改写为安全的主题 $\bar{S}_t$，移除会泄露条件的属性，并在需要时替换为替代的视觉锚定描述符（例如，空间位置）。核心约束是 $\bar{S}_t$ 必须保持唯一可指代性，即它仍应无歧义地在视觉输入中标识同一目标对象 $S_t$。

**第 2 步：配对路径实例化（Paired-Path Instantiation）。** 从每个骨架中，我们编译两个近同构的评估实例：

- **真路径（True-path）**：所有条件 $\{c_t\}_{t=1}^{T}$ 均成立，因此控制流到达终端层，正确答案对应 $q_{\text{fin}}$。
- **假路径（False-path）**：我们均匀采样一个分歧层 $j \in \{1, \ldots, T-1\}$ 并将 $c_j$ 替换为 $\tilde{c}_j$。由于 $\llbracket \tilde{p}_j \rrbracket (F_j) = 0$，流程在第 $j$ 层提前终止，正确答案变为 $q^{\text{aux}}_j$。

最后，我们将每个 $(\bar{S}_t, c_t)$ 合并为流畅的自然语言 if-子句，以产生最终的嵌套指令。这种配对编译产生了困难负样本：两条路径共享相同的结构和几乎相同的措辞，仅在隐藏在多个真实条件之中的单个微妙扰动条件上有所不同。因此，区分它们需要对每个条件进行细粒度推理，而非肤浅的模式匹配。

### 3.6 域特定实例化（Domain-Specific Instantiation）

VPIR 合成流水线在其核心是与域无关的；域特定适配仅局限于输入预处理和事实提取。我们在三个视觉域（自然图像、数据图表和 GUI 轨迹）上实例化该框架，每个域在进入统一引擎之前需要不同的输入归一化（表 2）。

**自然图像（Natural Images）。** 无需预处理；MLLM 直接从原始图像中提取开放模式的视觉属性（例如，颜色、空间关系）。

**图表（Charts）。** ChartQA 的标注常常表现出 x/y 长度不匹配和零占位伪影（缺失数据点以 null 边界框标记）。我们应用确定性 CSV 对齐来修复长度不一致，并使用基于 LLM 的值提取来修复缺失条目，在调用引擎之前产生干净的 meta_json。

**表 2：统一 VPIR 框架内的域特定适配。**

| 方面 | 自然（Natural） | 图表（Chart） | GUI |
|---|---|---|---|
| 输入 | 单张图像 | 图像 + 元数据 | 图像序列 + 标注 |
| 预处理 | 无 | CSV 对齐 + LLM 修复 | 完整性 + CoAT 解析 |
| 事实关注点 | 视觉属性 | 数值统计 | 时间动作 |

**GUI 轨迹（GUI Trajectories）。** 我们验证轨迹完整性（确保截图数量与标注长度匹配），将 CoAT 动作描述解析为每步的结构化字段（动作类型、目标元素、位置等），并将多图像序列传给引擎。

至关重要的是，核心组件（VPIR 谓词生成、两阶段验证和规划器回溯）保持完全与域无关。域特定代码被隔离在输入适配器、事实构建器和策略注册表中。这证明了 VPIR 抽象可跨视觉模态泛化——从不受约束的自然场景到结构化数据可视化和交互式界面轨迹。完整的预处理细节见附录。

---

## 4 评估

### 4.1 评估设置

**数据统计（Data Statistics）。** 我们使用公开可用的数据集从三个视觉域构建 MM-CondChain。自然域包含来自 SAM [Kirillov et al., 2023]（204 张）和 GQA [Hudson and Manning, 2019]（194 张）的 398 张图像。图表域包含来自 ChartQA [Masry et al., 2022] 的 200 张图表图像，涵盖柱状图、折线图和饼图，并带有结构化数值标注。GUI 域包含来自 AITZ [Zhang et al., 2024a] 的 377 条交互轨迹（共 3,421 张截图，平均每条轨迹 9.07 帧），该数据集提供了基于 AITW [Rawles et al., 2023] 的细粒度推理标注。这总共产生 975 个评估样本，每个样本包含一个成对的真路径和假路径实例。

**提取事实与 VPIR 变量统计（Extracted Facts and VPIR Variable Statistics）。** 图 3 显示了各域提取事实中属性的分布以及 VPIR 谓词中使用的变量。我们观察到清晰的域特定模式：自然实例主要依赖对象属性和空间关系；图表实例集中于数值和结构统计；GUI 实例则强调动作、状态和轨迹级元数据。我们还发现，VPIR 变量分布并不简单地镜像完整提取的事实分布。相反，VPIR 选择性地重用提取属性的子集来组成可执行谓词，这表明基准难度是由对锚定视觉事实的结构化组合推理驱动的，而非仅由原始属性频率驱动。

**逻辑模式统计（Logical Pattern Statistics）。** 图 4 显示 MM-CondChain 中的 VPIR 表达式具有可观的结构多样性。尽管某些模式族比其他更频繁出现，但该基准并非由一两个简单模板主导：前 20 个模板仅覆盖全部表达式的 50.07%，达到 80% 覆盖率需要 128 个独特模板。这表明基准包含广泛的组合逻辑结构，而非少量重复形式。此外，主导模板本身在结构上已经复杂。如右侧示例所示，单个 VPIR 模板可以涉及多个谓词、嵌套逻辑运算符、可执行程序形式及其对应的自然语言渲染。因此，正确求解这些实例不仅需要对相关对象、属性和关系进行视觉锚定，还需要对视觉因素如何共同决定条件是否成立进行组合推理。

**基准生成（Benchmark Generation）。** 我们使用 Gemini-3-Pro [Google DeepMind, d]——目前综合推理能力最强的 MLLM 之一——来实例化合成流水线中的所有 MLLM 和 LLM 智能体，包括规划器、验证器、事实抽取器和转换器。

**图 3：各域提取事实与 VPIR 变量的高频属性。** (a,c,e) 分别显示自然、图表和 GUI 域提取事实中出现频率最高的前 20 个属性；(b,d,f) 显示相应域 VPIR 谓词中使用频率最高的前 20 个变量。

（图 3 的具体数据：自然域提取事实前 20 属性频率依次为 gender 191、age_appearance 192、count 210、clothing_items 222、pose 272、visible_text 333、has_text 424、action 434、pattern 656、orientation 900、is_cropped 1002、size 1036、is_occluded 1184、parts 1354、material 1517、shape 1635、state 1722、colors 1869、spatial_relation 2039、position 2087，类别涵盖 Color/Material、Shape/Size、Appearance、State、Spatial、Action/Pose、Clothing、Body Features、Text、Count Stats、Other；自然域 VPIR 前 20 变量依次为 printed_design 100、body_features 106、count 109、surface_marking 121、pose 172、has_text 180、clothing_items 195、visible_text 216、pattern 280、action 306、is_cropped 501、shape 503、material 554、orientation 595、spatial_relation 804、position 835、is_occluded 924、colors 1142、parts 1177、state 1248，类别含 Surface/Markings；图表域提取事实前 20 属性依次为 direction 339、x2_index 339、x1_index 339、y2 339、y1 339、x2 339、x1 339、abs_delta 370、delta 370、min_label 583、max_label 583、num_points 771、y_range 922、median_y 922、max_y 1005、min_y 1005、mean_y 1005、series_name 1040、chart_type 1040、metric_name 1040，类别含 Chart Meta、Central Stats、Range Stats、Count Stats、Coordinates、Point Labels、Delta、Trend；图表域 VPIR 前 20 变量依次为 count_ge_mean 102、iqr 105、y_b 112、y_a 114、std_y 119、rank_in_series 126、y 127、gap_to_max 141、y2_rank 209、abs_delta 211、y1_rank 215、points 227、num_points 230、y_range 268、y2 326、y1 329、min_y 352、max_y 451、median_y 496、mean_y 692，类别含 Central Stats、Range Stats、Count Stats、Coordinates、Delta、Rank Stats、Dispersion、Gap Stats、Series Values、Threshold Count、Other；GUI 域提取事实前 20 属性依次为 is_scroll 389、action_type 389、vlm_is_continue 454、vlm_scroll_dir 454、vlm_has_scrolled 454、vlm_has_dialog 454、vlm_has_navigation 454、vlm_layout_changed 454、vlm_visited_list 454、vlm_most_common 454、vlm_ending_screen 454、vlm_starting_screen 454、vlm_visual_summary 454、vlm_has_status 454、vlm_has_navigation 455、vlm_primary_content 687、vlm_screen_label 687、step_id 687、episode_length 687、instruction 1501，类别含 Trajectory Meta、Action Type、VLM Summary；GUI 域 VPIR 前 20 变量依次为 vlm_ending_screen 168、vlm_layout_changed 173、num_elements_2 174、ad_is_click 178、vlm_visible_content 183、num_elements_1 188、vlm_starting_screen 188、vlm_visual_history 192、vlm_transition 204、vlm_layout_changed 222、shared_text_count 223、num_scrolls 249、num_elements 251、new_text_count 263、num_clicks 291、num_text_elements 293、num_icon_elements 309、vlm_visited_list 323、episode_length 367、vlm_screen_label 385，类别含 Trajectory Meta、Action Type、Screen Basic、VLM Summary、Element Count。）

**图 4：VPIR 表达式的逻辑模式构成。** 左侧：高层 VPIR 逻辑族的总分布。中间：前 20 个占主导地位的具体 VPIR 模板。右侧：一个示例，展示 VPIR 模板如何被实例化为可执行谓词和自然语言条件。

（图 4 的数据：总体逻辑组合中，Conj-Negation（合取-否定）2065 个、占 44.6%；Mixed-NoNeg（混合-无否定）1953 个、占 42.1%；Disj-Negation（析取-否定）409 个、占 8.8%；Rare-Other（其他稀有）109 个、占 2.4%；Terminal-Negation（终端-否定）98 个、占 2.1%；总计 4634 个。前 20 个主导 VPIR 逻辑模板依次为：((A & B) & ((C & D) | (E & F))) 323 个、((A & B) | (C & D)) & (E & F) 307 个、((A & B) & C) & ((D & E) | (F & G)) 296 个、((A & B) | C) & (D & !E) 229 个、(A | B) & (C & !D) 144 个、((A & B) | !C) & (D & E) 134 个、((A & B) | C) & (!D & E) 132 个、((A & B) | (C & D)) & E 117 个、((A & B) & (C & D)) & ((E & F) | (G & H)) 84 个、((A & B) | C) & (D & E) 80 个、(A & B) & ((C & D) | !E) 65 个、((A & B) | (C & D)) & (E & !F) 61 个、((A & !B) | C) & (D & E) 57 个、(A & !B) & ((C & D) | E) 47 个、(A & B) | (C & D) 46 个、(A & B) | (C & !D) 42 个、((A & B) & ((C & D) | (E & F))) & (G & H) 40 个、(A | B) & (C & D) 39 个、A & ((B & C) | (D & E)) 38 个、((A & B) | (C & D)) & ((E & F) & G) 34 个。前 20 个模板覆盖所有表达式的 50.0%，80% 覆盖率需要前 128 个模板，独特模板总数为 678。示例实例化：域为 natural；模板 ((A & B) | C) & (D & !E)；谓词映射 A = len(colors) >= 2、B = 'purple' in colors、C = shape != 'round'、D = state == 'whole'、E = is_occluded；VPIR 代码为 `((len(colors) >= 2 and 'purple' in colors) or shape != 'round') and (state == 'whole' and not is_occluded)`；渲染语言为“either it displays at least two colors including purple or is not round in shape, while also being whole and unobstructed（它要么呈现至少两种颜色且包含紫色，要么形状不是圆形，同时保持完整且未被遮挡）”。）

**评估模型（Evaluated Models）。** 我们评估一系列涵盖开源和专有家族的 MLLM。开源模型包括 Qwen3-VL 系列 [Bai et al., 2025]、Qwen3.5 系列 [Qwen Team, 2026]、GLM-4.6V 系列 [Team et al., 2025]、Kimi-K2.5 [Team et al., 2026]、InternVL3 系列 [Zhu et al., 2025] 和 InternVL3.5-8B [Wang et al., 2025]。专有模型包括 GPT-4o-1120 [Achiam et al., 2023]、GPT-5-0807 [OpenAI]、Gemini-2.5-Flash [Google DeepMind, a]、Gemini-2.5-Pro [Google DeepMind, b]、Gemini-3-Flash [Google DeepMind, c]、Gemini-3-Pro [Google DeepMind, d]、Qwen3-VL-Flash 和 Qwen3-VL-Plus。

**评估指标（Evaluation Metrics）。** 我们为每个域报告三个指标：(1) **真路径准确率（True-path Accuracy）**：在真路径实例中，模型正确遵循所有条件并选择与最终问题 $q_{\text{fin}}$ 对应的答案的百分比；(2) **假路径准确率（False-path Accuracy）**：在假路径实例中，模型正确识别提前终止点并选择辅助答案 $q^{\text{aux}}_j$ 的百分比；(3) **Path F1**：真路径与假路径准确率的调和平均，衡量两条路径上的均衡表现。我们还报告 Avg(F1)，即三个域 Path F1 的算术平均，作为总体得分。

**评估实现细节（Implementation Details of Evaluation）。** 所有模型均在零样本设置下使用各提供方的默认 API 参数（温度、最大 token 数等）进行评估。每个实例以具有指定输出格式的选择题形式呈现。答案提取优先匹配最后一个 `\boxed{...}`，回退到独立选项模式；无法解析的输出被标记为错误。

### 4.2 主要结果

**主要结果（Main Results）。** 主要结果汇总于表 3。总体而言，当前 MLLM 在 MM-CondChain 上仍显吃力。在所有评估模型中，Gemini-3-Pro 以 53.33 的平均 Path F1 取得最佳总体成绩，其次是 GPT-5-0807 的 50.34。即使最强的模型也仅略高于 50 F1，这表明多层控制流下的视觉锚定深度组合推理对当前 MLLM 而言仍极具挑战性。

**真路径与假路径（True vs. False Paths）。** 一个明显的模式是，许多模型在真路径上的表现显著优于假路径。例如，GPT-4o-1120 在自然域上的得分是 83.92 对 12.81，Qwen3.5-4B 在自然域上是 88.92 对 15.37，Qwen3.5-9B 在自然域上是 91.69 对 13.10。这一差距表明，在复杂的多层条件下，模型倾向于过度假设条件成立，从而偏向“继续（continue）”分支。这种偏差在真实视觉工作流中可能很危险：未能检测到被违反的条件可能导致模型在本应停止、切换分支或拒绝动作时继续执行。

**模型比较（Model Comparisons）。** 专有模型在总体性能上通常优于开源模型，Gemini-3-Pro 和 GPT-5-0807 分别位列第一和第二。与此同时，开源模型在特定设置下仍具竞争力：值得注意的是，Qwen3.5-397B-A17B 在 GUI 上取得最佳成绩（F1=40.19），在该域上超过了所有专有模型。我们还观察到，Thinking 模型通常优于其 Instruct 对应版本，这表明显式面向推理的模型更适合这一复杂基准。

**域间难度（Domain-wise Difficulty）。** 我们观察到清晰的与域相关的难度差异。GUI 是整体上最具挑战性的域：其最佳 F1 仅为 40.19，低于自然域（55.91）和图表域（66.04）的最佳成绩。这很可能是因为 GUI 实例需要跨多帧轨迹、用户动作和界面状态转换进行推理，而许多图表条件在相关值被锚定后就归结为确定性数值比较。

**表 3：MM-CondChain 在各域上的主要结果。** 所有数字均为百分比（%）。Path F1 是真路径与假路径准确率的调和平均。Avg(F1) 是三个域 F1 分数的平均。行在各类别内按 Avg(F1) 升序排列。

| 模型 | Natural True | Natural False | Natural F1 | Chart True | Chart False | Chart F1 | GUI True | GUI False | GUI F1 | Avg F1 |
|---|---|---|---|---|---|---|---|---|---|---|
| **开源 MLLM (Open-Source MLLMs)** | | | | | | | | | | |
| Qwen3.5-0.8B | 33.17 | 2.26 | 4.23 | 31.50 | 3.00 | 5.48 | 33.95 | 1.86 | 3.52 | 4.41 |
| GLM-4.6V-Flash | 83.92 | 9.55 | 17.14 | 81.91 | 5.53 | 10.36 | 87.53 | 0.53 | 1.05 | 9.52 |
| InternVL3-8B | 65.33 | 8.29 | 14.72 | 47.50 | 8.50 | 14.42 | 63.66 | 5.31 | 9.79 | 12.98 |
| InternVL3.5-8B | 82.41 | 10.30 | 18.31 | 76.00 | 19.50 | 31.04 | 82.23 | 1.33 | 2.61 | 17.32 |
| InternVL3-14B | 76.38 | 13.57 | 23.04 | 43.00 | 21.00 | 28.22 | 84.62 | 2.39 | 4.64 | 18.63 |
| Qwen3.5-4B | 88.92 | 15.37 | 26.20 | 86.50 | 20.00 | 32.49 | 65.78 | 7.69 | 13.77 | 24.15 |
| Qwen3.5-35B-A3B | 93.43 | 11.62 | 20.66 | 88.50 | 17.00 | 28.52 | 74.27 | 14.32 | 24.02 | 24.40 |
| Qwen3-VL-30B-A3B-Instruct | 27.64 | 27.14 | 27.38 | 44.00 | 35.50 | 39.30 | 73.67 | 7.98 | 14.40 | 27.03 |
| InternVL3-38B | 73.62 | 20.60 | 32.20 | 31.00 | 31.50 | 31.25 | 57.03 | 12.47 | 20.46 | 27.97 |
| Qwen3.5-9B | 91.69 | 13.10 | 22.92 | 86.50 | 28.50 | 42.87 | 71.62 | 11.67 | 20.07 | 28.62 |
| Qwen3-VL-8B-Instruct | 47.98 | 30.81 | 37.52 | 39.78 | 39.78 | 39.78 | 58.67 | 12.53 | 20.65 | 32.65 |
| GLM-4.6V | 73.37 | 26.13 | 38.54 | 66.00 | 34.50 | 45.31 | 30.50 | 24.40 | 27.11 | 36.99 |
| Qwen3-VL-8B-Thinking | 60.71 | 30.48 | 40.58 | 49.50 | 37.00 | 42.35 | 37.14 | 27.85 | 31.83 | 38.25 |
| Qwen3.5-122B-A10B | 95.48 | 20.85 | 34.23 | 84.50 | 37.50 | 51.95 | 65.78 | 23.08 | 34.17 | 40.12 |
| Qwen3-VL-30B-A3B-Thinking | 30.90 | 31.16 | 31.03 | 58.00 | 56.50 | 57.24 | 40.53 | 27.73 | 32.93 | 40.40 |
| Kimi-K2.5 | 75.57 | 41.06 | 53.21 | 46.00 | 52.00 | 48.82 | 50.93 | 25.20 | 33.72 | 45.25 |
| Qwen3-VL-235B-A22B-Instruct | 62.12 | 43.94 | 51.47 | 55.00 | 61.00 | 57.84 | 62.60 | 17.24 | 27.04 | 45.45 |
| Qwen3.5-397B-A17B | 52.01 | 31.16 | 38.97 | 67.00 | 52.00 | 58.55 | 40.05 | 40.32 | 40.19 | 45.90 |
| Qwen3-VL-235B-A22B-Thinking | 65.49 | 39.55 | 49.31 | 61.50 | 58.50 | 59.96 | 28.91 | 33.95 | 31.23 | 46.83 |
| **专有 MLLM (Proprietary MLLMs)** | | | | | | | | | | |
| GPT-4o-1120 | 83.92 | 12.81 | 22.23 | 17.00 | 18.00 | 17.49 | 63.40 | 12.20 | 20.46 | 20.06 |
| Gemini-2.5-Flash | 29.40 | 48.24 | 36.53 | 35.50 | 47.00 | 40.45 | 6.90 | 44.83 | 11.95 | 29.64 |
| Qwen3-VL-Flash | 61.56 | 29.65 | 40.02 | 59.50 | 47.50 | 52.83 | 58.62 | 10.61 | 17.97 | 36.94 |
| Gemini-2.5-Pro | 38.94 | 55.28 | 45.70 | 55.50 | 64.50 | 59.66 | 10.34 | 54.38 | 17.38 | 40.91 |
| Qwen3-VL-Plus | 67.59 | 32.16 | 43.58 | 56.00 | 54.50 | 55.24 | 34.75 | 38.20 | 36.39 | 45.07 |
| Gemini-3-Flash | 54.77 | 41.46 | 47.19 | 60.50 | 63.50 | 61.96 | 36.87 | 34.75 | 35.78 | 48.31 |
| GPT-5-0807 | 80.65 | 33.67 | 47.51 | 63.50 | 67.50 | 65.44 | 30.77 | 49.87 | 38.06 | 50.34 |
| Gemini-3-Pro | 73.87 | 44.97 | 55.91 | 70.00 | 62.50 | 66.04 | 32.63 | 45.62 | 38.05 | 53.33 |

**表 4：链深度与谓词复杂度对 Path F1（%）的影响。** 左：随着链深度增加，性能下降，从 D=2 到 D=6 相对下降约 30%。右：在固定深度下，增大层内谓词复杂度（SIMPLE 对比 COMPLEX）导致 28–36% 的退化。

| 模型 | D=2 | D=4 | D=6 | ∆2→6 |
|---|---|---|---|---|
| Gemini-3-Flash | 70.68 | 53.85 | 47.19 | −33.2% |
| Qwen3-VL-Plus | 61.51 | 52.56 | 43.58 | −29.1% |
| GPT-4o-1120 | 31.39 | 27.67 | 22.23 | −29.2% |

| 模型 | SIMPLE | COMPLEX | ∆ |
|---|---|---|---|
| Gemini-3-Flash | 65.26 | 47.19 | −27.7% |
| Qwen3-VL-Plus | 62.91 | 43.58 | −30.7% |
| GPT-4o-1120 | 34.75 | 22.23 | −36.0% |

### 4.3 设计消融

#### 4.3.1 链深度的影响（Effect of Chain Depth）

为研究链深度如何影响模型性能，我们在自然域上构建了最大深度受控为 2、4 和 6 层的消融实例，并评估了三个代表性模型。如表 4 左所示，随着链深度增加，所有模型都表现出持续的性能下降。从深度 2 到深度 6，所有测试模型的 Path F1 相对下降约 29–33%。值得注意的是，这种退化并不均匀：Gemini-3-Flash 遭受最大的相对下降（−33.2%），尽管其绝对分数最高，这表明即使是强模型也随着顺序验证步骤数量的增加而难以保持准确率。这些结果证实，跟踪多层条件逻辑对当前 MLLM 构成根本性挑战。随深度近似线性的退化表明错误会跨层累积，而非局限于特定条件。这凸显了 MM-CondChain 可配置深度设计在探测顺序视觉推理极限方面的价值。

#### 4.3.2 谓词复杂度的影响（Effect of Predicate Complexity）

除链深度之外，我们还考察层内谓词复杂度如何影响模型性能。我们对比两种 VPIR 生成设置：SIMPLE 谓词（至多 2 个逻辑运算符、至少 2 个属性键、无嵌套要求）与 COMPLEX 谓词（至少 4 个逻辑运算符、4 个属性键和 2 个嵌套组）。两种设置共享相同的链深度，以隔离组合逻辑的影响。如表 4 右所示，增加谓词复杂度导致所有模型的性能大幅下降，相对退化范围为 27.7% 至 36.0%。值得注意的是，GPT-4o-1120 遭受最大的相对下降（−36.0%），这表明基线性能较弱的模型不成比例地受到组合复杂度的冲击。这些结果揭示，当前 MLLM 不仅在跨层的顺序推理上存在困难（如深度消融所示），而且在单个谓词内部的组合推理上也存在困难。链深度与谓词复杂度这两个维度共同定义了 MM-CondChain 的难度图景，从而能够对模型能力进行细粒度诊断。

#### 4.3.3 小结（Summary）

上述消融揭示出 MM-CondChain 中两个正交的难度轴：纵向复杂度（链深度）和横向复杂度（层内谓词组合）。增加任一维度都会导致所有测试模型一致且显著的性能退化，这证实顺序推理和组合推理仍是当前 MLLM 的根本瓶颈。至关重要的是，这两个轴在我们基于 VPIR 的合成流水线中可独立控制，从而能够进行细粒度的难度校准。这一设计使 MM-CondChain 不仅可以用作评估基准，还可以用作诊断工具，用于精确定位模型在视觉锚定条件推理中失败的位置和原因。

---

## 5 结论

本文中，我们提出 MM-CondChain，一个用于评估 MLLM 视觉锚定深度条件推理的基准。与测试浅层组合或独立约束的先前基准不同，MM-CondChain 要求跟踪多层控制流，其中每个决策都由一个视觉可验证的条件所门控。为实现具有保证正确性的可扩展构建，我们提出了一个以可验证程序化中间表示（VPIR）为核心的智能体式合成流水线，它将逻辑形成与语言渲染解耦，并产生具有确定性真值和近同构困难负样本的基准实例。在三个视觉域和一系列 MLLM 上的实验表明，视觉锚定条件推理仍是一个根本瓶颈：即使最先进的模型也会随着链深度或谓词复杂度的增加而陷入困境。我们相信 MM-CondChain 将成为诊断模型弱点、推动未来研究走向更鲁棒多模态推理的宝贵资源。

---

## 参考文献（References）

Marah Abdin, Jyoti Aneja, Harkirat Behl, Sébastien Bubeck, Ronen Eldan, Suriya Gunasekar, Michael Harrison, Russell J Hewett, Mojan Javaheripi, Piero Kauffmann, et al. Phi-4 technical report. arXiv preprint arXiv:2412.08905, 2024.

Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. arXiv preprint arXiv:2303.08774, 2023.

Anthropic. System card: Claude opus 4.6. URL https://www-cdn.anthropic.com/4263b940cabb546aa0e3283f35b686f4f3b2ff47.pdf.

Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen, Xionghui Chen, Zesen Cheng, Lianghao Deng, Wei Ding, Chang Gao, Chunjiang Ge, et al. Qwen3-vl technical report. arXiv preprint arXiv:2511.21631, 2025.

Xinyan Chen, Renrui Zhang, Dongzhi Jiang, Aojun Zhou, Shilin Yan, Weifeng Lin, and Hongsheng Li. Mint-cot: Enabling interleaved visual tokens in mathematical chain-of-thought reasoning. In The Thirty-ninth Annual Conference on Neural Information Processing Systems.

Kaustubh Deshpande, Ved Sirdeshmukh, Johannes Baptist Mols, Lifeng Jin, Ed-Yeremai Hernandez-Cardona, Dean Lee, Jeremy Kritz, Willow E Primack, Summer Yue, and Chen Xing. Multichallenge: A realistic multi-turn conversation evaluation benchmark challenging to frontier llms. In Findings of the Association for Computational Linguistics: ACL 2025, pages 18632–18702, 2025.

Shengyuan Ding, Shenxi Wu, Xiangyu Zhao, Yuhang Zang, Haodong Duan, Xiaoyi Dong, Pan Zhang, Yuhang Cao, Dahua Lin, and Jiaqi Wang. Mm-ifengine: Towards multimodal instruction following. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 1099–1109, 2025.

Google DeepMind. Gemini 2.5 flash model card. https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-2-5-Flash-Model-Card.pdf, a. PDF. Accessed: 2026-03-05.

Google DeepMind. Gemini 2.5 pro model card. https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-2-5-Pro-Model-Card.pdf, b. PDF. Accessed: 2026-03-05.

Google DeepMind. Gemini 3 flash model card. https://deepmind.google/models/model-cards/gemini-3-flash/, c. Accessed: 2026-03-05.

Google DeepMind. Gemini 3 pro model card. https://deepmind.google/models/model-cards/gemini-3-pro/, d. Accessed: 2026-03-05.

Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, et al. The llama 3 herd of models. arXiv preprint arXiv:2407.21783, 2024.

Weilei He, Feng Ju, Zhiyuan Fan, Rui Min, Minhao Cheng, and Yi R Fung. Empowering reliable visual-centric instruction following in mllms. arXiv preprint arXiv:2601.03198, 2026.

Wenyi Hong, Wenmeng Yu, Xiaotao Gu, Guo Wang, Guobing Gan, Haomiao Tang, Jiale Cheng, Ji Qi, Junhui Ji, Lihang Pan, et al. Glm-4.5 v and glm-4.1 v-thinking: Towards versatile multimodal reasoning with scalable reinforcement learning. arXiv preprint arXiv:2507.01006, 2025.

Cheng-Yu Hsieh, Jieyu Zhang, Zixian Ma, Aniruddha Kembhavi, and Ranjay Krishna. Sugarcrepe: Fixing hackable benchmarks for vision-language compositionality. Advances in neural information processing systems, 36:31096–31116, 2023.

Hang Hua, Yunlong Tang, Ziyun Zeng, Liangliang Cao, Zhengyuan Yang, Hangfeng He, Chenliang Xu, and Jiebo Luo. Mmcomposition: Revisiting the compositionality of pre-trained vision-language models. arXiv preprint arXiv:2410.09733, 2024.

Drew A Hudson and Christopher D Manning. Gqa: A new dataset for real-world visual reasoning and compositional question answering. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 6700–6709, 2019.

Yifan Jiang, Jiarui Zhang, Kexuan Sun, Zhivar Sourati, Kian Ahrabian, Kaixin Ma, Filip Ilievski, and Jay Pujara. Marvel: Multidimensional abstraction and reasoning through visual evaluation and learning. In Advances in Neural Information Processing Systems, volume 37, 2024a.

Yuchu Jiang, Yue Cai, Xiangzhong Luo, Jiale Fu, Jiarui Wang, Chonghan Liu, and Xu Yang. d2cache: Accelerating diffusion-based llms via dual adaptive caching. arXiv preprint arXiv:2509.23094, 2025.

Yuxin Jiang, Yufei Wang, Xingshan Zeng, Wanjun Zhong, Liangyou Li, Fei Mi, Lifeng Shang, Xin Jiang, Qun Liu, and Wei Wang. FollowBench: A multi-level fine-grained constraints following benchmark for large language models. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors, Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 4667–4688, Bangkok, Thailand, August 2024b. Association for Computational Linguistics. URL https://aclanthology.org/2024.acl-long.257.

Justin Johnson, Bharath Hariharan, Laurens Van Der Maaten, Li Fei-Fei, C Lawrence Zitnick, and Ross Girshick. Clevr: A diagnostic dataset for compositional language and elementary visual reasoning. In Proceedings of the IEEE conference on computer vision and pattern recognition, pages 2901–2910, 2017.

Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C Berg, Wan-Yen Lo, et al. Segment anything. In Proceedings of the IEEE/CVF international conference on computer vision, pages 4015–4026, 2023.

Pengxiang Li, Shilin Yan, Joey Tsai, Renrui Zhang, Ruichuan An, Ziyu Guo, and Xiaowei Gao. Adaptive classifier-free guidance via dynamic low-confidence masking. arXiv preprint arXiv:2505.20199, 2025.

Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, et al. Deepseek-v3 technical report. arXiv preprint arXiv:2412.19437, 2024.

Pan Lu et al. Mathvista: Evaluating mathematical reasoning of foundation models in visual contexts. In International Conference on Learning Representations, 2024.

Ahmed Masry et al. Chartqa: A benchmark for visual question answering on charts. In ACL, 2022.

OpenAI. Gpt-5 system card. https://openai.com/index/gpt-5-system-card/. Accessed: 2026-03-05.

Valentina Pyatkin, Saumya Malik, Victoria Graf, Hamish Ivison, Shengyi Huang, Pradeep Dasigi, Nathan Lambert, and Hannaneh Hajishirzi. Generalizing verifiable instruction following. arXiv preprint arXiv:2507.02833, 2025.

Yusu Qian, Hanrong Ye, Jean-Philippe Fauconnier, Peter Grasch, Yinfei Yang, and Zhe Gan. Mia-bench: Towards better instruction following evaluation of multimodal llms. In The Thirteenth International Conference on Learning Representations.

Yusu Qian, Cheng Wan, Chao Jia, Yinfei Yang, Qingyu Zhao, and Zhe Gan. Prism-bench: A benchmark of puzzle-based visual tasks with cot error detection. arXiv preprint arXiv:2510.23594, 2025.

Chenhui Qiang, Zhaoyang Wei, Xumeng Han, Zipeng Wang, Siyao Li, Xiangyuan Lan, Jianbin Jiao, and Zhenjun Han. Ver-bench: Evaluating mllms on reasoning with fine-grained visual evidence. In Proceedings of the 33rd ACM International Conference on Multimedia, pages 12698–12705, 2025.

Qwen Team. Qwen3.5: Towards native multimodal agents, February 2026. URL https://qwen.ai/blog?id=qwen3.5.

Christopher Rawles, Alice Li, Daniel Rodriguez, Oriana Riva, and Timothy Lillicrap. Androidinthewild: A large-scale dataset for android device control. Advances in Neural Information Processing Systems, 36:59708–59728, 2023.

Hao Shao et al. Visual cot: Advancing multi-modal language models with a comprehensive dataset and benchmark for chain-of-thought reasoning. In NeurIPS, 2024.

Kimi Team, Tongtong Bai, Yifan Bai, Yiping Bao, SH Cai, Yuan Cao, Y Charles, HS Che, Cheng Chen, Guanduo Chen, et al. Kimi k2. 5: Visual agentic intelligence. arXiv preprint arXiv:2602.02276, 2026.

V Team, Wenyi Hong, Wenmeng Yu, Xiaotao Gu, Guo Wang, Guobing Gan, Haomiao Tang, Jiale Cheng, Ji Qi, Junhui Ji, Lihang Pan, Shuaiqi Duan, Weihan Wang, Yan Wang, Yean Cheng, Zehai He, Zhe Su, Zhen Yang, Ziyang Pan, Aohan Zeng, Baoxu Wang, Bin Chen, Boyan Shi, Changyu Pang, Chenhui Zhang, Da Yin, Fan Yang, Guoqing Chen, Jiazheng Xu, Jiale Zhu, Jiali Chen, Jing Chen, Jinhao Chen, Jinghao Lin, Jinjiang Wang, Junjie Chen, Leqi Lei, Letian Gong, Leyi Pan, Mingdao Liu, Mingde Xu, Mingzhi Zhang, Qinkai Zheng, Sheng Yang, Shi Zhong, Shiyu Huang, Shuyuan Zhao, Siyan Xue, Shangqin Tu, Shengbiao Meng, Tianshu Zhang, Tianwei Luo, Tianxiang Hao, Tianyu Tong, Wenkai Li, Wei Jia, Xiao Liu, Xiaohan Zhang, Xin Lyu, Xinyue Fan, Xuancheng Huang, Yanling Wang, Yadong Xue, Yanfeng Wang, Yanzi Wang, Yifan An, Yifan Du, Yiming Shi, Yiheng Huang, Yilin Niu, Yuan Wang, Yuanchang Yue, Yuchen Li, Yutao Zhang, Yuting Wang, Yu Wang, Yuxuan Zhang, Zhao Xue, Zhenyu Hou, Zhengxiao Du, Zihan Wang, Peng Zhang, Debing Liu, Bin Xu, Juanzi Li, Minlie Huang, Yuxiao Dong, and Jie Tang. Glm-4.5v and glm-4.1v-thinking: Towards versatile multimodal reasoning with scalable reinforcement learning, 2025. URL https://arxiv.org/abs/2507.01006.

Omkar Thawakar, Dinura Dissanayake, Ketan Pravin More, Ritesh Thawkar, Ahmed Heakl, Noor Ahsan, Yuhao Li, Ilmuz Zaman Mohammed Zumri, Jean Lahoud, Rao Muhammad Anwer, et al. Llamav-o1: Rethinking step-by-step visual reasoning in llms. In Findings of the Association for Computational Linguistics: ACL 2025, pages 24290–24315, 2025.

Tristan Thrush, Ryan Jiang, Max Bartolo, Amanpreet Singh, Adina Williams, Douwe Kiela, and Candace Ross. Winoground: Probing vision and language models for visio-linguistic compositionality, 2022. URL https://arxiv.org/abs/2204.03162.

Weiyun Wang, Zhangwei Gao, Lixin Gu, Hengjun Pu, Long Cui, Xingguang Wei, Zhaoyang Liu, Linglin Jing, Shenglong Ye, Jie Shao, et al. Internvl3. 5: Advancing open-source multimodal models in versatility, reasoning, and efficiency. arXiv preprint arXiv:2508.18265, 2025.

Bosi Wen, Pei Ke, Xiaotao Gu, Lindong Wu, Hao Huang, Jinfeng Zhou, Wenchuang Li, Binxin Hu, Wendy Gao, Jiaxing Xu, et al. Benchmarking complex instruction-following with multiple constraints composition. Advances in Neural Information Processing Systems, 37:137610–137645, 2024.

Xuecheng Wu, Jiaxing Liu, Danlei Huang, Yifan Wang, Yunyun Shi, Kedi Chen, Junxiao Xue, Yang Liu, Chunlin Chen, Hairong Dong, et al. Vic-bench: Benchmarking visual-interleaved chain-of-thought capability in mllms with free-style intermediate state representations. arXiv preprint arXiv:2505.14404, 2025.

Yijia Xiao, Edward Sun, Tianyu Liu, et al. Logicvista: Multimodal llm logical reasoning benchmark in visual contexts. arXiv preprint arXiv:2407.04973, 2024.

Runsen Xu et al. Mc-bench: A benchmark for multi-context visual grounding. In Proceedings of the IEEE/CVF International Conference on Computer Vision, 2025a.

Weiye Xu, Jiahao Wang, Weiyun Wang, Zhe Chen, Wengang Zhou, Aijun Yang, Lewei Lu, Houqiang Li, Xiaohua Wang, Xizhou Zhu, et al. Visulogic: A benchmark for evaluating visual reasoning in multi-modal large language models. arXiv preprint arXiv:2504.15279, 2025b.

Shilin Yan, Jiaming Han, Joey Tsai, Hongwei Xue, Rongyao Fang, Lingyi Hong, Ziyu Guo, and Ray Zhang. Crosslmm: Decoupling long video sequences from lmms via dual cross-attention mechanisms. arXiv preprint arXiv:2505.17020, 2025.

An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. arXiv preprint arXiv:2505.09388, 2025a.

Chenghao Yang, Yinbo Luo, Zhoufutu Wen, Qi Chu, Tao Gong, Longxiang Liu, Kaiyuan Zhang, Jianpeng Jiao, Ge Zhang, Wenhao Huang, et al. Mars-bench: A multi-turn athletic real-world scenario benchmark for dialogue evaluation. arXiv preprint arXiv:2505.23810, 2025b.

Sihan Yang, Runsen Xu, et al. Mmsi-bench: A benchmark for multi-image spatial intelligence. In International Conference on Learning Representations, 2026.

Xuyou Yang, Yucheng Zhao, Wenxuan Zhang, and Immanuel Koh. Space-eval: A benchmark for real-world multi-modal reasoning. In The Fourteenth International Conference on Learning Representations.

Shunyu Yao, Howard Chen, Austin W Hanjie, Runzhe Yang, and Karthik Narasimhan. Collie: Systematic construction of constrained text generation tasks. arXiv preprint arXiv:2307.08689, 2023.

M Yuksekgonul, F Bianchi, P Kalluri, D Jurafsky, J Zou, et al. When and why vision-language models behave like bags-of-words, and what to do about it? In 11th International Conference on Learning Representations, ICLR 2023. International Conference on Learning Representations, ICLR, 2023.

Aimen Zerroug, Mohit Vaishnav, Julien Colin, Sebastian Musslick, and Thomas Serre. A benchmark for compositional visual reasoning. In Advances in Neural Information Processing Systems, volume 35, pages 21551–21565, 2022.

Chi Zhang, Feng Gao, Baoxiong Jia, Yixin Zhu, and Song-Chun Zhu. Raven: A dataset for relational and analogical visual reasoning. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 5317–5327, 2019.

Jiwen Zhang, Jihao Wu, Teng Yihua, Minghui Liao, Nuo Xu, Xiao Xiao, Zhongyu Wei, and Duyu Tang. Android in the zoo: Chain-of-action-thought for gui agents. In Findings of the Association for Computational Linguistics: EMNLP 2024, pages 12016–12031, 2024a.

Qinyan Zhang, Xinping Lei, Ruijie Miao, Yu Fu, Haojie Fan, Le Chang, Jiafan Hou, Dingling Zhang, Zhongfei Hou, Ziqiang Yang, et al. Inverse ifeval: Can llms unlearn stubborn training conventions to follow real instructions? arXiv preprint arXiv:2509.04292, 2025.

Renrui Zhang, Dongzhi Jiang, Yichi Zhang, Haokun Lin, Ziyu Guo, Pengshuo Qiu, Aojun Zhou, Pan Lu, Kai-Wei Chang, Yu Qiao, et al. Mathverse: Does your multi-modal llm truly see the diagrams in visual math problems? In European Conference on Computer Vision, pages 169–186. Springer, 2024b.

Tiancheng Zhao, Tianqi Zhang, Mingwei Zhu, Haozhan Shen, Kyusong Lee, Xiaopeng Lu, and Jianwei Yin. Vl-checklist: Evaluating pre-trained vision-language models with objects, attributes and relations, 2022a. URL https://arxiv.org/abs/2207.00221.

Tiancheng Zhao, Tianqi Zhang, Mingwei Zhu, Haozhan Shen, Kyusong Lee, Xiaopeng Lu, and Jianwei Yin. An explainable toolbox for evaluating pre-trained vision-language models. In Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing: System Demonstrations, pages 30–37, 2022b.

Jeffrey Zhou, Tianjian Lu, Swaroop Mishra, Siddhartha Brahma, Sujoy Basu, Yi Luan, Denny Zhou, and Le Hou. Instruction-following evaluation for large language models. arXiv preprint arXiv:2311.07911, 2023.

Jinguo Zhu, Weiyun Wang, Zhe Chen, Zhaoyang Liu, Shenglong Ye, Lixin Gu, Hao Tian, Yuchen Duan, Weijie Su, Jie Shao, et al. Internvl3: Exploring advanced training and test-time recipes for open-source multimodal models. arXiv preprint arXiv:2504.10479, 2025.

Tao Zou, Xinghua Zhang, Haiyang Yu, Minzheng Wang, Fei Huang, and Yongbin Li. Eifbench: Extremely complex instruction following benchmark for large language models. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, pages 20941–20964, 2025.
