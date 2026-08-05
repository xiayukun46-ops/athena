# 06 — Knowledge Engine

> 知识引擎是 Athena 的核心——将原始内容转化为结构化知识。

**详细设计见**: [domain/knowledge-model.md](domain/knowledge-model.md) + [domain/graph-model.md](domain/graph-model.md)

---

## 什么是 Knowledge Engine

知识引擎不是单一组件，而是**一组协作的服务**：

```
原始文章 → [实体提取] → [关系提取] → [实体链接] → [声明聚合] → 知识图谱
              │               │              │              │
              └───────────────┴────── AI ────┴──────────────┘
```

---

## 为什么三层模型（Entity → Relation → Statement）

### 传统知识图谱的问题

大多数知识图谱只有两层：Entity 和 Relation。例如：
- `(Tim Cook) --[CEO_OF]--> (Apple Inc.)`

问题：这条信息是从哪里来的？可信度多高？有没有其他文章说不同的人 CEO？

### Athena 的三层模型

```
Statement（声明层）
  "2026-08-01 TechCrunch 文章第 3 段提到：Tim Cook 是 Apple 的 CEO"
        │
        ▼
Relation（关系层）
  (Tim Cook) --[LED_BY {role="CEO"}]--> (Apple Inc.)
  confidence = mean(支撑声明的置信度)
        │
        ▼
Entity（实体层）
  Tim Cook {type=PERSON, properties={...}}
  Apple Inc. {type=ORGANIZATION, properties={...}}
```

**关键创新**: Statement 是独立的一层。它存储了"谁说的、在哪说的、怎么说的"。这带来三个能力：

1. **溯源**: 用户点一下就能看到原始文章和摘录
2. **冲突保留**: 如果另一篇文章说"Tim Cook 已卸任"，两条 Statement 共存，用户可以对比
3. **置信度可计算**: 基于支撑声明的质量和数量，动态计算每条知识的置信度

### 替代方案

**方案 A: 传统三元组 (RDF)**  
直接存 `(Subject, Predicate, Object)` 不记录溯源。

- 优点: 简单，标准化
- 缺点: 无溯源、无置信度、无冲突保留
- 为什么不选: 不符合"可信知识"的定位

**方案 B: Property Graph (带属性)**  
在关系上附加属性（confidence, source），但不独立存储声明。

- 优点: 比 RDF 丰富
- 缺点: Source 只是"字符串属性"，无法支持多条声明 → 一条关系的聚合
- 为什么不选: 无法追溯"哪个来源说了什么"

**方案 C: 纯向量**  
不做结构化知识，全文存入向量数据库，检索时用相似度匹配。

- 优点: 实现简单
- 缺点: 无法回答结构化问题（"列出 Apple 所有 CEO 及任期"）
- 为什么不选: 向量搜索补充知识图谱，不能替代

---

## 知识处理管道

```
Stage 1: 实体提取 (NER)
  输入: Article.clean_text
  输出: list[Statement(ENTITY_EXTRACTION)]
  模型: LLM (GPT-5 / Claude) + 专用 NER 模型 (spaCy)

Stage 2: 实体链接 (Entity Linking)
  输入: 新提取的实体名称 + 已有实体候选
  输出: EntityId (MATCH) 或 NEW (创建新实体) 或 AMBIGUOUS (人工审核)
  模型: LLM + 向量相似度 + 规则

Stage 3: 关系提取 (RE)
  输入: Article.clean_text + 已链接的实体列表
  输出: list[Statement(RELATION_EXTRACTION)]
  模型: LLM

Stage 4: 声明聚合
  输入: 同一实体/关系的多条 Statement
  输出: 合并的属性、解决冲突、更新置信度

Stage 5: 知识发布
  输出: EntityCreated/Updated, RelationCreated 事件
```

---

## 置信度计算

```
实体置信度 = mean(支撑该实体的所有声明的置信度) × 衰减因子
  - 衰减因子: 1.0 (1-5 条声明), 0.95 (6-10), 0.90 (11-20), 0.85 (20+)
  - 逻辑: 少量高质量声明 > 大量低质量声明

声明置信度:
  - AI 提取: 模型返回的原始 confidence
  - 人工审核通过后: weighted(原始, 0.3) + weighted(1.0, 0.7)
```

---

## 冲突解决策略

当多条 Statement 对同一属性给出不同值时：

1. **相同值 → 合并**: 取最高置信度的 Statement 的 snippet
2. **互补值 → 合并**: 如一条 Statement 提供 birth_date，另一条提供 birth_place
3. **冲突值 → 保留**: 两个值都保留，标记 `needs_arbitration = true`
   - 主流观点: 置信度高 + 来源多
   - 少数派观点: 保留但不作为默认答案
4. **旧值被新值覆盖**: 新 Statement 的 valid_from 晚于旧值，旧值 archived

---

## 未来扩展

- **多模态**: Phase 5+ 支持从图片/视频中提取知识
- **时序推理**: "Apple 的 CEO" 的答案在 2011 年前后不同——支持时态查询
- **因果推理**: 不满足"B 是 A 的 CEO"，要回答"为什么 B 成为 A 的 CEO"
- **多语言对齐**: 不同语言新闻中提到的同一实体自动合并

---

## 相关文档

- [04-domain-model.md](04-domain-model.md) — 整体领域模型
- [05-event-model.md](05-event-model.md) — 知识管道的事件驱动
- [08-data-model.md](08-data-model.md) — 知识如何存储
- [10-agent-system.md](10-agent-system.md) — 执行知识提取的 Agent
- [domain/knowledge-model.md](domain/knowledge-model.md) — 知识本体论详细设计
