# 数据核对报告3

## 核对结论

二稿中的**核心实验数值、模型规模和基准规模大体可由对应论文原始 PDF 复现**；四张表中与正文重复的数值也已逐项回溯，没有发现表格自行改写数值的情形。不过，有 4 处需要修改或收紧：

1. **MM-CondChain 的“总数据集 4,634 例”不正确。**论文明确的评估集是 **975 个 evaluation samples**，每个样本含一对 True-path / False-path；文中的 4,634 出自逻辑模式分布图，不能当作总数据集规模。
2. **SugarCrepe 的“Swap 是所有模型的薄弱环节”范围过强。**原文支持“所评估的预训练 CLIP 模型，尤其在 Swap、属性和关系扰动上表现较差”，但不支持无条件的“所有模型”。
3. **GRIT 的 0.349→0.387 数值正确，但“显著提升”不宜写成统计显著。**论文给出的是一组消融观测值，没有报告显著性检验；建议改为“提升/观察到提升”。
4. **Self-Questioning 的数值并不支持“直接证明过程结构约束而非答案奖励是提升来源”。**论文恰恰指出大部分增益来自 RL：46.8→51.6；自提问格式只再增加 0.6 点至 52.2。

除上述问题外，CR³ 的“平均超 9 点”在语义上成立，但可用精确值替换；另有部分“所有”“最难”“可忽略”等总结性措辞应保留原论文的适用范围。建议在修改二稿时，优先处理第 1、2、4 项。

## 范围、方法与独立性说明

- **被核对文本**：`二稿.docx` 的正文与表 1–表 4；公式中的变量符号不属于外部数据，未作为数值事实单独核验。
- **证据优先级**：工作区中相应论文的 PDF 原文 → 仅在本地缺 PDF 的 AlphaGRPO 条目使用其 arXiv 原始摘要页。
- **去重规则**：同一数据在正文、表格和注释中重复出现时，合并为一项核验，并列出覆盖位置。例如 CR³、SpatialThinker、SVQA-R1 等结果同时覆盖 3.1/3.4 及表 4。
- **二稿定位记法**：表内的“P31”等是从 `二稿.docx` 抽取正文后的段落序号，用于稳定定位（**不是 Word 页码**）；“表 1–表 4”指二稿中的表格编号。
- **未使用材料**：未读取、未引用 `数据核对报告.md` 或 `数据核对报告2.md`。
- **单位约定**：性能差值除特别说明外均为**绝对百分点（pp）**；“%”保留为原论文的指标单位。不能把不同模型、训练集和协议下的绝对分数横向排序。

## 逐项核对

### A. 组合推理基准与规模（覆盖 2.1 节、表 1）

| 二稿位置与原表数据 | 二稿表述 / 数值 | PDF 原文定位与可复核数据 | 判定与建议 |
|---|---:|---|---|
| 2.1、表 1：VALSE | 6,795 例；存在、复数、计数、空间关系、动作、共指 | VALSE PDF，第 3 页表 1：`505 + 851 + 2,459 + 535 + 1,633 + 812 = 6,795`；表注说明这些是各 piece 的 examples 数。 | **正确。**6,795 是由原表六项相加得到的总数；建议表注写“由表 1 六个 piece 加总”，避免误称论文正文直接报告的单一总数。 |
| 2.1、表 1：CREPE | 37 万级图文对；系统性与生产力 | CREPE PDF，第 1 页摘要：systematicity 测试集“over 370K image-text pairs”；第 4 页表 1给出系统性集合 385,777 / 385,777 / 373,703，以及生产力集合 17,553。 | **正确，但应限定口径。**“37 万级”指其系统性评测部分，非全部派生文本/困难负样本的总和。 |
| 2.1、表 1：ARO | 5 万级用例；属性、关系、词序 | ARO PDF，第 1 页摘要：“more than 50,000 test cases”；第 1–2 页定义 Attribution、Relation、Order 四项测试。 | **正确。**“5 万级”是对“超过 50,000”的恰当概括。 |
| 2.1、表 1：SugarCrepe | 7.5 千级；Replace / Swap / Add | SugarCrepe PDF，第 5 页“Dataset overview”：最终评估集为 **7,512 examples**；同页定义 Replace、Swap、Add，且 Swap 不引入新概念、交换同类别原子概念。 | **正确。**建议将“7.5 千级”写为“7,512 例（约 7.5 千）”，更可复核。 |
| 引言 P7、2.1 P16、4.3 P70 | “Swap 是所有模型的薄弱环节”“物体 > 属性 > 关系，Swap 最难” | SugarCrepe PDF，第 9 页：原文仅称所评估的 pretrained CLIP models 在 Swap、属性与关系扰动上“far from human performance”；同页图 5 给出各模型、各子类结果。 | **范围过强。**替换为“在 SugarCrepe 所评估的预训练 CLIP 模型中，Swap 以及属性/关系扰动尤其困难”。“物体 > 属性 > 关系”也应标为跨表观察，而不是跨所有基准、所有模型的定律。 |
| 引言 P7–P8 | CREPE 的退化随复杂度增加；规模/数据扩张不能自动获得组合能力 | CREPE PDF，第 1 页摘要：复杂度提高时检索成功率下降，且结论“不随模型与训练数据集规模而改变”；第 2 页明确称未发现训练集或模型规模与组合推理的清晰趋势。 | **正确。**建议保留“本评测所测模型/数据规模范围内”的限定，避免外推到所有 MLLM。 |

### B. 验证器奖励（覆盖 3.1、表 3–表 4）

| 二稿位置与原表数据 | 二稿表述 / 数值 | PDF 原文定位与可复核数据 | 判定与建议 |
|---|---:|---|---|
| 3.1 P31、表 4：CR³ | 18.5 万→1.89 万；Qwen2.5-VL-7B / InternVL3-8B；平均超 9 点、较 SFT 超 5 点 | CR³ PDF，第 3 页：先随机抽取 **185,000**，约丢弃 90%，得 **18,900**；第 4 页列出 Qwen2.5-VL-7B 与 InternVL3-8B；第 5 页表 3：Qwen-7B 47.2→57.2（+10.0），InternVL3-8B 48.8→58.1（+9.3）。相对 SFT 分别为 +6.4、+7.9。 | **数值正确，表述可更精确。**两模型相对原始基线平均为 **+9.65 pp**，相对 SFT 平均为 **+7.15 pp**；正文的“10 absolute points”是对两项结果的四舍五入。建议改为“平均 +9.65 pp（论文概括为约 +10 pp）”。 |
| 3.1 P34、表 4：SpatialThinker | 7B；14 个基准；比 GPT-4o 平均高 4.7 pp；STVQA-7K | SpatialThinker PDF，第 3 页：SpatialThinker-7B 在 **14** 个基准上超过 GPT-4o **+4.7% avg.**；第 6 页：STVQA-7K 实为 **7,587** 个空间 VQA 对，来自 Visual Genome 的 human-annotated scene graphs；第 23 页列出 14 个基准。 | **正确。**“STVQA-7K”是数据集名称，实际数为 7,587；若强调规模，请同时给出精确值。 |
| 3.1 P35、表 4：SVQA-R1 | 3B；Q-Spatial++：27.72→58.42；“超 30 点” | SVQA-R1 PDF，第 7 页表 3：SFT(CoT) **27.72**、SVQA-R1 **58.42**；同页正文称相对 SpaceThinker-Qwen2.5VL-3B 为约 31% absolute improvement。 | **正确。**精确差为 **30.70 pp**；“超 30 个百分点”可用。为避免混淆，建议明确 27.72 在表 3 中是 SFT(CoT) 的结果（表 2中同数值还出现于 SpaceThinker-Qwen2.5VL-3B）。 |

### C. 视觉对齐奖励（覆盖 3.2、表 3–表 4）

| 二稿位置与原表数据 | 二稿表述 / 数值 | PDF 原文定位与可复核数据 | 判定与建议 |
|---|---:|---|---|
| 3.2 P39、表 4：Ground-R1 | Qwen2.5-VL-7B；相对 GRPO：V* +2.1、HR-4K +1.2 pp | Ground-R1 PDF，第 7 页表 3：Ground-R1(SRPO) vs Ground-R1-GRPO 在 V* 为 **87.4 vs 85.3**，HR-4K 为 **75.0 vs 73.8**，HR-8K 为 71.1 vs 69.3；紧接正文明确写 +2.1 / +1.2 / +1.8。 | **正确。**建议同时补出 HR-8K 的 +1.8 pp，或明确二稿只选择前两项代表结果。 |
| 3.2 P40、表 4：GRIT | Qwen2.5-VL-3B / InternVL3-2B；20 个三元组；GIoU 0.349→0.387 | GRIT PDF，第 2、6 页：使用 **20 image-question-answer triplets**，两个基座分别为 Qwen2.5-VL-3B 与 InternVL3-2B；第 14 页表 3：含计数数据与奖励的 GRIT 为 **0.387 / 0.437 / 51.8 / 64.4**，去除后为 **0.349 / 0.378 / 53.8 / 60.0**。 | **数值正确。**0.349→0.387 是 in-domain GIoU（差 +0.038），不是总 GIoU。原论文未报显著性检验，建议把“显著提升”改为“提升”。表 4“六数据集七测试集”也正确：第 6 页表 1列六个来源、七个测试列。 |
| 3.2 P43、表 4：POLIA | VSR：GRPO 59.0%→POLIA 81.3%；Aint 0.002 s；Rollout 97.24% | POLIA PDF，第 6 页表 1：Qwen2.5-VL+GRPO 为 **59.0**、POLIA 为 **81.3**（VSR）；第 8 页计算开销段：POLIA-3B 的 rollout 为 **536.25 s / 97.24%**，Aint 为 **0.002 s**。 | **正确。**VSR 增加 **22.3 pp**。这些是 POLIA-3B 的一次训练时间分解，故“开销可忽略”应限定为其测量配置，不宜泛化为所有模型/硬件。 |
| 3.2 P44、4.3 P70、表 4：POLIA | 在 VSR 等 7 个基准上验证 | POLIA PDF，第 2 页贡献和第 6 页“Datasets”：VSR、TallyQA、GQA、MathVista、MathVision、LogicVista、MME，共 **7** 个。 | **正确。**表 1以答案准确率报告，部分比较分数来自官方报告，不能与其他论文的指标直接比较。 |

### D. 推理过程优化（覆盖 3.3、表 3–表 4、5 节）

| 二稿位置与原表数据 | 二稿表述 / 数值 | PDF 原文定位与可复核数据 | 判定与建议 |
|---|---:|---|---|
| 3.3 P46、5 节 P75 | VisualPRM：8B；7 个基准；提升 3.7–8.9 点；其中 5 个数学类 | VisualPRM PDF，第 1 页摘要：VisualPRM 为 **8B**，InternVL2.5-78B 在 7 个基准上 +5.9；第 2 页给出 MiniCPM +8.0、Qwen2.5-VL-7B +3.7、InternVL2.5-8B +8.4、InternVL2.5-78B +5.9；第 6 页表 2补出 InternVL2.5-26B +8.9。表注列出 7 个基准，其中 MathVista、MathVision、MathVerse、DynaMath、WeMath 为 **5 个数学类**。 | **正确，但需说明测量条件。**3.7–8.9 是使用 VisualPRM 作为 critic 的 **Best-of-8 测试时评估总体提升**，不是一次统一 RL 训练的提升。二稿 P75 的“5/7 数学类”准确。 |
| 3.3 P49、表 4：Self-Questioning | A-OKVQA：基座 46.8%，标准 RL 51.6%，本方法 52.2% | Self-Questioning PDF，第 1 页摘要和第 2、6、8 页：46.8、51.6、52.2；第 2、8 页明确称 RL 是主要增益来源，自提问仅增加 **+0.6**。 | **三个数均正确；因果解读需改。**不能说它“直接证明过程结构约束而非答案奖励是提升来源”。可改为“在相同 RL 基础上，自提问格式额外带来 +0.6 pp；多数增益来自 RL 本身”。 |
| 3.3 P54、表 4：H-GRPO | SmolVLM-2.2B 在 A-OKVQA 为 73.4% | H-GRPO PDF，第 8 页表 1：H-GRPO (SmolVLM-2.2B) 在 A-OKVQA / Visual7W 为 **73.4 / 77.2**；第 7 页给出基座 SmolVLM-2.2B、Qwen2.5-VL-3B及训练设定。 | **正确。**该值是 in-domain A-OKVQA validation split；不要将其与 Self-Questioning 的 52.2% 或 POLIA 的 VSR 分数作横比。论文对“小模型受益”的讨论仍受两个基座、两个任务的实验范围限制。 |

### E. MM-CondChain 与与数据集规模有关的论断（覆盖 4.2、4.3）

| 二稿位置与原表数据 | 二稿表述 / 数值 | PDF 原文定位与可复核数据 | 判定与建议 |
|---|---:|---|---|
| 4.2 P68 | “975 个评估样本（每样本含 True-path/False-path 一对；总数据集 4,634 例）” | MM-CondChain PDF，第 9 页“Data Statistics”：**975 evaluation samples in total**，each containing a paired True-path and False-path instance。第 11 页图 4 的 **Total 4634** 位于“Overall Logic Pattern Composition”，并分成 2065 / 1953 / 409 / 109 / 98 五类逻辑模式。 | **部分正确、部分错误（必须修改）。**975 和“每样本一对路径”正确。4,634 是逻辑表达式/模式分布图的总计，不能称为“总数据集 4,634 例”。建议改为：“评估集含 975 个样本，每个样本配 True-path / False-path；图 4另统计了 4,634 个 VPIR 逻辑模式实例。”若按路径分别计数，可说明为 1,950 条配对路径实例，但原文的正式统计口径是 975。 |
| 4.2 P68 | 最强模型 53.33 Path F1 | MM-CondChain PDF，第 1、3、11 页及第 12 页表 3：Gemini-3-Pro 的平均 Path F1 为 **53.33**；Path F1 是 True-path 与 False-path 准确率的调和平均。 | **正确。**建议保留“所评估模型中最强”和“平均 Path F1”的限定。 |
| 4.3 P70 | 结果难以横向比较；不同方法使用 14 / 7 等不同数量基准 | SpatialThinker PDF，第 23 页：14 个基准；POLIA PDF，第 6 页：7 个基准；各论文的基座、训练数据、指标见其各自实验设置。 | **判断合理。**这是基于已核实的评测设置作出的分析结论，不是可直接比较的统一性能排名。 |

## 公式、单位与表格一致性检查

1. **CR³ 的二元奖励与数据筛选**：第 3 页的 `r_acc`、`r_format` 都以 0/1 表示，18.5 万→1.89 万与其并不冲突；表 3–表 4中“无外部标注”应理解为不需额外人工奖励标注，不能误解为完全没有训练数据。
2. **SpatialThinker / Ground-R1 / SVQA-R1 的百分比单位**：三篇原文混用“%”“absolute improvement”“points”。二稿统一用“绝对百分点”是可接受的，但应在首次出现处给出计算基线，例如 `58.42 - 27.72 = 30.70 pp`。
3. **GRIT 的 GIoU 与答案准确率不可混用**：0.349→0.387 是接地区域重叠指标；51.8/64.4 是答案 ACC。二稿表 4已把前者标为“接地 IoU”，这一点正确，建议正文也保持同一名称。
4. **POLIA 的 27.6 与 22.3 不是同一种比较**：表 1中 VSR 的 59.0→81.3 是绝对差 **22.3 pp**；其“Average Improvements 27.6↑”由论文定义为同尺度模型的平均**相对**性能差，不能把 27.6 当 VSR 的 pp 增益。
5. **VisualPRM 的提升不是过程训练指标**：3.7–8.9 取自 Best-of-8 下总体得分差，必须带上 critic / BoN 条件。
6. **四张表的重复值**：表 1 的四个基准规模、表 4的 CR³ / SpatialThinker / SVQA-R1 / Ground-R1 / GRIT / POLIA / Self-Questioning / H-GRPO 值均已被本报告相应条目覆盖；未发现表格值与正文同一结论发生不一致。

## 建议直接替换的关键句

以下替换只处理数据准确性，不改变二稿的论证结构。

1. **CR³（P31）**

   > 论文从 185,000 个候选样本筛至 18,900 个高难度样本。对 Qwen2.5-VL-7B 与 InternVL3-8B，CR³ 在三个组合基准上的平均提升相对原始基线分别为 +10.0 与 +9.3 pp（平均 +9.65 pp；论文概括为约 +10 pp）。

2. **SugarCrepe（P7/P16/P70）**

   > 在 SugarCrepe 所评估的预训练 CLIP 模型中，Swap 以及属性、关系扰动尤其困难；Swap 通过交换同类别原子概念而不引入新概念，是一个较纯粹的绑定测试。

3. **GRIT（P40）**

   > 加入计数数据与相应奖励后，消融中的 in-domain GIoU 从 0.349 提升至 0.387；论文将此作为计数相关训练和奖励有益的证据。

4. **Self-Questioning（P49）**

   > 在 A-OKVQA 上，基座、标准 RL 与 Self-Questioning 的准确率分别为 46.8%、51.6% 和 52.2%。因此，RL 贡献了主要增益，而子问题格式在该设置下额外贡献 0.6 个百分点。

5. **MM-CondChain（P68）**

   > MM-CondChain 的评估集包含 975 个样本，每个样本含一对 True-path / False-path；最强受评模型的平均 Path F1 为 53.33。论文图 4中的 4,634 是 VPIR 逻辑模式构成统计，不应写为总数据集规模。

## 证据索引

下列均为本次实际核对的原始来源。页码按 PDF 页序，表/图名称按论文原文标注。

| 编号 | 原始来源 | 本报告使用位置 |
|---|---|---|
| [1] | `papers/benchmarks/crepe-can-vision-language-foundation-models-reason-compositionally.pdf` | p.1 摘要；p.4 表 1；p.8（规模影响） |
| [2] | `papers/benchmarks/aro-when-and-why-vlms-behave-like-bags-of-words.pdf` | p.1 摘要；p.9（50,000） |
| [3] | `papers/benchmarks/sugarcrepe-fixing-hackable-benchmarks.pdf` | p.5（7,512与三类操作）；p.9（子类困难性） |
| [4] | `papers/verifier/cr3-boosting-compositional-reasoning-in-mllms.pdf` | p.3（185,000→18,900及奖励）；p.5 表 3 |
| [5] | `papers/benchmarks/valse-task-independent-benchmark.pdf` | p.3 表 1（6,795 的各分项） |
| [12] | `papers/process/visualprm-effective-process-reward-model.pdf` | p.1–2（8B、7基准）；p.6 表 2（3.7–8.9、5个数学类） |
| [13] | `papers/verifier/spatialthinker-reinforcing-scene-graph-grounded-spatial-reasoning.pdf` | p.3（14、+4.7）；p.6（7,587）；p.23（14个基准） |
| [14] | `papers/verifier/svqa-r1-reinforcing-spatial-reasoning.pdf` | p.7 表 2–3（27.72、58.42） |
| [15] | `papers/grounded/ground-r1-incentivizing-grounded-visual-reasoning.pdf` | p.7 表 3与Q3讨论（+2.1、+1.2、+1.8） |
| [16] | `papers/grounded/grit-teaching-mllms-to-think-with-images.pdf` | p.2、p.6表1（20、基座、测试集）；p.14 表 3（0.349、0.387） |
| [17] | `papers/grounded/POLIA_Policy_Optimizatio.pdf` | p.2（7数据集）；p.6 表1（59.0、81.3）；p.8（0.002 s、97.24%） |
| [19] | `papers/process/self-questioning-vlms-reinforcement-learning-compositional-visual-reasoning.pdf` | p.1–2、p.6 表 2、p.8结论（46.8、51.6、52.2） |
| [20] | `papers/process/h-grpo-permutation-invariant-reinforcement-learning.pdf` | p.7（基座）；p.8 表 1（73.4） |
| [21] | `papers/mm-condchain-programmatically-verified-benchmark.pdf` | p.9（975）；p.11 图 4（4,634）及结果；p.12 表 3（53.33） |
| [22] | [AlphaGRPO arXiv 原始摘要页](https://arxiv.org/abs/2605.12495) | 工作区无 PDF 时的补充来源；证实 DVReward 将复杂请求拆为原子、可验证的语义和质量问题。 |

> 说明：本报告不把二稿自身的章节编号、公式编号、作者信息、引用编号和论文发表年份当作“实验数据”逐一评级；它们仅用于定位。若后续需要，可另做一份参考文献与出版信息核查。
