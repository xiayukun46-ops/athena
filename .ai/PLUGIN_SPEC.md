# AI Agent — Plugin Rules

> Athena 插件系统的开发规范。

---

## 铁律

1. **新功能默认插件化** — 除非是核心框架能力，否则作为 Plugin 实现
2. **遵守 Plugin 接口** — 不绕过 `IPlugin` 直接调用
3. **含 plugin.json** — 每个插件必须有自描述的清单文件
4. **错误不传播** — 插件异常不影响核心系统

---

## 五类插件接口

| 接口 | 实现方法 |
|------|----------|
| `ISourcePlugin` | `fetch(config) → list[RawContent]` |
| `IProcessorPlugin` | `process(content) → Content` |
| `IStoragePlugin` | `write/read/query/delete` |
| `IAIProviderPlugin` | `chat/embed/models` |
| `IUIPlugin` | `register_routes/static_assets` |

---

## 插件清单模板

```json
{
  "name": "athena-{type}-{name}",
  "version": "0.1.0",
  "type": "source|processor|storage|ai|ui",
  "entrypoint": "package.module:ClassName",
  "dependencies": {"athena-core": ">=0.1.0"},
  "config_schema": {},
  "capabilities": {}
}
```

---

## 完整参考

- [docs/09-plugin-system.md](docs/09-plugin-system.md) — 插件系统设计
- [docs/architecture/plugin-specification.md](docs/architecture/plugin-specification.md) — 完整接口
