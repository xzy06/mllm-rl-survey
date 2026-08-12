# SpatialThinker: Reinforcing Scene Graph-Grounded Spatial Reasoning via Dense Rewards

> SpatialThinker：用稠密奖励强化场景图落地的空间推理（牛津大学 + UC Santa Cruz，NeurIPS 2025）

## 这篇论文到底在解决什么问题？

**MLLM 的空间推理很弱，尤其到了 3D 场景更弱**。模型能认出"桌上有个杯子"，但问它"杯子在桌子的左边还是右边""从侧面看这个布局是什么样的"就经常答错。空间推理对机器人操作、导航、AR 这类具身 AI 任务至关重要。

**为什么难？** 两个原因：

1. **现有 RL 只用"答案对不对"这个稀疏奖励**。答对了给 1 分，答错了给 0 分，模型不知道推理过程哪里错了，只能瞎试，学到的还是静态套路。
2. **场景图（scene graph）这个天然的结构化信息没被用进推理过程**。以前的方法要么把场景图当离线数据清洗工具（生成训练数据），要么把它当成独立的生成任务（和下游推理脱节），从来没有让模型"边生成场景图边推理"。

## 他们怎么做的？

**核心 idea：让场景图生成和空间推理在同一个前向过程中端到端完成（一个模型“感知→定位→推理→回答”一步到位），并用稠密的多目标奖励（lexicographic gating）引导。**

### 1. 方法总览

模型必须按固定模板输出：`<observe>`（场景描述）→ `<scene>`（问题相关的区域场景图，JSON 格式：物体+bbox+关系三元组）→ `<think>`（显式推理）→ `<answer>`（答案）。场景图不再是离线工具，而是推理链的中间产物——每一步推理都被“钉”在图像结构上。

### 2. 稠密多目标奖励（四分量 + lexicographic gating）

总奖励公式：

$$ R_{\text{total}} = \mathbb{I}[R_{\text{format}}=1]\cdot\Big(w_{\text{format}}R_f + w_{\text{count}}R_c + w_{\text{accuracy}}R_a \mathbb{I}[R_{\text{accuracy}}=1]\,w_{\text{spatial}}R_s\Big) $$

四个分量逐个说明：

- **格式奖励**（权重 $w_{\text{format}}=0.1$）：验证 `<scene>` 里的 JSON 可解析、每个物体有 ID 和 bbox、所有关系是合法的（主体-谓词-客体）三元组。这是硬门槛——格式不对整个奖励归零。
- **计数奖励**（权重 $w_{\text{count}}=0.2$）：
  $$ R_{\text{count}} = w_{\text{count}}\cdot\Big(\lambda_{\text{obj}}\cdot\max(0,\,1-\frac{|N_{\text{obj}}^{\text{pred}}-N_{\text{obj}}^{\text{gt}}|}{\max(N_{\text{obj}}^{\text{gt}},1)}) + \lambda_{\text{rel}}\cdot\max(0,\,1-\frac{|N_{\text{rel}}^{\text{pred}}-N_{\text{rel}}^{\text{gt}}|}{\max(N_{\text{rel}}^{\text{gt}},1)})\Big) $$
  其中 $\lambda_{\text{obj}}=0.7$、$\lambda_{\text{rel}}=0.3$。同时惩罚多生成和漏生成——论文明确说，**没有它模型会 reward hacking**：为了蒙对空间奖励，疯狂多生成物体和关系。
- **准确率奖励**（权重 $w_{\text{accuracy}}=0.5$）：最终答案与 ground truth 精确字符串匹配（数据集是多选题，所以匹配是确定性的）。权重最高，保证“先答对”优先。
- **空间奖励**（权重 $w_{\text{spatial}}=0.2$）：**只有在答案正确时才计算**。预测物体和真实物体用匈牙利算法做二分图匹配，代价函数是 CIoU + 语义相似度：
  $$ C(o_i^{\text{pred}}, o_j^{\text{gt}}) = \lambda_{\text{spatial}}(1-\text{IoU}(b_i,b_j)) + \lambda_{\text{semantic}}(1-\text{sim}(l_i,l_j)) $$
  其中 $\lambda_{\text{spatial}}=1.0$、$\lambda_{\text{semantic}}=2.0$；奖励 = 匹配对平均 CIoU（CIoU 对不重叠框也提供稠密梯度，因为包含距离和宽高比项）。
- **Lexicographic gating（优先级）**：format ≻ {count, accuracy} ≻ spatial——先满足格式，再联合优化计数和准确率，空间奖励只在答案正确时生效。论文指出，不加这个门控，模型会过度优化中间的空间奖励而牺牲最终答案正确性。

### 3. STVQA-7K 数据集

- **来源**：Visual Genome 的人工标注场景图，共 7,587 条空间多选题，覆盖 2D+3D，九类推理：关系、尺寸、朝向、距离、深度、可达性、位置、计数、存在性。
- **关系扩充**：在 VG150 的 50 个标准谓词外新增 34 个空间关系（near/far、bigger/taller、facing away、inside/beneath 等）。
- **生成与质量控制**：Claude Sonnet 4 生成 QA，再由 GPT-4o 用 pass@2 一致性做**双 LLM 交叉校验**（带来 +13% 准确率提升），从初始 56,224 题筛出 7,587 题。
- **局部监督**：按词元匹配提取每题相关的场景子图作为局部监督，bbox 保留绝对像素坐标（保留真实尺度供 CIoU 计算）。管线可扩展到 ~108K 样本。

### 4. 训练细节

- 基座：Qwen2.5-VL-3B / 7B（全参数更新，**没有 SFT 冷启动**）+ Qwen3-VL-30B（LoRA rank 64）。
- GRPO 在线 RL：每问采样 88 条 rollout，温度 1.0，上下文 16,384 tokens；rollout batch 512，global batch 128，训练 75 步（5 episodes）。
- 超参：lr 1e-6，AdamW + bf16，权重衰减 1e-2，KL 惩罚系数 1e-2，clip 范围 $\epsilon_l=0.2$、$\epsilon_h=0.3$。
- 输入分辨率 512×512 到 2048×2048（保细粒度空间信息）；4×H100，3B 约 13 小时、7B 约 15 小时。
- 推理开销：场景子图平均只增加 ~120 tokens，几乎不拖慢推理。

## 效果怎么样？

- **7B 模型只用 7K 样本**，在 14 个基准上平均超过 GPT-4o（+4.7%）、Claude 3.5 Sonnet（+9.6%）、Claude 4 Sonnet（+1.8%），逼近 GPT-5（-0.9%）。
- **稠密奖励 vs 稀疏奖励**：稀疏 RL 提升 +4.4%，稠密空间奖励提升 +7.7%，几乎是 1.7 倍——证明"只看答案对错"的奖励确实喂不饱空间推理。
- **OOD 泛化是最大亮点**：稀疏 RL 在真实世界 VQA 上只和 SFT 持平（+2.7% vs +2.9%），而 SpatialThinker 达到 +5.2%，说明稠密结构化奖励学到的是可迁移的推理方式，不是死记训练分布。
- **Scaling 有效**：30B 版本平均超过 GPT-5（+3.0%），CV-Bench 3D 达到 93.6%。

**局限性**：训练需要场景图标注（合成数据），模板强制格式让推理路径自由度受限；数学等知识密集型任务不是它的主场。

## 对谁有用？

- 做**空间/3D 推理、场景图、具身智能**的研究者——这是"结构化稠密奖励"路线的代表作；
- 做**RLVR 奖励设计**的人——它演示了把答案级稀疏奖励升级为"格式+结构+定位"稠密奖励的完整配方；
- 写综述时它是"验证器奖励→结构级验证"的典型：验证的不再只是答案，而是推理过程中的场景图结构。

## 原文信息

- 来源：arXiv
- 链接：https://arxiv.org/abs/2511.07403
- 作者：Hunar Batra, Haoqin Tu, Hardy Chen, Yuanze Lin, Cihang Xie, Ronald Clark
- 发表时间：2025 年 11 月（NeurIPS 2025）
- PDF 路径：papers/verifier/spatialthinker-reinforcing-scene-graph-grounded-spatial-reasoning.pdf
