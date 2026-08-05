# 14 — Testing Strategy

> Athena 的测试策略、覆盖率目标和工具链。

**详细策略见**: [guides/testing-strategy.md](guides/testing-strategy.md)

---

## 测试金字塔

```
         ╱ E2E ╲          10% — 关键用户旅程
       ╱─────────╲
     ╱ Integration ╲      20% — API + 跨模块
   ╱─────────────────╲
 ╱    Unit Tests       ╲   70% — 领域逻辑
╱─────────────────────────╲
```

---

## 为什么是这个比例

**替代方案 1: 以 E2E 为主**（如 Cypress 全覆盖）。

不选理由：E2E 慢（分钟级）、不稳定（网络/环境）、维护成本高。E2E 测最关键的 10% 流程即可。

**替代方案 2: 只写 Unit Tests**。

不选理由：模块间集成问题 Unit Test 发现不了（如"事件格式变了但消费者没更新"）。

---

## 各层要求

### Unit Tests (70%)

- 每个领域方法 ≥ 1 Happy Path + 1 Edge Case
- Mock 全部外部依赖
- 执行时间 < 1ms/test

### Integration Tests (20%)

- API 端点全覆盖
- 事件处理全覆盖
- 使用 Testcontainers（真实 PG/Redis，测试实例）
- 执行时间 < 100ms/test

### E2E Tests (10%)

- 关键用户旅程 ≤ 10 个
- Playwright（前端）/ HTTP client（API）
- 执行时间 < 10s/scenario

---

## 覆盖率门禁

```
CI 检查:
  整体覆盖率下降 > 1% → 失败
  新增文件 < 70%      → 警告
  核心域 < 90%        → 失败
```

### 覆盖率目标

| 层级 | Phase 1 | Phase 2 | Phase 3+ |
|------|---------|---------|----------|
| 核心域 | 90% | 90% | 90% |
| 应用层 | 80% | 80% | 85% |
| 基础设施 | 70% | 70% | 75% |

---

## AI 测试

AI 输出不具确定性——传统 assert 不适用。

### Prompt 评测

每个 Prompt 模板有标准评测集：

```python
eval_cases = [
    {"input": "...", "expected_type": "PERSON", "expected_name": "Tim Cook"},
    {"input": "...", "expected_type": "ORGANIZATION", "min_confidence": 0.7},
]
result = evaluate(prompt_template, eval_cases)
assert result.pass_rate >= 0.80
```

### 模型回归

- 新模型版本 → 运行评测集
- 关键指标不下降 > 5%
- 人工抽检 50 条输出

---

## 测试基础设施

| 工具 | 用途 |
|------|------|
| pytest + pytest-asyncio | Python 测试 |
| vitest | TypeScript 测试 |
| Testcontainers | 集成测试基础设施 |
| factory_boy | 测试数据工厂 |
| Schemathesis | API 模糊测试 |
| Playwright | E2E 测试 |

---

## 禁止的反模式

- ❌ 测试依赖执行顺序
- ❌ 测试调用真实外部 API
- ❌ `time.sleep()` 等待
- ❌ Skip 不修复的失败测试
- ❌ 测试中有 `except: pass`

---

## 相关文档

- [02-constitution.md](02-constitution.md) — Test First 原则
- [07-architecture.md](07-architecture.md) — 集成测试场景
- [guides/testing-strategy.md](guides/testing-strategy.md) — 完整策略
