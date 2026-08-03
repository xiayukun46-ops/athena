# Knowledge Model v2.0

## 概述

Knowledge Model 是 Athena 的核心知识表示本体论。它定义了系统如何理解、存储和推理关于世界的知识。

与 ER Diagram（物理存储）和 Graph Model（图查询优化）不同，Knowledge Model 关注的是**认知层面**的知识结构——面向人类理解和 AI 推理，而非面向存储引擎。

---

## 1. 知识三角（Knowledge Triangle）

Athena 的知识表示基于三个核心原语：

```
                    ENTITY（实体）
                    "是什么"
                       /\
                      /  \
                     /    \
                    /      \
                   /        \
                  /__________\
    STATEMENT（声明）        RELATION（关系）
    "谁说的"                 "什么关联"
```

- **Entity**: 世界上存在的或概念性的事物
- **Relation**: 实体之间的有向连接
- **Statement**: 关于实体或关系的可溯源断言

三者构成完整知识的最小单位：*谁（Source）声称实体 A 与实体 B 存在关系 R，置信度为 C*。

---

## 2. Entity（实体）

### 2.1 实体定义

实体是 Knowledge Model 的原子单元。每个实体代表现实世界中的一个具体事物或抽象概念。

### 2.2 实体类型体系

```yaml
EntityType:
  PERSON:
    description: 个人
    subtypes: [POLITICIAN, SCIENTIST, ARTIST, ATHLETE, ENTREPRENEUR, ACTIVIST]
    attributes: [birth_date, death_date, nationality, gender]
    
  ORGANIZATION:
    description: 组织
    subtypes: [COMPANY, GOVERNMENT, NGO, EDUCATIONAL, MILITARY, MEDIA, SPORTS_TEAM]
    attributes: [founded_date, headquarters, industry, parent_org]
    
  LOCATION:
    description: 地理位置
    subtypes: [CONTINENT, COUNTRY, REGION, CITY, LANDMARK, NATURAL_FEATURE]
    attributes: [coordinates, population, area, country]
    
  EVENT:
    description: 事件
    subtypes: [POLITICAL, ECONOMIC, SPORTS, DISASTER, SCIENTIFIC, CULTURAL, CONFLICT]
    attributes: [start_date, end_date, location, participants, scale]
    
  CONCEPT:
    description: 抽象概念
    subtypes: [THEORY, IDEOLOGY, FIELD_OF_STUDY, TECHNOLOGY, POLICY, TREND]
    attributes: [domain, related_fields, first_coined]
    
  PRODUCT:
    description: 产品
    subtypes: [SOFTWARE, HARDWARE, VEHICLE, PHARMACEUTICAL, CONSUMER_GOODS]
    attributes: [manufacturer, release_date, category, version]
    
  WORK:
    description: 创作作品
    subtypes: [BOOK, FILM, MUSIC, ARTWORK, PAPER, PATENT, GAME]
    attributes: [creators, publication_date, publisher, language]
    
  NATURAL_ENTITY:
    description: 自然实体
    subtypes: [SPECIES, CHEMICAL, MINERAL, CELESTIAL_BODY, GENE]
    attributes: [scientific_name, taxonomy, discovery_date]
```

### 2.3 实体属性模型

每个实体采用 EAV（Entity-Attribute-Value）扩展属性模式：

```
EntityCore:
  id: UUID
  canonical_name: str          # 规范名称（主名）
  entity_type: EntityType
  created_at: datetime
  updated_at: datetime
  version: int
  
EntityName:  # 多语言名称
  entity_id: UUID
  name: str
  language: str                # ISO 639-1
  is_preferred: bool           # 是否为该语言的优先名称
  
EntityAlias:  # 别名/曾用名/缩写
  entity_id: UUID
  alias: str
  alias_type: [ACRONYM, FORMER_NAME, NICKNAME, TRANSLITERATION, COMMON_MISSPELLING]
  language: str | None
  
EntityProperty:  # EAV 属性
  entity_id: UUID
  key: str                     # 属性名（如 "birth_date"）
  value: str                   # 属性值（如 "1964-01-07"）
  value_type: [STRING, NUMBER, DATE, BOOLEAN, JSON, URI]
  confidence: float            # 0.0 - 1.0
  source: StatementId | None   # 溯源到具体声明
  valid_from: datetime | None  # 属性开始生效时间
  valid_until: datetime | None # 属性失效时间（可选）
```

### 2.4 实体生命周期

```
DRAFT → ACTIVE → DEPRECATED → MERGED
  │        │          │
  │        │          └→ 被合并到另一个实体
  │        └→ 正常活跃状态
  └→ AI 自动提取，待人工审核

状态转换规则:
  DRAFT → ACTIVE: 置信度 >= 0.7 或 人工确认
  ACTIVE → DEPRECATED: 信息过时或不再有效
  ACTIVE → MERGED: 实体消歧后合并
  DRAFT → MERGED: 确认为重复实体
```

---

## 3. Relation（关系）

### 3.1 关系定义

关系是实体间的有向连接。每条关系可附带属性和溯源信息。

### 3.2 关系类型体系

```yaml
RelationType:
  # ── 层级关系 ──
  INSTANCE_OF:        # 实例归属（特斯拉 INSTANCE_OF 电动汽车制造商）
  SUBCLASS_OF:        # 子类归属（电动汽车 SUBCLASS_OF 汽车）
  PART_OF:            # 部分-整体（加州 PART_OF 美国）
  MEMBER_OF:          # 成员关系（某人 MEMBER_OF 某个组织）
  
  # ── 事件关系 ──
  PARTICIPATED_IN:    # 参与事件
  ORGANIZED:          # 组织/主办
  CAUSED:             # 因果关系
  PRECEDED:           # 时序先后
  
  # ── 人际/组织关系 ──
  WORKS_FOR:          # 雇佣关系
  FOUNDED:            # 创立关系
  LED_BY:             # 领导关系
  COLLABORATED_WITH:  # 合作关系
  COMPETES_WITH:      # 竞争关系
  ACQUIRED:           # 收购关系
  
  # ── 地理关系 ──
  LOCATED_IN:         # 位于
  BORDERS:            # 接壤
  NEAR:               # 邻近
  
  # ── 知识关系 ──
  RELATED_TO:         # 通用关联（兜底）
  SIMILAR_TO:         # 相似性
  OPPOSITE_OF:        # 对立
  CITED:              # 引用关系
  
  # ── 属性关系 ──
  HAS_PROPERTY:       # 拥有属性
  PRODUCES:           # 生产/产出
  OWNS:               # 拥有
  REGULATED_BY:       # 受监管
```

### 3.3 关系模型

```
Relation:
  id: UUID
  type: RelationType
  source_entity_id: UUID      # 关系起点
  target_entity_id: UUID      # 关系终点
  properties: dict             # 扩展属性
    weight: float              # 关系强度 (0.0-1.0)
    start_date: datetime       # 关系开始时间
    end_date: datetime         # 关系结束时间（可选）
    role: str                  # 关系中的角色描述
  confidence: float            # 综合置信度
  statements: list[UUID]       # 支撑该关系的声明列表
  created_at: datetime
  updated_at: datetime
  version: int
```

---

## 4. Statement（声明）

### 4.1 声明的核心定位

Statement 是 Knowledge Model 的**可溯源层**。每一条知识都必须有声明支撑：

> "我们之所以知道 A 和 B 有关联 R，是因为来源 S 中提到了。"

### 4.2 声明模型

```
Statement:
  id: UUID
  type: StatementType          # ENTITY_EXTRACTION | RELATION_EXTRACTION | MANUAL
  subject: UUID                # 声明的主体（实体 ID 或 关系 ID）
  predicate: str               # 声明的属性名
  object: str                  # 声明的属性值
  confidence: float            # 提取/输入时的置信度
  extraction_method: str       # AI 模型标识 或 "manual"
  source:
    article_id: UUID           # 源文章
    snippet: str               # 原文摘录（证据）
    position: int              # 在文章中的位置（段落偏移）
  reviewer: UserId | None      # 审核人
  review_status: [PENDING, APPROVED, REJECTED]
  created_at: datetime
```

### 4.3 声明聚合 → 知识冲突解决

多条声明可能指向同一个事实但给出不同结论。Athena 的策略：

```
同一实体/关系的多条声明:
  ├── 合并 (Merge): 信息一致，合并置信度
  ├── 增强 (Enrich): 信息互补，补充属性
  ├── 仲裁 (Arbitrate): 信息冲突:
  │     ├── 优先高置信度来源
  │     ├── 优先多数来源
  │     ├── 优先最近时间
  │     └── 保留冲突记录（不删除少数派观点）
  └── 过期 (Expire): 信息已被新证据推翻
```

冲突保留对于知识平台是关键——用户应该能看到"主流观点认为...但也有来源声称..."。

---

## 5. 溯源与置信度（Provenance & Confidence）

### 5.1 溯源链

```
Article (原始内容)
  └→ Statement (AI 提取的声明)
       └→ EntityProperty / Relation (结构化知识)
```

每一条知识到原始内容最多两步追溯。用户在任意层级可以：
- 看到知识的上游声明链
- 点击跳转到原始文章
- 对比不同来源的相同声明

### 5.2 置信度计算

```
实体置信度 = mean(支撑该实体的所有声明的置信度) × 声明数量衰减因子

关系置信度 = mean(支撑该关系的所有声明的置信度) × 来源多样性加分

声明置信度:
  - AI 提取: 模型原始 confidence
  - 人工输入: 1.0
  - 审核通过后: 在原基础上加权
```

### 5.3 来源可信度（Source Credibility）

```
SourceCredibility:
  source_id: UUID
  credibility_score: float     # 0.0 - 1.0
  bias_leaning: str            # 政治倾向（如适用）
  fact_check_rating: str       # 事实核查评级
  domain_authority: float      # 领域权威性
  calculated_at: datetime
```

来源可信度影响该来源所有声明的权重。

---

## 6. 时序模型（Temporal Model）

### 6.1 知识的时变性

知识不是静态的——"Apple 的 CEO"的答案在 2011 年前后完全不同。

```
EntitySnapshot:     # 实体在特定时间点的快照
  entity_id: UUID
  timestamp: datetime
  properties: dict            # 该时间点的所有属性值
  active_relations: list[UUID] # 该时间点的活跃关系
```

### 6.2 时态查询

```cypher
# 查询 2015 年的 Apple CEO
MATCH (p:PERSON)-[r:LED_BY]->(o:ORGANIZATION {name: "Apple Inc."})
WHERE r.start_date <= date("2015-01-01") 
  AND (r.end_date IS NULL OR r.end_date > date("2015-01-01"))
RETURN p.name
```

---

## 7. 多语言支持

### 7.1 跨语言实体

同一个实体在不同语言中有不同的名称，但在知识模型中它们是同一个实体：

```
Entity: {id: "ent_001", canonical_name: "Apple Inc."}
  ├── EntityName(zh): "苹果公司"
  ├── EntityName(ja): "アップル"
  ├── EntityName(ko): "애플"
  ├── EntityName(en): "Apple Inc."  [preferred]
  └── EntityAlias: "AAPL" [ACRONYM]
```

### 7.2 跨语言对齐

- 同一实体在不同语言新闻中被提及 → 实体链接技术合并
- 知识查询时根据用户语言返回对应名称
- 关系类型名支持 i18n

---

## 8. 知识质量维度

| 维度 | 指标 | 测量方式 |
|------|------|----------|
| 完整性 | 实体属性填充率 | 必填属性覆盖率 |
| 一致性 | 冲突声明占比 | 冲突声明 / 总声明 |
| 时效性 | 知识新鲜度 | 最近更新距今时间 |
| 置信度 | 平均置信度 | mean(所有声明的置信度) |
| 溯源性 | 可溯源声明占比 | 有 source 的声明 / 总声明 |
| 多样性 | 每实体来源数 | 支撑实体的唯一来源数 |

---

## 9. 知识模型与 AI 的接口

### 9.1 抽取式输入（AI → Knowledge）

```
原始文章 → NER Pipeline → Statement(ENTITY_EXTRACTION) → Entity(DRAFT)
原始文章 → RE Pipeline  → Statement(RELATION_EXTRACTION) → Relation(ACTIVE)
```

### 9.2 生成式消费（Knowledge → AI）

```
User Question → RAG Context Assembly:
  1. 检索相关实体
  2. 获取实体属性和关系
  3. 获取支撑声明（含原文摘录）
  4. 组装 LLM Prompt (结构化知识 + 原文证据)
  → LLM Generation → Answer with Citations
```

---

## 10. 与 Graph Model / ER Diagram 的关系

```
Knowledge Model (本体层)
  │ 定义：什么是实体、关系、声明
  │ 关注：知识结构、溯源逻辑、时态语义
  │
  ├──→ Graph Model (图存储层)
  │     定义：Node Labels, Edge Types, Properties
  │     关注：图查询效率、路径遍历、子图匹配
  │
  └──→ ER Diagram (关系存储层)
        定义：Tables, Columns, Indexes
        关注：事务一致性、JOIN 效率、数据完整性
```

三者上下位关系：Knowledge Model 决定"存什么"，ER/Graph 决定"怎么存"。

---

*本文档为 Athena 知识系统的核心设计，后续所有数据建模以此为准。*
