# 07 — Architecture Overview

> Athena 系统架构总览。从分层到组件到数据流。

**详细设计见**: [architecture/overview.md](architecture/overview.md) + [BLUEPRINT.md](BLUEPRINT.md)

---

## 架构风格: Modular Monolith

### 为什么不是微服务

当前团队规模和项目阶段（Phase 0-3）不需要分布式复杂度。

**替代方案对比**:

| 方案 | 部署 | 通信 | 事务 | 复杂度 | 适合阶段 |
|------|------|------|------|--------|----------|
| Modular Monolith | 单进程 | 进程内调用 | ACID | 低 | Phase 0-3 |
| Microservices | 多进程 | RPC/消息 | 最终一致 | 高 | Phase 4+ |
| Serverless | 函数 | 事件 | 无 | 中 | 不适合有状态知识处理 |

**拆分触发条件**（任一满足即启动拆分评估）:
- 某模块需要独立扩容
- 某模块需要不同技术栈
- 团队 > 20 人
- 部署频率需求差异大

### 为什么拆分成本低

模块间已通过**接口**（非直接调用）通信。例如：
- `ISourcePlugin` → 不是 `class RssSourcePlugin`
- `IEventBus` → 不是 `RedisStreamsClient`

拆分时把接口实现从"进程内"改为"gRPC/REST"，接口本身不变。

---

## 系统分层

```
Client Layer:     Web (Next.js) | Mobile (TBD) | API Consumers
                        │ HTTPS + WSS
API Gateway:       Kong — Auth | Rate Limit | Routing
                        │
Application:       Content | Knowledge | Search | AI | User | Plugin
                        │
Infrastructure:    PostgreSQL | Neo4j | Elasticsearch | Redis | MinIO
```

### 为什么有 API Gateway

**替代方案**: 各服务直接暴露端口。

不选理由：认证、限流、版本路由、日志应该在统一入口处理，而不是每个服务自己实现。

### 为什么选择 Kong

- Nginx/OpenResty 基础，高性能
- 插件生态丰富（认证、限流、日志、监控）
- 声明式配置（Kong Ingress Controller for K8s）

**替代方案**: Envoy, Traefik。Kong 在 API 管理功能上更完整。

---

## 数据存储分工

| 存储 | 角色 | 数据类型 |
|------|------|----------|
| PostgreSQL | Source of Truth | 所有业务数据 |
| Neo4j | Graph Query View | 知识图谱（只读副本） |
| Elasticsearch | Fulltext Index | 搜索索引 |
| Redis | Cache + Queue | 缓存 + 事件流 + 限流 |
| MinIO | Object Store | 原始 HTML、图片、文档 |

### 为什么 PG 是 Source of Truth

所有写操作只发生在 PostgreSQL。Neo4j 和 ES 通过消费事件同步更新。

**替代方案**: Neo4j 做主存储。不选理由：知识图谱是核心但不是全部——还有用户、订阅、统计等关系型数据。

---

## 关键数据流

**内容管道**:
```
Source → Collector → Article (PG) → ArticleFetched Event
                                        │
                ┌───────────────────────┼───────────────────────┐
                ▼                       ▼                       ▼
        AI Extraction          Search Indexer           Knowledge Pipeline
        (Summarize)            (Elasticsearch)          (NER → Linking → RE)
                                                               │
                                                               ▼
                                                       Entity/Relation (PG)
                                                               │
                                                               ▼
                                                       Graph Sync (Neo4j)
```

**搜索流程**:
```
User Query → Search Service → [Fulltext (ES) + Vector (pgvector)] → RRF → Results
```

**问答流程**:
```
User Question → Entity Search → Get Relations → Assemble Context → LLM → Answer + Citations
```

---

## 质量属性

| 属性 | 目标 | 实现方式 |
|------|------|----------|
| 性能 | API P50 < 50ms | FastAPI + async + Redis Cache |
| 可用性 | 99.9% (Phase 4+) | 多节点 + LB + 健康检查 |
| 可扩展 | 水平扩展 | Modular Monolith → Microservices |
| 安全 | OWASP Top 10 全覆盖 | 见 [13-security.md](13-security.md) |
| 可观测 | 全链路追踪 | OpenTelemetry + Sentry |

---

## 相关文档

- [04-domain-model.md](04-domain-model.md) — 怎么组织代码
- [08-data-model.md](08-data-model.md) — 怎么存数据
- [09-plugin-system.md](09-plugin-system.md) — 怎么扩展
- [13-security.md](13-security.md) — 怎么保护
- [BLUEPRINT.md](BLUEPRINT.md) — 完整施工蓝图
