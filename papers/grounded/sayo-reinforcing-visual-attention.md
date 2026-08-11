# Do MLLMs Really See It: Reinforcing Visual Attention in Multimodal LLMs (SAYO)

> SAYO：MLLM"看"得不稳——用区域级视觉注意力奖励做 RL，让模型学会稳定地盯着该看的地方再推理

## 这篇论文到底在解决什么问题？

多模态大模型（MLLM）做复杂推理时，**视觉注意力很弱且不稳定**：早期看错地方，后续推理过程中几乎不会被纠正（错误传播），最终推理失败。作者的分析显示：

- 错误的预测往往伴随注意力放错位置或空间定位不准；
- 视觉注意力准确性与整体任务性能存在**强相关**——注意力错位是推理错误的主要驱动因素；
- 根源在于训练时**对视觉注意力行为缺乏信用分配**：现有训练目标没有把"看哪儿"变成可优化的信号。已有的视觉提示技巧（如 ViP 区域标记、prompt reflection）只是间接影响感知，不解决"注意力行为如何被学到"的问题。

## 他们怎么做的？

**核心思想：把视觉注意力直接变成奖励信号**

- 提出 **SAYO**（region-level visual attention–based reward）：一种**区域级视觉注意力奖励**；
- 在 RL 训练框架中，奖励显式对齐"视觉 grounded 推理步骤"——模型在推理时关注了正确的视觉区域，就得到正向信号；
- 与只奖励"答案对不对"的结果奖励不同，SAYO 直接对"看哪儿"这一行为做信用分配，迫使模型学习可靠的注意力策略（stable visual attention policies）。

（注：论文正文 18 页，本概括提取到的超参数/模型规模细节有限——奖励的具体公式与训练超参以原文为准。）

## 效果怎么样？

- 在多个多模态推理与感知基准上，SAYO 一致提升性能（"consistently improves performance on diverse reasoning and perception tasks"）；
- 定位：该工作属于"回答-视觉证据对齐"奖励谱系——与显式 bbox（Ground-R1/GRIT）、物体级置信度（POLIA）、显著性分布（Saliency-R1）并列，SAYO 把对齐对象推广到**区域级注意力分布**，信号载体从"框"换成"注意力"。

## 对谁有用？

- 做视觉对齐奖励/grounded 推理的人：SAYO 证明"注意力本身可以被奖励化"，与显式框监督互补；
- 做组合推理的人：组合绑定错误常伴随注意力错位，SAYO 的机制对"看得准才答得对"是直接支撑，但其评测未显式覆盖组合基准（VALSE/SugarCrepe 类）。

## 原文信息

- 来源：arXiv
- 链接：https://arxiv.org/abs/2602.08241
- 作者：Siqu Ou, Tianrui Wan, Zhiyuan Zhao, Junyu Gao, Xuelong Li
- 发表时间：2026-02
- PDF 路径：papers/grounded/sayo-reinforcing-visual-attention.pdf
