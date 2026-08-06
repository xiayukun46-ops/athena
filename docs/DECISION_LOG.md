# Decision Log

> Athena 项目架构决策日志。
> 记录每一个"为什么这样改"、"为什么否定"、"哪个 RFC 被放弃"、"哪个设计被延期"。
> 按时间倒序排列，最新决策在前。

---

## 2026-08-06

### D-016: Sprint 1 定义为 Knowledge Core

**决策**: Sprint 1 聚焦纯领域层——Knowledge Core 包。
**为什么**: 领域层是所有未来模块的依赖基础。必须先稳定、先测试、先冻结。
**否定方案**: 同时启动数据库迁移。否定理由：数据库 Schema 依赖领域模型定义——领域层不完整时建表会有反复。
**参考**: [sprint1-plan.md](sprint1-plan.md)

### D-015: 序列化层与验证层纳入 Sprint 1

**决策**: 领域层不仅包含数据模型，还包含序列化（to_dict/from_dict）和领域验证（Validator）。
**为什么**: 序列化和验证是领域对象的"自描述能力"。如果没有它们，外部代码会重复实现序列化逻辑——违反 DRY。
**否定方案**: 序列化留到 API 层。否定理由：FastAPI 的 Pydantic 序列化不共享给 Worker/Collector/CLI。

### D-014: Architecture Freeze — 10 个领域冻结

**决策**: Knowledge Object, Event, Workflow, Plugin Interface, Agent Interface, Architecture Layer, API Convention, Naming Convention, Database Schema, Storage Engine 冻结。修改仅通过 ADR。
**为什么**: Freeze 后的变更成本指数增长。Phase 1 开始写代码后，领域模型变更会导致大量重写。
**延期**: 前端框架、移动端、Embedding 模型细节、缓存策略、UI 组件库未冻结——留给后续 RFC。
**参考**: [architecture-baseline.md](architecture/architecture-baseline.md)

### D-013: Documentation as Code 标准

**决策**: 文档质量用三条标准衡量：可视化（有图）、成熟度（形成 ADR/RFC）、完整性（AI 可独立实现）。
**为什么**: Blueprint 的目标不是给人看——是给未来的 AI（Codex, Claude Code, Cursor）不依赖聊天上下文独立开发。
**参考**: [TEMPLATE.md](TEMPLATE.md)

### D-012: RFC-010 版本策略采用 SemVer + Event Version 字段

**决策**: 设计文档使用 SemVer，领域事件使用 `version` 字段（整数递增），Breaking Change → 新事件类型。
**否定方案**: Schema Registry（Avro/Protobuf）。否定理由：引入额外组件，Phase 0-3 运维负担过重。
**延期**: Phase 3 评估 Confluent Schema Registry。

### D-011: RFC-009 插件热加载延至 Phase 3

**决策**: Phase 2 实现完整生命周期 + 异常隔离。Phase 3 基于文件监控（watchdog）实现热加载。
**否定方案**: 微服务隔离（每个插件独立进程）。否定理由：Phase 0-3 运维复杂度过高。
**延期**: WASM 沙箱作为 Phase 5 方向。

### D-010: RFC-008 双 Provider 策略 — OpenAI + Anthropic

**决策**: OpenAI（主力，成本低模型多）+ Anthropic（备援，自动切换）。
**否定方案**: 仅 OpenAI（单点故障）。仅本地 Ollama（质量不足 Phase 2 使用）。
**延期**: Phase 4 评估 Ollama 本地模型用于低延迟场景。

### D-009: RFC-007 Embedding 选择 OpenAI text-embedding-3-small

**决策**: Phase 2-3 主力 Embedding。$0.02/1M tokens，多语言支持好。
**否定方案**: 本地模型 BGE-M3（中文质量接近但英文有差距，且需要 GPU）。
**延期**: Phase 4 降本时重新评估本地模型。

### D-008: RFC-006 移动端框架延至 Phase 3 决策

**决策**: 暂定 Flutter。Phase 3 末基于团队技能栈和 Web 前端选型最终决定。
**为什么**: 移动端不是 Phase 1-3 的交付物。过早决策可能在 Phase 4 时需要推翻。
**延期**: PWA 也可以替代移动端——未排除。

### D-007: RFC-005 图数据库选择 Neo4j 而非 PostgreSQL AGE

**决策**: Neo4j 5.x 作为图数据库。
**为什么否决 PG AGE**: 图遍历基于 JOIN 非 Index-free Adjacency，性能差距 10-100x。GDS 算法库无可替代。Cypher 支持不完整。
**代价**: 需要维护独立 Neo4j 实例 + PG→Neo4j 同步管道。

### D-006: RFC-004 搜索引擎选择 Elasticsearch 而非 Meilisearch

**决策**: Elasticsearch 8.x 作为全文搜索引擎。
**为什么否决 Meilisearch**: CJK 分词不成熟（社区插件），无原生分面搜索，扩展受限。CJK 是硬需求——Athena 必须支持中日韩语言。
**代价**: ES 运维复杂度更高（内存消耗、集群管理）。

### D-005: RFC-003 前端选择 Next.js 而非 Remix

**决策**: Next.js 15 (App Router) 作为 Web 前端。
**为什么否决 Remix**: 社区规模约为 Next.js 的 1/10。虽然 Web Standard 优先的理念好，但生态不足支撑 Phase 5。
**代价**: App Router 学习曲线陡。

### D-004: RFC-002 消息队列选择 Redis Streams (P1-2) → Kafka (P3+)

**决策**: Phase 1-2 使用 Redis Streams。Phase 3+ 迁移至 Kafka。
**为什么否决 RabbitMQ**: 运维复杂度高（Erlang 运行时），单体阶段的复杂路由优势无法发挥。
**为什么否决 Kafka Phase 1**: 至少 3 Broker + KRaft，单体阶段过度设计。
**关键设计**: `IEventBus` 接口通过 Adapter 模式封装——换实现不影响业务代码。
**参考**: [RFC-002-message-queue.md](rfc/RFC-002-message-queue.md)

### D-003: RFC-001 后端语言选择 Python FastAPI 而非 Go / Rust

**决策**: Python 3.12 + FastAPI。
**为什么否决 Go**: AI SDK 生态不全，版本滞后（langchaingo 远落后于 LangChain）。
**为什么否决 Rust**: AI 生态几近空白。性能最强但开发效率和招聘困难。
**为什么否决混合方案**: Phase 0-3 Modular Monolith 混合语言增加运维复杂度。
**代价**: Python GIL 限制 CPU 密集型任务并行度。缓解：CPU 密集型下放到独立 Worker 或 Rust 插件。
**参考**: [RFC-001-backend-language.md](rfc/RFC-001-backend-language.md)

---

## 2026-08-05

### D-002: ADR-002 Phase 0 架构审查通过

**决策**: Phase 0 完成度 70%，批准进入 Phase 1（条件：完成 6 个 RFC）。
**识别风险**: EAV 性能、PG-Neo4j 同步、AI 质量 3 个高风险。

### D-001: ADR-001 项目架构初始化

**决策**: Modular Monolith（Phase 0-3）+ Apache 2.0 + 8 个 First 原则。
**为什么否决微服务**: 团队规模不需要。模块间已通过接口解耦——拆分成本可控。
**为什么否决 MIT 许可**: 缺少专利保护条款。AI 项目未来涉及算法专利。
**为什么否决传统 MVC**: 领域内聚优于技术分层。
**参考**: [ADR-001-project-init.md](adr/ADR-001-project-init.md)

---

## 被放弃的设计

| 设计 | 放弃时间 | 放弃原因 |
|------|----------|----------|
| 传统 MVC 分层 | 2026-08-03 | 跨层修改频繁，不适应 10 年尺度 |
| 微服务架构 | 2026-08-03 | Phase 0 过度设计（延至 Phase 4+） |
| MIT License | 2026-08-03 | 无专利保护 |
| Meilisearch | 2026-08-05 | CJK 分词不成熟 |
| PostgreSQL AGE | 2026-08-05 | 图遍历性能不足 |
| Remix | 2026-08-05 | 生态规模不足 |
| RabbitMQ | 2026-08-05 | 运维复杂度过高 |
| Rust 后端 | 2026-08-05 | AI 生态空白 |
| Go 后端 | 2026-08-05 | AI SDK 滞后 |
| 本地 Embedding (Phase 1) | 2026-08-06 | 质量不足 + 需要 GPU |
| 仅 OpenAI Provider | 2026-08-06 | 单点故障风险 |

---

## 被延期的设计

| 设计 | 延期时间 | 目标 Phase | 延期原因 |
|------|----------|------------|----------|
| 微服务拆分 | 2026-08-03 | Phase 4+ | 团队规模未达触发条件 |
| 移动端框架 | 2026-08-06 | Phase 3 | 非 Phase 1-3 交付物 |
| 本地 Embedding | 2026-08-06 | Phase 4 | 当前质量/成本不满足 |
| 插件热加载 | 2026-08-06 | Phase 3 | 非 Phase 1-2 需要 |
| 本地 Ollama Provider | 2026-08-06 | Phase 4 | 模型质量不足 |
| Schema Registry | 2026-08-06 | Phase 3 | 运维复杂度 |
| WASM 插件沙箱 | 2026-08-06 | Phase 5 | 技术不成熟 |

---

*Decision Log 持续更新。每次架构决策、否定、延期必须记录。*
