# AI Agent — Database Rules

> 编写数据库相关代码时必须遵守的规则。

---

## 铁律

1. **所有查询必须参数化** — 禁止字符串拼接 SQL/Cypher
2. **禁止 `SELECT *`** — 明确列出列名
3. **大表查询必须有 LIMIT**
4. **Schema 隔离** — 每个上下文用独立 Schema (`content.*`, `knowledge.*`)
5. **禁止跨 Schema JOIN**
6. **软删除** — 只用 `deleted_at IS NULL` 过滤，不物理删除

---

## 每张表必须包含

```sql
id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
deleted_at  TIMESTAMPTZ,
version     INTEGER NOT NULL DEFAULT 1
```

---

## 命名

- 表: snake_case 复数 (`content.articles`)
- 列: snake_case (`published_at`)
- 布尔: `is_` 前缀 (`is_published`)
- 外键: `{entity}_id` (`source_id`)
- 约束: `pk_`, `fk_`, `uq_`, `ck_`, `ix_` 前缀
- 索引: `ix_{table}_{column}`

---

## 迁移

- 工具: Alembic
- 每次变更 → 独立迁移文件
- 迁移文件不可修改
- 必须包含 `upgrade()` 和 `downgrade()`

---

## 完整参考

- [docs/12-database-standard.md](docs/12-database-standard.md) — 数据库标准
- [docs/08-data-model.md](docs/08-data-model.md) — 数据模型
- [docs/database/er-diagram.md](docs/database/er-diagram.md) — 完整 ER 图
- [docs/guides/database-convention.md](docs/guides/database-convention.md) — 详细约定
