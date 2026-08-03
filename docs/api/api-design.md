# API Design v2.0

## 概述

Athena 提供两套 API 范式：
- **RESTful API**: 资源 CRUD、搜索、AI 任务
- **GraphQL API**: 灵活的知识图谱查询、复合数据获取

所有 API 遵循 [API Style Guide](../../API_STYLE_GUIDE.md) 的约定。

---

## 1. 基础约定

### 1.1 URL 前缀

```
https://api.athena.ai/v1
```

### 1.2 认证

```http
Authorization: Bearer {jwt_token}
X-API-Key: {api_key}           # 服务间调用
```

### 1.3 通用请求头

```http
Content-Type: application/json
Accept: application/json
Accept-Language: zh-CN
X-Request-ID: {uuid}
X-Idempotency-Key: {key}       # 写操作幂等
```

### 1.4 通用响应格式

```json
{
  "data": { ... },
  "_meta": {
    "request_id": "...",
    "took_ms": 42,
    "page": 1,
    "size": 20,
    "total": 100,
    "next_cursor": "..."
  },
  "_links": {
    "self": "/v1/articles/123",
    "next": "/v1/articles?page=2"
  }
}
```

### 1.5 错误响应

```json
{
  "error": {
    "code": "ENTITY_NOT_FOUND",
    "message": "The requested entity could not be found.",
    "details": [
      {"field": "id", "issue": "Entity ent_xxx does not exist"}
    ]
  },
  "_meta": {
    "request_id": "..."
  }
}
```

---

## 2. Content API

### 2.1 Sources（内容源）

```
GET    /v1/sources                           # 列表内容源
GET    /v1/sources/{source_id}               # 内容源详情
POST   /v1/sources                           # 注册新内容源
PUT    /v1/sources/{source_id}               # 更新内容源
DELETE /v1/sources/{source_id}               # 删除内容源
POST   /v1/sources/{source_id}/pause         # 暂停
POST   /v1/sources/{source_id}/resume        # 恢复
POST   /v1/sources/{source_id}/fetch         # 手动触发抓取
```

**POST /v1/sources — 请求体**:
```json
{
  "name": "TechCrunch RSS",
  "source_type": "rss",
  "url": "https://techcrunch.com/feed/",
  "language": "en",
  "fetch_config": {
    "interval_seconds": 600,
    "timeout_seconds": 30,
    "max_items_per_fetch": 50
  }
}
```

**GET /v1/sources — 查询参数**:
```
?type=rss&language=en&status=active&page=1&size=20&sort=-created_at
```

### 2.2 Articles（文章）

```
GET    /v1/articles                           # 文章列表
GET    /v1/articles/{article_id}              # 文章详情（含全文）
GET    /v1/articles/{article_id}/related      # 关联文章
GET    /v1/articles/{article_id}/entities     # 文章中的实体
GET    /v1/articles/{article_id}/statements   # 文章产生的声明
DELETE /v1/articles/{article_id}              # 软删除
```

**GET /v1/articles — 查询参数**:
```
?source_id=...         # 按源筛选
&status=published      # 按状态筛选
&language=zh           # 按语言筛选
&category=AI           # 按分类筛选
&from=2026-01-01       # 发布起始时间
&to=2026-12-31         # 发布结束时间
&sort=-published_at    # 排序（- 降序）
&page=1&size=20        # 分页
&fields=title,summary,published_at  # 稀疏字段
```

**响应示例**:
```json
{
  "data": [
    {
      "id": "art_abc123",
      "type": "article",
      "attributes": {
        "title": "AI Breakthrough in Protein Folding",
        "summary": "Researchers at DeepMind...",
        "url": "https://techcrunch.com/2026/08/01/ai-protein/",
        "language": "en",
        "content_type": "article",
        "word_count": 1500,
        "reading_time_minutes": 6,
        "published_at": "2026-08-01T12:00:00Z",
        "categories": ["AI", "Science"],
        "tags": ["DeepMind", "protein-folding", "AlphaFold"]
      },
      "relationships": {
        "source": {"data": {"id": "src_001", "type": "source"}},
        "authors": {"data": [{"id": "aut_001", "type": "author"}]}
      },
      "_links": {
        "self": "/v1/articles/art_abc123",
        "source": "/v1/sources/src_001",
        "entities": "/v1/articles/art_abc123/entities"
      }
    }
  ],
  "_meta": {
    "total": 1024,
    "page": 1,
    "size": 20
  }
}
```

---

## 3. Knowledge API

### 3.1 Entities（知识实体）

```
GET    /v1/entities                           # 实体搜索/列表
GET    /v1/entities/{entity_id}               # 实体详情
POST   /v1/entities                           # 手动创建实体
PUT    /v1/entities/{entity_id}               # 更新实体
POST   /v1/entities/{entity_id}/merge         # 合并实体
POST   /v1/entities/{entity_id}/deprecate     # 废弃实体
GET    /v1/entities/{entity_id}/timeline      # 实体时间线
GET    /v1/entities/{entity_id}/relations     # 实体的关系列表
GET    /v1/entities/{entity_id}/statements    # 实体的声明列表
```

**GET /v1/entities — 查询参数**:
```
?q=Apple               # 模糊搜索（名称/别名）
&type=organization     # 实体类型
&language=en           # 名称语言
&status=active         # 实体状态
&min_confidence=0.7    # 最小置信度
&page=1&size=20
&sort=-created_at
```

**GET /v1/entities/{entity_id} — 响应**:
```json
{
  "data": {
    "id": "ent_apple",
    "type": "entity",
    "attributes": {
      "canonical_name": "Apple Inc.",
      "entity_type": "organization",
      "names": [
        {"name": "Apple Inc.", "language": "en", "is_preferred": true},
        {"name": "苹果公司", "language": "zh", "is_preferred": true},
        {"name": "アップル", "language": "ja"}
      ],
      "aliases": [
        {"alias": "AAPL", "alias_type": "acronym"},
        {"alias": "Apple Computer", "alias_type": "former_name"}
      ],
      "description": "American multinational technology company...",
      "properties": {
        "founded_date": "1976-04-01",
        "headquarters": "Cupertino, California, United States",
        "industry": "Technology",
        "market_cap": "3.5T",
        "employee_count": "164000",
        "ticker_symbol": "AAPL"
      },
      "status": "active",
      "confidence": 0.98,
      "source_count": 1250,
      "created_at": "2026-07-01T00:00:00Z",
      "updated_at": "2026-08-03T12:00:00Z"
    },
    "relationships": {
      "statements": {"data": [{"id": "stmt_001", "type": "statement"}]},
      "articles": {"data": [{"id": "art_001", "type": "article"}]}
    },
    "_links": {
      "relations": "/v1/entities/ent_apple/relations",
      "timeline": "/v1/entities/ent_apple/timeline",
      "graph": "/v1/graph/entity/ent_apple/neighbors"
    }
  }
}
```

### 3.2 Relations（关系）

```
GET    /v1/relations/{relation_id}            # 关系详情
GET    /v1/entities/{entity_id}/relations     # 实体的所有关系
POST   /v1/relations/{relation_id}/deprecate  # 废弃关系
```

**GET /v1/entities/{entity_id}/relations — 查询参数**:
```
?type=WORKS_FOR,LOCATED_IN   # 关系类型过滤
&direction=outgoing          # outgoing | incoming | both
&sort=-confidence
&page=1&size=20
```

**响应**:
```json
{
  "data": [
    {
      "id": "rel_001",
      "type": "relation",
      "attributes": {
        "relation_type": "LED_BY",
        "source": {"id": "ent_apple", "name": "Apple Inc.", "type": "organization"},
        "target": {"id": "ent_timcook", "name": "Tim Cook", "type": "person"},
        "properties": {
          "role": "CEO",
          "start_date": "2011-08-24"
        },
        "confidence": 0.99,
        "statement_count": 45,
        "status": "active"
      }
    }
  ]
}
```

### 3.3 Statements（声明）

```
GET    /v1/statements                         # 声明列表（按审核状态）
GET    /v1/statements/{statement_id}          # 声明详情（含原文摘录）
POST   /v1/statements/{statement_id}/approve  # 审核通过
POST   /v1/statements/{statement_id}/reject   # 审核拒绝
```

**GET /v1/statements — 查询参数**:
```
?review_status=pending   # pending | approved | rejected
&statement_type=entity_extraction
&subject_id=ent_apple
&page=1&size=20
```

**POST /v1/statements/{statement_id}/approve**:
```json
{
  "comment": "Verified against official sources."
}
```

---

## 4. Graph API（图查询）

### 4.1 端点

```
GET    /v1/graph/entity/{entity_id}/neighbors  # 邻居节点
GET    /v1/graph/entity/{entity_id}/subgraph   # 子图
GET    /v1/graph/paths                          # 路径查询
GET    /v1/graph/trending                      # 趋势实体
POST   /v1/graph/query                         # 自定义 Cypher（管理员）
```

**GET /v1/graph/entity/{entity_id}/neighbors**:
```
?types=WORKS_FOR,LOCATED_IN   # 关系类型
&direction=outgoing           # outgoing | incoming | both
&depth=1                      # 邻居深度（1-3）
&limit=50
```

**GET /v1/graph/paths**:
```
?from=ent_apple
&to=ent_openai
&max_depth=3
&limit=10
```

**GET /v1/graph/trending**:
```
?window=24h                  # 时间窗口
&entity_type=person
&type=mentions               # mentions（文章提及）| relations（关系增加）
&limit=20
```

**POST /v1/graph/query** (管理员):
```json
{
  "cypher": "MATCH (p:Person)-[:WORKS_FOR]->(o:Organization {name: $org_name}) RETURN p.name, o.name",
  "params": {"org_name": "Apple Inc."},
  "timeout_ms": 5000
}
```

---

## 5. Search API

### 5.1 搜索端点

```
GET    /v1/search                              # 统一搜索
GET    /v1/search/autocomplete                 # 搜索自动补全
GET    /v1/search/suggestions                  # 搜索建议
```

**GET /v1/search**:
```
?q=AI protein folding
&mode=hybrid                  # fulltext | vector | hybrid
&language=en
&types=article,entity         # 搜索类型
&filters.category=Science     # 过滤器
&filters.date_from=2026-01-01
&filters.entity_type=person   # 仅实体搜索时
&sort=-score                  # -score（相关性）| -published_at（时间）
&page=1&size=20
&highlight=true               # 高亮
```

**响应**:
```json
{
  "data": [
    {
      "id": "art_abc123",
      "type": "article",
      "score": 0.92,
      "source": "hybrid",
      "highlights": {
        "title": ["<em>AI</em> Breakthrough in <em>Protein Folding</em>"],
        "content_clean": ["...revolutionary <em>AI</em> model for predicting <em>protein</em> structures..."]
      },
      "attributes": {
        "title": "AI Breakthrough in Protein Folding",
        "summary": "Researchers at DeepMind...",
        "published_at": "2026-08-01T12:00:00Z"
      }
    },
    {
      "id": "ent_deepmind",
      "type": "entity",
      "score": 0.88,
      "source": "vector",
      "attributes": {
        "canonical_name": "DeepMind",
        "entity_type": "organization",
        "description": "British AI research laboratory..."
      }
    }
  ],
  "facets": {
    "categories": [
      {"value": "AI", "count": 45},
      {"value": "Science", "count": 32}
    ],
    "entity_types": [
      {"value": "organization", "count": 15},
      {"value": "person", "count": 8}
    ]
  },
  "suggestions": ["AI protein prediction", "AI drug discovery"],
  "_meta": {
    "total": 87,
    "took_ms": 95
  }
}
```

**GET /v1/search/autocomplete**:
```
?q=Apple
&types=entity
&limit=5
```

**响应**:
```json
{
  "data": [
    {"text": "Apple Inc.", "type": "entity", "description": "Technology company"},
    {"text": "Apple TV+", "type": "entity", "description": "Streaming service"},
    {"text": "Apple Vision Pro", "type": "entity", "description": "Mixed reality headset"}
  ]
}
```

---

## 6. AI API

### 6.1 AI 任务

```
POST   /v1/ai/summarize                       # 生成摘要
POST   /v1/ai/translate                       # 文本翻译
POST   /v1/ai/extract/entities                # 实体提取
POST   /v1/ai/extract/relations               # 关系提取
POST   /v1/ai/chat                            # 知识问答
GET    /v1/ai/tasks/{task_id}                 # 任务状态查询
```

**POST /v1/ai/summarize**:
```json
{
  "article_id": "art_abc123",
  "style": "concise",
  "max_length": 200,
  "language": "zh",
  "model": "auto"
}
```

**响应** (202 Accepted — 异步):
```json
{
  "data": {
    "task_id": "task_xyz789",
    "status": "pending",
    "_links": {
      "status": "/v1/ai/tasks/task_xyz789"
    }
  }
}
```

**POST /v1/ai/translate**:
```json
{
  "text": "Artificial intelligence is transforming the world.",
  "source_language": "auto",
  "target_language": "zh",
  "article_id": "art_abc123"
}
```

**POST /v1/ai/chat**:
```json
{
  "question": "What is Apple's current CEO and when did they take the role?",
  "language": "en",
  "max_tokens": 500,
  "temperature": 0.3,
  "include_sources": true,
  "context_entity_ids": ["ent_apple"]
}
```

**响应**:
```json
{
  "data": {
    "answer": "Apple's current CEO is Tim Cook, who took the role on August 24, 2011, succeeding Steve Jobs.",
    "sources": [
      {
        "article_id": "art_123",
        "title": "Tim Cook's Decade at Apple",
        "url": "https://...",
        "snippet": "Tim Cook became CEO of Apple on August 24, 2011...",
        "published_at": "2021-08-24T00:00:00Z"
      }
    ],
    "entities_mentioned": [
      {"id": "ent_apple", "name": "Apple Inc."},
      {"id": "ent_timcook", "name": "Tim Cook"},
      {"id": "ent_stevejobs", "name": "Steve Jobs"}
    ],
    "model": "gpt-5",
    "tokens_used": 245
  }
}
```

---

## 7. User API

```
POST   /v1/users/register                     # 注册
POST   /v1/users/login                        # 登录
POST   /v1/users/refresh                      # 刷新 Token
GET    /v1/users/me                           # 当前用户信息
PUT    /v1/users/me/preferences               # 更新偏好
GET    /v1/users/me/collections               # 收藏列表
POST   /v1/users/me/collections               # 添加收藏
DELETE /v1/users/me/collections/{article_id}  # 取消收藏
GET    /v1/users/me/history                   # 浏览历史
```

---

## 8. System API

```
GET    /v1/health                             # 健康检查
GET    /v1/health/ready                       # 就绪检查
GET    /v1/plugins                            # 插件列表
POST   /v1/plugins                            # 安装插件
DELETE /v1/plugins/{plugin_id}               # 卸载插件
GET    /v1/stats                              # 系统统计（管理员）
```

**GET /v1/stats**:
```json
{
  "data": {
    "articles_total": 1520000,
    "articles_today": 12000,
    "entities_total": 8500000,
    "relations_total": 42000000,
    "statements_total": 120000000,
    "sources_active": 500,
    "users_total": 15000,
    "ai_tokens_used_today": 5000000,
    "ai_cost_today": {"amount": 125.50, "currency": "USD"}
  }
}
```

---

## 9. GraphQL API

### 9.1 端点

```
POST /v1/graphql
```

### 9.2 Schema（核心部分）

```graphql
type Query {
  # ── 实体查询 ──
  entity(id: ID!): Entity
  entities(
    query: String
    type: EntityType
    language: String
    limit: Int = 20
    offset: Int = 0
  ): EntityConnection!
  
  # ── 文章查询 ──
  article(id: ID!): Article
  articles(
    sourceId: ID
    language: String
    category: String
    publishedAfter: DateTime
    limit: Int = 20
    offset: Int = 0
  ): ArticleConnection!
  
  # ── 图查询 ──
  graphSubgraph(
    entityId: ID!
    depth: Int = 1
    relationTypes: [String]
  ): Subgraph!
  
  graphPaths(
    fromEntityId: ID!
    toEntityId: ID!
    maxDepth: Int = 3
  ): [Path!]!
  
  # ── 搜索 ──
  search(
    query: String!
    mode: SearchMode = hybrid
    types: [SearchType!] = [ARTICLE, ENTITY]
    language: String
    limit: Int = 20
    offset: Int = 0
  ): SearchResultConnection!
  
  # ── 趋势 ──
  trending(
    window: TrendingWindow = LAST_24H
    entityType: EntityType
    limit: Int = 20
  ): [TrendingEntity!]!
}

# ── 类型定义 ──

type Entity {
  id: ID!
  canonicalName: String!
  entityType: EntityType!
  names(language: String): [EntityName!]!
  aliases: [EntityAlias!]!
  description: String
  properties: [EntityProperty!]!
  status: EntityStatus!
  confidence: Float!
  sourceCount: Int!
  createdAt: DateTime!
  updatedAt: DateTime!
  
  # 关系（懒加载）
  relations(
    types: [String]
    direction: RelationDirection = OUTGOING
    limit: Int = 20
  ): RelationConnection!
  
  # 相关文章
  articles(
    limit: Int = 20
  ): ArticleConnection!
  
  # 子图
  subgraph(depth: Int = 1): Subgraph!
}

type Article {
  id: ID!
  title: String!
  url: String!
  summary: String
  language: String!
  contentClean: String
  publishedAt: DateTime!
  wordCount: Int!
  readingTimeMinutes: Int!
  categories: [String!]!
  tags: [String!]!
  
  source: Source!
  authors: [String!]!
  entities(limit: Int = 50): [Entity!]!
  relatedArticles(limit: Int = 10): [Article!]!
}

type Relation {
  id: ID!
  relationType: String!
  source: Entity!
  target: Entity!
  confidence: Float!
  properties: JSON
  validFrom: DateTime
  validUntil: DateTime
}

type Statement {
  id: ID!
  statementType: StatementType!
  predicate: String!
  objectValue: String!
  confidence: Float!
  sourceSnippet: String
  reviewStatus: ReviewStatus!
}

type Subgraph {
  center: Entity!
  nodes: [Entity!]!
  edges: [Relation!]!
}

type Path {
  length: Int!
  nodes: [Entity!]!
  edges: [Relation!]!
}

type TrendingEntity {
  entity: Entity!
  mentionCount: Int!
  trend: Float!  # 增长率
}

# ── 示例查询 ──
# query {
#   entity(id: "ent_apple") {
#     canonicalName
#     entityType
#     relations(types: ["LED_BY", "ACQUIRED"], direction: OUTGOING) {
#       edges {
#         relationType
#         target {
#           canonicalName
#           entityType
#         }
#       }
#     }
#     articles(limit: 5) {
#       edges {
#         title
#         publishedAt
#       }
#     }
#   }
# }
```

---

## 10. Webhook API

用于第三方系统集成：

```
POST   /v1/webhooks                           # 注册 Webhook
GET    /v1/webhooks                           # 列出 Webhook
DELETE /v1/webhooks/{webhook_id}             # 删除 Webhook
```

**Webhook 注册请求**:
```json
{
  "url": "https://my-app.com/webhook/athena",
  "events": ["ArticlePublished", "EntityCreated"],
  "secret": "whsec_xxx",
  "filters": {
    "language": ["en", "zh"],
    "category": ["AI", "Technology"]
  }
}
```

---

## 11. 限流策略

| 端点组 | 匿名 | 注册用户 | Pro | Enterprise |
|--------|------|---------|-----|------------|
| 读操作 (GET) | 100/min | 1000/min | 5000/min | 20000/min |
| 写操作 (POST/PUT/DELETE) | 10/min | 100/min | 500/min | 2000/min |
| AI 操作 (POST /ai/*) | 0 | 10/min | 50/min | 200/min |
| 图查询 (POST /graph/query) | 0 | 10/min | 50/min | 200/min |
| Webhook | - | 5 | 20 | 100 |

限流响应头:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1691026800
Retry-After: 30
```

---

*本文档为 API 契约的权威定义。Phase 1 实现时通过 OpenAPI 3.1 规范文件具体化。*
