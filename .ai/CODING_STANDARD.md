# AI Agent — Coding Standard

> Athena 代码必须遵守的编写规范。违反的 PR 将被拒绝。

---

## Python 规范

- Python 3.12+, 格式化: `ruff format`, Lint: `ruff check`
- 类型检查: `mypy --strict`
- 依赖管理: `uv`
- 测试: `pytest` + `pytest-asyncio` + `pytest-cov`

### 命名

| 元素 | 规范 | 示例 |
|------|------|------|
| 模块 | snake_case | `entity_extractor.py` |
| 类 | PascalCase | `EntityExtractionService` |
| 函数 | snake_case | `extract_entities()` |
| 变量 | snake_case | `article_count` |
| 常量 | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| 接口/协议 | I 前缀 | `IEventBus` |

### 文件

- ≤ 400 行/文件, ≤ 30 行/函数, ≤ 200 行/类
- Import 顺序: 标准库 → 第三方 → 项目内部

### 文档

```python
def extract_entities(text: str, language: str = "auto") -> list[Entity]:
    """从文本中提取命名实体。

    Args:
        text: 待处理的原始文本。
        language: 文本语言代码，默认自动检测。

    Returns:
        提取到的实体列表。

    Raises:
        ValueError: 文本为空。
    """
```

---

## TypeScript 规范

- TypeScript 5.x, Node.js 22 LTS, 包管理: `pnpm`
- 格式化: `prettier`, Lint: `eslint`
- 测试: `vitest`

---

## Git 规范

### Commit: Conventional Commits

```
feat(domain): add KnowledgeEntity aggregate
fix(collector): handle RSS parse errors
docs(architecture): update data flow diagram
test(entity): add merge entity tests
```

### Branch

```
feature/{issue}-{brief}
bugfix/{issue}-{brief}
```

### PR

- 标题符合 Conventional Commits
- 描述: What / Why / How
- 关联 Issue

---

## 完整参考

- [docs/governance/coding-standard.md](docs/governance/coding-standard.md) — 完整编码规范
