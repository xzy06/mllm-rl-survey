# H-GRPO: Permutation-Invariant Reinforcement Learning for Grounded Visual Reasoning

> H-GRPO：排列不变的 grounded 推理强化学习（新加坡 A*STAR + IIT Kharagpur，2026）

## 这篇论文到底在解决什么问题？

**RL 后训练可能让 VLM 的推理"作弊"而不是"看图"。** 论文指出了一个尖锐的矛盾：模型答案正确率很高，但推理并不忠实（faithful）——它可能靠虚假相关、忽略视觉证据、甚至幻觉中间事实来凑出正确答案。而 RL 优化最终答案正确性时，**会放大这种捷径推理**（shortcut reasoning）：只要答对就有奖励，管你怎么答的。

以前的方法有什么问题？

- 视觉 CoT 方法（Visual CoT、Multimodal-CoT 等）主要在**语言空间**监督推理，推理步骤没有锚定到图像局部证据——"看起来有道理但图里根本没这回事"；
- R1 式 RL（R1-VL 的 StepGRPO、Vision-R1 等）要么只评估文本推理轨迹，要么只评估最终答案，**没有强制每一步都落到图像区域**；
- ViGoRL、Vision-SR1 做了 grounding，但推理形式是自由文本，**不同模型解决同一问题的方式不同、步骤顺序不同**——用固定顺序的参考链去比对，会冤枉正确的推理。

## 他们怎么做的？

**核心 idea：把推理强制结构化为"（子问题, 子答案, 证据框）"三元组序列，再用匈牙利匹配（bipartite matching）实现排列不变的奖励——推理步骤顺序不同但语义一致，照样给分。数学上 GRPO 是 H-GRPO 的特例（对角匹配退化为 GRPO）。** 技术流派：GRPO 变体（匈牙利匹配过程奖励）+ 结构化推理分解协议 + 数据合成管线。

### 第一步：Grounded 推理分解协议

模型输出：

$$ y = \{\tau_1, \ldots, \tau_m, r, a^{\text{final}}\}, \quad \tau_i = \langle q_i, a_i, b_i \rangle $$

每个推理步骤是一个三元组 τ_i：子问题 q_i（这一步要验证什么）、中间答案 a_i（推断出的事实）、证据框 b_i = [x_min, y_min, x_max, y_max]（支撑证据在哪）。最后综合出推理路径 r（自然语言总结）+ 最终答案 a^final。每一步"问什么、答什么、看哪儿"都显式可查。

### 第二步：匈牙利匹配（排列不变的步骤对齐）

预测三元组集合 D̂ = {τ̂_1,...,τ̂_m} 和参考三元组集合 D* = {τ*_1,...,τ*_n} 之间建二分图匹配，相似度矩阵每项：

$$ S_{ij} = \frac{1}{4}\Big(E(\hat{b}_i, b_j^*) + \text{sim}_q(\hat{q}_i, q_j^*) + \text{sim}_a(\hat{a}_i, a_j^*) + \text{IoU}(\hat{b}_i, b_j^*)\Big) $$

四个分量：
- **E(b̂_i, b*_j)**：预测框存在且与参考证据区域兼容；
- **sim_q / sim_a**：子问题、子答案的 Sentence-BERT 余弦相似度（语义对齐）；
- **IoU**：预测框与参考框的空间重叠（视觉 grounding）。

m ≠ n 时把矩阵 padding 到 k×k（k = max(m,n)），解一对一匹配约束（每行每列至多一个匹配）：

$$ X^* = \arg\max_X \sum_{i=1}^{k}\sum_{j=1}^{k} S_{ij} x_{ij}, \quad \text{s.t. } \sum_j x_{ij} \le 1,\ \sum_i x_{ij} \le 1 $$

最终匈牙利得分：

$$ S_{\text{HS}} = \frac{1}{\min(m,n)} \sum_{(i,j) \in \mathcal{M}} S_{ij} $$

### 第三步：总奖励（答案奖励被匈牙利奖励门控）

$$ \mathcal{R} = \alpha \mathcal{R}_{\text{format}} + \beta \mathcal{R}_{\text{answer}} \cdot \mathcal{R}_{\text{HS}} $$

- **格式奖励** R_format = 1/3(𝕀_pair + 𝕀_reason + 𝕀_final)：
  - 𝕀_pair = 𝟙[count(子问题标签) = count(子答案标签) ∧ count > 0]——子问题必须和子答案成对且至少一对；
  - 𝕀_reason：有显式推理路径；
  - 𝕀_final：有最终答案；
- **最终答案奖励** R_answer = 1（答案精确匹配）否则 0；
- **匈牙利推理奖励** R_HS = max(0, S_HS − γ)：γ 是质量阈值，低于阈值的弱/grounding 差的轨迹直接得 0——抑制"凑答案"的推理。

关键设计：**答案奖励 × 匈牙利奖励**——只有"答对了 且 中间推理步骤语义对齐、证据 grounding 到位"才拿到完整奖励；光答对但推理是编的，奖励会被门控掉。

### 第四步：数据合成 + 训练

- **GVRS 数据合成管线**：GPT-4o 起草 + 人工校验 + SAM3 框精化构建 40 个金标准参考示例 → 3 个 LLM（GPT-4o、Gemini-3、Qwen3.5-Omni-Plus）生成 12 个候选系统提示、按组合奖励择优，扩出 10,000 条带逐步 grounding 的训练样本（来源：Visual7W、Visual-CoT、A-OKVQA、ERQA），人工抽查 100 例；
- **两阶段训练**：先 SFT 一个 epoch（学输出格式 + grounded 分解的行为先验）→ 再 GRPO RL（G=8 rollouts/样本）；
- **超参**：lr 5e-6、warm-up ratio 0.03、weight decay 0.01（两阶段相同）；
- **基座**：Qwen2.5-VL-3B（强模型）+ SmolVLM-2.2B（小模型）——验证过程奖励对小模型是否更有用。

### 评测协议

统一评测四个维度：最终答案正确性、grounding 保真度、逐步推理对齐、对视觉证据的依赖度——避免"只刷准确率"的假象。in-domain：A-OKVQA / Visual7W；OOD：MMMU / RealWorldQA / RoboSpatial / MMStar。可解释性用 Gemini 3 Flash 当裁判，五维（相关性/连贯性/一致性/清晰度/整体）1-5 分。

### 与同类方法的区别

对比 ViGoRL（MCTS 生成 grounded 轨迹 + 动态缩放）、Vision-SR1（感知与推理分离），H-GRPO 是第一个把推理形式化为"子问题-子答案-证据框"三元组、并用排列不变匹配做过程奖励的——不要求固定推理顺序，对多解推理路径公平。

## 效果怎么样？

- **小模型受益最大**：SmolVLM-2.2B 上，SFT 提升有限、普通 GRPO 增益不稳定，而 H-GRPO 把 A-OKVQA 提到 73.4%、Visual7W 提到 77.2%——稀疏最终答案奖励对小模型不够，匈牙利过程奖励提供了有用的中间监督；
- Qwen2.5-VL-3B：A-OKVQA 82.8%、Visual7W 83.9%，在 Visual7W（定位敏感任务）上超过普通 GRPO；
- **OOD 泛化**：在 RealWorldQA、RoboSpatial、MMStar 上取得最佳，其中 RoboSpatial 70.2% 增益最大——grounding 中间步骤帮助模型在分布偏移下保持空间约束；
- 揭示了此前方法的"推理与 grounding 此消彼长"（trade-off），而 H-GRPO 两维度同时提升。

**局限性**：MMMU（知识密集型）提升有限——它擅长视觉/空间推理，不擅长需要广泛科学知识的任务；匈牙利匹配的计算开销比 GRPO 大；参考推理链的生成质量决定奖励上限。

## 对谁有用？

- 做**过程级 RL、grounding 监督**的人——"排列不变的步骤匹配奖励"是奖励设计的重要新机制；
- 做**可验证推理（faithful reasoning）**的人——它把"每一步都有证据"从口号变成了可评测指标；
- 写综述时它是"推理过程优化"方向的深化：奖励对齐的粒度从"最终答案/单证据框"细化到"逐步三元组"，且解决了多解推理路径的评估难题。

## 原文信息

- 来源：arXiv
- 链接：https://arxiv.org/abs/2606.29915
- 作者：Eric Peh, Debaditya Roy, Basura Fernando
- 发表时间：2026 年 6 月
- PDF 路径：papers/process/h-grpo-permutation-invariant-reinforcement-learning.pdf
