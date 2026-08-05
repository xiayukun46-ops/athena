# Athena Monorepo

> Phase 1 — Core Infrastructure (目录骨架，禁止业务代码)

---

## 目录结构

```
athena/
├── apps/                    # 终端应用
│   ├── mobile/              # Flutter (Phase 4)
│   ├── desktop/             # Desktop App (Phase 5)
│   └── web/                 # Next.js (Phase 4)
│
├── packages/                # 共享库
│   ├── core/                # 核心抽象 (IPlugin, IEventBus, DI)
│   ├── knowledge/           # 知识模型 (Entity, Relation, Statement)
│   ├── event/               # 事件系统 (DomainEvent, EventBus impl)
│   ├── workflow/            # 工作流引擎 (Pipeline, Stages, Scheduler)
│   └── shared/              # 共享内核 (ID Types, Value Objects)
│
├── services/                # 后端服务
│   ├── collector/           # 内容采集服务
│   ├── knowledge-engine/    # 知识提取引擎
│   ├── search/              # 搜索服务
│   ├── graph/               # 图查询服务
│   └── api/                 # API Gateway
│
├── plugins/                 # 插件
│   └── official/            # 官方插件
│       ├── github/          # GitHub 内容源
│       ├── nature/          # Nature 论文源
│       ├── nasa/            # NASA 数据源
│       └── who/             # WHO 数据源
│
├── agents/                  # AI Agent 定义
│   ├── collector/           # 内容采集 Agent
│   ├── reasoner/            # 推理 Agent
│   ├── summarizer/          # 摘要 Agent
│   ├── timeline/            # 时间线 Agent
│   └── workspace/           # 工作空间 Agent
│
├── infrastructure/          # 基础设施
│   ├── docker/              # Docker 配置
│   ├── terraform/           # IaC
│   └── scripts/             # 运维脚本
│
├── docs/                    # 项目文档 (Phase 0)
├── .ai/                     # AI 规范 (Phase 0)
└── .github/                 # CI/CD (Phase 0)
```

---

## 命名规范

- 目录: kebab-case
- Python 包: snake_case
- 服务名: kebab-case
- 插件名: `athena-plugin-{category}-{name}`

---

## 当前状态

Phase 0 — Architecture Freeze。所有目录为占位骨架。禁止业务代码。

Phase 1 启动后，`packages/shared/` 和 `services/collector/` 将首先被填充。
