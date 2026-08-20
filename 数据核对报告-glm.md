# 数据核对报告 2

**核对对象**：《多模态大语言模型组合推理中的强化学习方法：奖励信号的演进》（二稿.docx，2026-08-19 版本）
**核对依据**：工作区 `papers/` 目录下 27 篇论文 PDF 原文（以 PDF 提取文本逐条检索定位）；PDF 不含的信息（AlphaGRPO、RLVR 术语来源、Silkie 出处、SpatialThinker/SVQA-R1 会议性质）以网络检索结果为准。
**独立性声明**：本报告全程独立完成，未参考《数据核对报告.md》。
**结论标记**：✅ 相符 | ⚠️ 有出入（建议修改或加注） | ❌ 不符（建议更正） | ❓ 无法核实

---

## 一、总体结论

二稿数据总体质量很高：共核对 **68 项**可验证的数据性陈述，**60 项与原文完全相符**。发现：

- **2 处实质性错误**（❌）：
  1. 2.2 节"RLVR 术语出自 DeepSeek-R1"——术语实际出自 Ai2 的 **Tülu 3**（2024.11），DeepSeek-R1（2025.1）只是使其广为人知；
  2. 表 1 VALSE 行"计数与动作最弱"——VALSE 原文明确说最佳模型在 Counting 上表现"well"，最弱的是动作、复数、共指；"计数最弱"与原文相悖。
- **2 处会议引用不精确**（⚠️）：SpatialThinker 实为 NeurIPS 2025 **Workshops** 论文；SVQA-R1 实为 ICLR 2026 **Workshop**（ES-Reasoning）论文，均非主会议。
- **6 处轻微出入**（⚠️）：详见第四节修改建议。

---

## 二、逐项核对明细

### 2.1 第 1 节 引言 & 第 2.1 节 评测基准（含表 1）

| # | 二稿表述 | 原文出处与摘录 | 结论 |
|---|---------|---------------|------|
| 1 | CREPE 发现组合理解随组合复杂度增加而显著退化 | CREPE 摘要："For productivity, models' retrieval success **decays as complexity increases**, frequently nearing random chance at high complexity." | ✅ |
| 2 | ARO 指出 VLM 本质上像"词袋模型" | ARO 摘要："We present the settings in which state-of-the-art VLMs **behave like bags-of-words**" | ✅ |
| 3 | SugarCrepe：纯绑定测试（Swap）是所有模型的薄弱环节 | SugarCrepe §5.3："**All models struggle at identifying SWAP hard negatives**, regardless of their pertaining dataset and model size... SWAP hard negatives present the biggest challenge" | ✅ |
| 4 | ARO shortcut 分析：对比预训练目标不要求理解组合结构，模型凭词频与整体语义即可高分 | ARO §1/§4："it is possible to perform well on image-text retrieval over existing datasets **without using the composition and order information**"；"not learning the order information is a **valid shortcut**" | ✅ |
| 5 | CREPE：组合性缺陷与模型规模无关 | CREPE 摘要末句："These results **hold regardless of model and training dataset size**."；§5.3 "Effect of model size"；引言 "fifth, model size also has no [effect]" | ✅ |
| 6 | CR³ 较原始基线平均提升超 9 个绝对点 | CR³ §4.3："boosts the average compositional performance of Qwen2.5-VL-7B and InternVL3-8B **by 10 absolute points**"；按 Table 3 实算：7B 47.2→57.2（+10.0）、8B 48.8→58.1（+9.3），均值 +9.65 | ⚠️ "超 9 点"与 Table 3 计算吻合，但论文正文自述为"10 absolute points"，二者表述不一致，建议统一为"约 10 个绝对点"或注明按表计算 |
| 7 | 表1 VALSE 规模 **6,795 例** | VALSE Table 1（Overview of pieces）六项之和：505+851+2,459+535+1,633+812 = **6,795** | ✅（总值为分项求和，论文未直接给出总数） |
| 8 | 表1 VALSE 子任务"存在/复数/计数/空间关系/动作/共指" | VALSE 摘要贡献 iii)："existence, plurality, counting, spatial relations, actions, and entity coreference" | ✅ |
| 9 | 表1 VALSE 评测方式"真假判断（foiled instances）" | VALSE 摘要："a model is asked to **distinguish real captions from foils**" | ✅ |
| 10 | 表1 VALSE 关键发现"**计数与动作最弱**；存在性强、关系绑定弱" | VALSE §5.3：最佳模型 ViLBERT 12-in-1 "**performs strongly on existence, well on counting**, but struggles on **plurality, spatial relations, coreference, and actions**"；Table 2 该模型 acc_r：Existence 95.6（最高）、Counting 76.7/80.2（中上）、actant swap 58.9（最低）、plurality 72.4 | ❌ "动作最弱"成立，但"**计数最弱**不成立"——原文明确称 counting 表现"well"。建议改为"**动作与复数/共指最弱**；存在性强、关系绑定弱" |
| 11 | 表1 CREPE"系统性/生产力；检索（seen-unseen splits + 复杂度梯度）；37 万级" | CREPE 摘要："measures two important aspects... **systematicity and productivity**"；"test dataset containing **over 370K** image-text pairs and **three different seen-unseen splits**"；productivity 为 "17K image-text pairs with **nine different complexities**" | ✅（37 万级指 systematicity 部分，表述合理） |
| 12 | 表1 ARO"属性/关系/词序；检索；5 万级" | ARO 摘要："Visual Genome **Attribution**... Visual Genome **Relation**... COCO-Order & Flickr30k-**Order**... with **more than 50,000** test cases" | ✅ |
| 13 | 表1 ARO 关键发现"词袋模型；存在 shortcut" | ARO 摘要（词袋，见 #2）；§4："ARO dataset (50,000 test cases)"，shortcut 论述见 #4 | ✅ |
| 14 | 表1 SugarCrepe 规模"**7.5 千级**" | SugarCrepe §4 Dataset overview："The final evaluation set of SUGARCREPE consists of **7512 examples**" | ✅ |
| 15 | 表1 SugarCrepe 子任务"物体/属性/关系 × Replace/Swap/Add" | SugarCrepe §4：REPLACE 分 OBJ/ATT/REL，**SWAP 仅分 OBJ/ATT**（"omit swapping two relationships"），**ADD 仅分 OBJ/ATT** | ⚠️ 完整笛卡尔积不成立（Swap 与 Add 无"关系"子类），建议表述为"Replace(物/属/关系)、Swap(物/属)、Add(物/属)"或加注 |
| 16 | 表1 SugarCrepe"Swap 最难；物体 > 属性 > 关系" | SugarCrepe §5.3："lower performances on attributes/relations compared to objects"；Table 6（如 OpenAI RN50：Replace-Obj 91.77 > Replace-Att 80.58 > Replace-Rel 69.99）；Swap 最难见 #3 | ✅ |
| 17 | 表1 SugarCrepe 评测方式"二选一检索" | SugarCrepe §4："Each example is an image-to-text retrieval task composed of an image, a positive text, and **a** hard negative. ...random chance performance has an average accuracy of 50%." | ✅ |
| 18 | SugarCrepe"用 LLM 生成语义合理的困难负样本" | SugarCrepe 摘要："We employ **large language models**, instead of rule-based templates... to generate **fluent and sensical hard negatives**" | ✅ |
| 19 | 2.1 节"物体识别强于属性绑定，属性强于关系理解，纯粹的绑定（Swap）最难（综合多基准结论）" | SugarCrepe §5.3（见 #16）+ ARO（Attribution 高于 Relation、Order 接近随机）综合 | ✅（已标注"综合结论"，合法） |

### 2.2 第 2.2 节 RL 基础与奖励信号演进

| # | 二稿表述 | 原文出处与摘录 | 结论 |
|---|---------|---------------|------|
| 20 | DeepSeekMath 提出的 GRPO 去除了 PPO 的价值网络，对同一问题采样多个回答，用组内相对优势替代 critic 打分 | DeepSeekMath §2.2.1："**GRPO foregoes the critic model**, instead estimating the baseline from **group scores**" | ✅ |
| 21 | GRPO 配合确定性规则验证器提供奖励 | DeepSeekMath（RL 阶段采用 rule-based/answer-checking reward，论文 §2.2.1 论述 outcome reward 由答案正确性判定） | ✅ |
| 22 | RLVR"**术语出自 DeepSeek-R1**" | 网络核实（reinforcement-learning.com 知识库、aiwiki、LeetLLM 等多个来源一致）：**RLVR 术语由 Ai2 的 Tülu 3（Lambert et al., 2024.11, arXiv:2411.15124）提出**；"Tulu 3 coins 'RLVR'"；DeepSeek-R1（2025.1）在标签"rule-based rewards"下使用同一思想并使其广为人知 | ❌ 建议改为"术语出自 Tülu 3，经 DeepSeek-R1 发扬光大"，或删去括注 |
| 23 | DPO 以离线偏好对为原料、无需显式奖励模型；偏好对来自固定采样分布，不随策略迭代更新 | DPO §1："in learning from human preferences, we typically learn from a **fixed batch of offline preference-annotated action pairs**"；DPO 全文基于离线偏好数据集直接优化 | ✅ |
| 24 | GRPO 与 PRM 等价："在 token 级策略梯度与单次更新的设定下，标准 GRPO 目标与 PRM-aware 目标数学等价" | GRPO-is-secretly-a-PRM 摘要："GRPO... equipped with an ORM is **in fact equivalent to a PRM-aware RL objective**... (given mild assumptions)"；§2 两条假设原文："first, we assume the use of the **DAPO token-level policy gradient** objective... Second... **µ is set to µ = 1 update iteration per batch**"——与"token 级策略梯度 + 单次更新"逐字对应 | ✅ |
| 25 | 组内多条回答的共享前缀天然定义了"过程步骤" | 同上论文 §1："GRPO assigns step-level rewards... **whenever subsets of trajectories within each group share identical prefixes**" | ✅ |
| 26 | VisualPRM 等工作已将 PRM 扩展到多模态推理 | VisualPRM 摘要："an advanced **multimodal Process Reward Model (PRM) with 8B parameters**" | ✅ |
| 27 | LLaVA-RLHF、RLHF-V、Silkie 确立"奖励来自对回答的评判"，反馈粒度停留在回答整体或语言片段 | LLaVA-RLHF（奖励模型对回答整体打分，factually augmented）；RLHF-V（标题即 "Fine-grained **Correctional** Human Feedback"，片段级）；Silkie/VLFeedback（GPT-4V 按帮助性/视觉忠实性/伦理对回答评分） | ✅（定性归纳，与三篇论文定位一致） |

### 2.3 第 3.1 节 验证器奖励（含表 3、表 4 对应行）

| # | 二稿表述 | 原文出处与摘录 | 结论 |
|---|---------|---------------|------|
| 28 | CR³ 构造三个图文匹配任务 TG-VCR、VG-TCR、CITM，回答正误由确定性规则判定 | CR³ §3.3："three distinct yet complementary tasks... (TG-VCR)... (VG-TCR)... Compositional Image-Text Matching (CITM)"；§3.1 "rule-based reward functions" | ✅ |
| 29 | CR³ 奖励由答案正确与推理顺序两个二元分量构成；答案分量完全一致取 1；顺序分量在"先\<think\>后\<answer\>"格式正确时取 1 | CR³ §3.1："**Accuracy reward** r_acc: ...If they match identically, it returns a reward [of 1]... **Format reward** r_format: verifies [the output] ...</think> ... </answer> tags. The reward score is 1 only when..."（二者加权组合，权重 λ） | ✅（"推理顺序分量"即 format reward，描述一致） |
| 30 | CR³ 数据工序：语义与视觉双重筛选构造高难度负样本（**18.5 万→1.89 万**） | CR³ §3.2："We first randomly sample **185,000** instances... **Textual Filtering** (SBERT, threshold 0.7)... **Visual Filtering** (DINOv2, threshold 0.75)... discards approximately 90%... yielding a condensed, high-quality dataset of **18,900** instances" | ✅ |
| 31 | CR³ 基座 Qwen2.5-VL-7B 与 InternVL3-8B；无 SFT 常见的领域外退化 | CR³ Table 3（Qwen2.5-VL-7B、InternVL3-8B 均有 +CR3 行）；§4.4："standard SFT approaches... **exhibit performance degradation** across these diverse tasks [而 CR³ 一致提升]" | ✅ |
| 32 | 表4 CR³：评测 MMVP/Winoground/Cola；较 SFT 超 5 点 | CR³ §4.2 三个 in-domain 基准即 MMVP、Winoground、Cola；§4.3："an absolute average improvement of **over 5 points** compared to SFT-based method" | ✅ |
| 33 | SpatialThinker 输出模板"观察→场景图→推理→答案" | SpatialThinker §3.1："a visually-grounded and structured reasoning template: **\<observe\>** for scene description, **\<scene\>** for regional scene graphs..., **\<think\>** for explicit reasoning, and **\<answer\>** for the final output" | ✅ |
| 34 | SpatialThinker 奖励由格式、计数、准确率、空间四个分量经字典序门控组合；格式分量是硬门槛；空间奖励仅在答案正确时生效 | SpatialThinker §3.1："our dense reward design combines **lexicographic gating** with **four components—format, count, accuracy, and spatial rewards**"；"Spatial Reward. To supervise object localization, we compute the spatial reward **only when the final answer is correct**" | ✅ |
| 35 | SpatialThinker 7B 在 **14 个基准**上平均超越 GPT-4o **4.7 个百分点** | SpatialThinker 摘要："SpatialThinker-7B... **surpassing GPT-4o (+4.7% avg.)**... across **fourteen benchmarks**"（§4.1：14 = 8 spatial + 6 real-world VQA） | ✅ |
| 36 | SpatialThinker STVQA-7K 基于 Visual Genome 人工标注构建，框标注质量决定空间分量可靠性 | SpatialThinker §3.3："STVQA-7K, a synthetic visual question answering (VQA) dataset built from **human-annotated scene graphs in Visual Genome**" | ✅（见 #48 关于"7K 人工标注"表述的提醒） |
| 37 | SVQA-R1 将图像镜像翻转并用 GPT-4o 生成翻转后逻辑一致的问答对，要求对原图与翻转图给出语义一致的答案 | SVQA-R1 §3.1："we construct **horizontally flipped** image samples..."; "we employ **GPT-4o** to automatically generate revised QA pairs for each flipped [image]"；摘要："constructs view-consistent rewards by perturbing spatial relations between objects, e.g., **mirror flipping**" | ✅ |
| 38 | SVQA-R1 奖励为格式与语义两个分量加权 | SVQA-R1 §3.2："Format Reward r_f... a binary signal..."；"Semantic-aware Reward r_s... Sentence-BERT-based reward..."；"Final Reward. **The total reward is defined as a weighted sum** of all components" | ✅ |
| 39 | SVQA-R1 3B 模型在 Q-Spatial++ 上较 SFT(CoT) 基线提升超 30 个百分点（**27.72→58.42**） | SVQA-R1 摘要："improve the accuracy over the SFT-based baseline by **more than 30%** on the Q-Spatial++ benchmark"；Table 3：SFT(CoT) **27.72** → SVQA-R1 **58.42**；模型基座 Qwen2.5-VL-3B | ✅ |

### 2.4 第 3.2 节 视觉对齐奖励（含表 3、表 4 对应行）

| # | 二稿表述 | 原文出处与摘录 | 结论 |
|---|---------|---------------|------|
| 40 | Ground-R1 训练奖励仅含格式与答案验证，证据框由模型自生成；两阶段 rollout（先输出证据框、再基于裁剪局部图像作答） | Ground-R1 §3 图 3："**The grounding phase** analyzes input instructions and generates evidence region rollouts... **The answering phase** takes the input image, question, and the generated evidence regions as input"；§3（intra-bin reward）："a **format reward** which ensures that the responses conform to the desired format and an **answer reward** which evaluates the correctness of the final prediction" | ✅ |
| 41 | Ground-R1 诊断出标准 GRPO 全局归一化偏袒大而显著的证据区域，小证据获得持续负优势 | Ground-R1 §1（图 2 分析）："the large evidence regions **consistently receive higher rewards** than medium and small ones... This leads to **consistently negative advantages for small regions**... causing their gradients to be suppressed or even clipped" | ✅ |
| 42 | SRPO 按区域面积分箱做桶内/桶间归一化，较标准 GRPO 在 V\* 与 HR-4K 上分别提升 **2.1 与 1.2 个百分点** | Ground-R1 摘要："through **scale-aware binning and intra-/inter-bin comparisons**"（§1：分箱阈值 <10%、10–30%、>30%）；§4 Q3："SRPO brings substantial gains on high-resolution benchmarks, achieving an improvement of **+2.1% on V\***, **+1.2% on HR-4K**, and +1.8% on HR-8K"（vs Ground-R1-GRPO，Table 3 实算 87.4−85.3=2.1、75.0−73.8=1.2） | ✅ |
| 43 | 表4 Ground-R1 基座 Qwen2.5-VL-7B；评测"通用 LVLM + 高分辨率 + 接地" | Ground-R1 §4 Table 1 基线为 Qwen2.5-VL-7B；摘要："Experimental results on **general LVLM, high-resolution, and visual grounding benchmarks**" | ✅ |
| 44 | GRIT 包围框坐标内嵌思维链（\<think\>→\<rethink\>→\<answer\>），训练仅用 **20 个图文问答三元组** | GRIT 摘要图 1："Grounded reasoning achieved with **20 training data samples** (ours)"；§3.2：格式奖励检查 "\<think\>...\</think\> then \<rethink\>...\</rethink\>" + 有效包围框；消融 "trained with **20 VSR** without counting reward" | ⚠️ 数值与结构相符；"三元组"系作者措辞（原文为 20 个 VQA 样本，可理解为"图-问-答"三元组），建议写"20 个图文问答样本"更贴近原文 |
| 45 | GRIT 加入计数奖励后 grounding 质量显著提升（**GIoU 0.349→0.387**） | GRIT Table 3（消融）："GRIT **0.387**..."；"GRIT w/o counting data & reward **0.349**..." | ✅ |
| 46 | 表4 GRIT 基座 Qwen2.5-VL-3B / InternVL3-2B；VSR/TallyQA/GQA/MathVista/MME/OVDEval（六数据集七测试集） | GRIT §4.1："We train two pre-trained MLLMs, **Qwen2.5-VL-3B and InternVL-3-2B**"；Table 1 标题："compared with baselines across **seven testing sets**"；§4.1 列出 VSR、TallyQA、GQA、MathVista-mini、MME、OVDEval（position） | ✅ |
| 47 | POLIA 答案级外在优势沿用 GRPO 组内归一化；物体级内在优势先按置信度修正奖励、再组内归一化；置信度为 IoU 与归一化距离加权 | POLIA §4（图 2 与正文）："The answer-level **extrinsic advantages** are computed based on the extrinsic rewards of a group of candidate answers"；"si,o is derived from the matching quality between the predicted bounding box... computed as a **weighted combination of IoU and normalized L1 distance**, followed by clipping. We define the corrected object-level reward... ri,o = R(ci)·si,o"；随后 "normalize {ri,o}... within the same visual object group" | ✅ |
| 48 | POLIA 在 VSR 上将基线 GRPO 的 **59.0% 提升至 81.3%** | POLIA Table 1（7B）："Qwen2.5-VL+GRPO **59.0**... POLIA **81.3**"（VSR 列） | ✅ |
| 49 | POLIA Aint 计算仅耗时 **0.002 s**，Rollout 占训练总时间 **97.24%** | POLIA 附录（效率分析）："the Rollout phase is the dominant bottleneck, consuming 536.25 s (**97.24%**) of the total time... the computation of Aint accounts for only **0.002 s**" | ✅（建议注明该测速基于 **POLIA-3B** 单次迭代） |
| 50 | 表4 POLIA 基座 Qwen2.5-VL-7B；VSR 等 7 基准 | POLIA §5.1："For the 7B setting, we adopt **Qwen2.5-VL-7B-Instruct**"；Table 1 列：VSR、TallyQA、GQA、MathVista、MathVision、LogicVista、MME = **7 个** | ✅ |
| 51 | SAYO 以区域级视觉注意力作为奖励信号，把对齐对象从显式框推广到注意力分布 | SAYO 摘要："we propose SAYO... introduces a **region-level visual attention–based reward**" | ✅ |

### 2.5 第 3.3 节 推理过程优化（含表 3、表 4 对应行）

| # | 二稿表述 | 原文出处与摘录 | 结论 |
|---|---------|---------------|------|
| 52 | VisualPRM 训练 **8B** 过程奖励模型，在 **7 个**多模态推理基准上带来 **3.7~8.9 个点**提升（3.7~8.4 见摘要；8.9 为 InternVL2.5-26B） | VisualPRM 摘要："multimodal Process Reward Model (PRM) with **8B parameters**... improves... MiniCPM-V2.6, QwenVL2.5-7B, InternVL2.5-8B, and InternVL2.5-78B by **8.0, 3.7, 8.4, and 5.9 points**, respectively, across **seven** multimodal reasoning benchmarks"；Table 2：InternVL2.5-26B 行 "+... **+8.9**"（Overall） | ✅（区间口径处理严谨，与摘要及表 2 均吻合） |
| 53 | VisualPRM 步骤定义纯文本、无视觉锚定（本文观察） | VisualPRM §3 采用多轮对话式步骤正确性预测（步骤为文本推理步）；此为二稿作者自己的观察并已注明"本文观察" | ✅（标注规范） |
| 54 | Self-Questioning 奖励为二元：输出含子问题序列 + 最终答案正确 | Self-Questioning 摘要："guided by a reward signal that scores **whether the output contains sub-questions** and **whether the final answer is correct**" | ✅ |
| 55 | 子问题质量故意不检查 | Self-Questioning 附录："adopt a reasoning format, it does not **guarantee the quality** [of sub-questions]"；摘要："The model is never shown examples of how to decompose questions" | ✅ |
| 56 | A-OKVQA 上基座 **46.8%**、标准 RLVR **51.6%**、本方法 **52.2%**；对照模型与本方法唯一差别是格式要求 | Self-Questioning 摘要："both self-questioning and standard reinforcement learning substantially improve accuracy over the untrained model (**52.2% and 51.6% vs. 46.8%**)"；§4：SQ+GRPO 与 Direct+GRPO 仅 prompt 模板不同 | ✅ |
| 57 | Self-Questioning 基座 Qwen2.5-VL-3B | Self-Questioning §4.1："Our base model is **Qwen2.5-VL-3B-Instruct**"（3B 参数，摘要："a 3-billion-parameter model"） | ✅ |
| 58 | H-GRPO 推理结构化为"（子问题，子答案，证据框）"三元组序列，预测与参考三元组经匈牙利二分图匹配 | H-GRPO 摘要/§3.2："decompose the reasoning into a sequence of **triplets τi = ⟨qi, ai, bi⟩**, where each triplet contains a sub-question, intermediate answer, and supporting spatial evidence"；§3.4："we construct a **bipartite matching problem**... The optimal assignment is obtained by [Hungarian] arg max" | ✅ |
| 59 | 相似度矩阵综合证据框兼容性、子问题/子答案语义相似度与框 IoU **四个分量** | H-GRPO §3.4："Sij = 1/4 (**E**(ˆbi, b∗j) + **simq** + **sima** + **IoU**(ˆbi, b∗j))... E measures whether the predicted bounding box exists and is compatible... simq and sima are Sentence-BERT cosine similarities" | ✅ |
| 60 | 总奖励为格式奖励与"答案奖励 × 匈牙利奖励"之和；光答对但中间步骤不到位奖励即被门控 | H-GRPO §3.5："R = **αR_format + βR_answer · R_HS**... This formulation **conditions the final answer reward on the Hungarian reward**" | ✅ |
| 61 | GRPO 是 H-GRPO 对角匹配的特例 | H-GRPO §3.6/摘要："the **diagonal matching of H-GRPO reduces to GRPO**" | ✅ |
| 62 | SmolVLM-2.2B 在 A-OKVQA 达 **73.4%**；小模型受益最大；参考链经人工验证 | H-GRPO Table 1："H-GRPO (SmolVLM-2.2B) **73.4** [A-OKVQA] 77.2 [Visual7W]"；§4.1："improves in-domain performance, **especially for the smaller SmolVLM-2.2B backbone**"；§4 数据："refined through **human-in-the-loop verification**... We **manually validate** the quality" | ✅ |
| 63 | 表4 H-GRPO 评测 A-OKVQA/Visual7W 与 OOD（MMMU/RealWorldQA/RoboSpatial/MMStar） | H-GRPO §4：in-domain A-OKVQA、Visual7W；§4.2："**MMMU**, **RealWorldQA**, **RoboSpatial**, and **MMStar**" | ✅ |

### 2.6 第 4 节 探讨 & 第 5 节 未来方向

| # | 二稿表述 | 原文出处与摘录 | 结论 |
|---|---------|---------------|------|
| 64 | MM-CondChain **975 个评估样本**（每样本 True-path/False-path 一对；**总数据集 4,634 例**），程序化生成并机械验证；最强模型仅得 **53.33 分**（Path F1） | MM-CondChain §3："This results in **975 evaluation samples** in total, each containing a **paired True-path and False-path instance**"；附录统计表 "Total **4634**"；摘要："the strongest model attains only **53.33 Path F1**" | ✅ |
| 65 | 4.3：CR³ 报告 MMVP、Winoground、Cola；SpatialThinker 横跨 14 基准；SVQA-R1 聚焦 Q-Spatial++；POLIA 在 VSR 等 7 基准；H-GRPO 依赖 A-OKVQA/Visual7W 与 OOD 基准 | 分别见 #32、#35、#39、#50、#63 | ✅ |
| 66 | SugarCrepe Swap"不依赖场景图标注、判别性强、规则可判定"（4.3 建议） | 依据 SugarCrepe §4 Swap 定义（交换同类别原子概念，不引入新概念）推导，属作者论证而非论文原文陈述 | ✅（论证性内容，依据充分） |
| 67 | 4.4：SpatialThinker 依赖 7K 人工场景图标注；POLIA 需要数据集物体标注；Ground-R1 证明无框监督可行 | SpatialThinker §3.3（见 #36）：STVQA-7K 是**基于** VG 人工标注场景图**合成**的 QA 集（QA 由管线生成、GPT-4o 校验），"7K 人工场景图标注"易被误读为"7K 条人工标注"；POLIA §B（VSR 等数据集自带物体/框标注）；Ground-R1（见 #40） | ⚠️ 建议改为"依赖基于 VG 人工场景图标注合成的 STVQA-7K" |
| 68 | AlphaGRPO 的 DVReward 将复杂请求分解为原子化可验证子问题，再由通用 MLLM 逐项评估；FactScore 原子事实分解 | AlphaGRPO 摘要（arXiv:2605.12495）："DVReward utilizes an LLM to **decompose complex user requests into atomic, verifiable semantic and quality questions**, which are then **evaluated by a general MLLM**"；FactScore 摘要："breaks a generation into a series of **atomic facts**" | ✅ |
| 69 | 多模态 PRM 以数学推理为主（**7 个评测基准中 5 个为数学类**） | VisualPRM Table 2 表头："MMMU, **MathVista, MathVision, MathVerse-VO, DynaMath, WeMath**, LogicVista"——Math 类恰为 5 个 | ✅ |

### 2.7 参考文献（23 条）核对

| 文献 | 二稿引用 | 核对结果 |
|------|---------|---------|
| [1] CREPE | arXiv:2212.07796, CVPR 2023 | ✅ 编号与 PDF 一致；CVPR 2023 属实 |
| [2] ARO | arXiv:2210.01936, ICLR 2023 | ✅ 编号与 PDF 一致 |
| [3] SugarCrepe | arXiv:2306.14610, NeurIPS 2023 | ✅ 编号与 PDF 一致 |
| [4] CR³ | AAAI 2026, doi:10.1609/aaai.v40i29.39680 | ✅/❓ PDF 确为 "The Fortieth AAAI Conference (AAAI-26)" 论文（vol.40 与 v40 一致）；DOI 本身无法从 PDF 核实 |
| [5] VALSE | arXiv:2112.07566, ACL 2022 | ✅ 编号与 PDF 一致 |
| [6] LLaVA-RLHF | arXiv:2309.14525 | ✅ 与 PDF 一致 |
| [7] RLHF-V | arXiv:2312.00849, CVPR 2024 | ✅ 与 PDF 一致 |
| [8] Silkie | arXiv:2410.09421 | ⚠️ 编号与 arXiv v1 标题《Aligning Large Vision-Language Models with AI Feedback》一致；但该文 EMNLP 2024 正式版更名为 **VLFeedback: A Large-Scale AI Feedback Dataset...**；原始 Silkie 论文为 arXiv:**2312.10665**（Silkie: Preference Distillation for Large Visual Language Models）。建议改引 2312.10665 或注明正式版更名 |
| [9] DeepSeekMath | arXiv:2402.03300 | ✅ 与 PDF 一致 |
| [10] DPO | arXiv:2305.18290, NeurIPS 2023 | ✅ 与 PDF 一致 |
| [11] GRPO is Secretly a PRM | arXiv:2509.21154, 2025 | ✅ 与 PDF 一致 |
| [12] VisualPRM | arXiv:2503.10291, 2025 | ✅ 与 PDF 一致 |
| [13] SpatialThinker | arXiv:2511.07403, **NeurIPS 2025** | ⚠️ 编号与 PDF 一致；但 arXiv 官方页面标注 "Accepted at **NeurIPS 2025 Workshops**（SpaVLE Oral、EWM、ARLET、SEA）"，为 **Workshop 论文而非主会议**，建议改为 "NeurIPS 2025 Workshops" |
| [14] SVQA-R1 | arXiv:2506.01371, **ICLR 2026** | ⚠️ 编号与 PDF（v1）一致，PDF 自标 "Preprint. Under review"；OpenReview 显示其发表于 **ES-Reasoning Workshop @ ICLR 2026**（First Workshop on Efficient Spatial Reasoning），非主会议，建议改为 "ICLR 2026 Workshop" |
| [15] Ground-R1 | arXiv:2505.20272 (v3), 2026 | ✅ PDF 版本戳 "arXiv:2505.20272**v3**"；标题 "Ground-R1: Thinking with Images via Scale Relative Policy Optimization" 与 PDF 完全一致 |
| [16] GRIT | arXiv:2505.15879, 2025 | ✅ 与 PDF 一致 |
| [17] POLIA | ICML 2026 | ✅ PDF 版权页："Proceedings of the **43rd International Conference on Machine Learning**... **PMLR 306, 2026**" |
| [18] SAYO | arXiv:2602.08241, 2026 | ✅ 与 PDF 一致（标题亦一致） |
| [19] Self-Questioning | arXiv:2606.15651, 2026 | ✅ 与 PDF 一致 |
| [20] H-GRPO | arXiv:2606.29915, 2026 | ✅ 与 PDF 一致 |
| [21] MM-CondChain | arXiv:2603.12266, 2026 | ✅ 与 PDF 一致 |
| [22] AlphaGRPO | arXiv:2605.12495, ICML 2026 | ✅ arXiv 页确认（2026-05-12 提交）；官方 GitHub 标注 [ICML2026] |
| [23] FActScore | arXiv:2305.14251, EMNLP 2023 | ✅ 与 PDF 一致 |

---

## 三、修改建议汇总（按优先级）

1. **❌ 必改**（2.2 节）："'可验证奖励强化学习'（RLVR；术语出自 DeepSeek-R1）"→ 改为"术语出自 Tülu 3"或"经 DeepSeek-R1 推广"。
2. **❌ 必改**（表 1 VALSE 行）："计数与动作最弱"→ 改为"动作与复数/共指最弱"（或"除存在性外普遍偏弱，动作/复数/共指最弱"）。
3. **⚠️ 建议改**（参考文献 [13][14]）：SpatialThinker 补 "Workshops"；SVQA-R1 补 "Workshop"，避免与主会议混淆。
4. **⚠️ 建议改**（引言 & 3.1 & 表 4）：CR³ 提升幅度统一口径——论文自述"10 absolute points"，表 3 实算 +9.3/+10.0；二稿"超 9 点"保守成立，但建议注明"论文正文表述为 10 点"或直接采用"约 10 个绝对点"。
5. **⚠️ 建议改**（表 1 SugarCrepe 行）："物体/属性/关系 × Replace/Swap/Add"→ 注明 Swap、Add 无"关系"子类。
6. **⚠️ 建议改**（4.4 节）："SpatialThinker 依赖 7K 人工场景图标注"→"依赖基于 Visual Genome 人工场景图标注合成的 STVQA-7K"（7K 指合成 QA 样本数，非人工标注数；表 3"高（STVQA-7K 人工标注）"同理）。
7. **⚠️ 可选**（3.2/表 4）：GRIT"20 个图文问答三元组"→"20 个图文问答样本"；POLIA 0.002s/97.24% 注明"基于 POLIA-3B 实测"；参考文献 [8] 考虑改引 Silkie 原文（arXiv:2312.10665）。

## 四、核对方法附注

- 全部 27 篇 PDF 经文本层提取后逐条检索定位，关键数字均回读上下文确认（含表格数值的行/列比对，如 CR³ Table 3、POLIA Table 1、Ground-R1 Table 3、VisualPRM Table 2、H-GRPO Table 1、SVQA-R1 Table 3 等）。
- 工作区 PDF 不覆盖的 4 个事实（RLVR 术语来源、Silkie/VLFeedback 版本关系、SpatialThinker 与 SVQA-R1 的会议性质、AlphaGRPO 内容与编号）经网络检索多来源交叉确认。
- 二稿中的公式占位（如"（）"处空括号）为 Word 公式对象，不在数据核对范围内。
