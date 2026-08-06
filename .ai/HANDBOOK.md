# AI Handbook — Athena Development Guide

> 本文档是 Athena 项目的 AI 开发手册。
> 目标读者：任何 AI（Codex, Claude Code, Cursor, Gemini CLI, OpenAI Agents）。
> 目标：不依赖聊天上下文，独立理解项目并持续开发。

---

## 目录

1. [Architecture Workflow](#1-architecture-workflow)
2. [Coding Workflow](#2-coding-workflow)
3. [Review Workflow](#3-review-workflow)
4. [Issue Workflow](#4-issue-workflow)
5. [ADR Workflow](#5-adr-workflow)
6. [RFC Workflow](#6-rfc-workflow)
7. [Plugin Workflow](#7-plugin-workflow)
8. [Testing Workflow](#8-testing-workflow)
9. [Release Workflow](#9-release-workflow)
10. [Documentation Workflow](#10-documentation-workflow)

---

## 1. Architecture Workflow

### 触发条件
- 新建 Bounded Context
- 引入新的存储引擎
- 变更 Domain Model
- 跨模块通信方式变更

### 流程

```
识别架构影响
  ↓
查阅 [docs/adr/](../docs/adr/) — 是否已有决策？
  ├─ 有 → 遵守已有 ADR
  └─ 无 → 写 ADR
       ↓
   ADR Template: [docs/adr/ADR-000-template.md](../docs/adr/ADR-000-template.md)
   Must include: Background, Problem, Goals, Non-goals, Design, Alternatives, Risks, Future Work
       ↓
   提交 PR → ≥ 2 Maintainer Approve → Merge
       ↓
   更新 [docs/architecture/architecture-baseline.md](../docs/architecture/architecture-baseline.md)
```

### 关键约束
- 跨 Bounded Context 只通过 Domain Events
- 新模块必须先定义接口（Python ABC），后实现
- 目录结构: `src/{context}/domain|application|infrastructure|interfaces`
- 技术栈固定（见 RFC-001~010）：Python FastAPI, Redis Streams, PostgreSQL, Neo4j, ES

### 参考
- [docs/07-architecture.md](../docs/07-architecture.md)
- [docs/BLUEPRINT.md](../docs/BLUEPRINT.md)
- [docs/architecture/diagrams/](../docs/architecture/diagrams/)

---

## 2. Coding Workflow

### 启动条件
完成 Architecture 设计，ADR Approved。

### 流程

```
1. 阅读相关设计文档
   docs/domain/knowledge-canon.md (如果是 Knowledge 相关)
   docs/domain/ddd-detailed.md

2. 创建分支
   feature/{issue}-{brief}

3. TDD 实现
   a. 写测试 → 确认失败
   b. 写实现 → 确认通过
   c. ruff check + ruff format + mypy --strict

4. 自检
   对照 [REVIEW_PROCESS.md](REVIEW_PROCESS.md) 检查清单

5. Commit
   feat(scope): description  (Conventional Commits)

6. Push + PR
```

### Coding Standard

| 规则 | Python | TypeScript |
|------|--------|------------|
| 格式化 | ruff format | prettier |
| Lint | ruff check | eslint |
| 类型检查 | mypy --strict | tsc --noEmit |
| 测试 | pytest | vitest |
| 命名: 模块 | snake_case | kebab-case (file) |
| 命名: 类 | PascalCase | PascalCase |
| 命名: 函数 | snake_case | camelCase |
| 接口前缀 | I (IEventBus) | I (IEventBus) |

### 禁止
- 硬编码密钥/Token/URL
- 字符串拼接 SQL/Cypher
- print() / console.log() 调试语句
- except: pass / catch {} 空异常
- 跨上下文直接调用
- 跳过测试

### 参考
- [CODING_STANDARD.md](CODING_STANDARD.md)
- [docs/governance/coding-standard.md](../docs/governance/coding-standard.md)

---

## 3. Review Workflow

### 触发条件
PR 提交。

### 流程

```
PR 提交
  ↓
CI 自动门禁 (不可跳过)
  ├─ ruff check + ruff format
  ├─ mypy --strict / tsc --noEmit
  ├─ pytest / vitest
  ├─ 覆盖率 ≥ 基线
  ├─ Trivy 安全扫描 (无 HIGH/CRITICAL)
  └─ Gitleaks 密钥扫描
  ↓
人工审查 (≥ 1 Approve)
  ├─ 代码质量审查
  ├─ 架构一致性审查
  ├─ 安全审查
  └─ 文档完整性审查
  ↓
Squash Merge → main
```

### 审查清单

#### A. 代码质量
- [ ] ruff check + ruff format 通过
- [ ] mypy --strict 通过
- [ ] 无调试语句 (print/console.log)
- [ ] 无注释掉的代码
- [ ] 无空异常处理

#### B. 架构
- [ ] 未跨上下文直接调用
- [ ] 未跨 Schema 查询
- [ ] 新功能优先 Plugin

#### C. 测试
- [ ] 新增代码有测试
- [ ] 覆盖率未下降
- [ ] Happy Path + Edge Case

#### D. 安全
- [ ] 无硬编码密钥
- [ ] 参数化查询
- [ ] 输入验证

#### E. 文档
- [ ] API 变更已更新 OpenAPI
- [ ] 设计文档已同步
- [ ] Commit 符合 Conventional Commits

### 审批权限
| 变更 | 审批人 | 最少 |
|------|--------|:---:|
| Bug Fix (< 50 行) | Committer | 1 |
| Feature (50-500 行) | Committer | 1 |
| Feature (> 500 行) | Maintainer | 2 |
| ADR / RFC | Maintainer | 2 |
| 宪法修订 | Maintainer | 2/3 |

### 参考
- [REVIEW_PROCESS.md](REVIEW_PROCESS.md)

---

## 4. Issue Workflow

### 触发条件
新需求、Bug 报告、技术债务。

### 流程

```
创建 Issue
  ↓
标注 Labels: Feature/Bug/Documentation + Epic + Sprint
  ↓
Assign to Sprint (project/management/SPRINTS.md)
  ↓
Estimate (2h / 3h / 4h / 6h / 8h / 10h)
  ↓
标记依赖 (Depends on ISS-XXX)
  ↓
Start → In Progress → PR → Done
```

### Issue 模板
```
# ISS-XXX: Title

| Sprint | Sprint X | Priority | P0/P1/P2 | Est | Xh |
|--------|----------|----------|-----------|-----|-----|
| Status | Backlog | Depends | None / ISS-XXX |

## Scope
- [ ] Task 1
- [ ] Task 2

## Files
- path/to/file.py

## DoD
- [ ] Tests pass
- [ ] ruff + mypy pass
```

### 参考
- [project/management/ISSUES.md](../project/management/ISSUES.md)
- [project/management/SPRINTS.md](../project/management/SPRINTS.md)

---

## 5. ADR Workflow

### 触发条件
影响 Architecture / Plugin / Workflow / Knowledge / Event 的变更。

### 流程

```
识别需求 → 没有现有 ADR 覆盖？
  ↓
创建 ADR (docs/adr/ADR-XXX-{title}.md)
  ↓
使用模板: docs/adr/ADR-000-template.md
  Must include: Background, Problem, Goals, Non-goals, Design,
                Alternatives, Risks, Future Work, References
  ↓
提交 PR → ≥ 2 Maintainer Approve
  ↓
Merge → 更新 DECISION_LOG.md
```

### ADR 状态
- Proposed → Accepted / Rejected / Superseded

### ADR 编号
连续编号 (ADR-001, ADR-002...)，永久不重用。

### 参考
- [docs/adr/ADR-000-template.md](../docs/adr/ADR-000-template.md)
- [docs/DECISION_LOG.md](../docs/DECISION_LOG.md)

---

## 6. RFC Workflow

### 触发条件
新技术选型、API 变更、功能设计（> 200 行代码）。

### 流程

```
识别需求 → 没有现有 RFC 覆盖？
  ↓
创建 RFC (docs/rfc/RFC-XXX-{title}.md)
  ↓
使用模板: docs/rfc/RFC-000-template.md
  Must include: Background, Problem, Goals, Non-goals, Proposal,
                Alternatives, Trade-offs, Migration, Future Work
  ↓
提交 PR → 社区讨论 ≥ 7 天
  ↓
核心团队决策 → Accept / Reject / Needs Revision
  ↓
Accept → 转化为 ADR
```

### RFC 状态
Draft → Review → Accepted / Rejected

### 参考
- [docs/rfc/RFC-000-template.md](../docs/rfc/RFC-000-template.md)

---

## 7. Plugin Workflow

### 触发条件
新增内容源、AI Provider、存储引擎、处理器、UI 组件。

### 流程

```
确定 Plugin 类型: Source / Processor / Storage / AI / UI
  ↓
实现对应接口
  ISourcePlugin.fetch(config)
  IProcessorPlugin.process(content)
  IStoragePlugin.write/read/query/delete
  IAIProviderPlugin.chat/embed/models
  IUIPlugin.register_routes/static_assets
  ↓
创建 plugin.json manifest
  {
    "name": "athena-{type}-{name}",
    "version": "0.1.0",
    "type": "source",
    "entrypoint": "package.module:ClassName",
    "dependencies": {"athena-core": ">=0.1.0"},
    "config_schema": {},
    "capabilities": {}
  }
  ↓
注册到 Plugin Registry
  ↓
编写 Plugin 测试
```

### 约束
- Plugin 异常不传播到核心系统
- Plugin 连续失败 N 次 → 自动降级
- 遵循 Plugin Lifecycle (Register → Configure → Init → Activate → Deactivate → Dispose)

### 参考
- [docs/09-plugin-system.md](../docs/09-plugin-system.md)
- [docs/architecture/plugin-specification.md](../docs/architecture/plugin-specification.md)

---

## 8. Testing Workflow

### 强制规则
TDD — 先写测试，后写实现。

### 流程

```
1. 写测试
   def test_{function}_{scenario}():
       # Arrange
       # Act
       # Assert

2. 确认测试失败 (Red)

3. 写最小实现 (Green)

4. 重构 (Refactor)

5. 运行全量测试
   pytest / vitest
```

### 覆盖率目标

| 层级 | 目标 |
|------|:---:|
| 核心域 | ≥ 90% |
| 应用层 | ≥ 80% |
| 基础设施 | ≥ 70% |
| 新模块 (serialization/validation) | 100% |

### 测试分类

| 类型 | 工具 | 要求 |
|------|------|------|
| Unit | pytest / vitest | < 1ms, Mock 外部依赖 |
| Integration | pytest + Testcontainers | 真实 PG/Redis, < 100ms |
| E2E | Playwright | 关键流程 ≤ 10 个, < 10s |
| AI Eval | 自定义框架 | Prompt 评测集, pass_rate ≥ 80% |

### 参考
- [docs/14-testing.md](../docs/14-testing.md)
- [docs/guides/testing-strategy.md](../docs/guides/testing-strategy.md)

---

## 9. Release Workflow

### 流程

```
Sprint 完成
  ↓
所有 Issues Done
  ↓
全量测试通过
  ↓
Architecture Review 通过
  ↓
更新 CHANGELOG.md
  ↓
更新版本号
  ↓
创建 Git Tag
  ↓
GitHub Release
```

### 版本策略

| Phase | Version |
|-------|---------|
| 0-1 | No public release |
| 2 | v0.x-alpha |
| 4 | v1.0-beta |
| 5 | v1.0 GA |

### Release Checklist
- [ ] All tests passing
- [ ] CI pipeline green
- [ ] Security scan clean
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Architecture Review approved

### 参考
- [project/management/RELEASE_PLAN.md](../project/management/RELEASE_PLAN.md)
- [CHANGELOG.md](../CHANGELOG.md)

---

## 10. Documentation Workflow

### 强制规则
Documentation as Code — 所有文档必须满足三条标准。

### 三条标准

1. **可视化** — 设计必须有图。画不出图 = 设计不清晰。
2. **成熟度** — 设计必须形成 ADR 或 RFC。构不成 = 不成熟。
3. **完整性** — AI 必须能依据文档独立实现。实现不了 = 文档不完整。

### 流程

```
编码完成
  ↓
检查变更是否影响文档？
  ├─ 新功能 → 更新 API 设计文档
  ├─ 架构变更 → 更新 ADR + 架构图
  ├─ 新模块 → 更新 Knowledge Canon (如影响)
  └─ 无影响 → 跳过
  ↓
更新 docs/README.md (如需)
  ↓
更新 DECISION_LOG.md (如需)
  ↓
更新 CHANGELOG.md
```

### 文档模板
使用 [docs/TEMPLATE.md](../docs/TEMPLATE.md) 的九章结构:
Background → Problem → Goals → Non-goals → Design → Alternatives → Risks → Future Work → References

缺失任一章节 = 文档不合格。

### 参考
- [docs/TEMPLATE.md](../docs/TEMPLATE.md)
- [DOC_TEMPLATE.md](DOC_TEMPLATE.md)
- [docs/DECISION_LOG.md](../docs/DECISION_LOG.md)

---

## 快速索引

| 需求 | 文档 |
|------|------|
| 项目是什么 | [docs/00-vision.md](../docs/00-vision.md) |
| 架构总览 | [docs/07-architecture.md](../docs/07-architecture.md) |
| 施工蓝图 | [docs/BLUEPRINT.md](../docs/BLUEPRINT.md) |
| 知识对象定义 | [docs/domain/knowledge-canon.md](../docs/domain/knowledge-canon.md) |
| 架构图 | [docs/architecture/diagrams/](../docs/architecture/diagrams/) |
| 开发入口 | [project/management/MASTER.md](../project/management/MASTER.md) |
| 运作手册 | [PROJECT.md](PROJECT.md) |
| 决策日志 | [docs/DECISION_LOG.md](../docs/DECISION_LOG.md) |
| 当前 Sprint | [project/management/SPRINTS.md](../project/management/SPRINTS.md) |
| 变更记录 | [CHANGELOG.md](../CHANGELOG.md) |

---

*本 Handbook 面向所有 AI——Codex, Claude Code, Cursor, Gemini CLI, OpenAI Agents。不依赖聊天上下文，独立开发。*
