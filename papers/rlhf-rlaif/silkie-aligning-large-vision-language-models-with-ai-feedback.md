# VLFeedback: A Large-Scale AI Feedback Dataset for Large Vision-Language Models Alignment

> Silkie：让 GPT-4V 当裁判批量打分，用 8 万条 AI 反馈对齐 MLLM（北大/港大等，EMNLP 2024）

## 这篇论文到底在解决什么问题？

人类偏好标注是 MLLM 对齐的瓶颈：**贵、慢、难规模化**。而对齐效果又直接取决于反馈数据的质量和数量——没有足够的偏好数据，DPO/RLHF 就无从谈起。

为什么以前的方法不行？
- 人工标注多模态偏好成本极高，难以扩展到 8 万条量级；
- 已有的小规模对齐数据（如 LLaVA-RLHF 的 1 万条）不足以覆盖多样化的多模态指令。

这篇论文想改什么：**用 AI（GPT-4V）替代人类当标注员，规模化生产高质量多模态偏好数据**——这是 RLAIF（AI 反馈强化学习）路线的代表性工作。

## 他们怎么做的？

**核心 idea：构建 VLFeedback——第一个大规模 AI 标注的多模态反馈数据集（8 万+ 条），用 GPT-4V 从四个维度给模型回答打分并写理由，再用 DPO 对齐 Qwen-VL-Chat。** 技术流派：RLAIF（AI 反馈）+ DPO。

1. **第一步：收集指令**：从多个来源汇集 **82,052 条多模态指令**（覆盖视觉问答、图像描述、推理等广泛任务）；
2. **第二步：GPT-4V 四维评分**：让 GPT-4V 对每个"指令-回答"对从四个维度打分并给出评分理由（rationale）：
   - **正确性（Correctness）**：回答是否准确、与图像是否一致；
   - **详细度（Detailedness）**：信息是否充分；
   - **帮助性（Helpfulness）**：对用户是否真的有用；
   - **总体（Overall）**：综合质量。
3. **第三步：DPO 对齐**：从评分中构造偏好对，对 Qwen-VL-Chat 做 DPO 训练，得到对齐模型 **Silkie**。

**与同类方法的区别**：LLaVA-RLHF 用人类偏好（结果级、PPO），RLHF-V 用人类纠错（片段级、DPO）；Silkie 把标注者从人换成 GPT-4V，用"四维评分 + rationale"提高 AI 反馈的质量和可解释性——**对齐信号的可扩展性第一次不再受人类标注速度限制**。

## 效果怎么样？

- Silkie 在 MMBench、MM-Vet、LLaVA-Bench、MMHal-bench 等多个基准上**全面超越未对齐的 Qwen-VL-Chat**；
- 四维评分中"正确性"维度对对齐效果贡献最大；
- 验证了 AI 反馈可以规模化替代人类反馈的主流路线。

**局限性**：
- **"以盲导盲"问题**：GPT-4V 自身在组合推理上就有系统性弱点（属性绑定、空间关系错误），AI 反馈会**传播同样的盲区**——这与你综述 thesis 直接相关：AI 反馈的可靠性受限于标注模型自身的组合理解能力，形成闭环盲区；
- 偏好比较是**整体评分**，无法定位到具体组合错误的环节（比 RLHF-V 的片段级更粗）。

## 对谁有用？

- 做 **MLLM 对齐数据工程 / RLAIF** 的人——规模化 AI 反馈的范本；
- 综述定位：**Background 中"结果验证"阶段的反面教材**——它证明了"反馈来源从人换成 AI"可以规模化，但 AI 标注者自身的组合盲区会系统性传播，这正好引出"奖励必须来自可验证信号而非任何评判者"的核心论点。

## 原文信息

- 来源：arXiv
- 链接：https://arxiv.org/abs/2410.09421
- 作者：Lei Li, Zhihui Xie, Mukai Li, Shunian Chen, Peiyi Wang, Liang Chen, Yazheng Yang, Benyou Wang, Lingpeng Kong, Qi Liu
- 发表时间：2024 年 10 月（EMNLP 2024）
- PDF 路径：papers/rlhf-rlaif/silkie-aligning-large-vision-language-models-with-ai-feedback.pdf
