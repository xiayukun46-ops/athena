# AGENT_PROTOCOL.md — AI Agent Quick Reference

> 完整 Agent 系统设计见: [docs/10-agent-system.md](../docs/10-agent-system.md)
> 详细规范见: [docs/architecture/agent-specification.md](../docs/architecture/agent-specification.md)

## Agent 速查

- **架构**: Planner → Executor → Reflector + Working Memory + Episodic Memory
- **定义**: YAML（name, type, model, tools, permissions, schedule）
- **类型**: System Agent（自动）| Personal Agent（手动）| Third-party（插件）
- **安全**: 工具白名单 + Docker 沙箱 + 审批机制 + 审计日志
