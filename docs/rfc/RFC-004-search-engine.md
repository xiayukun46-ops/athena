# RFC-004: Search Engine Selection

## Metadata

| 字段 | 值 |
|------|-----|
| RFC ID | RFC-004 |
| Status | Draft |
| Priority | P1 |
| Target Phase | Phase 2 |

---

## 1. Background

Athena 的搜索需要同时支持全文搜索（关键词匹配 + 高亮 + 分面）和跨语言分词（特别是 CJK）。当前两个候选方案：Elasticsearch（成熟但重量级）和 Meilisearch（轻量但功能受限）。

## 2. Problem

搜索是 Athena 的核心功能（不是可选功能）。不恰当的搜索引擎选择可能导致：搜索结果质量差、多语言分词不准确、运维成本过高、扩展受限。

## 3. Goals

- [ ] P0: CJK 分词支持（中文、日文、韩文原生分析器）
- [ ] P0: 分面搜索（Faceted Search）— 按 entity_type, language, category 统计
- [ ] P0: 高亮（Highlight）— 返回匹配位置的文本片段
- [ ] P1: 分布式扩展（Phase 3+ 数据量 > 10M 文档）
- [ ] P1: 运维复杂度可控

## 4. Non-goals

- 不替代 PostgreSQL 做主存储（ES 是 Search Index，不是 Source of Truth）
- 不处理向量搜索（由 pgvector 负责，ES 仅负责全文）
- 不在此 RFC 中定义具体的 Index Mapping（留给 Phase 2 设计文档）

## 5. Proposal

**采用 Elasticsearch 8.x 作为 Athena 全文搜索引擎。**

核心理由：
1. CJK 分词成熟 — 内置 `kuromoji`（日文）、`nori`（韩文）、`smartcn`（中文）分析器
2. 分面搜索原生支持 — `aggregations` API 覆盖按 entity_type、language、category 的统计需求
3. 高亮功能完善 — `highlight` API 支持多字段、片段大小、前后文
4. 分布式架构成熟 — 数据量从 10K → 100M 不需换引擎
5. 与 PostgreSQL 互补 — PG 管事务和关系，ES 管搜索

## 6. Alternatives

| 方案 | 优点 | 缺点 | 为什么不选 |
|------|------|------|-----------|
| **Elasticsearch** | CJK 分词成熟；分面搜索；分布式扩展 | 运维复杂；内存消耗大 | **采用** |
| Meilisearch | 部署简单；API 友好；轻量 | CJK 分词不成熟（社区插件）；无分面搜索；扩展受限 | CJK 是硬需求 |
| PostgreSQL tsvector | 零运维（已在 PG 中）；事务一致 | CJK 分词弱（无内置中文分词器）；无分面搜索；高亮能力差 | 中文支持不足 |
| Typesense | 速度快；部署简单 | 社区小；CJK 分词不成熟；分布式能力弱 | 社区和功能双重不足 |

## 7. Risks

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| ES 运维复杂度拖慢 Phase 2 | 高 | 中 | Docker Compose 一键启动；Phase 1 编写运维 Runbook |
| ES 内存消耗 > 预算 | 中 | 中 | Phase 2 从 2GB heap 起步；监控 + 按需扩容 |
| CJK 分词质量不达标 | 低 | 高 | 建立分词评测集；Phase 2 调优自定义词典 |

## 8. Future Evolution

Phase 2: 单节点 ES Docker，基础全文搜索。
Phase 3: 升级为 3 节点集群，支持高可用。
Phase 5: 评估 Elastic Cloud（托管服务）vs 自运维。

**重新审视触发条件**: 文档量 < 100K 时如果运维成本与 Meilisearch 差距过大，可在 Phase 2 前重新评估。

## 9. References

- [Search Context Design](../domain/ddd-detailed.md)
- [API Design — Search](../api/api-design.md)
