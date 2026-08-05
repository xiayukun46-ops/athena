# Data Flow & Sequence Diagrams

---

## 10. Data Flow（数据流全景）

```mermaid
flowchart LR
    subgraph Input["Data Sources"]
        RSS_F["RSS"]
        API_F["API"]
        SCRAPE_F["Scraper"]
    end

    subgraph Ingestion["Content Ingestion"]
        COL["Collector"]
        CLEAN["Cleaner"]
    end

    subgraph Core["PostgreSQL — Source of Truth"]
        ART["articles"]
        SRC["sources"]
        ENT["entities"]
        REL["relations"]
        STMT["statements"]
        EVT["event_log"]
    end

    subgraph AI_Pipe["AI Pipeline"]
        EXTRACT["NER + RE\n(Background Worker)"]
        LINK["Entity Linking"]
    end

    subgraph Sync["Event-Driven Sync"]
        SYNC_G["Graph Sync Worker"]
        SYNC_S["Search Indexer"]
    end

    subgraph Read["Read-Optimized Views"]
        NEO["Neo4j\nGraph Queries"]
        ES["Elasticsearch\nFulltext Search"]
        VEC["pgvector\nVector Search"]
    end

    subgraph API_Layer["API Layer"]
        REST["REST API"]
        GQL["GraphQL"]
    end

    subgraph Clients["Clients"]
        WEB["Web App"]
        MOBILE["Mobile"]
        THIRD["3rd Party"]
    end

    RSS_F --> COL
    API_F --> COL
    SCRAPE_F --> COL
    COL --> CLEAN
    CLEAN --> ART
    CLEAN --> SRC
    ART -->|Event| EVT
    EVT --> EXTRACT
    EXTRACT --> STMT
    EXTRACT --> LINK
    LINK --> ENT
    LINK --> REL
    ENT -->|Event| EVT
    REL -->|Event| EVT
    EVT --> SYNC_G
    EVT --> SYNC_S
    SYNC_G --> NEO
    SYNC_S --> ES
    ART -->|Embedding| VEC
    ENT -->|Embedding| VEC
    
    REST --> ART
    REST --> ENT
    REST --> REL
    REST --> ES
    GQL --> NEO
    WEB --> REST
    MOBILE --> REST
    THIRD --> REST
    THIRD --> GQL

    style Core fill:#c8e6c9
    style EVT fill:#ffcc80
    style Read fill:#e3f2fd
```

**解释**: 数据从左到右流动。所有写入集中在 PostgreSQL（绿色），通过 `event_log` 表（橙色）触发异步处理。AI Pipeline 和 Sync Workers 消费事件。读优化视图（蓝色）由事件驱动更新。API 层统一对外暴露。REST 用于 CRUD + 搜索，GraphQL 用于灵活图查询。

---

## 11. Database ER Diagram（参考）

完整 PostgreSQL ER 图见: [docs/database/er-diagram.md](../../database/er-diagram.md)

核心表关系速览：

```mermaid
erDiagram
    content_sources ||--o{ content_articles : "provides"
    content_articles ||--o{ knowledge_statements : "extracts"
    knowledge_entities ||--o{ knowledge_entity_names : "named"
    knowledge_entities ||--o{ knowledge_entity_properties : "described"
    knowledge_entities ||--o{ knowledge_relations : "source"
    knowledge_entities ||--o{ knowledge_relations : "target"
    knowledge_statements ||--o{ knowledge_entity_properties : "supports"
    knowledge_relations ||--o{ knowledge_relation_statements : "supported"
    account_users ||--o{ knowledge_statements : "reviews"
    
    content_sources {
        UUID id PK
        VARCHAR name
        VARCHAR source_type
        VARCHAR status
    }
    content_articles {
        UUID id PK
        UUID source_id FK
        VARCHAR url_hash UK
        TEXT title
        VARCHAR status
    }
    knowledge_entities {
        UUID id PK
        VARCHAR canonical_name
        VARCHAR entity_type
        VARCHAR status
    }
    knowledge_relations {
        UUID id PK
        UUID source_entity_id FK
        UUID target_entity_id FK
        VARCHAR relation_type
    }
    knowledge_statements {
        UUID id PK
        UUID subject_id
        VARCHAR review_status
        UUID source_article_id FK
    }
```

**解释**: 4 个 Schema（content, knowledge, account, system）共 13 张表。核心链路：`sources → articles → statements → entity_properties + relations`。每张表包含标准字段（id, created_at, updated_at, deleted_at, version）。

---

## 12. Sequence Diagram（关键流程时序）

**场景: 用户搜索并查看知识**

```mermaid
sequenceDiagram
    actor User
    participant Web as Web App
    participant API as API Gateway
    participant Search as Search Service
    participant ES as Elasticsearch
    participant VEC as pgvector
    participant Knowledge as Knowledge Service
    participant PG as PostgreSQL
    participant NEO as Neo4j

    User->>Web: Search "AI protein folding"
    Web->>API: GET /v1/search?q=AI+protein&mode=hybrid
    API->>Search: Forward search request
    Search->>ES: Fulltext query
    Search->>VEC: Vector similarity
    ES-->>Search: Fulltext results
    VEC-->>Search: Vector results
    Search->>Search: RRF fusion
    Search-->>API: Ranked results + highlights
    API-->>Web: SearchResponse
    
    User->>Web: Click entity "DeepMind"
    Web->>API: GET /v1/entities/ent_dm
    API->>Knowledge: Get entity detail
    Knowledge->>PG: SELECT entity + properties
    PG-->>Knowledge: Entity data
    Knowledge-->>API: EntityDetail
    
    User->>Web: View entity graph
    Web->>API: GET /v1/graph/entity/ent_dm/neighbors
    API->>NEO: Cypher query
    NEO-->>API: Neighbor nodes + edges
    API-->>Web: GraphData
    
    User->>Web: Click source article
    Web->>API: GET /v1/articles/art_001
    API->>PG: SELECT article
    PG-->>API: Article with snippet
    API-->>Web: ArticleDetail with source citation
```

**解释**: 单一搜索会话涉及 5 个数据存储的协同。搜索阶段使用 ES + pgvector 的混合检索 + RRF 融合。实体详情走 PG。图查询走 Neo4j。溯源点击回到 PG 的 articles 表。全程用户感知到的延迟由最慢的环节决定（向量搜索 ~50ms + ES ~30ms + RRF ~5ms ≈ < 100ms P50）。
