# C4 Architecture Diagrams

> Athena Knowledge Platform — C4 Model
> Level 1-3: System Context → Container → Component

---

## 1. System Context（系统上下文）

Athena 在全球知识生态系统中的位置。

```mermaid
C4Context
    title System Context — Athena Knowledge Platform

    Person(user, "Knowledge Worker", "研究者、记者、学生、开发者")
    Person(curator, "Curator", "知识审核者")
    
    System(athena, "Athena Platform", "AI-driven Global Knowledge")
    
    System_Ext(news, "News Sources", "RSS Feeds, News APIs")
    System_Ext(academic, "Academic Sources", "arXiv, PubMed, OpenAlex")
    System_Ext(gov, "Government Sources", "Public Data, Regulations")
    System_Ext(social, "Social Media", "Twitter, Reddit")
    
    System_Ext(llm, "LLM Providers", "OpenAI, Anthropic, Ollama")
    System_Ext(third, "Third-party Apps", "Slack, Notion, Custom Apps")
    
    Rel(user, athena, "Search, Ask, Browse Knowledge")
    Rel(curator, athena, "Review Statements, Merge Entities")
    Rel(news, athena, "Push/Pull Content")
    Rel(academic, athena, "Push/Pull Content")
    Rel(gov, athena, "Push/Pull Content")
    Rel(social, athena, "Push/Pull Content")
    Rel(athena, llm, "AI API Calls")
    Rel(third, athena, "REST/GraphQL API")
    
    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

**解释**: Athena 处于内容源（上游）和知识消费者（下游）之间。外部系统分为三类：内容提供者（新闻、学术、政府、社交）、AI 服务提供者（LLM）、和消费者（终端用户 + 第三方应用）。Athena 不直接面向大众消费者——第三方应用是主要的规模化分发渠道。

---

## 2. Container Diagram（容器图）

Athena 内部的主要容器和它们之间的交互。

```mermaid
C4Container
    title Container — Athena Platform Internal

    Person(user, "User", "Knowledge Worker")
    
    System_Boundary(athena, "Athena Platform") {
        Container(web, "Web Application", "Next.js", "User-facing Web UI")
        Container(api, "API Gateway", "Kong", "Auth, Rate Limit, Routing")
        Container(app, "Application Server", "Python FastAPI", "Core Business Logic")
        Container(collector, "Collector Service", "Python", "Content Ingestion")
        Container(worker, "Background Workers", "Python", "AI Tasks, Graph Sync")
        
        ContainerDb(pg, "PostgreSQL", "PostgreSQL 16 + pgvector", "Source of Truth")
        ContainerDb(neo4j, "Neo4j", "Graph Database", "Knowledge Graph Query")
        ContainerDb(es, "Elasticsearch", "Search Engine", "Full-text Index")
        ContainerDb(redis, "Redis", "Cache + Message Bus", "Redis Streams")
        ContainerDb(minio, "MinIO", "Object Storage", "Raw Content, Assets")
    }
    
    System_Ext(llm, "LLM Providers", "OpenAI, Anthropic, Ollama")
    
    Rel(user, web, "HTTPS")
    Rel(web, api, "HTTPS")
    Rel(api, app, "Proxy")
    Rel(app, pg, "Read/Write")
    Rel(app, redis, "Cache + Publish Events")
    Rel(collector, pg, "Write Articles")
    Rel(collector, redis, "Publish ArticleFetched")
    Rel(worker, redis, "Consume Events")
    Rel(worker, llm, "AI API Calls")
    Rel(worker, neo4j, "Graph Sync")
    Rel(worker, es, "Index Content")
    Rel(app, neo4j, "Read Queries")
    Rel(app, es, "Read Queries")
    Rel(collector, minio, "Store Raw HTML")
    
    UpdateLayoutConfig($c4ShapeInRow="4", $c4BoundaryInRow="1")
```

**解释**: 核心容器分为三层：前端入口（Web → API Gateway）、业务处理（Application Server + Collector + Workers）、数据存储（PG + Neo4j + ES + Redis + MinIO）。数据写入只走 PostgreSQL（Source of Truth），Neo4j 和 ES 通过 Workers 消费事件异步同步。

---

## 3. Component Diagram（组件图）

Application Server 内部的组件分解。

```mermaid
C4Container
    title Component — Application Server (Python FastAPI)

    Container_Boundary(app, "Application Server") {
        Component(content_api, "Content API", "FastAPI Router", "CRUD for Sources & Articles")
        Component(knowledge_api, "Knowledge API", "FastAPI Router", "Entities, Relations, Statements")
        Component(search_api, "Search API", "FastAPI Router", "Fulltext + Vector Search")
        Component(ai_api, "AI API", "FastAPI Router", "Summarize, Translate, Chat")
        Component(graph_api, "Graph API", "FastAPI Router", "Graph Traversal")
        Component(user_api, "User API", "FastAPI Router", "Auth, Preferences")
        
        Component(event_bus, "Event Bus", "IEventBus", "Publish/Subscribe Domain Events")
        Component(plugin_mgr, "Plugin Manager", "PluginRegistry", "Load/Manage Plugins")
        
        Component(content_domain, "Content Domain", "DDD", "Source, Article Aggregates")
        Component(knowledge_domain, "Knowledge Domain", "DDD", "Entity, Relation, Statement")
        Component(search_domain, "Search Domain", "DDD", "SearchIndex Aggregate")
        Component(ai_domain, "AI Domain", "DDD", "CompletionTask Aggregate")
        
        Component(shared, "Shared Kernel", "Value Objects", "ID Types, Language, Confidence")
    }
    
    ContainerDb(pg, "PostgreSQL", "Source of Truth")
    ContainerDb(redis, "Redis", "Cache + Events")
    
    Rel(content_api, content_domain, "Uses")
    Rel(knowledge_api, knowledge_domain, "Uses")
    Rel(search_api, search_domain, "Uses")
    Rel(ai_api, ai_domain, "Uses")
    Rel(graph_api, knowledge_domain, "Uses")
    
    Rel(content_domain, event_bus, "Publishes Events")
    Rel(knowledge_domain, event_bus, "Publishes Events")
    Rel(ai_domain, event_bus, "Publishes Events")
    
    Rel(content_api, plugin_mgr, "Gets Source Plugins")
    Rel(knowledge_api, plugin_mgr, "Gets AI Plugins")
    Rel(ai_api, plugin_mgr, "Gets AI Plugins")
    
    Rel(content_domain, shared, "Uses")
    Rel(knowledge_domain, shared, "Uses")
    Rel(search_domain, shared, "Uses")
    Rel(ai_domain, shared, "Uses")
    
    Rel(content_domain, pg, "Read/Write")
    Rel(knowledge_domain, pg, "Read/Write")
    Rel(search_domain, pg, "Read")
    Rel(event_bus, redis, "Streams")
    
    UpdateLayoutConfig($c4ShapeInRow="4", $c4BoundaryInRow="1")
```

**解释**: Application Server 按 Bounded Context 组织为 6 个 API 模块 + 4 个领域模块。Shared Kernel 被所有领域模块依赖。Event Bus 是唯一的跨模块通信通道。Plugin Manager 为 API 层提供插件实例。所有写入走 PostgreSQL，事件通过 Redis Streams 发布。

---

*C4 Model (Level 1-3) — 完整架构层级。Level 4 (Code) 在 Phase 1 实现时补充。*
