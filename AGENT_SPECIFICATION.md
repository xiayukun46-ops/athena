# Agent Specification v1.0-draft

## 概述

Athena 将 AI Agent 视为一等公民。Agent 是具备自主决策能力的 AI 实体，能够在知识平台上执行复杂任务。

---

## 1. Agent 定义

Agent 是一个具有以下特征的自主计算单元：

- **目标导向**: 接收高层目标，自主规划执行步骤
- **工具使用**: 调用平台能力和外部工具完成任务
- **状态管理**: 维护执行上下文和中间状态
- **自我反思**: 评估执行结果，修正策略
- **人机协作**: 在关键节点请求人类确认或输入

---

## 2. Agent 架构

```
┌─────────────────────────────────────────┐
│               Agent Runtime              │
│                                          │
│  ┌─────────┐  ┌──────────┐  ┌────────┐  │
│  │ Planner │  │ Executor │  │ Reflee-│  │
│  │         │  │          │  │ ctor   │  │
│  └────┬────┘  └────┬─────┘  └───┬────┘  │
│       │            │             │       │
│  ┌────┴────────────┴─────────────┴────┐  │
│  │          Context / Memory          │  │
│  └────────────────────────────────────┘  │
│                                          │
│  ┌──────────────────────────────────┐    │
│  │          Tool Registry           │    │
│  └──────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

### 2.1 Planner（规划器）

接收任务，分解为可执行的步骤序列。

```python
class IPlanner:
    async def plan(self, goal: str, context: AgentContext) -> Plan: ...
    async def replan(self, plan: Plan, feedback: ExecutionFeedback) -> Plan: ...
```

### 2.2 Executor（执行器）

按计划调用工具，处理工具返回。

```python
class IExecutor:
    async def execute_step(self, step: PlanStep, context: AgentContext) -> StepResult: ...
    async def execute_plan(self, plan: Plan, context: AgentContext) -> PlanResult: ...
```

### 2.3 Reflector（反思器）

评估执行结果，决定是否重规划或继续。

```python
class IReflector:
    async def evaluate(self, step: PlanStep, result: StepResult) -> Evaluation: ...
    async def should_continue(self, plan: Plan, results: list[StepResult]) -> bool: ...
```

### 2.4 Memory（记忆系统）

管理短期和长期记忆。

```python
class IMemory:
    # Working Memory: 当前任务的上下文
    async def get_working(self, task_id: str) -> WorkingMemory: ...
    async def update_working(self, task_id: str, memory: WorkingMemory) -> None: ...
    
    # Episodic Memory: 历史任务经验
    async def store_episode(self, episode: Episode) -> None: ...
    async def retrieve_similar(self, task: Task, k: int) -> list[Episode]: ...
    
    # Semantic Memory: 长期知识
    async def store_knowledge(self, knowledge: Knowledge) -> None: ...
    async def query_knowledge(self, query: str) -> list[Knowledge]: ...
```

---

## 3. Agent 类型

### 3.1 System Agents（系统 Agent）

由平台管理，自动运行。

| Agent | 职责 |
|-------|------|
| ContentIngestor | 持续拉取和处理新内容 |
| EntityResolver | 实体链接与消歧 |
| KnowledgeCurator | 知识图谱质量维护 |
| TrendDetector | 热点检测与趋势分析 |
| QualityAuditor | 内容质量检查与去重 |

### 3.2 Personal Agents（个人 Agent）

由用户创建和管理。

```yaml
# .ai/agents/personal/research-assistant.yaml
name: "research-assistant"
type: personal
model: "gpt-5"
system_prompt: "你是一位研究助手，帮助用户... "
tools:
  - search_knowledge_graph
  - summarize_content
  - translate_text
schedule: null  # 手动触发
memory:
  working: true
  episodic: true
```

### 3.3 Third-party Agents（第三方 Agent）

通过插件系统接入的外部 Agent。

---

## 4. Tool System（工具系统）

Agent 通过标准化工具接口与平台交互：

```python
class Tool:
    name: str
    description: str
    parameters: JSONSchema
    handler: Callable[..., Any]
    
    # 权限控制
    required_permissions: list[Permission]
    
    # 工具类别
    category: ToolCategory  # data | action | external | ui
```

### 4.1 内置工具

| 工具 | 类别 | 说明 |
|------|------|------|
| `search_content` | data | 搜索知识库 |
| `query_graph` | data | 查询知识图谱 |
| `get_article` | data | 获取文章详情 |
| `summarize` | data | AI 摘要 |
| `translate` | data | 文本翻译 |
| `send_notification` | action | 发送通知 |
| `create_collection` | action | 创建收藏集 |
| `web_search` | external | 联网搜索 |
| `code_executor` | external | 代码执行 |

---

## 5. Agent 安全

### 5.1 权限模型

```
Agent → Permission Set → Tool Access
```

每个 Agent 有确定的权限范围，工具调用需权限检查。

### 5.2 沙箱执行

- Agent 代码在隔离沙箱中运行
- 网络访问白名单控制
- 资源使用（CPU/内存）有硬限制
- 所有工具调用记录审计日志

### 5.3 人工审批

- 高风险操作（删除、外部 API 写操作）需要人工审批
- 审批超时自动拒绝
- 审批记录持久化

---

## 6. Agent 协作

多个 Agent 可通过以下方式协作：

- **消息传递**: Agent 间异步消息通信
- **共享记忆**: 通过 Memory 系统共享上下文
- **工作流编排**: 定义 Agent 执行 DAG（Phase 3+）

```yaml
workflow:
  name: "daily-briefing"
  steps:
    - agent: ContentIngestor
      input: {sources: all}
    - agent: EntityResolver
      depends_on: [ContentIngestor]
    - agent: Summarizer
      depends_on: [EntityResolver]
    - agent: TrendDetector
      depends_on: [EntityResolver]
```

---

## 7. Agent 评测

每个 Agent 必须有评测方案：

- **单元评测**: 单个工具调用的准确性
- **任务评测**: 端到端任务完成质量
- **安全性评测**: 越狱、注入攻击抵抗能力
- **回归评测**: 版本升级后性能不退化

---

*本规范将通过 RFC 流程持续演进。*
