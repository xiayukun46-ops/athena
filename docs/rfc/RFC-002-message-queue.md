# RFC-002: 消息队列选型

## Metadata

| 字段 | 内容 |
|------|------|
| RFC ID | RFC-002 |
| Title | 消息队列 / Event Bus 选型 |
| Status | Draft |
| Author | AI Chief Architect |
| Created | 2026-08-03 |
| Target Phase | Phase 1 |
| Priority | P0 |

## Abstract

决定 Athena 的领域事件总线和异步任务队列的技术选型。
候选方案为 Redis Streams、RabbitMQ、Kafka。本 RFC 给出推荐决策及理由。

---

## Motivation

消息队列是 Athena 架构的核心组件：

1. **领域事件总线**：Content → Knowledge → Search → Notification 的异步解耦
2. **AI 任务队列**：Summarize / Translate / Extract 等异步任务的调度
3. **PG → Neo4j 同步**：事件驱动的图数据同步
4. **Outbox Pattern**：保证 PostgreSQL 写入与事件发布的原子性（缓解 R2 风险）

### 选型维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 运维复杂度 | 30% | Modular Monolith 阶段运维成本是首要考量 |
| 消息可靠性 | 25% | 不丢消息、持久化、死信队列 |
| 性能 | 20% | 吞吐量、延迟 |
| 扩展性 | 15% | 从单体到微服务的迁移路径 |
| 功能丰富度 | 10% | 路由、重试、延迟消息、流处理 |

---

## Proposal

### 推荐方案：Phase 1-2 用 Redis Streams，Phase 3+ 评估 Kafka

**We will use Redis Streams as the primary event bus for Phase 1-2, with a planned evaluation of Kafka for Phase 3+.**

### 理由

#### 1. 运维复杂度最低（Modular Monolith 阶段首选）

- Athena 已经依赖 Redis 做缓存——不需要引入新的基础设施组件
- Redis Streams 内置于 Redis 7.x，零额外部署
- 单体阶段只有 1 个消费者组，Redis Streams 完全够用
- Docker Compose 开发环境无需新增服务

#### 2. 消息可靠性满足 Phase 1-2 需求

- Redis Streams 支持 Consumer Group、ACK 确认、Pending 消息重试
- 消息持久化到 RDB/AOF
- 配合 `system_event_log` 表（Outbox Pattern），实现双保险：PG 落库 + Redis 投递

#### 3. 性能充足

- Redis 内存操作，延迟 < 1ms
- 单体阶段的吞吐量（< 10k msg/s）Redis 远未达到瓶颈

#### 4. 平滑迁移路径

- Redis Streams → Kafka 的接口差异可通过 Adapter 模式封装
- Domain Event 的 `IEventBus` 接口已定义，换实现不影响业务代码
- Phase 3+ 引入 Kafka 时，只需替换 Adapter 实现

#### 5. 不选 RabbitMQ 的理由

RabbitMQ 功能丰富但运维复杂度高（独立的 Erlang 运行时、集群配置、镜像队列）。
Phase 0-3 的 Modular Monolith 只有一个 Broker 实例，RabbitMQ 的优势（复杂路由、联邦）无法体现。

---

## Alternatives Considered

### 方案 A：Redis Streams ✅ 推荐（Phase 1-2）

| 维度 | 评分 |
|------|------|
| 运维复杂度 | ★★★★★ |
| 消息可靠性 | ★★★★☆ |
| 性能 | ★★★★★ |
| 扩展性 | ★★★☆☆ (单体 → 分布式需要外部协调) |
| 功能丰富度 | ★★★☆☆ (无原生 DLQ、延迟消息需手动实现) |

### 方案 B：RabbitMQ

| 维度 | 评分 |
|------|------|
| 运维复杂度 | ★★☆☆☆ (Erlang 运维 + 集群管理) |
| 消息可靠性 | ★★★★★ |
| 性能 | ★★★★☆ |
| 扩展性 | ★★★★☆ |
| 功能丰富度 | ★★★★★ (DLQ、延迟队列、TTL 原生支持) |

**不选原因**：运维复杂度对单体阶段过重。当 Athena 需要的消息路由复杂度（如 Topic Exchange、Header Exchange）自然出现时（Phase 3+），再评估是否引入。

### 方案 C：Kafka

| 维度 | 评分 |
|------|------|
| 运维复杂度 | ★☆☆☆☆ (ZooKeeper/KRaft + Brokers) |
| 消息可靠性 | ★★★★★ |
| 性能 | ★★★★★ |
| 扩展性 | ★★★★★ |
| 功能丰富度 | ★★★★★ (Streams、Kafka Connect) |

**不选原因**：Kafka 为分布式而生，单体阶段严重过度设计。运维成本（至少 3 Broker + KRaft）对 Phase 1-2 不合理。Phase 3+ 当事件量达到 > 100k msg/s 或需要多消费者组并行时重新评估。

---

## Impact Assessment

### Breaking Changes
无。

### Performance
- Redis Streams 在单体部署中延迟 < 1ms
- Consumer Group 支持水平扩展 Worker 数量
- 单体阶段推荐 1 Consumer Group → 多 Worker 并发消费模式

### Security
- Redis 需配置密码认证
- 生产环境 Redis 不与公网直连

### Testing
- 集成测试使用 Testcontainers Redis 实例
- 事件处理器单元测试直接调用 Handler，不经过 Broker

---

## Implementation Plan

### Phase 1: Outbox + Redis Streams

```
Transaction:
  1. Write to PostgreSQL (aggregate)
  2. Write to system_event_log (outbox)
  3. Publish to Redis Streams (fire-and-forget)
  
Outbox Worker:
  1. Poll system_event_log for unprocessed events
  2. Publish to Redis Streams
  3. Mark as processed
```

### Phase 3+: Kafka Migration Trigger

当以下任一条件满足时，启动 Kafka 迁移评估：
- 日均事件量 > 10M
- 需要 > 3 个独立 Consumer Group
- 需要 Event Replay / Time Travel（Kafka 的日志保留优势）
- 需要 Kafka Connect 集成到 Data Lake

---

## Open Questions

- [ ] Outbox Worker 的轮询间隔和批处理大小？→ Phase 1 压测后确定
- [ ] Redis Streams 的 MAXLEN 截断策略？→ 默认 100k，Phase 2 Review

## References

- [Event Model](../domain/event-model.md) — 领域事件目录
- [Architecture Overview](../architecture/overview.md) — 消息总线定位
- [Architecture Review](../architecture/review-2026-08-03.md) — R1/R2 风险
