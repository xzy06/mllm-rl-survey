# MM-RLHF: The Next Step Forward in Multimodal LLM Alignment

> MM-RLHF：多模态对齐的"全家桶"——120K 细粒度人工偏好数据集 + 先批评再打分的奖励模型 + 带动态奖励缩放的 MM-DPO 算法

## 这篇论文到底在解决什么问题？

大多数多模态大模型（MLLM）没有经过充分的人类偏好对齐。已有的对齐研究集中在特定领域（如幻觉抑制），一个更根本的问题没人系统回答：**对人类偏好做对齐，能否系统性增强 MLLM 的整体能力？** 另外，现有多模态偏好数据要么规模小、要么粒度粗，奖励模型打分也缺乏可解释性。

## 他们怎么做的？

**① 数据：MM-RLHF 数据集（120K 细粒度人工标注偏好对）**

- 多轮、细粒度的人类偏好标注，覆盖 10 个评价维度、27 个基准评测；
- 训练时均匀采样 1/5 数据（全文实验），以控制算力。

**② 奖励模型：Critique-Based Reward Model**

- 先输出**批评（critique）**再打分，兼顾可解释性与打分能力——这是首个把"批评-打分"结构用于多模态奖励模型的工作。

**③ 算法：MM-DPO（传统 DPO 的多模态扩展）**

- **Dynamic Reward Scaling**：按偏好对的奖励差距（reward margin）动态调整更新强度——margin 越大（高置信度样本）更新越强，约束在 $[\beta_{ori}, (1+w)\beta_{ori}]$ 内避免过激更新；解决传统 DPO 对所有样本统一缩放的缺陷；
- **训练所有可能的比较对**而非只训 hardest pairs：对同一问题多个回答，任意两个排名不同的回答都构成有效比较对，充分利用信息；
- 训练细节：混合 SFT loss（权重在 {0, 0.1, 0.25, 0.5, 1.0} 网格搜索）；vision encoder 全程冻结。

## 效果怎么样？

- 在 MM-RLHF 数据集上做对齐，几乎所有基准上对各基线（LLaVA-OV-7B/0.5B、InternVL-1B）一致提升；
- 奖励模型 **MM-RLHF-Reward-7B 在奖励模型基准上达到开源 SOTA，甚至超过多个 72B 模型**；
- 消融证实 Dynamic Reward Scaling 与全比较对训练各自有效。

## 对谁有用？

- 做多模态对齐/偏好学习的人：数据集与 MM-DPO 算法是"偏好对齐"路线的现成基准；
- 写综述/做组合推理的人：MM-RLHF 代表多模态 DPO 家族——反馈粒度仍是回答整体/片段级，**未触及组合绑定正确性**，是"奖励信号演进起点（偏好对齐端）"的对照样本。

## 原文信息

- 来源：arXiv
- 链接：https://arxiv.org/abs/2502.10391
- 作者：Yi-Fan Zhang, Tao Yu, Haochen Tian, Chaoyou Fu 等
- 发表时间：2025-02，ICML 2025
- PDF 路径：papers/rlhf-rlaif/mm-rlhf-next-step-multimodal-alignment.pdf
