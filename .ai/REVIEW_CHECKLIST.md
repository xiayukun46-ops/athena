# AI Agent — Review Checklist

> 每次 PR 提交前的自检清单。全部通过才能请求 Review。

---

## 代码质量

- [ ] `ruff check` + `ruff format` 通过
- [ ] `mypy --strict` 或 `tsc --noEmit` 通过
- [ ] 无 `print()` 调试语句
- [ ] 无注释掉的代码块
- [ ] 无 `except: pass` 空异常处理

---

## 架构

- [ ] 未跨上下文直接调用
- [ ] 未跨 Schema 查询数据库
- [ ] 新功能未硬编码（优先 Plugin）
- [ ] 接口变更已更新 ADR

---

## 测试

- [ ] 新增代码有测试
- [ ] 覆盖率未下降
- [ ] Happy Path + Edge Case 覆盖

---

## 安全

- [ ] 无硬编码密钥/Token
- [ ] SQL/Cypher 使用参数化查询
- [ ] 用户输入已验证
- [ ] 无 PII 泄露到日志

---

## 文档

- [ ] API 变更已更新 OpenAPI
- [ ] 设计文档已同步
- [ ] Commit 符合 Conventional Commits

---

## 完整参考

- [docs/02-constitution.md](docs/02-constitution.md) — 质量门禁
- [docs/13-security.md](docs/13-security.md) — 安全检查清单
