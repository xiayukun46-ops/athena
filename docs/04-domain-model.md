# 04 — Domain Model

> Athena 的领域模型。定义系统"是什么"——而不是"怎么实现"。

**详细设计见**: [domain/domain-model.md](domain/domain-model.md) (总览) + [domain/ddd-detailed.md](domain/ddd-detailed.md) (战术设计)

---

## 领域概览

Athena 划分为六个限界上下文（Bounded Context）：

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Content  │  │Knowledge │  │  Search  │
│ 内容管理 │→│ 知识图谱 │→│  搜索    │
└────┬─────┘  └────┬─────┘  └──────────┘
     │             │
     ▼             ▼
┌──────────┐  ┌──────────┐
│    AI    │  │   User   │
│ AI 编排  │  │   用户   │
└──────────┘  └──────────┘
```

---

## 为什么这样划分

### 选择 DDD 而非传统分层

**替代方案 1: MVC 分层 (Controller → Service → Repository)**

不选理由：当系统跨 6 个领域时，MVC 分层导致"改一个功能要跨 3 层改 6 个文件"。领域内聚更好——Content 相关的所有代码（API、逻辑、数据）在同一个包内。

**替代方案 2: 微服务（每个上下文一个独立服务）**

不选理由：Phase 0-3 团队规模不需要分布式复杂度。但模块间通过接口（非直接 API 调用）通信，未来拆分成本低。

### 选择 6 个上下文而非更少或更多

**更少（如 3 个）**: 将 Knowledge + Search + AI 合并。**不选理由**: 三者职责不同——Knowledge 管"存知识"，Search 管"找知识"，AI 管"理解知识"。合并后耦合过高。

**更多（如 10 个）**: 将 Content 拆分为 Source Management + Article Management。**不选理由**: 两者天然紧密耦合，拆分增加不必要的上下文映射复杂度。

---

## 各上下文职责

### Content Context
**聚合根**: Source, Article
- 多源内容接入（RSS / API / Scraper）
- 内容清洗、标准化、去重
- 发布 ArticleFetched 事件，触发下游处理

### Knowledge Context
**聚合根**: KnowledgeEntity, KnowledgeRelation, Statement
- 实体管理（CRUD、多语言、合并、废弃）
- 关系管理（创建、查询、时间范围）
- 声明管理（审核、聚合、冲突解决）

### Search Context
**聚合根**: SearchIndex
- 全文搜索（Elasticsearch）
- 向量搜索（pgvector）
- 混合搜索（RRF 融合）

### AI Context
**聚合根**: CompletionTask
- 模型路由（多 Provider、多 Model）
- Prompt 模板管理
- 异步任务调度

### User Context
**聚合根**: User
- 用户身份和偏好
- 订阅管理

### Plugin Context
- 插件注册、加载、生命周期
- 五类插件: Source / Processor / Storage / AI / UI

---

## 关键设计决策

### 决策 1: Statement 是独立聚合根

**为什么**: Statement 有自己的生命周期——创建、审核、聚合。它不隶属于 Entity 或 Relation。多条 Statement 可以指向同一个事实，形成共识或冲突。

**替代方案**: Statement 作为 Entity 的子实体。不选理由：如果 Statement 依附于 Entity，跨 Entity 的声明（如"Tim Cook 领导 Apple"同时影响两个实体）不好归属。

### 决策 2: Article 不继承 Entity

**为什么**: Article 是"内容"，Entity 是"知识"。一篇文章可以提多个实体，一个实体可以被多篇文章提及。两者是 M:N 关系，不是继承关系。

**替代方案**: 万物皆 Entity，Article 是 Entity 的子类型。不选理由：内容管理和知识管理有不同的生命周期和操作模式，强行统一增加复杂度。

### 决策 3: 跨上下文通信仅通过事件

**为什么**: 事件解耦。Content 发布文章后不需要知道 Knowledge 怎么处理——它只发射 ArticleFetched 事件。

**替代方案**: 直接 API 调用。不选理由：产生编译期/运行时依赖，未来拆分微服务时需大改。

---

## 未来扩展

- **新实体类型**: 在 EntityType 枚举新增即可，不影响现有模型
- **新内容源类型**: 实现 ISourcePlugin 接口，注册到 Plugin Manager
- **新 AI 能力**: 增加新的 CompletionTask 类型 + 对应的事件处理器
- **微服务拆分**: 接口替换——Python 模块内接口 → gRPC/REST，开销可控

---

## 相关文档

- [05-event-model.md](05-event-model.md) — 事件的完整定义
- [06-knowledge-engine.md](06-knowledge-engine.md) — 知识引擎设计
- [07-architecture.md](07-architecture.md) — 架构如何组织这些领域
- [08-data-model.md](08-data-model.md) — 数据如何存储
- [domain/ddd-detailed.md](domain/ddd-detailed.md) — 完整战术设计
