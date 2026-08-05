# DATABASE_RULES.md — AI Agent Quick Reference

> 完整数据库标准见: [docs/12-database-standard.md](../docs/12-database-standard.md)
> ER 图见: [docs/database/er-diagram.md](../docs/database/er-diagram.md)

## 速查铁律

- 所有查询参数化（禁止字符串拼接 SQL/Cypher）
- 禁止 `SELECT *`
- 大表查询必须有 LIMIT
- Schema 隔离：`content.* | knowledge.* | account.* | system.*`
- 软删除：只用 `deleted_at IS NULL`
- 每表必有：id(UUID) + created_at + updated_at + deleted_at + version
- 迁移工具：Alembic
