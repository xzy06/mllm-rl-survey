# CR3: Boosting Compositional Reasoning in MLLMs through Rule-based Reinforcement Learning

> **CR³：通过基于规则的强化学习增强 MLLM 的组合推理能力**（完整中文翻译）
>
> - 作者：Shun Qian（钱舜）、Bingquan Liu（刘秉权）、Chengjie Sun（孙承杰）、Peijin Xie（谢培锦）、Zhen Xu（徐振）、Baoxun Wang（王宝勋）
> - 机构：哈尔滨工业大学计算学部（Faculty of Computing, Harbin Institute of Technology）；腾讯平台与内容事业群（Platform and Content Group, Tencent）；哈尔滨工业大学语言技术与数字经济国家研究中心（National Research Center for Language Technology and Digital Economy, Harbin Institute of Technology）
> - 来源/发表信息：The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)
> - 对应 PDF：`cr3-boosting-compositional-reasoning-in-mllms.pdf`

---

## 摘要

组合推理（compositional reasoning）是多模态模型的一项关键能力，它使模型能够通过对物体、属性和关系的结构化组合来系统地理解复杂场景。然而，现有关于这一能力的研究主要集中在视觉语言模型（VLMs，如 CLIP 和 SigLIP）上，对多模态大语言模型（MLLMs）的探索十分有限。为弥补这一空白，我们提出 **CR3**——一个通过基于规则的强化学习（rule-based reinforcement learning）增强 MLLM 组合推理能力的新框架。CR3 利用基于规则的奖励，在系统筛选（systematically curated）的多模态指令遵循任务上优化 MLLM 的策略，并由一种模型自适应的动态任务混合策略（model-adaptive dynamic task mixing strategy）引导。我们的方法在三个组合推理基准上将性能提升超过 19%，显著优于监督微调（SFT）方法至少 12%。关键的是，CR3 展现出卓越的泛化能力：在 SFT 方法性能下降的域外（out-of-domain）基准上，CR3 仍能提升性能，凸显了其有效性与数据效率。

- 代码：https://github.com/AAbathur/CR3
- 数据集：https://github.com/AAbathur/CR3/tree/main/train/data

## 1 引言

组合推理——将复杂场景或描述分解为可解释的元素（物体、属性、关系），并通过结构化组合进行重建的能力——是人类智能的标志（Ma et al. 2023; Janssen and Partee 1997）。然而，大多数最先进的（SoTA）视觉语言模型（VLMs），如 CLIP 和 FLAVA，由于其有限的组合推理能力，常常表现得像"词袋"（bag-of-words）模型。虽然这些模型擅长识别孤立的物体，但它们经常无法将属性（如颜色、大小、形状）或状态（如正在吃、破损、站立）绑定到物体上，也无法解释空间和逻辑关系（如上方、下方、左边、右边）。例如，给定一张"红色立方体位于金属球左边"的图像，这些模型可能会对错误的描述"金属立方体位于红色球左边"赋予同样高的置信度，这揭示了其在组合推理上的根本局限。

Copyright © 2026，Association for the Advancement of Artificial Intelligence (www.aaai.org)。版权所有。

> 哪张图像最能描述文字说明"绿腿的人跑得很慢，而红腿的人跑得更快"？
>
> 文字说明"绿腿的人跑得很慢，而红腿的人跑得更快"最能描述第二张图像。在这张图像中，绿腿的人似乎跑在前面且更快，而红腿的人则落在后面，看起来疲惫不堪。
>
> **图 1：** Winoground（Thrush et al. 2022）中的一个示例及 GPT-4o 对它的回答。红色文字表示错误的选择，绿色文字表示所选图像上的正确描述。

这一关键局限即使在最先进的多模态大语言模型（MLLMs）中依然存在。近期研究（Ni et al. 2025; Chen et al. 2024a; Tong et al. 2024）表明，即使是像 GPT-4V（Achiam et al. 2023）这样的前沿 MLLM，在处理关系反转（relational inversions）和长尾组合（long-tail compositions）时也表现出显著局限。如图 1 所示，即使是 GPT-4o 这样的领先模型，也可能在简单的组合推理查询中失败，生成带有明显逻辑矛盾的回复。尽管组合推理能力十分重要，系统地提升 MLLM 的组合推理能力仍然是一个开放且关键的研究挑战。

应对这一挑战的一个直接方法是在专门设计的多模态指令数据集上进行监督微调（SFT）。然而，这种方法面临严峻的可扩展性挑战。为各种组合推理场景筛选全面、高质量的数据既费时又昂贵。此外，通过 SFT 训练的模型往往会过拟合训练数据中的特定模式，对新颖组合的泛化能力较差。

为克服这些局限，我们提出 **CR3**——一个通过**基于规则的强化学习**增强 MLLM **组合推理**能力的新框架。我们的框架首先利用多模态协同过滤机制（multimodal collaborative filtering mechanism），从开源数据集中筛选出高质量的、具备组合感知（compositionally-aware）的图文对。随后，这些图文对会被系统性地转换为三种不同且可验证的指令遵循任务，旨在强化组合推理能力。接下来，我们借鉴 DeepSeek-R1（Guo et al. 2025）的思想，采用基于规则的奖励函数来评估 MLLM 回复的奖励得分。随后，MLLM 的策略通过组相对策略优化（Group Relative Policy Optimization，GRPO）算法基于这些奖励进行优化。最后，为了最大化任务之间的协同效应，我们引入了一种模型自适应的动态混合策略（model-adaptive dynamic mixing strategy），该策略根据模型在不同阶段的性能智能地调整训练中不同任务的比例。大量实验结果证明了 CR3 框架的有效性。当应用于 Qwen2.5-VL（Bai et al. 2025）和 InternVL3（Zhu et al. 2025）等 SoTA MLLM 时，无论模型规模或架构如何，CR3 在三个具有挑战性的组合推理基准上均持续取得超过 19% 的性能提升。值得注意的是，与标准 SFT 方法相比，CR3 保持了显著优势，在每一个基线模型上都带来了至少 12% 的提升。我们进一步使用流行的多模态基准（如 MMMU（Yue et al. 2024）和 MMB（Liu et al. 2024））评估域外泛化能力。结果表明，CR3 在通用视觉语言任务上显著增强了基线模型的性能，而 SFT 方法则出现性能下降。这些结果凸显了 CR3 卓越的泛化能力和数据效率。我们的主要贡献总结如下：

- 我们提出了第一个通过规则引导的强化学习增强 MLLM 组合推理能力的框架，为这一关键能力确立了新的范式。
- 我们构建并公开发布了一个高质量、具备组合感知的视觉指令遵循数据集，专门用于推动 MLLM 研究。
- 通过大量实验，我们证明了 CR3 增强后的模型在跨多种多模态基准的组合推理中展现出稳健的泛化能力。

## 2 相关工作

### 2.1 多模态组合性（Multimodal Compositionality）

尽管 VLM 已在各种多模态任务上取得了显著成功，但它们常常缺乏稳健的组合理解和推理能力。NegCLIP（Yuksekgonul et al. 2023）等研究表明，SoTA VLM（如 CLIP（Radford et al. 2021）、FLAVA（Singh et al. 2022）、X-VLM（Zeng, Zhang, and Li 2022））表现得像"词袋"模型，无法捕捉关系、属性和位置依赖。DAC（Doveh et al. 2023）指出，网络抓取的文本描述（核心训练数据来源之一）质量低是关键瓶颈。后续工作（Stone et al. 2025）提出了自动描述精炼（automated caption refinement）来提升预训练数据集密度。在此基础上，TripletCLIP（Patel et al. 2024）、GMN（Sahin et al. 2024）和 SPEC（Peng et al. 2024）通过扰动描述合成硬负样本（hard negatives），显式地训练 VLM 以区分细微的组合差异。然而，这些工作聚焦于 VLM，在 MLLM 上的探索十分有限。

### 2.2 面向 MLLM 的基于规则的强化学习（Rule-based Reinforcement Learning for MLLMs）

强化学习（RL）增强了 LLM 的推理能力，这一点已由 OpenAI O1（Jaech et al. 2024）、Kimi 1.5（Team et al. 2025）和 DeepSeek-R1（Guo et al. 2025）证明。受这些进展启发，多模态领域已将基于规则的 RL 技术适配到 MLLM 上。一系列研究（Xie et al. 2025; Feng et al. 2025; Liu et al. 2025）将基于规则的强化学习策略扩展到了各种多模态任务。此外，MM-Eureka（Meng et al. 2025）和 VisualTinker-R1-Zero（Zhou et al. 2025）探索在多模态推理任务中复现"顿悟时刻"（aha moment）。R1-Onevision（Yang et al. 2025）和 OpenVLThinker（Deng et al. 2025）利用纯文本 R1 模型来弥补高质量多模态推理数据的缺乏。R1V（Peng et al. 2025）和 R1-VL（Zhang et al. 2025）通过迭代策略精炼推理。据我们所知，CR3 是首个专门针对多模态组合推理设计的基于规则的 RL 方法，大规模评测证实了其有效性。

## 3 方法

### 3.1 基于规则奖励的 GRPO（GRPO with Rule-Based Rewards）

为呈现 CR3 方法，本节简要概述用于强化学习训练的、带基于规则奖励的 GRPO 算法。

与近端策略优化（Proximal Policy Optimization，PPO）（Schulman et al. 2017）相比，GRPO 无需额外的评论家（critic）模型，因而具有更高的计算效率。取而代之的是，GRPO 通过评估多个候选回复的相对质量来直接估计策略模型。对于给定的问题 $q$，GRPO 首先从旧策略模型 $\pi_{old}$ 中采样 $G$ 个回复 $\{o_1, o_2, \ldots, o_G\}$，并用奖励模型计算对应的奖励 $\{r_1, r_2, \ldots, r_G\}$。第 $i$ 个回复的优势（advantage）计算如下：

$$A_{i,t} = \frac{r_i - \text{mean}(\{r_1, r_2, \ldots, r_G\})}{\text{std}(\{r_1, r_2, \ldots, r_G\})} \tag{1}$$

随后，模型通过最大化以下目标进行优化：

$$J_{GRPO}(\theta) = \mathbb{E}_{q \sim P(Q)} \left[ \frac{1}{G} \sum_{i=1}^{G} \frac{1}{|o_i|} \sum_{t=1}^{|o_i|} \left( \min \left( \frac{\pi_\theta(o_{i,t} \mid q, o_{i,<t})}{\pi_{\theta_{old}}(o_{i,t} \mid q, o_{i,<t})} A_{i,t}, \; \text{clip}\left( \frac{\pi_\theta(o_{i,t} \mid q, o_{i,<t})}{\pi_{\theta_{old}}(o_{i,t} \mid q, o_{i,<t})}, 1 - \varepsilon, 1 + \varepsilon \right) A_{i,t} \right) - \beta D_{KL}[\pi_\theta \| \pi_{ref}] \right) \right] \tag{2}$$

其中 $\varepsilon$ 和 $\beta$ 为超参数。

在我们的 CR3 方法中，关键的奖励模型采用基于规则的奖励函数，这与标准 RL 框架中的传统奖励模型不同。所采用的奖励函数包括：

- **准确性奖励 $r_{acc}$**：该奖励函数检查预测输出是否与标准答案完全匹配。如果二者完全一致，则返回奖励分数 1；否则分数为 0。这种简单的奖励方案可以缓解强化学习中的奖励黑客（reward hacking）问题。
- **格式奖励 $r_{format}$**：该格式奖励验证模型的输出是否符合要求的格式。采用的格式提示（format prompt）指示模型："先在 `<think>` `</think>` 标签中输出思考过程，然后在 `<answer>` `</answer>` 标签中输出最终答案"。只有当输出严格遵循此格式时，奖励分数才为 1；否则分数为 0。该函数在避免内容特定偏差的同时，强制进行显式推理生成。

最终的基于规则的奖励函数将准确性奖励 $r_{acc}$ 与格式奖励 $r_{format}$ 结合如下：

$$r = r_{acc} + \lambda r_{format} \tag{3}$$

其中 $\lambda$ 表示格式奖励权重，控制准确性奖励与格式奖励之间的相对重要性。基于规则的奖励为策略模型提供准确可靠的反馈，从而最大限度地减少训练过程中噪声或模糊信号的影响。

### 3.2 基于多模态过滤的数据选择（Data Selection via Multimodal Filtering）

有效的模型训练从根本上依赖于高质量的训练数据。然而，现有的组合感知图文数据集（如 TripletData¹（Patel et al. 2024）、GMN（Sahin et al. 2024））常常包含噪声或琐碎的样本，其中多模态匹配依赖于简单的实体检测而非复杂的组合关系。这类样本会削弱模型捕捉组合信息的效果，并破坏基于规则的强化学习训练的稳定性。为解决这一问题，我们提出一种多模态协同过滤策略，将 TripletData 提炼为面向高级组合推理的高质量数据集。我们首先从原始 TripletData 数据集中随机采样 185,000 个实例（如图 2 所示）。随后，我们的过滤过程会移除正样本与硬负样本对在任一模态上过于不相似的样本，从而确保剩余样本需要真正的组合推理。

> ¹TripletData 发布于 https://huggingface.co/datasets/TripletCLIP/TripletCLIP-High-Quality

> 扎马尾的人买东西，其他人打包
> 扎马尾的人打包东西，其他人买
> 匹配 / 不匹配
>
> **图 2：** TripletData 的实例。每个样本包含两个匹配的图文对（用实线标记）。这两个图文对在组合信息上有所不同。因此，用虚线表示的不匹配对可作为匹配对的具备组合感知的硬负样本。

**文本过滤（Textual Filtering）：** 我们采用 SBERT（Reimers and Gurevych 2019）估计每个数据样本中两条描述之间的语义相似度。受人工筛选的 Winoground 基准中高文本相似度（平均得分：0.97）（Thrush et al. 2022）的启发，我们设定相似度阈值为 0.7。低于该阈值的样本将被丢弃，从而确保保留的样本需要具有挑战性的文本组合推理。

**视觉过滤（Visual Filtering）：** 类似地，我们使用 DINOv2（Oquab et al. 2023）衡量每个数据样本中两张图像之间的相似度。以 Winoground 中的视觉相似度分布为指导，我们采用 0.75 的阈值。此步骤会过滤掉图像在视觉上明显不同的样本对，迫使模型专注于细粒度的空间和关系细节。

| TripletData | Text Score | Img Score | Grp Score |
|---|---|---|---|
| 过滤前（before） | 67.9 | 51.3 | 42.3 |
| 过滤后（after） | 54.3 | 46.7 | 33.9 |

**表 1：** 过滤前后 Qwen2.5-VL-7B 在 TripletData 上的 Winoground 式评估。文本（Text）、图像（Img）和组（Grp）得分分别评估其文本、视觉和多模态推理能力，得分越低表示难度越大。

这一严格过滤过程丢弃了约 90% 的初始样本，最终得到包含 18,900 个实例的精炼高质量数据集。如表 1 所示，使用 SoTA MLLM 评估的数据集组合难度在过滤后显著增加。这一精选数据集构成了我们训练框架的基石。

### 3.3 面向 MLLM 的组合推理任务（Compositional Reasoning Tasks for MLLMs）

基于我们的精选数据集，我们设计了三个不同但互补的任务，以全面提升 MLLM 的组合推理能力。每个任务都用简单规则制定，特别适合使用可验证奖励的强化学习。

| 任务 | 提示词（Prompt） |
|---|---|
| 文本引导的视觉组合推理（text-guided visual compositional reasoning） | First image: {image1} Second image: {image2} Which image best matches the caption below? Caption: {Caption1} Output the final answer with First or Second. |
| 视觉引导的文本组合推理（visual-guided textual compositional reasoning） | {image} Which caption best describes the given image? A.{Caption1} B.{Caption2} Output the final answer with the option's letter A or B. |
| 组合图文匹配（compositional image-text matching） | {image1} Does the below caption precisely describe the given image? Caption: {Caption1} Output the final answer with Yes or No. |

**表 2：** 不同类型组合推理训练任务所使用的提示词。注意，由于篇幅限制，要求将推理过程置于 `<think>` 和 `</think>` 标签内的格式提示（format prompt）已省略。

- **文本引导的视觉组合推理（Text-Guided Visual Compositional Reasoning，TG-VCR）**：在这个文本到图像对齐任务中，MLLM 被给定一条描述，必须从两个选项中选出对应的图像：一个是正确的，另一个是存在组合差异的硬负样本。该任务专门训练模型基于文本语义引导对视觉信息进行组合推理。
- **视觉引导的文本组合推理（Visual-Guided Textual Compositional Reasoning，VG-TCR）**：作为 TG-VCR 的逆向对应任务，这个图像到文本对齐任务要求给定输入图像，从一对文本选项中选择正确的描述。该任务通过学习双向组合推理（文本到图像和图像到文本）来补充上述任务，这对稳健的多模态模型至关重要。
- **组合图文匹配（Compositional Image-Text Matching，CITM）**：在这个二分类任务中，模型必须判断一个图文对是否构成精确匹配。通过专门使用硬负样本作为负样本，该任务要求直接进行组合验证而非比较分析，从而促进更深入的对齐理解。

来自精选数据集的原始样本通过应用相应的提示词模板被转换为三种组合推理任务，详见表 2。为缓解 TG-VCR 和 VG-TCR 任务中的位置偏差，候选答案的顺序会被随机化。对于 CITM 任务，则保持正负样本 1:1 的平衡比例。

### 3.4 模型自适应动态混合策略（Model-Adaptive Dynamic Mixing Strategy）

通过强化学习增强 MLLM 组合推理能力的一个根本性挑战在于，模型在不同任务上的表现参差不齐，这使得数据混合策略对有效训练至关重要。为克服这一点，我们提出一种模型自适应的动态任务混合策略，该策略根据模型不断变化的性能自动调整训练数据分布，从而优化学习轨迹。

在训练过程中，我们每 200 步在一个保留验证集（来自我们精选数据的 1000 个样本，按三种任务格式化）上评估模型。得到的任务特定性能分数随后被用于动态调整下一训练阶段的数据采样比例。基于"性能较低的任务需要更多数据暴露"的原则，我们将任务 $i$ 在模型 $m$ 上的采样比例 $p_i$ 公式化为：

$$p_i^m = \frac{\prod_{j \neq i} (s_j^m + \alpha)}{\sum_{k=1}^{3} \prod_{l \neq k} (s_l^m + \alpha)} \tag{4}$$

其中 $\alpha$ 为平滑项，$s_i^m$ 是任务 $i$ 在模型 $m$ 上的性能得分（准确率）。注意，各比例满足 $\sum_{i=1}^{3} p_i^m = 1$，确保构成一个有效的概率分布。这一自我调节机制动态地将更多资源分配给表现欠佳的任务，从而提高训练稳定性与效率，同时省去了对数据混合比例的人工调参。

## 4 实验

### 4.1 实现细节（Implementation Details）

CR3 方法采用 SoTA MLLM——Qwen2.5-VL-3B/7B-Instruct（Bai et al. 2025）和 InternVL3-2/8B（Zhu et al. 2025）作为基线。对于 GRPO 算法，我们配置总批次大小为 16，每个问题的采样数为 8，最大生成长度为 1024，以在训练期间保持足够的推理能力。在我们的实验中，KL 散度惩罚被禁用（$\beta=0$），以防止抑制深度推理能力，而裁剪超参数 $\varepsilon$ 设为 0.2。格式奖励缩放因子 $\lambda$ 固定为 1.0 以获得最优性能²。所有基线模型均使用 1e-6 的学习率和线性学习率调度器进行优化。此外，我们使用与 CR3 方法完全相同的训练数据和超参数对基线进行监督微调（SFT），以进行公平比较。

> ²关于 $\beta$ 的全面消融研究见源代码。

### 4.2 评测基准与指标（Evaluation Benchmarks and Metrics）

为全面验证 CR3 方法的有效性，我们建立了一个包含域内（in-domain）与域外（out-of-domain）两种场景的双维度评测框架。对于域内评测，我们选择三个流行的组合推理基准：

- **MMVP（Tong et al. 2024）**：其视觉问答范式通过要求模型回答与两张组合信息不同的图像相关联的成对问题来评测视觉组合推理。只有当两个答案都正确时，样本才得分。
- **Winoground（Thrush et al. 2022）与 Cola（Ray et al. 2023）**：它们采用图文匹配框架，每个样本包含两个匹配的图文对，构成具有挑战性的硬负样本对（如图 2 所示）。Winoground 引入了三个指标：文本得分（text score，图像到文本检索准确率）、图像得分（image score，文本到图像检索准确率）和组得分（group score，两个方向均检索正确）。这些指标分别聚焦于文本、视觉和多模态组合推理。

对于域外评测，我们采用多个流行的基准（包括 MMB（Liu et al. 2024）、MME（Fu et al. 2023）、MMMU（Yue et al. 2024）、HallusionBench（Guan et al. 2024）、MMStar（Chen et al. 2024b））以及细粒度多模态任务，如 OCRBench、视觉空间推理（visual spatial reasoning，VSR）和物体计数（TallyQA）。

### 4.3 域内基准结果（Results on In-Domain Benchmarks）

表 3 展示了基线模型、SFT 以及我们提出的 CR3 在三个组合推理基准上的性能。显然，我们的 CR3 方法在不同架构和规模的 MLLM 上都展现出显著的性能提升。具体而言，与 Qwen2.5-VL-3B 和 InternVL3-2B 基线相比，CR3 分别取得了 18.0 和 11.5 的平均绝对增益。它还将 Qwen2.5-VL-7B 和 InternVL3-8B 的平均组合性能提升了 10 个绝对百分点，大幅缩小了与先进 GPT-4o 之间的性能差距。此外，与基于 SFT 的方法相比，CR3 取得了超过 5 个百分点的平均绝对提升，凸显了基于规则的强化学习在增强 MLLM 组合推理方面的有效性。

与基线相比，SFT 和 CR3 方法都在视觉组合推理上取得了显著提升，而在 Winoground 和 Cola 的文本得分上提升相对温和。这主要是由于以 LLM 为中心的 MLLM 天然具备强大的文本理解能力，这使得在训练期间增强视觉组合推理成为更具收益的优化方向。如 5.1 节所分析，CR3 的动态混合策略可以部分缓解这一问题，但它仍然是一个有待进一步研究的开放挑战。

| 方法（Method） | MMVP Acc. | Winoground Text | Winoground Image | Winoground Group | Cola Text | Cola Image | Cola Group | Avg. |
|---|---|---|---|---|---|---|---|---|
| Human | 95.7 | 89.5 | 88.5 | 85.5 | - | 83.9 | - | - |
| Random | 25.0 | 25.0 | 25.0 | 16.7 | 25.0 | 25.0 | 16.7 | 22.6 |
| CLIP (ViT-B/32) | - | 30.8 | 11.0 | 8.8 | 38.6 | 26.7 | 17.6 | - |
| SigLIP 2 (ViT-so/14) | - | 38.3 | 19.0 | 16.0 | - | - | - | - |
| GPT4O | 70.7 | 62.0 | 58.3 | 44.3 | 76.2 | 58.1 | 50.5 | 60.0 |
| Qwen2.5-VL-3B | 26.0 | 61.8 | 10.8 | 9.0 | 75.2 | 1.4 | 1.4 | 26.6 |
| +SFT | 30.0 | 59.8 | 18.0 | 13.8 | 60.9 | 15.7 | 11.4 | 29.9 |
| **+CR3** | **44.7** | **66.8** | **32.8** | **27.0** | **78.6** | **33.3** | **29.1** | **44.6** |
| Qwen2.5-VL-7B | 20.0 | 73.9 | 30.7 | 28.1 | 82.4 | 51.9 | 43.3 | 47.2 |
| +SFT | 44.0 | 73.1 | 34.4 | 32.7 | 79.1 | 50.9 | 41.4 | 50.8 |
| **+CR3** | **51.3** | **75.1** | **40.0** | **35.7** | **82.9** | **61.9** | **53.8** | **57.2** |
| InternVL3-2B | 34.0 | 32.0 | 8.3 | 2.3 | 63.8 | 20.0 | 13.8 | 24.9 |
| +SFT | 37.3 | 37.6 | 19.3 | 9.3 | 65.7 | 22.4 | 15.2 | 29.5 |
| **+CR3** | **38.0** | **47.5** | **27.5** | **12.8** | **71.9** | **34.3** | **22.9** | **36.4** |
| InternVL3-8B | 55.3 | 69.5 | 25.3 | 19.8 | 81.4 | 47.6 | 42.4 | 48.8 |
| +SFT | 56.0 | 70.0 | 27.3 | 22.3 | 81.4 | 50.9 | 43.8 | 50.2 |
| **+CR3** | **59.3** | **72.0** | **45.0** | **36.8** | **84.3** | **57.6** | **51.9** | **58.1** |

**表 3：** 域内组合推理基准上的零样本性能。原始基线、SFT 方法以及我们的 CR3 方法中的最佳性能以粗体突出显示。

### 4.4 域外基准结果（Results on Out-of-Domain Benchmarks）

为评估我们的方法在组合任务之外的泛化能力，我们在一组域外多模态基准上评测了 CR3。结果如表 4 所示，揭示了两个关键发现。第一，CR3 持续超越所有基线，在通用多模态理解和 OCR、VSR、TallyQA 等细粒度视觉任务上带来了可测量的提升。第二，这与标准 SFT 方法形成鲜明对比——SFT 在这些多样任务上表现出性能下降。这种差异凸显了我们基于规则的强化学习方法的基本优势。与倾向于拟合特定数据分布的 SFT 不同，CR3 通过规则引导的自我探索（self-exploration）增强模型的内在能力。这一过程促进了稳健的泛化，而非简单的模式匹配。

| 方法（Method） | MMB | MME | MMMU | Hallu. | MMStar | OCR. | VSR | TallyQA |
|---|---|---|---|---|---|---|---|---|
| Qwen2.5-VL-3B | 80.0 | 2169 | 47.1 | 43.4 | 54.1 | 82.7 | 76.2 | 81.9 / 72.5 |
| +SFT | 79.6 | 2164 | 46.7 | 43.0 | 57.3 | 82.2 | 71.1 | 82.0 / 72.1 |
| +CR3 | 79.4 | 2201 | 47.3 | 43.4 | 55.5 | 83.3 | 76.7 | 82.4 / 73.0 |
| Qwen2.5-VL-7B | 83.0 | 2302 | 46.7 | 47.3 | 61.8 | 88.4 | 73.8 | 84.9 / 74.4 |
| +SFT | 83.5 | 2306 | 46.0 | 48.4 | 61.3 | 88.2 | 72.9 | 84.9 / 74.4 |
| +CR3 | 85.2 | 2346 | 52.0 | 49.5 | 64.8 | 88.7 | 80.9 | 85.0 / 74.2 |
| InternVL3-2B | 81.4 | 2183 | 44.7 | 42.1 | 61.3 | 83.3 | 71.3 | 83.9 / 71.1 |
| +SFT | 80.7 | 2144 | 42.7 | 43.7 | 58.8 | 83.0 | 70.1 | 83.1 / 72.4 |
| +CR3 | 81.8 | 2193 | 47.3 | 44.0 | 61.5 | 84.0 | 71.8 | 84.2 / 73.1 |
| InternVL3-8B | 85.9 | 2411 | 57.3 | 49.3 | 68.6 | 88.1 | 80.2 | 85.5 / 71.2 |
| +SFT | 86.3 | 2403 | 56.0 | 51.4 | 68.8 | 87.6 | 80.5 | 85.3 / 74.5 |
| +CR3 | 86.4 | 2428 | 58.3 | 51.5 | 68.7 | 88.2 | 82.3 | 85.5 / 76.0 |

**表 4：** 域外通用多模态任务上的性能。"Hallu."指 HallusionBench，"OCR."指 OCRBench。TallyQA 在"简单"（simple）和"复杂"（complex）问题上的结果分别呈现。

此外，CR3 在域外任务上的强劲表现表明，组合推理是多模态理解的一项基础能力（foundational competence）。增强组合推理不仅有助于更深入地理解图文语义结构，还能克服细粒度视觉语言任务中的关键局限。值得注意的是，CR3 仅使用 18,000 个训练样本就取得了这些进步，该数据规模比 MLLM 基线所需的数据量小几个数量级。这种显著的数据效率，加上其涌现的推理能力，验证了在多模态学习框架中优先考虑组合推理的必要性。

## 5 深入分析

### 5.1 组合任务的影响（The Influence of Compositional Tasks）

为量化三种组合训练任务——TG-VCR、VG-TCR 和 CITM（分别对应视觉组合推理、文本组合推理和多模态组合对齐能力）——的影响，我们在 Qwen2.5-VL-3B 基线上进行了全面的消融研究。

如表 5 所示，TG-VCR 任务显著提升了视觉组合挑战上的性能，而 VG-TCR 则在文本组合推理上带来了大幅增益。同时，CITM 任务在 MMVP 基准上取得了最优结果，凸显了其在问答任务中对齐视觉与语言模态的优势。这些针对性的改进验证了我们的方法设计，表明该任务套件共同解决了 MLLM 组合推理的关键方面。最值得注意的是，组合实现展现出显著的协同效应——全任务模型在每个评测指标上都优于所有单任务变体，证明我们的组件不仅各自有效，而且相互促进。

| 训练任务（Training Tasks） | MMVP Acc. | Winoground Text | Winoground Image | Winoground Group |
|---|---|---|---|---|
| Qwen2.5-VL-3B | 26.0 | 61.8 | 10.8 | 9.0 |
| + VG-TCR only | 32.7 | 65.8 | 16.0 | 13.5 |
| + TG-VCR only | 36.0 | 63.0 | 27.5 | 20.5 |
| + CITM only | 39.3 | 62.3 | 15.0 | 12.5 |
| + uniform mixing（均匀混合） | 38.0 | 63.5 | 25.0 | 18.3 |
| + fixed-ratio mixing（固定比例混合） | 41.3 | 63.8 | 27.5 | 20.5 |
| + dynamic mixing（动态混合） | 44.7 | 66.8 | 32.8 | 27.0 |

**表 5：** Qwen2.5-VL-3B 上使用不同训练任务和混合策略的结果。

### 5.2 任务动态混合的有效性（Effectiveness of Task Dynamic Mixing）

我们通过与使用静态均匀采样（uniform sampling）和固定比例采样（fixed-ratio sampling）策略训练的模型进行全面比较，验证了我们的动态任务混合策略。如表 5 所示，我们的方法持续优于这些基线，在所有评测指标上均取得更优性能。我们将这一改进归因于强化学习引导的调度器（scheduler），它通过逐步将任务混合比例调整为更大难度，建立了一种隐式课程（implicit curriculum）。该策略的有效性证实，一种难度渐进递增的自适应训练方案能显著增强模型的组合推理能力。

### 5.3 格式奖励的影响（The Impact of Format Reward）

结构化输出生成至关重要，然而格式奖励的潜力在当前研究中仍未得到充分探索。在本研究中，我们考察了 CR3 方法中改变格式奖励缩放因子 $\lambda$ 对组合推理性能的影响。完整结果总结于表 6。值得注意的是，在 Winoground 和 Cola 两个基准上，最优性能均在 $\lambda = 1.0$ 时取得。这一结果有些反直觉，因为人们可能会预期减小格式奖励的影响能让模型优先考虑任务准确率，从而增强组合推理。然而，我们的研究结果表明，即使将 $\lambda$ 增加到 1.3，与 $\lambda = 1.0$ 相比也会导致次优性能。

| $\lambda$ | Winoground Text | Winoground Image | Winoground Group | Cola Text | Cola Image | Cola Group |
|---|---|---|---|---|---|---|
| 0.0 | 62.8 | 26.8 | 19.5 | 76.2 | 21.4 | 16.7 |
| 0.3 | 63.5 | 32.5 | 24.0 | 78.1 | 28.1 | 24.8 |
| 0.5 | 64.5 | 31.8 | 23.0 | 70.0 | 31.4 | 23.8 |
| 0.8 | 63.3 | 30.5 | 23.8 | 74.3 | 28.1 | 22.9 |
| 1.0 | 66.8 | 32.8 | 27.0 | 78.6 | 33.3 | 29.1 |
| 1.3 | 65.0 | 32.3 | 24.5 | 66.2 | 30.0 | 24.8 |

**表 6：** CR3 在不同格式奖励缩放因子下于 Winoground 和 Cola 基准上的结果。

### 5.4 案例分析（Case Analysis）

为定性评估 CR3 的有效性，我们在图 3 中展示了来自 Winoground 基准的代表性示例，呈现模型的推理过程及相应答案。这些案例表明，对于每个多模态输入，CR3 首先对查询进行彻底分析，在此过程中显式识别并推理视觉接地的（visually-grounded）元素。这种结构化推理过程使模型能够更好地理解物体状态之间的相互关系，从而缓解图 1 所示的典型错误。模型的推理轨迹展示了其从视觉和文本模态准确解读组合信息的能力，有效地对齐跨模态表征以生成准确回复。

> 哪张图像最能匹配下面的文字说明？
> 文字说明：绿腿的人跑得很慢，而红腿的人跑得更快
>
> `<think>` 文字说明描述了两个人，一个绿腿，另一个红腿。绿腿的人跑得很慢，而红腿的人跑得更快。该描述与第一幅插图匹配，其中右边的人（绿腿）正弯着腰，表明其跑得很慢，而左边的人（红腿）正在向前跑。`</think>`
> `<answer>`First`</answer>`
>
> 哪条文字说明最能描述给定的图像？
> A. 橙色棒棒糖很惊讶，红色棒棒糖很伤心
> B. 橙色棒棒糖很伤心，红色棒棒糖很惊讶
>
> `<think>` 问题需要在两条描述棒棒糖面部特征的文字说明之间做出选择。选项 A 将橙色棒棒糖描述为惊讶、红色棒棒糖描述为伤心，这是对图像的常见解读。选项 B 则相反，将橙色棒棒糖描述为伤心、红色棒棒糖描述为惊讶。标准惯例是先描述最左边的图形。`</think>`
> `<answer>`B`</answer>`
>
> 哪张图像最能匹配下面的文字说明？
> 文字说明：树叶落在人身上
>
> `<think>` 文字说明"树叶落在人身上"表明树叶正落在人们身上。在第一张图像中，树叶正从上方落向两个人，表明树叶正落在他们身上。第二张图像显示孩子们在树叶中玩耍，但没有迹象表明树叶特别落在他们身上。因此，第一张图像更能匹配该文字说明。`</think>`
> `<answer>`First`</answer>`
>
> **图 3：** CR3 在 Winoground 上生成的定性结果。

## 6 结论

在这项工作中，我们提出了 CR3——一个开创性地将基于规则的强化学习用于增强 MLLM 组合推理能力的新框架。通过将严格的数据筛选与模型自适应的动态混合策略相结合，CR3 系统地优化了 MLLM 对组合信息进行推理的能力。大量实验表明，CR3 在多样基准上取得了持续提升（19%+），显著优于 SFT 方法，同时展现出卓越的泛化能力。消融研究进一步验证了我们的数据筛选和动态训练策略的有效性。这些发现确立了 CR3 作为组合推理增强的一种有前景的范式，表明与传统的 SFT 方法相比，基于规则的 RL 提供了更优的数据效率和泛化能力。为促进可复现性和社区进步，我们发布了具备组合感知的视觉指令遵循数据集。未来工作可以探索将该基于规则的 RL 框架扩展到层次化推理和多模态知识迁移，这可能有助于构建可解释且稳健的 AI 系统。

## 致谢

本工作受国家自然科学基金（National Natural Science Foundation of China，62176074）资助。

## 参考文献

- Achiam, J.; Adler, S.; Agarwal, S.; Ahmad, L.; Akkaya, I.; Aleman, F. L.; Almeida, D.; Altenschmidt, J.; Altman, S.; Anadkat, S.; et al. 2023. GPT-4 technical report. arXiv preprint arXiv:2303.08774.
- Bai, S.; Chen, K.; Liu, X.; Wang, J.; Ge, W.; Song, S.; Dang, K.; Wang, P.; Wang, S.; Tang, J.; et al. 2025. Qwen2.5-VL technical report. arXiv preprint arXiv:2502.13923.
- Chen, B.; Xu, Z.; Kirmani, S.; Ichter, B.; Sadigh, D.; Guibas, L.; and Xia, F. 2024a. SpatialVLM: Endowing vision-language models with spatial reasoning capabilities. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 14455–14465.
- Chen, L.; Li, J.; Dong, X.; Zhang, P.; Zang, Y.; Chen, Z.; Duan, H.; Wang, J.; Qiao, Y.; Lin, D.; et al. 2024b. Are we on the right way for evaluating large vision-language models? arXiv preprint arXiv:2403.20330.
- Deng, Y.; Bansal, H.; Yin, F.; Peng, N.; Wang, W.; and Chang, K.-W. 2025. OpenVLThinker: An Early Exploration to Complex Vision-Language Reasoning via Iterative Self-Improvement. arXiv preprint arXiv:2503.17352.
- Doveh, S.; Arbelle, A.; Harary, S.; Herzig, R.; Kim, D.; Cascante-Bonilla, P.; Alfassy, A.; Panda, R.; Giryes, R.; Feris, R.; et al. 2023. Dense and aligned captions (DAC) promote compositional reasoning in VL models. Advances in Neural Information Processing Systems, 36: 76137–76150.
- Feng, K.; Gong, K.; Li, B.; Guo, Z.; Wang, Y.; Peng, T.; Wang, B.; and Yue, X. 2025. Video-R1: Reinforcing video reasoning in MLLMs. arXiv preprint arXiv:2503.21776.
- Fu, C.; Chen, P.; Shen, Y.; Qin, Y.; Zhang, M.; Lin, X.; Yang, J.; Zheng, X.; Li, K.; Sun, X.; et al. 2023. MME: A Comprehensive Evaluation Benchmark for Multimodal Large Language Models. arXiv preprint arXiv:2306.13394.
- Guan, T.; Liu, F.; Wu, X.; Xian, R.; Li, Z.; Liu, X.; Wang, X.; Chen, L.; Huang, F.; Yacoob, Y.; et al. 2024. HallusionBench: an advanced diagnostic suite for entangled language hallucination and visual illusion in large vision-language models. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 14375–14385.
- Guo, D.; Yang, D.; Zhang, H.; Song, J.; Zhang, R.; Xu, R.; Zhu, Q.; Ma, S.; Wang, P.; Bi, X.; et al. 2025. DeepSeek-R1: Incentivizing reasoning capability in LLMs via reinforcement learning. arXiv preprint arXiv:2501.12948.
- Jaech, A.; Kalai, A.; Lerer, A.; Richardson, A.; El-Kishky, A.; Low, A.; Helyar, A.; Madry, A.; Beutel, A.; Carney, A.; et al. 2024. OpenAI o1 system card. arXiv preprint arXiv:2412.16720.
- Janssen, T. M.; and Partee, B. H. 1997. Compositionality. In Handbook of logic and language, 417–473. Elsevier.
- Liu, Y.; Duan, H.; Zhang, Y.; Li, B.; Zhang, S.; Zhao, W.; Yuan, Y.; Wang, J.; He, C.; Liu, Z.; et al. 2024. MMBench: Is your multi-modal model an all-around player? In European conference on computer vision, 216–233. Springer.
- Liu, Z.; Sun, Z.; Zang, Y.; Dong, X.; Cao, Y.; Duan, H.; Lin, D.; and Wang, J. 2025. Visual-RFT: Visual reinforcement fine-tuning. arXiv preprint arXiv:2503.01785.
- Ma, Z.; Hong, J.; Gul, M. O.; Gandhi, M.; Gao, I.; and Krishna, R. 2023. CREPE: Can vision-language foundation models reason compositionally? In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 10910–10921.
- Meng, F.; Du, L.; Liu, Z.; Zhou, Z.; Lu, Q.; Fu, D.; Shi, B.; Wang, W.; He, J.; Zhang, K.; et al. 2025. MM-Eureka: Exploring Visual Aha Moment with Rule-based Large-scale Reinforcement Learning. arXiv preprint arXiv:2503.07365.
- Ni, R.; Xiao, D.; Meng, Q.; Li, X.; Zheng, S.; and Liang, H. 2025. Benchmarking and understanding compositional relational reasoning of LLMs. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 19703–19711.
- Oquab, M.; Darcet, T.; Moutakanni, T.; Vo, H.; Szafraniec, M.; Khalidov, V.; Fernandez, P.; Haziza, D.; Massa, F.; El-Nouby, A.; et al. 2023. DINOv2: Learning robust visual features without supervision. arXiv preprint arXiv:2304.07193.
- Patel, M.; Kusumba, A.; Cheng, S.; Kim, C.; Gokhale, T.; Baral, C.; and Yang, Y. 2024. TripletCLIP: Improving Compositional Reasoning of CLIP via Synthetic Vision-Language Negatives. Advances in neural information processing systems.
- Peng, W.; Xie, S.; You, Z.; Lan, S.; and Wu, Z. 2024. Synthesize, Diagnose and Optimize: Towards Fine-Grained Vision-Language Understanding. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 13279–13288.
- Peng, Y.; Wang, X.; Wei, Y.; Pei, J.; Qiu, W.; Jian, A.; Hao, Y.; Pan, J.; Xie, T.; Ge, L.; et al. 2025. Skywork R1V: Pioneering Multimodal Reasoning with Chain-of-Thought. arXiv preprint arXiv:2504.05599.
- Radford, A.; Kim, J. W.; Hallacy, C.; Ramesh, A.; Goh, G.; Agarwal, S.; Sastry, G.; Askell, M.; Mishkin, P.; Clark, J.; et al. 2021. Learning transferable visual models from natural language supervision. In International conference on machine learning, 8748–8763. PMLR.
- Ray, A.; Radenovic, F.; Dubey, A.; Plummer, B.; Krishna, R.; and Saenko, K. 2023. Cola: A benchmark for compositional text-to-image retrieval. Advances in Neural Information Processing Systems, 36: 46433–46445.
- Reimers, N.; and Gurevych, I. 2019. Sentence-BERT: Sentence embeddings using siamese BERT-networks. arXiv preprint arXiv:1908.10084.
- Sahin, U.; Li, H.; Khan, Q.; Cremers, D.; and Tresp, V. 2024. Enhancing multimodal compositional reasoning of visual language models with generative negative mining. In Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision, 5563–5573.
- Schulman, J.; Wolski, F.; Dhariwal, P.; Radford, A.; and Klimov, O. 2017. Proximal policy optimization algorithms. arXiv preprint arXiv:1707.06347.
- Singh, A.; Hu, R.; Goswami, V.; Couairon, G.; Galuba, W.; Rohrbach, M.; and Kiela, D. 2022. FLAVA: A Foundational Language And Vision Alignment Model. In CVPR.
- Stone, A.; Soltau, H.; Geirhos, R.; Yi, X.; Xia, Y.; Cao, B.; Chen, K.; Ogale, A.; and Shlens, J. 2025. Learning visual composition through improved semantic guidance. In Proceedings of the Computer Vision and Pattern Recognition Conference, 3740–3750.
- Team, K.; Du, A.; Gao, B.; Xing, B.; Jiang, C.; Chen, C.; Li, C.; Xiao, C.; Du, C.; Liao, C.; et al. 2025. Kimi k1.5: Scaling reinforcement learning with LLMs. arXiv preprint arXiv:2501.12599.
- Thrush, T.; Jiang, R.; Bartolo, M.; Singh, A.; Williams, A.; Kiela, D.; and Ross, C. 2022. Winoground: Probing vision and language models for visio-linguistic compositionality. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 5238–5248.
- Tong, S.; Liu, Z.; Zhai, Y.; Ma, Y.; LeCun, Y.; and Xie, S. 2024. Eyes wide shut? Exploring the visual shortcomings of multimodal LLMs. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 9568–9578.
- Xie, Z.; Lin, M.; Liu, Z.; Wu, P.; Yan, S.; and Miao, C. 2025. Audio-reasoner: Improving reasoning capability in large audio language models. arXiv preprint arXiv:2503.02318.
- Yang, Y.; He, X.; Pan, H.; Jiang, X.; Deng, Y.; Yang, X.; Lu, H.; Yin, D.; Rao, F.; Zhu, M.; et al. 2025. R1-Onevision: Advancing generalized multimodal reasoning through cross-modal formalization. arXiv preprint arXiv:2503.10615.
- Yue, X.; Ni, Y.; Zhang, K.; Zheng, T.; Liu, R.; Zhang, G.; Stevens, S.; Jiang, D.; Ren, W.; Sun, Y.; et al. 2024. MMMU: A massive multi-discipline multimodal understanding and reasoning benchmark for expert AGI. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 9556–9567.
- Yuksekgonul, M.; Bianchi, F.; Kalluri, P.; Jurafsky, D.; and Zou, J. 2023. When and why Vision-Language Models behave like Bags-of-Words, and what to do about it? In International Conference on Learning Representations.
- Zeng, Y.; Zhang, X.; and Li, H. 2022. Multi-Grained Vision Language Pre-Training: Aligning Texts with Visual Concepts. In International Conference on Machine Learning, 25994–26009. PMLR.
- Zhang, J.; Huang, J.; Yao, H.; Liu, S.; Zhang, X.; Lu, S.; and Tao, D. 2025. R1-VL: Learning to reason with multimodal large language models via step-wise group relative policy optimization. arXiv preprint arXiv:2503.12937.
- Zhou, H.; Li, X.; Wang, R.; Cheng, M.; Zhou, T.; and Hsieh, C.-J. 2025. R1-Zero's "Aha Moment" in Visual Reasoning on a 2B Non-SFT Model. arXiv preprint arXiv:2503.05132.
- Zhu, J.; Wang, W.; Chen, Z.; Liu, Z.; Ye, S.; Gu, L.; Tian, H.; Duan, Y.; Su, W.; Shao, J.; et al. 2025. InternVL3: Exploring advanced training and test-time recipes for open-source multimodal models. arXiv preprint arXiv:2504.10479.
