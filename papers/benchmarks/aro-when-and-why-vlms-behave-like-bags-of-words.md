# When and why vision-language models behave like bags-of-words, and what to do about it?

> ARO：VLM 是"词袋模型"——5 万用例证明模型不绑属性、不辨关系、不看词序（Stanford，ICLR 2023 Oral）

## 这篇论文到底在解决什么问题？

VLM 在标准检索基准上表现不错，但论文提出了一个尖锐的怀疑：**高分可能是"假高分"**——现有检索任务存在 shortcut（捷径），模型即使完全不理解组合结构（属性绑定、关系、词序），靠"词袋"式的局部匹配也能通过。

为什么以前的方法不行？
- 既有组合基准规模小、负样本可 hack（模型用语言先验分辨）；
- 没人系统证明"模型到底有没有利用组合信息"。

这篇论文想改什么：**用 5 万+ 测试用例系统测三种组合结构（属性绑定、关系、词序），并证明模型是词袋模型 + 给出修复方案。**

## 他们怎么做的？

**核心 idea：构建大规模组合评测（5 万+ 用例），证明 VLM 对组合结构不敏感（词袋行为），并用组合感知的困难负样本挖掘（composition-aware hard negative mining）修复对比学习。** 技术流派：评测 + 训练数据改进。

1. **第一步：构建三个子集**（共 5 万+ 测试用例，比此前组合基准大几个数量级）：
   - **Visual Genome Attribution（属性绑定）**：图中有多个物体时，属性是否绑对物体（"红色杯子" vs 图里还有蓝盘子时）；
   - **Visual Genome Relation（关系）**：物体间关系（"猫在狗上面" vs "狗在猫上面"）；
   - **COCO & Flickr30k-Order（词序）**：词序敏感性（"人骑大象" vs "大象骑人"）。
2. **第二步：诊断**：在标准检索基准上对比"利用组合信息的模型"与"词袋式基线"，证明现有基准存在 shortcut——**不利用组合/顺序信息也能表现良好**（对比预训练优化的检索任务设计所致）；
3. **第三步：修复**：提出 composition-aware hard negative mining——在对比学习中主动挖掘"只在组合结构上不同的负样本"，简单修改即可显著提升顺序和组合性任务表现。

**评测模型**：CLIP、ViLT、ALIGN、BLIP 等主流 VLM。

**与同类方法的区别**：VALSE/CREPE 侧重"测"，ARO 同时给出"为什么高分是假的"（shortcut 分析）+ "怎么修"（负样本挖掘）；其 5 万+ 规模远超当时组合基准。

## 效果怎么样？

- 诊断结论：**VLM 类似 bag-of-words（词袋模型）**——对词序和组合结构不敏感；在属性绑定、关系、词序三类任务上全部显著落后于人类；
- 关键机制发现：现有检索基准的对比预训练目标允许 shortcut——模型不需要组合表示也能高分，**解释了"为什么模型不学组合"**（没有压力）；
- 修复有效：composition-aware hard negative mining 后，顺序和组合任务显著提升，且不影响标准检索性能。

**局限性**：评测基于 Visual Genome/COCO 的静态图文对；负样本挖掘是训练数据层面的修补，不改变模型架构；"词袋"结论对更新一代模型（BLIP-2、LLaVA 等）需重新验证。

## 对谁有用？

- 做 **VLM 评测方法学 / 对比学习改进**的人——shortcut 分析与负样本挖掘的经典；
- 综述定位：**Background 中"组合推理评测基准"的关键一环**——它证明"现有任务不逼模型学组合"，这直接引出"需要奖励信号主动干预"的必要性：评测不设压力，训练更没有压力，组合能力只能靠显式奖励逼出来。

## 原文信息

- 来源：arXiv
- 链接：https://arxiv.org/abs/2210.01936
- 作者：Mert Yuksekgonul, Federico Bianchi, Pratyusha Kalluri, Dan Jurafsky, James Zou
- 发表时间：2022 年 10 月（ICLR 2023 Oral）
- PDF 路径：papers/benchmarks/aro-when-and-why-vlms-behave-like-bags-of-words.pdf
