# RFC-001: 后端语言与框架选型

## Metadata

| 字段 | 内容 |
|------|------|
| RFC ID | RFC-001 |
| Title | 后端语言与框架选型 |
| Status | Draft |
| Author | AI Chief Architect |
| Created | 2026-08-03 |
| Target Phase | Phase 1 |
| Priority | P0 |

## Abstract

决定 Athena Knowledge Platform 后端服务的主要编程语言和 Web 框架。
候选方案为 Python (FastAPI)、Go、Rust。本 RFC 给出推荐决策及理由。

---

## Motivation

后端语言选型是 Phase 1 的第一个技术决策，影响后续所有模块的实现方式、性能上限、团队招聘、AI 生态兼容性。

### 选型维度

| 维度 | 权重 | 说明 |
|------|------|------|
| AI/ML 生态 | 40% | 与 LLM SDK、Embedding、Vector DB 的集成便利性 |
| 开发效率 | 25% | 团队上手速度、迭代速度 |
| 性能 | 15% | 并发能力、内存效率、冷启动速度 |
| 类型安全 | 10% | 编译期错误捕获、重构安全性 |
| 社区与人才 | 10% | 生态成熟度、招聘难度 |

---

## Proposal

### 推荐方案：Python 3.12 + FastAPI

**We will use Python 3.12 with FastAPI as the primary backend stack.**

### 理由

#### 1. AI/ML 生态优势（决定性因素）

Athena 是 **AI First** 平台。核心能力（RAG、NER、Entity Linking、Summarization）全部依赖 AI 模型。Python 拥有：

- **唯一的 LLM 一等公民生态**：OpenAI SDK、LangChain、LlamaIndex、HuggingFace Transformers 全部 Python-first
- **Embedding/Vector 原生支持**：sentence-transformers、pgvector Python binding
- **数据处理管线**：spaCy、NLTK、pandas 用于文本预处理
- **AI 评测框架**：大部分 ML 评测工具仅支持 Python

Go 和 Rust 的 AI SDK 均为社区移植，版本滞后，与 Athena 的 AI First 定义冲突。

#### 2. 开发效率与团队适配

- Python 学习曲线最低，团队组建快
- FastAPI 提供自动 OpenAPI 生成、Pydantic 类型验证、async/await 原生支持
- Type hints + mypy strict 模式弥补动态类型的不足
- `uv` 包管理器解决了历史 pip/poetry 的性能和锁定问题

#### 3. 性能足够

- FastAPI + uvicorn (uvloop) 单进程可处理 10k+ QPS（I/O bound）
- AI 调用的延迟瓶颈在网络 IO（LLM API），不在语言运行时
- CPU 密集型任务可下放到 Rust 插件或独立 Worker

#### 4. Modular Monolith 友好

- Python 的 import 机制天然支持模块边界
- 未来微服务拆分时，Python 转 Go/Rust 可按模块渐进迁移

---

## Alternatives Considered

### 方案 A：Python FastAPI ✅ 推荐

| 维度 | 评分 |
|------|------|
| AI/ML 生态 | ★★★★★ |
| 开发效率 | ★★★★★ |
| 性能 | ★★★☆☆ |
| 类型安全 | ★★★★☆ (mypy strict) |
| 社区人才 | ★★★★★ |

### 方案 B：Go

| 维度 | 评分 |
|------|------|
| AI/ML 生态 | ★★☆☆☆ (SDK 不全，版本滞后) |
| 开发效率 | ★★★★☆ |
| 性能 | ★★★★★ |
| 类型安全 | ★★★★☆ |
| 社区人才 | ★★★★☆ |

**不选原因**：Go 的 AI SDK 生态（如 `langchaingo`）远落后于 Python，与 AI First 原则冲突。Go 适合做基础设施层（API Gateway、消息队列 Worker），但不适合做 AI 密集型业务层。

### 方案 C：Rust

| 维度 | 评分 |
|------|------|
| AI/ML 生态 | ★☆☆☆☆ (极度匮乏) |
| 开发效率 | ★★☆☆☆ |
| 性能 | ★★★★★ |
| 类型安全 | ★★★★★ |
| 社区人才 | ★★★☆☆ |

**不选原因**：Rust 的 AI 生态几乎为空白。虽然性能最强，但开发效率和团队组建困难。Rust 适合做性能敏感的子组件（如 HTML 解析器、文本清洗），可通过 Python 绑定调用。

### 方案 D：混合方案（Python + Go/Rust）

**不选原因**：Phase 0-3 用 Modular Monolith，混合语言增加运维复杂度。Phase 4+ 拆分为微服务时自然支持混合语言。

---

## Impact Assessment

### Breaking Changes
无。这是首个技术选型决策。

### Performance
- Python GIL 限制 CPU 密集型任务的并行度
- **缓解**：CPU 密集型任务（NER 批处理）使用独立 Worker 进程或 Rust 插件
- AI 调用全部为 async IO-bound，GIL 不影响

### Security
- Python 依赖供应链攻击面较大（pip/PyPI）
- **缓解**：使用 `uv` 的锁文件 + `pip-audit` + Dependabot

### Testing
- pytest + pytest-asyncio + pytest-cov 已成熟
- mypy strict 模式覆盖类型安全
- ruff 覆盖 linting

---

## Open Questions

- [ ] 是否需要为部分热路径（HTML 解析、文本标准化）预研 Rust 插件方案？→ Phase 2 决定

## References

- [Architecture Overview](../architecture/overview.md) — 技术选型矩阵
- [Coding Standard](../governance/coding-standard.md) — Python 规范
- [ADR-001](../adr/ADR-001-project-init.md) — 项目初始化决策
