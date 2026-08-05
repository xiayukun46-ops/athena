# 08 — Data Model

> Athena 的数据模型。定义数据如何存储、如何关联、如何查询。

**详细 ER 图见**: [database/er-diagram.md](database/er-diagram.md) — PostgreSQL 完整 Schema  
**图模型见**: [domain/graph-model.md](domain/graph-model.md) — Neo4j 图模型

---

## 存储引擎选择

### 为什么不是单一数据库

**替代方案**: 全部用 PostgreSQL（包括图查询和全文搜索）。

不选理由：
- PostgreSQL 的递归 CTE 做路径查询性能差（Neo4j 原生图遍历快 10-100x）
- PostgreSQL 的全文搜索不支持专业分词（Elasticsearch 有 CJK 分析器）
- 每种数据类型用最合适的引擎，比一个引擎硬撑所有类型更好

### 分工原则

| 引擎 | 角色 | 典型查询 |
|------|------|----------|
| PostgreSQL | Source of Truth | CRUD, 聚合统计, JOIN |
| Neo4j | 图查询 | 路径遍历 (Person-[WORKS_FOR]->Org), 子图, 中心性 |
| Elasticsearch | 全文搜索 | "AI 蛋白质折叠", 高亮, 分面 |
| pgvector (PG扩展) | 向量搜索 | 语义相似度 |
| Redis | 缓存 + 消息 | Key-Value, Streams |
| MinIO | 对象存储 | 原始 HTML, 图片 |

---

## PostgreSQL Schema（核心表）

### 为什么用 EAV 模式存储实体属性

**问题**: 8 种实体类型有 50+ 种不同属性。传统的"每种实体一张表"导致表爆炸。

**方案**: knowledge_entity_properties 表使用 EAV (Entity-Attribute-Value):
```
entity_id | key            | value      | value_type
ent_001   | birth_date     | 1964-01-07 | date
ent_001   | nationality    | American   | string
ent_002   | headquarters   | Cupertino  | string
ent_002   | founded_date   | 1976-04-01 | date
```

**替代方案**: 
1. 每种实体类型一张表 (persons, organizations, locations...)。**不选理由**: 实体类型可能增加，每次加类型需新建表。
2. JSONB 存所有属性。**不选理由**: 不能按属性值建索引和查询。

**EAV 的代价**: 查询性能。缓解方案——Phase 2 对高频属性建立物化视图。

### 核心表关系

```
content_sources (1) ──→ (N) content_articles
content_articles (1) ──→ (N) knowledge_statements
knowledge_statements (1) ──→ (N) knowledge_entity_properties
knowledge_entities (1) ──→ (N) knowledge_entity_names
knowledge_entities (1) ──→ (N) knowledge_relations (source)
knowledge_entities (1) ──→ (N) knowledge_relations (target)
```

完整 13 张表的 Schema 见 [database/er-diagram.md](database/er-diagram.md)。

---

## Neo4j 图模型

### 为什么 PG 不够

以下查询在 PG 中需要递归 CTE + 多表 JOIN，在 Neo4j 中是原生图遍历：

```cypher
-- 查询 "Elon Musk" 和 "Sam Altman" 之间的最短关系路径
MATCH path = shortestPath(
  (p1:Person {name: "Elon Musk"})-[*..5]-(p2:Person {name: "Sam Altman"})
)
RETURN path
```

### 节点和边

```
节点:
  (:Entity) ─── (:Person)
  (:Entity) ─── (:Organization)
  (:Entity) ─── (:Location)
  (:Entity) ─── (:Event)
  (:Content) ─── (:Article)
  
边（20+ 类型）:
  [:WORKS_FOR {role, start_date, end_date}]
  [:LOCATED_IN]
  [:PART_OF]
  [:MENTIONS]     -- Article → Entity
  [:PARTICIPATED_IN] -- Entity → Event
```

### PG ↔ Neo4j 同步

- PG 写入 → EntityCreated Event → Redis Streams → Graph Sync Worker → Neo4j
- 延迟: < 1s (正常), < 5s (P99)
- 故障恢复: Event Store 重放

---

## 索引策略

| 表 | 索引 | 用途 |
|----|------|------|
| content_articles | UNIQUE(url_hash) | URL 去重 |
| content_articles | (published_at DESC) | 按时间排序 |
| knowledge_entities | (canonical_name) | 实体名称搜索 |
| knowledge_entities | (entity_type) | 按类型筛选 |
| knowledge_relations | UNIQUE(source, target, type) | 三元组去重 |
| knowledge_statements | (review_status) WHERE pending | 待审核列表 |
| content_article_embeddings | ivfflat(embedding) | 向量相似度搜索 |

---

## 相关文档

- [04-domain-model.md](04-domain-model.md) — 数据模型对应的领域
- [06-knowledge-engine.md](06-knowledge-engine.md) — 知识如何写入
- [07-architecture.md](07-architecture.md) — 数据在架构中的位置
- [12-database-standard.md](12-database-standard.md) — 数据库开发规范
- [database/er-diagram.md](database/er-diagram.md) — 完整 DDL
