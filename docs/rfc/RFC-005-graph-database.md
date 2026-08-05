# RFC-005: Graph Database Selection

## Metadata

| 字段 | 值 |
|------|-----|
| RFC ID | RFC-005 |
| Status | Draft |
| Priority | P1 |
| Target Phase | Phase 2 |

---

## 1. Background

Athena 的知识图谱需要专用的图数据库来执行路径遍历、子图查询、中心性分析等操作。PostgreSQL 可以处理实体和关系的 CRUD，但复杂的图遍历（如两实体间的最短路径）在 PG 中性能极差。

## 2. Problem

候选方案：Neo4j（专用图数据库）和 PostgreSQL + Apache AGE（PG 扩展）。需要在图查询性能、运维复杂度、与现有架构的集成之间做出权衡。

## 3. Goals

- [ ] P0: 路径遍历查询（≤ 3 度）< 500ms
- [ ] P0: 子图查询（≤ 2 度，≤ 200 节点）< 200ms
- [ ] P0: 支持 20+ 种关系类型和属性
- [ ] P1: 图算法支持（PageRank, Louvain 社区发现）
- [ ] P1: 与 PG 的事件驱动同步

## 4. Non-goals

- 不替代 PostgreSQL 做知识存储（Neo4j 是 Read-optimized Graph View，PG 是 Source of Truth）
- 不在此 RFC 中定义 Cypher 查询模板（留给 Graph Model 设计文档）
- 不评估 JanusGraph、ArangoDB、TigerGraph（社区/文档不足以支撑选择）

## 5. Proposal

**采用 Neo4j 5.x 作为 Athena 图数据库。**

核心理由：
1. 图遍历原生优化 — Index-free Adjacency，每个节点物理存储其邻接关系，遍历时零索引查找
2. GDS（Graph Data Science）算法库 — PageRank、Louvain、Betweenness Centrality 开箱即用
3. Cypher 查询语言 — 图查询的行业标准（ISO GQL 基于 Cypher）
4. 与 PG 分离部署 — 不增加 PG 负载，图查询故障不影响核心业务写入

## 6. Alternatives

| 方案 | 优点 | 缺点 | 为什么不选 |
|------|------|------|-----------|
| **Neo4j** | 图遍历性能最优；GDS 算法库；Cypher 标准 | 额外运维（独立服务）；数据同步需实现 | **采用** |
| PostgreSQL AGE | 无额外运维（PG 扩展）；事务一致 | 图遍历性能弱（基于 JOIN，非 Index-free）；Cypher 支持不完整；无 GDS | 图查询是核心功能，性能不能妥协 |
| Apache TinkerPop | 多后端支持（Neo4j, JanusGraph） | 抽象层增加复杂度；查询语言 Gremlin 学习曲线陡 | 过度抽象；不需要多后端 |

## 7. Risks

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| PG → Neo4j 同步断裂 | 中 | 高 | Outbox Pattern + Event Store 重放 |
| Neo4j 社区版限制 | 低 | 中 | 社区版单数据库 34B 节点足够 Phase 0-4 |

## 8. Future Evolution

Phase 2: 单节点 Neo4j Docker，基础图查询。
Phase 3: Neo4j 集群（Read Replicas）支持高并发读。
Phase 5: 评估 Neo4j Aura（托管服务）。

**重新审视触发条件**: 如果 PG AGE 的 Cypher 支持在 Phase 2 前达到生产可用级别，重新评估单引擎方案。

## 9. References

- [Graph Model Design](../domain/graph-model.md)
- [Architecture Overview](../architecture/overview.md)
