# 10 — Agent System

> Athena 的 AI Agent 系统。Agent 是具备自主决策能力的 AI 实体。

**详细规范见**: [architecture/agent-specification.md](architecture/agent-specification.md)  
**Agent 定义示例**: [../.ai/agents/](../.ai/agents/)

---

## 什么是 Agent

Agent 不是一个 API 调用，而是一个**自主计算单元**：

- **目标导向**: 接收高层目标，自主规划步骤
- **工具使用**: 调用平台能力和外部工具
- **状态管理**: 维护执行上下文和中间结果
- **自我反思**: 评估结果，修正策略
- **人机协作**: 关键节点请求人类确认

---

## 为什么需要 Agent 系统

### 替代方案: 直接调用 LLM API

```python
response = openai.chat("extract entities from this text")
```

不选理由：
1. 无法处理长任务（一篇文章的实体提取 + 关系提取 + 摘要需要多次 LLM 调用）
2. 无法工具调用（Agent 需要查询知识图谱、搜索已有实体）
3. 无法错误恢复（LLM 返回格式错误怎么办？Agent 可以重试、换模型、请求人工）
4. 无法权限控制（不同 Agent 有不同的数据访问权限）

---

## Agent 架构

```
┌─────────────────────────────────────────┐
│               Agent Runtime              │
│                                          │
│  ┌─────────┐  ┌──────────┐  ┌────────┐  │
│  │ Planner │  │ Executor │  │Reflector│  │
│  └────┬────┘  └────┬─────┘  └───┬────┘  │
│       │            │             │       │
│  ┌────┴────────────┴─────────────┴────┐  │
│  │          Memory System             │  │
│  │  Working Memory + Episodic Memory  │  │
│  └────────────────────────────────────┘  │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │          Tool Registry             │  │
│  │  search_content, query_graph, ...  │  │
│  └────────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Planner（规划器）
接收目标 → 分解为步骤序列 → 分配给 Executor

### Executor（执行器）
按步骤调用工具 → 处理返回 → 记录结果

### Reflector（反思器）
评估步骤结果 → 决定继续 / 重规划 / 请求人工

### Memory
- Working Memory: 当前任务的上下文（短时记忆）
- Episodic Memory: 历史任务经验——"上次处理类似文章时，这个实体被链接到了 X"

---

## Agent 类型

| 类型 | 触发 | 示例 |
|------|------|------|
| System Agent | 自动（定时/事件驱动） | ContentIngestor, EntityResolver, TrendDetector |
| Personal Agent | 用户手动触发 | ResearchAssistant, DailyBriefing |
| Third-party Agent | 插件安装 | 社区贡献的专用 Agent |

---

## 工具系统

Agent 通过标准化工具接口与平台交互：

```python
class Tool:
    name: str              # "search_knowledge_graph"
    description: str       # 给 LLM 看的功能描述
    parameters: JSONSchema # 参数的 JSON Schema
    handler: Callable      # 实际执行函数
    required_permissions: list[Permission]
```

### 为什么需要工具白名单

**不控制**: Agent 可以调用任何 API。→ Prompt 注入攻击 → Agent 被诱导删除数据。

**控制**: 每个 Agent 声明自己需要的工具。运行时检查。不允许的工具调用被拒绝。

---

## Agent 安全

| 措施 | 说明 |
|------|------|
| 工具白名单 | Agent 只能调用声明的工具 |
| 沙箱执行 | Docker 容器隔离 |
| 网络白名单 | 只能访问声明的域名 |
| 资源限制 | CPU 2 vCore, Memory 4GB, Timeout 5min |
| 人工审批 | 删除、外部 API 写操作需审批 |
| 审计日志 | 所有操作全量记录 |

---

## 相关文档

- [06-knowledge-engine.md](06-knowledge-engine.md) — Agent 执行的知识处理
- [09-plugin-system.md](09-plugin-system.md) — Agent 是 AI 类插件
- [13-security.md](13-security.md) — Agent 安全详细设计
- [architecture/agent-specification.md](architecture/agent-specification.md) — 完整接口
