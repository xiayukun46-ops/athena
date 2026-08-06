# Changelog

本文件记录 Athena 项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。
版本遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

---

## [Unreleased]

### Added (2026-08-06)
- Sprint 1 Planning 完成 (8 Issues, 38h 估计)
- GitHub 仓库创建并推送 (xiayukun46-ops/athena)
- DECISION_LOG.md 建立 (17 条决策记录)
- 项目定位升级: AI-Powered Global Knowledge Operating System
- Sprint 1 Board 建立 (ISS-001 ~ ISS-008)

### Added (2026-08-03 ~ 2026-08-06)
- Phase 0 Blueprint 完成 (16 编号文档 + 9 .ai/ 规范)
- M0.5 Architecture Consolidation (12 C4 图 + 8 RFC + Knowledge Canon + Workflow Engine)
- M0 Final Architecture Freeze (10 领域冻结 + Monorepo 骨架 + Phase 1 Plan)
- Phase 1 Knowledge Core 实现 (15 源文件, 39 tests, 0 框架依赖)

---

## [0.1.0-dev] — Phase 0 (2026-08-03 ~ 2026-08-06)

### Architecture
- Architecture Baseline 冻结 (10 个设计领域)
- C4 Model 完成 (12 张 Mermaid 图)
- DDD 战术设计完成 (6 个 Bounded Context)
- Knowledge Triangle 模型 (Entity → Relation → Statement)
- Event-driven 通信架构
- Plugin 系统设计 (5 类接口)
- Agent 系统设计

### Documentation
- 16 个编号核心文档 (00-15)
- 9 个 .ai/ 规范文件
- Knowledge Canon (13 知识对象唯一定义)
- Workflow Engine 规范 (12 阶段管道)
- Architecture Review #1 / #2
- Documentation as Code 标准

### Decisions
- ADR-001: 项目初始化 (Modular Monolith, Apache 2.0)
- ADR-002: Phase 0 审查批准
- RFC-001: 后端语言 Python FastAPI
- RFC-002: 消息队列 Redis Streams
- RFC-003: 前端 Next.js
- RFC-004: 搜索引擎 Elasticsearch
- RFC-005: 图数据库 Neo4j
- RFC-006: 移动端 Flutter (延后)
- RFC-007: Embedding OpenAI
- RFC-008: AI Provider 双策略
- RFC-009: 插件生命周期
- RFC-010: 版本管理

### Implementation
- athena_core 包 (identity, enums, base, metadata)
- athena_knowledge 包 (entity, relation, statement, quality, permission, lifecycle, workflow, events)
- 39 unit tests, all passing
