# Database Convention v1.0-draft

## 概述

Athena 采用多数据库架构，不同数据类型使用最适合的存储引擎。本文档定义数据库设计、命名、迁移和运维约定。

---

## 1. 数据库选择矩阵

| 数据类型 | 存储引擎 | 选型理由 |
|----------|----------|----------|
| 核心业务数据 | PostgreSQL 16 | 成熟稳定，支持 JSON/GIN/GIST |
| 全文搜索 | Elasticsearch 8.x | 专业搜索引擎，多语言分词 |
| 向量存储 | pgvector / Qdrant | 向量相似度检索 |
| 图数据 | Neo4j / PostgreSQL AGE | 知识图谱原生存储 |
| 缓存 | Redis 7.x | 高性能 KV 缓存 |
| 消息队列 | Redis Streams / RabbitMQ | 异步任务调度 |
| 时序数据 | TimescaleDB | 监控指标存储 |
| 文件存储 | MinIO (S3-compatible) | 对象存储 |

---

## 2. 命名约定

### 2.1 数据库（PostgreSQL）

```sql
-- Schema: 按限界上下文划分
CREATE SCHEMA content;     -- 内容管理
CREATE SCHEMA knowledge;   -- 知识图谱
CREATE SCHEMA account;     -- 用户账户
CREATE SCHEMA analytics;   -- 数据分析
CREATE SCHEMA system;      -- 系统管理
```

### 2.2 表

- 使用 snake_case 复数形式
- Schema 前缀避免冲突

```sql
content.articles
content.sources
content.tags
knowledge.entities
knowledge.relations
account.users
account.api_keys
```

### 2.3 列

- snake_case
- 布尔列使用 `is_` 前缀：`is_published`, `is_deleted`
- 时间列：`created_at`, `updated_at`, `deleted_at`
- 外键：`{entity}_id`，如 `source_id`, `author_id`

### 2.4 约束

```sql
-- Primary Key: pk_{table}
CONSTRAINT pk_articles PRIMARY KEY (id)

-- Foreign Key: fk_{table}_{column}
CONSTRAINT fk_articles_source_id FOREIGN KEY (source_id) REFERENCES content.sources(id)

-- Unique: uq_{table}_{column}
CONSTRAINT uq_articles_url_hash UNIQUE (url_hash)

-- Check: ck_{table}_{rule}
CONSTRAINT ck_articles_status CHECK (status IN ('draft', 'published', 'archived'))

-- Index: ix_{table}_{column}
CREATE INDEX ix_articles_published_at ON content.articles(published_at DESC);
```

---

## 3. 表设计规范

### 3.1 必选字段

每张表必须包含：

```sql
CREATE TABLE content.articles (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at  TIMESTAMPTZ,              -- 软删除
    version     INTEGER NOT NULL DEFAULT 1 -- 乐观锁
);
```

### 3.2 数据类型选择

| 用途 | PostgreSQL 类型 | 说明 |
|------|----------------|------|
| 主键 | UUID | gen_random_uuid() |
| 短文本 | VARCHAR(n) | n ≤ 255 |
| 长文本 | TEXT | 无长度限制 |
| 整数 | INTEGER / BIGINT | 按需选择 |
| 小数 | NUMERIC(p, s) | 金额等精确小数 |
| 布尔 | BOOLEAN | 不用 TINYINT |
| 日期时间 | TIMESTAMPTZ | 始终带时区 |
| JSON | JSONB | 存储半结构化数据 |
| 数组 | TEXT[] / INTEGER[] | 简单列表 |
| 全文搜索 | TSVECTOR | PostgreSQL 全文搜索 |
| 向量 | vector(N) | pgvector 扩展 |

### 3.3 不使用

- `ENUM` 类型（难以变更，用 VARCHAR + CHECK 约束替代）
- 数据库级外键级联删除（应用层控制）
- Trigger（业务逻辑在应用层）
- 存储过程（维护困难）

---

## 4. 索引策略

### 4.1 索引原则

1. 所有外键建立索引
2. WHERE 条件常用列建立索引
3. ORDER BY 列建立索引
4. 复合索引遵循最左前缀原则
5. 避免冗余索引
6. 文本搜索使用 GIN 索引

### 4.2 索引命名

```
ix_{table}_{column1}_{column2}
pk_{table}
uq_{table}_{column}
fk_{table}_{ref_table}
```

---

## 5. 迁移管理

### 5.1 工具

- **Alembic** (Python) 或 **Atlas** (Go)
- 所有迁移脚本版本化，纳入 Git

### 5.2 迁移规则

1. 每次 Schema 变更有独立的迁移文件
2. 迁移文件不可修改（只能新增）
3. 迁移包含 `upgrade()` 和 `downgrade()`
4. 生产环境先在 Staging 验证
5. 大数据量表迁移需评估锁表时间

### 5.3 迁移文件命名

```
{alembic_revision}_{brief_description}.py
```

示例：
```
a1b2c3d4_add_articles_table.py
e5f6g7h8_add_fulltext_index.py
```

---

## 6. 查询规范

### 6.1 必须遵守

- 所有查询使用参数化，禁止字符串拼接
- SELECT 明确列出列名，禁止 `SELECT *`
- 大表查询必须有 LIMIT
- 使用 EXPLAIN ANALYZE 验证查询计划
- N+1 问题使用 JOIN 或 Batch Load

### 6.2 ORM 使用

- 优先使用 ORM（SQLAlchemy 2.0 / Prisma）
- 复杂查询使用原生 SQL 或 Query Builder
- ORM 生成的 SQL 需在日志中可审查

---

## 7. 备份与恢复

### 7.1 备份策略

| 频率 | 类型 | 保留 |
|------|------|------|
| 每小时 | WAL 归档 | 24h |
| 每日 | 全量备份 | 30 天 |
| 每周 | 异地备份 | 12 周 |
| 每月 | 归档备份 | 12 个月 |

### 7.2 恢复演练

- 每季度执行恢复演练
- RPO（恢复点目标）< 1 小时
- RTO（恢复时间目标）< 4 小时

---

## 8. 数据隐私

### 8.1 敏感数据

- PII（个人身份信息）加密存储
- 密码使用 bcrypt / argon2
- API Key 仅存储 Hash
- 日志中脱敏处理

### 8.2 数据保留

- 用户数据：账户存在期间
- 匿名化数据：永久
- 删除请求：30 天内彻底清除

---

*本约定将通过 RFC 流程持续演进。*
