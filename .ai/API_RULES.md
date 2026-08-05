# AI Agent — API Rules

> Athena API 的开发规范。

---

## 铁律

1. **契约先行** — 先在 OpenAPI 3.1 定义，再写代码
2. **命名规范** — kebab-case URL, snake_case JSON keys
3. **版本化** — `/v1/`, `/v2/`, 旧版保留 ≥ 6 月
4. **标准响应格式** — `{data, _meta, _links}`
5. **所有写操作幂等** — POST 需 `X-Idempotency-Key`

---

## URL 模式

```
GET    /v1/{resource}           # 列表
GET    /v1/{resource}/{id}      # 详情
POST   /v1/{resource}           # 创建
PUT    /v1/{resource}/{id}      # 全量更新
DELETE /v1/{resource}/{id}      # 删除
```

---

## 响应格式

```json
{
  "data": { "id": "...", "type": "...", "attributes": {...} },
  "_meta": { "request_id": "...", "took_ms": 42 },
  "_links": { "self": "..." }
}
```

---

## AI 异步操作

返回 202 Accepted + task_id，客户端轮询：

```
POST /v1/ai/summarize → 202 {task_id}
GET  /v1/ai/tasks/{task_id} → 200 {status: "completed", output: ...}
```

---

## 完整参考

- [docs/11-api-style-guide.md](docs/11-api-style-guide.md) — API 风格指南
- [docs/api/api-design.md](docs/api/api-design.md) — 完整端点
- [docs/api/openapi.yaml](docs/api/openapi.yaml) — OpenAPI 定义
