# API Style Guide v1.0-draft

## 概述

Athena 采用 **API First** 设计原则。所有功能首先通过 API 契约定义，再实现后端逻辑。

---

## 1. API 设计原则

1. **契约优先**: OpenAPI 3.1 规范先行，后写代码
2. **面向资源**: RESTful 资源导向设计
3. **版本化**: URL 路径版本 (`/v1/`, `/v2/`)
4. **向后兼容**: 不破坏已有 API，废弃前提供迁移期
5. **自描述**: 响应包含 `_links` (HATEOAS) 和 `_meta`
6. **国际化**: 错误消息支持 i18n

---

## 2. URL 设计

### 2.1 基本模式

```
https://api.athena.ai/{version}/{resource}
```

### 2.2 资源命名

- 使用名词复数形式
- 使用 kebab-case
- 层级关系通过路径表达

```
GET    /v1/articles              # 文章列表
GET    /v1/articles/{id}          # 文章详情
POST   /v1/articles               # 创建文章
PUT    /v1/articles/{id}          # 更新文章（全量）
PATCH  /v1/articles/{id}          # 更新文章（部分）
DELETE /v1/articles/{id}          # 删除文章

GET    /v1/articles/{id}/comments # 文章评论
POST   /v1/articles/{id}/related  # 获取关联文章
```

### 2.3 特殊资源

```
# 搜索
GET /v1/search?q=AI&lang=zh&page=1&size=20

# 批量操作
POST /v1/articles/batch

# 图谱查询
POST /v1/graph/query

# AI 生成
POST /v1/ai/summarize
POST /v1/ai/translate
POST /v1/ai/chat
```

---

## 3. HTTP 方法语义

| 方法 | 语义 | 幂等 | 安全 |
|------|------|------|------|
| GET | 获取资源 | 是 | 是 |
| POST | 创建资源 / 执行操作 | 否 | 否 |
| PUT | 全量替换资源 | 是 | 否 |
| PATCH | 部分更新资源 | 否 | 否 |
| DELETE | 删除资源 | 是 | 否 |
| HEAD | 获取元信息 | 是 | 是 |
| OPTIONS | 获取支持的方法 | 是 | 是 |

---

## 4. 请求规范

### 4.1 Headers

```http
Authorization: Bearer {token}
Content-Type: application/json
Accept: application/json
Accept-Language: zh-CN
X-Request-ID: {uuid}
X-Idempotency-Key: {key}  # POST 幂等键
```

### 4.2 分页

使用 Cursor-based 分页（推荐）:

```http
GET /v1/articles?cursor={next_cursor}&limit=20
```

或 Offset-based 分页（简单场景）:

```http
GET /v1/articles?page=1&size=20
```

### 4.3 筛选与排序

```http
GET /v1/articles?status=published&lang=zh&sort=-published_at&limit=20
```

- `-` 前缀表示降序
- 多字段排序用 `,` 分隔

### 4.4 字段选择（Sparse Fieldsets）

```http
GET /v1/articles/123?fields=title,summary,published_at,author.name
```

---

## 5. 响应规范

### 5.1 成功响应

```json
{
  "data": {
    "id": "art_abc123",
    "type": "article",
    "attributes": {
      "title": "AI 发展的未来趋势",
      "summary": "...",
      "published_at": "2026-08-01T12:00:00Z"
    },
    "relationships": {
      "author": {
        "data": {"id": "usr_001", "type": "user"}
      },
      "tags": {
        "data": [
          {"id": "tag_ai", "type": "tag"},
          {"id": "tag_future", "type": "tag"}
        ]
      }
    },
    "_links": {
      "self": "/v1/articles/art_abc123",
      "author": "/v1/users/usr_001",
      "comments": "/v1/articles/art_abc123/comments"
    }
  },
  "_meta": {
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "took_ms": 42
  }
}
```

### 5.2 列表响应

```json
{
  "data": [...],
  "_meta": {
    "total": 1024,
    "page": 1,
    "size": 20,
    "next_cursor": "eyJpZCI6ImFydF8wMjAifQ=="
  },
  "_links": {
    "self": "/v1/articles?page=1&size=20",
    "next": "/v1/articles?cursor=eyJ...&size=20",
    "first": "/v1/articles?page=1&size=20",
    "last": "/v1/articles?page=52&size=20"
  }
}
```

### 5.3 错误响应

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Article not found",
    "details": [
      {
        "field": "id",
        "issue": "The article with id 'art_xxx' does not exist",
        "value": "art_xxx"
      }
    ]
  },
  "_meta": {
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "took_ms": 5
  }
}
```

### 5.4 HTTP 状态码

| 状态码 | 语义 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 202 | 已接受（异步处理） |
| 204 | 成功，无返回体 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 409 | 资源冲突 |
| 422 | 参数校验失败 |
| 429 | 请求限流 |
| 500 | 服务器内部错误 |
| 503 | 服务不可用 |

---

## 6. API 版本策略

### 6.1 版本号规则

- **主版本**: Breaking Change（URL 体现：`/v1/` → `/v2/`）
- **次版本**: 新增功能，兼容旧版
- **补丁版本**: Bug 修复

### 6.2 废弃流程

1. 标记 `Deprecated: true` + `Sunset: {date}` 在 OpenAPI 中
2. 响应头添加 `Deprecation: true` 和 `Sunset: Sat, 01 Jan 2027 00:00:00 GMT`
3. 至少保留 6 个月
4. 日志中记录调用方，主动通知

---

## 7. 安全规范

### 7.1 认证

- OAuth 2.0 + OpenID Connect
- API Key（服务间调用）
- JWT Bearer Token

### 7.2 限流

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1691026800
X-RateLimit-Retry-After: 30
```

### 7.3 CORS

生产环境严格限制 Origin 白名单。

---

## 8. 异步操作

长时间操作返回 202，提供状态查询端点：

```json
{
  "data": {
    "id": "job_abc123",
    "type": "async_job",
    "attributes": {
      "status": "processing",
      "created_at": "2026-08-03T10:00:00Z"
    },
    "_links": {
      "status": "/v1/jobs/job_abc123",
      "result": "/v1/articles/art_def456"
    }
  }
}
```

---

## 9. 文档与工具

- **OpenAPI 3.1**: API 定义源
- **Redoc / Scalar**: API 文档展示
- **Schemathesis**: 自动化 API 模糊测试
- **Postman Collection**: 开发者上手工具

---

*本指南将通过 RFC 流程持续演进。*
