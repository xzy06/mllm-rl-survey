# 中英对照审读稿

## [0:0] (gtx)
- ZH: 多模态大语言模型组合推理中的强化学习方法：奖励信号的演进
- EN: Reinforcement learning methods in combinatorial inference of multimodal large language models: the evolution of reward signals

## [1:0] (gtx)
- ZH: 席致远
- EN: Xi Zhiyuan

## [2:0] (gtx)
- ZH: 南方科技大学 工学院，广东 珠海 519000，12412015@sustech.edu.cn
- EN: School of Engineering, Southern University of Science and Technology, Zhuhai, Guangdong 519000, 12412015@sustech.edu.cn

## [4:0] (gtx)
- ZH: 摘要：多模态大语言模型（Multimodal Large Language Models, MLLMs）在通用视觉-语言任务上表现优异，却在组合推理（compositional reasoning）上存在系统性缺陷，即难以将物体、属性与空间/逻辑关系精确绑定。强化学习后训练是弥补这一缺口的有效手段，而奖励信号的设计直接决定组合能力能否被真正激发。本文综述 2024 ~ 2026 年间用强化学习增强 MLLM 组合推理的代表性工作，提出以“奖励信号演进”为核心的分析框架，将现有方法划分为验证器奖励、视觉对齐奖励与推理过程优化三类，并沿奖励来源、奖励粒度、监督需求、组合触及度等统一维度逐方法剖析。分析表明，奖励信号正从对最终回答的结果验证，逐步演进为对视觉语义结构的对齐与对推理过程的对齐；组合推理“正确性必须可定义”的约束是这一演进的深层驱动力，而面向组合绑定的显式视觉语义奖励是当前最有前景的研究缺口。
- EN: Abstract: Multimodal Large Language Models (MLLMs) perform well in general visual-language tasks, but have systemic flaws in compositional reasoning, that is, it is difficult to accurately bind objects, attributes and spatial/logical relationships. Post-reinforcement learning training is an effective means to fill this gap, and the design of the reward signal directly determines whether the combined ability can be truly stimulated. This article reviews the representative work on using reinforcement learning to enhance MLLM combinatorial inference from 2024 to 2026, proposes an analysis framework with "reward signal evolution" as the core, divides existing methods into three categories: validator reward, visual alignment reward and inference process optimization, and analyzes method by method along unified dimensions such as reward source, reward granularity, supervision requirements, and combinatorial reach. The analysis shows that the reward signal is gradually evolving from the verification of the final answer to the alignment of the visual semantic structure and the alignment of the reasoning process; the constraint that "correctness must be definable" in combinatorial reasoning is the deep driving force of this evolution, and explicit visual semantic rewards for combinatorial binding are currently the most promising research gaps.

## [5:0] (gtx)
- ZH: 关键词：多模态大语言模型；组合推理；强化学习；奖励信号
- EN: Keywords: multimodal large language model; combinatorial reasoning; reinforcement learning; reward signal

## [6:0] (gtx)
- ZH: 1. 引言
- EN: 1. Introduction

## [7:0] (gtx)
- ZH: 多模态大语言模型（Multimodal Large Language Models, MLLMs）在视觉问答、图像描述等通用任务上已接近人类水平，然而在组合推理（compositional reasoning）上仍存在系统性缺陷，即难以将物体、属性与空间/逻辑关系精确绑定。大规模评测揭示了这一缺陷的普遍性：CREPE 发现组合理解随组合复杂度增加而显著退化 [1]；ARO 指出视觉语言模型本质上像“词袋模型”，对词序与组合结构不敏感 [2]；SugarCrepe 显示，纯绑定测试（Swap）是其评测的预训练 CLIP 模型的普遍薄弱环节 [3]。这些结果表明，组合推理缺陷是当前 MLLM 的系统性短板。
- EN: Multimodal Large Language Models (MLLMs) are close to human level in general tasks such as visual question answering and image description. However, there are still systematic flaws in compositional reasoning, that is, it is difficult to accurately bind objects, attributes and spatial/logical relationships. Large-scale evaluations have revealed the prevalence of this flaw: CREPE found that combinatorial understanding degrades significantly as combinatorial complexity increases [1]; ARO pointed out that visual language models are essentially like "bag-of-words models" and are insensitive to word order and combinatorial structure [2]; SugarCrepe showed that pure binding testing (Swap) is a common weak link in the pre-trained CLIP models it evaluated [3]. These results suggest that combinatorial inference flaws are a systematic shortcoming of current MLLMs.

## [8:0] (gtx)
- ZH: 组合缺陷的根源可追溯到训练信号本身。ARO 的 shortcut 分析表明，现有对比预训练的目标并不要求模型理解组合结构，模型仅凭词频与整体语义即可取得高分 [2]；CREPE 的证据显示，组合性缺陷与模型规模无关，单纯扩大数据与参数无法自动习得组合能力 [1]。在此背景下，强化学习（Reinforcement Learning, RL）后训练成为主流手段，奖励的定义方式直接决定训练方向：与监督微调（SFT）直接灌输标准答案不同，RL 通过奖励信号让模型在试错中习得推理行为。例如 CR³ 将组合推理重新设计为答案可自动判分的任务，以规则判定的确定性奖励驱动 RL，论文报告其在组合基准上较原始基线平均提升约 10 个百分点 [4]。由此浮现关键问题：什么样的奖励信号才能真正驱动组合推理能力？
- EN: The origin of the combinational flaws can be traced back to the training signals themselves. ARO's shortcut analysis shows that the current goal of comparative pre-training does not require the model to understand the combination structure, and the model can achieve high scores based only on word frequency and overall semantics [2]; CREPE's evidence shows that combination defects have nothing to do with model size, and simply expanding data and parameters cannot automatically acquire combination capabilities [1]. In this context, post-training after reinforcement learning (RL) has become a mainstream method, and the way rewards are defined directly determines the direction of training: Unlike supervised fine-tuning (SFT), which directly instills standard answers, RL uses reward signals to allow the model to learn reasoning behaviors through trial and error. For example, CR³ redesigns combinatorial reasoning into a task where answers can be automatically scored, and drives RL with deterministic rewards for rule determination. The paper reports that it improves the combinatorial benchmark by an average of about 10 percentage points compared with the original baseline [4]. The key question emerges from this: What kind of reward signal can truly drive combinatorial reasoning ability?

## [9:0] (gtx)
- ZH: 本文梳理 2024 ~ 2026 年间用 RL 增强 MLLM 组合推理的代表性工作后发现，其发展本质上是奖励信号从“结果验证”向“视觉语义结构对齐”与“推理过程对齐”的逐步扩展，即奖励作用对象的扩展（答案→视觉结构→推理过程），三个方向至今并行发展：一类以对最终回答的结构化结果验证为奖励来源（CR³、SpatialThinker、SVQA-R1），一类以回答与视觉语义结构的对齐程度为奖励来源（Ground-R1、GRIT、POLIA），一类将优化信号作用于推理过程本身（Self-Questioning VLM、H-GRPO）。推动演进的深层驱动力，是组合推理“正确性必须可定义”的约束。
- EN: This article summarizes the use of RL to enhance MLLM from 2024 to 2026 After representative work on combinatorial reasoning, it was found that its development is essentially a gradual expansion of reward signals from "result verification" to "visual semantic structure alignment" and "reasoning process alignment", that is, the expansion of reward objects (answer → visual structure → reasoning process). Three directions have developed in parallel so far: one type is based on the structured result verification of the final answer. Reward sources (CR³, SpatialThinker, SVQA-R1), one is based on the alignment of the answer with the visual semantic structure (Ground-R1, GRIT, POLIA), and the other is based on the optimization signal acting on the reasoning process itself (Self-Questioning) VLM, H-GRPO). The deep driving force for evolution is the constraint that "correctness must be definable" in combinatorial reasoning.

## [10:0] (gtx)
- ZH: 本文以奖励信号演进为主线进行系统性综述，具体贡献如下：首先，首次以“奖励信号演进”为分析轴，将相关方法组织为连续谱系而非孤立方法的堆叠；其次，提出三分法分类框架，即验证器奖励、视觉对齐奖励与推理过程优化，并沿统一维度（奖励来源、监督需求、组合触及度、评测与局限）逐方法剖析；最后，分析可验证性约束对奖励设计的制约，讨论基准碎片化、文本偏置等开放问题，并展望未来方向。
- EN: This article conducts a systematic review with the evolution of reward signals as the main line. The specific contributions are as follows: First, for the first time, the "evolution of reward signals" is used as the analysis axis to organize related methods into a continuous lineage rather than a stack of isolated methods; secondly, a three-part classification framework is proposed, that is, validator rewards, visual pairs Optimize the reward and inference process, and analyze method by method along the same dimension (reward source, supervision requirements, combination reach, evaluation and limitations); finally, analyze the constraints of verifiability constraints on reward design, discuss open issues such as benchmark fragmentation and text bias, and look forward to future directions.

## [11:0] (gtx)
- ZH: 本文筛选遵循四条标准：第一，时间范围为 2024–2026 年，来源为 arXiv 预印本与正式发表论文；第二，方法必须面向多模态大语言模型并以强化学习（GRPO、PPO、DPO 等）为后训练手段，纯评测基准（VALSE、ARO、SugarCrepe 等）仅作为评测工具引用；第三，奖励信号设计必须是方法的核心贡献；第四，代表性优先，每个子方向选取 1–3 个代表性工作。三类方法的划定依据是奖励信息来源：外部判据对最终回答的验证归入验证器奖励，回答与视觉证据关系的对齐归入视觉对齐奖励，推理过程本身的信用分配归入推理过程优化。
- EN: The selection of this article follows four criteria: first, the time range is 2024–2026, and the source is arXiv preprints and officially published papers; second, the method must be oriented to multi-modal large language models and use reinforcement learning (GRPO, PPO, DPO, etc.) as post-training means, pure evaluation benchmarks (VALSE, ARO, SugarCrepe etc.) are only cited as evaluation tools; third, reward signal design must be the core contribution of the method; fourth, representation is given priority, and 1–3 representative works are selected from each sub-direction. The three categories of methods are delineated based on the source of reward information: the verification of the final answer by external criteria is classified as the verifier reward, the alignment of the relationship between the answer and the visual evidence is classified as the visual alignment reward, and the credit allocation of the reasoning process itself is classified as the optimization of the reasoning process.

## [12:0] (gtx)
- ZH: 2. 背景
- EN: 2. Background

## [13:0] (gtx)
- ZH: 2.1 组合推理的定义与评测基准
- EN: 2.1 Definition and evaluation benchmark of combinatorial reasoning

## [14:0] (gtx)
- ZH: 本文所称组合推理，指模型将视觉场景中的物体、属性与空间/逻辑关系精确绑定起来完成理解与推理的能力。它与“把问题分解为子问题”的推理范式不同：组合推理的核心在于绑定，要求模型同时识别物体、属性与空间位置，任何一处绑定错误都会导致整体理解偏差。这一区分针对推理目标而非手段，分解可以成为达成绑定的手段（3.3 节方法正以显式分解逼近绑定目标）。由此，组合推理可操作化为三个子问题：属性绑定、空间/逻辑关系与词序/结构敏感度。
- EN: The term combinatorial reasoning in this article refers to the model's ability to accurately bind objects, attributes and spatial/logical relationships in a visual scene to complete understanding and reasoning. It is different from the reasoning paradigm of "decomposing the problem into sub-problems": the core of combinatorial reasoning lies in binding, which requires the model to identify objects, attributes and spatial locations at the same time. Any binding error will lead to overall understanding deviation. This distinction is aimed at the reasoning goal rather than the means, and decomposition can become a means to achieve binding (the method in Section 3.3 is approaching the binding goal with explicit decomposition). From this, combinatorial reasoning can be operationalized into three sub-problems: attribute binding, spatial/logical relationship and word order/structure sensitivity.

## [15:0] (gtx)
- ZH: 围绕上述能力，学界构建了一系列评测基准。VALSE 通过构造伪造实例，测试模型对存在性、计数、空间关系等语言现象的判断 [5]；CREPE 将评测规模扩大至 37 万级图文对，从系统性与生产力两个维度系统考察组合性 [1]；ARO 以 5 万级用例覆盖属性、关系与词序三类组合结构，并揭示现有检索基准不要求组合理解、模型可绕道得分的 shortcut [2]；SugarCrepe 针对程序化基准易被 hack 的问题，用 LLM 生成语义合理的困难负样本，将评测收敛为 Replace、Swap、Add 三类原子操作 [3]。
- EN: Focusing on the above abilities, the academic community has constructed a series of evaluation benchmarks. VALSE tests the model's judgment on language phenomena such as existence, counting, and spatial relationships by constructing fake examples [5]; CREPE expands the evaluation scale to 370,000 image-text pairs, and systematically examines combinatoriality from the two dimensions of systematicity and productivity [1]; ARO covers three types of combination structures of attributes, relationships, and word order with 50,000 use cases, and reveals that existing retrieval benchmarks do not require combinatorial understanding, and the model can bypass shortcuts to score [2]; SugarCrepe targets programmatic benchmarks that are easily hacked For the problem, LLM is used to generate difficult negative samples with reasonable semantics, and the evaluation is converged into three types of atomic operations: Replace, Swap, and Add [3].

## [16:0] (gtx)
- ZH: 尽管各基准的评测协议不同，失败模式却高度一致：物体识别强于属性绑定，属性强于关系理解，纯粹的绑定（Swap）最难（综合多基准结论）。这为后续 RL 方法提供了明确的优化靶点。但各方法在评测集选择上各行其是，协议互不兼容，导致结果难以横向比较，这一“基准碎片化”问题将在第 4 节讨论。表 1 汇总了上述基准的核心信息。
- EN: Although the evaluation protocols of each benchmark are different, the failure modes are highly consistent: object recognition is stronger than attribute binding, attributes are stronger than relationship understanding, and pure binding (Swap) is the most difficult (comprehensive multi-benchmark conclusion). This provides clear optimization targets for subsequent RL methods. However, each method has its own way of selecting evaluation sets, and the protocols are incompatible with each other, making it difficult to compare results horizontally. This "benchmark fragmentation" problem will be discussed in Section 4. Table 1 summarizes the core information of the above benchmarks.

## [17:0] (gtx)
- ZH: 表 1：组合推理评测基准对比
- EN: Table 1: Comparison of combinatorial reasoning evaluation benchmarks

## [18:0] (gtx)
- ZH: 基准
- EN: benchmark

## [19:0] (gtx)
- ZH: 子任务维度
- EN: subtask dimensions

## [20:0] (gtx)
- ZH: 评测方式
- EN: Evaluation method

## [21:0] (gtx)
- ZH: 规模
- EN: scale

## [22:0] (gtx)
- ZH: 关键发现
- EN: Key findings

## [24:0] (gtx)
- ZH: 存在/复数/计数/空间关系/动作/共指
- EN: Existence/plural/counting/spatial relations/action/coreference

## [25:0] (gtx)
- ZH: 真假判断（foiled instances）
- EN: True or False Judgment (foiled instances)

## [26:0] (gtx)
- ZH: 6,795 例
- EN: 6,795 cases

## [27:0] (gtx)
- ZH: 存在性强、计数尚可；复数/空间/共指/动作偏弱
- EN: Strong presence, acceptable counting; weak plural/space/core-reference/action

## [29:0] (gtx)
- ZH: 系统性/生产力
- EN: Systematic/Productivity

## [30:0] (gtx)
- ZH: 检索（seen-unseen splits + 复杂度梯度）
- EN: Retrieval (seen-unseen splits + complexity gradient)

## [31:0] (gtx)
- ZH: 37 万级
- EN: Level 370,000

## [32:0] (gtx)
- ZH: 缺陷与规模无关
- EN: Defects have nothing to do with size

## [34:0] (gtx)
- ZH: 属性/关系/词序
- EN: Attributes/relationships/word order

## [35:0] (gtx)
- ZH: 检索
- EN: Search

## [36:0] (gtx)
- ZH: 5 万级
- EN: Level 50,000

## [37:0] (gtx)
- ZH: 词袋模型；存在 shortcut
- EN: Bag of words model; shortcut exists

## [39:0] (gtx)
- ZH: Replace：物/属/关系；Swap/Add：物/属
- EN: Replace: object/attribute/relationship; Swap/Add: object/attribute

## [40:0] (gtx)
- ZH: 二选一检索
- EN: Choose one search

## [41:0] (gtx)
- ZH: 7.5 千级
- EN: 7.5 thousand level

## [42:0] (gtx)
- ZH: Swap 最难（预训练 CLIP）；物体 > 属性 > 关系
- EN: Swap is the hardest (pre-trained CLIP); Object > Attribute > Relationship

## [43:0] (gtx)
- ZH: 2.2 RL 基础与奖励信号演进主线
- EN: 2.2 Main line of RL foundation and reward signal evolution

## [44:0] (gtx)
- ZH: 将强化学习引入视觉-语言对齐的早期工作沿用了 LLM 的 RLHF 与 RLAIF 范式。LLaVA-RLHF [6]、RLHF-V [7]、Silkie [8] 等工作共同确立了“奖励来自对回答的评判”这一范式，反馈粒度停留在回答整体或语言片段，尚未触及组合绑定正确性。
- EN: Early work introducing reinforcement learning to visual-language alignment followed the RLHF and RLAIF paradigms of LLM. LLaVA-RLHF [6], RLHF-V [7], Silkie [8] and other works have jointly established the paradigm of "rewards come from the judgment of answers". The feedback granularity stays at the answer as a whole or language fragments, and has not yet touched the correctness of the combination binding.

## [45:0] (gtx)
- ZH: 数学推理领域的突破改变了奖励信号的设计方式。DeepSeekMath 提出的 GRPO [9] 去除了 PPO 的价值网络，对同一问题采样多个回答，用组内相对优势
- EN: Breakthroughs in mathematical reasoning have changed the way reward signals are designed. GRPO [9] proposed by DeepSeekMath removes the value network of PPO, samples multiple answers to the same question, and uses the relative advantages within the group

## [47:0] (gtx)
- ZH: 替代 critic 打分，配合确定性规则验证器提供奖励，开辟了“可验证奖励强化学习”（RL with Verifiable Rewards, RLVR；术语由 Tülu 3 提出，经 DeepSeek-R1 推广）路线。一个自然的对照是直接偏好优化（DPO）[10]：它以离线偏好对为原料、无需显式奖励模型，在可验证奖励设定下也可自动构造偏好对；但 DPO 的偏好对来自固定采样分布，不随策略迭代更新，难以从模型自生成的新推理路径中持续获益。GRPO 的在线组采样、组内相对优势以及与规则/结构化奖励的天然兼容性，是本文 3.1 ~ 3.3 各方法普遍以其为算法底座、并在此基础上扩展奖励粒度的深层原因。
- EN: Replacing critic scoring and providing rewards with a deterministic rule verifier opens up the "RL with Verifiable Rewards, RLVR; term proposed by Tülu 3 and popularized by DeepSeek-R1" route. A natural comparison is Direct Preference Optimization (DPO) [10]: it uses offline preference pairs as raw materials, does not require an explicit reward model, and can automatically construct preference pairs under verifiable reward settings; however, DPO's preference pairs come from a fixed sampling distribution and are not iteratively updated with the strategy, making it difficult to continuously benefit from new inference paths self-generated by the model. GRPO's online group sampling, relative advantages within the group, and natural compatibility with rules/structured rewards are the underlying reasons why the methods in 3.1 ~ 3.3 of this article generally use it as the algorithm base and expand the reward granularity on this basis.

## [48:0] (gtx)
- ZH: 进一步的理论分析表明，GRPO 与过程奖励模型（Process Reward Model, PRM）并非两条独立路线：在 token 级策略梯度与单次更新的设定下，标准 GRPO 目标与 PRM-aware 目标数学等价，组内多条回答的共享前缀天然定义了“过程步骤”，GRPO 一直在隐式地做过程级信用分配 [11]。多模态侧，VisualPRM 等工作已将 PRM 扩展到多模态推理 [12]。
- EN: Further theoretical analysis shows that GRPO and Process Reward Model (PRM) are not two independent routes: under the settings of token-level policy gradient and single update, the standard GRPO goal and the PRM-aware goal are mathematically equivalent. The shared prefix of multiple answers in the group naturally defines the "process step", and GRPO has been implicitly assigning process-level credit [11]. On the multimodal side, work such as VisualPRM has extended PRM to multimodal reasoning [12].

## [49:0] (gtx)
- ZH: 至此，奖励信号的可验证性来源经历了一次根本转变：从人类/AI 的主观打分走向规则与结构的确定性验证。然而组合推理不同于数学，它没有唯一标准答案，正确性恰恰藏在属性与关系的绑定之中。如何为这种绑定定义可验证的奖励信号，正是第 3 节三类方法的出发点。
- EN: At this point, the source of verifiability of reward signals has undergone a fundamental shift: from subjective scoring by humans/AI to deterministic verification of rules and structures. However, combinatorial reasoning is different from mathematics in that it does not have a single standard answer. The correctness lies precisely in the binding of attributes and relationships. How to define a verifiable reward signal for this binding is the starting point for the three categories of methods in Section 3 .

## [50:0] (gtx)
- ZH: 3. 方法分类
- EN: 3. Classification of methods

## [51:0] (gtx)
- ZH: 根据奖励信号的增量贡献，现有方法可归纳为三类：结果验证奖励、视觉对齐奖励和推理过程奖励，分别对应组合推理中“是否正确”“是否看对”与“是否合理推理”三个层面的优化目标。具体地，判据设计创新（如何判定对错）归入 3.1，信号源创新（奖励依据什么）归入 3.2，优化对象创新（奖励作用于哪里）归入 3.3；各方法继承自 RLVR 底座（如 GRPO 的答案验证）的通用成分不计入分类依据。类别之间体现的是奖励粒度的扩展而非严格的继承关系；本节按三类展开梳理，每篇方法按统一维度（奖励来源、监督需求、组合触及度、评测与局限）呈现，类别间的关系集中于 3.4 节讨论。
- EN: According to the incremental contribution of reward signals, existing methods can be summarized into three categories: result verification rewards, visual alignment rewards and reasoning process rewards, which respectively correspond to the optimization goals at the three levels of "whether it is correct", "whether it is correct" and "whether it is reasonable to reason" in combined reasoning. Specifically, criterion design innovation (how to determine right or wrong) is classified into 3.1, signal source innovation (what rewards are based on) is classified into 3.2, and optimization object innovation (where rewards are used) is classified into 3.3; the common components inherited by each method from the RLVR base (such as GRPO's answer verification) are not included in the classification basis. The categories reflect the expansion of reward granularity rather than a strict inheritance relationship; this section is organized into three categories, and each method is presented according to unified dimensions (reward sources, supervision requirements, combination reach, evaluation and limitations). The relationship between categories is discussed in Section 3.4.

## [52:0] (gtx)
- ZH: 3.1验证器奖励（Verifier-based）
- EN: 3.1 Verifier rewards (Verifier-based)

## [53:0] (gtx)
- ZH: 验证器奖励建立在“正确性可定义”的前提上：当任务的答案可由规则、程序或结构约束自动判定时，验证器就能提供确定性训练信号，无需训练奖励模型。本文的“验证器”取确定性判据之义，与学习式验证器相对——后者如过程奖励模型（PRM）需标注数据训练获得，本文将其作为向 3.3 过程建模过渡的桥梁在第 3.3 节讨论；判据既可对照外部标准，也可退化为无外部标准的自洽性检查（SVQA-R1 的一致性判据即属此类，是向自监督方向的延伸）。组合推理的错误集中在精细绑定上，而绑定正误在一定任务设计下可以自动判定。围绕“验证什么”，不同工作分别验证最终答案、推理的中间结构与回答的跨视角一致性。
- EN: Validator rewards are built on the premise that "correctness is definable": when the answer to a task can be automatically determined by rules, procedures, or structural constraints, the validator can provide a deterministic training signal without the need to train a reward model. The "verifier" in this article means a deterministic criterion, as opposed to a learning verifier - the latter, such as the Process Reward Model (PRM), needs to be trained with annotated data. This article uses it as a bridge to transition to 3.3 process modeling and discusses it in Section 3.3; the criterion can either be compared with external standards or degenerate into a self-consistency check without external standards (the consistency criterion of SVQA-R1 falls into this category and is an extension to the direction of self-supervision). Errors in combinatorial reasoning are concentrated in fine binding, and correct or incorrect binding can be automatically determined under certain task designs. Focusing on "what to verify", different works respectively verify the final answer, the intermediate structure of reasoning and the cross-perspective consistency of the answer.

## [54:0] (gtx)
- ZH: CR³ [4] 是结果级验证的代表，其贡献是把组合推理重新设计成答案可自动判分的任务：构造三个图文匹配任务（TG-VCR、VG-TCR、CITM），回答正误由确定性规则判定，奖励由答案正确与推理顺序两个二元分量构成：
- EN: CR³ [4] is a representative of result-level verification. Its contribution is to redesign combinatorial reasoning into a task where answers can be automatically judged: three image-text matching tasks (TG-VCR, VG-TCR, CITM) are constructed. The correctness of the answer is determined by deterministic rules, and the reward is composed of two binary components: the correct answer and the order of reasoning:

## [56:0] (gtx)
- ZH: 其中答案分量在输出与标准答案完全一致时取 1，顺序分量在输出严格遵循“先以 <think> 给出推理、再以 <answer> 给出答案”的格式时取 1（
- EN: The answer component takes 1 when the output is completely consistent with the standard answer, and the sequence component takes 1 when the output strictly follows the format of "first give the reasoning with <think>, and then give the answer with <answer>" (

## [56:1] (gtx)
- ZH: ），强制显式推理生成。无需外部标注，但规则判定只是前提，真正决定信号质量的是数据工序：通过语义与视觉双重筛选构造高难度负样本（18.5 万→1.89 万），使二元奖励在“整体相似、细节绑定出错”的样本上保持梯度。论文报告 Qwen2.5-VL-7B 与 InternVL3-8B 在三个组合基准上较原始基线平均提升 9.65 个百分点（按表 3 实算；论文正文概括为约 10 点），且无 SFT 常见的领域外退化。
- EN: ), forcing explicit inference generation. There is no need for external annotation, but rule determination is only a prerequisite. What really determines the quality of the signal is the data process: constructing highly difficult negative samples (185,000 → 18,900) through semantic and visual dual screening, so that the binary reward maintains a gradient on samples with "overall similarity and error in detail binding". The paper reports that Qwen2.5-VL-7B and InternVL3-8B improve on the three combined benchmarks by an average of 9.65 percentage points compared to the original baseline (actual calculation according to Table 3; the main text of the paper summarizes it as about 10 points), and there is no out-of-field degradation common in SFT.

## [57:0] (gtx)
- ZH: SpatialThinker [13] 探索了结构级奖励，将验证对象扩展到推理的中间产物：模型按固定模板输出“观察→场景图→推理→答案”，奖励由格式、计数、准确率、空间四个分量经字典序门控组合：
- EN: SpatialThinker [13] explores structure-level rewards and extends the verification object to the intermediate products of reasoning: the model outputs "observation→scene graph→inference→answer" according to a fixed template, and the reward is composed of four components: format, count, accuracy, and space through lexicographic gating:

## [59:0] (gtx)
- ZH: 其中格式分量是硬门槛，空间奖励仅在答案正确时生效，防止模型为刷结构分而牺牲最终答案。论文报告 7B 模型在 14 个基准上平均超越 GPT-4o 4.7 个百分点，但 STVQA-7K 基于 Visual Genome 人工标注构建，框标注质量直接决定空间分量的可靠性。
- EN: The format component is a hard threshold, and the space reward only takes effect when the answer is correct, preventing the model from sacrificing the final answer for structural points. The paper reports that the 7B model surpasses GPT-4o by an average of 4.7 percentage points on 14 benchmarks, but STVQA-7K is built based on Visual Genome manual annotation, and the quality of box annotation directly determines the reliability of the spatial component.

## [60:0] (gtx)
- ZH: SVQA-R1 [14] 代表了对“跨视角一致性”的验证，将图像镜像翻转并用 GPT-4o 生成翻转后逻辑一致的问答对，要求模型对原图与翻转图给出语义一致的答案；奖励为格式与语义两个分量加权（
- EN: SVQA-R1 [14] represents the verification of "cross-view consistency". It flips the image mirror and uses GPT-4o to generate logically consistent question and answer pairs after the flip. The model is required to give semantically consistent answers to the original image and the flipped image; the reward is weighted by the two components of format and semantics (

## [60:1] (gtx)
- ZH: ）。论文报告 3B 模型在 Q-Spatial++ 上较 SFT(CoT) 基线提升超 30 个百分点（27.72→58.42），验证范围限于水平镜像翻转下的空间问答。
- EN: ). The paper reports that the 3B model improves by more than 30 percentage points (27.72 → 58.42) on Q-Spatial++ compared with the SFT (CoT) baseline. The verification scope is limited to spatial question and answer under horizontal mirror flipping.

## [61:0] (gtx)
- ZH: 节内小结：三篇工作的验证对象覆盖答案、中间结构与跨视角一致性，共同约束是“正确性必须可定义”：组合推理没有唯一标准答案，验证器只能验证可结构化的侧面。而绑定是否正确不在答案里，而在模型与视觉证据的关系中；对这一层面的优化，视觉对齐奖励提供了另一条独立路径（见 3.2）。
- EN: Section summary: The verification objects of the three works cover answers, intermediate structures and cross-view consistency. The common constraint is "correctness must be definable": there is no unique standard answer for combinatorial reasoning, and the verifier can only verify the structured aspects. Whether the binding is correct does not lie in the answer, but in the relationship between the model and the visual evidence; for optimization at this level, the visual alignment reward provides another independent path (see 3.2).

## [62:0] (gtx)
- ZH: 3.2视觉对齐奖励（Grounded）
- EN: 3.2 Visual alignment reward (Grounded)

## [63:0] (gtx)
- ZH: 答对不等于看图：仅凭文本统计规律或虚假相关，模型也能蒙对组合任务，而结果验证对此无能为力。视觉对齐奖励把信号源从“回答的外部判据”换成“回答与视觉证据的关系”，让“是否真的看了图、看了正确的区域”成为可优化信号。不同工作沿“对齐对象”（证据区域、思维链内嵌、物体级、显著性分布）与“监督强度”（少量问答对到零标注）两个维度展开探索。
- EN: Answering correctly is not the same as looking at the picture: the model can also mislead the combination task based only on text statistical rules or false correlations, but the result verification cannot do anything about it. The visual alignment reward changes the signal source from "external criteria of the answer" to "the relationship between the answer and visual evidence", making "whether you really looked at the picture and the correct area" an optimizable signal. Different works are explored along the two dimensions of "aligning objects" (evidence area, thought chain embedding, object level, saliency distribution) and "supervision intensity" (a small number of question and answer pairs to zero annotation).

## [64:0] (gtx)
- ZH: Ground-R1 [15] 是这一方向的起点，证明 RL 下不依赖外部框标注（训练奖励仅含格式与答案验证，证据框由模型自生成）即可驱动模型学会定位证据。两阶段 rollout 中，模型先输出证据框坐标、再基于裁剪出的局部图像作答，对齐信号来自答案对局部图像的依赖，其奖励本身仍是格式与答案验证。论文诊断出标准 GRPO 的全局归一化偏袒大而显著的证据区域，小证据获得持续负优势，故提出尺度相对策略优化（SRPO），按区域面积分箱做桶内/桶间归一化，较标准 GRPO 在 V* 与 HR-4K 上分别提升 2.1 与 1.2 个百分点。SRPO 属归一化机制而非奖励信号设计，却印证了主线上的一个必要条件：对齐奖励要真正生效，不同尺度的证据必须在优势计算中公平竞争，否则信号将被大区域垄断。
- EN: Ground-R1 [15] is the starting point in this direction, proving that RL can drive the model to learn to locate evidence without relying on external box annotations (the training reward only includes format and answer verification, and the evidence box is self-generated by the model). In the two-stage rollout, the model first outputs the coordinates of the evidence frame and then answers based on the cropped partial image. The alignment signal comes from the answer's dependence on the partial image, and the reward itself is still format and answer verification. The paper diagnoses that the global normalization of standard GRPO favors large and significant evidence areas, and small evidence obtains a continuous negative advantage. Therefore, scale relative strategy optimization (SRPO) is proposed, which performs intra-bucket/inter-bucket normalization by dividing bins by area area. Compared with standard GRPO, V* and HR-4K are improved by 2.1 and 1.2 percentage points respectively. SRPO is a normalization mechanism rather than a reward signal design, but it confirms a necessary condition on the main line: for alignment rewards to be truly effective, evidence of different scales must compete fairly in the advantage calculation, otherwise the signal will be monopolized by a large area.

## [65:0] (gtx)
- ZH: GRIT [16] 在监督强度上进一步压缩：包围框坐标直接内嵌进思维链（<think>→<rethink>→<answer>），训练仅用 20 个图文问答三元组即触发基座模型的 grounded 推理能力。消融还揭示对齐信号须与推理需求挂钩：加入计数奖励后 grounding 质量明显提升（GIoU 0.349→0.387）。但 bbox 终究只是“看哪儿”的粗略代理，奖励不约束框本身的质量。
- EN: GRIT [16] further compresses the supervision intensity: the bounding box coordinates are directly embedded in the thinking chain (<think>→<rethink>→<answer>), and the training only uses 20 image-text question and answer triples to trigger the grounded reasoning ability of the base model. Ablation also reveals that the alignment signal must be linked to inference requirements: the grounding quality is significantly improved after adding counting rewards (GIoU 0.349→0.387). But bbox is ultimately just a rough proxy for "where to look", and the reward does not constrain the quality of the box itself.

## [66:0] (gtx)
- ZH: POLIA [17] 把对齐粒度细化到物体级，是本节中奖励公式最完整的设计：答案级外在优势 
- EN: POLIA [17] refines the alignment granularity to the object level, which is the most complete design of the reward formula in this section: answer-level external advantages

## [66:1] (gtx)
- ZH:  沿用 GRPO 的组内归一化；物体级内在优势 
- EN: Inherit GRPO's intra-group normalization; object-level inherent advantages

## [66:2] (gtx)
- ZH:  先在答案引用的物体集合上按置信度修正奖励，再在组内归一化：
- EN: First correct the reward according to the confidence level on the set of objects referenced by the answer, and then normalize it within the group:

## [68:0] (gtx)
- ZH: 其中 
- EN: in

## [68:1] (gtx)
- ZH:  是预测框与真实物体匹配的置信度（IoU 与归一化距离加权）。看错地方的轨迹即使答对，其物体级优势也会被置信度压低，从而在奖励层面区分“答案对但看错地方”与“答案对且看对地方”。在 VSR 上 POLIA 将基线 GRPO 的 59.0% 提升至 81.3%，Aint 计算仅耗时 0.002 s，而 Rollout 阶段占训练总时间的 97.24%（基于 POLIA-3B 实测），开销可忽略。同方向的 SAYO [18] 以区域级视觉注意力作为奖励信号，把对齐对象从显式框推广到注意力分布。
- EN: is the confidence that the predicted box matches the real object (IoU weighted with normalized distance). Even if the trajectory of the wrong answer is correct, its object-level advantage will be suppressed by the confidence level, thus distinguishing "the answer is right but the answer is wrong" and "the answer is correct and the answer is right" at the reward level. On VSR, POLIA improves the baseline GRPO from 59.0% to 81.3%. The Aint calculation only takes 0.002 s, while the Rollout stage accounts for 97.24% of the total training time (based on POLIA-3B actual measurement), and the overhead is negligible. Same-direction SAYO [18] uses regional-level visual attention as a reward signal to generalize aligned objects from explicit boxes to attention distributions.

## [69:0] (gtx)
- ZH: 节内小结：该方向的对齐对象覆盖证据区域、思维链内嵌、物体级与显著性分布，监督需求较低：Ground-R1 不依赖外部框标注，GRIT 仅需 20 个问答三元组，POLIA 复用数据集物体标注。但上述工作多在通用/高分辨率 LVLM 与接地、空间问答基准上验证，显式组合基准（如 MMVP、Winoground、SugarCrepe）上的覆盖仍然不足；对齐奖励衡量“是否看对”，而组合推理还要求“是否合理推理”，后者由推理过程优化方向（3.3）处理。
- EN: Summary of the section: Alignment objects in this direction cover evidence areas, thought chain embeddings, object-level and saliency distributions, and have low supervision requirements: Ground-R1 does not rely on external box annotation, GRIT only requires 20 question and answer triples, and POLIA reuses data set object annotations. However, the above work is mostly verified on general/high-resolution LVLM and grounded and spatial question and answer benchmarks, and the coverage on explicit combination benchmarks (such as MMVP, Winoground, SugarCrepe) is still insufficient; alignment rewards measure "whether you see it right", while combination reasoning also requires "whether it is reasonable to reason", the latter is handled by the inference process optimization direction (3.3).

## [70:0] (gtx)
- ZH: 3.3推理过程优化（Process）
- EN: 3.3 Inference process optimization (Process)

## [71:0] (gtx)
- ZH: 前两类的信号分别作用于“是否正确”与“是否看对”，第三类则把优化信号作用于推理过程本身。理论上，这类方法与结果验证存在深层联系：GRPO 在 token 级设定下与 PRM-aware 目标数学等价，组内共享前缀天然构成“过程步骤” [11]，即结果奖励本就在隐式地做过程级信用分配，本节方法可视为将这一隐式机制显式化。第一步在多模态侧已经出现：VisualPRM [12] 训练 8B 过程奖励模型（学习式验证器，将验证对象从最终答案迁移到推理步骤），在 7 个多模态推理基准上带来 3.7 ~ 8.9 个点提升（3.7~8.4 见摘要；8.9 为 InternVL2.5-26B），但其步骤定义纯文本、无视觉锚定，不覆盖组合绑定（本文观察）。第二步是把证据框等视觉结构锚定进步骤，这正是 H-GRPO 的探索。三篇工作的显式化程度依次递进：VisualPRM 验证步骤（事后打分）、Self-Questioning 约束结构（强制分解）、H-GRPO 建模路径（步骤逐点进入目标函数）。
- EN: The first two types of signals act on "whether it is correct" and "whether it is correct" respectively, while the third type uses optimization signals to act on the reasoning process itself. Theoretically, this type of method has a deep connection with result verification: GRPO is mathematically equivalent to PRM-aware targets under token-level settings, and the shared prefixes within the group naturally constitute "process steps" [11], that is, the result rewards are implicitly allocated process-level credit. The method in this section can be regarded as making this implicit mechanism explicit. The first step has already appeared on the multimodal side: VisualPRM [12] trains the 8B process reward model (a learning verifier that migrates the verification object from the final answer to the inference step), which brings 3.7~8.9 points improvement on 7 multimodal reasoning benchmarks (3.7~8.4 see abstract; 8.9 is InternVL2.5-26B), but its step definition is plain text, has no visual anchoring, and does not cover combination binding (observed in this article). The second step is to anchor visual structures such as evidence boxes into the step, which is what H-GRPO explores. The degree of explicitness of the three works increases in sequence: VisualPRM verification steps (post-scoring), Self-Questioning constraint structure (forced decomposition), and H-GRPO modeling path (steps into the objective function point by point).

## [72:0] (gtx)
- ZH: Self-Questioning VLM [19] 是显式化的最小实现，设计精简到只剩一个格式约束：模型必须按“子问题/子答案序列 + 最终答案”输出，奖励为二元形式：
- EN: Self-Questioning VLM [19] is an explicit minimal implementation, and the design is reduced to only one format constraint: the model must output according to "sub-question/sub-answer sequence + final answer", and the reward is in binary form:

## [74:0] (gtx)
- ZH: 子问题质量故意不检查。正是这种“不检查”逼出了分解行为：模型必须自己探索该问什么，A-OKVQA 上基座模型仅 46.8%，标准 RLVR 对照达 51.6%，而本方法达 52.2%；对照模型与本方法的唯一差别就是格式要求，51.6% 到 52.2% 的额外增益可归因于子问题格式约束（46.8% 到 51.6% 的主增益来自 RL 本身）。该“格式+答案”二元奖励与 3.1 节 CR³ 同源，仅将格式约束细化为显式子问题分解；其过程信号限于结构存在性，模型可能用无意义的问题应付格式。
- EN: Sub-question quality is intentionally not checked. It is this "no checking" that forces the decomposition behavior: the model must explore on its own what to ask, the base model only achieves 46.8% on A-OKVQA, the standard RLVR control reaches 51.6%, and this method reaches 52.2%; the only difference between the control model and this method is the format requirement, 51.6% to 52.2% of the additional gain can be attributed to the sub-problem format constraints (46.8% to 51.6% of the main gain comes from RL itself). This "format + answer" binary reward is homologous to CR³ in Section 3.1, which only refines the format constraints into explicit sub-problem decomposition; its process signal is limited to the structure existence, and the model may cope with the format with meaningless questions.

## [75:0] (gtx)
- ZH: H-GRPO [20] 则将过程奖励细化到步骤质量，并显式耦合视觉证据：把推理结构化为“（子问题，子答案，证据框）”三元组序列 
- EN: H-GRPO [20] refines the process reward to step quality and explicitly couples visual evidence: structuring the reasoning into a sequence of "(sub-question, sub-answer, evidence box)" triples

## [75:1] (gtx)
- ZH: ，预测与参考三元组经匈牙利二分图匹配，相似度矩阵综合证据框兼容性、子问题/子答案语义相似度与框 IoU 四个分量：
- EN: , the prediction and reference triples are matched through the Hungarian bipartite graph, and the similarity matrix integrates the four components of evidence box compatibility, sub-question/sub-answer semantic similarity and box IoU:

## [77:0] (gtx)
- ZH: 其中 
- EN: in

## [77:3] (gtx)
- ZH:  分别衡量证据框兼容性、子问题与子答案的语义相似度，IoU 为空间重叠。总奖励为格式奖励与“答案奖励 × 匈牙利奖励”之和：
- EN: The evidence frame compatibility, semantic similarity of sub-questions and sub-answers are measured respectively, and IoU is the spatial overlap. The total reward is the sum of the format reward and "answer reward × Hungarian reward":

## [79:0] (gtx)
- ZH: 门控关系保证：光答对但中间步骤与证据 grounding 不到位，奖励即被门控，从而抑制“忽略图像仅凭文本脑补”的捷径。数学上，GRPO 是 H-GRPO 对角匹配的特例，在方法层面印证了“结果验证与过程验证同源”的结论。小模型受益最大（SmolVLM-2.2B 在 A-OKVQA 达 73.4%），但参考推理链的质量决定奖励上限（参考链经人工验证）。
- EN: Gating relationship guarantee: if the answer is correct but the intermediate steps and evidence grounding are not in place, the reward will be gated, thereby inhibiting the shortcut of "ignoring the image and only relying on the text to make up for it". Mathematically, GRPO is a special case of H-GRPO diagonal matching, which confirms the conclusion that "result verification and process verification have the same origin" at the method level. Small models benefit the most (SmolVLM-2.2B reaches 73.4% in A-OKVQA), but the quality of the reference inference chain determines the upper limit of the reward (the reference chain is manually verified).

## [80:0] (gtx)
- ZH: 节内小结：三篇工作的过程信号构造路径各异，从最简的格式约束到结合参考链匹配与视觉证据的结构化奖励。过程信号多为模型自生成，监督需求是三类中最低的；但除 H-GRPO 的证据框约束外，过程信号普遍不含视觉语义结构，“过程”与“视觉”如何在奖励层面深度融合，仍是开放问题（详见第 4 节）。
- EN: Section summary: The process signal construction paths of the three works are different, from the simplest format constraints to structured rewards that combine reference chain matching and visual evidence. Process signals are mostly self-generated by the model, and the supervision requirement is the lowest among the three categories; however, except for the evidence frame constraints of H-GRPO, process signals generally do not contain visual semantic structures. How to deeply integrate "process" and "visual" at the reward level is still an open question (see Section 4 for details).

## [81:0] (gtx)
- ZH: 3.4 三类方法对比分析
- EN: 3.4 Comparative analysis of three types of methods

## [82:0] (gtx)
- ZH: 将三个方向放在一起看，三类方法并非离散类别，也不是彼此替代的技术路线，而是同一研究问题下的互补探索，分别从“是否正确”“是否看对”“是否合理推理”三个层面切入，构成奖励信号设计空间中的不同刻度（如图 1 所示）。从提出时间看，三类方法并未呈现严格的先后递进：结果验证与视觉对齐方向的代表工作自 2025 年中期至 2026 年间相继出现，过程优化方向以 VisualPRM [12]（2025 年 3 月）为过程建模先声、Self-Questioning [19] 与 H-GRPO [20] 集中于 2026 年中，三个方向的活跃期相互重叠。此外，直接以组合推理为优化对象的研究目前仍属少数，多数方法以显式组合基准、空间推理或通用 VQA 基准为评测载体，本文按奖励设计的增量贡献（见 3 节开头）而非评测载体归类，各方法的组合参考价值与评测局限详见 4.3 节。“演进”指设计空间的维度扩展而非时间上的先后淘汰。表 2 汇总类别层面的对比；表 3 与表 4 分别给出逐方法的奖励粒度刻度与实验设置。即便在方法层面，三个方向也存在互相借鉴：H-GRPO 的“答案奖励×匈牙利门控”融合了结果验证与过程匹配，POLIA [17] 的物体级优势同样依赖答案级判据的引导，类别不是封闭的抽屉。
- EN: Looking at the three directions together, the three types of methods are not discrete categories, nor are they technical routes that replace each other, but are complementary explorations under the same research problem, starting from the three levels of "whether it is correct", "whether it is correct" and "whether it is reasonable reasoning", constituting different scales in the reward signal design space (as shown in Figure 1). Judging from the time of their introduction, the three types of methods do not show a strict progression: representative work in the direction of result verification and visual alignment appeared one after another from mid-2025 to 2026. The process optimization direction started with VisualPRM [12] (March 2025) as the precursor to process modeling, Self-Questioning [19] and H-GRPO [20] concentrated in mid-2026. The active periods of the three directions overlap with each other. In addition, there are still a few studies that directly target combinatorial reasoning for optimization. Most methods use explicit combination benchmarks, spatial reasoning or general VQA benchmarks as evaluation carriers. This article is classified according to the incremental contribution of reward design (see the beginning of Section 3) rather than the evaluation carrier. The combined reference value and evaluation limitations of each method are detailed in Section 4.3. "Evolution" refers to the dimensional expansion of the design space rather than the sequential elimination in time. Table 2 summarizes the comparison at the category level; Tables 3 and 4 provide the method-by-method reward granularity scale and experimental settings respectively. Even at the method level, the three directions can learn from each other: H-GRPO's "Answer Reward × Hungarian Gating" integrates result verification and process matching, and the object-level advantages of POLIA [17] also rely on the guidance of answer-level criteria, and categories are not closed drawers.

## [83:0] (gtx)
- ZH: 表 2：方法分类对比表
- EN: Table 2: Method classification comparison table

## [84:0] (gtx)
- ZH: 维度
- EN: Dimensions

## [85:0] (gtx)
- ZH: 验证器奖励
- EN: Validator rewards

## [86:0] (gtx)
- ZH: 视觉对齐奖励
- EN: visual alignment bonus

## [87:0] (gtx)
- ZH: 推理过程优化
- EN: Reasoning process optimization

## [88:0] (gtx)
- ZH: 奖励信号来源
- EN: Reward signal source

## [89:0] (gtx)
- ZH: 结果验证（规则/图结构/视图一致性）
- EN: Result validation (rules/graph structure/view consistency)

## [90:0] (gtx)
- ZH: 回答-视觉语义结构对齐度
- EN: Answer-Visual semantic structure alignment

## [91:0] (gtx)
- ZH: 过程结构/步骤信用分配
- EN: Process Structure/Step Credit Assignment

## [92:0] (gtx)
- ZH: 奖励粒度（典型刻度）
- EN: Reward granularity (typical scale)

## [93:0] (gtx)
- ZH: 答案级 → 结构/一致性级
- EN: Answer Level → Structure/Consistency Level

## [94:0] (gtx)
- ZH: 区域级 → 物体级 → 显著性级
- EN: Area level → object level → significance level

## [95:0] (gtx)
- ZH: 子问题级 → 步骤+证据级
- EN: Sub-question level → step+evidence level

## [96:0] (gtx)
- ZH: 是否触及组合绑定
- EN: Whether to touch the combination binding

## [97:0] (gtx)
- ZH: 间接（验证绑定结果）
- EN: Indirect (verify binding results)

## [98:0] (gtx)
- ZH: 直接（绑定到视觉证据）
- EN: Direct (tied to visual evidence)

## [99:0] (gtx)
- ZH: 间接（过程正确性）
- EN: Indirect (procedural correctness)

## [100:0] (gtx)
- ZH: 代表工作
- EN: representative work

## [104:0] (gtx)
- ZH: 主要短板
- EN: Main shortcomings

## [105:0] (gtx)
- ZH: 正确性难定义
- EN: Correctness is difficult to define

## [106:0] (gtx)
- ZH: 评测未显式覆盖组合
- EN: Review does not explicitly cover combinations

## [107:0] (gtx)
- ZH: 过程信号多为纯文本
- EN: Process signals are mostly plain text

## [108:0] (gtx)
- ZH: 表 3：代表方法的设计对比（奖励粒度、增量贡献层、信号机制与监督需求）
- EN: Table 3: Design comparison of representative methods (reward granularity, incremental contribution layer, signaling mechanism and supervision requirements)

## [109:0] (gtx)
- ZH: 方法
- EN: method

## [110:0] (gtx)
- ZH: 奖励粒度
- EN: Reward granularity

## [111:0] (gtx)
- ZH: 信号机制
- EN: signaling mechanism

## [112:0] (gtx)
- ZH: 监督需求
- EN: Supervision needs

## [113:0] (gtx)
- ZH: 增量贡献层
- EN: incremental contribution layer

## [115:0] (gtx)
- ZH: 答案级
- EN: answer level

## [116:0] (gtx)
- ZH: 二元规则验证器
- EN: Binary rule validator

## [117:0] (gtx)
- ZH: 无
- EN: none

## [118:0] (gtx)
- ZH: 判据
- EN: criterion

## [120:0] (gtx)
- ZH: 场景图结构级
- EN: scene graph structure level

## [121:0] (gtx)
- ZH: 字典序门控多分量奖励
- EN: Lexicographically gated multi-component rewards

## [122:0] (gtx)
- ZH: 高（STVQA-7K 基于人工场景图标注合成）
- EN: High (STVQA-7K based on artificial scene map annotation synthesis)

## [123:0] (gtx)
- ZH: 判据
- EN: criterion

## [125:0] (gtx)
- ZH: 答案一致性级
- EN: Answer consistency level

## [126:0] (gtx)
- ZH: 跨视角一致性惩罚
- EN: Cross-view consistency penalty

## [127:0] (gtx)
- ZH: 无（自监督）
- EN: None (self-supervised)

## [128:0] (gtx)
- ZH: 判据
- EN: criterion

## [130:0] (gtx)
- ZH: 证据区域级
- EN: evidence area level

## [131:0] (gtx)
- ZH: 两阶段格式+答案奖励
- EN: Two-stage format + answer bonus

## [132:0] (gtx)
- ZH: 低（仅格式，无框标注）
- EN: Low (formatting only, no boxed annotations)

## [133:0] (gtx)
- ZH: 信号源
- EN: signal source

## [135:0] (gtx)
- ZH: 区域级（思维链内嵌）
- EN: Regional level (embedded in the thinking chain)

## [136:0] (gtx)
- ZH: 格式+计数奖励
- EN: Format + Count Bonus

## [137:0] (gtx)
- ZH: 极低（20 个问答三元组）
- EN: Very low (20 Q&A triples)

## [138:0] (gtx)
- ZH: 信号源
- EN: signal source

## [140:0] (gtx)
- ZH: 物体级
- EN: object level

## [141:0] (mymemory)
- ZH: 置信度修正的物体级内在优势
- EN: Intrinsic Benefits of Confidence Correction at the Object Level

## [142:0] (mymemory)
- ZH: 低（利用数据集物体标注）
- EN: Low (using dataset object annotation)

## [143:0] (mymemory)
- ZH: 信号源
- EN: Signal

## [145:0] (mymemory)
- ZH: 子问题结构级
- EN: Subquestion Structure Level

## [146:0] (mymemory)
- ZH: 二元格式+正确性奖励
- EN: Binary Format + Correctness Reward

## [147:0] (mymemory)
- ZH: 无
- EN: None

## [148:0] (mymemory)
- ZH: 对象
- EN: Objects

## [150:0] (mymemory)
- ZH: 推理步骤+证据级
- EN: Reasoning Steps + Evidence Level

## [151:0] (mymemory)
- ZH: 匈牙利门控过程奖励
- EN: Hungarian Gated Process Reward

## [152:0] (mymemory)
- ZH: 无
- EN: None

## [153:0] (mymemory)
- ZH: 对象
- EN: Objects

## [154:0] (mymemory)
- ZH: 表 4：代表方法的实验设置与结果对比（基座模型、评测基准、关键数据/设计与代表性结果）
- EN: Table 4: Comparison of experimental settings and results of representative methods (pedestal model, benchmark, key data/design and representative results)

## [155:0] (mymemory)
- ZH: 方法
- EN: THE METHOD

## [156:0] (mymemory)
- ZH: 基座模型
- EN: Pedestal model

## [157:0] (mymemory)
- ZH: 评测基准
- EN: Benchmark

## [158:0] (mymemory)
- ZH: 关键数据/设计
- EN: Key Data/Design

## [159:0] (mymemory)
- ZH: 代表性结果
- EN: Representative results

## [163:0] (mymemory)
- ZH: 语义+视觉双重筛选：18.5 万→1.89 万难负样本
- EN: Semantic + visual double screening: 185,000→ 18,900 hard negative samples

## [164:0] (mymemory)
- ZH: 较原始基线平均超 9 点，较 SFT 超 5 点
- EN: 9 points above original baseline average and 5 points above SFT

## [167:0] (mymemory)
- ZH: 14 基准
- EN: 14 Benchmark

## [168:0] (mymemory)
- ZH: 匈牙利匹配 + CIoU 稠密梯度
- EN: Hungarian Match + CIoU Dense Gradient

## [169:0] (mymemory)
- ZH: 14 基准平均超 GPT-4o 4.7 个百分点
- EN: 14 Benchmark average exceeds GPT-4o by 4.7 percentage points

## [173:0] (mymemory)
- ZH: 镜像翻转问答对
- EN: Mirror Flip Q&A Correct

## [174:0] (mymemory)
- ZH: 较 SFT(CoT) 提升超 30 个百分点
- EN: Over 30 percentage points higher than SFT (CoT)

## [177:0] (mymemory)
- ZH: 通用 LVLM + 高分辨率 + 接地
- EN: Universal LVLM + High Resolution + Ground

## [178:0] (mymemory)
- ZH: 两阶段 rollout + 尺度分箱归一化
- EN: Two-stage rollout + scale binning normalization

## [179:0] (mymemory)
- ZH: 较标准 GRPO：V* +2.1、HR-4K +1.2 个百分点
- EN: More standard GRPO: V * +2.1, HR-4K +1.2 percentage points

## [182:0] (mymemory)
- ZH: VSR/TallyQA/GQA/MathVista/MME/OVDEval（六数据集七测试集）
- EN: VSR/TallyQA/GQA/MathVista/Mme/OVDEval (six data sets, seven test sets)

## [183:0] (mymemory)
- ZH: bbox 坐标内嵌思维链（仅 20 个问答三元组）
- EN: bbox coordinates embedded thought chains (20 Q&A triples only)

## [184:0] (mymemory)
- ZH: 接地 IoU 0.349→0.387
- EN: Ground IoU 0.349→ 0.387

## [187:0] (mymemory)
- ZH: VSR 等 7 基准
- EN: VSR et al. 7 benchmarks

## [188:0] (mymemory)
- ZH: 双层优势 
- EN: Two-Layer Advantage

## [189:0] (mymemory)
- ZH: GRPO 基线 59.0→81.3
- EN: GRPO Baseline 59.0→ 81.3

## [193:0] (mymemory)
- ZH: 子问题质量刻意不检查
- EN: Sub-question quality deliberately not checked

## [194:0] (mymemory)
- ZH: 52.2（基座 46.8 / 标准 RL 51.6）
- EN: 52.2 (Base 46.8/Standard RL 51.6)

## [197:0] (mymemory)
- ZH: A-OKVQA/Visual7W 与 OOD 基准（MMMU/RealWorldQA/RoboSpatial/MMStar）
- EN: A-OKVQA/Visual7W vs. OOD Benchmark (MMMU/RealWorldQA/RoboSpatial/MMStar)

## [198:0] (mymemory)
- ZH: 三元组序列（子问题/子答案/证据框）匹配
- EN: Triple sequence (subquestion/subanswer/evidence box) matching

## [200:0] (mymemory)
- ZH: 注：表中数值均为论文报告值；“提升”“超出”均指绝对百分点（含 SVQA-R1 的 +30 点）；GIoU 为接地 IoU。各方法基座、训练数据与评测协议不同，数值不可直接横向比较（见 4.3 节）。
- EN: Note: The values in the table are the reported values of the thesis; "promotion" and "over" refer to absolute percentage points (+30 points with SVQA-R1); GIoU is grounded IoU. Different method bases and training data are different from the evaluation protocol, and the values cannot be directly compared horizontally (see Section 4.3).

## [202:0] (mymemory)
- ZH: 图 1：奖励信号设计空间演化示意图
- EN: Figure 1: Schematic diagram of the evolution of the reward signal design space

## [203:0] (mymemory)
- ZH: 4. 探讨
- EN: 4. Explore

## [204:0] (mymemory)
- ZH: 4.1 奖励信号连续谱
- EN: 4.1 Continuous Spectrum of Reward Signals

## [205:0] (mymemory)
- ZH: 3.4 节的三分法在描述上是方便的，但表 3 的粒度刻度揭示了一个更本质的事实：三类方法并非离散的类别，而是同一奖励设计空间中的连续谱。这一判断有数学层面的支撑：如 2.2 节所述，在 token 级策略梯度与单次更新的设定下，标准 GRPO 与 PRM-aware 目标等价 [11]，结果奖励本就在隐式地做过程级信用分配。方法层面同样呈现连续的混合形态：H-GRPO 同时包含结果验证与过程匹配两种信号，POLIA 的外在优势与内在优势同处一个损失函数，SVQA-R1 的一致性惩罚则介于验证器与自监督对齐之间。所谓“演进”并非时间上的先后淘汰，而是奖励设计空间的维度扩展：推理展开维度上自答案级（CR³）经结构级（SpatialThinker）延伸至步骤级（H-GRPO），视觉锚定维度上自区域级（Ground-R1）细化至物体级（POLIA）；两个维度相互独立、不可直接比较，各刻度至今仍在并行发展。
- EN: Section 3.4 trisections are conveniently described, but the granularity scale of Table 3 reveals a more essential fact: the three types of methods are not discrete categories, but sequential spectra in the same reward design space. This judgment is supported by the mathematical level: as described in Section 2.2, under the setting of the token-level strategy gradient and a single update, the standard GRPO is equivalent to the PRM-aware target [11], and the resultant reward is implicitly done at the process-level credit allocation. At the method level, there is also a continuous hybrid pattern: H-GRPO contains both result validation and process matching signals, Polia's external and internal advantages coexist as a loss function, and SVQA-R1's consistency penalty is between the validator and self-supervised alignment. The so-called "evolution" is not a sequential elimination in time, but a dimensional extension of the reward design space: the inference expansion dimension extends from the answer level (CR ³) through the structural level (SpatialThinker) to the step level (H-GRPO), and the visual anchoring dimension is refined from the regional level (Ground-R1) to the object level (Polia); the two dimensions are independent of each other and cannot be directly compared, and each scale is still developing in parallel.

## [206:0] (mymemory)
- ZH: 4.2 组合正确性正变得可验证
- EN: 4.2 Combination correctness is becoming verifiable

## [207:0] (mymemory)
- ZH: 本文 3.1 的验证器方法都建立在“正确性可定义”的前提上，而这一前提正被评测基准的构建方式不断加固。MM-CondChain [21] 展示了组合推理正确性程序化验证的完整范式：用可执行程序把多层组合条件构造出来并机械验证；其 975 个评估样本（每样本含 True-path/False-path 一对）由程序化管线生成并机械验证，评分全可复现，最强模型也仅得 53.33 分（Path F1），说明深度组合推理的可验证评测不仅是可能的，且当前模型远未饱和。但程序化验证的是逻辑层的一致性，自然图像域的感知事实仍依赖 MLLM 提取；当 MLLM 感知能力不足时，提取出的“视觉事实”本身带噪声，以它为输入的验证器只会放大噪声。这恰好划定了可验证奖励的适用半径：当正确性可分解为离散逻辑结构时，奖励可以完全规则化；当绑定依赖开放感知判断时，只能回到人工标注或自监督的近似。
- EN: The validator methods in 3.1 are built on the premise that correctness can be defined, and this premise is being reinforced by the way the benchmarks are built. MM-CondChain [21] demonstrates the complete paradigm of programmatic verification of the correctness of combinatorial reasoning: multi-layered combinatorial conditions are constructed and mechanically verified using an executable program; its 975 evaluation samples (each containing a True-path/False-path pair) are generated by a programmatic pipeline and mechanically verified, the scores are all reproducible, and the strongest model scores only 53.33 points (Path F1), indicating that verifiable evaluation of deep combinatorial reasoning is not only possible, but that the current model is far from saturated. However, the consistency of the logic layer is verified programmatically, and the perceived facts in the natural image domain still rely on MLLM extraction; when the perception ability of MLLM is insufficient, the extracted "visual facts" themselves carry noise, and the verifier with it as input will only amplify the noise. This precisely delineates the applicable radius of the verifiable reward: when correctness can be decomposed into discrete logical structures, the reward can be fully regularized; when binding relies on open perception judgments, it can only return to manual labeling or self-supervised approximations.

## [208:0] (mymemory)
- ZH: 4.3 基准碎片化与 Swap 试金石
- EN: 4.3 Benchmark Fragmentation and Swap Touchstone

## [209:0] (mymemory)
- ZH: 三类方法在评测上各行其是：CR³ 报告 MMVP、Winoground、Cola，SpatialThinker 横跨 14 个基准，SVQA-R1 聚焦 Q-Spatial++，Ground-R1 在通用/高分辨率与接地基准上验证，POLIA 在 VSR 等 7 个基准上验证，H-GRPO 则依赖 A-OKVQA/Visual7W 与 OOD 基准，任何两篇方法论文的结果都难以直接横向比较。现有共识恰好指向一个可作统一试金石的子任务：SugarCrepe 的 Swap，即交换两个同类别概念而不引入新概念，是最纯粹的绑定测试 [3]。Swap 不依赖场景图标注、判别性强且与 RL 训练接口简单（规则可判定），因此建议直接采用 SugarCrepe 官方 Swap 子集作为统一附加基准。
- EN: The three types of methods are evaluated separately: CR ³ reports MMVP, Winoground, Cola, SpatialThinker spanning 14 benchmarks, SVQA-R1 focuses Q-Spatial + +, Ground-R1 is validated on general/high resolution and grounding benchmarks, Polia is validated on 7 benchmarks such as VSR, H-GRPO relies on A-OKVQA/Visual7W and OOD benchmarks, and the results of any two method papers are difficult to directly compare horizontally. The existing consensus points to a subtask that can serve as a unifying touchstone: SugarCrepe's Swap, which exchanges two concepts of the same category without introducing a new one, is the purest binding test [3]. Swap does not rely on scene icons, is highly discriminative, and has a simple training interface with RL (rules can be determined). Therefore, it is recommended to directly use the official Swap subset of SugarCrepe as a unified additional benchmark.

## [210:0] (mymemory)
- ZH: 4.4 开放问题
- EN: 4.4 Open Questions

## [211:0] (mymemory)
- ZH: 三个开放问题贯穿全文。其一，文本偏置仍未根治：H-GRPO 的动机正是“忽略图像仅凭文本也能得分”的捷径 [20]，而结果验证方法无法区分“真的看了图”与“恰好蒙对”；视觉对齐奖励虽触及此点，但其评测多在通用 VQA 上，显式组合基准的覆盖仍然不足。其二，组合推理“无唯一答案”与“可验证奖励”存在结构性冲突：验证器只能验证可结构化的侧面，这一约束同时限制了三类方法的上限。其三，外部标注成本：SpatialThinker 依赖基于 Visual Genome 人工场景图标注合成的 STVQA-7K，POLIA 需要数据集物体标注，Ground-R1 证明了无框监督的可行性，但代价是“看对地方”无法被直接验证。
- EN: Three open questions run through the text. First, the text bias is still not cured: H-GRPO's motivation is precisely the shortcut of "ignoring the image can be scored only by the text" [20], and the result verification method cannot distinguish between "really looked at the graph" and "just blinded". Although the visual alignment reward touches this point, its evaluation is mostly on the general VQA, and the coverage of the explicit combination benchmark is still insufficient. Second, there is a structural conflict between "no unique answer" and "verifiable reward" for combinatorial reasoning: the verifier can only verify the structured side, which limits the upper limit of the three types of methods at the same time. Third, external labeling costs: SpatialThinker relies on STVQA-7K synthesized based on Visual Genome artificial scene labeling. Polia requires dataset object labeling. Ground-R1 proves the feasibility of frameless supervision, but the cost is that "looking at the right place" cannot be directly verified.

## [212:0] (mymemory)
- ZH: 5. 未来方向
- EN: 5. Future directions

## [213:0] (mymemory)
- ZH: 分解式可验证奖励。AlphaGRPO 的 DVReward 将复杂请求分解为原子化可验证子问题，再由通用 MLLM 逐项评估 [22]。这一思想对组合推理的直接启示是：将组合提示分解为可验证的子奖励（物体存在性、属性匹配、关系成立），使奖励沿组合结构逐项可判。当前 H-GRPO 的三元组匹配已具备雏形，但子奖励仍依赖参考链而非程序化判定；文本事实核查已有先例（FactScore 的原子事实分解 [23]），迁移到视觉绑定子奖励是自然延伸。
- EN: Split verifiable rewards. AlphaGRPO's DVReward decomposes complex requests into atomized verifiable sub-problems, which are then evaluated item by item by a generic MLLM [22]. The direct inspiration of this idea for combinatorial reasoning is to decompose the combinatorial hints into verifiable sub-rewards (object existence, attribute matching, relationship establishment), so that the rewards can be judged item by item along the combinatorial structure. At present, the triple matching of H-GRPO has a prototype, but the sub-reward still relies on the reference chain rather than procedural judgment; the text fact checking has a precedent (FactScore atomic fact decomposition [23]), and the migration to the visual binding sub-reward is a natural extension.

## [214:0] (mymemory)
- ZH: 统一奖励框架。3.4 节显示三类信号已在方法层面互相渗透；下一步更系统的方向是显式加权融合，即结果验证保证正确性、视觉对齐约束证据、过程信号塑造推理结构，并以多模态 PRM [12] 为统一载体。但需审慎的是，多模态 PRM 以数学推理为主（7 个评测基准中 5 个为数学类），是否具备判断组合绑定正确性所需的感知与对齐能力尚待验证；因此“将组合绑定纳入多模态 PRM 的步骤定义”本身是一个尚待验证的前提，而非现成的解决方案。
- EN: A unified reward framework. Section 3.4 shows that the three types of signals have penetrated each other at the methodological level; the next more systematic direction is explicit weighted fusion, that is, result verification ensures correctness, visual alignment constraint evidence, and process signals shape the inference structure, and multimodal PRM [12] is used as a unified carrier. However, it is prudent to note that multimodal PRM is based on mathematical reasoning (5 of the 7 benchmarks are mathematical), and whether it has the perception and alignment capabilities required to judge the correctness of combinatorial binding has yet to be verified; therefore, "incorporating combinatorial binding into the step definition of multimodal PRM" itself is a premise that has yet to be verified, rather than an off-the-shelf solution.

## [215:0] (mymemory)
- ZH: 评测协议标准化。承接 4.3，向 Swap 式纯绑定测试收敛：统一 Swap 评测协议、共享训练/测试划分，使不同奖励设计在同一试金石上可比；MM-CondChain 的程序化验证范式亦可为标准化提供基础设施 [21]。
- EN: Standardization of evaluation protocols. Undertake 4.3, converge to Swap-style pure binding testing: unify Swap evaluation protocol, share training/test division, so that different reward designs can be compared on the same touchstone; MM-CondChain's programmatic verification paradigm can also provide infrastructure for standardization [21].

## [216:0] (mymemory)
- ZH: 6. 结论
- EN: 6. Conclusion

## [217:0] (mymemory)
- ZH: 本文以奖励信号为主线，梳理了 2024 ~ 2026 年间用强化学习增强 MLLM 组合推理的代表性工作。这些工作围绕“如何为组合推理定义有效奖励信号”这一共同问题，在粒度维度上形成结果验证、视觉对齐与推理过程优化三类互补探索，共同构成奖励信号设计空间中的连续谱（推理展开：答案级→结构级→步骤级；视觉锚定：区域级→物体级）。推动这一空间不断扩展的深层驱动力，是“正确性必须可定义”的约束；面向组合绑定的显式视觉语义奖励仍是当前最有前景、也最亟待填补的研究缺口，现有工作（POLIA）已推进到物体级，向属性-关系组合绑定的扩展尚未被系统探索。随着组合正确性评测走向程序化验证，奖励信号设计有望获得更坚实的地基，但感知事实的验证边界与基准碎片化问题决定了这一扩展仍将是渐进而非跳跃的过程。
- EN: Taking the reward signal as the main line, this paper combines the representative work of strengthening MLLM combination reasoning with reinforcement learning from 2024 to 2026. These efforts revolve around the common problem of "how to define an effective reward signal for combined reasoning", forming three types of complementary exploration in granularity dimension: result validation, visual alignment, and inference process optimization, which together constitute a continuous spectrum in the reward signal design space (inference expansion: answer-level→ structural level→ step level; visual anchoring: regional-level→ object level). The deep driving force driving the expansion of this space is the constraint that "correctness must be definable". Explicit visual semantic rewards for combination binding are still the most promising and most urgent research gap to be filled. Existing work (Polia) has been advanced to the object level, and the extension to attribute-relational combination binding has not yet been systematically explored. As the combined correctness assessment moves toward programmatic validation, the reward signal design is expected to gain a more solid foundation, but the validation boundary and benchmark fragmentation problems of perceived facts determine that this expansion will still be a gradual rather than a jumping process.

## [219:0] (mymemory)
- ZH: 参考文献
- EN: References
