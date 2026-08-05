# Architecture Baseline — Frozen Design

> Athena 架构冻结基线。本文档列出的所有设计决策已完成冻结。
> 冻结后修改必须通过 ADR 流程，不再接受 RFC 级别的随意变更。
> 版本：v1.0 | 冻结日期：2026-08-06

---

## 基线说明

Architecture Freeze 意味着：以下设计决策已确定为 Phase 1-3 的实现基础。任何变更必须：

1. 提交 ADR（非 RFC）——因为涉及已冻结的架构基线
2. 说明 Breaking Change 影响范围
3. 提供迁移计划
4. ≥ 2 名 Maintainer Approve

---

## 1. Knowledge Object（知识对象）— 已冻结

```
定义位置: docs/domain/knowledge-canon.md

冻结内容:
  - KnowledgeEntity (id, canonical_name, entity_type, names, aliases, properties, status, quality_score)
  - KnowledgeRelation (id, relation_type, source/target, statements, confidence, valid_from/until)
  - Statement (id, statement_type, subject_id, predicate, object_value, confidence, source)
  - EntityType (8 种: PERSON | ORGANIZATION | LOCATION | EVENT | CONCEPT | PRODUCT | WORK | NATURAL_ENTITY)
  - RelationType (20+ 种)
  - Identity 前缀 (ent_, rel_, stmt_, art_, src_, usr_, tsk_)
  - QualityScore (completeness, consistency, freshness, confidence, provenance, diversity)
  - 生命周期状态机 (DRAFT→ACTIVE→DEPRECATED→MERGED 等)

冻结理由: Knowledge Object 是所有模块的基础数据结构。变更影响全部下游。
```

---

## 2. Event（领域事件）— 已冻结

```
定义位置: docs/domain/event-model.md

冻结内容:
  - DomainEvent 结构 (event_id, event_type, aggregate_id, aggregate_type, payload, metadata, occurred_at, version)
  - EventMetadata (correlation_id, causation_id, source_context)
  - 事件命名规范 (过去式: ArticleFetched, EntityCreated)
  - 事件版本策略 (version 字段, Breaking Change → 新事件类型)
  - Outbox Pattern (system_event_log 表 + Redis Streams)
  - 跨上下文通信规则 (只通过事件, 不直接 API 调用)

冻结理由: 事件是上下文间唯一的通信契约。变更影响所有消费者。
```

---

## 3. Workflow（工作流引擎）— 已冻结

```
定义位置: docs/architecture/workflow-engine.md

冻结内容:
  - 12 阶段管道 (Collector → Normalizer → Verifier → Deduplicator → EntityExtractor → EventBuilder → KnowledgeBuilder → Embedding → Indexer → GraphBuilder → Publisher)
  - 状态机 (Scheduled → Fetching → ... → DLQ)
  - Retry Policy (3 次, 指数退避 1s/2s/4s)
  - Dead Letter Queue (dlq-{stage}, 7 天保留)
  - Audit Log 结构
  - Plugin Hook 接口 (before_stage, after_stage, on_error)

冻结理由: 管道顺序和阶段接口是知识处理的核心流程。变更破坏数据一致性。
```

---

## 4. Plugin Interface（插件接口）— 已冻结

```
定义位置: docs/architecture/plugin-specification.md

冻结内容:
  - 五类插件接口:
    ISourcePlugin.fetch(config)
    IProcessorPlugin.process(content)
    IStoragePlugin.write/read/query/delete
    IAIProviderPlugin.chat/embed/models
    IUIPlugin.register_routes/static_assets
  - 生命周期 (Register → Configure → Init → Activate → Deactivate → Dispose)
  - Plugin Manifest 格式 (plugin.json: name, version, type, entrypoint, dependencies, config_schema, capabilities)
  - 错误隔离 (插件异常不传播到核心)

冻结理由: 插件接口是扩展性的基石。接口变更破坏所有现有插件。
```

---

## 5. Agent Interface（Agent 接口）— 已冻结

```
定义位置: docs/architecture/agent-specification.md

冻结内容:
  - Agent 运行时 (Planner → Executor → Reflector + Working Memory + Episodic Memory)
  - Agent 定义格式 (YAML: name, type, model, tools, permissions, schedule)
  - 工具系统 (Tool: name, description, parameters, handler, required_permissions)
  - 安全模型 (工具白名单, Docker 沙箱, 审批机制, 审计日志)

冻结理由: Agent 是 AI 自主运行的核心。接口变更影响所有 Agent 实现。
```

---

## 6. Architecture Layer（架构分层）— 已冻结

```
定义位置: docs/07-architecture.md + docs/architecture/overview.md

冻结内容:
  - 分层模型: Client → API Gateway → Application → Infrastructure
  - Modular Monolith (Phase 0-3) → Microservices 拆分触发条件
  - 6 个 Bounded Context (Content | Knowledge | Search | AI | User | Plugin)
  - 目录结构: src/{context}/domain|application|infrastructure|interfaces
  - 技术栈: Python 3.12 + FastAPI (RFC-001), Redis Streams (RFC-002)

冻结理由: 架构分层是代码组织的基础。变更需要大规模重构。
```

---

## 7. API Convention（API 约定）— 已冻结

```
定义位置: docs/11-api-style-guide.md

冻结内容:
  - URL 规范: kebab-case, 复数名词, /v1/ 前缀
  - 响应格式: {data, _meta, _links} (JSON:API 风格)
  - 分页: Cursor-based (推荐) | Page-based
  - HTTP 状态码语义
  - 异步 AI 操作: 202 Accepted + task_id 轮询
  - API 版本策略: 旧版保留 ≥ 6 个月

冻结理由: API 是对外契约。变更影响所有消费者（Web, Mobile, 第三方）。
```

---

## 8. Naming Convention（命名规范）— 已冻结

```
定义位置: docs/governance/coding-standard.md

冻结内容:
  - Python: snake_case 模块/函数/变量, PascalCase 类, UPPER_SNAKE 常量
  - TypeScript: kebab-case 文件, PascalCase 组件, camelCase 函数
  - 数据库: snake_case 表/列, 复数表名
  - ID 前缀: ent_, rel_, stmt_, art_, src_, usr_, tsk_
  - Git: Conventional Commits, feature/bugfix/docs 分支前缀
  - Import 顺序: 标准库 → 第三方 → 项目内部

冻结理由: 命名一致性是代码可读性的基础。
```

---

## 9. Database Schema — 已冻结

```
定义位置: docs/08-data-model.md + docs/database/er-diagram.md

冻结内容:
  - 4 个 Schema (content, knowledge, account, system)
  - 13 张核心表结构 (列名、类型、约束)
  - 必选字段 (id UUID PK, created_at, updated_at, deleted_at, version)
  - EAV 属性模型 (knowledge_entity_properties)
  - 索引策略
  - 软删除策略 (deleted_at)

冻结理由: Schema 是数据一致性的基础。变更需要数据迁移。
```

---

## 10. Storage Engine — 已冻结

```
冻结内容:
  - PostgreSQL 16 + pgvector: Source of Truth
  - Neo4j 5: Graph Query (Read-optimized) — RFC-005
  - Elasticsearch 8: Fulltext Search — RFC-004
  - Redis 7: Cache + Message Bus (Redis Streams) — RFC-002
  - MinIO: Object Storage

冻结理由: 存储引擎选择影响性能和运维。变更需要数据迁移。
```

---

## 未冻结内容

以下内容尚未达到冻结标准，可在 Phase 1-2 中通过 RFC 调整：

- 前端框架 (Next.js — RFC-003, 待 Phase 4 实施前确认)
- 移动端框架 (Flutter — RFC-006, 待 Phase 4 确认)
- Embedding 模型 (OpenAI embed-3 — RFC-007, Phase 4 评估本地模型)
- AI Provider 路由策略 (RFC-008, 可在 Phase 3 调整)
- 插件热加载策略 (RFC-009, Phase 3 实施)
- 缓存策略细节
- 监控仪表盘设计
- UI 组件库选择

---

## 修订程序

1. 提出者撰写 ADR，标注 "Architecture Baseline Amendment"
2. ADR 必须包含 Breaking Change 影响分析 + 迁移计划
3. ≥ 2 Maintainer Approve
4. 本文件同步更新

---

*本基线自 2026-08-06 起生效。任何未列入本文件的架构决策不被视为已冻结。*
