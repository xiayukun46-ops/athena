# Pipeline Diagrams

> Knowledge Pipeline + Event Pipeline

---

## 4. Knowledge Pipeline（知识管道）

从原始内容到结构化知识的端到端流程。

```mermaid
flowchart TD
    subgraph Sources["Content Sources"]
        RSS["RSS Feeds"]
        API["News APIs"]
        SCRAPER["Web Scrapers"]
    end

    subgraph Collector["Collector Service"]
        FETCH["Fetch Stage"]
        PARSE["Parse Stage"]
        CLEAN["Clean Stage"]
        DEDUP["Dedup Stage"]
        PUB["Publish Stage"]
    end

    subgraph Storage["PostgreSQL (Source of Truth)"]
        ARTICLES["content.articles"]
        SOURCES["content.sources"]
    end

    subgraph AI_Pipeline["AI Extraction Pipeline"]
        NER["Entity Extraction (NER)"]
        LINK["Entity Linking"]
        RE["Relation Extraction (RE)"]
        AGG["Statement Aggregation"]
    end

    subgraph Knowledge["Knowledge Store"]
        ENTITIES["knowledge.entities"]
        RELATIONS["knowledge.relations"]
        STATEMENTS["knowledge.statements"]
    end

    subgraph Read_Views["Read-Optimized Views"]
        ES["Elasticsearch\n(Search Index)"]
        NEO4J["Neo4j\n(Graph View)"]
        VEC["pgvector\n(Vector Index)"]
    end

    RSS --> FETCH
    API --> FETCH
    SCRAPER --> FETCH
    FETCH --> PARSE
    PARSE --> CLEAN
    CLEAN --> DEDUP
    DEDUP -->|New| PUB
    DEDUP -->|Duplicate| SKIP["Skip + Log"]
    PUB --> ARTICLES
    PUB -->|ArticleFetched Event| NER
    
    NER --> STATEMENTS
    NER --> LINK
    LINK --> ENTITIES
    RE --> STATEMENTS
    RE --> RELATIONS
    AGG --> ENTITIES
    AGG --> RELATIONS
    
    ENTITIES -->|Event| ES
    ENTITIES -->|Event| NEO4J
    ARTICLES -->|Event| ES
    ARTICLES -->|Embedding| VEC

    style SKIP fill:#f99,stroke:#f00
```

**解释**: 内容从 Source 进入 Collector 的五段管道（Fetch→Parse→Clean→Dedup→Publish）。重复内容被拦截（去重率目标 ≥ 80%）。发布后触发 ArticleFetched 事件，启动 AI 管道（NER→Linking→RE→Aggregation）。知识写入 PG 后，通过事件同步到三个读优化视图（ES/Neo4j/pgvector）。

---

## 5. Event Pipeline（事件管道）

领域事件在限界上下文之间的流动。

```mermaid
flowchart LR
    subgraph Content["Content Context"]
        AF["ArticleFetched"]
        AP["ArticlePublished"]
    end

    subgraph Knowledge["Knowledge Context"]
        EC["EntityCreated"]
        EU["EntityUpdated"]
        EM["EntityMerged"]
        RC["RelationCreated"]
        SA["StatementApproved"]
    end

    subgraph AI["AI Context"]
        TS["TaskStarted"]
        TC["TaskCompleted"]
        TF["TaskFailed"]
    end

    subgraph Search["Search Context"]
        SP["SearchPerformed"]
        IR["IndexRebuilt"]
    end

    subgraph Bus["Redis Streams"]
        S1["Stream: content-events"]
        S2["Stream: knowledge-events"]
        S3["Stream: ai-events"]
    end

    subgraph Consumers["Event Consumers"]
        W1["AI Extraction Worker"]
        W2["Graph Sync Worker"]
        W3["Search Indexer"]
        W4["Notification Worker"]
    end

    AF --> S1
    AP --> S1
    EC --> S2
    EU --> S2
    EM --> S2
    RC --> S2
    SA --> S2
    TS --> S3
    TC --> S3
    TF --> S3

    S1 --> W1
    S1 --> W3
    S2 --> W2
    S2 --> W3
    S3 --> W4
    S1 --> W4

    style Bus fill:#e3f2fd
```

**解释**: 事件按上下文分组发布到独立的 Redis Stream。消费者按需订阅：AI Extraction Worker 消费 Content 事件触发实体提取；Graph Sync Worker 消费 Knowledge 事件同步 Neo4j；Search Indexer 消费 Content + Knowledge 事件更新 ES；Notification Worker 消费多类事件推送通知。Outbox Pattern 保证 PG 写入与事件发布的原子性。
