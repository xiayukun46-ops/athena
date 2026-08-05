# REVIEW_PROCESS.md

> Athena 审查与审批流程。PR 提交前和合并前必须通过的检查。

---

## 审查清单

### A. 代码质量

- [ ] `ruff check` + `ruff format` 通过 (Python)
- [ ] `eslint` + `prettier` 通过 (TypeScript)
- [ ] `mypy --strict` / `tsc --noEmit` 通过
- [ ] 无 `print()` / `console.log()` 调试语句
- [ ] 无注释掉的代码块
- [ ] 无 `except: pass` / `catch {}` 空异常处理
- [ ] 命名符合 Coding Standard

### B. 架构合规

- [ ] 未跨 Bounded Context 直接调用
- [ ] 未跨 PostgreSQL Schema 查询
- [ ] 新功能优先 Plugin（如适用）
- [ ] 跨上下文通信仅通过 Domain Events
- [ ] 接口变更已更新 ADR（如适用）

### C. 测试

- [ ] 新增代码有测试
- [ ] Happy Path + Edge Case 覆盖
- [ ] 覆盖率不低于 main 分支
- [ ] AI 相关变更包含评测用例

### D. 安全

- [ ] 无硬编码密钥 / Token / 密码
- [ ] SQL / Cypher 查询全部参数化（禁止字符串拼接）
- [ ] 用户输入在边界处验证
- [ ] 无 PII 泄露到日志
- [ ] Agent 权限声明正确

### E. 文档

- [ ] 设计文档已同步更新
- [ ] API 变更已更新 OpenAPI
- [ ] Commit 符合 Conventional Commits
- [ ] PR 描述包含 What / Why / How

---

## 审批流程

```
PR 提交
  ↓
CI 自动门禁（不可跳过）
  ├─ Lint ✓
  ├─ Type Check ✓
  ├─ Test ✓
  ├─ Coverage ✓
  ├─ Security Scan ✓
  └─ Build ✓
  ↓
人工审查
  ├─ 审查清单逐项确认
  ├─ ≥ 1 人 Approve
  └─ 所有讨论线程已解决
  ↓
Squash Merge → main
```

---

## 审批权限

| 变更类型 | 审批人 | 最少人数 |
|----------|--------|----------|
| Bug Fix (< 50 行) | Committer | 1 |
| Feature (50-500 行) | Committer | 1 |
| Feature (> 500 行) | Maintainer | 2 |
| ADR / RFC | Maintainer | 2 |
| 宪法修订 | Maintainer | 2/3 多数 |

---

## 阶段审批

每个 Phase / Milestone 完成后：

1. 提交 Architecture Review Report
2. 等待 Maintainer 审查
3. 收到 `APPROVED` 指令 → 进入下一阶段
4. 未收到 → 修改直到通过

---

## 相关文件

- [PROJECT.md](PROJECT.md) — 铁律和门禁
- [WORKFLOW.md](WORKFLOW.md) — 开发流程
- [CODING_STANDARD.md](CODING_STANDARD.md) — 代码规范
- [docs/02-constitution.md](../docs/02-constitution.md) — 质量门禁定义
