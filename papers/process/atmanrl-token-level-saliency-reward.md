# ATMANRL: Towards Faithful Reasoning via Differentiable Attention Saliency

> ATMANRL：用"可微注意力掩码"揪出 CoT 里真正起作用的 token——把显著性当奖励并入 GRPO，让模型学会"写有用的推理过程"，而不只是"话多"

## 这篇论文到底在解决什么问题？

大模型用 chain-of-thought（CoT）解题时，推理过程常常**不忠实（unfaithful）**：写了一大段，但最终答案其实没怎么依赖它——把推理过程里的关键 token 抹掉，答案照样对；甚至推理里明摆着有错，答案还是对的。这种"推理是装饰品"的问题，光靠结果奖励（答案对就给分）治不了，因为结果奖励根本不管过程。

作者把概念拆开：
- **saliency（显著性）**：推理 token 对最终答案 logits 的可测因果贡献；
- **faithfulness（忠实性）**：推理过程必须真实反映产生答案的潜在推理——这要求更高。

要做的事：**训练时显式奖励"有显著因果贡献的推理过程"**。这篇论文（Aleph Alpha + TU Darmstadt，ICLR 2026 Workshop）用可微注意力掩码（ATMAN）逐样本找出关键 token，把显著性做成奖励，与结果奖励一起在 GRPO 里联合优化。

## 他们怎么做的？

**第一步：ATMAN——可微注意力掩码**

- 在注意力分数上加一个**加性掩码（additive attention mask）** $H_{AtMan}$，可以精细抑制/增强某个 token 的注意力贡献；
- 加性而非乘法，所以不改变输入分布与位置编码（位置编码用乘法掩码会受影响）；
- 每个样本独立学一个掩码，掩码参数用 SGD 优化。

**第二步：用掩码识别关键 token**

- 掩码初始化为**负值**——相当于先把 CoT 里所有 token 的注意力压下去，观察答案概率掉多少；
- 然后做约 **200 步 SGD 优化**，目标函数是"恢复正确答案概率"：哪几个 token 被重新放开后就能把答案概率拉回来，它们就是**对答案有真实因果贡献的关键 token**；
- 优化结束后，从掩码值导出每个 token 的显著性度量（saliency measure）。

**第三步：saliency 奖励 + 结果奖励联合训练（GRPO 框架）**

- 对每个采样到的 rollout 算出 token 级显著性；
- **saliency reward** 鼓励模型生成"更多关键 token 分布合理"的推理过程——具体指标如：平均推理 token 数下降（不废话）、数字/符号类关键 token 占比上升、停用词占比下降；
- 与 outcome-based reward **在 GRPO 中联合**优化：既对答案正确性负责，也对"推理过程确实在起作用"负责；
- 模型：Llama-3.2-3B-Instruct，评测 GSM8K 与 MMLU。

**关键区分**：saliency 只要求"这些 token 确实因果地影响了答案"，不要求"推理文字反映了模型真实思维"（后者需要可解释性干预，本方法不做）——所以这是**通往 faithful reasoning 的第一步**，不是终点。

## 效果怎么样？

- 在 GSM8K / MMLU 上（Llama-3.2-3B-Instruct）：**Avg tokens / CoT 下降**（推理更精简）、**Numbers 与 Symbols 占比上升、Stop words 占比下降**（推理内容更"有用"）、**Pass@4 提升**；
- 说明模型学会了"把力气花在关键数字和符号上"，而不是堆砌话术；
- 局限：目前只在**纯文本 LLM** 上验证，未扩展到多模态；saliency 度量依赖 ATMAN 掩码优化的稳定性；workshop 论文，规模与消融相对有限。

## 对谁有用？

- 做"过程信号 / 推理可解释性"的人：ATMANRL 提供了一条"把注意力/显著性做成可微奖励"的技术路线，可与任何结果型 RL 框架（GRPO）组合；
- 写综述/做组合推理的人：这是**"显著性/过程信号与结果信号可组合"在纯文本域的旁证**——正文 4.1 用它说明 AtMan 类显著性信号的组合性并非多模态特有；其"注意力掩码识别关键 token"与多模态的视觉显著性/注意力对齐思路同源。

## 原文信息

- 来源：arXiv
- 链接：https://arxiv.org/abs/2604.16158
- 作者：Max Henning Höth（Aleph Alpha）、Kristian Kersting（TU Darmstadt / Hessian.AI）、Björn Deiseroth、Letitia Parcalabescu（Aleph Alpha）
- 发表时间：2026-04，ICLR 2026 Workshop
- PDF 路径：papers/process/atmanrl-token-level-saliency-reward.pdf
