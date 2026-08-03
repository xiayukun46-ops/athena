# Agent Definitions

此目录存放 Agent 定义文件。

## 目录结构

```
agents/
├── system/        # 系统 Agent（平台自动管理）
│   ├── content-ingestor.yaml
│   ├── entity-resolver.yaml
│   └── ...
├── personal/      # 个人 Agent（用户创建）
│   └── research-assistant.yaml
└── README.md
```

## Agent 定义格式

参见 [AGENT_SPECIFICATION.md](../../AGENT_SPECIFICATION.md) 第 3 节。

## 约定

- Agent 定义使用 YAML 格式
- 文件名使用 kebab-case
- 每个 Agent 文件包含完整的配置（model, prompt, tools, permissions）
