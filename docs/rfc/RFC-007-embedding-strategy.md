# RFC-007: Embedding Strategy

## Metadata

| 字段 | 值 |
|------|-----|
| RFC ID | RFC-007 |
| Status | Draft |
| Priority | P1 |
| Target Phase | Phase 2 |

---

## 1. Background

Athena 的向量搜索、语义相似度、Entity Linking 都依赖文本 Embedding。需要确定 Embedding 模型选型、向量存储方案和更新策略。

## 2. Problem

Embedding 影响搜索召回质量、多语言支持、AI Pipeline 效率。选择不当会导致搜索结果差（向量质量低）、成本高（频繁重算 Embedding）、延迟大。

## 3. Goals

- [ ] P0: 多语言支持 — 至少支持中英日韩 + 拉丁语系
- [ ] P0: 向量维度 ≤ 1536（与 pgvector ivfflat 索引兼容）
- [ ] P1: Embedding 生成延迟 < 100ms per text
- [ ] P1: 每百万 token Embedding 成本 < $0.50
- [ ] P2: 支持本地模型（离线/隐私场景）

## 4. Non-goals

- 不在此 RFC 中定义具体的 Embedding Pipeline 实现
- 不评估 Fine-tuning 自有 Embedding 模型（留给 Phase 5）
- 不替代 LLM — Embedding 负责"相似度"，LLM 负责"理解"

## 5. Proposal

**Phase 2-3: 使用 OpenAI text-embedding-3-small 作为主力 Embedding 模型，pgvector 作为向量存储。Phase 4+ 评估本地模型降本。**

核心理由：
1. text-embedding-3-small: $0.02/1M tokens，维度 512/1536 可选，多语言支持好
2. pgvector 已在 PostgreSQL 中 — 零额外运维
3. Embedding 只在内容入库时生成一次（非实时计算），更新频率低

**Embedding 更新策略**：
- 文章内容清洗后生成 Embedding（ArticleFetched 事件触发）
- Embedding 不可变 — 内容不变不重算
- 模型升级时批量重算（Phase 3+ 建立重算管道）

## 6. Alternatives

| 方案 | 优点 | 缺点 | 为什么不选 |
|------|------|------|-----------|
| **OpenAI embed-3** | 质量好；多语言；成本低 | 依赖外部 API；网络延迟 | **采用** |
| 本地模型（BGE/M3E） | 零 API 成本；低延迟 | 多语言质量不如 OpenAI；需要 GPU | Phase 4 降本时考虑 |
| Cohere Embed | 质量好 | 成本高（$0.10/1M）；多语言不如 OpenAI | 成本差距 5x |

## 7. Risks

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| OpenAI API 不可用 | 低 | 高 | Phase 4 引入本地模型作为 Fallback |
| Embedding 质量退化 | 低 | 中 | 建立 Embedding 质量回归测试 |

## 8. Future Evolution

Phase 4+ 评估本地模型（BGE-M3）替代 OpenAI 以降本。多语言场景下，本地模型的中文质量已接近 OpenAI，英文仍有差距。

---

## 9. References

- [Data Model — pgvector](../08-data-model.md)
- [RFC-001 — Backend Language](RFC-001-backend-language.md)
