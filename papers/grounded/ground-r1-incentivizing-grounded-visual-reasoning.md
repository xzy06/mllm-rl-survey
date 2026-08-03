# Ground-R1: Incentivizing Grounded Visual Reasoning via Reinforcement Learning

> Ground-R1：用强化学习逼模型"指着图里的证据回答"（MBZUAI + 北大 + 中山大学，2025）

## 这篇论文到底在解决什么问题？

**大视觉语言模型（LVLM）的答案不可靠、也不可解释。** 模型经常靠预训练数据里的虚假相关（spurious correlation）猜答案，而不是真正去看图里相关的证据区域——你说"图片里有几只鸟"，它瞥一眼就答"2 只"，其实根本没数。

为什么以前的方法不行？

- 让模型输出 bounding box 需要**昂贵的框标注**（一张图标注一个框的成本很高）；
- 让模型输出推理理由需要**人工 rationale 标注**；
- 让模型调用外部工具（OCR、检测器）**推理时开销大**、还依赖工具质量。

这篇论文想要：**只靠"问题-答案对"这种最便宜的监督，让模型学会自己定位证据区域、自己放大看图、再给出有依据的答案。**

## 他们怎么做的？

**核心 idea：把推理拆成"找证据→放大看图→作答"两个阶段，分别用不同的奖励驱动——找证据阶段只给格式奖励（不要求框和任何标注对齐），作答阶段给格式 + 答案准确率奖励；整个流程用 GRPO 端到端训练，只靠"问题-答案对"监督。** 技术流派：两阶段 rollout 的 GRPO 变体（Grounding Rollout + Answer Rollout），不依赖 bbox 标注、rationale 标注和外部工具。

### 第一步：Grounding Rollout（找证据阶段）

给定问题 q 和图像 v，模型先从当前策略 π_θold 采样 G1=4 个 grounding rollouts，每个输出一个证据框 b_i ∈ ℝ⁴（轴对齐 bbox，左上/右下角坐标）：

\[ \boldsymbol{b} = \{\boldsymbol{b}_i\}_{i=1}^{G_1} \sim \pi_{\theta_{\text{old}}}(\cdot \mid \boldsymbol{q}, \boldsymbol{v}), \quad G_1 = 4 \]

提示词要求模型把分析过程写在 `<think>` `</think>` 标签里、把 bbox 坐标以 `[x1,y1,x2,y2]` 格式写在 `<box>` `</box>` 标签里，并说明"可以多轮 grounding 细化区域，bbox 始终基于原图；如果不再需要更多视觉信息，可以直接输出 `<answer>`"。

**这个阶段的奖励只有格式奖励** r^ground_i：推理在 `<think>` 标签内 + 坐标在 `<box>` 标签内即得分，**不做坐标级监督**——不要求框和任何 GT 标注匹配。这是关键设计：论文消融加入 GT bbox IoU 奖励的 Ground-R1-BBox（82.0）与 Ground-R1（81.7）几乎无差，证明 RL 下纯格式奖励足以让模型学会找证据，从而省掉昂贵的框标注。

### 第二步：Answer Rollout（作答阶段）

把每个证据框 b_i 裁剪出局部图像区域 e_i，与原图 + 问题一起送回模型，采样 G2=2 个 answer rollouts：

\[ \boldsymbol{o}_i = \{\boldsymbol{o}_{i,j}\}_{j=1}^{G_2} \sim \pi_{\theta_{\text{old}}}(\cdot \mid \boldsymbol{q}, \boldsymbol{v}, \boldsymbol{e}_i), \quad G_2 = 2 \]

每个证据框产出 2 条答案轨迹，共 G1·G2 = 8 条推理轨迹。作答阶段奖励 r^answer_i,j 由两部分组成：

- **格式奖励**：推理在 `<think>` 标签内 + 最终答案在 `<answer>` 标签内；
- **准确率奖励**（按题型自适应）：多选题 → 精确匹配（二元 0/1）；开放题 → 与 GT 的 ROUGE-1/2/L 平均分（词法对齐）。

模型可以多轮"找证据→放大→再找证据"，每次 bbox 都基于原图坐标，直到信息足够直接给 `<answer>`。

### 第三步：GRPO 联合优化

两阶段由同一个 GRPO 目标联合优化，advantage 在全部 8 条轨迹的奖励组内归一化：

\[ A_{i,j} = \frac{r^{\text{answer}}_{i,j} - \text{mean}(\{r^{\text{answer}}_{i,j}\})}{\text{std}(\{r^{\text{answer}}_{i,j}\})} \]

策略更新用标准 PPO 式 clip（ε 为超参）。**注意：论文消融发现不加 KL 约束反而更好**（Ground-R1-KL 80.0 vs Ground-R1 81.7）——作者解释：grounding-then-answering 范式与基座预训练的 vanilla QA 分布差异大，强 KL 对齐会阻碍模型适应中间 grounding 目标和任务奖励。

### 训练配置

- **数据**：VisCoT 数据集（438K QA 对，带 bbox 标注），**只取 1/50 = 8K 样本，并故意丢弃 bbox 标注**——只用问题-答案对；
- **基座**：Qwen2.5-VL-7B-Instruct；
- **训练**：1000 步、batch size 8、学习率 1e-6、采样温度 1、最大输出 512 tokens；
- **算力**：8×H100，约 12 小时。

### 与同类方法的区别

和 Vision-R1 / LMM-R1 等 R1 系列相比，Ground-R1 在推理中引入显式证据区域 grounding（两阶段 rollout + 放大看图），而非纯文本 CoT；和 CogCoM 等 grounded 方法相比，它不需要专门的 grounding 训练数据（CogCoM 用了额外 grounded VQA 数据集，因此在 RefCOCO test-A 上略胜一筹）。

## 效果怎么样？

- 在多个基准上取得 SOTA，且**不需要推理时调用外部工具**；
- 涌现出类似人类认知的行为：
  - **不确定性意识**：不确定时会自动放大看细节，而不是硬答；
  - **空间感知**：自动定位到和问题相关的区域；
  - **迭代细化**：第一轮看错了会自己纠正框的位置。
- 推理过程可解释：`<think>` 里的推理 + `<box>` 里的证据，人可以检查"它到底看哪儿了"。

**局限性**：格式奖励给了模型很大自由度，bbox 可能定位不准（没有框级监督兜底）；依赖模型本身"愿意"放大看，初始策略不好的小模型可能学不会；多轮放大的推理开销比单次回答大。

## 对谁有用？

- 做**grounded reasoning、减少幻觉**的研究者——"零框标注让模型学会指证据"的标杆；
- 做**RLVR 奖励设计**的人——它展示了"格式奖励"这种最轻量的监督也能驱动视觉定位行为；
- 写综述时它是"视觉对齐奖励"方向的代表之一：对齐对象从"答案"变成了"证据区域"。

## 原文信息

- 来源：arXiv
- 链接：https://arxiv.org/abs/2505.20272
- 作者：Meng Cao, Haoze Zhao, Can Zhang, Xiaojun Chang, Ian Reid, Xiaodan Liang
- 发表时间：2025 年 5 月
- PDF 路径：papers/grounded/ground-r1-incentivizing-grounded-visual-reasoning.pdf
