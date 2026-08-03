# 核心方向补充调研 — 比原 7 篇更贴合/更新的论文

> 调研日期：2026-08-03
> 目的：检查是否存在比用户原 7 篇核心论文（CR³、SpatialThinker、Ground-R1、GRIT、POLIA、Self-Questioning VLM、H-GRPO）更贴合"奖励信号演进"方向或更新的论文
> 来源：Awesome-Multimodal-Reasoning 论文清单 + arXiv 搜索
>
> **修正记录（2026-08-03 二次核查）**：逐篇核对评测集后——① 结构修正为**用户的三分法**（3.1 验证器 / 3.2 视觉对齐 / 3.3 推理过程），不再分四类；② **VisualPRM 降级**为 Background 引用（评测集为 MMMU/MathVision/MathVerse 等数学推理基准，不含组合推理）；③ **AlphaGRPO 仅作 Future 思想引用**（面向文生图/编辑生成任务，非组合理解）；④ **Saliency-R1、DLR 列为补充引用**（机制贴合 thesis，但评测集未显式含组合推理）；⑤ 核心新增仅 **SVQA-R1** 一篇；⑥ **MM-CondChain 降级**为 Discussion 论据（评测基准/造题，无 RL 方法贡献，不放主体）

---

## 一、高度推荐补充的论文（与论文 thesis 直接相关）

### 1. VisualPRM — 多模态过程奖励模型（推荐度：★★★☆☆ → 已降级为 Background 引用）

- **论文**：VisualPRM: An Effective Process Reward Model for Multimodal Reasoning（arXiv:2503.10291，2025 年 3 月，引用 131+）
- **定位**：8B 参数的多模态过程奖励模型，是目前多模态 PRM 的代表性工作
- **核心贡献**：
  - 构建了多模态过程监督数据集（含标注的推理步骤级反馈）
  - 训练 8B 的 PRM 用于 Best-of-N 推理时扩展（test-time scaling）
  - 显著提升现有 MLLM 的推理能力
- **与论文的关系**（**已降级**）：不放入核心方法章节。逐篇核查发现其评测集为 **MMMU、MathVision、MathVerse、DynaMath、WeMath——全部是数学推理基准**，不含组合推理评测（VALSE/SugarCrepe/ARO 等）。仅在 Background 中作为"多模态 PRM 技术路线"的引入文献引用

### 2. Saliency-R1 — 显著性图对齐奖励（推荐度：★★★★☆ → 3.2 补充引用）

- **论文**：Saliency-R1: Enforcing Interpretable and Faithful Vision-language Reasoning via Saliency-map Alignment Reward（arXiv:2604.04500，CVPR 2026）
- **定位**：将模型推理时的注意力/显著性图（saliency map）与视觉证据对齐，作为奖励信号
- **核心贡献**：
  - 引入显著性图对齐奖励：模型回答问题时，其关注的图像区域必须与问题相关的显著性区域一致
  - 同时提升推理的可解释性（interpretability）和忠实度（faithfulness）
- **与论文的关系**（**补充引用，不单独成节**）：归入 3.2 视觉对齐奖励。奖励机制贴合 thesis（saliency-map 对齐=视觉语义结构对齐的直接体现），训练数据含 relation reasoning、评测含 OpenPSG（场景图关系，算部分相关）；但核心目标是 faithfulness/interpretability，非显式组合逻辑

### 3. SVQA-R1 — 空间推理的 GRPO 变体（推荐度：★★★★★ → 3.1 核心新增 ✅）

- **论文**：SVQA-R1: Reinforcing Spatial Reasoning in MLLMs via View-Consistent Reward Optimization（arXiv:2506.01371，ICLR 2026，引用 14+）
- **定位**：首个将 R1 式训练扩展到空间 VQA 的工作
- **核心贡献**：
  - 提出 **Spatial-GRPO**：在 GRPO 基础上引入视图一致性奖励（view-consistent reward）——同一场景从不同视角提问，回答必须一致
  - 在空间 VQA 基准上大幅提升准确率，且推理路径可解释
- **与论文的关系**（**核心新增 ✅**）：归入 3.1 验证器奖励——视图一致性奖励本质是**空间一致性验证**。显式优化空间 VQA（空间关系正是 thesis 中组合推理的子问题之一），Spatial-GRPO 的奖励信号不依赖外部标注，支撑"空间逻辑推理"子问题

### 4. AlphaGRPO — 分解式可验证奖励（推荐度：★★☆☆☆ → 已降级，仅 Future 思想引用）

- **论文**：AlphaGRPO: Unlocking Self-Reflective Multimodal Generation in Unified Multimodal Models via Decompositional Verifiable Reward（arXiv:2605.12495，ICML 2026）
- **定位**：将 GRPO 应用于统一多模态生成模型（AR-Diffusion UMM），提出分解式可验证奖励（Decompositional Verifiable Reward, DVReward）
- **核心贡献**：
  - 将复杂提示分解为可验证的语义子奖励和质量子奖励
  - 支持推理式文生图（Reasoning T2I）和自我反思修正（Self-Reflective Refinement）
- **与论文的关系**（**已降级**）：**不单独成节**。面向**生成任务**（文生图、图像编辑，评测 GenEval/DPG-Bench/WISE，均为生成质量基准），非组合理解。仅在 Future Directions 提一句"分解式可验证奖励"思想

### 5. MM-CondChain — 程序化验证的深度组合推理基准（推荐度：★★★★☆ → 已降级，仅 Background/Discussion 引用）

- **论文**：MM-CondChain: A Programmatically Verified Benchmark for Visually Grounded Deep Compositional Reasoning（arXiv:2603.12266，2026 年 3 月）
- **定位**：首个"程序化可验证"的视觉 grounding 深度组合推理基准，多层控制流（conditional workflows）
- **核心贡献**：条件链式推理（如"若弹出权限对话框且界面为绿色，则点击允许"），答案可由程序自动验证
- **与论文的关系**（**已降级**）：**不放入 3.1 方法主体**。它是评测基准（造题）而非解题方法——无 RL 方法/奖励设计贡献。价值保留在两点：(1) Background 中作为"程序化可验证的组合推理基准"一句带过；(2) Discussion 中作为论据：深度组合推理的正确性可以被程序化验证——奖励信号能走向规则化的前提。**注意边界**：其"程序化验证"是逻辑层面的（MLLM 提取事实 + 代码验证逻辑），自然图像域的感知事实无人工核对

### 6. Decompose, Look, and Reason (DLR) — 强化潜在推理（推荐度：★★★☆☆ → 3.3 补充引用）

- **论文**：Decompose, Look, and Reason: Reinforced Latent Reasoning for VLMs（arXiv:2604.07518，2026 年 4 月）
- **定位**：强化潜在推理框架，动态将查询分解为文本前提
- **核心贡献**：将"分解"作为可学习的推理行为，用 RL 强化——模型学会先分解问题，再看图，再推理
- **与论文的关系**（**补充引用，不单独成节**）：归入 3.3 推理过程优化。"分解查询→看→推理"机制上是组合推理核心操作（与 Self-Questioning VLM 同源），但评测集为通用 vision-centric benchmarks，未显式含组合推理

---

## 二、可选的补充论文（相关性中等，用于充实章节）

### 7. GRPO-CARE — 一致性感知 RL（推荐度：★★★☆☆）

- **论文**：GRPO-CARE: Consistency-Aware Reinforcement Learning for Multimodal Reasoning（arXiv:2506.16141，ACL Findings 2026，引用 48+）
- **核心**：两层奖励——基础正确性奖励 + 自适应一致性奖励（答案与推理的连贯性），不需要显式监督
- **与论文的关系**：一致性奖励是"奖励信号设计"的另一种新维度（不同于视觉对齐、过程级），可以放在 Future Directions 中作为讨论点

### 8. STAR-R1 — 多视角空间变换推理（推荐度：★★★☆☆）

- **论文**：STAR-R1: Multi-View Spatial Transformation Reasoning by Reinforcing Multimodal LLMs（CVPR 2026）
- **核心**：先学习结构化空间推理轨迹，再用参照关系的细粒度奖励（fine-grained rewards on referential relations）
- **与论文的关系**：与 SpatialThinker、SVQA-R1 形成空间推理方法群，可归入"验证器奖励"或"视觉对齐"的讨论中

### 9. StructVRM — 结构化可验证奖励模型（推荐度：★★★☆☆）

- **论文**：StructVRM: Aligning Multimodal Reasoning with Structured and Verifiable Reward Models（2025 年 8 月）
- **核心**：用结构化、可验证的奖励模型对齐多模态推理
- **与论文的关系**：PRM 与 verifiable reward 的交叉，可充实 3.2/3.3b 的讨论

### 10. Perception-Grounded Policy Optimization（推荐度：★★★☆☆）

- **论文**：Not All Tokens See Equally: Perception-Grounded Policy Optimization for Large Vision-Language Models（2026 年 4 月）
- **核心**：从优化目标角度（而非奖励设计角度）让策略感知视觉输入，处理 RLVR 中"文本偏置"问题
- **与论文的关系**：与 H-GRPO 解决的问题相同（模型忽略图像），但改的是优化目标。可作为 3.3b 的对照方法

---

## 三、与用户原 7 篇的对比结论

### 建议补充进论文的（1 篇核心新增 ✅ + 2 篇补充引用 ⚠️ + 3 篇降级 ❌）

| 论文 | 归入章节 | 贴合度判定依据 |
|------|---------|--------------|
| **SVQA-R1** (2506.01371) | **3.1 验证器（核心新增 ✅）** | 显式优化空间推理——组合推理子问题；视图一致性=空间一致性验证 |
| **MM-CondChain** (2603.12266) | Discussion 论据 + Background（降级 ❌） | 评测基准（造题）非解题方法，无 RL 贡献；仅"组合正确性可程序验证"论据 |
| **Saliency-R1** (2604.04500) | 3.2 视觉对齐（补充引用 ⚠️） | 显著性对齐奖励贴合 thesis；评测含 OpenPSG 关系推理但非显式组合 |
| **DLR** (2604.07518) | 3.3 推理过程（补充引用 ⚠️） | 分解+推理机制贴合；评测集为通用 vision-centric，非组合推理 |
| **VisualPRM** (2503.10291) | Background（降级 ❌） | 评测集全为数学推理基准（MMMU/MathVerse 等），不含组合推理 |
| **AlphaGRPO** (2605.12495) | Future 思想引用（降级 ❌） | 面向生成任务（GenEval/DPG-Bench），非组合理解 |

### 建议不补充的

- **GRPO-CARE、STAR-R1、StructVRM、Perception-Grounded PO**：与主线重叠度高或偏应用（GUI/医学），可以作为引用但不值得单独成节

### 对论文结构的影响

论文结构**保持用户的三分法不变**，仅更新成员：

```
3.1 验证器奖励（Verifier-based）：CR³、SpatialThinker、SVQA-R1（新✅）
3.2 视觉对齐奖励（Grounded）：Ground-R1、GRIT、POLIA、Saliency-R1（新⚠️，补充引用）
3.3 推理过程优化（Process）：Self-Questioning VLM、H-GRPO、DLR（新⚠️，补充引用）
4. Discussion：MM-CondChain——"组合正确性正变得可验证"论据
Background：VisualPRM（多模态 PRM 技术路线引入）
Future：AlphaGRPO（分解式可验证奖励思想）
```

> 核心论文共 **8 篇**（原 7 篇 + SVQA-R1），Saliency-R1/DLR 为补充引用，MM-CondChain/VisualPRM/AlphaGRPO 降级（MM-CondChain 仅作 Discussion 论据）。

---

## 附：本次新增文献清单

| # | 论文 | arXiv ID | 年份 |
|---|------|----------|------|
| 1 | VisualPRM: An Effective Process Reward Model for Multimodal Reasoning | 2503.10291 | 2025 |
| 2 | SVQA-R1: Reinforcing Spatial Reasoning in MLLMs via View-Consistent Reward Optimization | 2506.01371 | 2025 |
| 3 | GRPO-CARE: Consistency-Aware RL for Multimodal Reasoning | 2506.16141 | 2025 |
| 4 | MM-CondChain: Programmatically Verified Benchmark for Deep Compositional Reasoning | 2603.12266 | 2026 |
| 5 | Saliency-R1: Saliency-map Alignment Reward | 2604.04500 | 2026 |
| 6 | Decompose, Look, and Reason: Reinforced Latent Reasoning for VLMs | 2604.07518 | 2026 |
| 7 | AlphaGRPO: Decompositional Verifiable Reward | 2605.12495 | 2026 |
