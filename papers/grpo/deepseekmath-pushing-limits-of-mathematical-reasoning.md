# DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models

> DeepSeekMath：120B 数学 token 语料 + GRPO 算法——无 critic 的组内相对优势强化学习，7B 模型 MATH 83.6%（DeepSeek-AI，2024）

## 这篇论文到底在解决什么问题？

开源模型在数学推理上长期落后于闭源模型，原因是双重的：**训练数据不够（数学语料稀少、质量差）**，以及 **RL 训练成本太高**。当时主流的 RL 对齐（如 PPO）需要额外训练一个 value network（critic）来估计基线，内存和训练开销巨大，且对数学这种"答案可验证"的任务是浪费——为什么不用已有的规则验证器直接给奖励？

这篇论文想改什么：**一是把数学预训练语料做到 120B token 量级（远超当时开源同行），二是提出 GRPO——彻底去掉 critic 的 PPO 变体，让 RL 只靠一个 policy 模型 + 规则验证器就能训。**

## 他们怎么做的？

**核心 idea：数据上"挖矿"——从 Common Crawl 里用分类器筛出数学网页（120B 数学 token）；算法上"砍掉 critic"——GRPO 用组内采样回答的均值/标准差做基线，奖励来自确定性规则验证器。** 技术流派：数据工程 + RL 算法创新。

1. **第一步：数学语料挖掘**：训练分类器从 Common Crawl 中识别数学相关页面，配合质量过滤与去重，构建 **120B 数学相关 token** 语料（以中文和英文为主）；
2. **第二步：继续预训练**：用这 120B token 继续预训练 DeepSeek-Coder-Base-v1.5 7B，得到 **DeepSeekMath 7B**——不改架构，纯靠数据质量/数量取胜；
3. **第三步：SFT**：用约 144K 数学题（GSM8K、MATH 相关 CoT 格式）做指令微调，得到 DeepSeekMath-Instruct 7B；
4. **第四步：GRPO 强化学习**（核心算法贡献）：
   - 对同一个问题采样 **G 个回答**（一组），用**组内相对优势**代替 PPO 的 value network：
     $$
     A_i = \frac{r_i - \bar{r}}{\sigma_r}
     $$
     其中 $\bar{r}$、$\sigma_r$ 是组内奖励的均值与标准差——该回答的奖励相对于组内的归一化偏离；
   - **无 critic**：只保留 policy 模型，内存大幅下降；
   - **奖励来自规则验证器**：数学答案比对即可确定性计算，无需训练 reward model；
   - 目标函数含 clip 机制（同 PPO）与 KL 惩罚（使用无偏 KL 估计器，而非 PPO 的近似形式）。

**GRPO vs PPO 关键区别**：

| 维度 | PPO | GRPO |
|------|-----|------|
| 基线 | 需要单独训练的 value network（critic） | 无 critic，用组内均值做基线 |
| 奖励来源 | reward model（通常需训练） | 规则/验证器（可确定性计算） |
| 内存 | 高（policy + value 两个模型） | 低（只有 policy） |
| 奖励信号类型 | 可以是任何分数 | 最适合可验证奖励（verifiable rewards） |

## 效果怎么样？

- **DeepSeekMath 7B（base）**：MATH **51.7%**（不使用外部工具和投票机制，同规模开源模型的 SOTA）；
- **DeepSeekMath-7B-RL（GRPO 训练后）**：MATH **83.6%** pass@1，逼近当时 GPT-4（84.3%）；GSM8K **90.7%**；
- 7B 规模的模型无需工具/投票即达到竞赛级数学水平，证明"数据量 + 无 critic RL"的组合足够强；
- 论文至今被引 **7000+**，GRPO 成为 DeepSeek-R1 的训练核心与 RLVR（RL with Verifiable Rewards）路线的代表算法。

**局限性**：GRPO 的组内相对优势依赖"同题多采样"的奖励方差——当奖励不可自动验证（如开放生成任务）时优势计算失去意义；结果级奖励只验证最终答案，不验证推理过程本身（这正是后续 PRM 路线与"GRPO is Secretly a PRM"分析的切入点）。

## 对谁有用？

- 做 **RLVR / 推理增强 RL** 的人——GRPO 是这一路线的算法源头，去 critic 的组内基线思想被 R1 系列、多模态 RL（H-GRPO、Ground-R1 等）广泛沿用；
- 综述定位：**Background 中"GRPO 与推理过程优化"的锚点**——它定义了"结果级可验证奖励 + 组内相对优势"这一奖励范式；你论文 3.3 推理过程优化的对比（GRPO 的隐式过程奖励 vs 显式过程奖励）以此为起点。同时它揭示的"奖励必须可验证"约束，正是组合推理（无唯一标准答案）难以直接套用 GRPO 的根本原因，也是"结果验证→结构验证→视觉对齐"演进的驱动力。

## 原文信息

- 来源：arXiv
- 链接：https://arxiv.org/abs/2402.03300
- 作者：Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Mingchuan Zhang, Y.K. Li, Y. Wu, Daya Guo（DeepSeek-AI）
- 发表时间：2024 年 2 月
- PDF 路径：papers/grpo/deepseekmath-pushing-limits-of-mathematical-reasoning.pdf
