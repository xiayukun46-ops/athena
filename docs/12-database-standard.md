# 12 — Database Standard

> PostgreSQL 数据库设计、命名、迁移和运维规范。

**详细规范见**: [guides/database-convention.md](guides/database-convention.md)  
**物理模型见**: [database/er-diagram.md](database/er-diagram.md)

---

## 命名规范

### Schema
按限界上下文划分，物理隔离：

```sql
CREATE SCHEMA content;     -- 内容管理
CREATE SCHEMA knowledge;   -- 知识图谱
CREATE SCHEMA account;     -- 用户账户
CREATE SCHEMA system;      -- 系统管理
```

### 为什么需要 Schema 隔离

**替代方案**: 全部在 `public` schema 中。

不选理由：6 个上下文 13+ 张表混在 public 中 → 命名冲突、权限管理困难、未来拆分微服务时不好导出。

### 表

- snake_case 复数形式：`content.articles`, `knowledge.entities`
- 不使用数据库前缀（如 `tbl_articles`）——Schema 已经提供了命名空间

### 列

- snake_case
- 布尔：`is_` 前缀（`is_published`, `is_deleted`）
- 时间：`created_at`, `updated_at`, `deleted_at`, `published_at`
- 外键：`{entity}_id`（`source_id`, `author_id`）

### 为什么用 `deleted_at` 软删除

**替代方案**: 物理删除 `DELETE FROM`。

不选理由：
1. 数据不可恢复（误删无法回滚）
2. 无法审计（谁删了什么？）
3. 级联影响（文章删除后的实体关系链断裂）

软删除 + 定期归档（Phase 3+）是更好的策略。

### 约束命名

```sql
CONSTRAINT pk_articles PRIMARY KEY (id)
CONSTRAINT fk_articles_source FOREIGN KEY (source_id) REFERENCES content.sources(id)
CONSTRAINT uq_articles_url_hash UNIQUE (url_hash)
CONSTRAINT ck_articles_status CHECK (status IN ('...'))
CREATE INDEX ix_articles_published ON content.articles(published_at DESC);
```

---

## 必选字段

每张表必须包含：

```sql
id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
deleted_at  TIMESTAMPTZ,              -- 软删除
version     INTEGER NOT NULL DEFAULT 1 -- 乐观锁
```

### 为什么用 UUID 而非自增 ID

**替代方案**: `SERIAL` / `BIGSERIAL`。

不选理由：
1. 分布式不友好（多节点 ID 冲突）
2. 暴露数据量（`/articles/100000` 暴露了文章数）
3. UUID 在 Phase 4+ 的微服务场景下无需全局 ID 生成器

---

## 索引策略

1. 所有外键必建索引
2. WHERE 常用列建索引
3. ORDER BY 列建索引
4. 向量列使用 ivfflat (pgvector)
5. 全文搜索不在 PG 做——用 Elasticsearch

### 为什么不在 PG 做全文搜索

PG 的 `tsvector` 不支持专业分词（特别是 CJK），性能在百万级文档时下降明显。

---

## 迁移管理

- 工具: Alembic (Python)
- 每次 Schema 变更→独立迁移文件
- 迁移文件不可修改（只增不改）
- 生产环境先在 Staging 验证
- 大数据量表迁移需评估锁表时间

### 为什么用 Alembic 而非手动 SQL

**替代方案**: 手动管理 SQL 脚本。

不选理由：版本追踪、回滚、多环境同步全都需要自己实现。Alembic 有成熟的 autogenerate + 版本管理。

---

## 禁止事项

- ❌ 数据库级 ENUM（难变更，用 VARCHAR + CHECK）
- ❌ 数据库级外键级联删除（应用层控制更安全）
- ❌ Trigger（业务逻辑在应用层）
- ❌ 存储过程（维护困难，测试困难）
- ❌ `SELECT *`（明确列出列名）
- ❌ 大表无 LIMIT 的查询

---

## 相关文档

- [08-data-model.md](08-data-model.md) — 数据模型总览
- [11-api-style-guide.md](11-api-style-guide.md) — API 与 DB 的类型映射
- [database/er-diagram.md](database/er-diagram.md) — 完整 ER 图
- [guides/database-convention.md](guides/database-convention.md) — 完整规范
