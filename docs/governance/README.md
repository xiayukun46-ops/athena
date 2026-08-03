# Governance

本目录包含 Athena 项目的治理文件。

## 文件说明

| 文件 | 说明 |
|------|------|
| [constitution.md](constitution.md) | 项目宪法——八项核心原则、决策层级、质量门禁 |
| [coding-standard.md](coding-standard.md) | 编码规范——命名、结构、测试、Git 规范 |
| [../CONTRIBUTING.md](../CONTRIBUTING.md) | 贡献指南——从 Issue 到 PR 的完整流程 |

## 决策体系

Athena 的决策按层级递进：

```
L0: Constitution (宪法)
  ↓ 不可违背的根本原则
L1: ADR (架构决策记录)
  ↓ 重大架构决策，需 2 人 Approve
L2: RFC (设计提案)
  ↓ 功能设计、API 变更，社区讨论 ≥ 7 天
L3: PR Review (代码审查)
  ↓ 日常代码决策
```

## 质量门禁

所有 PR 必须通过：
1. CI 全绿（Lint + Type Check + Test + Build）
2. 覆盖率不下降
3. 安全扫描通过
4. 至少 1 人 Approve
5. 文档已同步更新

详见 [Project Constitution](constitution.md)。
