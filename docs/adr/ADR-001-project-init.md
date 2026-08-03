# ADR-001: 项目架构初始化

## Status

Accepted

## Date

2026-08-03

## Context

Athena Knowledge Platform 从零开始建设，需要确立项目的基础架构、治理体系和开发规范。项目定位为 AI 驱动的全球知识平台，设计寿命 10 年以上。

## Decision

1. **项目治理**: 采用 Constitution + ADR + RFC 三级决策体系
2. **架构风格**: Phase 0-3 采用 Modular Monolith，为未来微服务拆分预留接口
3. **核心原则**: 确立八个优先原则（Documentation / Architecture / Domain / API / Plugin / AI / Test / Security First）
4. **许可协议**: Apache 2.0（含专利保护，对商业友好）
5. **技术选型目录**: 先定义候选方案，通过独立 RFC 做出最终决策
6. **插件架构**: 所有业务功能以插件形式实现，核心最小化
7. **AI 原生**: AI 能力作为架构原语，不是附加功能

## Alternatives Considered

| 方案 | 优点 | 缺点 | 结论 |
|------|------|------|------|
| 直接采用微服务 | 独立部署、团队自治 | Phase 0 过度设计，分布式复杂度高 | 不采用 |
| MIT 许可 | 简单宽松 | 缺少专利保护条款 | 不采用 |
| 传统 MVC 架构 | 开发速度快 | 不支撑 AI 原生的设计目标 | 不采用 |
| Monorepo | 统一版本管理 | 工具链复杂度 | 待 RFC-010 决策 |

## Consequences

### Positive
- 建立了清晰的项目治理和决策框架
- Modular Monolith 在早期平衡了开发效率和架构灵活性
- 插件架构支持未来生态扩展
- Apache 2.0 许可保护贡献者和使用者

### Negative
- 文档先行的开发方式初期速度较慢
- 过多的预先设计可能导致部分假设错误

### Mitigations
- 每季度架构 Review 纠正错误假设
- RFC 流程允许社区提出改进方案
- ADR 记录所有决策变更，保证可追溯

## References

- [PROJECT_CONSTITUTION.md](../governance/constitution.md)
- [Architecture Overview](../architecture/overview.md)
- [Domain Model](../domain/domain-model.md)
