# AI Agent — Agent Protocol

> Athena AI Agent 的开发协议。

---

## Agent 定义

每个 Agent 使用 YAML 定义：

```yaml
name: agent-name
type: system | personal
schedule: "*/5 * * * *"  # 或 event-driven
model:
  provider: openai
  name: gpt-5-mini
tools:
  - search_knowledge_graph
  - create_entity
permissions:
  scope: [read:entities, write:entities]
  max_tokens_per_day: 500000
```

---

## 铁律

1. **工具白名单** — Agent 只能调用声明的 tools
2. **权限最小** — scope 只声明必需权限
3. **沙箱执行** — Docker 容器，CPU/Mem/Timeout 限制
4. **高风险操作需审批** — 删除、合并、外部写操作
5. **全量审计** — 所有 Agent 操作记录日志

---

## Agent 目录

```
.ai/agents/
  system/
    content-ingestor.yaml       # 内容接入
    entity-resolver.yaml        # 实体消歧
    knowledge-curator.yaml      # 知识维护
  personal/
    research-assistant.yaml     # 研究助手
```

---

## 完整参考

- [docs/10-agent-system.md](docs/10-agent-system.md) — Agent 系统设计
- [docs/architecture/agent-specification.md](docs/architecture/agent-specification.md) — 完整规范
