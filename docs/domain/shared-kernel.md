# Shared Kernel v1.0

## 概述

Shared Kernel 是 Athena 所有限界上下文共享的基础类型、值对象和约定。

---

## 1. ID 约定

所有聚合根的 ID 使用带类型前缀的格式：`{prefix}_{uuid_short}`

| 前缀 | 聚合根 | 示例 |
|------|--------|------|
| `src_` | Source | `src_a1b2c3d4` |
| `art_` | Article | `art_e5f6g7h8` |
| `ent_` | KnowledgeEntity | `ent_i9j0k1l2` |
| `rel_` | KnowledgeRelation | `rel_m3n4o5p6` |
| `stmt_` | Statement | `stmt_q7r8s9t0` |
| `usr_` | User | `usr_u1v2w3x4` |
| `tsk_` | CompletionTask | `tsk_y5z6a7b8` |
| `idx_` | SearchIndex | `idx_c9d0e1f2` |
| `plg_` | Plugin | `plg_g3h4i5j6` |

### ID 生成方法

```python
import uuid

def generate_id(prefix: str) -> str:
    """生成带前缀的类型化 ID"""
    short_uuid = uuid.uuid4().hex[:8]
    return f"{prefix}_{short_uuid}"
```

---

## 2. 通用值对象

以下值对象在 `src/shared/domain/` 中定义，所有限界上下文引用。

```python
# ── 标识符类型 ──
from uuid import UUID

class EntityId(UUID): ...
class ArticleId(UUID): ...
class SourceId(UUID): ...
class UserId(UUID): ...
class StatementId(UUID): ...
class RelationId(UUID): ...
class TaskId(UUID): ...

# ── 语言 ──
@dataclass(frozen=True)
class Language:
    """ISO 639-1 语言代码"""
    code: str
    name: str | None = None
    
    @staticmethod
    def from_code(code: str) -> "Language":
        return Language(code=code)

# ── URL ──
@dataclass(frozen=True)
class HttpUrl:
    value: str
    
    def __post_init__(self):
        # 基础 URL 格式验证
        if not self.value.startswith(("http://", "https://")):
            raise ValueError(f"Invalid URL: {self.value}")

# ── 置信度 ──
@dataclass(frozen=True)
class Confidence:
    value: float
    
    def __post_init__(self):
        if not (0.0 <= self.value <= 1.0):
            raise ValueError("Confidence must be in [0.0, 1.0]")
    
    @property
    def is_high(self) -> bool:
        return self.value >= 0.8
    
    @property
    def is_low(self) -> bool:
        return self.value < 0.3

# ── 日期范围 ──
@dataclass(frozen=True)
class DateRange:
    start: datetime
    end: datetime | None = None
    
    def contains(self, dt: datetime) -> bool:
        if self.end:
            return self.start <= dt <= self.end
        return self.start <= dt

# ── 分页 ──
@dataclass(frozen=True)
class Pagination:
    page: int = 1
    size: int = 20
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

@dataclass(frozen=True)
class Cursor:
    value: str
    has_more: bool = False

# ── 金额 ──
@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "USD"  # ISO 4217

# ── 排序 ──
@dataclass(frozen=True)
class SortConfig:
    field: str
    order: str = "desc"  # asc | desc
    
    @property
    def prefix(self) -> str:
        return "-" if self.order == "desc" else ""
```

---

## 3. 领域事件基类

```python
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

@dataclass
class DomainEvent(ABC):
    """所有领域事件的基类"""
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    @property
    @abstractmethod
    def event_type(self) -> str:
        """事件类型名（如 'ArticlePublished'）"""
        ...

@dataclass
class EventMetadata:
    correlation_id: UUID = field(default_factory=uuid4)
    causation_id: UUID | None = None
    source_context: str = ""
    version: int = 1
```

---

## 4. 聚合根基类

```python
@dataclass
class AggregateRoot(ABC):
    id: UUID
    version: int = 1
    _events: list[DomainEvent] = field(default_factory=list, init=False, repr=False)
    
    def add_event(self, event: DomainEvent) -> None:
        self._events.append(event)
    
    def collect_events(self) -> list[DomainEvent]:
        events = self._events.copy()
        self._events.clear()
        return events

@dataclass
class Entity(ABC):
    id: UUID

@dataclass(frozen=True)
class ValueObject(ABC):
    """不可变值对象基类"""
```

---

## 5. 通用枚举

```python
class ContentType(str, Enum):
    ARTICLE = "article"
    PAPER = "paper"
    REPORT = "report"
    SOCIAL_POST = "social_post"
    TRANSCRIPT = "transcript"

class EntityType(str, Enum):
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    EVENT = "event"
    CONCEPT = "concept"
    PRODUCT = "product"
    WORK = "work"
    NATURAL_ENTITY = "natural_entity"

class SearchMode(str, Enum):
    FULLTEXT = "fulltext"
    VECTOR = "vector"
    HYBRID = "hybrid"

class ReviewStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
```

---

## 6. 跨上下文规则

### 6.1 事件通信规则

- 上下文间仅通过领域事件通信
- 不进行直接 API 调用
- 不共享数据库表
- 事件消费者必须幂等

### 6.2 数据所有权

- 每个聚合根的数据仅由其所属上下文写入
- 其他上下文通过事件获取数据副本（最终一致性）

### 6.3 事务边界

- 一个事务仅修改一个聚合根
- 跨聚合根的一致性通过事件最终一致实现

---

*Shared Kernel 随领域模型演进同步更新。新增通用类型需 PR + Review。*
