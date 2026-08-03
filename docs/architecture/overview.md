# Architecture Overview v1.0-draft

## 1. 架构愿景

Athena 的架构目标：构建一个**可演进十年以上**的 AI 驱动知识平台。

核心设计哲学：

- **演进式架构**: 当前不需要微服务，但架构允许未来拆分
- **适配器模式**: 基础设施可替换，核心领域不依赖具体实现
- **事件驱动**: 异步解耦，支持弹性扩展
- **CQRS 就绪**: 读写分离的架构基础

---

## 2. 系统全景图

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌─────────────┐ │
│  │   Web App │  │Mobile App │  │  API User │  │3rd-Party App│ │
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └──────┬──────┘ │
└────────┼───────────────┼──────────────┼───────────────┼────────┘
         │               │              │               │
         └───────────────┴──────┬───────┴───────────────┘
                                │
┌───────────────────────────────┼────────────────────────────────┐
│                       API Gateway Layer                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              API Gateway (Kong / Envoy)                    │  │
│  │   Auth │ Rate Limit │ Routing │ Versioning │ Logging      │  │
│  └────────────────────────┬─────────────────────────────────┘  │
└───────────────────────────┼────────────────────────────────────┘
                            │
┌───────────────────────────┼────────────────────────────────────┐
│                     Application Layer                           │
│  ┌─────────┐  ┌─────────┐  ┌────────┐  ┌──────────────────┐  │
│  │ Content │  │Knowledge│  │ Search │  │       AI         │  │
│  │ Service │  │ Service │  │Service │  │   Orchestrator   │  │
│  └────┬────┘  └────┬────┘  └───┬────┘  └────────┬─────────┘  │
│       │            │            │                │             │
│  ┌────┴────────────┴────────────┴────────────────┴─────────┐  │
│  │                    Plugin Manager                        │  │
│  │   Load │ Register │ Configure │ Lifecycle │ Isolate      │  │
│  └───────────────────────┬─────────────────────────────────┘  │
└──────────────────────────┼────────────────────────────────────┘
                            │
┌───────────────────────────┼────────────────────────────────────┐
│                     Infrastructure Layer                        │
│  ┌─────────┐  ┌──────────┐  ┌────────┐  ┌──────────────────┐ │
│  │PostgreSQL│  │Elastic.  │  │ Redis  │  │   Object Store   │ │
│  │ (Core)  │  │(Search)  │  │(Cache) │  │   (MinIO / S3)   │ │
│  └─────────┘  └──────────┘  └────────┘  └──────────────────┘ │
│                                                                │
│  ┌─────────┐  ┌──────────────────────────────────────────────┐│
│  │ Vector  │  │         Message Bus (RabbitMQ / Kafka)       ││
│  │ Store   │  │   Events │ Commands │ Dead Letter │ Retry    ││
│  └─────────┘  └──────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────────────┘
```

---

## 3. 架构决策

### 3.1 Modular Monolith → Microservices

**当前选择**: Modular Monolith

**理由**:
- Phase 0-3 的团队规模适合单体
- 避免分布式事务、网络延迟等复杂性
- 模块边界明确，未来拆分成本可控

**触发拆分条件**:
- 某模块需要独立扩展
- 某模块需要独立部署节奏
- 某模块需要不同的技术栈
- 团队规模 > 20 人

**如何拆分**: 内部模块间已通过接口通信，拆分时只需将接口替换为 RPC/消息。

### 3.2 同步 vs 异步

| 场景 | 模式 | 实现 |
|------|------|------|
| CRUD 操作 | 同步 REST | 立即返回结果 |
| 长时间 AI 任务 | 异步 202 | 任务状态轮询 |
| 内容处理管道 | 异步事件 | Message Bus |
| 搜索 | 同步 REST | < 200ms 响应 |
| 通知推送 | 异步事件 | Message Bus |

### 3.3 CQRS 策略

- **Phase 0-2**: 统一读写模型（简化开发）
- **Phase 3+**: 引入读模型（search_index 等）
- **Phase 5+**: 完整 CQRS（Event Sourcing 可选）

---

## 4. 技术选型（暂定，待 RFC 确定）

| 层级 | 候选方案 | 当前倾向 | 待决策 |
|------|---------|----------|--------|
| 后端语言 | Python / Go / Rust | Python | RFC-001 |
| 后端框架 | FastAPI / Litestar | FastAPI | RFC-002 |
| 前端框架 | Next.js / Remix | Next.js | RFC-003 |
| ORM | SQLAlchemy 2.0 / Prisma | SQLAlchemy 2.0 | RFC-004 |
| 消息队列 | RabbitMQ / Redis Streams | Redis Streams | RFC-005 |
| 搜索 | Elasticsearch / Meilisearch | Elasticsearch | RFC-006 |
| 向量数据库 | pgvector / Qdrant / Milvus | pgvector | RFC-007 |
| 图数据库 | Neo4j / PostgreSQL AGE | Neo4j | RFC-008 |
| API 网关 | Kong / Envoy / Traefik | Kong | RFC-009 |
| 容器编排 | Docker Compose / K8s | Docker Compose | RFC-010 |
| Mobile | Flutter / React Native | Flutter | RFC-011 |

---

## 5. 数据流

### 5.1 内容处理管道

```
Source → Fetch → Clean → Enrich → Store → Index → Publish
  │        │       │        │        │        │         │
  │        │       │        │        │        │         └→ Search Index
  │        │       │        │        │        └→ PostgreSQL + Elasticsearch
  │        │       │        │        └→ Knowledge Graph Update
  │        │       │        └→ NER + Translation + Summarization
  │        │       └→ HTML Strip + Markdown + Language Detection
  │        └→ RSS Parser / API Client / Headless Browser
  └→ Plugin Registry Selection
```

### 5.2 搜索流程

```
User Query → Query Understanding → Routing → Search → Ranking → Response
                  │                      │
                  │                      ├→ Fulltext (Elasticsearch)
                  │                      ├→ Vector (pgvector)
                  │                      └→ Graph (Neo4j)
                  │
                  └→ Intent Detection + Entity Extraction
```

### 5.3 AI 调用链

```
Task → Model Router → Provider API → Response → Post-process → Cache
  │        │              │
  │        │              └→ OpenAI / Anthropic / Local
  │        └→ load_balancer + fallback + cost optimization
  └→ Prompt Template + Context Assembly
```

---

## 6. 非功能性需求

### 6.1 性能目标

| 指标 | 目标 | 测量方式 |
|------|------|----------|
| API P50 延迟 | < 50ms | APM |
| API P99 延迟 | < 500ms | APM |
| 搜索 P50 延迟 | < 100ms | APM |
| 搜索 P99 延迟 | < 1s | APM |
| 内容处理吞吐 | > 1000/min | Metrics |
| AI 任务 P95 延迟 | < 30s | APM |

### 6.2 可用性

| 指标 | 目标 |
|------|------|
| 整体可用性 | 99.9%（Phase 4+）|
| 数据持久性 | 99.999% |
| RPO | < 1 小时 |
| RTO | < 4 小时 |

### 6.3 安全

- OWASP Top 10 全覆盖
- SOC 2 Type II 就绪架构
- GDPR 合规（数据驻留、删除权）
- 每季度渗透测试

---

## 7. 部署拓扑（Phase 4 目标）

```
┌─────────────────────────┐  ┌─────────────────────────┐
│      Region: Asia       │  │      Region: EU          │
│  ┌───────────────────┐  │  │  ┌───────────────────┐  │
│  │   Application     │  │  │  │   Application     │  │
│  │   + PostgreSQL    │  │  │  │   + PostgreSQL    │  │
│  └───────────────────┘  │  │  └───────────────────┘  │
└─────────────────────────┘  └─────────────────────────┘
            │                            │
            └──────────┬─────────────────┘
                       │
            ┌──────────┴──────────┐
            │    Global DNS LB    │
            │   (Geo-routing)     │
            └─────────────────────┘
```

---

*本文档随架构演进持续更新。每个技术选型决策必须通过 ADR 记录。*
