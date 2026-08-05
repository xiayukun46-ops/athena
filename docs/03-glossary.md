# 03 — Glossary

> Athena 项目的统一领域语言（Ubiquitous Language）。
> 本文档是术语的权威定义。所有文档、代码、讨论必须使用此处定义的术语。
> 
> 完整 A-Z 术语表见: [glossary.md](glossary.md)

---

## 核心术语

### Entity（知识实体）
知识图谱中的一个节点。代表现实世界中的具体事物（人、组织、地点）或抽象概念。
- **类型**: Person, Organization, Location, Event, Concept, Product, Work, NaturalEntity
- **不同于**: DDD Entity（有唯一标识的领域对象）
- **参见**: [04-domain-model.md](04-domain-model.md), [domain/knowledge-model.md](domain/knowledge-model.md)

### Relation（关系）
两个 Entity 之间的有向连接。附带属性和时间范围。
- **示例**: "Tim Cook" —[LED_BY]→ "Apple Inc." (role=CEO, start=2011-08-24)
- **参见**: [domain/graph-model.md](domain/graph-model.md)

### Statement（声明）
从原始文章中提取的关于实体或关系的**可溯源断言**。
- **为什么存在**: 传统知识图谱直接存"事实"，但无法回答"谁说的？在哪说的？"
- **参见**: [domain/knowledge-model.md](domain/knowledge-model.md) — Knowledge Triangle

### Knowledge Triangle（知识三角）
Athena 的核心知识表示模型：Entity → Relation → Statement
- 三条边缺一不可：实体告诉"是什么"，关系告诉"什么关联"，声明告诉"谁说的"

### Confidence（置信度）
0.0 到 1.0 之间的值，表示一条知识的可信程度。
- 由支撑声明的置信度加权计算
- **不代表**概率，**代表**提取质量

### Provenance（溯源）
知识的来源追溯链：原始文章 → 声明 → 结构化知识
- 用户在任意层级可点击跳转到原始内容

### Bounded Context（限界上下文）
DDD 术语。领域模型的语义边界。Athena 有六个：
Content、Knowledge、Search、AI、User、Plugin
- **参见**: [04-domain-model.md](04-domain-model.md)

### Aggregate Root（聚合根）
DDD 术语。聚合的入口实体。对聚合内其他实体的操作必须通过聚合根。
- **示例**: KnowledgeEntity 是聚合根，EntityProperty 是其内部的实体

### Modular Monolith（模块化单体）
Athena Phase 0-3 的架构风格。代码组织在独立模块中（与微服务相同的边界），但部署为单个进程。
- **为什么**: 早期团队规模不需要分布式复杂度，但模块边界为未来拆分预留

### RAG（检索增强生成）
先检索相关文档，再让 LLM 基于检索结果生成回答。
- Athena 的核心 AI 模式：RAG 管道 = 实体检索 + 关系查询 + 原文摘录 → LLM 生成

### Plugin（插件）
Athena 的可扩展组件。五类：Source、Processor、Storage、AI、UI
- **参见**: [09-plugin-system.md](09-plugin-system.md)

### Outbox Pattern（发件箱模式）
保证数据库写入与事件发布的原子性。
- 事件先写入 `system_event_log` 表（与业务数据在同一个事务中），再由独立 Worker 投递到消息队列
- **参见**: [05-event-model.md](05-event-model.md)

### pgvector
PostgreSQL 向量扩展，用于存储和查询 Embeddings。
- **选型理由**: 避免引入独立的向量数据库，降低运维复杂度

### Shared Kernel（共享内核）
多个限界上下文共享的基础类型和值对象。
- 包括: EntityId, Language, Confidence, Pagination, DomainEvent 基类
- **参见**: [domain/shared-kernel.md](domain/shared-kernel.md)

---

## 相关文档

- [glossary.md](glossary.md) — 完整 A-Z 术语表
- [04-domain-model.md](04-domain-model.md) — 领域模型
- [07-architecture.md](07-architecture.md) — 架构总览
