# Project Constitution

## Preamble

本文档是 Athena Knowledge Platform（以下简称 "Athena" 或 "本项目"）的最高指导文件。
所有架构决策、代码实现、贡献行为均受本宪法约束。
本宪法优先于任何其他项目文档，仅在通过正式 RFC 流程后方可修订。

---

## Article I: Project Identity

Athena 是一个 **AI 驱动的全球知识平台**，旨在：

- 聚合、理解并结构化全球多语言信息
- 通过 AI 智能实现信息的深度理解、关联与洞察
- 为个人和组织提供可信、实时、个性化的知识服务
- 以开放架构支持十年以上的持续演进

**设计寿命**: 10+ 年
**目标用户**: 全球知识工作者、研究者、决策者
**技术愿景**: 成为知识管理领域的 Infrastructure

---

## Article II: Core Principles（核心原则）

以下八项原则按优先级排列，不可违背：

### P1. Documentation First（文档优先）
- 任何功能必须在设计文档完成后才能开始编码
- 文档与代码同步更新，CI 检查文档完整性
- 架构变更必须经过 ADR 流程

### P2. Architecture First（架构优先）
- 先定义接口、契约、数据流，后实现
- 每个模块必须有明确的边界和职责
- 引入新技术必须通过架构评审

### P3. Domain First（领域优先）
- 代码组织围绕领域模型而非技术分层
- 领域语言（Ubiquitous Language）统一贯穿代码与文档
- 领域模型独立于基础设施实现

### P4. API First（API 优先）
- 所有功能首先定义为 API 契约
- API 版本化，向后兼容至少两个大版本
- 外部集成统一通过 API Gateway

### P5. Plugin First（插件优先）
- 核心系统保持最小化，扩展能力通过插件实现
- 插件接口标准化，支持热加载
- 社区贡献以插件为主要形式

### P6. AI First（AI 优先）
- AI 不是功能附加，而是架构原生能力
- 数据管道天然支持 Embedding、RAG、Agent 工作流
- Prompt 管理、Model Routing、AI 评测作为一等公民

### P7. Test First（测试优先）
- TDD：先写测试，后写实现
- 覆盖率目标：核心域逻辑 >= 90%，应用层 >= 80%，基础设施层 >= 70%
- 集成测试覆盖所有 API 端点

### P8. Security First（安全优先）
- 零信任架构：默认不信任任何输入
- 数据加密：传输层 TLS 1.3，存储层 AES-256
- 每次 PR 必须通过安全扫描

---

## Article III: Architecture Governance

### 3.1 决策层级

| 层级 | 机制 | 适用范围 |
|------|------|----------|
| L0 | 本宪法 | 不可动摇的根本原则 |
| L1 | ADR (Architecture Decision Record) | 重大架构决策 |
| L2 | RFC (Request for Comments) | 功能设计、API 变更 |
| L3 | PR Review | 日常代码决策 |

### 3.2 ADR 流程

1. 提出者撰写 ADR 草案，放入 `docs/adr/`
2. 核心团队 Review，至少 2 人 Approve
3. ADR 以 Accepted / Rejected / Superseded 状态归档
4. 所有 ADR 编号连续，不可删除或重用

### 3.3 RFC 流程

1. 提出者撰写 RFC 草案，放入 `docs/rfc/`
2. 社区讨论周期 >= 7 天
3. 核心团队做出最终决策（Accept / Reject / Needs Revision）
4. 接受的 RFC 转化为 ADR 和实现任务

---

## Article IV: Quality Gates

以下门禁未通过则禁止合并：

1. **CI 全绿**：Lint + Type Check + Test + Build
2. **覆盖率不下降**：代码覆盖率相比 main 分支不得降低
3. **安全扫描通过**：无 High/Critical 漏洞
4. **至少 1 人 Approve**：核心团队成员 CR 通过
5. **文档更新**：相关文档已同步修改
6. **Commit 规范**：遵循 Conventional Commits

---

## Article V: Evolution Rules

### 5.1 宪法修订

- 修订提案需以 RFC 形式提交
- 需核心团队 >= 2/3 多数通过
- 修订后旧版本归档，保留完整历史

### 5.2 架构演进

- 每季度进行一次架构健康度评估
- 技术债务需在 ADR 中记录并设定偿还期限
- 废弃技术需有迁移计划，不可突然移除

### 5.3 向后兼容

- API 大版本更新需保留旧版本至少 6 个月
- 数据迁移需支持双写过渡期
- 插件接口变更需提供适配层

---

## Article VI: Community & Governance

### 6.1 角色

| 角色 | 职责 | 权限 |
|------|------|------|
| Maintainer | 项目方向决策、合并权限 | Write + Admin |
| Committer | 代码审查、文档维护 | Write |
| Contributor | 提交 PR、参与讨论 | Triage |

### 6.2 行为准则

本项目遵循 [Contributor Covenant](https://www.contributor-covenant.org/) 行为准则。

---

## Signed

本宪法自项目初始化之日起生效。

*Last revised: 2026-08-03*
