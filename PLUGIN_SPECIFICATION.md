# Plugin Specification v1.0-draft

## 概述

Athena 采用 **插件优先 (Plugin First)** 架构。核心系统仅提供最小化的框架能力（路由、生命周期、依赖注入），所有业务功能均以插件形式实现。

---

## 1. 设计目标

- **可替换性**: 任何插件可被替换而不影响系统运行
- **可组合性**: 插件可依赖其他插件，形成能力组合
- **可发现性**: 插件声明自身能力，系统自动发现与注册
- **可隔离性**: 插件故障不影响核心系统和其他插件
- **热加载**: 插件可在运行时加载、卸载、更新（Phase 3+）

---

## 2. 插件类型

### 2.1 Source Plugin（数据源插件）

负责从外部获取原始内容。

**接口**:
```python
class ISourcePlugin(IPlugin):
    """内容源插件接口"""
    
    source_type: SourceType          # rss | api | scraper | push
    content_types: list[ContentType] # article | paper | social | report
    
    async def fetch(self, config: SourceConfig) -> AsyncIterator[RawContent]: ...
    async def validate_config(self, config: SourceConfig) -> bool: ...
    async def health_check(self) -> HealthStatus: ...
```

**示例**: RSS 订阅源、Twitter API、学术论文爬虫

### 2.2 Processor Plugin（处理器插件）

负责对内容进行转换和增强。

**接口**:
```python
class IProcessorPlugin(IPlugin):
    """内容处理器插件接口"""
    
    stage: PipelineStage  # preprocess | enrich | analyze | transform
    priority: int         # 同 Stage 内的执行优先级
    
    async def process(self, content: Content) -> Content: ...
    async def batch_process(self, contents: list[Content]) -> list[Content]: ...
```

**示例**: HTML 清洗、NER 实体提取、翻译、摘要生成

### 2.3 Storage Plugin（存储插件）

负责数据的持久化。

**接口**:
```python
class IStoragePlugin(IPlugin):
    """存储插件接口"""
    
    storage_type: StorageType  # relational | document | graph | vector | cache
    
    async def write(self, entity: Entity) -> str: ...
    async def read(self, id: str) -> Entity | None: ...
    async def query(self, query: Query) -> list[Entity]: ...
    async def delete(self, id: str) -> bool: ...
```

**示例**: PostgreSQL 存储、Elasticsearch 索引、Neo4j 图存储

### 2.4 AI Plugin（AI 插件）

负责 AI 模型调用和能力提供。

**接口**:
```python
class IAIProviderPlugin(IPlugin):
    """AI 提供商插件接口"""
    
    provider: str              # openai | anthropic | local
    capabilities: list[AICapability]  # chat | embedding | vision | audio
    
    async def chat(self, messages: list[Message], **kwargs) -> ChatResponse: ...
    async def embed(self, texts: list[str]) -> list[Embedding]: ...
    async def models(self) -> list[ModelInfo]: ...
```

**示例**: OpenAI GPT-5、Anthropic Claude、本地 Ollama

### 2.5 UI Plugin（界面插件）

负责提供用户交互界面。

**接口**:
```python
class IUIPlugin(IPlugin):
    """UI 插件接口"""
    
    ui_type: UIType  # web_panel | widget | dashboard | page
    
    def register_routes(self, router: APIRouter) -> None: ...
    def static_assets(self) -> Path: ...
```

**示例**: 知识图谱可视面板、AI 对话窗口

---

## 3. 插件清单 (Plugin Manifest)

每个插件必须包含 `plugin.json`：

```json
{
  "name": "athena-source-rss",
  "version": "0.1.0",
  "type": "source",
  "description": "RSS feed content source",
  "author": "Athena Team",
  "license": "Apache-2.0",
  "entrypoint": "athena_source_rss.plugin:RSsSourcePlugin",
  "dependencies": {
    "athena-core": ">=0.1.0"
  },
  "config_schema": {
    "type": "object",
    "properties": {
      "feed_url": {"type": "string", "format": "uri"},
      "poll_interval_seconds": {"type": "integer", "default": 300}
    },
    "required": ["feed_url"]
  },
  "capabilities": {
    "source_type": "rss",
    "content_types": ["article"]
  }
}
```

---

## 4. 插件生命周期

```
Register → Configure → Initialize → Activate → [Run] → Deactivate → Dispose
```

每个状态转换有对应的 Hook 方法：

| 状态转换 | Hook | 说明 |
|----------|------|------|
| Register | `on_register()` | 插件注册到系统 |
| Configure | `on_configure(config)` | 加载用户配置 |
| Initialize | `on_init()` | 初始化资源（连接池等） |
| Activate | `on_activate()` | 插件就绪 |
| Deactivate | `on_deactivate()` | 优雅关闭 |
| Dispose | `on_dispose()` | 释放资源 |

---

## 5. 依赖注入

插件通过 DI 容器获取依赖：

```python
class RssSourcePlugin(ISourcePlugin):
    def __init__(self, http_client: IHttpClient, cache: ICachePlugin):
        self.http_client = http_client
        self.cache = cache
```

DI 容器自动解析插件接口依赖，基于注册的插件类型匹配。

---

## 6. 错误隔离

- 每个插件运行在独立的错误边界内
- 插件异常不会传播到核心系统
- 插件连续失败 N 次自动降级
- 错误通过统一事件总线报告

---

## 7. 版本兼容

- 插件声明依赖的核心版本范围（`>=0.1.0, <1.0.0`）
- 主版本变更表示 Breaking Change
- 插件市场自动检查版本兼容性
- 支持多版本插件共存（不同插件使用不同版本依赖）

---

## 8. 未来扩展

- **插件市场**: 中心化的插件发现、安装、更新
- **沙箱执行**: 插件在隔离环境中运行（WASM / Docker）
- **插件组合**: 可视化编排多个插件的工作流
- **计费系统**: 付费插件的 License 管理

---

*本规范将通过 RFC 流程持续演进。*
