# MM-CondChain: A Programmatically Verified Benchmark for Visually Grounded Deep Compositional Reasoning

> MM-CondChain：程序化可验证的"深度组合推理"评测基准（arXiv 2026）

## 这篇论文到底在解决什么问题？

MLLM 越来越多地被用来执行**视觉工作流**，比如操作 GUI：下一步动作取决于"屏幕上是否弹出了权限对话框，并且界面是绿色的，就点 Allow；否则点 Cancel"这样的**组合条件**。这类任务里，多个物体/属性/关系要组合起来判断，而且判断结果决定流程分支，甚至可能中途提前终止。

**但现有基准根本测不了这种能力**：要么只测浅层组合（一两步），要么测的是互相独立的约束，没有"条件链式"的深度嵌套组合。

一句话：**深度组合推理（deep compositional reasoning）的正确性，没有一个可靠的评测手段。**

## 他们怎么做的？

**核心 idea：把“逻辑构造”和“语言渲染”解耦——先用可执行程序（VPIR）把每层组合条件构造出来并机械验证，再翻译成自然语言。语言可能骗人，代码不会。**

### 1. 管线总览（VPIR-based agentic synthesis）

多模态输入（自然图像 / 图表 / GUI 轨迹）→ Planner 逐层扩展条件链 → 每层四阶段（见下）→ 每层必须通过程序验证才能继续扩展 → Composer 把验证过的链编译成配对测试实例。

### 2. 逐层 VPIR 合成（每层四步）

1. **选择关系策略 \(r_t\)**：约束主体如何转移（如“从物体到其属性”“从 GUI 状态到控件”）。
2. **提取结构化事实 \(F_t\)**：类型化键值映射 \(\{(k, v_k)\}\)——key 是视觉属性维度（color、spatial_relation、count、gui_state），value 是类型化观察值（red、left-of、50、list-layout），以 JSON 兼容类型存储并暴露为变量。
3. **生成 VPIR 谓词对 \((p_t, \tilde{p}_t)\)**：true-logic + 反事实 false-logic。在沙箱环境 \(\text{Env}(F_t)\) 中执行，**只允许白名单原语**（len、set、all、any、min/max/sum），保证确定性：
   \[ \llbracket p \rrbracket(F_t) \triangleq \text{Exec}(p; \text{Env}(F_t)) \in \{0,1\} \]
   谓词只有在机械执行下成立才被接受——彻底排除逻辑不一致和不可验证的 claim。
4. **LLM Translator 渲染**：把验证过的可执行逻辑翻译成自然语言条件文本（true 版 \(c_t\) + 反事实版 \(\tilde{c}_t\)），再做表达级验证（流畅、无歧义、忠于 VPIR 语义）。

### 3. Planner / Verifier / Composer 分工

- **Planner**：决定链是扩展、终止还是回滚（每层验证通过才能继续）。
- **Verifier**：质量把关（渲染是否忠于已验证的 VPIR 语义）。
- **Composer**：把验证过的链编译成**配对实例**——True-path（所有条件都成立，走完整路径）+ False-path（把某一层条件替换成最小扰动的反事实，触发提前终止）。这种“近同构”设计产生 **hard negatives**：两个实例视觉上几乎一样，只有一处条件不同，模型必须精确验证组合条件才能区分。

### 4. 基准规模与评测

- 三个视觉域：自然图像、数据图表、GUI 轨迹（各域有适配的视觉事实提取方式）。
- 评测指标 **Path F1**：模型必须走对整条条件链的执行路径（每层条件判断正确且最终结果正确）才算有效，对部分正确按 F1 计分——比单点答案准确率严格得多。
- 共评测 10 个 MLLM。

## 效果怎么样？

- **最强模型也只拿到 53.33 Path F1**——连 SOTA 都刚过及格线，说明深度组合推理确实是 MLLM 的硬伤；
- **hard negatives（精心构造的干扰项）上分数断崖式下跌**——模型容易看到部分条件满足就草率回答；
- **链深度和谓词复杂度增加时性能急剧下降**——模型"组合"的能力和链长成反比，这正是组合推理短板的直接证据。

**对研究界的意义**：它证明了深度组合推理的正确性**可以被程序化验证**（因为条件链是离散逻辑结构），这为"可验证奖励"（RLVR）提供了新燃料——组合推理的奖励信号不必依赖 LLM 裁判或人工标注。

## 对谁有用？

- 做**GUI 智能体、视觉工作流执行**的人——这是直接相关的评测集；
- 做**组合推理 RL** 的人——它提供了"可验证奖励"的落地场景；
- 写综述时它是 Discussion 部分的关键论据：**"组合正确性正变得可验证"**，这正是奖励信号从结果验证走向规则化验证的前提条件。

## 原文信息

- 来源：arXiv
- 链接：https://arxiv.org/abs/2603.12266
- 作者：Haozhan Shen, Shilin Yan, Hongwei Xue, Shuaiqi Lu, Xiaojun Tang, Guannan Zhang, Tiancheng Zhao, Jianwei Yin
- 发表时间：2026 年 3 月
- PDF 路径：papers/verifier/mm-condchain-programmatically-verified-benchmark.pdf
