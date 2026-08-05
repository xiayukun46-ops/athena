# Knowledge Canon

> Athena 知识对象的唯一权威定义。本文档是 Single Source of Truth。
> 任何模块不得重复定义本文档中已定义的术语和结构。
> 版本：v1.0 | 批准日期：2026-08-06

---

## 1. 概述

Knowledge Canon 定义了 Athena 知识系统中所有核心对象的语义、结构、约束和关系。它是领域模型（`04-domain-model.md`）的子集——只定义"知识对象是什么"，不定义"代码怎么写"（那是 DDD 的职责）。

### 使用规则

1. **唯一真理**：任何地方需要引用"Entity"的定义 → 引用本文档。不要在 `docs/api/`、`docs/domain/`、`.ai/` 中重复定义。
2. **变更流程**：修改本文档需通过 RFC，因为这影响所有模块。
3. **版本化**：本文档使用语义化版本。Breaking Change（如删除字段）→ 主版本递增。

---

## 2. Identity（身份）

每个知识对象有一个全局唯一的 Identity。

```
Identity = {prefix}_{uuid_short}

前缀约定:
  ent_   KnowledgeEntity     ent_a1b2c3d4
  rel_   KnowledgeRelation   rel_e5f6g7h8
  stmt_  Statement           stmt_i9j0k1l2
  art_   Article             art_m3n4o5p6
  src_   Source              src_q7r8s9t0
  usr_   User                usr_u1v2w3x4
  tsk_   CompletionTask      tsk_y5z6a7b8
```

**规则**:
- ID 创建后不可变
- 被合并的实体的 ID 永久保留（指向合并目标）
- ID 不携带语义信息（不要 `ent_apple_inc`）——语义信息在 `canonical_name` 字段中

---

## 3. Knowledge Object（知识对象）

### 3.1 KnowledgeEntity（知识实体）

现实世界中的具体事物或抽象概念。

```yaml
KnowledgeEntity:
  id: Identity                    # ent_{8}
  canonical_name: String          # 规范名称（全局尽量唯一）
  entity_type: EntityType         # 8 种类型之一
  names: list[EntityName]         # 多语言名称
  aliases: list[EntityAlias]      # 别名/缩写/曾用名
  description: String             # 自然语言描述
  properties: list[EntityProperty] # EAV 扩展属性
  status: EntityStatus            # draft | active | deprecated | merged
  merged_into: Identity | None    # 被合并到的目标实体 ID
  quality_score: QualityScore     # 质量评分
  created_at: Timestamp
  updated_at: Timestamp
  version: Integer
```

**EntityType（实体类型）**: `PERSON | ORGANIZATION | LOCATION | EVENT | CONCEPT | PRODUCT | WORK | NATURAL_ENTITY`

**EntityStatus（生命周期）**: `DRAFT → ACTIVE → DEPRECATED → MERGED`

---

### 3.2 KnowledgeRelation（知识关系）

两个 KnowledgeEntity 之间的有向连接。

```yaml
KnowledgeRelation:
  id: Identity                    # rel_{8}
  relation_type: RelationType     # 关系类型
  source_entity_id: Identity      # 关系起点
  target_entity_id: Identity      # 关系终点
  properties: dict                # 扩展属性（如 role, start_date）
  statements: list[Identity]      # 支撑此关系的声明 ID 列表
  confidence: Confidence          # 综合置信度 0.0-1.0
  valid_from: Timestamp | None    # 关系开始时间
  valid_until: Timestamp | None   # 关系结束时间
  status: RelationStatus          # active | deprecated
  quality_score: QualityScore
  created_at: Timestamp
  updated_at: Timestamp
  version: Integer
```

**RelationType（关系类型）**: `INSTANCE_OF | SUBCLASS_OF | PART_OF | MEMBER_OF | WORKS_FOR | FOUNDED | LED_BY | LOCATED_IN | PARTICIPATED_IN | CAUSED | RELATED_TO` 等 20+ 种

---

### 3.3 Statement（声明）

从原始内容中提取的、关于实体或关系的可溯源断言。

```yaml
Statement:
  id: Identity                    # stmt_{8}
  statement_type: StatementType   # entity_extraction | relation_extraction | manual
  subject_id: Identity            # 声明对象（Entity ID 或 Relation ID）
  predicate: String               # 属性名（如 "birth_date"）
  object_value: String            # 属性值（如 "1964-01-07"）
  confidence: Confidence          # 提取/输入时的置信度
  extraction_method: String       # AI 模型标识 或 "manual"
  source: StatementSource         # 溯源信息
  reviewer_id: Identity | None    # 审核人
  review_status: ReviewStatus     # pending | approved | rejected
  created_at: Timestamp
```

**StatementSource（溯源）**:
```yaml
StatementSource:
  article_id: Identity            # 源文章
  snippet: String                 # 原文摘录
  position: Integer               # 文章内位置偏移
```

---

### 3.4 Event（领域事件）

限界上下文中发生的有意义的状态变化。不同于"知识事件"（如政治事件）——那是 KnowledgeEntity 的一种。

```yaml
DomainEvent:
  event_id: Identity
  event_type: String              # ArticleFetched, EntityCreated ...
  aggregate_id: Identity          # 聚合根 ID
  aggregate_type: String          # Article, KnowledgeEntity ...
  payload: dict                   # 事件负载
  metadata: EventMetadata
  occurred_at: Timestamp
  version: Integer                # 事件 Schema 版本

EventMetadata:
  correlation_id: Identity        # 关联 ID（跨服务追踪）
  causation_id: Identity | None   # 因果事件 ID
  source_context: String          # 发布上下文名称
```

---

### 3.5 Evidence（证据）

Statement 的溯源信息即为 Evidence。证据链：`Article → Statement → Entity.Property`。

用户点击任何实体属性，可以追溯到：
1. 支撑该属性的 Statement 列表
2. 每个 Statement 的原始文章和摘录片段
3. AI 提取该 Statement 时使用的模型和置信度

---

### 3.6 Source（内容源）

内容的来源。不同于 StatementSource——Source 是数据源配置，StatementSource 是声明溯源。

```yaml
Source:
  id: Identity                    # src_{8}
  name: String
  source_type: SourceType         # rss | api | scraper | manual
  url: URL
  language: Language
  credibility: SourceCredibility  # 来源可信度
```

**SourceCredibility**:
```yaml
SourceCredibility:
  credibility_score: Float        # 0.0 - 1.0
  bias_leaning: String | None     # left / center / right
  fact_check_rating: String | None
  domain_authority: Float         # 领域权威性 0.0-1.0
```

---

### 3.7 Timeline（时间线）

实体属性随时间的变化序列。通过 `EntityProperty.valid_from/valid_until` 和 `EntitySnapshot` 实现。

```yaml
EntitySnapshot:
  entity_id: Identity
  snapshot_at: Timestamp          # 快照时间点
  properties: dict                # 该时间点的所有属性
  active_relations: list[Identity] # 该时间点的活跃关系
```

---

### 3.8 Version（版本）

```yaml
版本层次:
  设计文档版本: 文件内标注（如 v1.0）+ Git 历史
  领域事件版本: event.version 字段（整数递增）
  Prompt 版本:    模板文件内标注（SemVer）
  API 版本:       URL 路径（/v1/, /v2/）
  数据版本:       aggregate.version 字段（乐观锁）
```

---

### 3.9 Metadata（元数据）

所有知识对象共享的元数据结构：

```yaml
StandardMetadata:
  created_at: Timestamp
  updated_at: Timestamp
  deleted_at: Timestamp | None    # 软删除
  version: Integer                # 乐观锁
```

---

### 3.10 Quality Score（质量评分）

```yaml
QualityScore:
  completeness: Float             # 属性填充率 0.0-1.0
  consistency: Float              # 冲突声明占比的反比
  freshness: Float                # 最近更新距今时间的衰减
  confidence: Float               # 支撑声明的平均置信度
  provenance: Float               # 可溯源声明占比
  diversity: Float                # 唯一来源数
  overall: Float                  # 加权综合评分
```

---

### 3.11 Lifecycle（生命周期）

```yaml
KnowledgeEntity:
  DRAFT → ACTIVE → DEPRECATED → MERGED

KnowledgeRelation:
  ACTIVE → DEPRECATED

Statement:
  [Created] → PENDING → APPROVED | REJECTED

Article:
  DRAFT → PUBLISHED → ARCHIVED → DELETED

Source:
  ACTIVE → PAUSED → ERROR → DEPRECATED
```

---

### 3.12 Permissions（权限）

```yaml
Permission:
  scope: list[PermissionScope]    # read:entities, write:statements ...
  constraints: dict               # 资源级限制

PermissionScope:
  READ_SOURCES | WRITE_SOURCES
  READ_ARTICLES | WRITE_ARTICLES
  READ_ENTITIES | WRITE_ENTITIES | MERGE_ENTITIES
  READ_RELATIONS | WRITE_RELATIONS
  READ_STATEMENTS | WRITE_STATEMENTS | APPROVE_STATEMENTS
  SEARCH
  AI_CHAT | AI_SUMMARIZE | AI_TRANSLATE | AI_EXTRACT
  MANAGE_PLUGINS
  MANAGE_USERS
  VIEW_ANALYTICS
```

---

## 4. 交叉引用规则

本文档中定义的所有概念，在以下文档中**不得重复定义**：

| 文档 | 允许的操作 |
|------|-----------|
| `docs/04-domain-model.md` | 引用：描述限界上下文如何使用这些对象 |
| `docs/api/api-design.md` | 引用：描述 API 如何暴露这些对象 |
| `docs/database/er-diagram.md` | 翻译：将本文档的 YAML 翻译为 SQL DDL |
| `docs/domain/graph-model.md` | 映射：将本文档的 Entity/Relation 映射为 Neo4j 节点/边 |
| `docs/domain/event-model.md` | 扩展：基于本文档的 DomainEvent 定义具体事件 |
| `.ai/` 所有文件 | **禁止**包含领域对象定义——引用本文档 |

---

## 5. 修订历史

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-08-06 | v1.0 | 初始发布。定义 13 个知识对象的完整规范 |
