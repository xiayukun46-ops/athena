# PROJECT.md

> Athena AI Agent 总纲。所有开发行为的最高规则。

---

## 铁律 (7 条，不可违背)

1. **Documentation First** — 无文档不编码。任何修改前确认设计文档已存在并已更新。
2. **Architecture First** — 接口先于实现。跨模块依赖只通过抽象接口，不直接导入实现类。
3. **Domain First** — 代码按限界上下文组织 (`src/content/` 非 `src/controllers/`)。
4. **API First** — 新功能先在 OpenAPI 定义，再写实现。
5. **Plugin First** — 新功能默认以 Plugin 实现，不硬编码进核心。
6. **Test First** — 先写测试。覆盖率门禁不可绕过。
7. **Security First** — 零信任。所有输入验证。禁止硬编码密钥。

---

## 阶段门禁

**禁止自动进入下一阶段。**

每个阶段完成后停止，等待 Review。只有收到 `APPROVED` 才能继续。
未通过必须修改。不能跳过。沉默不等于批准。

---

## 决策路径

```
新需求
  ↓
docs/adr/ 有相关决策？ → 遵守
  ↓ 无
是否重大架构变更？
  ├─ 是 → 写 ADR，≥ 2 人 Approve
  └─ 否 → 写 RFC，讨论 ≥ 7 天
```

---

## 文档标准

所有设计文档必须遵循九章结构：
Background → Problem → Goals → Non-goals → Design → Alternatives → Risks → Future Work → References
详见 [docs/TEMPLATE.md](../docs/TEMPLATE.md)

---

## 快速参考

| 了解 | 文档 |
|------|------|
| 愿景 | [docs/00-vision.md](../docs/00-vision.md) |
| 宪法 | [docs/02-constitution.md](../docs/02-constitution.md) |
| 术语 | [docs/03-glossary.md](../docs/03-glossary.md) |
| 架构 | [docs/07-architecture.md](../docs/07-architecture.md) |
| 蓝图 | [docs/BLUEPRINT.md](../docs/BLUEPRINT.md) |
| 任务树 | [docs/TASK-TREE.md](../docs/TASK-TREE.md) |

---

## 本文件相关

- [WORKFLOW.md](WORKFLOW.md) — 开发工作流
- [REVIEW_PROCESS.md](REVIEW_PROCESS.md) — 审查与审批
- [DOC_TEMPLATE.md](DOC_TEMPLATE.md) — 文档模板
- [CODING_STANDARD.md](CODING_STANDARD.md) — 编码规范
