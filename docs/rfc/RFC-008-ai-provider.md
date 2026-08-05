# RFC-008: AI Provider Strategy

## Metadata

| 字段 | 值 |
|------|-----|
| RFC ID | RFC-008 |
| Status | Draft |
| Priority | P1 |
| Target Phase | Phase 3 |

---

## 1. Background

Athena 的 AI Pipeline 需要调用 LLM 完成实体提取、关系提取、摘要、翻译、问答。需要多 Provider 策略以保证可用性和成本控制。

## 2. Problem

单一 Provider 有风险：API 不可用、成本波动、模型退场。Athena 需要多 Provider 路由 + 降级机制 + 成本优化。

## 3. Goals

- [ ] P0: 至少支持 2 个 Provider（OpenAI + Anthropic）
- [ ] P0: 单个 Provider 故障时自动切换到备用 Provider
- [ ] P1: 成本敏感的模型选择（简单任务用小模型，复杂任务用大模型）
- [ ] P1: 异步任务队列（所有 AI 调用通过队列，非阻塞）

## 4. Non-goals

- 不在 Phase 2 前实现完整的 Model Gateway（Phase 3 实现）
- 不在此 RFC 中决定每个具体任务使用哪个模型（留给 Phase 3 设计）

## 5. Proposal

**采用双 Provider 策略：OpenAI（主力）+ Anthropic（备援）。通过 IAIProviderPlugin 接口抽象，Model Router 根据任务类型、成本预算和可用性自动路由。**

路由规则：
1. 默认路由到 OpenAI（成本低、模型选择多）
2. OpenAI 不可用或限流 → 自动切换到 Anthropic
3. 简单任务（摘要、分类）→ 小模型（GPT-5-mini / Claude-Haiku）
4. 复杂任务（NER、RE、问答）→ 大模型（GPT-5 / Claude-Sonnet）
5. Phase 4+ 评估本地模型（Ollama）用于低延迟/隐私场景

## 6. Alternatives

| 方案 | 优点 | 缺点 | 为什么不选 |
|------|------|------|-----------|
| **OpenAI + Anthropic** | 双保障；模型互补；社区支持好 | 两个 Provider 都要维护 | **采用** |
| 仅 OpenAI | 简单 | 单点故障；成本不可控 | 风险太大 |
| OpenAI + 本地 Ollama | 离线能力；零 API 成本 | 本地模型质量不足（Phase 2 不可用） | Phase 4 引入 |
| 多 Provider（5+） | 极致可用性 | 维护成本爆炸 | 过度设计 |

## 7. Risks

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| OpenAI 大规模故障 | 低 | 高 | Anthropic 自动接管 |
| 两个 Provider 同时不可用 | 极低 | 极高 | Phase 4 Ollama 本地 Fallback |
| 成本超预算 | 中 | 中 | 用量追踪 + 每日预算上限 + 告警 |

## 8. Future Evolution

Phase 4 引入 Ollama 本地模型用于低延迟场景（≤ 50ms）。Phase 5 评估 Google Gemini 作为第三个 Provider。

---

## 9. References

- [AI Context Design](../domain/ddd-detailed.md)
- [Security — AI](../13-security.md)
