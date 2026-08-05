# AI Agent — Architecture Rules

> 编写 Athena 代码时必须遵守的架构约束。

---

## 模块边界

```
src/
  shared/         ← 共享内核，所有模块依赖它
  content/        ← Content Context
  knowledge/      ← Knowledge Context
  search/         ← Search Context
  ai/             ← AI Context
  user/           ← User Context
  plugin/         ← Plugin Manager
```

### 依赖规则

- `shared/` 不依赖任何模块
- `content/` 可依赖 `shared/`，不可依赖 `knowledge/` 或 `ai/`
- `knowledge/` 可依赖 `shared/`，不可依赖 `content/`（通过事件通信）
- 模块间只能通过 Domain Events 或 Plugin 接口通信

---

## 接口定义

所有跨模块依赖必须通过接口（抽象基类）：

```python
# ✅ 正确
class ContentIngestionService:
    def __init__(self, event_bus: IEventBus): ...

# ❌ 错误
class ContentIngestionService:
    def __init__(self, knowledge_service: KnowledgeService): ...
```

---

## 数据访问规则

- 每个上下文只能访问自己的 PostgreSQL Schema
- 不可跨 Schema JOIN 或直接读其他上下文的表
- 需要其他上下文的数据 → 通过 API 或事件获取副本

---

## 目录结构规则

```
src/{context}/
  domain/           # 领域模型、聚合根、值对象、领域服务
  application/      # 用例、应用服务、命令/查询
  infrastructure/   # 仓储实现、外部集成
  interfaces/       # API 路由、Schema、事件处理器
```

---

## 完整参考

- [docs/07-architecture.md](docs/07-architecture.md) — 架构总览
- [docs/04-domain-model.md](docs/04-domain-model.md) — 领域模型
- [docs/BLUEPRINT.md](docs/BLUEPRINT.md) — 完整施工蓝图
