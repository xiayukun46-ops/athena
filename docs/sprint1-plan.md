# Sprint 1 — Knowledge Core

> Sprint 名称: Knowledge Core
> 周期: Week 1-2 (Phase 1)
> 状态: Planning
> 计划日期: 2026-08-06

---

## 1. Sprint Goal

交付 Athena 最核心的领域层——Knowledge Core 包。完成 Knowledge Canon 中定义的全部知识对象、事件、工作流、权限模型的纯 Python 实现。100% 类型安全、100% 单元测试覆盖、零框架依赖。所有未来模块依赖此包。

---

## 2. Sprint Scope

### In Scope

- `packages/core/src/athena_core/` — 共享基础类型（identity, enums, base, metadata）
- `packages/knowledge/src/athena_knowledge/` — 知识领域模型（entity, relation, statement, quality, permission, lifecycle, workflow, events）
- 序列化层（to_dict / from_dict）— 所有领域对象支持 JSON 互转
- 领域验证层（Domain Validator）— 跨聚合根的一致性校验
- 单元测试 — 100% 覆盖所有公开方法和边界条件
- 包配置 — pyproject.toml, 类型标记

### Partial (当前已完成)

| 模块 | 状态 | 说明 |
|------|:---:|------|
| identity.py | ✅ | 9 个类型化 ID |
| enums.py | ✅ | 20+ StrEnum |
| base.py | ✅ | AggregateRoot, Entity, ValueObject, DomainEvent |
| metadata.py | ✅ | StandardMetadata |
| entity.py | ✅ | KnowledgeEntity + 值对象 |
| relation.py | ✅ | KnowledgeRelation |
| statement.py | ✅ | Statement + StatementSource |
| quality.py | ✅ | QualityScore 六维算法 |
| permission.py | ✅ | 四级预设权限 |
| lifecycle.py | ✅ | 6 个状态机 |
| workflow.py | ✅ | RetryPolicy, WorkflowContext |
| events.py | ✅ | 10 个领域事件 |
| tests | ✅ | 39 tests passing |

---

## 3. Out of Scope

- 数据库代码（Alembic, SQLAlchemy）— Sprint 1 仅领域层
- HTTP API（FastAPI Router）— Sprint 5
- 内容采集（Collector Service）— Sprint 3-4
- AI 集成 — Phase 2
- 搜索 — Phase 2
- 图数据库同步 — Phase 2
- 前端 UI — Phase 4

---

## 4. Deliverables

| # | 交付物 | 文件 |
|---|--------|------|
| D1 | athena_core 完成 | `packages/core/` 4 模块 |
| D2 | athena_knowledge 完成 | `packages/knowledge/` 8 模块 |
| D3 | 序列化层 | `packages/knowledge/src/athena_knowledge/serialization.py` |
| D4 | 验证层 | `packages/knowledge/src/athena_knowledge/validation.py` |
| D5 | 完整测试 | `packages/knowledge/tests/` 100% 覆盖 |
| D6 | 包配置 | `pyproject.toml` × 2 |
| D7 | Sprint Report | `docs/sprint1-report.md` |

---

## 5. Task Breakdown (Issues)

### Issue-001: Knowledge Object — 聚合根补全

**范围**: `entity.py`, `relation.py`, `statement.py`

- [ ] KnowledgeEntity: 补全 `__repr__`, `__str__`
- [ ] KnowledgeRelation: 补全 `is_active_at` 边界测试
- [ ] Statement: 补全 `__post_init__` 验证（predicate 非空）
- [ ] 所有聚合根: `__eq__` 基于 ID

**依赖**: 无
**估计**: 3h

### Issue-002: Knowledge Identity — ID 系统加固

**范围**: `identity.py`

- [ ] 补全 `is_valid_id` 边界（空字符串、无下划线）
- [ ] 添加 `parse_id` 函数（从字符串解析前缀和 UUID 部分）
- [ ] 添加 ID 常量文档（PREFIX_* 的使用说明）

**依赖**: 无
**估计**: 2h

### Issue-003: Knowledge Lifecycle — 状态机集成

**范围**: `lifecycle.py`, `entity.py`, `relation.py`, `statement.py`

- [ ] EntityLifecycle 与 KnowledgeEntity 集成（activate/deprecate/merge 使用 StateMachine.validate_transition）
- [ ] RelationLifecycle 与 KnowledgeRelation 集成
- [ ] StatementLifecycle 与 Statement 集成

**依赖**: Issue-001
**估计**: 4h

### Issue-004: Knowledge Metadata — 元数据扩展

**范围**: `metadata.py`

- [ ] 添加 `created_by`, `updated_by` 字段
- [ ] 添加 `source` 字段（metadata 来源追踪）
- [ ] 添加 `tags` 字典
- [ ] 元数据 diff 工具

**依赖**: 无
**估计**: 2h

### Issue-005: Quality Score — 算法完善

**范围**: `quality.py`

- [ ] 补全 `compute` 方法的边界处理（空 properties、负数 confidence）
- [ ] 添加 `decay` 函数（基于时间的质量衰减）
- [ ] 添加 `compare` 静态方法（比较两个 QualityScore）
- [ ] 添加 `to_dict` / `from_dict`

**依赖**: 无
**估计**: 3h

### Issue-006: Serialization — 序列化层

**范围**: 新建 `serialization.py`

- [ ] `to_dict(entity)` — 递归序列化所有领域对象到 dict
- [ ] `from_dict(data, cls)` — 从 dict 反序列化
- [ ] `to_json(entity)` — JSON 字符串
- [ ] `from_json(json_str, cls)` — 从 JSON 反序列化
- [ ] 支持所有值对象（EntityName, EntityAlias, EntityProperty, StatementSource, QualityScore）
- [ ] 支持所有聚合根

**依赖**: Issue-001, Issue-004
**估计**: 8h

### Issue-007: Validation — 领域验证层

**范围**: 新建 `validation.py`

- [ ] `EntityValidator` — 验证 KnowledgeEntity 完整性
- [ ] `RelationValidator` — 验证 KnowledgeRelation
- [ ] `StatementValidator` — 验证 Statement
- [ ] `ValidationResult` — 统一验证结果（errors, warnings）
- [ ] `ValidationRule` — 可组合的验证规则

**依赖**: Issue-001
**估计**: 6h

### Issue-008: Unit Test — 完整测试覆盖

**范围**: `tests/`

- [ ] Identity: 边界测试（空字符串、超长字符串、特殊字符）
- [ ] Entity: 属性冲突、merge 后状态、质量重算
- [ ] Relation: 循环关系、时间边界
- [ ] Statement: 重复审批、空 predicate
- [ ] Quality: 所有维度独立测试
- [ ] Permission: 所有预设权限测试
- [ ] Lifecycle: 所有状态转换组合
- [ ] Workflow: 重试耗尽、DLQ 场景
- [ ] Serialization: 往返测试
- [ ] Validation: 规则组合测试

**依赖**: Issue-001~007
**估计**: 10h

---

## 6. Task Dependency Graph

```
Issue-002 (Identity)     Issue-004 (Metadata)
       │                        │
       └────────┬───────────────┘
                │
          Issue-001 (Object)
                │
       ┌────────┼────────┐
       │        │        │
  Issue-003  Issue-007  Issue-005
  (Lifecycle) (Valid)   (Quality)
       │        │        │
       └────────┼────────┘
                │
          Issue-006 (Serialization)
                │
          Issue-008 (Tests)
```

---

## 7. Estimated Complexity

| Issue | 复杂度 | 估计 | 风险 |
|-------|:---:|------|------|
| 001 - Object | Medium | 3h | 低 |
| 002 - Identity | Low | 2h | 低 |
| 003 - Lifecycle | Medium | 4h | 中（集成可能暴露状态机设计问题） |
| 004 - Metadata | Low | 2h | 低 |
| 005 - Quality | Medium | 3h | 低 |
| 006 - Serialization | High | 8h | 中（递归序列化复杂） |
| 007 - Validation | High | 6h | 中（规则组合设计） |
| 008 - Tests | High | 10h | 中（覆盖率目标 100%） |
| **合计** | | **38h** | |

---

## 8. Potential Risks

| 风险 | 概率 | 影响 | 缓解 |
|------|:---:|:---:|------|
| 序列化层递归复杂度过高 | 中 | 高 | 先实现简单 dict 序列化，再扩展 |
| 状态机集成破坏现有测试 | 低 | 中 | Issue-003 独立分支，合并前全量回归 |
| 100% 覆盖率无法达成 | 中 | 中 | 按模块拆分目标（核心域 100%，工具类 90%） |
| Python dataclass 限制 | 低 | 中 | 遇到限制时记录为技术债务 |

---

## 9. Definition of Done

每个 Issue 完成必须满足：

- [ ] 代码通过 `ruff check` + `ruff format`
- [ ] `mypy --strict` 无错误
- [ ] 所有新增测试通过
- [ ] 覆盖率 ≥ 90%（核心域 100%）
- [ ] 所有公开方法有 Google Style Docstring
- [ ] PR 已 Review 并 Squash Merge
- [ ] 相关文档已更新

---

## 10. Testing Strategy

| 层级 | 范围 | 工具 |
|------|------|------|
| Unit | 每个公开方法的 Happy Path + Edge Case | pytest |
| Property | 序列化往返（serialize → deserialize → equals original） | pytest |
| State Machine | 所有合法/非法状态转换组合 | pytest |
| Validation | 正常对象 + 畸形对象 + 空对象 | pytest |

覆盖率目标：
- `athena_core`: 95%
- `athena_knowledge`: 95%
- `serialization.py`: 100%
- `validation.py`: 100%

---

## 11. Architecture Impact

- **无架构变更** — Sprint 1 严格在已有 Architecture Baseline 内
- 不引入新的 Bounded Context
- 不修改已有接口
- 序列化层和验证层是领域层的附加能力，不改变领域模型

---

## 12. ADR Impact

- 无新增 ADR
- 已有 ADR-001（项目初始化）和 ADR-002（Phase 0 审查）不受影响

---

## 13. RFC Impact

- 无新增 RFC
- 已有 RFC-001 ~ 010 不受影响
- 序列化格式（dict/JSON）为领域层内部约定，不涉及 RFC

---

## 14. Rollback Strategy

- 所有开发在 feature 分支进行
- 每个 Issue 独立分支，合并前全量回归
- 如某 Issue 阻塞，可独立回滚不影响其他
- main 分支始终可运行 `39 tests passing`

---

## 15. Future Extension

| 扩展点 | 说明 | 触发条件 |
|--------|------|----------|
| 新的 EntityType | 在 `EntityType` enum 添加 | 业务需求 |
| 新的 RelationType | 在 `RelationType` enum 添加 | 业务需求 |
| 自定义 QualityScore 权重 | QualityScore.compute 的 weights 参数 | 业务需求 |
| 自定义 Permission 组合 | Permission 类支持 scope 并集 | Phase 2+ |
| 新的 Lifecycle | 继承 StateMachine 定义转换表 | 新增聚合根 |
| 自定义 Serialization | Serialization registry | Phase 3+ |
| 自定义 Validation Rules | ValidationRule 组合 | Phase 2+ |

---

## Sprint Board

```
┌─────────────────────────────────────────────────────────┐
│  Sprint 1 — Knowledge Core                              │
├──────────┬──────────────────────────┬───────────────────┤
│  Backlog │  In Progress             │  Done              │
├──────────┼──────────────────────────┼───────────────────┤
│          │                          │ Core Identity ✅   │
│          │                          │ Core Enums ✅      │
│          │                          │ Core Base ✅       │
│          │                          │ Core Metadata ✅   │
│          │                          │ Entity ✅          │
│          │                          │ Relation ✅        │
│          │                          │ Statement ✅       │
│          │                          │ Quality ✅         │
│          │                          │ Permission ✅      │
│          │                          │ Lifecycle ✅       │
│          │                          │ Workflow ✅        │
│          │                          │ Events ✅          │
│          │                          │ Basic Tests ✅     │
├──────────┼──────────────────────────┼───────────────────┤
│ ISS-001  │                          │                    │
│ ISS-002  │                          │                    │
│ ISS-003  │                          │                    │
│ ISS-004  │                          │                    │
│ ISS-005  │                          │                    │
│ ISS-006  │                          │                    │
│ ISS-007  │                          │                    │
│ ISS-008  │                          │                    │
└──────────┴──────────────────────────┴───────────────────┘
```

---

*Sprint Plan 等待 Review。Approved 后按 Issue 顺序开发。*
