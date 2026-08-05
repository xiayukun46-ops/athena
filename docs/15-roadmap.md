# 15 — Development Roadmap

> Athena 分阶段开发路线图。

**详细规划见**: [product/roadmap.md](product/roadmap.md)

---

## 总览

| Phase | 时间 | 主题 | 核心产物 | 禁止 |
|-------|------|------|----------|------|
| **0** | 2026 Q3-Q4 | Foundation | 全部文档, 施工蓝图 | 任何代码 |
| **1** | 2026 Q4 - 2027 Q1 | Core Infra | Monorepo, DB, Event Bus, Collector | 业务功能, UI |
| **2** | 2027 Q1-Q2 | Domain Core | Entity, Relation, Knowledge Graph, Search | 用户界面 |
| **3** | 2027 Q2-Q3 | AI Integration | Model Gateway, RAG, Evaluation | 产品化 |
| **4** | 2027 Q3-Q4 | User Experience | Web App, Personalization | 开放平台 |
| **5** | 2028+ | Ecosystem | Plugin Market, SDK, Integrations | - |

---

## Phase 0 — Foundation（当前）

**状态**: 90% 完成

- [x] 项目宪法与治理
- [x] 完整文档体系（16 编号文档 + 详细子文档）
- [x] 架构设计（DDD / Knowledge Model / ER / Graph / Event / API）
- [x] RFC-001（后端语言: Python FastAPI）
- [x] RFC-002（消息队列: Redis Streams）
- [ ] RFC-003（前端框架）
- [ ] RFC-004（搜索引擎）
- [ ] RFC-005（图数据库）
- [ ] RFC-006（移动端）

**当前阻塞**: Blueprint 完成后的最终审批

---

## Phase 1 — Core Infrastructure

**准入**: Blueprint 审批 + ≥ 2 个 P1 级 RFC 完成

**6 个 Sprint, 6-8 周**:

| Sprint | 交付 |
|--------|------|
| 1 | Shared Kernel + DB Migrations（13 张表） |
| 2 | Event Bus（Redis Streams + Outbox）+ Plugin Manager |
| 3 | Collector Service — RSS Source |
| 4 | Collector Service — API + Scraper Sources |
| 5 | Content API（RESTful CRUD） |
| 6 | Docker Compose + CI/CD 完善 |

---

## Phase 2 — Domain Core

**8 个 Sprint, 8-10 周**:

| Sprint | 交付 |
|--------|------|
| 1-2 | Entity Service（CRUD + 多语言） |
| 3-4 | AI Extraction Pipeline（NER + Linking） |
| 5 | Relation Service |
| 6 | Graph Sync + Graph API（Neo4j） |
| 7-8 | Search Service（Fulltext + Vector + Hybrid） |

---

## Phase 3 — AI Integration

**6 个 Sprint, 6-8 周**:

| Sprint | 交付 |
|--------|------|
| 1-2 | AI Model Gateway |
| 3-4 | RAG Pipeline |
| 5-6 | AI Evaluation Framework |

---

## Phase 4 — User Experience

**8 个 Sprint, 8-10 周**:

| Sprint | 交付 |
|--------|------|
| 1-4 | Web Frontend（Next.js） |
| 5-6 | Personalization Engine |
| 7-8 | Mobile App（TBD） |

---

## Phase 5 — Ecosystem（2028+）

- 插件市场
- 公开 API + SDK (Python / TypeScript / Dart)
- 第三方集成（Slack, Notion, Obsidian）
- 社区治理

---

## 版本策略

| Phase | 版本 |
|-------|------|
| 0-1 | 无公开发布 |
| 2 | v0.x Alpha |
| 4 | v1.0 Beta |
| 5 | v1.0 GA |

---

## 相关文档

- [00-vision.md](00-vision.md) — 愿景
- [01-product-strategy.md](01-product-strategy.md) — 产品策略
- [07-architecture.md](07-architecture.md) — 架构如何支撑路线图
- [BLUEPRINT.md](BLUEPRINT.md) — 完整施工蓝图
- [product/roadmap.md](product/roadmap.md) — 详细阶段规划
