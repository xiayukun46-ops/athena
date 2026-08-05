# Athena — Document Index

> 完整文档导航。Blueprint Phase 产出。

---

## 核心序列 (docs/)

按编号阅读，从 00 到 15：

| # | 文档 | 内容 |
|---|------|------|
| 00 | [00-vision.md](00-vision.md) | 项目愿景——为什么存在，去哪里 |
| 01 | [01-product-strategy.md](01-product-strategy.md) | 产品策略——做什么，不做什么 |
| 02 | [02-constitution.md](02-constitution.md) | 项目宪法——八大原则，决策体系 |
| 03 | [03-glossary.md](03-glossary.md) | 术语表——统一领域语言 |
| 04 | [04-domain-model.md](04-domain-model.md) | 领域模型——六个限界上下文 |
| 05 | [05-event-model.md](05-event-model.md) | 事件模型——事件驱动通信 |
| 06 | [06-knowledge-engine.md](06-knowledge-engine.md) | 知识引擎——从内容到知识 |
| 07 | [07-architecture.md](07-architecture.md) | 架构总览——分层、组件、数据流 |
| 08 | [08-data-model.md](08-data-model.md) | 数据模型——存储引擎与 Schema |
| 09 | [09-plugin-system.md](09-plugin-system.md) | 插件系统——五类插件 |
| 10 | [10-agent-system.md](10-agent-system.md) | Agent 系统——AI 自主实体 |
| 11 | [11-api-style-guide.md](11-api-style-guide.md) | API 风格指南——RESTful 规范 |
| 12 | [12-database-standard.md](12-database-standard.md) | 数据库标准——命名、索引、迁移 |
| 13 | [13-security.md](13-security.md) | 安全架构——零信任、威胁模型 |
| 14 | [14-testing.md](14-testing.md) | 测试策略——金字塔、覆盖率 |
| 15 | [15-roadmap.md](15-roadmap.md) | 路线图——Phase 0-5 |

---

## 详细设计文档 (docs/)

按主题深入：

| 目录 | 关键文档 |
|------|----------|
| **architecture/** | [overview.md](architecture/overview.md), [security.md](architecture/security.md), [plugin-specification.md](architecture/plugin-specification.md), [agent-specification.md](architecture/agent-specification.md), [collector-service.md](architecture/collector-service.md), [review-2026-08-03.md](architecture/review-2026-08-03.md) |
| **domain/** | [domain-model.md](domain/domain-model.md), [ddd-detailed.md](domain/ddd-detailed.md), [knowledge-model.md](domain/knowledge-model.md), [graph-model.md](domain/graph-model.md), [event-model.md](domain/event-model.md), [shared-kernel.md](domain/shared-kernel.md) |
| **api/** | [api-design.md](api/api-design.md), [openapi.yaml](api/openapi.yaml) |
| **database/** | [er-diagram.md](database/er-diagram.md) |
| **governance/** | [constitution.md](governance/constitution.md), [coding-standard.md](governance/coding-standard.md) |
| **guides/** | [api-style-guide.md](guides/api-style-guide.md), [database-convention.md](guides/database-convention.md), [testing-strategy.md](guides/testing-strategy.md), [environment-setup.md](guides/environment-setup.md) |
| **product/** | [roadmap.md](product/roadmap.md) |

---

## 决策记录

| 目录 | 关键文件 |
|------|----------|
| **adr/** | [ADR-001](adr/ADR-001-project-init.md), [ADR-002](adr/ADR-002-architecture-review.md) |
| **rfc/** | [RFC-001](rfc/RFC-001-backend-language.md), [RFC-002](rfc/RFC-002-message-queue.md) |

---

## AI 规范 (.ai/)

| 文件 | 内容 |
|------|------|
| [PROJECT.md](../.ai/PROJECT.md) | AI Agent 项目铁律 |
| [ARCHITECTURE.md](../.ai/ARCHITECTURE.md) | 架构约束 |
| [CODING_STANDARD.md](../.ai/CODING_STANDARD.md) | 编码规范 |
| [DATABASE_RULES.md](../.ai/DATABASE_RULES.md) | 数据库规则 |
| [PLUGIN_SPEC.md](../.ai/PLUGIN_SPEC.md) | 插件规范 |
| [AGENT_PROTOCOL.md](../.ai/AGENT_PROTOCOL.md) | Agent 协议 |
| [API_RULES.md](../.ai/API_RULES.md) | API 规则 |
| [TESTING_STANDARD.md](../.ai/TESTING_STANDARD.md) | 测试标准 |
| [REVIEW_CHECKLIST.md](../.ai/REVIEW_CHECKLIST.md) | 审查清单 |

---

## 顶层文档

| 文件 | 说明 |
|------|------|
| [MASTER.md](../MASTER.md) | 开发前必读清单 |
| [README.md](../README.md) | 项目介绍 |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | 贡献指南 |
| [LICENSE](../LICENSE) | Apache 2.0 |
| [BLUEPRINT.md](BLUEPRINT.md) | 施工总图 |

---

*最后更新: 2026-08-05 — Blueprint Phase*
