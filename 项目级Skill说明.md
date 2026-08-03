# 项目级 Skill 说明（已迁移至全局）

> **来源：** 2026-08-03 从 `chat-1` 项目（`Documents\Qoder\2026-08-03\chat-1\.qoder\skills\`）迁移至全局目录 `C:\Users\pilot\.qoder\skills\`，现可在所有项目中调用。
> **共 10 个**，均为 Superpowers 风格的开发流程类 Skill，核心理念是"先设计、后实现、必验证"。

---

## 1. brainstorming — 头脑风暴：把想法打磨成设计

- **触发时机：** 任何创造性工作之前（新建功能、组件、项目，或修改行为），必须先走此流程
- **作用：** 通过逐个提问理解意图、需求与约束，提出 2–3 种方案及权衡，最终形成设计文档（保存至 `docs/specs/`）并提交
- **硬性门槛：** 设计未获用户批准前，禁止写任何代码或开始实现

## 2. writing-plans — 编写实施计划

- **触发时机：** 设计获批后、动代码之前，用于多步骤任务
- **作用：** 生成"零上下文工程师也能执行"的详细计划：每个任务都是 2–5 分钟的可独立测试小步（写失败测试 → 运行确认失败 → 最小实现 → 运行确认通过 → 提交），遵循 DRY/YAGNI/TDD 原则
- **输出：** 计划保存至 `docs/plans/`

## 3. executing-plans — 执行实施计划（本会话内）

- **触发时机：** 手头有书面计划需要执行，且子代理驱动开发不可用或不适用
- **作用：** 加载并批判性审查计划 → 逐步执行任务（带人工检查点）→ 完成后调用 finishing-a-development-branch 收尾
- **原则：** 遇阻立即停下询问，绝不强行猜着做

## 4. subagent-driven-development — 子代理驱动开发

- **触发时机：** 有实施计划、任务彼此独立、且在本会话内执行（推荐方式，优先于 executing-plans）
- **作用：** 每个任务派发全新子代理实现（避免上下文污染），任务后做两阶段审查（规范符合性 + 代码质量），最后做整体分支审查；每任务记录基线 SHA，禁止并行派发多个实现子代理
- **注意：** 在 main/master 分支上直接实施前必须征得用户同意

## 5. using-git-worktrees — Git 工作树隔离

- **触发时机：** 开始需要隔离的功能开发，或执行实施计划之前
- **作用：** 确保工作在隔离工作区进行：先检测是否已处于隔离状态（避免重复创建），优先用平台原生 worktree 工具，无原生工具时回退到 `git worktree`
- **注意：** 在普通仓库中创建工作树前需征求用户同意

## 6. test-driven-development — 测试驱动开发（TDD）

- **触发时机：** 任何功能、修复、重构或行为变更的实现之前（所有编码任务自动激活）
- **作用：** 强制"先测试后代码"（RED-GREEN-REFACTOR）：先写一个最小失败测试，再写恰好通过它的实现代码
- **铁律：** 没有失败测试之前，禁止写任何生产代码；写了就要删掉重来

## 7. systematic-debugging — 系统化根因调试

- **触发时机：** 任何 bug、测试失败、意外行为、性能问题或构建失败，在提出修复方案之前
- **作用：** 四阶段流程，核心是**先找根因再动手修**（症状修复 = 失败）：仔细读报错 → 稳定复现 → 检查最近改动 → 定位根因 → 修复并验证
- **铁律：** 未完成根因调查之前，禁止提出任何修复

## 8. requesting-code-review — 请求代码审查

- **触发时机：** 完成任务时、实现大功能后、合并前（审查要早、要勤）；卡住时或大重构前也推荐
- **作用：** 派遣代码审查子代理（携带精确构造的上下文：基线/末端 SHA、需求、功能描述，而非本会话历史），从规范符合性、代码质量、测试覆盖、安全、性能五方面审查
- **反馈处理：** Critical 立即修，Important 继续前修，Minor 记录待办；认为审查有误可带理由反驳

## 9. finishing-a-development-branch — 完成开发分支

- **触发时机：** 实现完成、测试通过后，需要决定如何收尾时
- **作用：** ① 跑全量测试（不绿不继续）② 检测环境（普通仓库 / 命名分支工作树 / detached HEAD）③ 确认基线分支 ④ 呈现 3 个选项：本地合并 / 推送建 PR / 保留分支 ⑤ 执行选择并清理工作区

## 10. verification-before-completion — 完成前验证

- **触发时机：** 声称工作"完成/已修复/测试通过"之前、提交或建 PR 之前
- **作用：** 强制"证据先于声明"：声称任何状态前，必须在本轮消息中运行完整验证命令、读取完整输出并核对退出码
- **铁律：** 没有新鲜的验证证据，不得声称完成；"应该能过""看起来没问题"都是红灯

---

## 快速速查

| Skill | 一句话作用 |
|-------|-----------|
| brainstorming | 想法 → 设计（动代码前的必经关） |
| writing-plans | 设计 → 可执行的小步计划 |
| executing-plans | 本会话内按计划执行 |
| subagent-driven-development | 每任务派新子代理执行 + 双重审查 |
| using-git-worktrees | 建隔离工作区防污染 |
| test-driven-development | 先写失败测试再实现 |
| systematic-debugging | 先查根因再修复 |
| requesting-code-review | 派遣子代理审查代码 |
| finishing-a-development-branch | 测试、合并选项与清理收尾 |
| verification-before-completion | 无新鲜验证证据不声称完成 |

**完整流程链路：** brainstorming → writing-plans →（subagent-driven-development 或 executing-plans）→ requesting-code-review → finishing-a-development-branch，全程由 using-git-worktrees、test-driven-development、systematic-debugging、verification-before-completion 保驾护航。