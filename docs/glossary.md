# Glossary (术语表) v1.0

## 概述

本文档定义 Athena 项目中的统一领域语言（Ubiquitous Language），确保团队、文档和代码使用一致的术语。

---

## A

**Aggregate (聚合)**
DDD 术语。一组相关联的实体和值对象，以聚合根为访问入口。如 `Article`（文章聚合，含 Source 引用和 Authors 列表）。

**Aggregate Root (聚合根)**
聚合的入口实体，拥有全局唯一标识。对聚合内其他实体的操作必须通过聚合根。如 `KnowledgeEntity`。

---

## B

**Bounded Context (限界上下文)**
DDD 术语。领域模型的语义边界。Athena 有六个限界上下文：Content、Knowledge、Search、AI、User、Plugin。

---

## C

**Claim (参见 Statement)**
声明。

**Confidence (置信度)**
0.0 到 1.0 之间的值，表示一条知识（实体属性或关系）的可信程度。由支撑声明的置信度加权计算。

**CQRS (Command Query Responsibility Segregation)**
读写分离模式。Athena Phase 3+ 为搜索场景引入读模型。

---

## D

**Domain Event (领域事件)**
限界上下文中发生的有意义的状态变化。如 `ArticlePublished`、`EntityCreated`。

**Domain Service (领域服务)**
DDD 术语。处理跨实体、无自然归属的业务逻辑的无状态服务。如 `EntityLinkingService`。

---

## E

**Entity (DDD 实体)**
有唯一标识的领域对象，标识在其生命周期中不变。

**Entity (Knowledge 知识实体)**
知识图谱中的一个节点。代表现实世界中的具体事物（人、组织、地点等）或抽象概念。

**Entity Linking (实体链接)**
将文本中的名称提及（mention）映射到知识图谱中已有实体的过程。

**Event Sourcing (事件溯源)**
将聚合的状态变更存储为不可变事件序列的模式。Athena Phase 5+ 可选引入。

---

## G

**Graph Projection (图投影)**
Neo4j GDS 术语。为图算法创建内存中的图视图。

---

## K

**Knowledge Triangle (知识三角)**
Athena 知识模型的核心结构：Entity (实体) – Relation (关系) – Statement (声明)。

---

## L

**LLM (Large Language Model)**
大语言模型，如 GPT-5、Claude 等。

---

## M

**Modular Monolith (模块化单体)**
Athena Phase 0-3 的架构风格。代码组织在独立模块中（与微服务相同的边界），但部署为单个进程。

---

## N

**NER (Named Entity Recognition)**
命名实体识别。从文本中识别出人名、地名、组织名等命名实体。

---

## P

**pgvector**
PostgreSQL 向量扩展，用于存储和查询 Embeddings。

**Plugin (插件)**
Athena 的可扩展组件。五类插件：Source、Processor、Storage、AI、UI。详见 [Plugin Specification](architecture/plugin-specification.md)。

**Provenance (溯源)**
知识的来源追溯链：原始文章 → 声明 → 结构化知识。

---

## R

**RAG (Retrieval-Augmented Generation)**
检索增强生成。先检索相关文档，再让 LLM 基于检索结果生成回答。Athena 的核心 AI 模式。

**Relation (关系)**
知识图谱中两个实体间的有向连接。如 "Tim Cook" –[LED_BY]→ "Apple Inc."。

**Repository (仓储)**
DDD 术语。聚合的持久化抽象接口。如 `IArticleRepository`。

**RFC (Request for Comments)**
Athena 的功能设计提案流程。见 [RFC Template](rfc/RFC-000-template.md)。

**RRF (Reciprocal Rank Fusion)**
混合搜索中融合全文搜索和向量搜索结果排序的算法。

---

## S

**Statement (声明)**
从原始文章中提取的关于实体或关系的断言。声明是知识的可溯源最小单元。包含原文摘录、置信度和审核状态。

**Shared Kernel (共享内核)**
多个限界上下文共享的通用类型和值对象。如 `UserId`、`Language`、`Pagination`。

---

## T

**Test Pyramid (测试金字塔)**
Athena 的测试分层策略：Unit (70%) → Integration (20%) → E2E (10%)。

---

## U

**Ubiquitous Language (统一语言)**
DDD 核心实践。所有团队成员（开发、产品、领域专家）使用相同的术语。本文档即为该语言的权威定义。

---

## V

**Value Object (值对象)**
DDD 术语。无唯一标识、通过属性值来定义的不可变对象。如 `Language`、`Confidence`。

**Vector Search (向量搜索)**
基于语义相似度的搜索。将文本转为 Embedding 向量，通过余弦相似度查找最相关的结果。

---

*术语表随领域模型演进同步更新。新增术语需通过 PR 添加到本文档。*
