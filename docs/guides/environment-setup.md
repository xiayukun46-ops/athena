# Environment Setup Guide v1.0

## 概述

本文档指导开发者搭建 Athena 本地开发环境。

---

## 1. 系统要求

| 工具 | 版本 | 必需 | 说明 |
|------|------|------|------|
| Python | 3.12+ | 是 | 后端服务 |
| Node.js | 22 LTS | 是 | 前端 & Node 服务 |
| pnpm | 9.x | 是 | Node.js 包管理 |
| uv | 0.3+ | 是 | Python 包管理 |
| Docker | 26+ | 是 | 基础设施容器化 |
| Docker Compose | v2 | 是 | 多容器编排 |
| Git | 2.45+ | 是 | 版本控制 |
| VS Code | latest | 推荐 | IDE（含推荐插件） |

---

## 2. 快速开始

### 2.1 克隆仓库

```bash
git clone https://github.com/your-org/athena.git
cd athena
```

### 2.2 环境变量

```bash
cp .env.example .env
# 编辑 .env 填入本地配置
```

`.env.example`:
```bash
# Database
DATABASE_URL=postgresql+asyncpg://athena:athena@localhost:5432/athena_dev
DATABASE_TEST_URL=postgresql+asyncpg://athena:athena@localhost:5432/athena_test

# Redis
REDIS_URL=redis://localhost:6379/0

# Elasticsearch
ES_URL=http://localhost:9200

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=athenadev

# AI Providers (optional for development)
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx

# JWT
JWT_SECRET=dev-secret-change-in-production
JWT_ALGORITHM=HS256

# App
APP_ENV=development
LOG_LEVEL=debug
```

### 2.3 启动基础设施

```bash
docker compose up -d
```

服务列表:
- PostgreSQL 16 + pgvector (port 5432)
- Redis 7 (port 6379)
- Elasticsearch 8 (port 9200)
- Neo4j 5 (ports 7474, 7687)
- MinIO (ports 9000, 9001)

### 2.4 安装依赖

```bash
# Python
uv sync

# Node.js
pnpm install
```

### 2.5 初始化数据库

```bash
# 运行迁移
uv run alembic upgrade head

# (可选) 加载种子数据
uv run python scripts/seed.py
```

### 2.6 启动开发服务器

```bash
# 终端 1: 后端 API
uv run uvicorn src.main:app --reload --port 8000

# 终端 2: 前端 (Phase 4+)
pnpm dev --port 3000
```

### 2.7 验证

```bash
# 健康检查
curl http://localhost:8000/v1/health

# 预期响应
# {"status": "ok", "version": "0.1.0-dev"}
```

---

## 3. VS Code 配置

### 3.1 推荐插件

```json
{
  "recommendations": [
    "ms-python.python",
    "charliermarsh.ruff",
    "ms-python.mypy-type-checker",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "ms-azuretools.vscode-docker",
    "tamasfe.even-better-toml"
  ]
}
```

### 3.2 工作区设置

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit"
    }
  },
  "mypy-type-checker.args": ["--strict"],
  "python.testing.pytestEnabled": true
}
```

---

## 4. 常用命令

```bash
# ── Python ──
uv run ruff check .             # Lint 检查
uv run ruff format .            # 代码格式化
uv run mypy src/                # 类型检查
uv run pytest                   # 运行所有测试
uv run pytest --cov=src         # 带覆盖率
uv run pytest tests/unit/       # 仅单元测试
uv run pytest -m integration    # 仅集成测试

# ── Node.js ──
pnpm lint                       # ESLint
pnpm format                     # Prettier
pnpm typecheck                  # TypeScript 类型检查
pnpm test                       # 运行测试
pnpm test -- --coverage         # 带覆盖率

# ── Docker ──
docker compose up -d            # 启动基础设施
docker compose down             # 停止
docker compose logs -f          # 查看日志
docker compose ps               # 查看状态

# ── Database ──
uv run alembic upgrade head     # 运行迁移
uv run alembic downgrade -1     # 回滚一个版本
uv run alembic revision --autogenerate -m "description"  # 生成迁移
```

---

## 5. 故障排查

### PostgreSQL 连接失败

```bash
# 确认服务运行
docker compose ps postgres

# 检查端口
netstat -an | grep 5432

# 重置数据
docker compose down -v postgres
docker compose up -d postgres
```

### Python 依赖冲突

```bash
# 清理缓存
uv cache clean

# 重建虚拟环境
rm -rf .venv
uv sync
```

### Docker 资源不足

```bash
# 检查 Docker 资源使用
docker system df

# 清理未使用的资源
docker system prune -a --volumes
```

---

*环境配置随项目演进持续更新。Phase 1 加入更多自动化脚本。*
