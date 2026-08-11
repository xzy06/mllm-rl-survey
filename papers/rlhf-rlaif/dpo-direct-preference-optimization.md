# Direct Preference Optimization: Your Language Model is Secretly a Reward Model

> DPO：把 RLHF 的"训练奖励模型 + PPO 优化"两步压缩成一步——用策略直接当隐式奖励模型，一个交叉熵损失搞定，不需要强化学习

## 这篇论文到底在解决什么问题？

大模型要靠人类偏好对齐（RLHF）才能听话，但传统 RLHF 又慢又难：先训一个显式奖励模型（RM），再用 PPO 做强化学习优化——要采样、要调一堆超参数、训练不稳定。有没有办法**跳过 RL 循环**，直接用偏好数据微调？

DPO（Stanford，2023）给出的答案是：有。关键洞察是——偏好模型（Bradley-Terry）下，奖励函数和最优策略之间存在解析对应关系。于是"在奖励函数空间里做损失"可以等价地变成"在策略空间里做损失"，策略本身就是隐式奖励模型。

## 他们怎么做的？

**核心思想：变量替换**

- 标准 RLHF 分两步：① 用偏好对训练奖励模型 $r_\phi$（二分类对数似然）；② 用 PPO 优化策略以最大化奖励并做 KL 约束。
- DPO 利用"最优策略 ↔ 奖励函数"的一一映射（$\beta$ 控制偏离参考策略的程度），把奖励函数写成策略的形式代入偏好损失，得到直接作用在策略上的目标：

$$ \mathcal{L}_{DPO}(\pi_\theta; \pi_{ref}) = -\mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \left[ \log \sigma\left( \beta \log \frac{\pi_\theta(y_w | x)}{\pi_{ref}(y_w | x)} - \beta \log \frac{\pi_\theta(y_l | x)}{\pi_{ref}(y_l | x)} \right) \right] $$

- 就是**一个二分类交叉熵损失**：提高被偏好回答 $y_w$ 的概率、降低被拒绝回答 $y_l$ 的概率，权重由隐式奖励差 $\hat{r}_\theta(y_l) - \hat{r}_\theta(y_w)$ 决定——奖励估计错得越离谱（把差的排到前面），更新力度越大，有自纠正效果。

**实现要点**

- 不需要从策略采样、不需要显式 RM、几乎不需要超参数调优；主要超参数就是 $\beta$（实现里默认 0.1）；
- 参考模型 $\pi_{ref}$ 固定为 SFT 模型，训练中不更新；
- 附录给了 PyTorch 实现（`dpo_loss(pi_logps, ref_logps, yw_idxs, yl_idxs, beta)`），只有几行。

## 效果怎么样？

- 在对话、摘要等任务上与 PPO-RLHF 相当或更好，且**没有 RL 的稳定性问题**；
- 对超参数不敏感（"with virtually no tuning of hyperparameters"）；
- 局限：DPO 是**离线**目标——偏好对来自固定采样分布，不随策略迭代更新，无法从模型自己生成的新路径中持续获益（这是 GRPO 等在线方法的相对优势）。

## 对谁有用？

- 做对齐（RLHF/RLAIF/可验证奖励）的人：DPO 是"偏好对齐"路线的基准方法；
- 做组合推理 RL 的人：可验证奖励下 DPO 也能用（同题多答、规则判正负造偏好对），但要理解其离线属性与 GRPO 的在线组采样之间的本质差异——这是"为什么组合推理方法普遍用 GRPO 而非 DPO"问题的答案起点。

## 原文信息

- 来源：arXiv
- 链接：https://arxiv.org/abs/2305.18290
- 作者：Rafael Rafailov, Archit Sharma, Eric Mitchell 等（Stanford）
- 发表时间：2023-05，NeurIPS 2023
- PDF 路径：papers/rlhf-rlaif/dpo-direct-preference-optimization.pdf
