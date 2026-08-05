# Plugin & Agent Architecture

---

## 8. Plugin Architecture（插件架构）

```mermaid
graph TD
    subgraph Core["Athena Core"]
        PM["Plugin Manager"]
        DI["DI Container"]
        EB["Event Bus"]
    end

    subgraph PluginTypes["Plugin Types"]
        direction LR
        SP["Source Plugins\n(ISourcePlugin)"]
        PP["Processor Plugins\n(IProcessorPlugin)"]
        STP["Storage Plugins\n(IStoragePlugin)"]
        AIP["AI Provider Plugins\n(IAIProviderPlugin)"]
        UIP["UI Plugins\n(IUIPlugin)"]
    end

    subgraph Instances["Plugin Instances"]
        RSS["RSS Source"]
        API_SRC["API Source"]
        SCRAPE["Scraper Source"]
        HTML_CLEAN["HTML Cleaner"]
        LANG_DETECT["Language Detector"]
        PG_STORE["PostgreSQL Store"]
        ES_STORE["Elasticsearch Store"]
        OAI["OpenAI Provider"]
        ANTHRO["Anthropic Provider"]
        GRAPH_VIZ["Graph Visualization"]
    end

    PM -->|Registers| SP
    PM -->|Registers| PP
    PM -->|Registers| STP
    PM -->|Registers| AIP
    PM -->|Registers| UIP

    SP --> RSS
    SP --> API_SRC
    SP --> SCRAPE
    PP --> HTML_CLEAN
    PP --> LANG_DETECT
    STP --> PG_STORE
    STP --> ES_STORE
    AIP --> OAI
    AIP --> ANTHRO
    UIP --> GRAPH_VIZ

    DI -->|Injects| RSS
    DI -->|Injects| OAI
    EB -->|Events| RSS

    style Core fill:#e8eaf6
    style PluginTypes fill:#fff9c4
    style Instances fill:#e8f5e9
```

**解释**: 五类插件接口定义了扩展契约。Plugin Manager 负责注册和生命周期。DI Container 注入依赖（如 HttpClient 注入 RSS Source Plugin）。Event Bus 用于插件间通信。具体实现（RSS Source、OpenAI Provider 等）是接口的实例。新能力只需实现对应接口 + 注册。

---

## 9. Agent Architecture（Agent 运行时）

```mermaid
graph TD
    subgraph AgentRuntime["Agent Runtime (Sandboxed)"]
        PLANNER["Planner\n(任务分解)"]
        EXECUTOR["Executor\n(步骤执行)"]
        REFLECTOR["Reflector\n(结果评估)"]
        
        WM["Working Memory\n(当前任务上下文)"]
        EM["Episodic Memory\n(历史任务经验)"]
    end

    subgraph Tools["Tool Registry"]
        T1["search_knowledge_graph"]
        T2["query_entity_detail"]
        T3["create_entity"]
        T4["merge_entities"]
        T5["flag_for_review"]
        T6["send_notification"]
    end

    subgraph Permissions["Permission Boundary"]
        SCOPE["Scope: read:entities, write:statements"]
        APPROVAL["Requires Approval: merge_entities"]
    end

    subgraph External["Platform Services"]
        API["Athena API"]
        LLM["LLM Provider"]
        AUDIT["Audit Log"]
    end

    PLANNER --> EXECUTOR
    EXECUTOR --> REFLECTOR
    PLANNER <--> WM
    REFLECTOR --> EM
    EXECUTOR --> Tools
    Tools --> PERMISSIONS
    PERMISSIONS --> API
    EXECUTOR --> LLM
    EXECUTOR --> AUDIT

    style AgentRuntime fill:#e8eaf6
    style Permissions fill:#ffcdd2
```

**解释**: Agent 在沙箱中运行（Docker 容器，CPU/Mem/Timeout 限制）。Planner 分解目标→Executor 调用工具→Reflector 评估结果，循环直到完成。Working Memory 保存当前任务状态，Episodic Memory 保存历史经验（"上次处理类似文章时..."）。所有工具调用经过权限检查（Scope + Approval）。全部操作写入审计日志。
