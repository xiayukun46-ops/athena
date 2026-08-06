# RISK_REGISTER — Risk Register

> 项目风险登记表。每季度 Review 更新。

---

## Active Risks

| ID | Risk | Probability | Impact | Mitigation | Owner | Status |
|----|------|:---:|:---:|------|-------|:---:|
| R1 | EAV 属性模型百万实体查询性能下降 | M | H | 物化视图 + JSONB 冗余 | Backend | Open |
| R2 | PG↔Neo4j 事件同步一致性断裂 | M | H | Outbox Pattern + Event Store 重放 | Infra | Open |
| R3 | AI 提取知识质量不可控 | H | H | Statement 审核流程 + 质量评分 | AI | Open |
| R4 | Statement 冲突解决策略未细化 | M | M | 仲裁规则定义 | Domain | Open |
| R5 | 文档体系与代码膨胀不一致 | M | M | 季度文档审计 | All | Open |
| R6 | 技术选型延迟 (4 RFCs 未 Approval) | L | M | 按优先级推进 RFC | Architect | Open |

## Resolved Risks

| ID | Risk | Resolution |
|----|------|------------|
| R0 | Phase 0 设计不完整 | All gaps identified in Review #2 |
