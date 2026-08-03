# Qoder 个人级技能完整指南

> 安装路径：`~/.qoder/skills/`
> 技能总数：18 个
> 更新日期：2026-08-03

---

## 目录

- [技能调用方式](#技能调用方式)
- [一、工程流程类（12 个）](#一工程流程类12-个)
  - [1. ask-matt — 技能路由器](#1-ask-matt--技能路由器)
  - [2. grill-with-docs — 拷问+文档生成](#2-grill-with-docs--拷问文档生成)
  - [3. to-spec — 生成规格文档](#3-to-spec--生成规格文档)
  - [4. implement — 按规格实现](#4-implement--按规格实现)
  - [5. diagnosing-bugs — 系统化调试](#5-diagnosing-bugs--系统化调试)
  - [6. prototype — 一次性原型](#6-prototype--一次性原型)
  - [7. research — 后台调研](#7-research--后台调研)
  - [8. codebase-design — 深模块设计词汇](#8-codebase-design--深模块设计词汇)
  - [9. domain-modeling — 领域建模](#9-domain-modeling--领域建模)
  - [10. code-review — 双轴代码审查](#10-code-review--双轴代码审查)
  - [11. resolving-merge-conflicts — 解决合并冲突](#11-resolving-merge-conflicts--解决合并冲突)
  - [12. improve-codebase-architecture — 架构深化扫描](#12-improve-codebase-architecture--架构深化扫描)
- [二、生产力类（5 个）](#二生产力类5-个)
  - [13. grill-me — 触发拷问](#13-grill-me--触发拷问)
  - [14. grilling — 拷问循环](#14-grilling--拷问循环)
  - [15. handoff — 交接文档](#15-handoff--交接文档)
  - [16. teach — 多会话教学](#16-teach--多会话教学)
  - [17. writing-great-skills — 技能写作参考](#17-writing-great-skills--技能写作参考)
- [三、自定义技能（1 个）](#三自定义技能1-个)
  - [18. paper-research — 论文搜索与概括](#18-paper-research--论文搜索与概括)
- [推荐工作流组合](#推荐工作流组合)

---

## 技能调用方式

在 Qoder 中有两种触发方式：

- **自动触发**：agent 根据 `description` 中的触发条件自动激活
- **手动触发**：输入 `/技能名` 显式调用

---

## 一、工程流程类（12 个）

### 1. ask-matt — 技能路由器

**作用**：当你不确定该用哪个技能时，它推荐合适的技能或工作流。

**何时用**：面对一个任务不知道从哪开始，或者想了解正确的工作流程。

**用法**：`/ask-matt`，然后描述你的情况，例如：

```
/ask-matt 我有一个新功能想法，但还不确定怎么开始
```

---

### 2. grill-with-docs — 拷问+文档生成

**作用**：relentless 地提问来打磨你的计划或设计，同时在过程中生成 ADR（架构决策记录）和词汇表。

**何时用**：有代码库，想在开始编码前与 agent 对齐设计方向。

**用法**：`/grill-with-docs`，然后描述你想做什么。agent 会逐个提问，每个问题都附上推荐答案，你确认后再继续。

**典型工作流**：

```
grill-with-docs → to-spec → implement → code-review
```

---

### 3. to-spec — 生成规格文档

**作用**：将当前对话（讨论、拷问结果）综合为一份可构建的 spec 文档。

**何时用**：经过 grilling 或讨论后，想法已经清晰，想要正式化为规格说明再实现。

**用法**：`/to-spec`，agent 会将对话中的关键决策、需求、约束整理成结构化文档。

---

### 4. implement — 按规格实现

**作用**：基于 spec 或 ticket 执行实现，在预设的接缝处驱动 TDD，最后以 code-review 收尾。

**何时用**：已有 spec 或 ticket，准备开始写代码。

**用法**：`/implement`，指定要实现的 spec/ticket 文件路径。agent 会：

1. 读取规格
2. 在约定位置执行 TDD 循环（红-绿-重构）
3. 完成后自动触发 code-review

---

### 5. diagnosing-bugs — 系统化调试

**作用**：6 阶段调试循环：构建反馈回路 → 复现并最小化 → 形成假设 → 插桩验证 → 修复 → 回归测试。

**何时用**：遇到难以定位的 bug、性能回归、异常崩溃。agent 也会在你报告"某东西坏了/报错/变慢"时自动触发。

**用法**：`/diagnosing-bugs`，描述问题现象。也可以直接说：

```
这个功能报错了，帮我诊断
```

---

### 6. prototype — 一次性原型

**作用**：构建抛弃式原型来回答一个设计问题——状态模型是否合理、UI 应该长什么样。

**何时用**：想快速验证某个设计想法是否可行，不需要正式实现。

**用法**：`/prototype`，描述你想验证的设计问题，例如：

```
/prototype 我想知道这个表单的多步流程怎么设计才合理
```

---

### 7. research — 后台调研

**作用**：针对一个问题调研高可信度的一手资料，产出带引用的 Markdown 文件。

**何时用**：需要调研某个技术话题、收集 API 文档事实、或者把阅读工作量委托给后台代理。

**用法**：`/research`，描述你要调研的问题，例如：

```
/research 调研 PostgreSQL 的 MVCC 机制和 MySQL InnoDB 的区别
```

---

### 8. codebase-design — 深模块设计词汇

**作用**：提供一套共享的设计词汇和原则——depth（深度）、seam（接缝）、leverage（杠杆率）、locality（局部性），用于设计或重构模块边界。

**何时用**：设计新模块、重构现有模块、评估架构质量时作为参考。

**用法**：`/codebase-design`，或者在设计讨论中自动触发。它会用深模块理论指导你评估：

- 模块接口是否太宽
- 接缝是否干净
- 变更是否影响过多调用方

---

### 9. domain-modeling — 领域建模

**作用**：主动构建和打磨项目的领域模型——挑战术语、用边界场景做压力测试、更新 CONTEXT.md 和 ADRs。

**何时用**：术语模糊不清、需要记录领域决策、或者团队对领域概念理解不一致。

**用法**：`/domain-modeling`，描述需要建模的领域。agent 会：

1. 建立词汇表（glossary）
2. 用边界场景测试模型
3. 将决策记录到 CONTEXT.md 和 ADRs

---

### 10. code-review — 双轴代码审查

**作用**：从两个维度审查 diff：Standards（是否遵循代码规范 + Fowler 坏味道基线）和 Spec（是否忠实实现了原始需求）。

**何时用**：审查分支、PR、或任意一组变更。

**用法**：`/code-review`，指定要审查的范围（分支名、commit 范围等）。agent 会：

1. 识别变更的固定起点
2. 从 Standards 轴检查代码质量
3. 从 Spec 轴检查需求符合度
4. 输出结构化审查报告

---

### 11. resolving-merge-conflicts — 解决合并冲突

**作用**：逐块解决 git merge/rebase/cherry-pick 冲突，按意图而非文本解决，永不 `--abort`。

**何时用**：遇到合并冲突、rebase 冲突、cherry-pick 冲突。

**用法**：`/resolving-merge-conflicts`。agent 会：

1. `git status` 列出冲突文件
2. 对每个冲突块：读 ours 侧 → 读 theirs 侧 → 追溯各自的 primary source（commit message/PR描述）
3. 按意图解决，而非机械地选一边
4. `git add` → 完成操作

---

### 12. improve-codebase-architecture — 架构深化扫描

**作用**：扫描代码库寻找深化机会——浅模块、宽接缝、低局部性、上帝模块等。

**何时用**：代码库开始变得难以修改时，或作为定期维护。

**用法**：`/improve-codebase-architecture`。agent 会：

1. 扫描所有模块，检查 depth/seam/leverage/locality
2. 列出每个改进机会（文件、当前形状、改进方向、工作量）
3. 让你选择要追求的改进
4. 对选中的改进运行 grill-with-docs 来打磨设计

---

## 二、生产力类（5 个）

### 13. grill-me — 触发拷问

**作用**：触发一个 `grilling` 会话，让 agent relentless 地拷问你的计划或想法。

**何时用**：有一个计划/想法/决策，想在执行前做压力测试。

**用法**：`/grill-me`，然后描述你的计划。等价于直接调用 `/grilling`。

---

### 14. grilling — 拷问循环

**作用**：逐个提问，遍历决策树的每个分支，每个问题都附上推荐答案，直到达成共识。

**核心规则**：

- 一次只问一个问题（避免信息过载）
- 能通过环境探索的事实（文件、工具）直接查，不问你
- 决策权在你——每个决策都等你确认
- 未达成共识前不行动

**何时用**：想 stress-test 你的想法，或者使用了任何 "grill" 相关的措辞。

**用法**：`/grilling`，描述要拷问的计划。例如：

```
/grilling 我想用 microservices 重构这个 monolith
```

---

### 15. handoff — 交接文档

**作用**：将当前对话压缩成交接文档，供新 agent 在新会话中继续工作。

**输出内容**：

- 上下文（用户想完成什么）
- 已完成的工作（引用已有的 spec/plan/commit/diff）
- 进行中的工作状态
- 下一步
- 未解决的决策
- 建议调用的技能

**规则**：

- 不重复已有产物（spec、plan、ADR 等），只引用路径
- 脱敏（API key、密码等）
- 保存到系统临时目录，不是当前工作区

**何时用**：上下文快满了，或需要切换到新会话继续工作。

**用法**：`/handoff`，可以附带说明下个会话的用途：

```
/handoff 下个会话要继续实现 auth 模块
```

---

### 16. teach — 多会话教学

**作用**：在持久化工作区中教你一个主题，跨多个会话进行。包含课程、参考文档、学习记录的完整体系。

**工作区结构**：

| 文件/目录 | 用途 |
|-----------|------|
| `MISSION.md` | 学习目标——为什么学这个 |
| `./reference/*.html` | 参考材料（速查表、语法、术语表） |
| `RESOURCES.md` | 高质量学习资源列表 |
| `./learning-records/*.md` | 学习记录（类似 ADR） |
| `./lessons/*.html` | 课程——每个教一个紧凑的知识点 |
| `./assets/*` | 可复用组件（样式、测验组件等） |
| `NOTES.md` | 用户偏好和工作笔记 |

**教学理念**：

- **知识**（来自高可信资源）→ **技能**（交互式练习）→ **智慧**（真实社区实践）
- 区分 fluency（即时回忆）和 storage strength（长期记忆）
- 用可取的难度（retrieval practice、spacing、interleaving）构建长期记忆
- 每节课落在最近发展区（zone of proximal development）

**何时用**：想系统学习一个主题，愿意跨多个会话进行。

**用法**：在你要用作教学工作区的目录中，输入：

```
/teach 我想学 Rust 的所有权和生命周期系统
```

第一次使用时，agent 会先帮你建立 MISSION.md，然后逐步创建课程。

---

### 17. writing-great-skills — 技能写作参考

**作用**：提供技能写作的词汇和原则，帮助你创建、审查、改进 Agent Skills。

**核心概念**：

| 概念 | 含义 |
|------|------|
| **Predictability** | 根本美德——agent 每次走相同的*过程* |
| **Model-invoked** | 保留 description，agent 可自动触发（占用 context load） |
| **User-invoked** | 无 description，只能手动调用（占用 cognitive load） |
| **Information hierarchy** | 内容分层：in-skill step → in-skill reference → external reference |
| **Progressive disclosure** | 将参考材料推到链接文件中，保持顶层简洁 |
| **Leading word** | 利用模型预训练知识的紧凑概念词（如 _lesson_, _fog of war_） |
| **Completion criterion** | 步骤完成条件——需 checkable + exhaustive |

**6 种失败模式**：

- **Premature completion** — 步骤没做完就跳到下一步
- **Duplication** — 同一含义出现在多处
- **Sediment** — 旧内容堆积，无人清理
- **Sprawl** — 技能太长，即使每行都有用
- **No-op** — 写了 agent 默认就会做的事
- **Negation** — 用"不要做X"反而让 agent 更倾向做X

**何时用**：创建新技能、审查技能质量、或改进现有技能时。

**用法**：`/writing-great-skills`，然后描述你想做什么。配套的 GLOSSARY.md 包含所有术语的详细定义。

---

## 三、自定义技能（1 个）

### 18. paper-research — 论文搜索与概括

**作用**：搜索论文、下载 PDF、生成中文大白话概括并输出 .md 文件。

**何时用**：提供一个论文标题时自动触发。

**用法**：

```
/paper-research Attention Is All You Need
```

或带路径：

```
/paper-research BERT: Pre-training of Deep Bidirectional Transformers, D:\papers
```

默认保存到 `~/Desktop/xzy/papers`。

**概括结构**：

- 这篇论文到底在解决什么问题
- 他们怎么做的
- 效果怎么样
- 对谁有用
- 原文信息

---

## 推荐工作流组合

这些技能设计为可串联使用。以下是典型场景：

### 场景一：从想法到上线

```
/grill-with-docs → /to-spec → /implement → /code-review
```

### 场景二：调试线上问题

```
/diagnosing-bugs → 修复 → /code-review
```

### 场景三：架构优化

```
/improve-codebase-architecture → /grill-with-docs → /to-spec → /implement
```

### 场景四：不确定用什么

```
/ask-matt → 根据推荐继续
```

### 场景五：跨会话交接

```
/handoff → 新会话中继续
```

### 场景六：系统学习

```
/teach <主题> → 跨多个会话逐步学习
```

### 场景七：论文研究与写作

```
/grill-me → /research + /paper-research（并行）→ /to-spec → 写作
```

---

## 技能来源

| 来源 | 技能数 | 说明 |
|------|--------|------|
| [mattpocock/skills](https://github.com/mattpocock/skills) | 17 | 工程流程类 12 个 + 生产力类 5 个 |
| 用户自定义 | 1 | paper-research（论文搜索与概括） |

所有技能已适配为 Qoder 格式：移除了 `disable-model-invocation`、`argument-hint` 等 Qoder 不支持的字段，统一了人称引用和跨技能引用格式。
