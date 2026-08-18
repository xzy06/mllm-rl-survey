# GRIT: Teaching MLLMs to Think with Images

> **[GRIT：教会多模态大语言模型用图像思考]**（完整中文翻译）
>
> - 作者：Yue Fan、Xuehai He、Diji Yang、Kaizhi Zheng、Ching-Chen Kuo、Yuting Zheng、Sravana Jyothi Narayanaraju、Xinze Guan、Xin Eric Wang
> - 机构：UC Santa Cruz、UC Santa Barbara、eBay
> - 来源/发表信息：第 39 届神经信息处理系统大会（39th Conference on Neural Information Processing Systems, NeurIPS 2025）；arXiv:2505.15879v2 [cs.CV]
> - 对应 PDF：`grit-teaching-mllms-to-think-with-images.pdf`
> - 联系邮箱：yfan71@ucsc.edu, ericxwang@ucsb.edu
> - 项目主页：https://grounded-reasoning.github.io

---

**图 1：** 纯自然语言推理与我们的接地推理（grounded reasoning）对比——后者将图像区域的显式边界框与自然语言思维链混合在一起。我们的 GRIT 方法仅用 20 个训练样本即可让 MLLM 实现接地推理，形成清晰可靠的"用图像思考"过程。

> 图 1 中的示例内容：
> - 图像显示一个由树枝筑成的巢，里面有九个蛋。蛋分为两组：七个在巢内，两个在外面。因此，蛋的总数是九个。
> - 要确定巢内蛋的数量，我们需要数出巢内可见的蛋：
> - **可视化（Visualization）**
> - 巢里有多少个蛋？（How many eggs are in the nest?）
> - 检查后，蛋有各种颜色：蓝色、绿色、黄色、粉色和红色。巢里有六个蛋。
> - 仅用 20 个训练数据样本实现的接地推理（我们的方法，ours）
> - 6
> - [150, 160, 250, 270], [280, 160, 380, 270], [390, 160, 490, 270], [500, 160, 600, 270], [610, 160, 710, 270], [720, 160, 820, 270]
> - 思考中……（Thinking…）
> - 回答：（Answer:）
> - 现有视觉推理模型的纯自然语言推理
> - 思考中……（Thinking…）
> - 回答：（Answer:）巢里有九个蛋。
> - 输入图像（Input image）
> - 输入查询（Input query）

---

## 摘要

近期研究表明，使用强化学习（Reinforcement Learning，RL）构建推理模型是有效的，这类模型会在给出最终答案之前先阐述思维链。然而，尽管旨在为视觉-语言任务实现推理的进展不断涌现，现有开源视觉推理模型通常以纯自然语言生成推理内容，缺乏对视觉信息的显式整合。这限制了它们生成表达清晰且具有视觉依据的推理链的能力。为此，我们提出 GRIT（Grounded Reasoning with Images and Texts，图像与文本相结合的接地推理），一种训练 MLLM 用图像思考的新方法。GRIT 引入了一种接地推理范式，在该范式中，模型生成的推理链将自然语言与显式的边界框（bounding box）坐标交错排列。这些坐标指向模型在推理过程中所参考的输入图像区域。此外，GRIT 配备了一种基于 GRPO 算法的强化学习方法——用于接地推理的 GRPO（GRPO for Grounded Reasoning，GRPO-GR）。GRPO-GR 采用聚焦于最终答案准确性和接地推理输出格式的稳健奖励，从而消除了对带有推理链标注或显式边界框标签的数据的需求。因此，GRIT 实现了卓越的数据效率，仅需来自现有数据集的 20 个图像-问题-答案三元组（triplet）。全面的评估表明，GRIT 能有效地训练 MLLM 生成连贯且具有视觉依据的推理链，展示了推理能力与接地（grounding）能力的成功统一。所有代码、数据和模型检查点（checkpoint）将全部开源。

## 1 引言

推理模型 [1, 2, 3, 4, 5] 经过训练，能够通过"推理链"来阐述其解决问题的过程，推理链由详细、逐步的思考过程以及最终答案组成。近期研究表明，与直接以零样本思维链（Chain-of-Thought，CoT）[6] 方式提示的模型相比，经过此类训练的推理模型在推理方面表现更优；在零样本 CoT 中，现成模型只是在推理时被简单引导"出声思考"，往往很少反映其真实的内部过程 [7]。推理模型最初在语言领域尤为突出 [2, 6, 5, 8, 9]，如 DeepSeek-R1 [2] 等模型展示了处理复杂任务的能力，随后又扩展到视觉-语言领域 [10, 11, 12]。

当前开源视觉推理模型在面对多模态输入时，所产生的推理链仅由自然语言构成。这导致推理不够清晰，且未能充分以视觉输入的细节为依据。为克服这一问题，一个关键问题是：如何让模型学会"用图像思考"，就像人类在思考时会参考视觉输入一样。然而，实现这一能力面临重大的技术挑战。当前 MLLM 设计用于生成语言 token，缺乏直接在推理链中生成图像的内在机制。此外，处理和理解交错包含多个视觉元素的推理序列也是一大障碍，因为许多 MLLM 难以在单个输入中维护跨多幅图像的上下文。除这些技术挑战外，数据也是主要障碍。在大多数情况下，复杂的多模态问题没有唯一正确的推理路径，且显式在推理步骤中融入视觉证据的人工标注数据严重匮乏。

为解决这些挑战并让 MLLM 实现更具视觉依据的推理，我们提出 GRIT（Grounded Reasoning with Images and Text，图像与文本相结合的接地推理）方法。GRIT 引入了一种新颖的接地推理范式，模型生成的推理链可自由混入指向输入图像相关区域的边界框坐标。这些边界框用于指明模型在推理过程中所参考的具体视觉信息。为简化推理过程，在所提出的接地推理范式中，生成边界框坐标之后，模型不会接收额外的像素输入；相反，模型基于对原始输入图像的理解来解读并利用这些坐标所指明的视觉信息。通过用生成的边界框裁剪输入图像，得到的推理链可以可视化为文本与输入图像高亮区域交错的形式，如图 1 所示。

为了训练 MLLM 以接地推理范式生成推理链，GRIT 包含一种基于 GRPO 算法的强化学习方法——用于接地推理的 GRPO（GRPO for Grounded Reasoning，GRPO-GR）。该方法配备了新颖的奖励函数，不仅关注答案准确性，还专门聚焦于推理与接地两方面的格式。具体而言，这种格式奖励鼓励推理输出采用思维 token 对（如 `<think>` 和 `</think>`）与再思维 token 对（如 `<rethink>` 和 `</rethink>`）进行结构化；同时，它也奖励在生成序列中包含语法有效的边界框。因此，GRPO-GR 中的奖励并不约束推理步骤的具体文本内容或接地区域的语义准确性，从而消除了对带有推理链标注或显式边界框标签的数据的需求。由此我们发现，GRIT 方法具有极高的数据效率：仅利用来自现有 VQA 数据集的图像-问题-答案三元组，就能让 MLLM 获得接地推理能力。

利用 GRIT 方法，我们仅使用取自现有物体关系与计数 VQA 数据集 VSR [14] 和 TallyQA [15] 的 20 个图像-问题-答案三元组，训练了先进的 MLLM——Qwen 2.5-VL [3] 和 InternVL 3 [13]。GRIT 的一个重要成果是，训练后的模型保持了广泛的通用性，不仅能有效处理视觉问答，还能处理高度依赖接地的指代表达理解（referring expression comprehension）任务。在我们使用来自 VQA 和指代表达理解基准的多种测试数据的实验中，我们揭示了几个关键发现。首先，训练后的模型在其接地推理输出中有效地统一了原本内置于基础 MLLM、但相互割裂的接地与推理能力。其次，通过定性和定量分析，我们揭示了 GRIT 训练模型生成的推理链中，所引用的图像区域与伴随文本之间存在高度相关性。此外，我们证明边界框的生成会促使模型在后续推理中更有效地关注输入视觉信息。最后，我们观察到，随着训练数据的增加，使用 GRIT 训练的模型性能有所提升，但也暴露出提升泛化能力的挑战。我们的贡献如下：

- 我们提出 GRIT（Grounded Reasoning with Images and Text，图像与文本相结合的接地推理），一种新方法，通过接地推理范式教会 MLLM 用图像思考，在该范式中模型生成的推理链将自然语言与显式边界框坐标交错排列。
- 我们开发了 GRPO-GR 强化学习算法，其采用新颖的奖励函数，仅使用图像-问题-答案三元组即可高效地赋予 MLLM 接地推理能力，无需稠密的推理链或边界框标注。
- 通过全面评估，我们证明使用 GRIT 训练的 MLLM（如 Qwen 2.5-VL 和 InternVL 3）成功统一了接地与推理能力，能够生成准确且连贯的接地推理。

## 2 相关工作

### 2.1 用于视觉-语言推理的强化学习

近期研究将带可验证奖励的强化学习（RL）应用于视觉问答任务，以构建视觉推理模型，将 DeepSeek-R1 [2] 等纯语言模型的方法扩展到增强多模态大语言模型（Multimodal Large Language Model，MLLM）。例如，R1-OneVision [12] 和 R1-V [16] 分别聚焦于图表推理和数学问题，而 Vision-R1 [11] 则强调符号推理任务。然而，这些方法往往将视觉接地与文本推理视为相互独立，或未能将它们紧密整合到单一生成过程中。VLM-R1 [10] 将 RL 应用于指代表达理解任务——一种高度依赖接地的任务，并对边界框和答案准确性给予奖励。虽然在这些任务上效果不错，但 VLM-R1 通常仅输出边界框作为最终答案，推理过程是隐式的，而非可解释的、文本与视觉接地交错的轨迹。相比之下，我们的 GRIT（图像与文本相结合的接地推理）框架使用 RL 训练 MLLM 在单一生成轨迹中自由混合接地与推理。使用 GRIT 训练的模型生成自然语言与边界框坐标交错的链，实现视觉证据与文本逻辑相互促进的动态交互。虽然 ChatGPT-o3/4 [17] 等专有系统已展现出类似的"用图像思考"能力，但 GRIT 提供了首个开源方案，通过轻量 RL 实现这种交错式视觉-文本推理，且无需中间推理或接地步骤的显式标注。

### 2.2 视觉思维链推理

视觉-语言任务中的思维链（Chain-of-Thought，CoT）推理思想早于以 RL 为中心的方法 [18, 19, 20, 21]，这类方法提示模型生成包含视觉线索的推理链。早期方法如 Multimodal-CoT [19] 采用多阶段提示，而 CCoT [21] 等其他方法则利用场景图等外部工具。这些方法通常依赖提示或辅助模块，而非学习交错推理的端到端生成过程。其他工作旨在以极少的监督学习视觉接地 CoT。UV-CoT [22] 使用自生成的边界框和辅助 MLLM 进行监督，但仍在很大程度上将接地与推理阶段分离。VisCoT [23]、CogVLM [24] 和 CogCoM [25] 等开创性工作则在带有文本理由（rationale）与对应边界框详细标注的数据集上微调模型。然而，这需要高质量、稠密的标注，将每个推理步骤与特定视觉证据关联起来。GRIT 方法的区别在于，它仅凭任务级奖励信号即可让 MLLM 生成显式、可解释且具有视觉依据的推理步骤，无需推理链中边界框或中间文本思维的监督信号。视觉接地（通过边界框坐标）被嵌入连续的推理链中。这使得使用 GRIT 训练的模型能够实现一种接地 CoT 形式，其中视觉信息被直接整合进思维过程，使它们能够"用"图像推理，而不仅仅是"关于"图像推理。

## 3 GRIT：图像与文本相结合的接地推理

### 3.1 接地推理范式

GRIT 框架在 MLLM 中培养一种直接、有依据的接地推理范式，使推理过程更加透明且可验证。给定图像 \(I\) 和文本问题 \(q\)，GRIT 使模型能够生成两部分输出 \((c, a)\)：首先是推理链 \(c\)（以 `<think>` 开头），随后是简洁的最终答案 \(a\)（在 `<answer>` 之后）。推理链 \(c\) 自由混合自然语言文本 \(T\) 和可选的边界框坐标 \(B\)。在 \(c\) 的 token 生成的任意步骤 \(p\)，模型可以选择生成边界框 \(c_p \in B\)，也可以选择继续生成自然语言文本 \(c_p \in T\)。该决定基于输入和已有推理链 \(c_{1:p-1}\)。当模型在步骤 \(q\) 生成一个或多个边界框坐标后，这些坐标旨在直接告知并塑造后续推理步骤 \(c_{q+1}, c_{q+2}, \ldots\)。关键在于，后续 token 的生成不会基于生成的边界框接收额外的像素输入。相反，模型依赖其内部理解——在新增坐标的指导下——继续推理过程。这要求模型学会解读自身的接地动作（即边界框），并将该理解整合到其持续的文本思考中。利用 MLLM 中固有的接地和推理能力，所提出的接地推理范式鼓励模型统一这些现有能力，形成新的接地推理能力。与生成像素级注意力掩码（attention mask）或将边界框所指图像区域作为多轮生成附加输入等替代方法相比，接地推理范式效率显著更高。

### 3.2 使用 GRPO-GR 的强化学习

GRIT 方法通过新提出的强化学习算法——用于接地推理的 GRPO（GRPO for Grounded Reasoning，GRPO-GR）来训练 MLLM 获得接地推理能力。GRPO-GR 基于组相对策略优化（Group-Relative Policy Optimisation，GRPO）[26] 算法，通过结合答案正确性与格式遵循的奖励来优化策略 \(\pi_\theta\)，以生成推理序列 \((c, a)\)，如图 2 所示。训练和推理时，会在模型输入后追加一个固定的提示后缀（prompt suffix），详见附录 D。

**RL 公式。** 模型充当策略 \(\pi_\theta\)，在给定输入 \((I, q)\) 时生成输出序列 \((c, a)\)。训练期间，对于每个图像-问题对 \((I, q)\)，我们从当前策略 \(\pi_\theta\) 中采样一组 \(N\) 个候选补全（completion）\(\{o_1, \ldots, o_N\}\)。对于每个补全 \(o_i\)，根据各组件（详见下文）的组合计算任务奖励 \(r_i = R(q, o_i)\)。这些奖励用于推导组归一化优势（group-normalised advantage）：

$$A_i = \frac{r_i - \text{mean}\{r_1, \ldots, r_N\}}{\text{std}\{r_1, \ldots, r_N\} + \delta}, \tag{1}$$

其中 \(\delta\) 是为数值稳定性引入的小常数（例如 \(10^{-8}\)）。

任务奖励 \(r_i\) 是由三个组件组成的复合信号：接地推理格式奖励（\(r_{\text{format}}\)）、可选的接地目标计数奖励（\(r_{\text{count}}\)）以及 GPT 辅助的答案准确性奖励（\(r_{\text{ans}}\)）。这些组件旨在鼓励期望的接地推理行为和准确的最终答案。

**接地推理格式奖励（\(r_{\text{format}}\)）。** 该奖励鼓励推理输出采用特殊 token 对进行结构化，并包含语法有效的边界框。它由特殊 token 格式信号 \(s_{\text{st}}\) 和边界框格式信号 \(s_{\text{bf}}\) 组成：

$$r_{\text{format}} = s_{\text{st}} + s_{\text{bf}}, \tag{2}$$

其中 \(s_{\text{st}}\) 奖励推理链 \(c\) 中特殊推理格式 token（`<think>...</think>` 后接 `<rethink>...</rethink>`）的正确使用和顺序，这些 token 用于构建推理结构，可能跨多个步骤。每正确放置一个 token 对，奖励增加 0.5：\(s_{\text{st}} = 0.5 \times \mathbb{I}(\text{正确的 think token 对}) + 0.5 \times \mathbb{I}(\text{正确的 rethink token 对})\)。边界框格式信号 \(s_{\text{bf}}\) 激励在 \(c\) 中显式生成语法正确的边界框。这些边界框通过正则表达式匹配以逗号分隔的整数四元组来检测，通常预期出现在 rethink token 之前。若至少存在一个这样的边界框，则赋予 0.5 的奖励：\(s_{\text{bf}} = 0.5 \times \mathbb{I}(\text{num\_bboxes} \geq 1)\)。该奖励组件鼓励所需格式和视觉接地元素的存在，而不约束接地区域本身的文本内容或语义准确性。

**接地目标计数奖励（\(r_{\text{count}}\)）。** 这个可选奖励组件专门用于来自视觉计数相关数据集（详见实验设置）的训练样本。若推理中生成的边界框数量与目标对象的真实（ground-truth）数量完全一致，则设为 0.5。这鼓励模型在计数推理过程中系统性地生成正确数量的边界框。

**GPT 辅助的答案准确性奖励（\(r_{\text{ans}}\)）。** 该奖励结合了最终答案正确性的信号，通过补充外部视觉-语言模型评判器，比单纯基于规则的检查提供更稳健的信号。其计算方式为：\(r_{\text{ans}} = s_{\text{GPT}} + 0.1 \cdot s_{\text{BLEU}}\)，其中 \(s_{\text{GPT}}\) 是由 GPT-4o 评判器评估问题、预测答案与真实答案三元组 \((q, \hat{a}, a)\) 得出的二元正确性得分（0 或 1），\(s_{\text{BLEU}}\) 是 \(\hat{a}\) 与 \(a\) 之间的句子级 BLEU-1 相似度。GPT-4o 的提示词是固定的，详见附录 D。由于 \(s_{\text{BLEU}}\) 对长度不匹配敏感，我们对其降权，确保与真实答案高度匹配才能获得最高奖励。

**优化目标。** 通过最大化使用所计算组归一化优势 \(A_i\) 的 GRPO 目标 \(J_{\text{GRPO}}(\theta)\) 来更新策略参数 \(\theta\)：

$$J_{\text{GRPO}}(\theta) = \frac{1}{N}\sum_{i=1}^{N}\left[\min\left(s_i A_i,\ \text{clip}\left(s_i,\ 1-\epsilon,\ 1+\epsilon\right) A_i\right) - \beta D_{\text{KL}}\left[\pi_\theta(\cdot|q) \| \pi_{\text{ref}}(\cdot|q)\right]_i\right], \tag{3}$$

其中 \(\pi_{\text{ref}}\) 是参考策略（通常是初始预训练模型），\(\beta\) 控制 KL 散度惩罚强度，\(\epsilon\) 定义重要性比率 \(s_i = \frac{\pi_\theta(o_i|q)}{\pi_{\theta_{\text{old}}}(o_i|q)}\) 的信任区间，\(\theta_{\text{old}}\) 是更新前的策略参数。该目标在组内最大化期望奖励与保持接近参考策略之间取得平衡，促进稳定的学习。

> **图 2：** 通过 GRPO-GR 更新模型。在 GRPO-GR 训练期间，我们采样一组模型补全，并计算接地推理格式奖励（\(r_{\text{format}}\)）、可选的接地目标计数奖励（\(r_{\text{count}}\)）以及 GPT 辅助的答案准确性奖励（\(r_{\text{ans}}\)）。这些奖励用于计算组归一化优势并引导策略优化。
>
> 图 2 中的示例输出：`<think> I need to check ...located at [123,456,234,567] ... [321,432,654,543] ... <think>` `<rethink> So ... Therefore ... </rethink>` `<Answer> The answer is ...`

## 4 实验

我们首先从接地和推理两个角度评估使用 GRIT 方法训练的模型的接地推理性能。然后，我们进一步定性和定量地分析接地推理过程中生成的边界框与其他推理内容之间的交互。最后，我们考察增加训练数据量的影响。

### 4.1 设置

**测试数据。** 我们在从六个公开数据集采样构建的精选测试集上评估使用 GRIT 训练的模型：VSR [14]（Visual Spatial Reasoning，聚焦空间关系验证）、TallyQA [15]（物体计数）、GQA [27]（组合式物体空间问题）、MME [28]（涵盖计数和位置等多样视觉任务）、MathVista-mini [29]（视觉情境中的数学推理）以及 OVDEval [30] 的位置子集（开放词汇物体接地，open-vocabulary object grounding）。为评估接地推理输出中生成的边界框的质量，我们利用 VSR、TallyQA 和 GQA 中可用的与问题相关的边界框标注，并针对评估目的手动精修了 VSR 和 GQA 数据的边界框坐标。我们在附录 A 中提供了包括数据统计在内的更多细节。

**训练数据。** 为展示 GRIT 方法的数据效率，我们仅在仅含 20 个唯一图像-查询-答案三元组的数据集上进行训练。这个小规模训练集取自 Visual-Spatial Reasoning（VSR）[14] 和 TallyQA [15] 数据集。这些数据聚焦于同时需要显式视觉接地和多步推理的任务，为评估 GRIT 在有限数据下学习接地推理格式的能力提供了合适的测试平台。更多细节请参见附录 B。

**训练实现。** 我们直接使用 GRIT 方法和强化学习训练两个预训练 MLLM：Qwen2.5-VL-3B 和 InternVL-3-2B。我们以 128 的总批大小训练 200 步。在 GRPO-GR 训练期间，每个输入样本生成 4 条候选推理轨迹，学习率为 \(2\times10^{-6}\)。训练优化器为 AdamW，并采用余弦（Cosine）学习率调度器。所有训练均在 8 张 NVIDIA A100（80GB）GPU 上进行，采用 DeepSpeed ZeRO-2，每个模型的训练时间约为 12 小时。

### 4.2 研究问题 1：从接地和推理两个角度看，接地推理的准确性如何？

**指标。** 为全面评估模型在各测试集上的性能，我们评估其输出的两个关键方面：（1）自然语言答案的正确性，采用 GPT-as-judge 答案准确率得分 [31] 进行评估，该得分由 GPT-4o 给出，介于 0（完全不正确）和 1（完全正确）之间，用于评判模型生成的自然语言答案的正确性。GPT-4o 使用的提示格式与训练中 GPT 辅助的答案准确性奖励相同（第 3.2 节）；（2）接地坐标的准确性，以接地 IoU（grounding IoU，GIoU）衡量，即模型生成的所有边界框的并集（即在推理链内，或作为 OVDEval 等任务的直接答案）与所有对应真实边界框的并集之间的平均交并比（Intersection over Union，IoU）。与传统目标检测任务的指标不同，接地 IoU 关注的是模型每条接地推理输出中的接地区域集合是否共同与标注的问题关键图像区域对齐。

**基线。** 我们包含基于与 GRIT 训练模型相同的基础 MLLM 和相同数据的基线：（1）直接查询（Direct Query）以零样本方式仅将任务查询与输入图像直接输入原始 MLLM，不添加任何特定格式或推理提示，以评估其原始任务解决能力。（2）思维链（Chain-of-Thought，CoT）[6] 向原始 MLLM 输入带固定提示后缀的查询，指示模型在答案之前生成逐步推理链。CoT 基线的提示后缀与 GRIT 训练模型所用的提示相同，用于衡量模型在未经任何后训练情况下的潜在能力。（3）一次性上下文学习（One-shot In-Context Learning，ICL）[32] 在每个测试问题前加上单个固定示例，该示例由 {问题、接地视觉思考轨迹、答案} 组成，指示模型模仿其格式和推理风格。（4）少样本 SFT（Few-shot SFT）在 GRPO 所用的相同演示数据上以标准监督学习方式微调 MLLM，以隔离强化学习的效果。

**结果。** 结果汇总在表 1 中。与基线相比，使用 GRIT 训练的模型在所采用的测试数据上总体取得更高的得分。尽管仅用 20 个训练样本训练，使用 GRIT 训练的模型不仅在 VSR 和 TallyQA（训练中见过的两个数据集）上提升了 GPT-as-judge 答案准确率得分，而且还能有效泛化到其他域外数据，表明其具备强大的推理能力。接地 IoU 指标的结果表明，使用 GRIT 训练的模型虽然未针对该指标直接优化，但在推理过程中定位与问题相关的图像区域方面优于基线。值得注意的是，在 OVDEval 测试数据上，使用 GRIT 训练的模型比零样本 MLLM 取得了更准确的检测结果，凸显了其接地能力的显著提升。这些结果表明接地与推理的统一更为成功，二者的整合明显增强了各自能力的表现。

从结果中我们还观察到，基于现成 MLLM 的基线表现出刚性，它们往往只生成边界框或只生成最终答案。对于 CoT 和一次性 ICL 基线，尽管它们被提示或由 ICL 引导生成与边界框坐标交错的推理链，但其接地和推理功能被迫同时运作。结果，它们的答案准确性或接地 IoU 通常出现严重退化，表明这些能力在很大程度上仍然分离并可能相互干扰，导致次优性能。这表明其固有的接地与推理能力之间存在普遍脱节。至于少样本 SFT 基线，虽然与零样本基线相比，它在接地 IoU 和 GPT-as-judge 答案准确率得分方面表现出更均衡的性能，但仍明显低于使用我们的 GRIT 方法训练的模型。这很可能是因为监督微调主要学习模仿输出文本与边界框交错的形式，而非发展一种接地在逻辑上指导每一步的深度整合推理过程。

**表 1：接地推理准确性的评估。** 将 GRIT 训练模型与基线在七个测试集上以 GPT-as-judge 答案准确率得分（ACC）和接地 IoU（GIoU）进行比较。GRIT 训练模型总体优于基线，表明其成功统一了 MLLM 中原本固有但相互分离的接地与推理能力。

| 模型/方法 | VSR ACC | VSR GIoU | TallyQA ACC | TallyQA GIoU | GQA ACC | GQA GIoU | MathVista ACC | MME ACC | OVDEval GIoU |
|---|---|---|---|---|---|---|---|---|---|
| Qwen2.5-VL 3B [8] | | | | | | | | | |
| 直接查询（Direct query） | 49.5 | 0.00 | 40.8 | 0.00 | 55.4 | 0.00 | 58.5 | 88.9 | 0.389 |
| 思维链（Chain-of-Thought） | 37.5 | 0.122 | 33.2 | 0.113 | 39.5 | 0.269 | 33.0 | 41.3 | 0.388 |
| 一次性 ICL（One-shot ICL） | 13.2 | 0.213 | 36.3 | 0.268 | 20.4 | 0.441 | 29.1 | 24.7 | 0.328 |
| 少样本微调（Few-shot fine-tuning） | 59.7 | 0.216 | 44.5 | 0.284 | 64.6 | 0.475 | 45.0 | 68.3 | 0.391 |
| GRIT | 72.9 | 0.325 | 47.8 | 0.447 | 62.8 | 0.485 | 59.8 | 89.3 | 0.398 |
| InternVL3 2B [13] | | | | | | | | | |
| 直接查询（Direct query） | 52.9 | 0.000 | 15.5 | 0.000 | 29.4 | 0.000 | 43.0 | 40.0 | 0.551 |
| 思维链（Chain-of-Thought） | 6.4 | 0.428 | 6.8 | 0.279 | 4.1 | 0.292 | 7.5 | 14.0 | 0.219 |
| 一次性 ICL（One-shot ICL） | 3.4 | 0.435 | 3.7 | 0.275 | 2.6 | 0.435 | 14.1 | 1.3 | 0.593 |
| 少样本微调（Few-shot fine-tuning） | 54.0 | 0.381 | 22.5 | 0.116 | 46.8 | 0.114 | 17.4 | 62.3 | 0.078 |
| GRIT | 64.9 | 0.495 | 44.2 | 0.324 | 63.2 | 0.457 | 48.2 | 82.0 | 0.560 |

### 4.3 研究问题 2：接地推理过程中，生成的边界框如何与自然语言内容交互？

**接地推理内容的定性分析。** 我们通过多种输入-输出示例定性展示使用 GRIT 训练的模型所生成的接地推理。使用 GRIT 方法训练的一大优势在于，其奖励设计对推理链内容不施加刚性约束。因此，模型学会了灵活适应各类查询的推理策略。具体而言，如图 3i 所示，GRIT 训练的模型有时会直接给出答案，然后在后续推理中对答案进行反思；而在其他情况下，如图 3ii 所示，它们会先执行接地动作来识别视觉证据，随后在推理中分析所选图像区域。关键在于，我们的模型动态决定是否需要接地，显著减少了误报（false-positive）接地的情况。例如，在图 3iii 中，针对输入图像中不存在实体的查询不会引发错误的接地，展现出稳健的多模态推理能力。

**图像区域与思维的跨模态相关性。** 为系统评估使用 GRIT 训练的模型在接地推理链中图像区域与交错自然语言内容之间的一致性，我们引入视觉-语言推理跨模态相关性（Vision-Language Reasoning Cross-Modal Correlation）指标。给定模型生成的每条推理链 \(c\)，我们提取其中相关的边界框 \(\{c_i | c_i \in B\}\)。为建立严格的评估，我们从输入图像中随机采样相同数量的边界框作为负候选 \(\{h_0, \ldots, h_j\} \in B\)。我们将这两组框分别绘制在输入图像上，然后请 GPT-4o 从两张输入图像中识别出与掩去边界框坐标的文本推理最匹配的那组边界框。利用 GPT-4o 强大的标记集合（Set-of-Mark，SoM）能力 [33]，该过程使我们能够定量评估语义一致性。我们重复该过程三次以确保稳健性，并报告平均相关性得分及标准差。我们使用该跨模态相关性指标，在六个测试集（VSR、TallyQA、GQA、MME 和 MathVista）上评估使用 GRIT 训练的模型、零样本 ICL 和少样本 SFT 的输出，排除 OVDEval，因为它主要构成接地挑战。除了评估模型生成的输出外，我们还人工编写并使用相同的视觉-语言推理跨模态相关性方法评估了 20 条带交错边界框的人工推理链，以建立人类表现基线。如图 4 所示，使用我们的 GRIT 框架训练的模型优于零样本 ICL 和少样本 SFT，展现出与文本推理高度相关的图像区域选择，但与人工编写的推理链相比仍存在差距，表明未来仍有改进空间。

**接地对后续推理的影响。** 使用 GRIT 训练的模型在生成视觉整合的思维过程时，会将推理与接地动作交错进行。为进一步理解生成的边界框如何影响后续推理，我们检查推理过程中输入视觉 token 的注意力分数。具体而言，我们使用 `<rethink>` token 将 GRIT 训练的 Qwen2.5-VL 模型的输出拆分为 rethink 前段（pre-rethink）和 rethink 段，其中 rethink 前段通常包含边界框坐标（这是受第 3.2 节详述的接地推理格式奖励引导优化的结果）。然后，我们通过从 rethink 前段中移除所有边界框，构建一个替代的 rethink 前段，模拟推理过程中未执行任何接地动作的情形。接下来，我们将替代的 rethink 前段重新输入 GRIT 训练的 Qwen2.5-VL 模型以继续生成 token。我们称基于修改后输入新生成的内容为无边界框 rethink 内容（no-bounding-box rethink content）。最后，我们计算并比较生成原始与无边界框 rethink 内容期间，各层对输入视觉 token 的平均注意力分数。该比较在 GQA 子集中随机选取的 100 个数据样本上重复进行，由于生成长度不同，我们展示生成的前 50 个 token 的结果。从图 5 所示的结果中，我们发现原始 rethink 段中每个视觉 token 的平均注意力分数总体显著高于无边界框 rethink 段。这表明原始 rethink 前段中边界框的存在会导致后续推理链中的视觉注意力增强，这可能有利于推理过程与图像的一致性。

> **图 3：Qwen2.5-VL-GRIT 的推理示例。**
>
> （i）模型先用区域给出答案，然后在后续推理中对答案进行反思。
>
> 问题（Question）：How many zebras are pictured here?
>
> 模型输出（Model output）：
> `<think> There are six zebras in the picture. The coordinates for the zebras are as follows:`
> `1. (200, 168, 248, 202) 2. (169, 159, 214, 186) 3. (76, 167, 108, 192) 4. (24, 173, 50, 197)`
> `5. (51, 163, 70, 191) 6. (413, 159, 441, 189) 7. (463, 171, 483, 186) </think>`
> `<rethink> The coordinates provided for the zebras are accurate and cover all the zebras`
> `visible in the image. There are no overlapping or missing coordinates. </rethink>`
> `<answer> 7`
>
> 真实答案（Ground truth answer）：7
>
> （ii）模型先在其推理中定位关键图像区域，然后在后续推理中进行分析。
>
> 问题（Question）：Is the truck beneath the cat?
>
> 模型输出（Model output）：
> `<think> The bounding box coordinates for the truck are approximately (0, 209, 488, 364).`
> `The cat is positioned on top of this truck. </think>`
> `<rethink> The cat is on top of the truck, so the truck is beneath the cat. </rethink>`
> `<answer> Yes`
>
> 真实答案（Ground truth answer）：Yes
>
> （iii）模型正确处理关于不存在实体的查询，不执行任何接地动作。
>
> 问题（Question）：Is there a knife in the image?
>
> 模型输出（Model output）：
> `<think> There is no knife present in the image. The focus is on a pot of soup with carrots`
> `and other ingredients. The bounding box coordinates for the knife would be outside the`
> `image area. </think>`
> `<rethink> The image shows a pot of soup with carrots and other ingredients, but there is`
> `no knife present. The bounding box coordinates for the knife would be outside the image`
> `area. </rethink>`
> `<answer> No`
>
> 真实答案（Ground truth answer）：no

> **图 4：** 由我们的视觉-语言推理跨模态相关性指标评估的、接地推理中图像区域与"思维"之间的相关性。结果表明，使用 GRIT 训练的模型优于基线。

> **图 5：** 生成 rethink 段期间模型对图像 token 的平均注意力。GRIT 训练模型原始 rethink 段的曲线总体更高，表明生成的边界框促使后续推理对图像输入产生更强的注意力。

### 4.4 研究问题 3：扩大训练数据有何影响？

为理解 GRIT 的性能如何随训练数据增加而扩展（除了 20 个样本所展现的数据效率之外），我们使用 20、500 和 7,000 个图像-问题-答案三元组训练了 Qwen2.5-VL 3B 模型的多个变体。这些样本取自 VSR 和 TallyQA 数据集，保持相同的数据来源混合比例。我们使用 GPT-as-judge 答案准确率得分，在第 4.1 节介绍的测试数据集上评估这些训练变体。图 6 展示了我们在测试数据上的结果，测试数据分为域内（in-domain，与训练数据来自同一数据集：VSR、TallyQA）或域外（out-of-domain，GQA、MathVista-mini）。结果表明，随着用于 GRIT 的训练数据增多，答案准确率总体上升。我们发现，与域内测试数据的增长相比，域外测试数据的答案准确率提升更为微弱，这凸显了泛化的常见挑战。此外，我们观察到模型性能增长逐渐放缓，表明持续改进可能需要呈指数级增长的数据。我们结合近期研究对此观察进行解读，这些研究表明，带可验证奖励的 RL 主要将现有推理模式偏向获得奖励的结果，而非从根本上改变这些模式 [34]，且性能也深受预训练的影响 [35, 36]。这意味着，要显著提升 GRIT 训练模型的域外性能，增加训练数据的多样性比单纯扩大数据量更为关键，这为未来研究指明了重要方向。

> **图 6：** 扩大训练数据对模型性能的影响。

## 5 结论

在本文中，我们提出 GRIT（Grounded Reasoning with Images and Text，图像与文本相结合的接地推理），一种新方法，其中模型通过将自然语言与指向相关图像区域的显式边界框坐标交错排列，生成具有视觉依据的推理链。我们提出了接地推理范式和 GRPO-GR 强化学习训练方法。因此，GRIT 具有极高的数据效率，既不需要稠密的推理链，也不需要显式的边界框标注。我们的实验表明，GRIT 能有效地训练预训练 MLLM 生成准确且连贯的接地推理。虽然有限的资源使我们的研究聚焦于较小的 MLLM 以验证 GRIT 方法和效率，而非探索全规模扩展下的峰值性能，但我们确定了进一步提高 GRIT 训练模型泛化能力的关键方向，即数据多样性和模型预训练。尽管如此，GRIT 以极少数据灌输复杂接地推理能力的有效性凸显了其巨大潜力。

## 参考文献（References）

[1] OpenAI. Introducing openai o1-preview. https://openai.com/index/introducing-openai-o1-preview/, 2024.

[2] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. arXiv preprint arXiv:2501.12948, 2025.

[3] An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, et al. Qwen2.5 technical report. arXiv preprint arXiv:2412.15115, 2024.

[4] Qwen Team. Qwq-32b: Embracing the power of reinforcement learning, March 2025.

[5] Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, et al. The llama 3 herd of models. arXiv preprint arXiv:2407.21783, 2024.

[6] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. Advances in neural information processing systems, 35:24824–24837, 2022.

[7] Yanda Chen, Joe Benton, Ansh Radhakrishnan, Jonathan Uesato Carson Denison, John Schulman, Arushi Somani, Peter Hase, Misha Wagner Fabien Roger Vlad Mikulik, Sam Bowman, Jan Leike Jared Kaplan, et al. Reasoning models don’t always say what they think. Anthropic Research, 2025.

[8] Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, Sinan Tan, Peng Wang, Junyang Lin, Chang Zhou, and Jingren Zhou. Qwen-vl: A frontier large vision-language model with versatile abilities. arXiv preprint arXiv:2308.12966, 2023.

[9] Shibo Hao, Sainbayar Sukhbaatar, DiJia Su, Xian Li, Zhiting Hu, Jason Weston, and Yuandong Tian. Training large language models to reason in a continuous latent space. arXiv preprint arXiv:2412.06769, 2024.

[10] Haozhan Shen, Peng Liu, Jingcheng Li, Chunxin Fang, Yibo Ma, Jiajia Liao, Qiaoli Shen, Zilun Zhang, Kangjia Zhao, Qianqian Zhang, et al. Vlm-r1: A stable and generalizable r1-style large vision-language model. arXiv preprint arXiv:2504.07615, 2025.

[11] Wenxuan Huang, Bohan Jia, Zijie Zhai, Shaosheng Cao, Zheyu Ye, Fei Zhao, Zhe Xu, Yao Hu, and Shaohui Lin. Vision-r1: Incentivizing reasoning capability in multimodal large language models. arXiv preprint arXiv:2503.06749, 2025.

[12] Yi Yang, Xiaoxuan He, Hongkun Pan, Xiyan Jiang, Yan Deng, Xingtao Yang, Haoyu Lu, Dacheng Yin, Fengyun Rao, Minfeng Zhu, et al. R1-onevision: Advancing generalized multimodal reasoning through cross-modal formalization. arXiv preprint arXiv:2503.10615, 2025.

[13] Jinguo Zhu, Weiyun Wang, Zhe Chen, Zhaoyang Liu, Shenglong Ye, Lixin Gu, Yuchen Duan, Hao Tian, Weijie Su, Jie Shao, et al. Internvl3: Exploring advanced training and test-time recipes for open-source multimodal models. arXiv preprint arXiv:2504.10479, 2025.

[14] Fangyu Liu, Guy Emerson, and Nigel Collier. Visual spatial reasoning. Transactions of the Association for Computational Linguistics, 11:635–651, 2023.

[15] Manoj Acharya, Kushal Kafle, and Christopher Kanan. Tallyqa: Answering complex counting questions. In Proceedings of the AAAI conference on artificial intelligence, volume 33, pages 8076–8084, 2019.

[16] Liang Chen, Lei Li, Haozhe Zhao, Yifan Song, and Vinci. R1-v: Reinforcing super generalization ability in vision-language models with less than $3. https://github.com/Deep-Agent/R1-V, 2025. Accessed: 2025-02-02.

[17] OpenAI. Introducing openai o3 and o4-mini. https://openai.com/index/introducing-o3-and-o4-mini/, 2025.

[18] Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed H Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language models. In The Eleventh International Conference on Learning Representations, 2022.

[19] Zhuosheng Zhang, Aston Zhang, Mu Li, Hai Zhao, George Karypis, and Alex Smola. Multimodal chain-of-thought reasoning in language models. arXiv preprint arXiv:2302.00923, 2023.

[20] Zhenfang Chen, Qinhong Zhou, Yikang Shen, Yining Hong, Zhiqing Sun, Dan Gutfreund, and Chuang Gan. Visual chain-of-thought prompting for knowledge-based visual reasoning. In AAAI Conference on Artificial Intelligence, 2024.

[21] Chancharik Mitra, Brandon Huang, Trevor Darrell, and Roei Herzig. Compositional chain-of-thought prompting for large multimodal models. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 14420–14431, 2024.

[22] Kesen Zhao, Beier Zhu, Qianru Sun, and Hanwang Zhang. Unsupervised visual chain-of-thought reasoning via preference optimization. arXiv preprint arXiv:2504.18397, 2025.

[23] Hao Shao, Shengju Qian, Han Xiao, Guanglu Song, Zhuofan Zong, Letian Wang, Yu Liu, and Hongsheng Li. Visual cot: Advancing multi-modal language models with a comprehensive dataset and benchmark for chain-of-thought reasoning. Advances in Neural Information Processing Systems, 37:8612–8642, 2024.

[24] Weihan Wang, Qingsong Lv, Wenmeng Yu, Wenyi Hong, Ji Qi, Yan Wang, Junhui Ji, Zhuoyi Yang, Lei Zhao, Song XiXuan, et al. Cogvlm: Visual expert for pretrained language models. Advances in Neural Information Processing Systems, 37:121475–121499, 2024.

[25] Ji Qi, Ming Ding, Weihan Wang, Yushi Bai, Qingsong Lv, Wenyi Hong, Bin Xu, Lei Hou, Juanzi Li, Yuxiao Dong, et al. Cogcom: Train large vision-language models diving into details through chain of manipulations. 2024.

[26] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Y Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300, 2024.

[27] Drew A Hudson and Christopher D Manning. Gqa: A new dataset for real-world visual reasoning and compositional question answering. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 6700–6709, 2019.

[28] Chaoyou Fu, Peixian Chen, Yunhang Shen, Yulei Qin, Mengdan Zhang, Xu Lin, Jinrui Yang, Xiawu Zheng, Ke Li, Xing Sun, Yunsheng Wu, and Rongrong Ji. Mme: A comprehensive evaluation benchmark for multimodal large language models, 2024.

[29] Pan Lu, Hritik Bansal, Tony Xia, Jiacheng Liu, Chunyuan Li, Hannaneh Hajishirzi, Hao Cheng, Kai-Wei Chang, Michel Galley, and Jianfeng Gao. Mathvista: Evaluating mathematical reasoning of foundation models in visual contexts. arXiv preprint arXiv:2310.02255, 2023.

[30] Yiyang Yao, Peng Liu, Tiancheng Zhao, Qianqian Zhang, Jiajia Liao, Chunxin Fang, Kyusong Lee, and Qing Wang. How to evaluate the generalization of detection? a benchmark for comprehensive open-vocabulary detection. arXiv preprint arXiv:2308.13177, 2023.

[31] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric Xing, et al. Judging llm-as-a-judge with mt-bench and chatbot arena. Advances in Neural Information Processing Systems, 36:46595–46623, 2023.

[32] Tom B Brown. Language models are few-shot learners. arXiv preprint arXiv:2005.14165, 2020.

[33] Jianwei Yang, Hao Zhang, Feng Li, Xueyan Zou, Chunyuan Li, and Jianfeng Gao. Set-of-mark prompting unleashes extraordinary visual grounding in gpt-4v. arXiv preprint arXiv:2310.11441, 2023.

[34] Yang Yue, Zhiqi Chen, Rui Lu, Andrew Zhao, Zhaokai Wang, Shiji Song, and Gao Huang. Does reinforcement learning really incentivize reasoning capacity in llms beyond the base model? arXiv preprint arXiv:2504.13837, 2025.

[35] Yihe Deng, Hritik Bansal, Fan Yin, Nanyun Peng, Wei Wang, and Kai-Wei Chang. Open-vlthinker: An early exploration to complex vision-language reasoning via iterative self-improvement. arXiv preprint arXiv:2503.17352, 2025.

[36] Hardy Chen, Haoqin Tu, Fali Wang, Hui Liu, Xianfeng Tang, Xinya Du, Yuyin Zhou, and Cihang Xie. Sft or rl? an early investigation into training r1-like reasoning large vision-language models. arXiv preprint arXiv:2504.11468, 2025.

## 附录 A 测试数据细节

为进行评估，我们整理了来自六个公开开源数据集的测试数据，涵盖一系列视觉推理和接地任务。测试数据的统计信息见表 2。

- VSR [14] 测试空间关系验证。对于我们的 VSR 评估集，我们从 Visual CoT 基准 [23] 的 VSR 子集中获取问题-图像-答案三元组，并手动筛选掉答案模糊的样本。
- TallyQA [15] 聚焦于计数；我们均匀采样目标物体计数在 0 到 9 之间的评估问题，构建我们的 TallyQA 评估集。
- GQA [27] 提供基于场景图的组合式物体空间问题。我们首先从 Visual CoT 基准中获取 GQA 子集，然后手动筛选以保留高质量样本，构建我们的 GQA 评估集。
- 从 MME [28] 中，我们仅使用计数、位置和存在性子集，以拓宽我们的评估范围。
- MathVista [29] 评估视觉情境中的数学推理。遵循先前工作，我们采用其 TestMini 划分。
- 最后，OVDEval [30] 是开放词汇检测（open-vocabulary detection，OVD）测试集，要求模型将语言查询中的细粒度语义接地到视觉特征的坐标上。我们使用其位置子集，并将其简化为单目标的物体检测任务。

在这些评估集中，源自 VSR、TallyQA 和 GQA 的评估集不仅附有真实语言答案，还带有对推导答案至关重要的图像区域的边界框标注。具体而言，我们手动精修了 Visual CoT 基准中用于我们的 VSR 和 GQA 数据的边界框坐标。对于我们的 TallyQA 评估集，我们采用原始边界框标注。除 OVDEval 外，所有评估集都是 VQA 基准，其要求的答案是一个单词或短语。相比之下，OVDEval 有所不同，因为接地不是推理链的可选组件，而是查询答案的显式要求。

**表 2：实验中使用的测试数据统计。** 我们从六个不同的基准中收集测试数据。

| 数据来源 | VSR | TallyQA | GQA | MathVista | MME | OVDEval |
|---|---|---|---|---|---|---|
| 样本数（Counts） | 288 | 491 | 509 | 1000 | 240 | 2164 |
| 平均问题/答案长度（Avg question/answer length） | 6.7/1.0 | 6.0/1.0 | 7.1/1.0 | 38.2/1.2 | 13.3/1.0 | 16.4/4 |
| 多选题与是非题占比（Ratio of multi-choice and yes/no questions, %） | 71.2 | 0 | 58.9 | 70.8 | 100 | 0 |
| 带接地目标标注占比（Ratio of annotated grounding targets, %） | 58.8 | 25.6 | 25.3 | - | - | 17.3 |

## 附录 B 训练数据细节

为展示我们的 GRIT 方法的数据效率，我们收集了一个仅含 20 个唯一图像-查询-答案三元组的小型训练数据集。这些三元组取自现有开源 VQA 数据集，同时涵盖接地和视觉推理挑战。具体而言，我们从 Visual Spatial Reasoning（VSR）数据集 [14] 中选取了 10 个，从 TallyQA 数据集 [15] 中选取了 10 个。我们选择 VSR 中的示例，因为它们通常涉及物体定位和空间关系推理（例如 "Is the motorcycle away from the bird?"）。从 TallyQA 中，我们选择了计数任务（例如 "How many signs are on the post?"），并特别确保所选示例均匀覆盖 0 到 4 的物体计数，因为这些任务天然适合在推理过程中进行显式的接地计数。这个精心挑选的数据集让模型进行多步视觉分析，用于评估 GRIT 强化视觉接地与逻辑思考之间联系的能力。

为验证在 GRIT 方法中加入计数相关训练数据及其相应的接地目标计数奖励的重要性，我们进行了一项消融实验。标准训练使用 TallyQA 的数据，包含关于图像中物体数量的问题，答案为一位数的数字。对于这些计数任务，我们使用接地目标计数奖励（详见第 3.2 节），该奖励旨在鼓励在推理输出中生成与计数相符的灵活数量的边界框。在消融实验中，我们使用修改后的数据集和奖励函数训练 InternVL-3 2B 模型。我们不再使用 10 个 VSR 和 10 个 TallyQA 样本及完整奖励集，而是使用包含 20 个 VSR 样本的数据集进行训练，并在训练中排除接地目标计数奖励。这样我们可以隔离计数相关数据和奖励组件的贡献。我们报告域内和域外数据（与第 4.4 节相同）的 GPT-as-judge 答案准确率得分和接地 IoU。结果见表 3，表明在训练中排除计数相关数据和接地目标计数奖励会导致接地性能显著下降，体现在与原 GRIT 训练模型相比更低的接地 IoU 得分。此外，我们观察到这种排除还对模型在域外数据上的答案准确性产生负面影响。因此，该消融研究强调了在 GRIT 方法中同时纳入计数相关训练数据和接地目标计数奖励的重要性。

**表 3：关于计数数据与接地目标计数奖励重要性的消融研究。** 将原始 GRIT 训练模型（使用 10 个 VSR + 10 个 TallyQA 样本及计数奖励训练）与消融变体（使用 20 个 VSR 样本、不含计数奖励训练）进行比较。结果显示消融模型性能下降。

|  | GIoU 域内（In-domain） | GIoU 域外（Out-of-domain） | ACC 域内（In-domain） | ACC 域外（Out-of-domain） |
|---|---|---|---|---|
| GRIT | 0.387 | 0.437 | 51.8 | 64.4 |
| 不含计数数据与奖励的 GRIT（GRIT w/o counting data & reward） | 0.349 | 0.378 | 53.8 | 60.0 |

## 附录 C 关于计数相关训练数据与奖励的消融研究

（注：该消融实验的完整描述与结果已在附录 B 中呈现，见上文表 3。）

## 附录 D 提示词（Prompts）

我们在 GRIT 模型训练和推理时，以及在实验的思维链（Chain-of-Thought）基线中，都会追加图 7 所示的提示词。该提示词指导模型遵循接地推理范式；然而，如实验结果所示，未经训练的 MLLM 会遭遇显著的性能下降。这是因为提示词中的指令要求 MLLM 同时执行接地和推理，这对零样本模式下的它们来说非常具有挑战性。值得注意的是，虽然提示词提到使用 "JSON" 来展示边界框，但 GRIT 训练的模型并不总是遵循这种格式。这是有意为之，因为 GRPO-GR 中的奖励使用正则表达式识别有效的边界框，而非依赖 JSON 格式，从而为模型策略的 RL 优化提供更大的搜索空间。这也表明，提示后缀仅为策略提供初始化，只要包含接地推理范式的指令，对其进行调整的影响可以忽略不计。

> **图 7：** 训练和推理期间追加到模型输入的提示后缀。
>
> First, think between `<think>` and `</think>` while output necessary coordinates needed to answer the question in JSON with key 'bbox_2d'. Then, based on the thinking contents and coordinates, rethink between `<rethink>` `</rethink>` and then answer the question after `<answer>`.

另外，在 GRPO-GR 的 GPT 辅助答案准确性奖励以及实验中的 GPT-as-judge 答案准确率得分中，我们采用图 8 所示的提示格式。

此外，在计算模型输出的视觉-语言推理跨模态相关性指标的实验中，我们利用 GPT-4o 判断模型接地推理链中的边界框是否比随机采样的边界框与自然语言推理内容更相关。我们使用的提示格式见图 9。

> **图 8：** GPT-as-judge 答案准确率得分和 GPT 辅助答案准确性奖励的提示格式。$question 和 $answer 被替换为数据样本中的查询和真实答案，$predicted_content 被替换为模型输出。
>
> You are responsible for proofreading the answers, you need to give a score to the model's answer by referring to the standard answer, based on the given question. The full score is 1 point and the minimum score is 0 points. Please output the score in the json form "{score: <score>}". The evaluation criteria require that the closer the model's answer is to the standard answer, the higher the score.
> Question: {$question}
> Standard answer: {$answer}
> Model's answer: {$predicted_content}

> **图 9：** 计算视觉-语言推理跨模态相关性指标的提示格式。这里，提供给 GPT-4o 的输入图像是同一图像绘制两组边界框的图像，一组来自生成的接地推理链，一组来自随机采样。$grounded_reasoning_masked 是移除所有边界框坐标后生成的接地推理链。
>
> Please decide which image has the bounding boxes that match the following description: {$grounded_reasoning_masked}
> Reply with exactly "Image 0" or "Image 1".

## 附录 E 更多示例

> （i）我们的 GRIT 模型能准确感知接地目标，思考问题中可能存在的歧义，并最终输出正确答案。
>
> 问题（Question）：What kind of animal stands on the ground?
>
> 模型输出（Model output）：`<think> The image shows two animals standing on the ground. The larger animal is a cow with a white and black coat, and the smaller animal is a calf. The bounding box coordinates for the cow are approximately (42, 73, 433, 296), and for the calf, they are approximately (199, 160, 363, 293). </think>` `<rethink> The question asks about the animal that stands on the ground. Both the cow and the calf are standing on the ground, so either could be the correct answer. However, the cow is the larger and more prominent animal in the image. </rethink>` `<answer> cow`
>
> 真实答案（Ground truth answer）：cow
>
> （ii）尽管接地推理过程中生成的边界框略有偏差，我们的 GRIT 模型仍能分析相关图像区域，成功修正一开始的错误答案，并最终生成正确答案。
>
> 问题（Question）：Is there only one person appear in the image? Please answer yes or no.
>
> 模型输出（Model output）：`<think> There is only one person in the image. bbox_2d_1: [0, 28, 305, 364] bbox_2d_2: [275, 0, 410, 280] </think>` `<rethink> The image shows two people, one in the foreground playing tennis and another in the background. bbox_2d_1: [0, 28, 305, 364] bbox_2d_2: [275, 0, 410, 280] </rethink>` `<answer> No`
>
> 真实答案（Ground truth answer）：No
