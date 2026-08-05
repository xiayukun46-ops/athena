# API_RULES.md — AI Agent Quick Reference

> 完整 API 设计见: [docs/11-api-style-guide.md](../docs/11-api-style-guide.md)
> OpenAPI 定义见: [docs/api/openapi.yaml](../docs/api/openapi.yaml)

## API 速查

- URL: kebab-case, 复数名词, /v1/ 前缀
- 响应: `{data, _meta, _links}` 格式
- 分页: Cursor-based（推荐）| Page-based
- AI 异步: 202 Accepted + task_id 轮询
- 版本: 旧版保留 ≥ 6 个月
- 认证: JWT (用户) | API Key (服务)
