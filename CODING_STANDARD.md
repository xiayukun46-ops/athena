# Coding Standard

## 适用范围

本标准适用于 Athena Knowledge Platform 所有代码仓库，所有贡献者必须遵守。

---

## 1. 语言与框架约定

### 1.1 Python（后端服务）

- 版本：Python 3.12+
- 格式化：`ruff format`（替代 Black）
- Lint：`ruff check`（替代 flake8/isort/pylint）
- 类型检查：`mypy --strict`
- 依赖管理：`uv`（替代 pip/poetry）
- 测试框架：`pytest` + `pytest-cov`

### 1.2 TypeScript / JavaScript（前端 & Node.js 服务）

- 版本：TypeScript 5.x, Node.js 22 LTS
- 格式化：`prettier`
- Lint：`eslint` + `@typescript-eslint`
- 类型检查：`tsc --noEmit`
- 包管理：`pnpm`
- 测试框架：`vitest`

### 1.3 Flutter / Dart（移动端 & 桌面端，待定）

- 版本：Flutter 3.x Stable, Dart 3.x
- 格式化：`dart format`
- Lint：`flutter analyze`
- 状态管理：待 RFC 决策
- 测试：`flutter test`

---

## 2. 命名规范

| 元素 | 规范 | 示例 |
|------|------|------|
| Package / Module | snake_case | `knowledge_graph` |
| Class / Type | PascalCase | `KnowledgeNode` |
| Function / Method | snake_case | `extract_entities` |
| Variable | snake_case | `article_count` |
| Constant | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Interface / Protocol | PascalCase + I 前缀 | `IPlugin` |
| Abstract Class | PascalCase + Abstract 前缀 | `AbstractRepository` |
| File (Python) | snake_case | `entity_extractor.py` |
| File (TypeScript) | kebab-case | `entity-extractor.ts` |
| Database Table | snake_case, 复数 | `knowledge_nodes` |
| Database Column | snake_case | `created_at` |
| API Endpoint | kebab-case | `/api/v1/knowledge-graph` |
| Environment Variable | UPPER_SNAKE_CASE | `DATABASE_URL` |

---

## 3. 代码组织

### 3.1 目录结构（Python 后端）

```
src/
  {bounded_context}/
    domain/           # 领域模型、实体、值对象
    application/      # 用例、应用服务
    infrastructure/   # 数据库实现、外部集成
    interfaces/       # API 路由、Schema
    __init__.py
  shared/
    domain/           # 共享领域基类
    infrastructure/   # 共享基础设施
```

### 3.2 文件长度

- 单文件不超过 400 行
- 单函数不超过 30 行
- 单类不超过 200 行

### 3.3 Import 顺序（Python）

1. 标准库
2. 第三方库
3. 项目内部模块

每组之间空一行，组内按字母序排列。

---

## 4. 注释与文档

### 4.1 Docstring（Python）

使用 Google Style Docstring：

```python
def extract_entities(text: str, language: str = "auto") -> list[Entity]:
    """从文本中提取命名实体。

    Args:
        text: 待处理的原始文本。
        language: 文本语言代码，默认自动检测。

    Returns:
        提取到的实体列表，按置信度降序排列。

    Raises:
        ValueError: 文本为空或语言不支持。
    """
```

### 4.2 注释原则

- 注释解释 **Why**，代码说明 **What**
- 禁止注释掉的代码块（依赖 Git 历史）
- TODO 需关联 Issue：`# TODO(#123): 实现缓存层`

---

## 5. 错误处理

### 5.1 Python

- 使用自定义异常层次结构
- 绝不 `except Exception: pass`
- 领域异常继承自 `DomainError`
- 应用层异常继承自 `ApplicationError`

### 5.2 TypeScript

- 使用 `Result<T, E>` 模式处理可预期错误
- 不可恢复错误使用 Exception
- 禁止 `catch (e) {}` 静默吞异常

---

## 6. 测试规范

### 6.1 测试分类

| 类型 | 范围 | 速度 | 命名 |
|------|------|------|------|
| Unit | 单个函数/方法 | < 1ms | `test_{function}_{scenario}` |
| Integration | 多个组件交互 | < 100ms | `test_{feature}_integration` |
| E2E | 完整用户流程 | < 10s | `test_{user_journey}_e2e` |

### 6.2 测试结构

遵循 AAA 模式：Arrange → Act → Assert

```python
def test_extract_entities_returns_empty_on_blank_text():
    # Arrange
    text = ""
    
    # Act
    result = extract_entities(text)
    
    # Assert
    assert result == []
```

---

## 7. Git 规范

### 7.1 Branch 命名

```
feature/{issue}-{简要描述}
bugfix/{issue}-{简要描述}
docs/{简要描述}
refactor/{简要描述}
```

### 7.2 Commit Message

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

类型：`feat` | `fix` | `docs` | `style` | `refactor` | `test` | `chore` | `perf` | `ci`

### 7.3 PR 要求

- PR 标题与 Commit 规范一致
- 描述包含：What / Why / How / Testing
- 关联 Issue
- 合并策略：Squash Merge

---

## 8. 安全编码

### 8.1 输入验证

- 所有外部输入在边界处验证
- 使用 Pydantic / Zod 进行 Schema 验证
- SQL 使用参数化查询，禁止字符串拼接

### 8.2 密钥管理

- 禁止硬编码密钥、Token、密码
- 开发环境使用 `.env`（已加入 .gitignore）
- 生产环境使用 Secret Manager

### 8.3 依赖安全

- CI 中集成 `pip-audit` / `npm audit`
- Dependabot 自动提交依赖更新 PR
- 定期审查依赖许可证兼容性

---

## 参考文献

- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
