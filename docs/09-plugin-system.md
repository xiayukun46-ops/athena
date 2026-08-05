# 09 — Plugin System

> Athena 的插件系统。核心最小化，所有业务能力插件化。

**详细规范见**: [architecture/plugin-specification.md](architecture/plugin-specification.md)

---

## 为什么需要插件系统

### 核心问题: 如何支持 10 年的扩展？

**替代方案**: 所有功能硬编码在核心中。

不选理由：
- 5 年后出现新内容源（比如脑机接口新闻格式）→ 改核心代码 → 风险大
- 3 年后社区想贡献新 AI 模型 → 核心代码没有扩展点 → 无法贡献
- 10 年间核心膨胀 → 维护成本指数增长 → 没人敢改 → 项目死亡

**选择**: 核心只做路由、生命周期、依赖注入。所有业务能力通过插件接入。

### 插件化的代价

1. 初期开发更慢（需要设计接口 → 实现接口 → 测试接口）
2. 调试更复杂（插件在运行时加载）
3. 接口设计错误的影响更大（所有插件依赖接口）

但这些代价在 10 年尺度上是值得的。

---

## 五类插件

| 插件类型 | 接口 | 职责 | 示例 |
|----------|------|------|------|
| Source | `ISourcePlugin` | 数据源接入 | RSS, API, Scraper, Webhook |
| Processor | `IProcessorPlugin` | 内容处理 | HTML 清洗, NER, 翻译 |
| Storage | `IStoragePlugin` | 数据持久化 | PG, Neo4j, ES |
| AI | `IAIProviderPlugin` | AI 模型调用 | OpenAI, Anthropic, Ollama |
| UI | `IUIPlugin` | 界面组件 | 图谱可视化, 控制面板 |

---

## 插件生命周期

```
Register → Configure → Initialize → Activate → [Run] → Deactivate → Dispose

每个阶段有 Hook:
  on_register()     — 插件被发现和注册
  on_configure(cfg) — 加载用户配置
  on_init()         — 初始化资源（连接池、模型加载）
  on_activate()     — 标记为就绪
  on_deactivate()   — 优雅关闭
  on_dispose()      — 释放资源
```

### 为什么需要显式生命周期

**替代方案**: `__init__` + 直接使用。

不选理由：没有统一的初始化和清理机制。插件可能在用到时才初始化（延迟大），或者清除不掉（资源泄漏）。

---

## 插件清单 (plugin.json)

每个插件包含自描述的清单：

```json
{
  "name": "athena-source-rss",
  "version": "0.1.0",
  "type": "source",
  "entrypoint": "athena_source_rss.plugin:RSsSourcePlugin",
  "dependencies": {"athena-core": ">=0.1.0"},
  "config_schema": {
    "feed_url": {"type": "string", "format": "uri"},
    "poll_interval_seconds": {"type": "integer", "default": 300}
  },
  "capabilities": {
    "source_type": "rss",
    "content_types": ["article"]
  }
}
```

### 为什么用 JSON 而非代码注册

**替代方案**: Python 装饰器 `@register_plugin`。

不选理由：装饰器要求 Plugin Manager 启动前导入所有插件模块。JSON 清单可以在不加载代码的情况下发现插件，支持延迟加载。

---

## 依赖注入

插件通过 DI 容器获取依赖，不自己创建：

```python
# ✅ 正确: 依赖注入
class RssSourcePlugin(ISourcePlugin):
    def __init__(self, http_client: IHttpClient, cache: ICachePlugin):
        self.http_client = http_client
        self.cache = cache

# ❌ 错误: 自己创建
class RssSourcePlugin(ISourcePlugin):
    def __init__(self):
        self.http_client = aiohttp.ClientSession()  # 硬编码 + 资源泄漏
```

---

## 错误隔离

- 插件异常不传播到核心系统
- 同一插件连续失败 N 次 → 自动降级
- 错误通过事件总线报告

---

## 未来扩展

- **插件市场** (Phase 5): 中心化发现、安装、更新
- **沙箱执行** (Phase 5+): WASM / Docker 容器隔离
- **付费插件**: License 管理 + 计费

---

## 相关文档

- [10-agent-system.md](10-agent-system.md) — Agent 是 AI 类插件
- [07-architecture.md](07-architecture.md) — 插件在架构中的位置
- [architecture/plugin-specification.md](architecture/plugin-specification.md) — 完整接口定义
