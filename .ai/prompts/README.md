# Prompt Templates

此目录存放 Prompt 模板文件。

## 目录结构

```
prompts/
├── summarization/  # 摘要相关
├── translation/    # 翻译相关
├── extraction/     # 信息抽取相关
├── chat/           # 对话相关
└── README.md
```

## Prompt 模板格式

参见 [AGENT_SPECIFICATION.md](../docs/architecture/agent-specification.md) 第 5 节 PromptTemplate 实体。

## 约定

- 模板使用 Jinja2 语法
- 文件名使用 snake_case
- 每个模板包含版本号和评估基准
