# Phase 1 Development Plan

> Phase 1 — Core Infrastructure
> 周期：2026 Q4 - 2027 Q1 (6-8 周)
> 准入条件：Architecture Freeze APPROVED + ≥ 2 个 P1 RFC Approved

---

## 1. 目标

搭建 Athena 的技术骨架。完成后系统可运行、可测试、可部署——但没有任何面向用户的功能。

### 交付物

- Monorepo 项目结构
- Shared Kernel（共享类型与值对象）
- 13 张 PostgreSQL 表的 Schema + Alembic 迁移
- Event Bus（Redis Streams + Outbox Pattern）
- Plugin Manager（注册、加载、生命周期）
- Collector Service（RSS / API / Scraper 三种源内容采集）
- Content REST API（内容源和文章的 CRUD）
- Docker Compose 本地开发环境
- CI/CD 管道完善

---

## 2. 模块与开发顺序

```
Sprint 1 (Week 1-2): Foundation
  └── Shared Kernel + Database Migrations
       ├── src/shared/domain/ (EntityId, Language, Confidence, DomainEvent...)
       ├── src/shared/infrastructure/ (Database, Config, Logging)
       └── alembic/ (13 张表迁移)

Sprint 2 (Week 3-4): Communication
  └── Event Bus + Plugin Manager
       ├── src/shared/event_bus/ (IEventBus, Redis Streams, Outbox Worker)
       └── src/plugin/ (Plugin Registry, Loader, DI)

Sprint 3 (Week 5-6): Content Ingestion
  └── Collector Service — RSS Source
       ├── src/content/domain/ (Source, Article 聚合根)
       ├── src/content/infrastructure/ (ISourcePlugin → RSS 实现)
       └── Collector Pipeline (Fetch → Parse → Clean → Dedup → Publish)

Sprint 4 (Week 7-8): Content Ingestion (cont.)
  └── Collector Service — API + Scraper Sources
       ├── API Source Plugin
       └── Scraper Source Plugin

Sprint 5 (Week 9-10): Content API
  └── Content REST API
       ├── src/content/interfaces/ (FastAPI Router)
       ├── GET/POST /v1/sources
       └── GET /v1/articles, GET /v1/articles/{id}

Sprint 6 (Week 11-12): DevOps
  └── Docker + CI/CD
       ├── docker-compose.yml (PG + Redis + ES + Neo4j + MinIO + App)
       ├── Dockerfile (Python App)
       ├── CI 管道完善 (Test + Coverage + Security)
       └── Makefile / Taskfile
```

---

## 3. 依赖关系

```
Sprint 1 (Shared Kernel)     ← 无依赖，最先做
    ↓
Sprint 2 (Event Bus)         ← 依赖 Shared Kernel
Sprint 2 (Plugin Manager)    ← 依赖 Shared Kernel
    ↓
Sprint 3-4 (Collector)       ← 依赖 Event Bus + Plugin Manager + DB
    ↓
Sprint 5 (Content API)       ← 依赖 Collector + DB
    ↓
Sprint 6 (Docker + CI/CD)    ← 依赖全部
```

---

## 4. 风险

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| Alembic 迁移复杂性超预期 | 低 | 中 | Sprint 1 预留缓冲；复杂迁移可拆分 |
| Redis Streams 实现有坑 | 中 | 中 | Sprint 2 早期做 PoC；提前验证 Consumer Group 行为 |
| RSS/API 源格式多样性 | 高 | 中 | Sprint 3-4 只支持 3 个代表性源；不追求全覆盖 |
| Docker Compose 环境不稳定 | 中 | 低 | Sprint 6 使用 Testcontainers 辅助调试 |

---

## 5. 测试计划

| Sprint | 测试类型 | 覆盖目标 |
|--------|----------|----------|
| 1 | Unit | Shared Kernel 类型 100% 测试覆盖 |
| 1 | Integration | 13 张表可创建 + 迁移正向/逆向 |
| 2 | Unit | IEventBus 接口行为正确 |
| 2 | Integration | 事件发布/消费端到端通过 |
| 3-4 | Unit | Collector 各 Stage 独立可测 |
| 3-4 | Integration | RSS → Article 入库全流程 |
| 5 | Integration | Content API 端点测试 |
| 6 | E2E | Docker Compose 启动 + Health Check |

---

## 6. 完成标准

每个 Sprint 的 Definition of Done：

- [ ] 所有代码通过 Lint + Type Check
- [ ] 所有测试通过
- [ ] 覆盖率不低于目标
- [ ] 安全扫描无 HIGH/CRITICAL
- [ ] 相关文档已更新
- [ ] PR 已 Review 并 Squash Merge

### Phase 1 整体完成标准

- [ ] `docker compose up` 后所有服务健康
- [ ] 可通过 API 注册一个 RSS Source 并触发采集
- [ ] 采集的文章可通过 API 查询
- [ ] 事件总线正常发布/订阅
- [ ] CI 管道全绿

---

## 7. 时间估计

| Sprint | 内容 | 估计 |
|--------|------|------|
| 1 | Shared Kernel + DB | 2 周 |
| 2 | Event Bus + Plugin Manager | 2 周 |
| 3 | Collector RSS | 2 周 |
| 4 | Collector API + Scraper | 2 周 |
| 5 | Content API | 2 周 |
| 6 | Docker + CI/CD | 2 周 |
| **合计** | | **12 周** |

*估计基于 1-2 名全职开发者。团队规模增加可压缩。*

---

## 8. 禁止事项

Phase 1 明确不做的内容：

- 前端 UI（Web / Mobile）
- 知识实体 CRUD（Phase 2）
- AI 提取管道（Phase 2）
- 搜索功能（Phase 2）
- 图数据库同步（Phase 2）
- 用户认证（Phase 2）
- 插件市场（Phase 5）

---

## 相关文档

- [Architecture Baseline](architecture/architecture-baseline.md) — 冻结的架构决策
- [BLUEPRINT.md](../BLUEPRINT.md) — 完整施工蓝图
- [15-roadmap.md](../15-roadmap.md) — 路线图
- [Collector Service](architecture/collector-service.md) — Sprint 3-4 详细设计
