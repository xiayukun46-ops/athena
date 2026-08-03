# Contributing to Athena

感谢你对 Athena Knowledge Platform 的关注！

本文档将指导你如何参与贡献，从提交 Issue 到合并 PR 的完整流程。

---

## 行为准则

本项目遵循 [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) 行为准则。参与即表示你同意遵守其条款。

---

## 贡献方式

### 报告 Bug

1. 在 [Issues](https://github.com/your-org/athena/issues) 中搜索是否已有相同问题
2. 使用 Bug Report 模板创建 Issue
3. 提供：复现步骤、期望行为、实际行为、环境信息

### 提出功能建议

1. 检查 [Roadmap](DEVELOPMENT_ROADMAP.md) 和已有 [RFCs](docs/rfc/)
2. 如果未覆盖，创建 Feature Request Issue
3. 重大功能需先通过 RFC 流程

### 提交代码

#### 第一步：找到或创建 Issue

所有代码变更必须关联 Issue。

#### 第二步：Fork & Branch

```bash
git checkout -b feature/{issue-number}-{brief-description}
```

#### 第三步：遵循编码规范

- 阅读 [CODING_STANDARD.md](CODING_STANDARD.md)
- 运行 Lint 和类型检查
- 编写测试

#### 第四步：提交 Commit

```bash
# 遵循 Conventional Commits
git commit -m "feat(domain): add KnowledgeNode entity"
```

提交前运行：

```bash
# Python
ruff check && ruff format && mypy src/ && pytest

# TypeScript
pnpm lint && pnpm typecheck && pnpm test
```

#### 第五步：创建 Pull Request

- 填写 PR 模板
- 描述 What / Why / How
- 关联 Issue（`Closes #123`）
- 请求 Review

---

## 开发环境

### 前置条件

- Python 3.12+
- Node.js 22 LTS
- Docker & Docker Compose
- uv（Python 包管理）
- pnpm（Node.js 包管理）

### 环境搭建

```bash
# 1. 克隆仓库
git clone https://github.com/your-org/athena.git
cd athena

# 2. Python 环境
uv sync

# 3. Node.js 环境
pnpm install

# 4. 启动依赖服务
docker compose up -d

# 5. 初始化数据库
uv run alembic upgrade head
```

---

## 代码审查标准

审查者将关注：

1. **架构一致性**：是否符合领域模型和架构约束
2. **代码质量**：命名、结构、注释是否清晰
3. **测试覆盖**：是否有充分的测试
4. **安全性**：是否有明显的安全问题
5. **性能**：是否有明显的性能隐患
6. **文档**：API 变更是否有对应文档更新

---

## DCO（Developer Certificate of Origin）

所有提交必须包含 Signed-off-by：

```
Signed-off-by: Your Name <your.email@example.com>
```

使用 `git commit -s` 自动添加。

---

## 沟通渠道

- **架构讨论**：[GitHub Discussions](https://github.com/your-org/athena/discussions)
- **日常交流**：待定（Slack / Discord）
- **RFC 评审**：[docs/rfc/](docs/rfc/)

---

*Athena 因你而更好。*
