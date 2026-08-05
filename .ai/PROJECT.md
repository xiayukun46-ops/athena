# Athena — Project Rules for AI Agents

> 你是 Athena 项目的 AI 协作伙伴。以下是你必须遵守的铁律。
> 违反任一条的代码将被直接拒绝。

---

## 铁律 (不可违背)

1. **无文档不编码** — 修改代码前确认相关设计文档已存在且已更新
2. **架构边界不可逾越** — 不可跨上下文直接访问数据库或调用内部 API
3. **事件是唯一通道** — 上下文间通信仅通过 Domain Events，不做直接 API 调用
4. **接口先行** — 新功能先定义接口（OpenAPI / Python ABC），再实现
5. **插件化优先** — 新功能默认以 Plugin 形式实现，不硬编码进核心
6. **TDD 不可跳过** — 先写测试，后写实现
7. **安全零例外** — 所有输入需验证，禁止硬编码密钥

---

## 决策路径

```
发现新需求
  ↓
查阅 docs/adr/ — 是否已有决策？
  ├─ 有 → 遵守
  └─ 无 → 是否需要 ADR？
           ├─ 重大架构变更 → 写 ADR
           └─ 日常开发 → 写 RFC 或直接实现
```

---

## 参考文档

| 想了解 | 读这个 |
|--------|--------|
| 项目是什么 | [docs/00-vision.md](docs/00-vision.md) |
| 原则 | [docs/02-constitution.md](docs/02-constitution.md) |
| 术语 | [docs/03-glossary.md](docs/03-glossary.md) |
| 怎么组织代码 | [docs/04-domain-model.md](docs/04-domain-model.md) |
| 架构 | [docs/07-architecture.md](docs/07-architecture.md) |
| 代码规范 | [docs/governance/coding-standard.md](docs/governance/coding-standard.md) |
| 施工蓝图 | [docs/BLUEPRINT.md](docs/BLUEPRINT.md) |


## 文档模板规范

所有设计文档必须遵循 [docs/TEMPLATE.md](docs/TEMPLATE.md) 的九章结构：

1. Background  2. Problem  3. Goals  4. Non-goals  5. Design  6. Alternatives  7. Risks  8. Future Work  9. References

缺失任一章节的文档不被接受。