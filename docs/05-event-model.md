# 05 — Event Model

> 领域事件是 Athena 上下文间通信的唯一方式。本文档定义事件的设计原则、目录和路由。

**完整事件目录见**: [domain/event-model.md](domain/event-model.md)

---

## 为什么用事件驱动

### 核心问题: 上下文间如何通信？

**替代方案 1: 直接 API 调用**

Content 发布文章后直接调 Knowledge 的 API：`POST /internal/entities/extract`

- **不选理由**: 产生编译期依赖、级联故障（Knowledge 挂了 Content 也挂）、无法重放
- **适用场景**: 同步请求（如用户搜索），不适用异步处理管道

**替代方案 2: 共享数据库**

Content 写 `articles` 表，Knowledge 直接读 `articles` 表。

- **不选理由**: 打破上下文边界、Knowledge 与 Content 的表结构耦合、数据迁移互相阻塞
- **适用场景**: 单体应用快速开发（不是 10 年项目）

**选择: 事件驱动**

Content 发布 ArticleFetched 事件。Knowledge、AI、Search 各自消费。Content 不需要知道谁在消费。

### 事件驱动的优势

1. **解耦**: 发布者不知道消费者
2. **可重放**: Event Store 记录所有事件，可重建系统状态
3. **可扩展**: 新消费者只需订阅事件，不修改发布者
4. **审计**: 完整的事件历史是可追溯的审计日志

### 事件驱动的代价

1. **最终一致性**: 不是强一致。Article 发布后 Neo4j 图可能延迟 < 1s。
2. **调试复杂**: 需要追踪事件链。
3. **顺序性**: 同一聚合根的事件必须有序。

---

## 事件设计原则

### 原则 1: 事件不可变

发布后的事件永不修改。如果需要纠正错误，发布一个新事件（补偿事件）。

### 原则 2: 事件命名用过去式

`ArticleFetched` 而非 `FetchArticle`。事件描述"已发生的事实"。

### 原则 3: 事件包含足够上下文

消费者不应为了理解事件而回调发布者。关键字段都在 Payload 中。

### 原则 4: 每个事件关联一个聚合根

`ArticleFetched` 的 aggregate 是 Article。`EntityCreated` 的 aggregate 是 KnowledgeEntity。

---

## 事件目录（核心）

| 事件 | 上下文 | 聚合根 | 关键 Payload |
|------|--------|--------|-------------|
| `ArticleFetched` | Content | Article | article_id, source_id, url_hash, title, language, content_type |
| `ArticlePublished` | Content | Article | article_id, categories, tags |
| `EntityCreated` | Knowledge | KnowledgeEntity | entity_id, canonical_name, entity_type, statement_ids |
| `EntityUpdated` | Knowledge | KnowledgeEntity | entity_id, changed_fields |
| `EntityMerged` | Knowledge | KnowledgeEntity | source_entity_id, target_entity_id |
| `RelationCreated` | Knowledge | KnowledgeRelation | relation_id, type, source/target entity, statement_ids |
| `StatementApproved` | Knowledge | Statement | statement_id, reviewer_id |
| `TaskCompleted` | AI | CompletionTask | task_id, output, tokens_used, cost |
| `SearchPerformed` | Search | SearchIndex | query_text, mode, result_count, latency_ms |
| `UserRegistered` | User | User | user_id, email |

完整目录（20+ 事件）见 [domain/event-model.md](domain/event-model.md)。

---

## 事件路由

```
ArticleFetched → [Knowledge (实体提取), AI (摘要生成), Search (索引)]
EntityCreated  → [Search (实体索引), Graph (Neo4j 同步)]
RelationCreated → [Graph (Neo4j 同步)]
StatementApproved → [Knowledge (重新计算置信度)]
TaskCompleted → [Content (更新摘要), Knowledge (存储提取结果)]
```

---

## 实现: Outbox Pattern

**问题**: 如何保证"写数据库"和"发事件"的原子性？

**方案**: 
1. 事件写入 `system_event_log` 表（与业务数据在同一个 PG 事务中）
2. 独立 Outbox Worker 轮询 `system_event_log`，投递到 Redis Streams
3. 消费者从 Redis Streams 消费

**为什么不全用 Redis Streams**: Redis 不参与 PG 事务。如果 PG 写入成功但 Redis 投递失败，数据不一致。Outbox 的双保险保证了原子性。

---

## 未来影响

- **Phase 3+**: Redis Streams → Kafka 迁移。IEventBus 接口不变，只换 Adapter
- **Event Sourcing（Phase 5+）**: 聚合根的状态变为所有事件的折叠结果
- **CQRS**: 读写分离时，读模型通过消费事件更新

---

## 相关文档

- [04-domain-model.md](04-domain-model.md) — 领域上下文定义
- [06-knowledge-engine.md](06-knowledge-engine.md) — 事件如何驱动知识提取
- [07-architecture.md](07-architecture.md) — 事件在架构中的位置
- [rfc/RFC-002-message-queue.md](rfc/RFC-002-message-queue.md) — 消息队列选型
