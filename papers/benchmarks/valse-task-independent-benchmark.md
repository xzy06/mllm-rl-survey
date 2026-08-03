# VALSE: A Task-Independent Benchmark for Vision and Language Models Centered on Linguistic Phenomena

> VALSE：围绕"语言现象"测 V&L 模型——伪造实例真/假判别（海德堡/都柏林等，ACL 2022）

## 这篇论文到底在解决什么问题？

VQA 和图文检索这类任务把模型能力"一锅烩"了——答对了一道题，说不清是看懂了图、猜中了统计规律、还是语言先验在帮忙。**单个语言现象（单复数、空间关系、共指）到底 grounding 得怎么样，现有评测根本测不出来。**

为什么以前的方法不行？
- VQA 是开放式答案，无法单独隔离"语言结构理解"这个变量；
- 检索类任务模型可以用语言先验 hack（后面 ARO 也证明了这点）。

这篇论文想改什么：**做一个任务无关（task-independent）的结构化评测**——围绕 6 种语言现象分别测试，用"伪造实例"（foiled instances）逼模型做严格的真/假判断。

## 他们怎么做的？

**核心 idea：对图像的真实描述做"最小修改"生成伪造描述（foil），让模型判断"描述与图像是否匹配"——每种语言现象单独一组测试，隔离出模型对特定语言结构的 grounding 能力。** 技术流派：基准构建（foiled instances 方法）。

1. **第一步：设计六项语言现象测试**（每项对应一个语言结构）：
   1. **存在性（Existence）**：图中是否有该物体；
   2. **复数（Plurality）**：单复数等数量表达；
   3. **计数（Counting）**：具体数量；
   4. **空间关系（Spatial Relations）**："左边/右边/上面"等；
   5. **动作（Actions）**：正在发生的动作；
   6. **实体共指（Entity Coreference）**：代词（他/她/它）是否指向正确的实体。
2. **第二步：构造伪造实例**：基于 COCO 的真实描述，用规则/模板生成最小修改的"假描述"（如把"左边"改成"右边"、单数改复数），配成"真实描述 vs 伪造描述"的判别任务；
3. **第三步：评测协议**：模型对每条描述输出"匹配/不匹配"二值判断，按语言现象分组报告准确率；评估了 5 个广泛使用的预训练 V&L 模型。

**与同类方法的区别**：VALSE 是**任务无关**的（不依赖 VQA/检索任务形式），只测"语言结构 grounding"这一个变量——这使它成为后续组合评测（SugarCrepe、ARO 等）的共同参照系。

## 效果怎么样？

- 5 个主流 V&L 模型在**存在性**上表现较好、**计数**尚可；
- 在**复数、空间关系、共指、动作**上普遍挣扎——这些恰是最需要"语言结构精确绑定"的现象；
- 结论：通用 V&L 模型的 grounding 是**不均匀的**，语言现象级测试能暴露出任务级评测看不到的短板。

**局限性**：伪造实例基于规则生成，存在"语言不自然/可被 hack"的 artifact（这正是 SugarCrepe 后来指出的问题）；只测判别不测生成；没有覆盖属性绑定（Attribution）这一核心组合维度。

## 对谁有用？

- 做 **V&L 评测方法学**的人——任务无关评测的奠基工作；
- 综述定位：**Background 中"组合推理评测基准"的起点**——它定义的语言现象清单（存在/复数/计数/空间/动作/共指）是"组合推理可操作化"的雏形，但缺了"属性绑定"这一维，后续 SugarCrepe/ARO 才补全。

## 原文信息

- 来源：arXiv
- 链接：https://arxiv.org/abs/2112.07566
- 作者：Letitia Parcalabescu, Michele Cafagna, Lilitta Muradjan, Anette Frank, Iacer Calixto, Albert Gatt
- 发表时间：2021 年 12 月（ACL 2022 Main）
- PDF 路径：papers/benchmarks/valse-task-independent-benchmark.pdf
