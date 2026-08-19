# 二稿《多模态大语言模型组合推理中的强化学习方法:奖励信号的演进》数据核对报告

> 核对日期:2026-08-18
> 核对范围:二稿全部数据表述(段落、表格、公式、注释)
> 核对基准:论文 PDF 原文为准;PDF 不含处参考 Web 检索(仅 AlphaGRPO 一篇,已标注)
> 核对方式:27 篇 PDF 全文文本化后逐关键词检索,每个数据点摘录原文与页码

---

## 1. 核对范围与方法

### 1.1 覆盖范围

- 二稿全文 104 个段落(含空段;非空 94 段)、4 张表(表 1~表 4)、9 个公式(#(1)~#(9))、图 1 说明
- 参考文献 23 篇([1]~[23]),其中 22 篇有本地 PDF、1 篇(AlphaGRPO [22])无 PDF 改用 arXiv HTML 检索核实

### 1.2 方法说明

1. 用 PyMuPDF 将 papers/ 下 27 个 PDF 全部文本化,带 `===== PAGE n =====` 页码标记
2. 对二稿每个数据点抽取关键词,批量检索原文,摘录命中上下文
3. 对公式类数据点做公式级比对(变量、门控位置、系数)
4. 检索不到的表述二次深挖(扩展同义词、缩短上下文窗口),仍无出处者判为"无原文出处"
5. 结论分三档:**✓ 一致**、**✗ 需修正**(原文支持不同表述或书写错误)、**⚠ 需注意**(口径/来源/推断性问题)

### 1.3 页码约定

下文"PDF 第 N 页"指 PDF 文件页码(即提取文本的 PAGE 标记)。部分论文(如 CR³)PDF 页与论文标注页一致,可直接对应到论文页。

---

## 2. 结论总览

| 类别 | 数量 | 说明 |
|---|---|---|
| ✓ 一致 | 84 项 | 数据与论文原文吻合,均附出处 |
| ✗ 需修正 | 8 项(E1~E8) | 公式书写错误 1(E1)、表格数据错误 1(E2)、结论性表述失准 2(E3 表 1 关键发现 + E7 P045 小结)、无出处数据 1(E4)、评测基准表述失准 3(E5/E6/E8) |
| ⚠ 需注意 | 11 项(N1~N7 与 D18/D53/D77/D91 等概括、弱确认、点评性条目) | 口径、来源、推断性问题,建议加注而非改数 |

**修正清单(速览)**:

| 编号 | 位置 | 问题 | 修正建议 |
|---|---|---|---|
| E1 | 公式 #(3) | 门控 `1[Ra=1]` 错挂在准确率分量上 | 应挂空间分量:`Rtotal = 1[Rfmt=1](wfRf + wcRc + waRa + 1[Ra=1]·wsRs)` |
| E2 | 表 1 VALSE 行 | "851 例"错误(851 仅复数子集) | 改为 6,795 例 |
| E3 | 表 1 VALSE 行 | "空间关系、共指最弱"失准 | 改为"计数与动作最弱"或"存在性强、关系绑定弱" |
| E4 | P044 | "0.0004%"无原文出处(自算) | 改为"Aint 仅耗时 0.002 s;Rollout 占 97.24%" |
| E5 | 表 4 Ground-R1 行 | 评测基准"通用 VQA 与空间问答"不符 | 改为"通用 LVLM + 高分辨率 + 接地" |
| E6 | 表 4 GRIT 行 | 评测基准"通用 VQA 与空间问答"不符 | 改为"VSR/TallyQA/GQA/MathVista/MME/OVDEval(七测试集)" |
| E7 | P045 节内小结 | "多在通用 VQA 与空间问答上验证"概括不全 | 改为"在通用/高分辨率与接地基准上验证,显式组合基准覆盖不足" |
| E8 | 表 4 H-GRPO 行 | "自建 OOD 基准"失准(OOD 为既有基准) | 改为"A-OKVQA/Visual7W 与 OOD 基准(MMMU/RealWorldQA/RoboSpatial/MMStar)" |

---

## 3. 逐数据点核对详表

> 排序按二稿出现顺序。每点给出一致性结论、二稿表述、原文出处(论文 + PDF 页码 + 原文摘录)。

### 3.1 引言与背景(第 1 节)

#### D01 P008 | CREPE:组合理解随复杂度增加显著退化 — ✓ 一致

- **二稿**: "CREPE 发现组合理解随组合复杂度增加而显著退化 [1]"
- **出处**: [CREPE][PDF p1] "For systematicity, we find that model performance decreases consistently when novel compositions dominate the retrieval set, with Recall@1 dropping by up to 12%. For productivity, models' retrieval success decays as complexity increases, frequently nearing random chance at high complexity. These results hold regardless of model and training dataset size."
- **说明**: 概括性转述,与原文一致。

#### D02 P008 | ARO:VLM 像"词袋模型" — ✓ 一致

- **二稿**: "ARO 指出视觉语言模型本质上像'词袋模型',对词序与组合结构不敏感 [2]"
- **出处**: [ARO][PDF p1] "We present the settings in which state-of-the-art VLMs behave like bags-of-words—i.e. when they have poor relational understanding, can blunder when linking objects to their attributes, and demonstrate a severe lack of order sensitivity."
- **说明**: 一致。

#### D03 P008 | SugarCrepe:Swap 是薄弱环节 — ✓ 一致

- **二稿**: "SugarCrepe 显示,纯绑定测试(Swap)是所有模型的薄弱环节 [3]"
- **出处**: [SugarCrepe][PDF p8] "All models struggle at identifying SWAP hard negatives... SWAP hard negatives present the biggest challenge."
- **说明**: 一致。

#### D04 P009 | ARO shortcut 分析 — ✓ 一致

- **二稿**: "现有对比预训练的目标并不要求模型理解组合结构,模型仅凭词频与整体语义即可取得高分 [2]"
- **出处**: [ARO][PDF p1] "Given that contrastive pretraining optimizes for retrieval on large datasets with similar shortcuts, we hypothesize that this can explain why the models do not need to learn to represent compositional information.";[PDF p2] "not learning the compositional information is a valid shortcut strategy";[PDF p6] "the task can be solved without taking order information into account — and behaving like a bag-of-words becomes a high-reward strategy."
- **说明**: 一致。

#### D05 P009 | CREPE:缺陷与规模无关 — ✓ 一致

- **二稿**: "组合性缺陷与模型规模无关,单纯扩大数据与参数无法自动习得组合能力 [1]"
- **出处**: [CREPE][PDF p1] "These results hold regardless of model and training dataset size."
- **说明**: 一致。

#### D06 P009 | CR³ 平均提升超 9 个绝对点 — ✓ 一致

- **二稿**: "论文报告其在组合基准上较原始基线平均提升超 9 个绝对点 [4]"
- **出处**: [CR³][PDF p5 表 3] Qwen2.5-VL-7B: 47.2 → 57.2(+10.0);InternVL3-8B: 48.8 → 58.1(+9.3);Qwen2.5-VL-3B: 26.6 → 44.6(+18.0);InternVL3-2B: 24.9 → 36.4(+11.5);[PDF p6] "CR3 achieves average absolute gains of 18.0 and 11.5 compared to Qwen2.5-VL-3B and InternVL3-2B baselines... boosts the average compositional performance of Qwen2.5-VL-7B and InternVL3-8B by 10 absolute points."
- **说明**: 7B/8B 平均 +9.65,超 9 点成立;正文用四舍五入的 "10 absolute points"。口径为三个组合基准的平均绝对提升,二稿表 4 注已有说明。

#### D07 P016 | VALSE 覆盖六种语言现象 — ✓ 一致

- **二稿**: "VALSE 通过构造伪造实例,测试模型对存在性、计数、空间关系等语言现象的判断 [5]"
- **出处**: [VALSE][PDF p1] "We cover a wide spectrum of basic linguistic phenomena affecting the linguistic and visual modalities: existence, plurality, counting, spatial relations, actions, and entity coreference."
- **说明**: 一致。

#### D08 P016 | CREPE 规模 37 万级 — ✓ 一致

- **二稿**: "CREPE 将评测规模扩大至 37 万级图文对 [1]"
- **出处**: [CREPE][PDF p1] "CREPE consists of a test dataset containing over 370K image-text pairs and three different seen-unseen splits."
- **说明**: 一致。

#### D09 P016 | ARO 5 万级、三类组合结构 — ✓ 一致

- **二稿**: "ARO 以 5 万级用例覆盖属性、关系与词序三类组合结构 [2]"
- **出处**: [ARO][PDF p1] "ARO consists of Visual Genome Attribution, to test the understanding of objects' properties; Visual Genome Relation, to test for relational understanding; and COCO-Order & Flickr30k-Order, to test for order sensitivity in VLMs. ARO is orders of magnitude larger than previous benchmarks of compositionality, with more than 50,000 test cases."
- **说明**: 一致。

#### D10 P016 | ARO 揭示检索基准 shortcut — ✓ 一致

- **二稿**: "并揭示现有检索基准不要求组合理解、模型可绕道得分的 shortcut [2]"
- **出处**: [ARO][PDF p1] "we demonstrate that it is possible to perform well on image-text retrieval over existing datasets without using the composition and order information."
- **说明**: 一致。

#### D11 P016 | SugarCrepe 三类原子操作 — ✓ 一致

- **二稿**: "用 LLM 生成语义合理的困难负样本,将评测收敛为 Replace、Swap、Add 三类原子操作 [3]"
- **出处**: [SugarCrepe][PDF p5] "The REPLACE form... The SWAP form... The ADD form."(三种 hard-negative 形式,每形式下再分细类共 7 类);[PDF p3] "Existing hard negative generation process introduces undesirable biases... produce hard negatives by replacing a word of specific..."(程序化负样本的问题)
- **说明**: 一致。"三类原子操作"即 REPLACE/SWAP/ADD 三种形式。

#### D12 表 1 R01 | VALSE 规模 "851 例" — ✗ 需修正(E2)

- **二稿**: 表 1 VALSE 行规模列 "851 例"
- **出处**: [VALSE][PDF p3 表 1] 各子任务实例数:existence 505、plurality 851、counting 2,459、relations 535、actions 1,633、coreference 812,合计 **6,795**;[PDF p4] "The dataset consists of 851 validated instances out of 1000 generated candidates"(851 仅为 plurality 子任务)。
- **结论**: ✗ 错误。851 是复数(plurality)子任务的实例数,二稿误当作 VALSE 总规模。应改为 **6,795 例**。

#### D13 表 1 R01 | VALSE "空间关系、共指最弱" — ✗ 需修正(E3)

- **二稿**: 表 1 VALSE 行关键发现列 "空间关系、共指最弱"
- **出处**: [VALSE][PDF p8 表 2] 最佳模型 ViLBERT 12-in-1 的 foil 识别准确率:存在 95.6、复数 72.4/76.7/80.2/77.3、计数 67.7/65.9/58.9、空间关系 75.7、动作 69.2、共指 86.9、Foil-it 75.1、Avg 75.1;[PDF p8] 论文结论 "V&L models identify named objects and their presence in images well (existence), but struggle to ground their interdependence and relationships."
- **结论**: ✗ 失准。最弱的是**计数(58.9)与动作(69.2)**;空间关系 75.7 处中上水平;共指 86.9 明显偏强。论文结论是"物体存在性识别强、相互依赖与关系绑定弱"。建议关键发现列改为"计数与动作最弱"或直接引论文结论"存在性强、关系绑定弱"。

#### D14 表 1 R02 | CREPE 行(37 万级/缺陷与规模无关) — ✓ 一致

- **出处**: [CREPE][PDF p1] "over 370K image-text pairs";"These results hold regardless of model and training dataset size."
- **说明**: 同 D05/D08,一致。

#### D15 表 1 R03 | ARO 行(词袋模型;存在 shortcut) — ✓ 一致

- **出处**: [ARO][PDF p1] 同 D02/D04。
- **说明**: 一致。

#### D16 表 1 R04 | SugarCrepe "7.5 千级" — ✓ 一致

- **二稿**: 表 1 SugarCrepe 行规模列 "7.5 千级"
- **出处**: [SugarCrepe][PDF p5] "The final evaluation set of SUGARCREPE consists of 7512 examples."
- **说明**: 一致。

#### D17 表 1 R04 | SugarCrepe "Swap 最难" — ✓ 一致

- **二稿**: 表 1 SugarCrepe 行关键发现列 "Swap 最难"
- **出处**: [SugarCrepe][PDF p8] "All models struggle at identifying SWAP hard negatives... SWAP hard negatives present the biggest challenge."
- **说明**: 一致。

#### D18 P017 | "物体识别强于属性绑定,属性强于关系理解,Swap 最难" — ⚠ 需注意(概括性结论)

- **二稿**: "物体识别强于属性绑定,属性强于关系理解,纯粹的绑定(Swap)最难"
- **出处**: "Swap 最难"有直接出处([SugarCrepe][PDF p8],见 D17)。"物体>属性>关系"无单句直接出处,是综合 ARO(关系理解最差、属性链接易错,[PDF p1] "poor relational understanding, can blunder when linking objects to their attributes")、VALSE(存在性 95.6 最强、关系/计数最弱)与 SugarCrepe 实验表(各模型 Replace-REL 普遍低于 Replace-OBJ/ATT)的概括。
- **结论**: ⚠ 合理概括,数据表支持,但非原文原话。若审稿较真可加注"综合多基准结论"。

#### D19 P020 | LLaVA-RLHF:奖励来自人类对回答的评判 — ✓ 一致

- **二稿**: "LLaVA-RLHF [6]、RLHF-V [7]、Silkie [8] 等工作共同确立了'奖励来自对回答的评判'这一范式,反馈粒度停留在回答整体或语言片段"
- **出处**: [LLaVA-RLHF][PDF p1] "we adapt the Reinforcement Learning from Human Feedback (RLHF) from the text domain to the task of vision-language alignment, where human annotators are asked to compare two responses and pinpoint the more hallucinated one, and the vision-language model is trained to maximize the simulated human rewards."
- **说明**: 一致(回答级比较)。

#### D20 P020 | RLHF-V:反馈粒度到语言片段 — ✓ 一致

- **出处**: [RLHF-V][PDF p1] "RLHF-V collects human preference in the form of segment-level corrections on hallucinations, and performs dense direct preference optimization over the human feedback."
- **说明**: 一致(段级纠正即"语言片段"粒度)。

#### D21 P020 | Silkie:AI 反馈 — ✓ 一致

- **出处**: [Silkie][PDF p1] "we investigate the efficacy of AI feedback to scale supervision for aligning LVLMs. We introduce VLFeedback, the first large-scale vision-language feedback dataset, comprising over 82K multimodal instructions... generated by off-the-shelf models without human [annotation]."
- **说明**: 一致(回答级 AI 反馈)。

### 3.2 RL 基础(第 2 节)

#### D22 P021 | GRPO 去除价值网络、组内相对优势 — ✓ 一致

- **二稿**: "DeepSeekMath 提出的 GRPO [9] 去除了 PPO 的价值网络,对同一问题采样多个回答,用组内相对优势...替代 critic 打分"
- **出处**: [DeepSeekMath][PDF p2] "GRPO foregoes the critic model, instead estimating the baseline from group scores, significantly reducing training resources.";[PDF p13] "GRPO foregoes the value model, instead estimating the baseline from group scores."
- **说明**: 一致。

#### D23 公式 #(1) | GRPO 归一化公式 — ✓ 一致

- **二稿**: `Ai=(ri−r̄)/σr` #(1)
- **出处**: [DeepSeekMath][PDF p14] "Âi,t = ẽri = ri−mean(r)/std(r)"(原文公式 (6) 附近:"these rewards are normalized by subtracting the group average and dividing by the group standard deviation... sets the advantages Âi,t of all tokens in the output as the normalized reward")
- **说明**: 一致(二稿为简化单 token 写法)。

#### D24 P023 | "配合确定性规则验证器提供奖励" — ✓ 一致

- **二稿**: "配合确定性规则验证器提供奖励,开辟了 RLVR 路线"
- **出处**: [DeepSeekMath][PDF p15] "We divide the reward function as 'Rule' and 'Model'... Rule refers to judging the quality of a response based on the correctness of the answer."
- **说明**: "规则判据"一致。"RLVR 术语归属"见 N4。

#### D25 P023 | RLVR 术语归属 — ⚠ 需注意(N4)

- **二稿**: "开辟了'可验证奖励强化学习'(RL with Verifiable Rewards, RLVR)路线"
- **出处**: [DeepSeekMath] 全文无 "verifiable reward / RLVR" 字样(检索 "verifiable"、"rule-based" 均无该术语)。DeepSeekMath 原文用 "Rule" 与 "Model" 二分奖励(p15)。"RLVR" 术语由 **DeepSeek-R1**(2025)正式使用。
- **结论**: ⚠ 术语归属需加注。建议改为"以规则验证器提供奖励,开辟了可验证奖励强化学习(RLVR,术语见 DeepSeek-R1)的雏形",或在引用处加脚注。

#### D26 P023 | DPO:离线偏好对、无需显式奖励模型 — ✓ 一致

- **二稿**: "一个自然的对照是直接偏好优化(DPO)[10]:它以离线偏好对为原料、无需显式奖励模型"
- **出处**: [DPO][PDF p1] "we show how to directly optimize a language model to adhere to human preferences, without explicit reward modeling or reinforcement learning.";[PDF p5] "Sample completions y1, y2 ∼ πref(·|x) for every prompt x, label with human preferences to construct the offline dataset of preferences."
- **说明**: 一致。

#### D27 P023 | DPO 偏好对静态、不随策略更新 — ✓ 一致

- **二稿**: "DPO 的偏好对来自固定采样分布,不随策略迭代更新"
- **出处**: [DPO][PDF p3] "Assuming access to a static dataset of comparisons D = {x(i), y(i)w, y(i)l} sampled from p∗."
- **说明**: 一致(static dataset)。

#### D28 P024 | GRPO 与 PRM-aware 目标等价 — ✓ 一致

- **二稿**: "在 token 级策略梯度与单次更新的设定下,标准 GRPO 目标与 PRM-aware 目标数学等价,组内多条回答的共享前缀天然定义了'过程步骤',GRPO 一直在隐式地做过程级信用分配 [11]"
- **出处**: [GRPO-is-PRM][PDF p1] "we provide theoretical proof in this work that the Group Relative Policy Optimization (GRPO) RL algorithm equipped with an ORM is in fact equivalent to a PRM-aware RL objective equipped with a non-trivial, Monte-Carlo-based PRM (given mild assumptions).";[PDF p1 图 1] "Overlapping trajectory prefixes define process steps";[PDF p1] "We prove that the standard GRPO algorithm with outcome-level rewards performs sub-trajectory-level credit assignment in this manner, whenever trajectories within a group share overlapping prefixes."
- **说明**: 一致("token 级策略梯度与单次更新"与原文 "given mild assumptions" 相符)。

#### D29 P024 | VisualPRM 将 PRM 扩展到多模态 — ✓ 一致

- **二稿**: "多模态侧,VisualPRM 等工作已将 PRM 扩展到多模态推理 [12]"
- **出处**: [VisualPRM][PDF p1] "We introduce VisualPRM, an advanced multimodal Process Reward Model (PRM) with 8B parameters."
- **说明**: 一致。

### 3.3 CR³(3.1 节)

#### D30 P030 | 三个图文匹配任务 — ✓ 一致

- **二稿**: "构造三个图文匹配任务(TG-VCR、VG-TCR、CITM)"
- **出处**: [CR³][PDF p4] "Text-Guided Visual Compositional Reasoning (TG-VCR)... Visual-Guided Textual Compositional Reasoning (VG-TCR)... Compositional Image-Text Matching (CITM)."
- **说明**: 一致。

#### D31 P030/P031 | 回答正误由确定性规则判定 — ✓ 一致

- **二稿**: "回答正误由确定性规则判定,奖励由答案正确与推理顺序两个二元分量构成"
- **出处**: [CR³][PDF p3] "The adopted reward functions include: Accuracy reward racc: this reward function checks whether the predicted output exactly matches the ground-truth answer. If they match identically, it returns a reward score of 1; otherwise, the score is 0.";"Format reward rformat: the format reward verifies whether the model's output adheres to a required format... The reward score is 1 only when the output strictly follows this format; otherwise, the score is 0."
- **说明**: 一致。

#### D32 公式 #(2) | r = racc + λrformat — ✓ 一致

- **出处**: [CR³][PDF p3] "The final rule-based reward function combines the accuracy reward racc with the format reward rformat as follows: r = racc + λrformat (3)."
- **说明**: 一致。

#### D33 P032 | λ = 1.0 — ✓ 一致

- **二稿**: "[公式] λ=1.0"(内联于公式 #(2) 之后,当前 P032)
- **出处**: [CR³][PDF p4] "The format reward scaling factor λ is fixed at 1.0 to achieve optimal performance."
- **说明**: 一致。注:λ=1.0 仅出现在二稿公式中(P032 内联 OMML),正文未单独给出该数值。

#### D34 P032 | 答案分量取 1 的条件 — ✓ 一致

- **二稿**: "答案分量在输出与标准答案完全一致时取 1,顺序分量在输出严格遵循'先以 <think> 给出推理、再以 <answer> 给出答案'的格式时取 1"
- **出处**: [CR³][PDF p3] "checks whether the predicted output exactly matches the ground-truth answer... returns a reward score of 1; otherwise, the score is 0";"The adopted format prompt instructs the model to: 'first output the thinking process in <think> </think> tags and then output the final answer in <answer> </answer> tags'. The reward score is 1 only when the output strictly follows this format; otherwise, the score is 0."
- **说明**: 一致。

#### D35 P032 | 18.5 万→1.89 万难负样本 — ✓ 一致

- **二稿**: "通过语义与视觉双重筛选构造高难度负样本(18.5 万→1.89 万)"
- **出处**: [CR³][PDF p3] "We first randomly sample 185,000 instances... This stringent filtering process discards approximately 90% of the initial samples, yielding... 18,900 instances."(语义过滤阈值 0.7 参照 Winoground、视觉过滤阈值 0.75,见同页)
- **说明**: 一致。

#### D36 P032 | 7B/8B 平均提升超 9 个绝对点 — ✓ 一致

- **二稿**: "论文报告 Qwen2.5-VL-7B 与 InternVL3-8B 在三个组合基准上较原始基线平均提升超 9 个绝对点"
- **出处**: [CR³][PDF p5 表 3] Qwen2.5-VL-7B: MMVP 20.0→51.3、Winoground 43.3→53.8、Cola 47.2→57.2(平均 +10.0);InternVL3-8B: 48.8→58.1(+9.3);[PDF p6] "boosts the average compositional performance of Qwen2.5-VL-7B and InternVL3-8B by 10 absolute points."
- **说明**: 一致(平均 9.65)。

#### D37 表 4 R01 | 较 SFT 超 5 点 — ✓ 一致

- **二稿**: 表 4 CR³ 行 "较 SFT 超 5 点"
- **出处**: [CR³][PDF p5 表 3] 7B: +SFT 50.8 → +CR3 57.2(+6.4);8B: +SFT 50.2 → +CR3 58.1(+7.9);[PDF p6] "absolute average improvement of over 5 points compared to SFT-based method."
- **说明**: 一致。

#### D38 P032 | 无 SFT 常见的领域外退化 — ✓ 一致

- **二稿**: "且无 SFT 常见的领域外退化"
- **出处**: [CR³][PDF p1] "CR3 demonstrates superior generalization by improving performance on out-of-domain benchmarks where SFT methods degrade";[PDF p2] "SFT methods suffer performance [degradation]... We further evaluate out-of-domain generalization using popular multimodal benchmarks (e.g., MMMU and MMB)."
- **说明**: 一致。

### 3.4 SpatialThinker(3.1 节)

#### D39 P033 | 固定模板"观察→场景图→推理→答案" — ✓ 一致

- **二稿**: "模型按固定模板输出'观察→场景图→推理→答案'"
- **出处**: [SpatialThinker][PDF p2] "This promotes human-like reasoning following observe, localize, think, answer";[PDF p4] 模板 `<observe>...<scene>...<think>...<answer>`(详见论文第 4 页模板设计)
- **说明**: 一致(observe/localize/think/answer 四段式)。

#### D40 公式 #(3) | 字典序门控公式 — ✗ 需修正(E1)

- **二稿**: `Rtotal = 1[Rfmt=1](wfRf + wcRc + waRa·1[Ra=1] + wsRs)` #(3),正文文字 "空间奖励仅在答案正确时生效"
- **出处**: [SpatialThinker][PDF p5 公式 (3)] "Rtotal = I[Rformat = 1] · (wformatRf + wcountRc + waccuracyRaI[Raccuracy = 1] wspatialRs)";[PDF p5] 权重 "Rf... is weighted at wformat = 0.1";"wcount = 0.2";"carries the highest weight (waccuracy = 0.5)";"wspatial = 0.2";[PDF p5] "we compute the spatial reward only when the final answer is correct."
- **结论**: ✗ 公式书写错误。原文门控 `I[Raccuracy=1]` 作用在**空间分量 wspatialRs** 上(答案正确时才给空间奖励),二稿公式却写为 `waRa·1[Ra=1]`(门控挂在准确率分量上),且排版丢了加号。**正文文字是对的,公式错了**。正确写法:`Rtotal = 1[Rfmt=1](wfRf + wcRc + waRa + 1[Ra=1]·wsRs)`。

#### D41 P035 | 7B 模型 14 基准平均超 GPT-4o 4.7 个百分点 — ✓ 一致

- **二稿**: "论文报告 7B 模型在 14 个基准上平均超越 GPT-4o 4.7 个百分点"
- **出处**: [SpatialThinker][PDF p3] "SpatialThinker-7B, trained on only 7K samples from our synthesized STVQA-7K dataset, outperforms SFT (+5.5%) and conventional RL baselines (+3.2%) across fourteen benchmarks, surpassing GPT-4o (+4.7% avg.)";[PDF p8] "We evaluate across 14 benchmarks: eight spatial and six real-world VQA."
- **说明**: 一致(14 = 8 空间 + 6 真实世界 VQA)。

#### D42 P035 | STVQA-7K 基于 Visual Genome 人工标注 — ✓ 一致

- **二稿**: "STVQA-7K 基于 Visual Genome 人工标注构建"
- **出处**: [SpatialThinker][PDF p6] "STVQA-7K, a synthetic visual question answering (VQA) dataset built from human-annotated scene graphs in Visual Genome... STVQA-7K comprises 7,587 spatially grounded multiple-choice VQA pairs."
- **说明**: 一致。

#### D43 表 3 R02 | 匈牙利匹配 + CIoU 稠密梯度 — ✓ 一致

- **二稿**: 表 3 SpatialThinker 行 "匈牙利匹配 + CIoU 稠密梯度"
- **出处**: [SpatialThinker][PDF p5] "Predicted and ground-truth objects are matched using the Hungarian algorithm for bipartite matching with a cost function that combines Complete IoU (CIoU) and semantic similarity";"CIoU offers dense supervision over IoU."
- **说明**: 一致。

#### D44 表 4 R02 | 基座 7B、14 基准 — ✓ 一致

- **出处**: [SpatialThinker][PDF p1] "Qwen2.5-VL 7B"(示例与主实验);[PDF p8] 14 基准组成。
- **说明**: 一致(SpatialThinker-7B 为主结果,另有 30B 变体)。

#### D45 P073 | 依赖 7K 人工场景图标注 — ✓ 一致

- **二稿**: "SpatialThinker 依赖 7K 人工场景图标注"
- **出处**: [SpatialThinker][PDF p2] "Trained on only 7K samples";[PDF p3] "training on only 7K samples from our synthesized STVQA-7K dataset"。
- **说明**: 一致(7K 为训练样本规模;STVQA-7K 共 7,587 对,标注源自 Visual Genome 人工场景图)。

### 3.5 SVQA-R1(3.1 节)

#### D46 P036 | 镜像翻转 + GPT-4o 生成翻转后问答对 — ✓ 一致

- **二稿**: "将图像镜像翻转并用 GPT-4o 生成翻转后逻辑一致的问答对"
- **出处**: [SVQA-R1][PDF p3] "we employ GPT-4o to automatically generate revised QA pairs for each flipped image... to produce a logically correct version suitable for the flipped view";[PDF p1] "perturbing spatial relations between objects, e.g., mirror flipping."
- **说明**: 一致。

#### D47 P036 | 奖励为格式与语义两分量加权 — ✓ 一致

- **二稿**: "[公式] r=λ1rf+λ2rs"
- **出处**: [SVQA-R1][PDF p4-5 公式 (1)] "r = λ1 · rf + λ2 · rs";[PDF p6] "we set the weighting coefficients λ1 and λ2 to 0.5, balancing between the semantic and format rewards."
- **说明**: 一致。

#### D48 P036/表 4 | "较 SFT 基线提升超 30 个百分点" — ⚠ 需注意(N1)

- **二稿**: "论文报告 3B 模型在 Q-Spatial++ 上较 SFT 基线提升超 30 个百分点"
- **出处**: [SVQA-R1][PDF p2] "SVQA-R1 can improve the accuracy over the SFT-based baseline by more than 30% on the Q-Spatial++ benchmark";[PDF p7 表 3] Base 21.78、SFT 37.62、SFT (CoT) 27.72、SFT (CoT)∗ 27.72、SVQA-R1 58.42。
- **结论**: ⚠ 数字本身正确但口径需注意:58.42 − 27.72 = +30.7pp,对应的是 **SFT(CoT) 基线**(SpaceThinker-Qwen2.5VL-3B);若对照表 3 中普通 SFT(37.62),提升仅 +20.8pp。原文摘要的 "SFT-based baseline" 即指 SFT(CoT)。建议二稿在表 4 该行注 "相对 SFT(CoT) 基线(27.72→58.42)"。

### 3.6 Ground-R1(3.2 节)

#### D49 P040 | 两阶段 rollout:先出证据框、再基于裁剪作答 — ✓ 一致

- **二稿**: "两阶段 rollout 中,模型先输出证据框坐标、再基于裁剪出的局部图像作答"
- **出处**: [Ground-R1][PDF p4] "the corresponding evidence region ei is derived through zoom-in and cropping operations";"The answering phase takes the input image, question, and the generated evidence regions as input and delivers final answers."
- **说明**: 一致。

#### D50 P040 | 全局归一化偏袒大区域、小证据负优势 — ✓ 一致

- **二稿**: "标准 GRPO 的全局归一化偏袒大而显著的证据区域,小证据获得持续负优势"
- **出处**: [Ground-R1][PDF p1] "most existing methods suffer from a systematic scale-driven bias in optimization, where training rewards are dominated by large visual regions, suppressing learning from small but semantically critical evidence";[PDF p2] "consistently negative advantages for small regions."
- **说明**: 一致。

#### D51 P040 | 按区域面积分箱、桶内/桶间归一化 — ✓ 一致

- **二稿**: "提出尺度相对策略优化(SRPO),按区域面积分箱做桶内/桶间归一化"
- **出处**: [Ground-R1][PDF p4] "we apply... equal-sized bins based on their relative areas";"we apply binary rewards including both intra- and inter-bin rewards";[PDF p1] "scale-aware binning and intra-/inter-bin comparisons."
- **说明**: 一致。

#### D52 P040 | 较标准 GRPO:V* +2.1、HR-4K +1.2 — ✓ 一致

- **二稿**: "较标准 GRPO 在 V* 与 HR-4K 上分别提升 2.1 与 1.2 个百分点"
- **出处**: [Ground-R1][PDF p7] "To quantify the effectiveness of SRPO, we compare Ground-R1 with Ground-R1-GRPO, which shares the same architecture but replaces SRPO with standard GRPO... SRPO brings substantial gains on high-resolution benchmarks, achieving an improvement of +2.1% on V∗, +1.2% on HR-4K, and +1.8% on HR-8K."
- **说明**: 一致。对比基线为 Ground-R1-GRPO(同一架构仅 SRPO→GRPO),即二稿所称"标准 GRPO"。

#### D53 P040 | "无需框标注" — ⚠ 弱确认(机制成立)

- **二稿**: "证明 RL 下无需框标注即可驱动模型学会定位证据"
- **出处**: [Ground-R1] 训练奖励为格式 + 答案验证(无框 IoU 奖励),证据框由模型自生成(p4 两阶段 rollout 机制);论文对 Ground-R1 的定位是免逐步监督("without step-wise supervision",[PDF p1])。
- **结论**: ⚠ 机制上成立(训练中不使用人工框标注),但论文无"无需框标注"原话;建议表述为"不依赖外部框标注"并加注机制依据。

#### D54 表 4 R04 | 评测基准"通用 VQA 与空间问答" — ✗ 需修正(E5)

- **二稿**: 表 4 Ground-R1 行评测基准列 "通用 VQA 与空间问答"
- **出处**: [Ground-R1][PDF p1] "Experimental results on general LVLM, high-resolution, and visual grounding benchmarks";[PDF p6 表 1] 评测含 MME、MM-Vet、SEED、MME-RWL、RWQA、POPE(通用 LVLM)+ V∗、HR-4K、HR-8K(高分辨率);[PDF p7 表 3 附近] 另有视觉接地评测(RefCOCO/RefCOCO+/RefCOCOg、Visual Search,见论文 4.3 节)。
- **结论**: ✗ 不符。应改为 "**通用 LVLM(MME/MM-Vet/SEED 等)+ 高分辨率(V*/HR-4K/HR-8K)+ 视觉接地**"。

### 3.7 GRIT(3.2 节)

#### D55 P041 | 框坐标内嵌思维链(<think>→<rethink>→<answer>) — ✓ 一致

- **二稿**: "包围框坐标直接内嵌进思维链(<think>→<rethink>→<answer>)"
- **出处**: [GRIT][PDF p2] "such format reward encourages reasoning outputs structured by a thinking token pair (e.g., <think> and </think>) and a rethink token pair (e.g., <rethink> and </rethink>); it also rewards the inclusion of syntactically valid bounding boxes within the generated sequence."
- **说明**: 一致。

#### D56 P041 | 仅用 20 个图文问答三元组 — ✓ 一致

- **二稿**: "训练仅用 20 个图文问答三元组即触发基座模型的 grounded 推理能力"
- **出处**: [GRIT][PDF p1] "GRIT achieves exceptional data efficiency, requiring as few as 20 image-question-answer triplets from existing datasets";[PDF p2] "we train state-of-the-art MLLMs—Qwen 2.5-VL and InternVL 3 using only 20 image–question–answer triplets drawn from existing object-relation and counting VQA datasets, VSR and TallyQA."
- **说明**: 一致。

#### D57 P041 | GIoU 0.349→0.387 — ✓ 一致

- **二稿**: "加入计数奖励后 grounding 质量显著提升(GIoU 0.349→0.387)"
- **出处**: [GRIT][PDF p14 表] "GRIT 0.387 ... GRIT w/o counting data & reward 0.349"(GIoU 列,消融去掉计数数据与计数奖励后接地 IoU 降至 0.349)。
- **说明**: 一致。注意:0.349 是同时去掉计数训练数据与计数奖励的消融值,二稿表述"加入计数奖励后提升"成立,建议加"含计数训练数据"以更精确。

#### D58 表 4 R05 | 基座 Qwen2.5-VL-3B / InternVL3-2B — ✓ 一致

- **出处**: [GRIT][PDF p6] "We train two pre-trained MLLMs, Qwen2.5-VL-3B and InternVL-3-2B, directly using the GRIT method."
- **说明**: 一致。

#### D59 表 4 R05 | 评测基准"通用 VQA 与空间问答" — ✗ 需修正(E6)

- **二稿**: 表 4 GRIT 行评测基准列 "通用 VQA 与空间问答"
- **出处**: [GRIT][PDF p6] "GRIT-trained models are compared with baselines across seven testing sets on GPT-as-judge answer accuracy score (ACC) and grounding IoU (GIoU)";表 1 测试集:VSR、TallyQA、GQA、MathVista(-mini)、MME、OVDEval;[PDF p5] "MathVista-mini on mathematical reasoning in visual contexts, and position subset of OVDEval on open-vocabulary object grounding."
- **结论**: ✗ 不符。应改为 "**VSR/TallyQA/GQA/MathVista/MME/OVDEval(六数据集七测试集)**"。

#### D60 P041 | "奖励不约束框本身的质量" — ✓ 一致

- **二稿**: "bbox 终究只是'看哪儿'的粗略代理,奖励不约束框本身的质量"
- **出处**: [GRIT][PDF p5] "This reward component encourages the required format and presence of visual grounding elements without constraining the textual content or semantic accuracy of the grounded regions themselves."
- **说明**: 一致(点评有原文支撑)。

### 3.8 POLIA(3.2 节)

#### D61 P042 | 外在优势沿用 GRPO 组内归一化 — ✓ 一致

- **二稿**: "答案级外在优势 Aext 沿用 GRPO 的组内归一化"
- **出处**: [POLIA][PDF p2] "we compute an extrinsic advantage for each candidate answer following GRPO";[PDF p5 算法 1] "Compute weighted extrinsic rewards {R(ci)}; Normalize rewards to compute extrinsic advantages {Aext i }."
- **说明**: 一致。

#### D62 P042 | 内在优势:按置信度修正奖励后再组内归一化 — ✓ 一致

- **二稿**: "物体级内在优势 Aint 先在答案引用的物体集合上按置信度修正奖励,再在组内归一化"
- **出处**: [POLIA][PDF p2] "we broadcast the answer-level extrinsic rewards to each visual object with a correction based on its confidence. Then, we compute an intrinsic advantage for each visual object by comparing the corrected object-level rewards within the same visual object group."
- **说明**: 一致。

#### D63 公式 #(4)~(6) | ri,o = R(ci)·si,o 等三式 — ✓ 一致

- **二稿**: `ri,o=R(ci)·si,o`、`Aint=…组内归一化…`、`Ai=Aext+ωAint` #(4)~(6)
- **出处**: [POLIA][PDF p5] "We define the corrected object-level reward of each visual object as: ri,o = R(ci) · si,o";"We compute an intrinsic advantage Aint i,o for each object by comparing the ri,o within the same visual object group."
- **说明**: 一致(组内归一化形式与 GRPO 同构;ω 为内外优势融合系数,论文同节给出)。

#### D64 P044 | si,o 为 IoU 与归一化距离加权 — ✓ 一致

- **二稿**: "si,o 是预测框与真实物体匹配的置信度(IoU 与归一化距离加权)"
- **出处**: [POLIA][PDF p5] "si,o is derived from the matching quality between the predicted bounding box in ci and the ground-truth box of object o, computed as a weighted combination of IoU and normalized L1 distance, followed by clipping."
- **说明**: 一致。

#### D65 P044 | VSR 上 59.0→81.3 — ✓ 一致

- **二稿**: "在 VSR 上 POLIA 将基线 GRPO 的 59.0% 提升至 81.3%"
- **出处**: [POLIA][PDF p6 表] "Qwen2.5-VL+GRPO 59.0 ... POLIA 81.3"(VSR 列,7B 设置);[PDF p6] "For the 7B setting, we adopt Qwen2.5-VL-7B-Instruct as the base model."
- **说明**: 一致。

#### D66 P044 | "物体级打分仅占总训练时间的 0.0004%" — ✗ 需修正(E4)

- **二稿**: "物体级打分仅占总训练时间的 0.0004%"
- **出处**: [POLIA][PDF p8] "the Rollout phase is the dominant bottleneck, consuming 536.25 s (97.24%) of the total time";"the newly introduced components incur negligible overhead: the computation of Aint accounts for only 0.002 s, while Grouping is virtually instantaneous."
- **结论**: ✗ 无原文出处。原文只给绝对耗时(0.002 s)与 Rollout 占比(97.24%);"0.0004%"为自算值(0.002/536.25≈0.00037%,且分母口径不明确)。建议改为 "**Aint 计算仅耗时 0.002 s(Rollout 阶段占训练总时间 97.24%)**"。

#### D67 表 4 R06 | 基座 Qwen2.5-VL-7B — ✓ 一致

- **出处**: [POLIA][PDF p6] "For the 7B setting, we adopt Qwen2.5-VL-7B-Instruct as the base model."
- **说明**: 一致。

#### D68 表 4 R06 | 评测基准列 "VSR" — ⚠ 需注意(N6)

- **二稿**: 表 4 POLIA 行评测基准列 "VSR"
- **出处**: [POLIA][PDF p6] "We evaluate POLIA on seven widely used multimodal reasoning benchmarks: VSR, TallyQA, GQA, MathVista, MathVision, LogicVista, and MME."
- **结论**: ⚠ 单写 "VSR" 易被误读为仅在 VSR 上评测;代表性结果 59.0→81.3 确为 VSR 数字。建议改为 "**VSR 等 7 基准**"。

#### D69 P045 | 复用数据集物体标注 — ✓ 一致

- **二稿**: "POLIA 复用数据集物体标注"
- **出处**: [POLIA][PDF 附录] "POLIA is trained under a constrained object-level supervision setup, rather than relying on large-scale annotated data."(物体级标注来自数据集的 ground-truth 框)
- **说明**: 一致(使用目标级标注但非大规模)。

### 3.9 SAYO(3.2 节)

#### D70 P044 | 以区域级视觉注意力为奖励信号 — ✓ 一致

- **二稿**: "同方向的 SAYO [18] 以区域级视觉注意力作为奖励信号,把对齐对象从显式框推广到注意力分布"
- **出处**: [SAYO][PDF p1] "we propose SAYO, a visual reasoning model trained with a reinforcement learning (RL) framework that introduces a region-level visual attention–based reward."
- **说明**: 一致。

#### D71 P045 | 监督需求低的概括 — ✓ 一致

- **二稿**: "Ground-R1 无需框标注,GRIT 仅需 20 个问答三元组,POLIA 复用数据集物体标注"
- **出处**: 分见 D53/Ground-R1(奖励不含框监督)、D56/GRIT(20 三元组)、D69/POLIA(目标级标注)。各分项均一致;总体概括成立。

#### D72 P045 | "上述工作多在通用 VQA 与空间问答上验证" — ✗ 需修正(E7)

- **二稿**: "但上述工作多在通用 VQA 与空间问答上验证,显式组合基准上的覆盖仍然不足"
- **出处**: 与 E5/E6 同源:Ground-R1 评测含高分辨率(V*/HR-4K/HR-8K)与视觉接地(RefCOCO 系列,[PDF p6-7]);GRIT 评测含 VSR(空间关系)、OVDEval(接地, [PDF p6]);POLIA 含 VSR/GQA/TallyQA 等空间与物理感知基准([PDF p6])。这些均非"通用 VQA 与空间问答"可概括。
- **结论**: ✗ 概括失准(承接 E5/E6 的错误口径)。建议改为 "**在通用/高分辨率 LVLM 与接地、空间问答基准上验证,但显式组合基准(如 MMVP/Winoground/SugarCrepe)上的覆盖仍然不足**"。

### 3.10 VisualPRM(3.3 节)

#### D73 P047 | 8B 过程奖励模型 — ✓ 一致

- **二稿**: "VisualPRM [12] 训练 8B 过程奖励模型(学习式验证器)"
- **出处**: [VisualPRM][PDF p1] "We introduce VisualPRM, an advanced multimodal Process Reward Model (PRM) with 8B parameters."
- **说明**: 一致。

#### D74 P047 | 7 基准提升 3.7~8.9 个点 — ⚠ 需注意(N2)

- **二稿**: "在 7 个多模态推理基准上带来 3.7 ~ 8.9 个点提升"
- **出处**: [VisualPRM][PDF p2] "VisualPRM improves the overall reasoning performance of MiniCPM-V2.6, QwenVL2.5-7B, InternVL2.5-8B, and InternVL2.5-78B by 8.0, 3.7, 8.4, and 5.9 points, respectively, across seven multimodal reasoning benchmarks";[PDF p6 表 3] InternVL2.5-26B: 36.9→45.8(+8.9)。
- **结论**: ⚠ 范围跨来源混用:3.7 来自摘要(四模型口径下限),8.9 来自表 3(InternVL2.5-26B,摘要未纳入该模型)。若严格按摘要口径为 3.7~8.4。建议加注 "3.7~8.4 见摘要;8.9 为 InternVL2.5-26B(表 3)"。

#### D75 P047 | "将验证对象从最终答案迁移到推理步骤" — ✓ 一致

- **二稿**: "将验证对象从最终答案迁移到推理步骤"
- **出处**: [VisualPRM][PDF p2] "VisualProcessBench, a benchmark with human-annotated step-wise correctness labels, to measure the abilities of PRMs to detect erroneous steps";[PDF p1] "PRMs can serve as effective critic models for test-time scaling of MLLMs."
- **说明**: 一致(概括成立)。

#### D76 P047 | "步骤定义纯文本、无视觉锚定" — ⚠ 需注意(N3)

- **二稿**: "但其步骤定义纯文本、无视觉锚定,不覆盖组合绑定"
- **出处**: [VisualPRM] 全文检索 "visual anchor" 无命中。VisualPRM 的步骤来自问答的逐步解题文本链(VisualPRM400K,"a step-by-step solution, and correctness annotations for each step",[PDF p2]),步骤为文本形式。
- **结论**: ⚠ 无原文表述,属二稿推断(机制上成立:步骤确实是文本解链,未见视觉结构锚定)。建议标注"本文观察"以免被质疑无出处。

#### D77 P076 | 多模态 PRM 主要面向数学推理 — ⚠ 需注意(N2 附注)

- **二稿**: "多模态 PRM 主要面向数学推理"
- **出处**: [VisualPRM] 七个评测基准为 MMMU、MathVista、MathVision、MathVerse、DynaMath、WeMath、LogicVista([PDF p2,7])——其中 5 个为数学基准,MMMU 与 LogicVista 非纯数学。
- **结论**: ⚠ 总体成立(5/7 数学),但并非全部。可改"以数学推理为主"。

### 3.11 Self-Questioning(3.3 节)

#### D78 P048 | "子问题/子答案序列 + 最终答案"格式约束 — ✓ 一致

- **二稿**: "模型必须按'子问题/子答案序列 + 最终答案'输出"
- **出处**: [Self-Questioning][PDF p2] "We require the model to produce output in a structured format, alternating <sub q> (sub-question) and <sub a> (sub-answer) tags."
- **说明**: 一致。

#### D79 公式 #(7) | 二元奖励 +1/−1 — ✓ 一致

- **二稿**: `R(y,a∗)=+1 if Format(y)∧Correct(y,a∗), −1 otherwise` #(7)
- **出处**: [Self-Questioning][PDF p4] "R(y, a∗) = (1.0 if Format(y)∧Correct(y,a∗); −1.0 otherwise) (2)."
- **说明**: 一致(二稿 +1 对应原文 1.0)。

#### D80 P050 | 46.8 / 51.6 / 52.2 — ✓ 一致

- **二稿**: "A-OKVQA 上基座模型仅 46.8%,标准 RLVR 对照达 51.6%,而本方法达 52.2%"
- **出处**: [Self-Questioning][PDF p1] "both self-questioning and standard reinforcement learning substantially improve accuracy over the untrained model (52.2% and 51.6% vs. 46.8%)";[PDF p2] "RL raises A-OKVQA accuracy from 46.8% to 51.6%, with self-questioning providing only an additional gain of +0.6%, for an overall 52.2%";[PDF p6 表 2] Base 46.8 / Direct+GRPO 51.6 / SQ+GRPO 52.2。
- **说明**: 一致。

#### D81 P050 | 子问题质量故意不检查 — ✓ 一致(推断但准确)

- **二稿**: "子问题质量故意不检查。正是这种'不检查'逼出了分解行为"
- **出处**: [Self-Questioning][PDF p2] "we define a reward function that grants a score of 1.0 if and only if the model (a) produces output in the sub-question format... and (b) the final answer is correct"(奖励只检查格式与最终答案,不含子问题内容质量)。论文亦用 "self-questioning" 定位该设计。
- **说明**: 一致(奖励函数定义支持该解读)。

#### D82 P050 | "标准 RLVR 对照" — ✓ 一致

- **二稿**: "标准 RLVR 对照达 51.6%"
- **出处**: [Self-Questioning][PDF p4] "Baseline: Direct RLVR To isolate the specific effect of self-questioning... this baseline... represents standard reinforcement learning from verifiable rewards (RLVR) applied to visual question answering."
- **说明**: 一致(Self-Questioning 论文自身使用 RLVR 术语)。

#### D83 表 4 R07 | 基座 Qwen2.5-VL-3B — ✓ 一致

- **出处**: [Self-Questioning][PDF p2] "Our base model is Qwen2.5-VL-3B-Instruct."
- **说明**: 一致。

### 3.12 H-GRPO(3.3 节)

#### D84 P051 | 三元组结构 τi=⟨qi,ai,bi⟩ — ✓ 一致

- **二稿**: "把推理结构化为'(子问题,子答案,证据框)'三元组序列"
- **出处**: [H-GRPO][PDF p1] "the VLM decomposes the reasoning into a sequence of triplets τi = ⟨qi, ai, bi⟩, where each triplet contains a sub-question, intermediate answer, and supporting spatial evidence."
- **说明**: 一致。

#### D85 P051 | 匈牙利二分图匹配 — ✓ 一致

- **二稿**: "预测与参考三元组经匈牙利二分图匹配"
- **出处**: [H-GRPO][PDF p3] "aligns predicted and reference reasoning steps through bipartite matching";[PDF p5] "We then solve a bipartite matching problem."
- **说明**: 一致。

#### D86 公式 #(8) | Sij 四分量均值 — ✓ 一致

- **二稿**: `Sij=¼[E(bi,bj*)+simq(qi,qj*)+sima(ai,aj*)+IoU(bi,bj*)]` #(8)
- **出处**: [H-GRPO][PDF p5] "Sij = 1/4 [E(b̂i, b∗j) + simq(q̂i, q∗j) + sima(âi, a∗j) + IoU(b̂i, b∗j)]";"E(b̂i, b∗j) measures whether the predicted bounding box exists and is compatible with the reference evidence region, simq and sima are Sentence-BERT cosine similarities... and IoU... measures the spatial overlap."
- **说明**: 一致。

#### D87 公式 #(9) | R = αRfmt + βRans·RHS — ✓ 一致

- **二稿**: `R=αRfmt+βRans·RHS` #(9)
- **出处**: [H-GRPO][PDF p6] "We define the overall reward as R = αRformat + βRanswer · RHS, (1)";[PDF p7] "Hungarian Reasoning Reward. We convert the Hungarian matching score into a dense process-level reward: RHS = max(0, SHS − γ)."
- **说明**: 一致。

#### D88 P055 | 门控机制解读 — ✓ 一致

- **二稿**: "光答对但中间步骤与证据 grounding 不到位,奖励即被门控,从而抑制'忽略图像仅凭文本脑补'的捷径"
- **出处**: [H-GRPO][PDF p6] "This formulation conditions the final answer reward on the Hungarian reward. As a result, the model receives strong reward only when it produces the correct answer through sufficiently grounded and well-aligned intermediate reasoning";[PDF p2] "A model may produce the correct answer while relying on spurious correlations, ignoring relevant visual evidence."
- **说明**: 一致。

#### D89 P055 | GRPO 是 H-GRPO 对角匹配特例 — ✓ 一致

- **二稿**: "数学上,GRPO 是 H-GRPO 对角匹配的特例"
- **出处**: [H-GRPO][PDF p3] "It should be noted that GRPO is a special case of H-GRPO where the diagonal matching of H-GRPO reduces to GRPO."
- **说明**: 一致。

#### D90 P055 | SmolVLM-2.2B A-OKVQA 73.4% — ✓ 一致

- **二稿**: "小模型受益最大(SmolVLM-2.2B 在 A-OKVQA 达 73.4%)"
- **出处**: [H-GRPO][PDF p8 表 1] "SmolVLM-2.2B 71.1 / GRPO (SmolVLM-2.2B) 71.7 / H-GRPO (SmolVLM-2.2B) 73.4";[PDF p8] "vanilla GRPO gives only marginal or unstable gains. In contrast, H-GRPO achieves the best results for this backbone, improving to 73.4% on A-OKVQA and 77.2% on Visual7W. This suggests that sparse final-answer rewards are insufficient for smaller VLMs."
- **说明**: 一致。补充:Qwen2.5-VL-3B 上 H-GRPO(82.8)略低于 GRPO(83.4),故"小模型受益最大"成立。

#### D91 P055 | "参考推理链的质量决定奖励上限" — ⚠ 点评性表述

- **二稿**: "但参考推理链的质量决定奖励上限"
- **出处**: [H-GRPO][PDF p7] GVRS 参考链经人工验证("We manually validate the quality of the generated traces using three expert annotators on a random subset of 100 examples");奖励依赖与参考链的匹配(Sij/RHS)。
- **结论**: ⚠ 合理推断(奖励构造依赖参考链,参考链经人工验证),非原文原话。可保留,建议不加引号式断言。

#### D92 表 4 R08 | 评测基准 "A-OKVQA 与自建 OOD 基准" — ✗ 需修正(E8)

- **二稿**: 表 4 H-GRPO 行评测基准列 "A-OKVQA 与自建 OOD 基准"
- **出处**: [H-GRPO][PDF p8] "For in-domain evaluation, we use the standard evaluation splits of A-OKVQA and Visual7W";"For out-of-distribution evaluation, we use MMMU, RealWorldQA, RoboSpatial, and MMStar."(均为既有公开基准)
- **结论**: ✗ "自建"失准。自建的是训练集 GVRS([PDF p7] "GVRS is constructed from four sources: Visual7W, Visual-CoT, A-OKVQA, and ERQA"),OOD 评测用的是既有标准基准。应改为 "**A-OKVQA/Visual7W 与 OOD 基准(MMMU/RealWorldQA/RoboSpatial/MMStar)**"。

### 3.13 MM-CondChain(第 4 节)

#### D93 P069 | 程序化验证范式 — ✓ 一致

- **二稿**: "用可执行程序把多层组合条件构造出来并机械验证"
- **出处**: [MM-CondChain][PDF p4] "we apply programmatic verification during benchmark construction, not evaluation... we verify the semantic correctness of generated conditions by executing predicates against extracted visual facts";[PDF p1] "the ground truth is mechanically verified via code execution"(表 3 中 "Prog. Verif." 列)。
- **说明**: 一致。

#### D94 P069 | "975 道题由程序化管线生成并机械验证" — ⚠ 需注意(N5)

- **二稿**: "其 975 道题由程序化管线生成并机械验证"
- **出处**: [MM-CondChain][PDF p9] "This results in 975 evaluation samples in total, each containing a paired True-path and False-path instance";[PDF p10] 总数据集 "Total 4634"。
- **结论**: ⚠ "975"是**评估样本数**(每样本含 True-path/False-path 一对),并非全部题目;总数据集为 4,634。建议改为 "**975 个评估样本**"。

#### D95 P069 | 最强模型仅 53.33 Path F1 — ✓ 一致

- **二稿**: "最强模型也仅得 53.33 分(Path F1)"
- **出处**: [MM-CondChain][PDF p1] "even the strongest model attains only 53.33 Path F1";[PDF p11] "Gemini-3-Pro achieves the best overall result with 53.33 average Path F1."
- **说明**: 一致(53.33 为 Gemini-3-Pro 三域平均 Path F1)。

#### D96 P069 | 评分全可复现 — ✓ 一致

- **二稿**: "评分全可复现"
- **出处**: [MM-CondChain][PDF p3 表] "Determ.: deterministic evaluation without LLM-as-judge";[PDF p1] "programmatic verification framework... mechanically verifiable."
- **说明**: 一致(确定性程序化判定)。

### 3.14 AlphaGRPO 与 FActScore(第 5 节)

#### D97 P075 | AlphaGRPO DVReward 分解机制 — ✓ 一致(证据:Web 检索)

- **二稿**: "AlphaGRPO 的 DVReward 将复杂请求分解为原子化可验证子问题,再由通用 MLLM 逐项评估 [22]"
- **出处**: 本地无 PDF,经 WebSearch + arXiv HTML 全文核实(arXiv:2605.12495): "Decompositional Verifiable Reward (DVReward)... decomposes user prompts into atomic verifiable questions across both semantic alignment and visual fidelity... indicate the correct way to use MLLM as the reward model."
- **结论**: ✓ 一致。**证据强度:B(网络检索)**,建议文末或引用处标注该文献经 arXiv HTML 核实。

#### D98 P075 | FActScore 原子事实分解 — ✓ 一致

- **二稿**: "文本事实核查已有先例(FactScore 的原子事实分解 [23])"
- **出处**: [FActScore][PDF p1] "we introduce FACTSCORE, a new evaluation that breaks a generation into a series of atomic facts and computes the percentage of atomic facts supported by a reliable knowledge source."
- **说明**: 一致。

### 3.15 表 4 注与其余论述性引用

#### D99 表 4 注 | "提升/超出均指绝对百分点" — ⚠ 需注意(N7)

- **二稿**: 表 4 注 "表中数值均为论文报告值;'提升''超出'均指绝对百分点"
- **逐条核对**: CR³ +10.0/+9.3(表 3,绝对)✓;SpatialThinker +4.7(14 基准平均差值)✓;SVQA-R1 +30.7(27.72→58.42 绝对差值)✓(口径见 N1);Ground-R1 +2.1/+1.2(绝对)✓;POLIA 59.0→81.3(绝对)✓;GRIT GIoU 0.349→0.387 为 IoU 差值(表注已单列 "GIoU 为接地 IoU")✓。
- **结论**: ⚠ 总体成立。唯一需留意:SVQA-R1 摘要原文 "more than 30%" 未明说绝对/相对,但表 3 数值支持绝对口径(+30.7pp)。

#### D100 P071 | "Ground-R1 在通用与高分辨率基准上验证" — ✓ 一致

- **出处**: [Ground-R1][PDF p1] "Experimental results on general LVLM, high-resolution, and visual grounding benchmarks."
- **说明**: 一致(与 E5 修正后口径一致)。

#### D101 P071 | POLIA 通用 VQA 与空间问答 — ✓ 一致

- **出处**: [POLIA][PDF p6] 7 基准(VSR/TallyQA/GQA/MathVista/MathVision/LogicVista/MME)确属通用多模态推理与空间/物理感知类。
- **说明**: 一致。

#### D102 P073 | H-GRPO 动机为文本捷径 — ✓ 一致

- **二稿**: "H-GRPO 的动机正是'忽略图像仅凭文本也能得分'的捷径 [20]"
- **出处**: [H-GRPO][PDF p2] "A model may produce the correct answer while relying on spurious correlations, ignoring relevant visual evidence, or hallucinating intermediate facts."
- **说明**: 一致。

#### D103 P073 | Ground-R1 无框监督可行但"看对地方"无法直接验证 — ✓ 一致(点评)

- **二稿**: "Ground-R1 证明了无框监督的可行性,但代价是'看对地方'无法被直接验证"
- **出处**: [Ground-R1] 训练奖励为格式+答案(无框 IoU 奖励,见 D53);论文自述免逐步监督([PDF p1] "without step-wise supervision")。
- **说明**: 一致(机制与论文定位相符,属合理点评)。

---

## 4. 需修正清单(E1~E8)与修正建议文本

### E1 公式 #(3)门控位置错误(重要)

- **位置**: P034 公式 #(3)
- **二稿现文**: `Rtotal = 1[Rfmt=1](wfRf + wcRc + waRa·1[Ra=1] + wsRs)`
- **原文**: [SpatialThinker][PDF p5 公式 (3)] `Rtotal = I[Rformat=1]·(wformatRf + wcountRc + waccuracyRa·I[Raccuracy=1] + wspatialRs)`,权重 wformat=0.1、wcount=0.2、waccuracy=0.5、wspatial=0.2;正文 "we compute the spatial reward only when the final answer is correct"。
- **修正建议**: 门控 `1[Ra=1]` 应移到空间分量前,公式改为:
  `Rtotal = 1[Rfmt=1](wfRf + wcRc + waRa + 1[Ra=1]·wsRs)`
- 注意:正文文字("空间奖励仅在答案正确时生效,防止模型为刷结构分而牺牲最终答案")是正确的,无需改动;仅公式书写有误。

### E2 VALSE 表 1 规模错误

- **位置**: 表 1 R01 VALSE 行规模列
- **二稿现文**: "851 例"
- **原文**: [VALSE][PDF p3 表 1] 存在 505 + 复数 851 + 计数 2,459 + 空间关系 535 + 动作 1,633 + 共指 812 = **6,795 例**
- **修正建议**: "6,795 例(851 为复数子集规模)"

### E3 VALSE 表 1 关键发现失准

- **位置**: 表 1 R01 VALSE 行关键发现列
- **二稿现文**: "空间关系、共指最弱"
- **原文**: [VALSE][PDF p8 表 2] 最佳模型 ViLBERT 12-in-1 各子任务准确率:存在 95.6、共指 86.9、空间关系 75.7、动作 69.2、计数 58.9(最低);结论 "identify named objects and their presence in images well (existence), but struggle to ground their interdependence and relationships"
- **修正建议**: "计数与动作最弱"或"存在性强、关系/计数绑定弱"

### E4 POLIA "0.0004%" 无出处

- **位置**: P044
- **二稿现文**: "物体级打分仅占总训练时间的 0.0004%"
- **原文**: [POLIA][PDF p8] "the computation of Aint accounts for only 0.002 s";"the Rollout phase is the dominant bottleneck, consuming 536.25 s (97.24%) of the total time"
- **修正建议**: "Aint 计算仅耗时 0.002 s(而 Rollout 阶段占训练总时间的 97.24%),开销可忽略"

### E5 表 4 Ground-R1 评测基准不符

- **位置**: 表 4 R04
- **二稿现文**: "通用 VQA 与空间问答"
- **原文**: [Ground-R1][PDF p1] "general LVLM, high-resolution, and visual grounding benchmarks";表 1/3:MME、MM-Vet、SEED、MME-RWL、RWQA、POPE、V∗、HR-4K、HR-8K + RefCOCO 系列/Visual Search(4.3 节)
- **修正建议**: "通用 LVLM(MME/MM-Vet/SEED/MME-RWL/RWQA/POPE)+ 高分辨率(V*/HR-4K/HR-8K)+ 视觉接地"

### E6 表 4 GRIT 评测基准不符

- **位置**: 表 4 R05
- **二稿现文**: "通用 VQA 与空间问答"
- **原文**: [GRIT][PDF p6] "across seven testing sets";VSR、TallyQA、GQA、MathVista(-mini)、MME、OVDEval
- **修正建议**: "VSR/TallyQA/GQA/MathVista/MME/OVDEval(七测试集)"

### E7 P045 节内小结概括不全

- **位置**: P045
- **二稿现文**: "但上述工作多在通用 VQA 与空间问答上验证,显式组合基准上的覆盖仍然不足"
- **修正建议**: "上述工作多在通用/高分辨率 LVLM 与接地、空间问答基准上验证,显式组合基准(如 MMVP、Winoground、SugarCrepe)上的覆盖仍然不足"

### E8 表 4 H-GRPO "自建 OOD 基准"失准

- **位置**: 表 4 R08
- **二稿现文**: "A-OKVQA 与自建 OOD 基准"
- **原文**: [H-GRPO][PDF p8] in-domain = A-OKVQA/Visual7W;OOD = MMMU、RealWorldQA、RoboSpatial、MMStar(均为既有基准);自建的是训练集 GVRS
- **修正建议**: "A-OKVQA/Visual7W 与 OOD 基准(MMMU/RealWorldQA/RoboSpatial/MMStar)"

---

## 5. 需注意清单(N1~N7,不必改数、建议加注)

| 编号 | 位置 | 问题 | 建议 |
|---|---|---|---|
| N1 | P036/表 4 SVQA-R1 | "较 SFT 超 30 个百分点"对应 SFT(CoT) 基线 27.72→58.42(+30.7);对照普通 SFT 37.62 仅 +20.8 | 注 "相对 SFT(CoT) 基线" |
| N2 | P047 VisualPRM | "3.7~8.9"跨来源:3.7~8.4 出自摘要,8.9 出自表 3(InternVL2.5-26B) | 注来源或改 "3.7~8.4" |
| N3 | P047 VisualPRM | "步骤定义纯文本、无视觉锚定"无原文表述,为本文推断 | 标 "本文观察" |
| N4 | P023 DeepSeekMath | 原文无 "RLVR" 术语(用 Rule/Model 二分);RLVR 术语出自 DeepSeek-R1 | 加注术语出处 |
| N5 | P069 MM-CondChain | "975 道题"应为 "975 个评估样本"(总数据集 4,634) | 改表述 |
| N6 | 表 4 POLIA | 评测基准列仅写 "VSR",实际 7 基准 | 改 "VSR 等 7 基准" |
| N7 | 表 4 注 | "提升/超出均指绝对百分点"总体成立;SVQA-R1 摘要原文未明说绝对/相对(数值支持绝对) | 保持,可加 "SVQA-R1 按绝对百分点计" |

---

## 6. 证据强度标注

| 强度 | 定义 | 涉及条目 |
|---|---|---|
| A | 论文 PDF 原文直接支持(页码 + 摘录) | 绝大多数条目 |
| B | 本地无 PDF,经 Web 检索/arXiv HTML 核实 | D97(AlphaGRPO) |
| C | 二稿自行推断/自算,原文无对应表述 | E4(0.0004%)、N3(纯文本步骤)、D53(无需框标注,机制成立)、D18(物体>属性>关系) |

**说明**:
1. 全部 27 篇 PDF 均完成全文检索;除 AlphaGRPO 外,所有结论均以 PDF 原文为据。
2. E4 的 0.0004% 为自算值,且原文无"占比"表述,已列入修正。
3. N3/D18 等推断性表述不构成数据错误,但建议在正文以"本文观察/综合各基准结论"的口径呈现,避免审稿质疑。

---

*报告完*
