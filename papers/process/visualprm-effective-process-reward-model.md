# VisualPRM: An Effective Process Reward Model for Multimodal Reasoning

> VisualPRM：给多模态推理配一个"步骤裁判"——8B 的过程奖励模型，用蒙特卡洛自动标注步骤对错，Best-of-N 选答案，数学推理提 3.7–8.9 个点

## 这篇论文到底在解决什么问题？

大模型推理时，光看最终答案打分（ORM，outcome reward model）不够——答案对了但中间步骤可能是瞎蒙的。过程奖励模型（PRM）逐步骤打分，能更精细地评估推理质量。文本域已经有不少 PRM（Math-Shepherd、OmegaPRM），但**多模态 PRM 基本没人做**：

- 多模态推理（看图解题）的步骤质量怎么判断？文本 PRM 的管线没有覆盖视觉；
- 更糟的是，实测发现**开源 MLLM 当裁判根本判不出错误步骤**——正样本（正确步骤）F1 76.8，负样本（错误步骤）F1 只有 19.2，严重偏向"全判对"。

这篇论文（InternVL 团队，2025）做了三件事：一个 8B 多模态 PRM 模型、一个 40 万条的过程监督数据管线（VisualPRM400K）、一个带人工标注的评测基准（VisualProcessBench）。

## 他们怎么做的？

**第一步：造数据（VisualPRM400K，全程自动，零人工）**

- 问题来源：MMPR v1.1 的题目（图像 + 问题）；
- 用 InternVL2.5 系列模型采样逐步解（step-by-step solution）；
- 步骤正确性用**蒙特卡洛期望正确率**自动标注：给定某个步骤 $s_{\le i}$，模型续写多个后续 $\tilde{s}_{>i} \sim M(\tilde{s}_{>i} | I, q, s_{\le i})$，统计续写后最终答案正确的比例：
  $$ mc_i = \frac{\text{num(correct completions)}}{\text{num(sampled completions)}} $$
  若 $mc_i > 0$ 则判定该步骤正确。步骤数上限 12，超出则均匀合并。
- 总计约 400K 条多模态过程监督数据，每条含（图像、问题、逐步解、每步正确性标注）。

**第二步：训练 8B 过程奖励模型**

- 数据组织为多轮对话，模型在给定（图像、问题、已有步骤）的条件下预测**每一步的正确性（正确/错误二分类）**；
- 与之前"只监督到第一个错误步骤"的做法不同，VisualPRM **监督全部步骤**；
- 推理时逐步骤打分，再合并为回答分：步骤得分 = 离散分数（正确/错误）的生成概率加权和，默认取平均。

**第三步：评测（VisualProcessBench）**

- 2,866 个样本、26,950 条**人工**步骤级正确性标注（标注员至少大学学历），用于评测 PRM 和 MLLM 找错步骤的能力；
- 用 Best-of-N（BoN）策略评测：采样 N 个回答，用 PRM 打分挑最好的。

## 效果怎么样？

- 在 7 个多模态推理基准（MMMU、MathVista、MathVision、MathVerse-VO、DynaMath、WeMath、LogicVista）上，给 4 个不同规模的基座模型（含 InternVL2.5-78B）带来 **3.7–8.9 个点**的提升（BoN 策略）；
- PRM 一致优于 ORM 和 Self-Consistency（自洽投票）；
- 对比揭示关键事实：**开源 MLLM 当 critic 判不出错误步骤**（负样本 F1 仅 19.2），而 VisualPRM 总体 F1 达 62.0——"步骤裁判"必须专门训练。

## 对谁有用？

- 做多模态推理（数学、科学、逻辑）的人：可以用 PRM 做 test-time scaling（BoN），或把步骤信号搬进 RL 训练；
- 做过程奖励/组合推理的人：VisualPRM 的步骤定义**纯文本、无视觉锚定**——它判定"这一步是否通向正确答案"，不判定"这一步是否把属性/关系绑到了正确的图像区域"，这既是局限也是后续方向（把视觉证据框锚定进步骤）。

## 原文信息

- 来源：arXiv
- 链接：https://arxiv.org/abs/2503.10291
- 作者：Weiyun Wang, Zhangwei Gao, Lianjie Chen, Zhe Chen, Jinguo Zhu 等（InternVL 团队）
- 发表时间：2025-03
- PDF 路径：papers/process/visualprm-effective-process-reward-model.pdf
