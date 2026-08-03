# Event Model v2.0

## 概述

本文档定义 Athena 中所有领域事件的完整目录、负载结构和路由规则。

事件是限界上下文间解耦通信的唯一方式——不通过直接 API 调用、不通过共享数据库。

---

## 1. 事件基础模型

### 1.1 事件信封

```python
@dataclass
class EventEnvelope:
    """事件信封——所有事件的统一包装"""
    event_id: UUID
    event_type: str                  # 完整事件类型名
    aggregate_id: UUID               # 聚合根 ID
    aggregate_type: str              # 聚合根类型
    payload: dict                    # 事件负载（JSON）
    metadata: EventMetadata
    occurred_at: datetime

@dataclass
class EventMetadata:
    correlation_id: UUID             # 关联 ID（跨服务追踪）
    causation_id: UUID | None        # 因果事件 ID（哪个事件触发了此事件）
    source_context: str              # 发布上下文名称
    version: int = 1                 # 事件 Schema 版本
```

### 1.2 事件版本策略

- 事件负载不可变——发布后不修改
- Schema 变更通过 `version` 字段区分
- 消费者需兼容同一事件类型的不同版本
- 重大不兼容变更创建新事件类型（`EntityCreatedV2`）

---

## 2. Content Context 事件

### 2.1 SourceRegistered
```
Context: content
Aggregate: Source
--- Payload ---
source_id: UUID
source_name: str
source_type: str       # rss | api | scraper | manual
url: str
language: str
--- 订阅者 ---
Plugin Manager (自动发现新源插件)
```

### 2.2 SourcePaused / SourceResumed / SourceErrored
```
--- Payload ---
source_id: UUID
reason: str | None     # 暂停/错误原因
--- 订阅者 ---
Notification (SourceErrored → 告警通知)
```

### 2.3 ArticleFetched
```
Context: content
Aggregate: Article
--- Payload ---
article_id: UUID
source_id: UUID
url: str
url_hash: str
title: str
language: str
published_at: datetime
fetched_at: datetime
content_type: str      # article | paper | report | social_post | transcript
word_count: int
--- 订阅者 ---
Knowledge (→ 触发实体/关系抽取)
AI (→ 触发摘要生成)
Search (→ 触发索引)
Analytics (→ 内容量统计)
```

### 2.4 ArticlePublished
```
--- Payload ---
article_id: UUID
source_id: UUID
title: str
language: str
categories: list[str]
tags: list[str]
--- 订阅者 ---
Search (→ 索引更新)
Notification (→ 推送通知)
Analytics (→ 发布统计)
```

### 2.5 ArticleArchived / ArticleDeleted
```
--- Payload ---
article_id: UUID
--- 订阅者 ---
Search (→ 从索引中移除)
Knowledge (→ 降低关联声明权重)
```

### 2.6 ArticleSummarized
```
--- Payload ---
article_id: UUID
summary: str
model: str             # 使用的 AI 模型
tokens_used: int
--- 订阅者 ---
Search (→ 摘要索引更新)
```

### 2.7 ContentDuplicateDetected
```
--- Payload ---
existing_article_id: UUID
new_article_id: UUID
similarity_score: float
--- 订阅者 ---
Analytics (→ 去重统计)
```

---

## 3. Knowledge Context 事件

### 3.1 EntityCreated
```
Context: knowledge
Aggregate: KnowledgeEntity
--- Payload ---
entity_id: UUID
canonical_name: str
entity_type: str       # person | org | location | event | concept | product | work | natural
language: str
statement_ids: list[UUID]  # 创建该实体的声明
--- 订阅者 ---
Search (→ 实体索引)
Graph (→ Neo4j 节点创建)
Analytics (→ 实体增长统计)
```

### 3.2 EntityUpdated
```
--- Payload ---
entity_id: UUID
changed_fields: list[str]  # 变更的字段名列表
previous_values: dict      # 变更前的值（可选）
new_values: dict           # 变更后的值
--- 订阅者 ---
Search (→ 实体索引更新)
Graph (→ Neo4j 节点属性更新)
```

### 3.3 EntityMerged
```
--- Payload ---
source_entity_id: UUID
target_entity_id: UUID
merge_reason: str           # "duplicate_detected" | "manual_merge"
--- 订阅者 ---
Search (→ 合并搜索条目)
Graph (→ Neo4j 节点合并)
```

### 3.4 EntityDeprecated
```
--- Payload ---
entity_id: UUID
reason: str
--- 订阅者 ---
Search (→ 降低搜索权重)
Graph (→ 节点状态标记)
```

### 3.5 EntityPropertyConflictDetected
```
--- Payload ---
entity_id: UUID
property_key: str
conflicting_values: list[dict]  # [{value, confidence, statement_id}]
--- 订阅者 ---
Notification (→ 提醒人工审核)
```

### 3.6 RelationCreated
```
Context: knowledge
Aggregate: KnowledgeRelation
--- Payload ---
relation_id: UUID
relation_type: str
source_entity_id: UUID
target_entity_id: UUID
confidence: float
statement_ids: list[UUID]
--- 订阅者 ---
Search (→ 关系索引)
Graph (→ Neo4j 边创建)
```

### 3.7 RelationDeprecated
```
--- Payload ---
relation_id: UUID
reason: str
--- 订阅者 ---
Graph (→ 边状态标记)
```

### 3.8 StatementApproved / StatementRejected
```
Context: knowledge
Aggregate: Statement
--- Payload ---
statement_id: UUID
reviewer_id: UUID
review_comment: str | None
--- 订阅者 ---
Entity / Relation (→ 重新计算置信度)
Notification (→ 通知提交者)
Analytics (→ 审核统计)
```

### 3.9 KnowledgeSnapshotCreated
```
--- Payload ---
entity_id: UUID
snapshot_at: datetime
property_count: int
relation_count: int
--- 订阅者 ---
Analytics (→ 知识增长曲线)
```

---

## 4. Search Context 事件

### 4.1 SearchPerformed
```
Context: search
Aggregate: SearchIndex
--- Payload ---
query_text: str
search_mode: str       # fulltext | vector | hybrid
result_count: int
latency_ms: int
user_id: UUID | None
language: str | None
--- 订阅者 ---
Analytics (→ 搜索分析、热门查询)
```

### 4.2 IndexRebuildStarted / IndexRebuildCompleted / IndexRebuildFailed
```
--- Payload ---
index_id: UUID
index_type: str        # fulltext | vector
document_count: int
duration_ms: int | None  # completed only
error: str | None        # failed only
--- 订阅者 ---
Notification (IndexRebuildFailed → 告警)
```

---

## 5. AI Context 事件

### 5.1 TaskStarted / TaskCompleted / TaskFailed
```
Context: ai
Aggregate: CompletionTask
--- Payload ---
task_id: UUID
prompt_name: str
model: str
task_type: str         # summarize | translate | extract_entities | extract_relations
target_article_id: UUID | None
--- TaskCompleted 附加 ---
output: dict
tokens_used: int
cost_amount: Decimal
cost_currency: str
latency_ms: int
--- TaskFailed 附加 ---
error: str
retry_count: int
--- 订阅者 ---
Analytics (→ AI 用量/成本统计)
Notification (TaskFailed → 告警)
```

### 5.2 ModelSwitchEvent
```
--- Payload ---
task_id: UUID
from_model: str
to_model: str
reason: str            # "rate_limit" | "timeout" | "cost_threshold" | "quality_degradation"
--- 订阅者 ---
Analytics (→ 模型切换频率统计)
```

---

## 6. User Context 事件

### 6.1 UserRegistered
```
Context: user
Aggregate: User
--- Payload ---
user_id: UUID
email: str
--- 订阅者 ---
Notification (→ 欢迎邮件)
Analytics (→ 注册统计)
```

### 6.2 UserPreferencesUpdated
```
--- Payload ---
user_id: UUID
changed_preferences: list[str]
--- 订阅者 ---
Recommendation Engine (→ 重新计算推荐)
```

### 6.3 SubscriptionChanged
```
--- Payload ---
user_id: UUID
previous_tier: str
new_tier: str
--- 订阅者 ---
Notification (→ 确认通知)
Analytics (→ 收入统计)
```

---

## 7. 事件路由矩阵

| 事件 | Content | Knowledge | Search | AI | User | Notification | Analytics | Graph |
|------|:-------:|:---------:|:------:|:--:|:----:|:------------:|:---------:|:-----:|
| ArticleFetched | - | ✓ | ✓ | ✓ | | | | |
| ArticlePublished | - | | ✓ | | | ✓ | ✓ | |
| ArticleArchived | - | ✓ | ✓ | | | | | |
| EntityCreated | | - | ✓ | | | | ✓ | ✓ |
| EntityUpdated | | - | ✓ | | | | | ✓ |
| EntityMerged | | - | ✓ | | | | | ✓ |
| RelationCreated | | - | ✓ | | | | | ✓ |
| StatementApproved | | ✓ | | | | ✓ | ✓ | |
| SearchPerformed | | | - | | | | ✓ | |
| TaskCompleted | ✓ | ✓ | ✓ | - | | | ✓ | |
| UserRegistered | | | | | - | ✓ | ✓ | |
| PluginInstalled | ✓ | ✓ | ✓ | ✓ | | ✓ | | |

---

## 8. 事件存储与重放

### 8.1 Event Store

```sql
-- system_event_log 表（详见 ER Diagram）
-- 关键：事件不可变、不可删除
```

### 8.2 事件重放

```
# 重建 Neo4j 图（从 Event Store 重放）
FOR event IN events WHERE aggregate_type = 'KnowledgeEntity':
    IF event.type == 'EntityCreated':
        CREATE node
    ELIF event.type == 'EntityUpdated':
        UPDATE node
    ELIF event.type == 'EntityMerged':
        MERGE nodes
```

### 8.3 幂等性保证

- 所有事件消费者必须实现幂等处理
- 通过 `event_id` 去重
- 推荐使用 Redis 记录已处理的 event_id（TTL 7 天）

---

*事件目录随领域模型演进同步更新。新增事件类型无需 ADR，变更现有事件负载需 ADR。*
