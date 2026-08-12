# GRIT: Teaching MLLMs to Think with Images

> GRIT：教 MLLM"用图来思考"——推理链里穿插真实图像区域坐标（UC Santa Cruz + eBay，2025，引用 117+）

## 这篇论文到底在解决什么问题？

**MLLM 的"推理"其实是纯文本推理。** 模型生成 Chain-of-Thought 时，思考过程全是文字，根本没有真正"看"图——它可能推理链写得头头是道，但引用的是训练数据里的先验，而不是图像里真实的物体位置。典型的"文字想象"而不是"视觉推理"。

为什么难解决？

- 让推理链里带上视觉锚点（比如 bounding box），需要**稠密的推理链标注**或**框标注**，成本极高；
- 已有的 grounded reasoning 方法（如 Set-of-Mark）推理时需要**外部检测器**，慢且依赖工具。

这篇论文想要：**只用图像-问题-答案三元组（最便宜的监督），就让模型自发学会在推理链中穿插显式的 bbox 坐标——"思考"和"看图"在同一句话里完成。**

## 他们怎么做的？

**核心 idea：定义一种"grounded reasoning"输出范式（推理链 = 自然语言 + 显式 bbox 坐标交错），再用专门设计的 GRPO-GR 三重奖励把它逼出来——训练只需要 IQA 三元组，不需要任何推理链标注或 bbox 标注，20 个样本就够。** 技术流派：GRPO 变体（GRPO-GR）+ 奖励重设计（格式/计数/裁判三类信号相加）。

### 第一步：定义 Grounded Reasoning 范式

模型输出固定三段式结构（prompt 后缀在训练和推理时固定追加）：

```
<think> 自然语言推理，穿插 bbox 坐标（JSON 格式 "bbox_2d": [[x1,y1,x2,y2], ...]）</think>
<rethink> 基于刚才的坐标重新审视推理</rethink>
<answer> 最终答案</answer>
```

关键点：推理链里每一个关键判断都锚定在具体图像区域上——"思考"和"看图"在同一句话里完成，而不是先想完再找证据。

### 第二步：GRPO-GR 三重奖励

对每个完成 o_i 计算任务奖励 r_i = R(q, o_i)，三个分量共同组成：

1. **格式奖励 r_format = s_st + s_bf**（两个子信号相加）：
   - s_st：特殊 token 结构完整（`<think>`/`<rethink>`/`<answer>` 齐全）；
   - s_bf：bbox 语法合法（能解析成合法的 JSON 坐标数组）；
2. **计数奖励 r_count**（可选，只用于计数类训练样本，如 TallyQA）：生成框的数量与 GT 物体数完全一致 → 给 0.5 分——逼模型系统地"数着框推理"，而不是随便画几个框；
3. **GPT 辅助答案准确率奖励 r_ans**：让 GPT 当裁判对答案打分（0-1 分），prompt 要求输出 `{score: x}` 格式——代替死板的字符串匹配，能处理开放答案的语义等价。

组内归一化优势（δ = 1e-8 防除零）：

$$ A_i = \frac{r_i - \text{mean}\{r_1,\dots,r_N\}}{\text{std}\{r_1,\dots,r_N\} + \delta} $$

策略更新用标准 GRPO 目标（importance ratio clip + β·KL 惩罚）。

### 第三步：训练配置

- **数据**：只有 20 个唯一的图像-问题-答案三元组（10 个来自 VSR 空间关系 + 10 个来自 TallyQA 计数）；
- **基座**：Qwen2.5-VL-3B 和 InternVL-3-2B（预训练模型直接 RL）；
- **训练**：200 步、总 batch 128、每组采样 G=4 条候选轨迹、学习率 2e-6、AdamW + Cosine 调度；
- **算力**：8×A100 80GB + DeepSpeed ZeRO2，每个模型约 12 小时。

### 评测协议

六个测试集：VSR（空间关系）、TallyQA（计数）、GQA（组合物体空间问题）、MathVista-mini（视觉数学）、MME（计数/位置）、OVDEval position 子集（开放词汇 grounding）。指标两个维度：**ACC**（GPT-as-judge 答案正确率）+ **GIoU**（生成框与人工精修 GT 框的 IoU）。

### 与同类方法的区别

GRIT 不要求稠密推理链标注或 bbox 标注（对比 Set-of-Mark 类方法要外部检测器、SFT 类方法要推理链样本）；和纯文本 CoT 的本质区别是推理中强制穿插 bbox——"有图有真相"的推理范式。

## 效果怎么样？

- **20 个样本触发能力**：Qwen2.5-VL、InternVL 3 等模型训练后能稳定产出 grounded reasoning 链——这几乎是"最小监督"的极限；
- 消融实验（表 3）：去掉计数数据和计数奖励后，GIoU 从 0.387 掉到 0.349、OOD 准确率 64.4→60.0——说明计数奖励对 grounding 质量有实质贡献；
- 提出了 **Vision-Language Reasoning Cross-Modal Correlation 指标**：用 GPT-4o 判断模型推理链里的 bbox 是否真的和推理内容相关（而不是随便画的框），比只看 GIoU 更贴近"推理是否真的 grounded"。

**局限性**：GPT 裁判的准确率奖励有成本和偏差；20 样本的魔力依赖基座模型已有的 grounding 能力（Qwen2.5-VL 本身支持 bbox 输出）；bbox 只是"看哪儿"的粗略代理，像素级证据（saliency）未覆盖。

## 对谁有用？

- 做**数据高效 RL** 的人——20 样本触发新能力的案例非常有参考价值；
- 做**grounded reasoning / 视觉证据推理**的人——它是"推理链+坐标"范式的开创者；
- 写综述时它是"视觉对齐奖励"方向的代表：对齐载体是推理链中显式的 bbox 坐标，训练却不需要任何框标注——奖励信号设计在"结果验证"和"视觉结构对齐"之间搭了桥。

## 原文信息

- 来源：arXiv
- 链接：https://arxiv.org/abs/2505.15879
- 作者：Yue Fan, Xuehai He, Diji Yang, Kaizhi Zheng, Ching-Chen Kuo, Yuting Zheng, Sravana Jyothi Narayanaraju, Xinze Guan, Xin Eric Wang
- 发表时间：2025 年 5 月
- PDF 路径：papers/grounded/grit-teaching-mllms-to-think-with-images.pdf
