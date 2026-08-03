# Domain Model v1.0-draft

## 概述

Athena 的领域模型遵循 Domain-Driven Design（DDD），以限界上下文（Bounded Context）为边界组织领域知识。

---

## 1. 限界上下文地图

```
┌──────────────────────────────────────────────────────────┐
│                     Athena Platform                       │
│                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Content  │  │Knowledge │  │  Search  │  │   AI     │ │
│  │ 内容管理 │  │ 知识图谱 │  │  搜索    │  │ AI 服务  │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘ │
│       │              │              │              │      │
│  ┌────┴──────────────┴──────────────┴──────────────┴───┐ │
│  │                   Shared Kernel                      │ │
│  │  Entity Base, Value Objects, Domain Events, ID Types │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐   │
│  │  User    │  │ Plugin   │  │ Notification         │   │
│  │  用户    │  │ 插件管理 │  │ 通知                 │   │
│  └──────────┘  └──────────┘  └──────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

### 上下文关系

- **Content → Knowledge**: 内容经过处理后产生知识
- **Content → AI**: 内容送入 AI 进行分析
- **Knowledge → Search**: 知识图谱提供增强搜索
- **AI → Knowledge**: AI 抽取的实体和关系更新图谱
- **User → All**: 用户上下文贯穿所有领域

---

## 2. Content Context（内容上下文）

### 核心职责
多源内容的接入、标准化、存储和生命周期管理。

### 领域实体

```
Source (内容源)
├── id: SourceId
├── name: str
├── type: SourceType (rss | api | scraper | manual)
├── url: HttpUrl
├── language: Language
├── fetch_config: FetchConfig
├── status: SourceStatus
└── last_fetched_at: datetime | None

Article (文章)
├── id: ArticleId
├── source_id: SourceId
├── url: HttpUrl
├── url_hash: str (去重标识)
├── title: str
├── content_raw: str (原始 HTML/文本)
├── content_clean: str (清洗后文本)
├── language: Language
├── author: str | None
├── published_at: datetime
├── fetched_at: datetime
├── status: ArticleStatus (draft | published | archived | deleted)
├── metadata: ArticleMetadata
└── version: int

ArticleMetadata (值对象)
├── word_count: int
├── reading_time_minutes: int
├── categories: list[str]
├── tags: list[str]
├── image_urls: list[HttpUrl]
└── source_metadata: dict
```

### 领域服务

- `ContentIngestionService`: 内容接入编排
- `ContentCleaningService`: HTML 清洗、文本标准化
- `DuplicateDetectionService`: 基于 URL/内容相似度的去重

---

## 3. Knowledge Context（知识上下文）

### 核心职责
实体识别、关系抽取、知识图谱构建与查询。

### 领域实体

```
Entity (实体)
├── id: EntityId
├── name: str
├── type: EntityType (person | org | location | event | concept | product)
├── aliases: list[str]
├── description: str
├── properties: dict
├── source_article_ids: list[ArticleId]
├── confidence: float
└── version: int

Relation (关系)
├── id: RelationId
├── source_entity_id: EntityId
├── target_entity_id: EntityId
├── type: RelationType
├── properties: dict
├── source_article_ids: list[ArticleId]
├── confidence: float
└── version: int

KnowledgeGraph (聚合根)
├── id: GraphId
├── name: str
├── description: str
├── entities: list[Entity] (懒加载)
├── relations: list[Relation] (懒加载)
└── snapshot_version: int
```

### 领域服务

- `EntityExtractionService`: 从文本中提取命名实体
- `RelationExtractionService`: 提取实体间关系
- `EntityLinkingService`: 实体链接与消歧
- `GraphQueryService`: 图谱查询（路径、子图、聚合）

---

## 4. Search Context（搜索上下文）

### 核心职责
全文搜索、向量搜索、混合搜索。

### 关键概念

```
SearchQuery (值对象)
├── text: str
├── language: Language
├── filters: SearchFilters
├── sort: SortConfig
└── pagination: Pagination

SearchResult
├── items: list[SearchResultItem]
├── total: int
├── facets: list[Facet]
└── suggestions: list[str]

SearchResultItem
├── article: Article | None
├── entity: Entity | None
├── score: float
├── highlights: dict[str, list[str]]
└── source: SearchSource (fulltext | vector | hybrid)
```

### 索引设计

- **全文索引**: Elasticsearch，支持多语言分词
- **向量索引**: pgvector / Qdrant，用于语义搜索
- **混合搜索**: RRF (Reciprocal Rank Fusion) 融合

---

## 5. AI Context（AI 上下文）

### 核心职责
模型路由、Prompt 管理、AI 能力编排。

### 领域实体

```
ModelProvider (聚合根)
├── id: ProviderId
├── name: str
├── provider_type: str (openai | anthropic | local)
├── models: list[ModelInfo]
├── config: ProviderConfig
└── status: ProviderStatus

PromptTemplate (实体)
├── id: PromptId
├── name: str
├── version: int
├── template: str (Jinja2)
├── variables: list[PromptVariable]
├── model_requirements: ModelRequirements
└── evaluations: list[PromptEvaluation]

CompletionTask (聚合根)
├── id: TaskId
├── prompt_id: PromptId
├── model: str
├── input: dict
├── output: CompletionResult | None
├── status: TaskStatus
├── tokens_used: int
├── cost: Decimal
└── latency_ms: int
```

---

## 6. User Context（用户上下文）

### 核心职责
用户身份、偏好、订阅管理。

### 领域实体

```
User (聚合根)
├── id: UserId
├── email: Email
├── display_name: str
├── preferences: UserPreferences
├── subscription: Subscription
├── role: UserRole
└── status: UserStatus

UserPreferences (值对象)
├── language: Language
├── topics: list[TopicId]
├── sources: list[SourceId]
├── notification_settings: NotificationSettings
└── ui_settings: dict
```

---

## 7. 领域事件

关键领域事件用于上下文间解耦通信：

| 事件 | 发布上下文 | 订阅上下文 |
|------|-----------|-----------|
| `ArticleFetched` | Content | Knowledge, AI |
| `ArticlePublished` | Content | Search, Notification |
| `EntityExtracted` | Knowledge | Search |
| `RelationFound` | Knowledge | Search |
| `SearchPerformed` | Search | Analytics |
| `UserRegistered` | User | Notification |
| `SubscriptionChanged` | User | Notification |

---

## 8. 领域模型演进原则

1. 领域模型独立于持久化方案
2. 聚合根保证事务一致性边界
3. 跨上下文通信只能通过事件或 API
4. 值对象不可变
5. 工厂方法创建复杂实体
6. 领域服务处理跨实体的业务逻辑

---

*本模型将通过 RFC 流程持续细化。*
