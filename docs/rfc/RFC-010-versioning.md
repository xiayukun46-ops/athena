# RFC-010: Document & Event Versioning

## Metadata

| 字段 | 值 |
|------|-----|
| RFC ID | RFC-010 |
| Status | Draft |
| Priority | P2 |
| Target Phase | Phase 1-2 |

---

## 1. Background

Athena 有多类需要版本管理的对象：设计文档（ADR/RFC）、领域事件（Schema 变更）、Prompt 模板、API Schema。需要统一的版本策略。

## 2. Problem

当前 ADR 使用连续编号（ADR-001...），RFC 使用连续编号（RFC-001...），领域事件无版本号。随着项目演进，需要明确：如何表示 Breaking Change、如何保留历史版本、如何让消费者知道版本变更。

## 3. Goals

- [ ] P0: 统一的设计文档版本策略（ADR/RFC 编号 + Status）
- [ ] P1: 领域事件 Schema 版本策略（Event Versioning）
- [ ] P1: Prompt 模板版本策略

## 4. Non-goals

- 不引入 Git-based 版本（Git 管理文件版本已足够）
- 不在 Phase 1 实现 Event Schema Registry（Phase 2 引入）

## 5. Proposal

### 设计文档版本

- ADR/RFC: 连续编号（ADR-001, RFC-001），永久不重用
- Status: Draft → Review → Accepted/Rejected → Superseded（被新 ADR 替代）
- 文件内部标注版本号和修订历史

### 领域事件版本

- 事件 Payload 增加 `version` 字段（整数，从 1 起始）
- Breaking Change → 递增主版本，创建新事件类型（如 `EntityCreatedV2`）
- 消费者需兼容同一事件的多个版本
- Phase 2 引入 Event Schema Registry 自动检测不兼容变更

### Prompt 模板版本

- 模板文件内部标注版本号（`# Version: 1.0.0`）
- 变更时递增版本 + 记录变更日志
- 评测集关联到特定版本

## 6. Alternatives

| 方案 | 优点 | 缺点 | 为什么不选 |
|------|------|------|-----------|
| SemVer + 事件 Payload version 字段 | 简单；消费者可判断兼容性 | Breaking Change 需人工判断 | **采用** |
| Schema Registry（Avro/Protobuf） | 自动兼容性检查 | 引入新组件；增加复杂度 | Phase 3 评估 |
| 只靠 Git 历史 | 零成本 | 不可编程；消费者无法自动检测 | 不可靠 |

## 7. Future Evolution

Phase 3: 评估 Schema Registry（如 Confluent Schema Registry）用于事件 Payload 的自动兼容性验证。
Phase 5: Prompt A/B 测试框架，基于版本对比。

---

## 8. References

- [Event Model](../domain/event-model.md)
- [TEMPLATE.md](../TEMPLATE.md)
