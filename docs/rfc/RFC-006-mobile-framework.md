# RFC-006: Mobile Framework Selection

## Metadata

| 字段 | 值 |
|------|-----|
| RFC ID | RFC-006 |
| Status | Draft |
| Priority | P2 |
| Target Phase | Phase 4 |

---

## 1. Background

Phase 4 可能需要移动端应用。候选方案：Flutter 和 React Native。此决策可延后至 Phase 3 末。

## 2. Problem

移动端不是 Athena 的核心交付物。Web App 是主界面。但移动端的便利性（推送通知、离线浏览）对知识工作者有价值。

## 3. Goals

- [ ] P2: 跨平台（iOS + Android）代码复用 ≥ 90%
- [ ] P2: 与 Python 后端 + REST API 的集成
- [ ] P2: 开发效率

## 4. Non-goals

- 不在此阶段做最终决策（留给 Phase 3 RFC）
- 不评估原生开发（Swift + Kotlin）— 不符合团队资源和跨平台需求

## 5. Proposal

**暂定 Flutter 为移动端方案。Phase 3 末重新评估确认。**

暂定理由：Dart 类型安全 + 高性能渲染 + 单一代码库。与 Python 后端的集成通过 REST API（不需要 SDK 语言一致）。

## 6. Alternatives

| 方案 | 优点 | 缺点 | 结论 |
|------|------|------|------|
| **Flutter** | 性能好；Dart 类型安全 | Dart 学习成本；社区 < React Native | 暂定 |
| React Native | React 生态；Web 前端技能复用 | 性能不如 Flutter；原生桥接开销 | 如果 Web 用 React/Next.js，团队技能复用优势明显 |
| PWA | 零安装；Web 技能复用 | iOS 推送受限；离线能力弱 | 不适合"知识工作者工具"定位 |

## 7. Future Evolution

Phase 3 末基于以下条件最终决定：
- Web 前端团队规模和技能栈
- 移动端用户需求的明确程度
- Flutter 和 React Native 的版本成熟度

---

## 8. References

- [Product Strategy](../01-product-strategy.md)
- [API Design](../api/api-design.md)
