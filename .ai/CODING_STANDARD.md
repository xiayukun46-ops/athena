# CODING_STANDARD.md

> Athena 编码规范。违反的代码在 Review 阶段被拒绝。

---

## Python

| 规则 | 标准 |
|------|------|
| 版本 | Python 3.12+ |
| 格式化 | `ruff format` |
| Lint | `ruff check` |
| 类型检查 | `mypy --strict` |
| 包管理 | `uv` |
| 测试 | `pytest` + `pytest-asyncio` + `pytest-cov` |
| 文档 | Google Style Docstring |

### 命名

| 元素 | 规范 | 示例 |
|------|------|------|
| 模块/文件 | snake_case | `entity_extractor.py` |
| 类 | PascalCase | `EntityExtractionService` |
| 函数/方法 | snake_case | `extract_entities()` |
| 变量 | snake_case | `article_count` |
| 常量 | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| 接口/抽象类 | I 前缀 | `IEventBus`, `ISourcePlugin` |
| 私有成员 | _ 前缀 | `_internal_method()` |

### 结构限制

| 限制 | 值 |
|------|-----|
| 文件最大行数 | 400 |
| 函数最大行数 | 30 |
| 类最大行数 | 200 |

### Import 顺序

```
1. 标准库 (os, json, datetime)
2. 第三方库 (fastapi, sqlalchemy)
3. 项目内部 (src.shared, src.content)
```

每组间空一行。组内按字母序。

---

## TypeScript

| 规则 | 标准 |
|------|------|
| 版本 | TypeScript 5.x, Node.js 22 LTS |
| 格式化 | `prettier` |
| Lint | `eslint` + `@typescript-eslint` |
| 类型检查 | `tsc --noEmit` |
| 包管理 | `pnpm` |
| 测试 | `vitest` |

---

## Git

### Branch

```
feature/{issue}-{描述}
bugfix/{issue}-{描述}
docs/{描述}
refactor/{描述}
```

### Commit (Conventional Commits)

```
feat(scope): description
fix(scope): description
docs(scope): description
test(scope): description
refactor(scope): description
chore(scope): description
```

### PR

- 标题符合 Conventional Commits
- 描述: What / Why / How
- 关联 Issue (`Closes #xxx`)
- 合并策略: Squash Merge

---

## 禁止事项

- `print()` / `console.log()` 调试语句
- 注释掉的代码块
- `except: pass` / `catch {}` 空异常
- 硬编码密钥 / Token / URL
- 字符串拼接 SQL / Cypher

---

## 完整参考

- [docs/governance/coding-standard.md](../docs/governance/coding-standard.md) — 完整编码规范
- [PROJECT.md](PROJECT.md) — 铁律
- [WORKFLOW.md](WORKFLOW.md) — 开发流程
