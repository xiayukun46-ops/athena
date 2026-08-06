# EPICS — Epic-Level Tasks

> Athena 最高层的任务分解。每个 Epic 是一个独立可交付的价值单元。

---

## Epic 1: Knowledge Foundation

| 字段 | 值 |
|------|-----|
| Status | In Progress |
| Sprint | Sprint 1 |
| Goal | 完成 Knowledge Core 领域层 |
| Deliverables | athena_core + athena_knowledge 包, 100% 测试覆盖 |
| Issues | ISS-001 ~ ISS-008 |

---

## Epic 2: Knowledge Engine

| 字段 | 值 |
|------|-----|
| Status | Planned |
| Target | Phase 2 |
| Goal | AI 驱动的知识提取管道 |
| Deliverables | Collector Service, NER Pipeline, Entity Linking, Relation Extraction |

---

## Epic 3: Knowledge Graph

| 字段 | 值 |
|------|-----|
| Status | Planned |
| Target | Phase 2 |
| Goal | 完整的知识图谱存储和查询 |
| Deliverables | Neo4j 同步, Graph API, GDS 图算法 |

---

## Epic 4: Search

| 字段 | 值 |
|------|-----|
| Status | Planned |
| Target | Phase 2 |
| Goal | 全文 + 向量混合搜索 |
| Deliverables | Elasticsearch 索引, pgvector, Hybrid Search API |

---

## Epic 5: AI Reasoning

| 字段 | 值 |
|------|-----|
| Status | Planned |
| Target | Phase 3 |
| Goal | AI 推理和问答 |
| Deliverables | Model Gateway, RAG Pipeline, AI Evaluation |

---

## Epic 6: Workspace

| 字段 | 值 |
|------|-----|
| Status | Planned |
| Target | Phase 4 |
| Goal | 用户交互界面 |
| Deliverables | Web App (Next.js), Personalization |

---

## Epic 7: Flutter

| 字段 | 值 |
|------|-----|
| Status | Planned |
| Target | Phase 4 (延后决策) |
| Goal | 移动端应用 |
| Deliverables | Flutter App (待 RFC-006 最终确认) |
