# WORKFLOW.md

> Athena 开发工作流。从接到任务到合并 PR 的完整流程。

---

## 1. 任务启动

收到任务后，按以下步骤启动：

```
1. 阅读 MASTER.md — 确认理解项目法则
2. 阅读 docs/TASK-TREE.md — 确认任务在任务树中
3. 阅读相关设计文档 — 理解当前架构和约束
4. 确认前置条件已满足 — 依赖的 ADR/RFC 是否已 Approved
```

**不跳过任何一步。**

---

## 2. 设计阶段

所有功能实现前必须完成设计文档：

```
小型变更 (< 200 行)     → 不需要 ADR/RFC，但需要写设计注释
中型变更 (200-1000 行)  → 写 RFC（docs/rfc/）
大型变更 (> 1000 行)    → 写 ADR（docs/adr/）
架构变更                → 必须 ADR，≥ 2 人 Approve
```

**设计文档必须遵循九章结构**（见 [DOC_TEMPLATE.md](DOC_TEMPLATE.md)）。

---

## 3. 实现阶段

设计文档 Approved 后进入实现：

```
1. 创建 Branch
   feature/{issue}-{描述}
   bugfix/{issue}-{描述}

2. 写测试（TDD）
   pytest / vitest
   先写测试 → 确认失败 → 写实现 → 确认通过

3. 写实现
   遵守 Coding Standard
   遵守架构边界
   跨模块只通过接口/事件

4. 本地验证
   ruff check + ruff format
   mypy --strict / tsc --noEmit
   pytest / vitest
```

---

## 4. 提交阶段

```
1. Commit
   遵循 Conventional Commits
   feat(domain): ...
   fix(collector): ...
   docs(architecture): ...

2. 自检
   对照 REVIEW_PROCESS.md 检查清单逐项确认

3. Push + PR
   PR 标题: Conventional Commits 格式
   PR 描述: What / Why / How
   关联 Issue (Closes #xxx)
```

---

## 5. 审查阶段

```
1. CI 自动检查
   Lint + Type Check + Test + Coverage + Security

2. Reviewer 审查
   至少 1 人 Approve

3. 修改（如需）
   不通过 → 修改 → 重新提交
   循环直到通过

4. 合并
   Squash Merge 到 main
```

---

## 6. 完成阶段

合并后：

```
1. 更新 TASK-TREE.md — 标记任务完成
2. 更新相关文档 — 如有设计变更
3. 关闭关联 Issue
```

---

## 禁止事项

- 跳过设计阶段直接写代码
- 跨上下文直接调用（绕过事件/接口）
- 提交未通过 CI 的代码
- 在 main 分支直接开发
- 跳过测试

---

## 相关文件

- [PROJECT.md](PROJECT.md) — 铁律
- [REVIEW_PROCESS.md](REVIEW_PROCESS.md) — 审查清单
- [CODING_STANDARD.md](CODING_STANDARD.md) — 编码规范
- [DOC_TEMPLATE.md](DOC_TEMPLATE.md) — 文档模板
