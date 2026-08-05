# Deployment & Infrastructure Diagrams

---

## 6. Deployment Diagram（部署拓扑）

```mermaid
graph TD
    subgraph DNS["Global DNS (Geo-routed)"]
        LB["Load Balancer"]
    end

    subgraph Region_Asia["Region: Asia (Primary)"]
        subgraph K8S_ASIA["Kubernetes Cluster"]
            GW1["API Gateway (Kong)"]
            APP1["App Server x3"]
            COL1["Collector x2"]
            WORK1["Workers x4"]
        end
        subgraph DATA_ASIA["Data Layer"]
            PG1["PostgreSQL (Primary)"]
            NEO1["Neo4j (Cluster)"]
            ES1["Elasticsearch (Cluster)"]
            REDIS1["Redis (Cluster)"]
            MINIO1["MinIO (Cluster)"]
        end
    end

    subgraph Region_EU["Region: EU (Replica)"]
        subgraph K8S_EU["Kubernetes Cluster"]
            GW2["API Gateway (Kong)"]
            APP2["App Server x2"]
            WORK2["Workers x2"]
        end
        subgraph DATA_EU["Data Layer"]
            PG2["PostgreSQL (Read Replica)"]
            NEO2["Neo4j (Read Replica)"]
            ES2["Elasticsearch (Replica)"]
            REDIS2["Redis (Replica)"]
        end
    end

    subgraph External["External Services"]
        LLM["LLM Providers\n(OpenAI, Anthropic)"]
        CDN["CDN\n(Static Assets)"]
        MON["Monitoring\n(Prometheus + Grafana)"]
    end

    LB --> GW1
    LB --> GW2
    GW1 --> APP1
    GW1 --> COL1
    GW2 --> APP2
    APP1 --> PG1
    APP1 --> REDIS1
    APP2 --> PG2
    COL1 --> MINIO1
    WORK1 --> LLM
    WORK1 --> NEO1
    WORK1 --> ES1
    PG1 -.->|Replication| PG2
    NEO1 -.->|Replication| NEO2
    ES1 -.->|Replication| ES2
    APP1 --> MON
    APP2 --> CDN

    style PG1 fill:#c8e6c9
    style PG2 fill:#c8e6c9
    style LLM fill:#ffcc80
```

**解释**: Phase 4+ 的生产拓扑。双区域部署（Asia Primary + EU Replica），数据层主从复制。Kubernetes 管理容器化服务。LLM 调用从 Worker 层发起（不经过 API Gateway）。监控系统独立部署。Phase 1-3 的 Modular Monolith 使用单区域 Docker Compose，此图为 Phase 4+ 目标态。

---

## 7. Domain Diagram（限界上下文关系）

```mermaid
graph TD
    subgraph Core["Core Domains"]
        CONTENT["Content Context\n(内容管理)"]
        KNOWLEDGE["Knowledge Context\n(知识图谱)"]
        SEARCH["Search Context\n(搜索)"]
        AI["AI Context\n(AI 编排)"]
    end

    subgraph Supporting["Supporting Domains"]
        USER["User Context\n(用户)"]
        NOTIF["Notification\n(通知)"]
    end

    subgraph Generic["Generic Domains"]
        PLUGIN["Plugin Context\n(插件管理)"]
    end

    subgraph Shared["Shared Kernel"]
        SK["EntityId, Language\nConfidence, DomainEvent"]
    end

    CONTENT -->|"ArticleFetched"| KNOWLEDGE
    CONTENT -->|"ArticleFetched"| AI
    CONTENT -->|"ArticleFetched"| SEARCH
    KNOWLEDGE -->|"EntityCreated, RelationCreated"| SEARCH
    AI -->|"TaskCompleted"| KNOWLEDGE
    AI -->|"TaskCompleted"| CONTENT
    USER -->|"UserEvent"| NOTIF
    CONTENT -->|"ArticlePublished"| NOTIF
    KNOWLEDGE -->|"TrendDetected"| NOTIF
    PLUGIN -.->|"Provides Extensions"| CONTENT
    PLUGIN -.->|"Provides Extensions"| AI
    PLUGIN -.->|"Provides Extensions"| SEARCH
    
    CONTENT -.-> SK
    KNOWLEDGE -.-> SK
    SEARCH -.-> SK
    AI -.-> SK
    USER -.-> SK
    PLUGIN -.-> SK

    style Core fill:#e3f2fd
    style Supporting fill:#f3e5f5
    style Generic fill:#fff3e0
```

**解释**: 六个 Bounded Context 分为三层：Core（Content/Knowledge/Search/AI）是业务核心，Supporting（User/Notification）辅助核心业务，Generic（Plugin）提供横向能力。实线箭头 = 领域事件流（异步解耦）。虚线 = 依赖 Shared Kernel。跨 Core 上下文只有事件通信，无直接 API 调用。
