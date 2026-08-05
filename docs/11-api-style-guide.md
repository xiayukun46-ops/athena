# 11 — API Style Guide

> Athena API 的设计规范和约定。

**详细指南见**: [guides/api-style-guide.md](guides/api-style-guide.md)  
**OpenAPI 定义**: [api/openapi.yaml](api/openapi.yaml)

---

## 核心原则

1. **契约优先**: OpenAPI 3.1 先于代码
2. **面向资源**: RESTful 资源导向
3. **版本化**: URL 路径版本 `/v1/`, `/v2/`
4. **向后兼容**: 旧版本保留 ≥ 6 个月
5. **自描述**: 响应包含 `_links` (HATEOAS) + `_meta`

---

## URL 设计

```
标准 CRUD:
GET    /v1/articles              # 列表
GET    /v1/articles/{id}         # 详情
POST   /v1/articles              # 创建
PUT    /v1/articles/{id}         # 全量更新
PATCH  /v1/articles/{id}         # 部分更新
DELETE /v1/articles/{id}         # 删除

子资源:
GET    /v1/articles/{id}/related  # 关联文章
GET    /v1/articles/{id}/entities # 文章中的实体

动作:
POST   /v1/sources/{id}/fetch     # 手动触发抓取
POST   /v1/ai/chat                # AI 问答
```

### 为什么用 kebab-case 而非 camelCase

URL 大小写不敏感，kebab-case 可读性最好。`/knowledge-graph` > `/knowledgeGraph` > `/knowledge_graph`。

---

## 请求规范

### 分页

使用 Cursor-based（推荐）或 Page-based：

```http
GET /v1/articles?cursor=eyJ...&limit=20
GET /v1/articles?page=1&size=20
```

### 筛选

```http
GET /v1/articles?status=published&language=zh&sort=-published_at
```

`-` 前缀表示降序。

### 稀疏字段

```http
GET /v1/articles/123?fields=title,summary,published_at
```

### 为什么需要稀疏字段

减少响应体积。移动端可能只需要 title + summary，不需要全文。

---

## 响应规范

### 成功（单条）

```json
{
  "data": {
    "id": "art_abc123",
    "type": "article",
    "attributes": { "title": "...", "summary": "..." },
    "relationships": {
      "source": { "data": { "id": "src_001", "type": "source" } }
    }
  },
  "_meta": { "request_id": "...", "took_ms": 42 },
  "_links": { "self": "/v1/articles/art_abc123" }
}
```

### 为什么用 JSON:API 风格

**替代方案**: 简单包装 `{articles: [...]}`。

不选理由：缺少 `type` 字段（多态响应不好解析）、缺少 `relationships`（关联数据需要额外请求）、缺少 `_links`（HATEOAS）。

### 列表

```json
{
  "data": [...],
  "_meta": { "total": 1024, "page": 1, "size": 20, "next_cursor": "..." },
  "_links": { "self": "...", "next": "..." }
}
```

### 错误

```json
{
  "error": {
    "code": "ENTITY_NOT_FOUND",
    "message": "The requested entity could not be found.",
    "details": [{ "field": "id", "issue": "Entity ent_xxx does not exist" }]
  },
  "_meta": { "request_id": "..." }
}
```

### HTTP 状态码约定

| 状态码 | 语义 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 202 | 已接受（异步处理——AI 任务） |
| 204 | 成功，无响应体 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 409 | 冲突 |
| 422 | 参数校验失败 |
| 429 | 限流 |

---

## 异步操作

AI 任务（Summarize, Translate, Extract）返回 202：

```json
{
  "data": {
    "task_id": "tsk_xyz789",
    "status": "pending",
    "_links": { "status": "/v1/ai/tasks/tsk_xyz789" }
  }
}
```

轮询 `GET /v1/ai/tasks/{task_id}` 直到完成。

---

## 版本策略

- 主版本（Breaking）→ URL 体现：`/v1/` → `/v2/`
- 旧版本保留 ≥ 6 个月
- 废弃 API 先在 OpenAPI 标记 `deprecated: true`，响应头加 `Deprecation` + `Sunset`

---

## 相关文档

- [07-architecture.md](07-architecture.md) — API 在架构中的位置
- [12-database-standard.md](12-database-standard.md) — 数据库与 API 的类型映射
- [api/api-design.md](api/api-design.md) — 完整端点定义
- [api/openapi.yaml](api/openapi.yaml) — OpenAPI 3.1 骨架
