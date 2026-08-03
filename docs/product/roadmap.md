# Development Roadmap

## 概述

Athena Knowledge Platform 采用分阶段迭代开发策略。每个阶段有明确的目标、交付物和验收标准。

---

## Phase 0: Foundation（2026 Q3-Q4）—— 当前阶段

### 目标
建立项目治理体系、架构设计和技术选型，不做任何业务代码实现。

### 交付物

- [x] 项目宪法（[Project Constitution](../governance/constitution.md)）
- [x] 编码规范（[Coding Standard](../governance/coding-standard.md)）
- [x] 贡献指南（CONTRIBUTING.md）
- [x] ADR 模板与流程
- [x] RFC 模板与流程
- [x] 领域模型初稿
- [x] 架构总览
- [x] 插件规范
- [x] Agent 规范
- [x] API 风格指南
- [x] 数据库约定
- [x] CI/CD 工作流

### 不做什么

- 不写任何业务代码
- 不选型具体框架版本
- 不实现数据库

---

## Phase 1: Core Infrastructure（2026 Q4 - 2027 Q1）

### 目标
搭建核心基础设施，实现最小可运行骨架。

### 交付物

- 项目 Monorepo 搭建（Turborepo / Nx）
- 核心共享库（shared kernel）
- 数据库 Schema 初始化
- 消息队列基础设施
- API Gateway 骨架（路由、认证、限流）
- 日志 / 监控 / Tracing 基础设施
- Docker 化开发环境
- CI/CD 管道完善

### 不做什么

- 不实现业务功能
- 不做前端 UI

---

## Phase 2: Domain Core（2027 Q1 - Q2）

### 目标
实现核心领域模型和基础业务能力。

### 交付物

- 内容源接入框架（RSS, API, Web Scraping）
- 文章 / 文档领域模型
- 多语言文本处理管道
- 基础实体识别（NER）
- 知识图谱存储与查询
- 搜索基础设施（全文 + 向量）
- 基础 API（CRUD + 搜索）

---

## Phase 3: AI Integration（2027 Q2 - Q3）

### 目标
深度集成 AI 能力，实现智能理解与生成。

### 交付物

- Model Gateway（多模型路由）
- Prompt 管理平台
- RAG 管道（检索增强生成）
- 智能摘要生成
- 关系抽取与知识图谱增强
- 情感分析 / 立场检测
- AI 评测框架

---

## Phase 4: User Experience（2027 Q3 - Q4）

### 目标
构建面向终端用户的产品体验。

### 交付物

- Web 应用（Next.js）
- 移动端应用（Flutter，待 RFC 决策）
- 个性化推荐引擎
- 智能问答界面
- 知识仪表盘
- 消息推送

---

## Phase 5: Ecosystem（2028+）

### 目标
开放平台，构建开发者生态。

### 交付物

- 插件市场
- 公开 API
- 第三方集成（Slack, Notion, Obsidian）
- SDK（Python, TypeScript, Dart）
- 社区治理体系

---

## 长期展望（2029+）

- 实时知识图谱
- 多模态理解（图像、视频、音频）
- 自主 Agent 研究助手
- 去中心化知识网络
- 企业级私有部署方案

---

## 版本策略

- 采用语义化版本（SemVer）
- 主版本号代表重大架构变更
- Phase 0-1 不发布版本
- Phase 2 起发布 v0.x Alpha
- Phase 4 发布 v1.0 Beta
- Phase 5 发布 v1.0 GA

---

*本路线图每季度 Review 一次，根据实际情况调整优先级和排期。*
