# ARCHITECTURE.md — AI Agent Quick Reference

> 完整架构设计见: [docs/07-architecture.md](../docs/07-architecture.md)
> 施工蓝图见: [docs/BLUEPRINT.md](../docs/BLUEPRINT.md)

## 架构速查

- **风格**: Modular Monolith（Phase 0-3）→ Microservices（Phase 4+）
- **分层**: Client → API Gateway → Application → Infrastructure
- **上下文**: Content | Knowledge | Search | AI | User | Plugin
- **通信**: Domain Events（Redis Streams）+ REST API + GraphQL
- **存储**: PG(Source of Truth) + Neo4j(Graph) + ES(Search) + Redis(Cache)

## 关键约束

- 跨上下文只通过事件通信，不直接调用
- 模块目录按 Bounded Context 组织（`src/content/` 非 `src/controllers/`）
- 新功能优先 Plugin 实现
