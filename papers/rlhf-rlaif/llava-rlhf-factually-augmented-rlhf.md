# Aligning Large Multimodal Models with Factually Augmented RLHF

> LLaVA-RLHF：用"图像事实"增强奖励模型，治 MLLM 的幻觉（CMU/UW/UC Berkeley/Microsoft，2023）

## 这篇论文到底在解决什么问题？

大视觉语言模型（MLLM）在 RLHF 对齐时有一个隐蔽的毛病：**奖励模型（reward model）只看到"问题+回答"两段文本就打分，看不到图**。于是它学会走捷径——回答里只要出现看起来合理的描述就高分，哪怕描述和图完全对不上。这直接**奖励了幻觉**（reward hacking），模型越对齐越会"一本正经地胡说八道"。

为什么以前的方法不行？
- 人工直接评估模型回答太贵、无法规模化；
- 普通 RLHF 的 reward model 输入是纯文本，**缺乏视觉事实依据**，无法判断"回答是否忠于图像"。

这篇论文想改什么：**给奖励模型补上"视觉事实"这个裁判依据**——判断一个回答好不好，不能只看文字，还要看它和图像事实（图像描述）对不对得上。

## 他们怎么做的？

**核心 idea：把图像描述（caption）作为"事实增强"注入 reward model 的输入——从"问题+回答"两输入变成"问题+回答+图像事实"三输入，让奖励判断有据可依。** 技术流派：RLHF 的 reward model 输入改造（Factually Augmented RLHF，Fact-RLHF）。

1. **第一步：构建偏好数据**：收集约 1 万条人工标注的多模态偏好对（同一个问题，两个回答哪个更好），覆盖多个领域；
2. **第二步：训练事实增强的 reward model**：奖励模型输入不再是"问题+回答"，而是"问题+回答+该图的事实描述（caption）"——回答若与图像事实冲突（幻觉），reward model 能看出矛盾打低分；
3. **第三步：PPO 优化策略**：用训练好的 reward model 当信号，对 LLaVA 1.5（7B/13B）做标准的 PPO 强化学习对齐。

**关键设计动机**：奖励信号必须"有事实依据"——这是防止 reward hacking 的直接手段。如果 reward model 能引用图像事实来验证回答，模型"编造"的行为就无法获得高奖励。

**与同类方法的区别**：普通 RLHF 的 reward model 只看文本（问题+回答）；Fact-RLHF 额外注入图像描述作为事实锚点——这是第一个把"视觉事实"纳入 MLLM 奖励信号的系统性工作。

## 效果怎么样？

- 在幻觉评测基准 MMHAL-bench 上显著优于基座模型和普通 RLHF（幻觉率大幅下降）；
- 通用能力基本保持或略有提升（VQAv2、MM-Vet 等基准不降反升）；
- 消融显示：去掉图像事实输入后，幻觉抑制效果明显变差——证明"事实增强"是核心机制。

**局限性**：
- 奖励仍是**结果级整体判断**——"这个回答与图像是否一致"，而非"组合理解是否正确"；
- 图像描述是**粗粒度事实**：caption 本身可能丢失组合细节（如"左边发霉的橙子"被描述成"两个橙子"），奖励模型也救不回描述里没有的信息；
- 主要针对**幻觉**问题，组合推理不是其直接目标。

## 对谁有用？

- 做 **MLLM 对齐 / 幻觉抑制**的人——"奖励信号要有事实依据"的设计范本；
- 综述定位：**Background 中"结果验证（RLHF/RLAIF）"阶段的代表**——它的奖励来自"人对回答的评判"，而非"对组合正确性的验证"，恰好反衬出后续方法（验证器/视觉对齐/过程奖励）的演进动机。

## 原文信息

- 来源：arXiv
- 链接：https://arxiv.org/abs/2309.14525
- 作者：Zhiqing Sun, Sheng Shen, Shengcao Cao, Haotian Liu, Chunyuan Li, Yikang Shen, Chuang Gan, Liang-Yan Gui, Yu-Xiong Wang, Yiming Yang, Kurt Keutzer, Trevor Darrell
- 发表时间：2023 年 9 月
- PDF 路径：papers/rlhf-rlaif/llava-rlhf-factually-augmented-rlhf.pdf
