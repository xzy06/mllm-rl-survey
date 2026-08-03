# SVQA-R1: Reinforcing Spatial Reasoning in MLLMs via View-Consistent Reward Optimization

> SVQA-R1：用"视图一致性"奖励强化 MLLM 的空间推理（Stony Brook University，ICLR 2026）

## 这篇论文到底在解决什么问题？

**MLLM 处理空间关系（"左边/右边/上面/下面"）很不靠谱**。空间推理要求模型把物体、属性和相对位置精确绑定在一起，但现有方法主要靠 SFT 学静态模式——给定同样的输入永远输出同样的答案，模型没有"自己检查一下我是不是真的理解了这个布局"的能力。

之前的空间推理增强路线（SpatialVLM、SpatialPIN）都是**造大尺寸合成数据 + SFT**，有两个毛病：

1. 数据规模动辄百万级，成本高；
2. SFT 收敛到静态输出模式，泛化和自我纠错能力弱。

这篇论文借鉴 R1 范式，把空间推理变成**基于规则的强化学习问题**——用奖励信号逼模型自己学会"换一个视角看，答案还是一致"。

## 他们怎么做的？

**核心 idea：用镜像翻转造“视图一致”的监督信号，再设计一个全新的 Spatial-GRPO 让模型学到视角不变的空间理解。**

### 1. Mirror-Consistent 数据构造（基础工程）

- 把图像水平翻转（“左边”变“右边”），用 GPT-4o 生成翻转后仍然逻辑正确的 QA 对。
- **关键坑**：朴素 prompt 会让 GPT-4o 机械地把 left↔right 互换，产生逻辑矛盾（比如多物体场景里物体身份和方向对不上）。修复：在 prompt 里显式要求“先推理相对位置和物体身份，验证原答案的 left/right 关系，发现错误必须修正对象-方向映射”，并以 JSON 输出。
- 翻转前后 QA 语义对齐是后续联合奖励计算有意义的前提。

### 2. 混合奖励设计

空间推理是开放式回答（答案可能是“左边”、一段描述或数值），规则匹配会误伤语义正确但措辞不同的答案，所以用两个分量：

- **格式奖励 \(r^f\)**：输出是否符合 `<think>...</think> <answer>...</answer>` 结构，二值（0/1）。
- **语义奖励 \(r^s\)**：Sentence-BERT（all-MiniLM-L6-v2）编码预测与参考答案，算余弦相似度。能识别语义等价（GT 是 "couch"，预测 "sofa" 也高分），对距离、bbox 等数值答案也能度量数值差异。
- 总奖励：\( r = \lambda_1 r^f + \lambda_2 r^s \)，权重 \(\lambda_1=\lambda_2=0.5\)。

### 3. Spatial-GRPO（核心贡献）

基于两个人类空间认知观察：① 定量测量（距离）在镜像下不变；② 定性关系（in front of / next to）保持，而方向表达（left/right）需要对称调整。目标是让模型对原图和翻转图的回答语义一致。

- 定义视图一致性差距：\(\Delta = \mathtt{Avg}(\{r_i^s\}_{i=1}^{G}) - \mathtt{Avg}(\{\hat{r}_i^s\}_{i=1}^{G})\)（原图组与翻转图组的语义奖励均值差）。
- 修改奖励：当某组得分显著高于另一组时，给高分组扣分：
  \[ r_i^s = r_i^s - \eta\|\Delta\|, \quad \text{if } r_i^s > \delta \text{ and } \Delta \ge 0 \]
  翻转组对称处理（\(\delta=0.5\) 阈值，\(\eta=1\) 惩罚系数）——逼两组奖励收敛，模型必须“两个视角都说对”才能拿到高分。
- 优化目标：联合最大化原图+翻转图两组 rollouts 的期望奖励（\(\frac{1}{2G}\sum_{i=1}^{G}(R_i+\hat{R}_i)\)），PPO 式 clipped loss + KL 惩罚 \(\beta D_{\text{KL}}(\pi_\theta \| \pi_{\text{ref}})\)。

### 4. 训练与评测设置

- 基座：Qwen2.5-VL-3B；GRPO 组大小 \(G=8\)，最大生成长度 2048 tokens；梯度累积 2，每设备 batch 8；8×A6000。
- 训练数据：Vqasynth_Spacellava（28,000+ 多轮对话，拆成单轮 QA，含空间 VQA 与通用 VQA 混合）。
- 评测：Q-Spatial++（87 张真实图像、101 个专家标注的水平距离问题）；OOD 泛化用 OpenSpaces（5,000 QA）。
- 指标：success rate（\(\max(\text{GT}/\text{Pred},\text{Pred}/\text{GT}) < 2\) 算成功）、sMAPE（尺度不变误差）、mIoU 与 Accuracy@0.75（bbox 定位质量）、Yes/No 准确率。

## 效果怎么样？

- **Q-Spatial++ 上达到 58%**，比 SFT 基线提升超过 30 个百分点，幅度非常大；
- 远超开源模型 InternVL-2.5、Qwen2.5-VL，明显优于 Gemini-1.5-Flash，接近 GPT-4o；
- 推理路径可解释——模型输出中间推理步骤，能看出它"先定位物体，再判断关系"的轨迹。

**局限性**：GPT-4o 生成翻转 QA 的质量决定数据上限（多物体复杂场景仍可能出错）；镜像翻转只覆盖水平方向，真正的多视角（NeRF/3D 变换）一致性还没做；评测集中在空间 VQA，对更广的组合推理（属性+逻辑）未覆盖。

## 对谁有用？

- 做**空间推理、3D 理解**的研究者——R1 式 RL 在空间任务上的首个代表；
- 做**无标注奖励设计**的人——"视图一致性"是一个几乎零成本的验证器，不需要人工标注；
- 写综述时它属于"验证器奖励"方向的新形态：验证器从"答案对不对"进化成"换个视角还对不对"。

## 原文信息

- 来源：arXiv
- 链接：https://arxiv.org/abs/2506.01371
- 作者：Peiyao Wang, Haibin Ling
- 发表时间：2025 年 6 月（ICLR 2026）
- PDF 路径：papers/verifier/svqa-r1-reinforcing-spatial-reasoning.pdf
