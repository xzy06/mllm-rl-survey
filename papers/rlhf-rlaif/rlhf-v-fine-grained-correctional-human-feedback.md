# RLHF-V: Towards Trustworthy MLLMs via Behavior Alignment from Fine-grained Correctional Human Feedback

> RLHF-V：让标注员"直接改错"而不是"打分"，用细粒度纠错反馈对齐 MLLM（清华/NUS，CVPR 2024）

## 这篇论文到底在解决什么问题？

MLLM 的幻觉问题靠 RLHF 治不好，原因在反馈的**粒度**：人类标注员只能对"整个回答"打个好坏分，但一个回答里往往只有一两句话是幻觉——**错误片段被淹没在整体评分里**，模型学到的是"整体上像话就行"，并不知道该改哪里。

为什么以前的方法不行？
- 结果级 RLHF：反馈是"哪个回答更好"，粒度粗，无法定位幻觉片段；
- 训练 reward model 成本高，且 reward model 自身也有盲区。

这篇论文想改什么：**把人类反馈从"评分"改成"纠错"**——标注员直接删除/替换回答中与图像不符的具体片段，把"哪里错了、错在哪儿"说得清清楚楚，再用稠密 DPO 学进去。

## 他们怎么做的？

**核心 idea：细粒度纠错人类反馈（fine-grained correctional human feedback）——标注员不是给回答打分，而是逐片段修正幻觉；修正后的数据用 dense DPO 训练，让对齐信号精确到句/片段级别。** 技术流派：人类反馈 + 纠错式标注 + DPO（无需训练 reward model）。

1. **第一步：细粒度纠错标注**：标注员拿到"图像+问题+模型回答"，直接**纠正回答中与图像不符的具体片段**（删除幻觉句、替换错误描述），保留正确部分——产出的是"纠错后的干净回答"，而非"哪个更好的偏好对"；
2. **第二步：dense DPO 训练**：把"原始回答 vs 纠错后回答"转化为逐片段的正负偏好，用 Dense Direct Preference Optimization 训练——不同于普通 DPO 只看整句，dense DPO 把奖励信号细化到每个片段/每个 token 的位置；
3. **第三步：评测验证**：在幻觉基准（MMHAL-bench 等）和通用基准上对比基座、LLaVA-RLHF 等方法。

**数据规模**：RLHF-V 数据集约 **1.4K 细粒度密集反馈样本**（量小但每条都带精确的片段级修正）。

**与同类方法的区别**：LLaVA-RLHF 是"整体偏好 + PPO"，RLHF-V 是"片段纠错 + DPO"——反馈粒度从结果级细化到片段级，且不需要单独训练 reward model（DPO 直接从偏好学习）。

## 效果怎么样？

- MMHAL-bench 上幻觉率显著低于基座模型和 LLaVA-RLHF（片段级纠错信号比整体评分更有效）；
- 通用能力（VQAv2、MM-Vet 等）基本保持；
- 1.4K 样本的小数据也能超过更大规模的偏好对齐——说明"标注质量/粒度"比"标注数量"更重要。

**局限性**：
- 纠错粒度仍是**语言片段**，不是"视觉-语义组合单元"；
- 组合错误（如"左边的橙子是发霉的"被纠正为"橙子是发霉的"，丢失空间绑定）需要标注员**主动识别绑定错误**，标注成本极高，难以规模化；
- DPO 不经过 RL 循环，严格说不是"RL 增强"，常作为对比基线。

## 对谁有用？

- 做 **MLLM 可信对齐 / 幻觉抑制**的人——"反馈粒度决定对齐质量"的经典案例；
- 综述定位：**Background 中"结果验证"阶段的最细粒度代表**——即使细化到片段级，反馈仍来自"人对回答的评判"，且组合绑定错误无法低成本标注，这为"组合正确性需要可验证信号"的论点提供了反面证据。

## 原文信息

- 来源：arXiv
- 链接：https://arxiv.org/abs/2312.00849
- 作者：Tianyu Yu, Yuan Yao, Haoye Zhang, Taiwen He, Yifeng Han, Ganqu Cui, Jinyi Hu, Zhiyuan Liu, Hai-Tao Zheng, Maosong Sun, Tat-Seng Chua
- 发表时间：2023 年 12 月（CVPR 2024）
- PDF 路径：papers/rlhf-rlaif/rlhf-v-fine-grained-correctional-human-feedback.pdf
