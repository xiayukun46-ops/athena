# TESTING_STANDARD.md — AI Agent Quick Reference

> 完整测试策略见: [docs/14-testing.md](../docs/14-testing.md)
> 详细指南见: [docs/guides/testing-strategy.md](../docs/guides/testing-strategy.md)

## 测试速查

- **TDD**: 先测试，后实现
- **金字塔**: Unit 70% | Integration 20% | E2E 10%
- **覆盖率**: 核心域 ≥ 90% | 应用层 ≥ 80% | 基础设施 ≥ 70%
- **工具**: pytest (Python) | vitest (TS) | Playwright (E2E)
- **AI 测试**: 评测集 + pass_rate ≥ 80%
