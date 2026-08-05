# AI Agent — Testing Standard

> Athena 测试编写规范。

---

## 铁律

1. **TDD** — 先写测试，后写实现
2. **覆盖率门槛** — 核心域 ≥ 90%, 应用层 ≥ 80%, 基础设施 ≥ 70%
3. **测试独立性** — 测试不依赖执行顺序
4. **外部依赖 Mock** — 单元测试不调用真实 API/DB

---

## 测试结构 (AAA)

```python
def test_extract_entities_success():
    # Arrange
    text = "Tim Cook is CEO of Apple."
    
    # Act
    result = extract_entities(text)
    
    # Assert
    assert len(result) == 2
    assert result[0].name == "Tim Cook"
```

---

## 测试分类

| 类型 | 工具 | 要求 |
|------|------|------|
| Unit | pytest | < 1ms, Mock 全部外部依赖 |
| Integration | pytest + Testcontainers | 真实 PG/Redis，< 100ms |
| E2E | Playwright / HTTP | 关键流程 ≤ 10 个，< 10s |
| AI Eval | 自定义框架 | Prompt 评测集，pass_rate ≥ 80% |

---

## 完整参考

- [docs/14-testing.md](docs/14-testing.md) — 测试策略
- [docs/guides/testing-strategy.md](docs/guides/testing-strategy.md) — 详细策略
