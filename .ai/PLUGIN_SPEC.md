# PLUGIN_SPEC.md — AI Agent Quick Reference

> 完整插件系统设计见: [docs/09-plugin-system.md](../docs/09-plugin-system.md)
> 详细规范见: [docs/architecture/plugin-specification.md](../docs/architecture/plugin-specification.md)

## 五类插件

| 接口 | 方法 |
|------|------|
| ISourcePlugin | fetch(config) |
| IProcessorPlugin | process(content) |
| IStoragePlugin | write/read/query/delete |
| IAIProviderPlugin | chat/embed/models |
| IUIPlugin | register_routes |

## 速查

- 插件清单：plugin.json（name, version, type, entrypoint, dependencies, config_schema）
- 生命周期：Register → Configure → Init → Activate → Deactivate → Dispose
- 错误隔离：插件异常不传播到核心
