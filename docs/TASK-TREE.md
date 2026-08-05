# Blueprint Task Tree

> Athena Knowledge Platform 完整任务分解树。
> 每个叶子节点是一个可独立分配和追踪的任务。
> 状态: [ ] 待开始 / [~] 进行中 / [x] 已完成
> 更新日期: 2026-08-05

---

## Blueprint

```
Blueprint
├── Vision         [████████░░] 80%
├── Product        [██████░░░░] 60%
├── Architecture   [████████░░] 80%
├── Domain         [████████░░] 80%
├── Event          [████████░░] 80%
├── Knowledge      [████████░░] 80%
├── Search         [██████░░░░] 60%
├── AI             [██████░░░░] 60%
├── Plugin         [████████░░] 80%
├── SDK            [░░░░░░░░░░]  0%
└── Infrastructure [██░░░░░░░░] 20%
```

---

## 1. Vision（愿景与策略）

```
Vision
├── [x] 00-vision.md — 企业级产品愿景文档
├── [x] 01-product-strategy.md — 企业级产品策略文档
├── [x] 02-constitution.md — 项目宪法完整法律框架
├── [x] 03-glossary.md — 统一领域语言术语表
├── [x] 15-roadmap.md — 分阶段路线图
├── [ ] MASTER.md — 开发入口引导（已有初版）
├── [ ] README.md — 项目介绍（已有初版，需与蓝图对齐）
└── [ ] CONTRIBUTING.md — 贡献指南（已有初版，需与蓝图对齐）
```

---

## 2. Product（产品设计）

```
Product
├── Product Strategy
│   ├── [x] 01-product-strategy.md — 产品策略主文档
│   ├── [x] Competitive analysis — 竞争分析矩阵 + 6 家竞品深度对比
│   ├── [x] Go-to-Market strategy — 三阶段 GTM 计划
│   ├── [x] Business model — 六层收入模型
│   ├── [x] User personas — 三层用户 + 三个 Persona
│   ├── [x] Success metrics — 30+ KPI 定义
│   └── [ ] Pricing page design — Phase 4 需要
│
├── User Experience (Phase 4)
│   ├── [ ] UX Research plan — 用户研究方法论
│   ├── [ ] Information architecture — Web App 信息架构
│   ├── [ ] Design system — 组件库和设计语言
│   ├── [ ] Wireframes — 关键页面线框图
│   ├── [ ] Prototype — 可交互原型
│   └── [ ] Usability testing plan — 可用性测试方案
│
├── Feature Specification (Phase 2-4)
│   ├── [ ] Knowledge Graph browser — 知识图谱浏览功能规格
│   ├── [ ] Q&A interface — 问答界面功能规格
│   ├── [ ] Entity detail page — 实体详情页功能规格
│   ├── [ ] Statement review tool — 声明审核工具功能规格
│   ├── [ ] Search experience — 搜索体验功能规格
│   └── [ ] Personalization engine — 个性化推荐引擎功能规格
│
└── Product Analytics
    ├── [ ] Analytics event schema — 埋点事件定义
    ├── [ ] Dashboard design — 产品分析仪表盘
    └── [ ] A/B testing framework — A/B 测试框架设计
```

---

## 3. Architecture（系统架构）

```
Architecture
├── Architecture Documentation
│   ├── [x] 07-architecture.md — 架构总览
│   ├── [x] architecture/overview.md — 架构详细文档
│   ├── [x] architecture/security.md — 安全架构
│   ├── [x] architecture/collector-service.md — Collector Service 设计
│   ├── [x] architecture/review-2026-08-03.md — 架构审查报告
│   ├── [x] BLUEPRINT.md — 完整施工蓝图
│   ├── [ ] Architecture Decision Records — 待决 ADR
│   │   ├── [x] ADR-001 — 项目初始化
│   │   ├── [x] ADR-002 — Phase 0 审查批准
│   │   ├── [ ] ADR-003 — 前端框架选型 (待 RFC-003)
│   │   ├── [ ] ADR-004 — 搜索引擎选型 (待 RFC-004)
│   │   ├── [ ] ADR-005 — 图数据库选型 (待 RFC-005)
│   │   └── [ ] ADR-006 — 移动端选型 (待 RFC-006)
│   └── [ ] diagrams/ — 架构图
│       ├── [ ] system-context.mmd — 系统上下文图
│       ├── [ ] container.mmd — 容器图
│       ├── [ ] component.mmd — 组件图
│       ├── [ ] data-flow.mmd — 数据流图
│       └── [ ] deployment.mmd — 部署图
│
├── Module Design
│   ├── [x] Modular Monolith structure — 模块化单体目录结构
│   ├── [x] Context mapping — 限界上下文映射关系
│   ├── [x] Cross-context communication — 事件驱动的跨上下文通信
│   ├── [ ] Dependency injection design — DI 容器设计
│   ├── [ ] Configuration management — 配置管理方案
│   └── [ ] Error handling strategy — 全局错误处理策略
│
├── API Design
│   ├── [x] 11-api-style-guide.md — API 风格指南
│   ├── [x] api/api-design.md — API 详细设计
│   ├── [x] api/openapi.yaml — OpenAPI 3.1 骨架
│   ├── [ ] Authentication & Authorization — 认证授权设计
│   ├── [ ] Rate limiting design — 限流设计
│   └── [ ] API versioning strategy — API 版本策略
│
└── Technology Decisions
    ├── [x] RFC-001 — 后端语言 (Python FastAPI)
    ├── [x] RFC-002 — 消息队列 (Redis Streams)
    ├── [ ] RFC-003 — 前端框架 (Next.js vs Remix)
    ├── [ ] RFC-004 — 搜索引擎 (Elasticsearch vs Meilisearch)
    ├── [ ] RFC-005 — 图数据库 (Neo4j vs PostgreSQL AGE)
    ├── [ ] RFC-006 — 移动端框架 (Flutter vs React Native)
    └── [ ] Tech radar — 技术雷达文档
```

---

## 4. Domain（领域模型）

```
Domain
├── Domain Documentation
│   ├── [x] 04-domain-model.md — 领域模型总览
│   ├── [x] domain/domain-model.md — 限界上下文地图
│   ├── [x] domain/ddd-detailed.md — DDD 战术设计
│   ├── [x] domain/shared-kernel.md — 共享内核
│   └── [x] 03-glossary.md — 统一语言术语表
│
├── Content Context
│   ├── [x] Source aggregate — 内容源聚合根设计
│   ├── [x] Article aggregate — 文章聚合根设计
│   ├── [x] ContentIngestionService — 内容接入领域服务
│   ├── [x] ContentCleaningService — 内容清洗领域服务
│   ├── [x] DuplicateDetectionService — 去重领域服务
│   ├── [ ] ISourceRepository — 仓储接口实现
│   ├── [ ] IArticleRepository — 仓储接口实现
│   └── [ ] Content application services — 应用服务
│
├── Knowledge Context
│   ├── [x] KnowledgeEntity aggregate — 知识实体聚合根
│   ├── [x] KnowledgeRelation aggregate — 知识关系聚合根
│   ├── [x] Statement aggregate — 声明聚合根
│   ├── [x] EntityLinkingService — 实体链接领域服务
│   ├── [x] EntityExtractionService — 实体提取领域服务
│   ├── [x] RelationExtractionService — 关系提取领域服务
│   ├── [x] KnowledgeAggregationService — 声明聚合领域服务
│   ├── [x] GraphQueryService — 图谱查询领域服务
│   ├── [ ] IEntityRepository — 仓储接口实现
│   ├── [ ] IRelationRepository — 仓储接口实现
│   ├── [ ] IStatementRepository — 仓储接口实现
│   └── [ ] Knowledge application services — 应用服务
│
├── Search Context
│   ├── [x] SearchIndex aggregate — 搜索索引聚合根
│   ├── [x] SearchQuery value object — 搜索查询值对象
│   ├── [x] SearchOrchestrationService — 搜索编排领域服务
│   ├── [ ] ISearchRepository — 仓储接口实现
│   ├── [ ] Fulltext search implementation — 全文搜索实现
│   ├── [ ] Vector search implementation — 向量搜索实现
│   └── [ ] Hybrid search implementation — 混合搜索实现
│
├── AI Context
│   ├── [x] CompletionTask aggregate — AI 完成任务聚合根
│   ├── [x] ModelRouter — 模型路由服务
│   ├── [x] PromptCompiler — Prompt 编译服务
│   ├── [ ] IAIProviderPlugin — Provider 接口实现
│   └── [ ] AI application services — 应用服务
│
├── User Context
│   ├── [x] User aggregate — 用户聚合根
│   ├── [x] UserPreferences value object — 用户偏好值对象
│   ├── [ ] IUserRepository — 仓储接口实现
│   └── [ ] User application services — 应用服务
│
└── Plugin Context
    ├── [x] Plugin Manager design — 插件管理器设计
    ├── [x] Plugin lifecycle — 插件生命周期
    ├── [x] Plugin manifest — 插件清单规范
    ├── [ ] Plugin registry implementation — 插件注册实现
    └── [ ] Plugin sandbox — 插件沙箱
```

---

## 5. Event（事件系统）

```
Event
├── Event Documentation
│   ├── [x] 05-event-model.md — 事件模型总览
│   └── [x] domain/event-model.md — 领域事件目录
│
├── Event Bus
│   ├── [x] IEventBus interface — 事件总线接口
│   ├── [ ] Redis Streams implementation — Redis Streams 实现
│   ├── [ ] Outbox Pattern implementation — Outbox 模式实现
│   ├── [ ] Outbox Worker — 发件箱投递 Worker
│   ├── [ ] Event Consumer Groups — 消费者组
│   ├── [ ] Dead Letter Queue — 死信队列
│   └── [ ] Event retry policy — 事件重试策略
│
├── Event Catalog
│   ├── [x] Content events — ArticleFetched, ArticlePublished, etc.
│   ├── [x] Knowledge events — EntityCreated, EntityMerged, etc.
│   ├── [x] AI events — TaskStarted, TaskCompleted, etc.
│   ├── [x] Search events — SearchPerformed, IndexRebuilt, etc.
│   ├── [x] User events — UserRegistered, SubscriptionChanged, etc.
│   └── [ ] Event schema versioning — 事件 Schema 版本管理
│
├── Event Handlers
│   ├── [ ] ArticleFetched → AI Extraction handler
│   ├── [ ] ArticleFetched → Search Indexer handler
│   ├── [ ] EntityCreated → Graph Sync handler
│   ├── [ ] EntityCreated → Search Indexer handler
│   ├── [ ] RelationCreated → Graph Sync handler
│   ├── [ ] StatementApproved → Confidence Recalculation handler
│   └── [ ] TaskCompleted → Content Update handler
│
└── Event Store
    ├── [ ] system_event_log table — 事件存储表
    ├── [ ] Event replay capability — 事件重放能力
    └── [ ] Event store cleanup policy — 事件清理策略
```

---

## 6. Knowledge（知识引擎）

```
Knowledge
├── Knowledge Documentation
│   ├── [x] 06-knowledge-engine.md — 知识引擎总览
│   ├── [x] domain/knowledge-model.md — 知识本体论
│   └── [x] domain/graph-model.md — 图模型
│
├── Entity Extraction Pipeline
│   ├── [ ] NER Pipeline — 命名实体识别管道
│   │   ├── [ ] LLM-based NER — 基于 LLM 的实体提取
│   │   ├── [ ] Rule-based NER fallback — 基于规则的降级方案
│   │   └── [ ] Multi-model ensemble — 多模型集成
│   ├── [ ] Entity Linking — 实体链接
│   │   ├── [ ] Candidate generation — 候选实体生成
│   │   ├── [ ] Disambiguation — 实体消歧
│   │   └── [ ] Coreference resolution — 共指消解
│   └── [ ] Entity Merging — 实体合并
│       ├── [ ] Merge detection — 重复检测
│       ├── [ ] Property reconciliation — 属性协调
│       └── [ ] Relation redirection — 关系重定向
│
├── Relation Extraction Pipeline
│   ├── [ ] LLM-based Relation Extraction — 基于 LLM 的关系提取
│   ├── [ ] Relation type classification — 关系类型分类
│   ├── [ ] Temporal relation detection — 时序关系检测
│   └── [ ] Confidence scoring — 置信度评分
│
├── Statement Aggregation
│   ├── [ ] Statement merging logic — 声明合并逻辑
│   ├── [ ] Conflict detection — 冲突检测
│   ├── [ ] Conflict resolution — 冲突解决
│   └── [ ] Confidence recalculation — 置信度重算
│
├── Knowledge Quality
│   ├── [ ] Quality scoring dashboard — 质量评分仪表盘
│   ├── [ ] Automated quality checks — 自动化质量检查
│   ├── [ ] Manual review workflow — 人工审核工作流
│   └── [ ] Knowledge freshness monitoring — 知识时效性监控
│
└── Graph Operations
    ├── [ ] Graph Sync Worker — 图同步 Worker
    ├── [ ] Graph rebuild from Event Store — 从事件存储重建图
    ├── [ ] GDS Algorithm integration — 图算法集成
    └── [ ] Graph query optimization — 图查询优化
```

---

## 7. Search（搜索系统）

```
Search
├── Search Documentation
│   ├── [ ] Search architecture — 搜索架构设计
│   └── [ ] Search relevance model — 搜索相关性模型
│
├── Fulltext Search (Elasticsearch)
│   ├── [ ] ES Index mapping — 索引映射设计
│   ├── [ ] Multi-language analyzers — 多语言分词器
│   │   ├── [ ] CJK analyzer — 中日韩分词
│   │   ├── [ ] Standard analyzer — 英文分词
│   │   └── [ ] Language detection — 语言自动检测
│   ├── [ ] Article indexing pipeline — 文章索引管道
│   ├── [ ] Entity indexing pipeline — 实体索引管道
│   ├── [ ] Faceted search — 分面搜索
│   └── [ ] Highlighting — 搜索高亮
│
├── Vector Search (pgvector)
│   ├── [ ] Embedding generation pipeline — 向量生成管道
│   ├── [ ] IVF index configuration — IVF 索引配置
│   ├── [ ] Semantic similarity scoring — 语义相似度评分
│   └── [ ] Batch embedding — 批量向量化
│
├── Hybrid Search
│   ├── [ ] RRF (Reciprocal Rank Fusion) — 融合排序
│   ├── [ ] Weight tuning — 权重调优
│   └── [ ] Search quality evaluation — 搜索质量评估
│
├── Search Features
│   ├── [ ] Autocomplete — 自动补全
│   ├── [ ] Search suggestions — 搜索建议
│   ├── [ ] Query understanding — 查询理解
│   ├── [ ] Entity-aware search — 实体感知搜索
│   └── [ ] Multi-language search — 多语言搜索
│
└── Search API
    ├── [ ] GET /v1/search — 统一搜索端点
    ├── [ ] GET /v1/search/autocomplete — 自动补全端点
    └── [ ] GET /v1/search/suggestions — 搜索建议端点
```

---

## 8. AI（AI 集成）

```
AI
├── AI Documentation
│   ├── [ ] AI architecture — AI 架构设计
│   └── [ ] Model evaluation framework — 模型评测框架
│
├── Model Gateway
│   ├── [ ] Provider abstraction — Provider 抽象层
│   │   ├── [ ] OpenAI provider — OpenAI 适配器
│   │   ├── [ ] Anthropic provider — Anthropic 适配器
│   │   └── [ ] Ollama provider (local) — 本地模型适配器
│   ├── [ ] Model Router — 模型路由
│   │   ├── [ ] Load balancing — 负载均衡
│   │   ├── [ ] Fallback strategy — 降级策略
│   │   └── [ ] Cost optimization — 成本优化
│   ├── [ ] Rate limiting — API 限流
│   └── [ ] Usage tracking — 用量追踪
│
├── Prompt Management
│   ├── [ ] Prompt template engine — 模板引擎
│   ├── [ ] Prompt versioning — 版本管理
│   ├── [ ] Prompt A/B testing — 效果对比
│   └── [ ] Prompt library — 模板库
│
├── RAG Pipeline
│   ├── [ ] Context assembly — 上下文组装
│   ├── [ ] Retrieval optimization — 检索优化
│   ├── [ ] Source citation — 来源引用
│   └── [ ] Answer verification — 答案验证
│
├── AI Tasks
│   ├── [ ] Summarization task — 摘要任务
│   ├── [ ] Translation task — 翻译任务
│   ├── [ ] Entity extraction task — 实体提取任务
│   ├── [ ] Relation extraction task — 关系提取任务
│   ├── [ ] Chat/Q&A task — 问答任务
│   └── [ ] Async task queue — 异步任务队列
│
├── AI Evaluation
│   ├── [ ] Evaluation framework — 评测框架
│   ├── [ ] Benchmark datasets — 基准数据集
│   ├── [ ] Regression testing — 回归测试
│   ├── [ ] Human evaluation pipeline — 人工评测管道
│   └── [ ] Quality monitoring — 质量监控
│
└── AI Security
    ├── [ ] Prompt injection detection — 注入检测
    ├── [ ] Output validation — 输出验证
    ├── [ ] PII sanitization — PII 脱敏
    └── [ ] Audit logging — 审计日志
```

---

## 9. Plugin（插件系统）

```
Plugin
├── Plugin Documentation
│   ├── [x] 09-plugin-system.md — 插件系统总览
│   └── [x] architecture/plugin-specification.md — 插件规范
│
├── Plugin Manager
│   ├── [ ] Plugin registry — 插件注册中心
│   ├── [ ] Plugin loader — 插件加载器
│   ├── [ ] Lifecycle hooks — 生命周期钩子
│   ├── [ ] Dependency injection — 依赖注入
│   ├── [ ] Hot reload (Phase 3+) — 热加载
│   └── [ ] Plugin config management — 插件配置管理
│
├── Plugin Types
│   ├── Source Plugins
│   │   ├── [ ] RSS Source Plugin — RSS 内容源
│   │   ├── [ ] API Source Plugin — API 内容源
│   │   ├── [ ] Scraper Source Plugin — 爬虫内容源
│   │   └── [ ] Webhook Source Plugin — Webhook 内容源
│   ├── Processor Plugins
│   │   ├── [ ] HTML Cleaner Plugin — HTML 清洗
│   │   ├── [ ] Language Detector Plugin — 语言检测
│   │   └── [ ] Custom processor examples — 自定义处理器示例
│   ├── Storage Plugins
│   │   ├── [ ] PostgreSQL Plugin — PG 存储
│   │   └── [ ] Elasticsearch Plugin — ES 存储
│   ├── AI Provider Plugins
│   │   ├── [ ] OpenAI Plugin — OpenAI 适配
│   │   └── [ ] Anthropic Plugin — Anthropic 适配
│   └── UI Plugins
│       └── [ ] Graph Visualization Plugin — 图谱可视化
│
├── Plugin Security
│   ├── [ ] Plugin signature verification — 签名验证
│   ├── [ ] Permission system — 权限系统
│   └── [ ] Sandbox execution — 沙箱执行
│
└── Plugin Marketplace (Phase 5)
    ├── [ ] Plugin discovery — 插件发现
    ├── [ ] Plugin installation — 插件安装
    ├── [ ] Plugin rating/review — 评分和评论
    └── [ ] Plugin monetization — 付费插件
```

---

## 10. SDK（开发者工具）

```
SDK
├── SDK Design
│   ├── [ ] SDK architecture — SDK 架构设计
│   ├── [ ] API client design — API 客户端设计
│   └── [ ] Documentation strategy — 文档策略
│
├── Python SDK
│   ├── [ ] Core client — 核心客户端
│   ├── [ ] Entity API wrapper — 实体 API 封装
│   ├── [ ] Search API wrapper — 搜索 API 封装
│   ├── [ ] AI API wrapper — AI API 封装
│   ├── [ ] Async support — 异步支持
│   ├── [ ] Error handling — 错误处理
│   ├── [ ] Type hints — 类型提示
│   └── [ ] PyPI publication — PyPI 发布
│
├── TypeScript SDK
│   ├── [ ] Core client — 核心客户端
│   ├── [ ] Entity API wrapper — 实体 API 封装
│   ├── [ ] Search API wrapper — 搜索 API 封装
│   ├── [ ] AI API wrapper — AI API 封装
│   ├── [ ] React hooks — React Hooks 集成
│   └── [ ] npm publication — npm 发布
│
├── Dart SDK (Phase 5+)
│   ├── [ ] Core client — 核心客户端
│   └── [ ] pub.dev publication — pub.dev 发布
│
├── CLI Tool
│   ├── [ ] athena-cli — 命令行工具
│   ├── [ ] Source management commands — 源管理命令
│   └── [ ] Query commands — 查询命令
│
└── Developer Portal
    ├── [ ] API reference — API 参考文档
    ├── [ ] Quickstart guides — 快速入门指南
    ├── [ ] Tutorials — 教程
    └── [ ] Changelog — 变更日志
```

---

## 11. Infrastructure（基础设施）

```
Infrastructure
├── Development Environment
│   ├── [x] .env.example — 环境变量模板
│   ├── [x] docs/guides/environment-setup.md — 环境搭建指南
│   ├── [ ] docker-compose.yml — 本地开发环境
│   ├── [ ] Makefile / Taskfile — 常用命令封装
│   └── [ ] VS Code devcontainer — 容器化开发环境
│
├── CI/CD
│   ├── [x] .github/workflows/ci.yml — CI 管道
│   ├── [ ] Test pipeline — 测试管道完善
│   ├── [ ] Build pipeline — 构建管道
│   ├── [ ] Deploy pipeline — 部署管道
│   ├── [ ] Release pipeline — 发布管道
│   └── [ ] Dependency update automation — 依赖自动更新
│
├── Database Infrastructure
│   ├── [x] docs/database/er-diagram.md — ER 图
│   ├── [ ] Alembic migrations — 数据库迁移脚本
│   ├── [ ] Seed data — 种子数据
│   ├── [ ] Backup strategy — 备份策略实现
│   └── [ ] Migration testing — 迁移测试
│
├── Observability
│   ├── [ ] Structured logging — 结构化日志
│   ├── [ ] Metrics collection — 指标收集 (Prometheus)
│   ├── [ ] Distributed tracing — 分布式追踪 (OpenTelemetry)
│   ├── [ ] Health check endpoints — 健康检查端点
│   ├── [ ] Alerting rules — 告警规则
│   └── [ ] Dashboards — 监控仪表盘 (Grafana)
│
├── Deployment (Phase 4+)
│   ├── [ ] Docker image — Docker 镜像构建
│   ├── [ ] Kubernetes manifests — K8s 部署文件
│   ├── [ ] Helm chart — Helm Chart
│   ├── [ ] Terraform — 基础设施即代码
│   ├── [ ] Multi-region deployment — 多区域部署
│   └── [ ] Blue-green deployment — 蓝绿部署
│
├── Security Infrastructure
│   ├── [ ] TLS certificate management — 证书管理
│   ├── [ ] Secret management — 密钥管理
│   ├── [ ] WAF configuration — WAF 配置
│   ├── [ ] DDoS protection — DDoS 防护
│   └── [ ] Vulnerability scanning — 漏洞扫描自动化
│
└── Operations
    ├── [ ] Runbooks — 运维手册
    ├── [ ] Incident response plan — 事件响应计划
    ├── [ ] Disaster recovery plan — 灾难恢复计划
    ├── [ ] Capacity planning — 容量规划
    └── [ ] Cost monitoring — 成本监控
```

---

## 统计总览

| 模块 | 总任务 | 已完成 | 进行中 | 待开始 | 完成率 |
|------|--------|--------|--------|--------|--------|
| Vision | 8 | 5 | 0 | 3 | 63% |
| Product | 17 | 7 | 0 | 10 | 41% |
| Architecture | 27 | 18 | 0 | 9 | 67% |
| Domain | 30 | 24 | 0 | 6 | 80% |
| Event | 20 | 14 | 0 | 6 | 70% |
| Knowledge | 25 | 2 | 0 | 23 | 8% |
| Search | 20 | 0 | 0 | 20 | 0% |
| AI | 26 | 0 | 0 | 26 | 0% |
| Plugin | 20 | 2 | 0 | 18 | 10% |
| SDK | 21 | 0 | 0 | 21 | 0% |
| Infrastructure | 26 | 4 | 0 | 22 | 15% |
| **总计** | **240** | **76** | **0** | **164** | **32%** |

---

## 当前优先任务 (Next Actions)

按优先级排列的前 10 个待完成任务：

1. [ ] `docs/diagrams/system-context.mmd` — C4 系统上下文图
2. [ ] `docs/diagrams/container.mmd` — C4 容器图
3. [ ] `drafts/RFC-003-frontend-framework.md` — 前端框架选型 RFC
4. [ ] `drafts/RFC-004-search-engine.md` — 搜索引擎选型 RFC
5. [ ] `drafts/RFC-005-graph-database.md` — 图数据库选型 RFC
6. [ ] `docker-compose.yml` — 本地开发环境配置
7. [ ] `README.md` — 与 Blueprint 对齐的更新版
8. [ ] `MASTER.md` — 开发入口引导更新
9. [ ] `CONTRIBUTING.md` — 与 Blueprint 对齐的更新版
10. [ ] `drafts/ADR-003` — 前端框架选型 ADR（RFC-003 通过后）

---

*任务树随蓝图演进持续更新。新任务通过 RFC 或 ADR 流程添加。*
