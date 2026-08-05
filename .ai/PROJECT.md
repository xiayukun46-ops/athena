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

## 任务启动规则

**任何任务开始之前，必须先阅读 `.ai/` 和 `docs/` 中的所有相关规范。**

如果发现：
- 规范之间存在冲突
- 规范缺失覆盖当前场景

**不允许自行假设。** 必须：
1. 明确指出冲突或缺失的具体内容
2. 提出解决方案建议
3. 等待确认，或提交 RFC

假设驱动的开发是架构腐化的第一推手。

## Documentation as Code（文档即代码）

Blueprint 的目标不是给人阅读，而是让未来任何 AI（Codex、Claude Code、Cursor 等）在**不依赖聊天上下文**的情况下，能够独立理解项目并持续开发。

### 三条质量标准

**1. 可视化标准**
任何设计如果无法画图（Mermaid / C4 / 时序图 / 状态机），说明设计还不够清晰。
→ 文档必须有图。不接受纯文字描述复杂架构。

**2. 成熟度标准**
任何设计如果不能形成 ADR 或 RFC，说明设计还不够成熟。
→ 所有架构决策归于 ADR。所有功能提案归于 RFC。

**3. 完整性标准**
任何设计如果 AI 无法依据文档独立实现，说明文档还不够完整。
→ 文档必须包含：接口签名、数据 Schema、状态转换、错误处理、边界条件。
→ 缺失任一要素 = 文档不合格。

### 验收方法

对每份设计文档，执行以下测试：
1. 让一个从未见过此项目的新 AI 实例读取该文档
2. 该 AI 能否独立画出设计图？→ 通过可视化标准
3. 该 AI 能否独立写出对应代码？→ 通过完整性标准
