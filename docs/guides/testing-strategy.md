# Testing Strategy v1.0

## 概述

Athena 遵循 **Test First** 原则。测试不是开发后的检查项，而是设计的驱动力。

---

## 1. 测试金字塔

```
                 ╱ E2E ╲          少量，关键用户旅程
               ╱─────────╲
             ╱ Integration ╲      中等量，API + 跨模块
           ╱─────────────────╲
         ╱    Unit Tests       ╲   最大量，领域逻辑
       ╱─────────────────────────╲
```

### 1.1 比例目标

| 层级 | 占比 | 覆盖率目标 |
|------|------|-----------|
| Unit | 70% | 核心域 ≥ 90%，应用层 ≥ 80%，基础设施 ≥ 70% |
| Integration | 20% | 所有 API 端点 ≥ 100%，事件处理 ≥ 80% |
| E2E | 10% | 关键用户旅程 100% |

---

## 2. 测试分类

### 2.1 Unit Tests

**范围**: 单个函数或方法，无外部依赖。

```python
# Python (pytest)
def test_extract_entities_returns_correct_count():
    text = "Tim Cook visited Beijing on Monday."
    result = extract_entities(text)
    assert len(result) == 2
    assert result[0].name == "Tim Cook"
    assert result[0].type == EntityType.PERSON

# TypeScript (vitest)
it("should return correct relation type for employment", () => {
    const relation = classifyRelation("works at", person, org);
    expect(relation.type).toBe(RelationType.WORKS_FOR);
});
```

**要求**:
- 每个领域方法至少 1 个 Happy Path + 1 个 Edge Case
- Mock 外部依赖（数据库、HTTP、AI）
- 执行时间 < 1ms per test

### 2.2 Integration Tests

**范围**: 多个组件协作，真实数据库/消息队列（测试实例）。

```python
# API 集成测试
@pytest.mark.integration
async def test_create_article_api():
    response = await client.post("/v1/articles", json={
        "source_id": "src_001",
        "url": "https://example.com/article/1",
        "title": "Test Article"
    })
    assert response.status_code == 201
    article = response.json()["data"]
    assert article["attributes"]["title"] == "Test Article"

# 事件处理集成测试
@pytest.mark.integration
async def test_article_fetched_triggers_entity_extraction():
    event = ArticleFetched(article_id=article.id, ...)
    await event_bus.publish(event)
    await asyncio.sleep(0.5)  # 等待异步处理
    statements = await statement_repo.find_by_article(article.id)
    assert len(statements) > 0
```

**要求**:
- 使用 Testcontainers 管理依赖（PG, Redis, ES 测试实例）
- 测试数据隔离（每个测试有独立的 Schema/DB）
- 执行时间 < 100ms per test

### 2.3 E2E Tests

**范围**: 完整用户流程，全栈环境。

```
场景: 用户搜索并阅读文章
  1. 用户登录
  2. 搜索 "AI protein folding"
  3. 点击搜索结果第一项
  4. 查看文章详情（含 AI 摘要）
  5. 点击 "关联实体" 跳转到实体详情页
  6. 收藏文章
```

**要求**:
- Playwright（前端 E2E）
- 关键流程不超过 10 个（保持可维护性）
- 执行时间 < 10s per scenario

### 2.4 专项测试

| 类型 | 工具 | 频率 |
|------|------|------|
| AI 评测 | 自定义 Evaluation Framework | 每次 Prompt 变更 |
| 安全扫描 | Trivy / Gitleaks / OWASP ZAP | 每次 PR |
| 性能测试 | k6 / Locust | 每 Sprint |
| 模糊测试 | Schemathesis (API) | 每日 |
| 快照测试 | Jest Snapshots (UI) | 每次 UI 变更 |

---

## 3. 测试基础设施

### 3.1 工具链

```
Python:
  pytest + pytest-cov + pytest-asyncio
  factory_boy / polyfactory (fixtures)
  respx / aioresponses (HTTP mock)

TypeScript:
  vitest + @vitest/coverage-v8
  msw (API mock)
  testing-library (React component)

E2E:
  Playwright
  Testcontainers (Python bindings)
```

### 3.2 CI 集成

```yaml
# .github/workflows/ci.yml (补充)
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg16
      redis:
        image: redis:7-alpine
    steps:
      - run: uv run pytest --cov=src --cov-report=xml
      - run: pnpm test -- --coverage
      - uses: codecov/codecov-action@v3
```

### 3.3 覆盖率门禁

```
CI 检查:
  - 整体覆盖率下降 > 1% → 失败
  - 新增文件覆盖率 < 70% → 警告
  - 核心域文件覆盖率 < 90% → 失败
```

---

## 4. 测试数据策略

### 4.1 Fixtures

```python
# 使用 Factory 生成测试数据
class ArticleFactory(factory.Factory):
    class Meta:
        model = Article
    
    id = factory.LazyFunction(uuid4)
    title = factory.Faker("sentence")
    url = factory.Faker("url")
    language = Language("en")
    status = ArticleStatus.DRAFT

# 在测试中使用
def test_publish_article():
    article = ArticleFactory(status=ArticleStatus.DRAFT)
    article.publish()
    assert article.status == ArticleStatus.PUBLISHED
```

### 4.2 测试隔离

```
策略: Test-per-Class 数据库隔离
实现: 
  - Integration: 每个 TestClass 创建独立 PostgreSQL Schema
  - Unit: 无持久化依赖
  - E2E: 每个 Scenario 使用独立测试用户
```

---

## 5. AI 测试

### 5.1 Prompt 评测

```python
class PromptEvaluation:
    """每次 Prompt 变更必须通过评测"""
    prompt_name: str
    test_cases: list[TestCase]
    pass_threshold: float = 0.8
    
    async def evaluate(self) -> EvalResult:
        """运行所有测试用例，计算通过率"""
```

### 5.2 模型回归测试

- 新模型版本上线前，运行标准评测集
- 关键指标不下降 5% 以上
- 人工抽检 50 条 AI 输出

---

## 6. 测试职责

| 角色 | 职责 |
|------|------|
| 开发者 | 编写 Unit + Integration 测试 |
| QA (Phase 4+) | E2E 场景设计、手动探索测试 |
| AI 工程师 | Prompt 评测、模型回归 |
| 安全工程师 | 安全扫描、渗透测试 |

---

## 7. 反模式（禁止）

- 测试依赖执行顺序
- 测试调用真实外部 API（除 E2E 白名单）
- `time.sleep()` 等待（用 `await` / `waitFor`）
- 测试中有未覆盖的异常分支
- 跳过失败测试而不修复

---

*测试策略每季度 Review，覆盖率目标和工具链随项目成熟度调整。*
