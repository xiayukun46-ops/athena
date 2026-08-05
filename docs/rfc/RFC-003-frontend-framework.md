# RFC-003: Frontend Framework Selection

## Metadata

| 字段 | 值 |
|------|-----|
| RFC ID | RFC-003 |
| Status | Draft |
| Priority | P1 |
| Target Phase | Phase 4 |

---

## 1. Background

Phase 4 将构建面向终端用户的 Web 应用。当前 Phase 0 架构设计阶段，需要确定前端技术选型作为后续架构决策的输入。候选方案：Next.js（React 生态）和 Remix（Web Standard 优先）。

## 2. Problem

Web 前端是用户与知识图谱交互的主要界面。选择的前端框架需满足 Phase 4-5 的长期需求，影响 UI 组件库、路由设计、数据获取模式、SEO 策略、团队招聘。

## 3. Goals

- [ ] P0: 服务端渲染（SSR）支持 — Athena 的实体页面需要 SEO（每个实体是一个可被搜索引擎索引的页面）
- [ ] P0: 渐进式增强 — 核心功能在 JS 禁用时仍可用
- [ ] P1: 与 Python FastAPI 后端的集成便利性
- [ ] P1: 活跃的社区和组件生态
- [ ] P2: 开发者学习成本低

## 4. Non-goals

- 不在此 RFC 中决定 UI 组件库（Tailwind vs MUI vs shadcn）
- 不决定状态管理方案（留给 Phase 4 设计文档）
- 不评估 Svelte/Vue/Angular — 生态规模和招聘市场不支持

## 5. Proposal

**采用 Next.js 15 (App Router) 作为 Athena Web 前端框架。**

核心理由：
1. React 生态规模最大 — 组件库（shadcn/ui, Radix）、状态管理（TanStack）、数据获取（tRPC）选择最多
2. App Router 的 Server Components 天然适合知识浏览场景（大量只读内容，服务端渲染后发 HTML）
3. 文件系统路由 + 布局嵌套 = 实体详情页天然 SEO 友好
4. 与 Python FastAPI 的集成：通过 OpenAPI 生成 TypeScript 客户端（openapi-typescript），类型安全

## 6. Alternatives

| 方案 | 优点 | 缺点 | 为什么不选 |
|------|------|------|-----------|
| Next.js | React 生态最大；SSR/SSG/ISR 成熟；Vercel 支持 | App Router 学习曲线陡；部分 API 不稳定 | **采用** |
| Remix | Web Standard 优先；数据加载直观（loader/action） | 社区规模小（Next.js 的 1/10）；React 生态共享 | 生态不足以支撑 Phase 5 |
| Astro | 内容站点性能极致；多框架支持 | 不是 SPA 框架；交互性受限；不适合复杂 Web 应用 | 适合官网，不适合应用 |

## 7. Risks

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| Next.js 大版本 Breaking Change | 中 | 中 | 锁定主版本；升级前在 Staging 测试 |
| App Router 复杂性影响开发速度 | 中 | 低 | Phase 4 前团队完成 Next.js 培训 |

## 8. Future Evolution

Phase 4 先用 Pages Router（如果 App Router 不稳定）或直接用 App Router。
Phase 5 考虑将核心 UI 组件抽取为独立包供第三方使用。

**重新审视触发条件**: Next.js 16 发布后评估是否需要迁移。

## 9. References

- [Architecture Overview](../architecture/overview.md)
- [API Design](../api/api-design.md)
