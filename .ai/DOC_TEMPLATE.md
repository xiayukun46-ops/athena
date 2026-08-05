# DOC_TEMPLATE.md

> Athena 设计文档强制模板。缺失任一章节的文档不被接受。
> 完整标准见: [docs/TEMPLATE.md](../docs/TEMPLATE.md)

---

## 强制九章

```
1. Background    背景 — 为什么有这篇文档
2. Problem       问题 — 具体、可量化的问题陈述
3. Goals         目标 — 成功标准 + 优先级
4. Non-goals     非目标 — 明确排除的范围
5. Design        设计 — 架构/接口/数据流/迁移
6. Alternatives  替代方案 — ≥ 2 个 + 不选理由
7. Risks         风险 — 概率/影响/缓解
8. Future Work   未来演进 — 短期/长期/触发条件
9. References    参考 — 所有引用文档链接
```

---

## 快速检查

提交文档前，逐项确认：

- [ ] Background 解释了触发原因和项目阶段
- [ ] Problem 是具体的、可量化的（非"XX 太慢了"）
- [ ] Goals 有量化的成功指标
- [ ] Non-goals 排除了至少 2 个可能被误解的范围
- [ ] Design 包含架构图（Mermaid）或接口定义（代码块）
- [ ] Alternatives ≥ 2 个，每个标明了不选的技术理由
- [ ] Risks 每个都有缓解措施
- [ ] Future Work 包含重新审视的触发条件
- [ ] References 所有引用可点击

---

## 反例

缺失 Problem 章节:
> 被拒理由: 读者无法判断"这篇文档要解决什么问题"

Alternatives 只有 1 个:
> 被拒理由: 无法证明当前方案是经过比较的选择

Risks 无缓解措施:
> 被拒理由: 识别风险但不提供缓解等于没有风险管理

---

## 相关文件

- [docs/TEMPLATE.md](../docs/TEMPLATE.md) — 完整模板标准（含每章正例）
- [docs/adr/ADR-000-template.md](../docs/adr/ADR-000-template.md) — ADR 模板
- [docs/rfc/RFC-000-template.md](../docs/rfc/RFC-000-template.md) — RFC 模板
