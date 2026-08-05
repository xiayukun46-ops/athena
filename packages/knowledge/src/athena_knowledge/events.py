"""Domain events for the Knowledge bounded context.

Complete event catalog as defined in docs/domain/event-model.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from athena_core.base import DomainEvent
from athena_core.enums import ContentType, EntityType, RelationType, SearchMode
from athena_core.identity import (
    ArticleId, EntityId, RelationId, SourceId, StatementId, UserId,
    new_article_id, new_entity_id, new_relation_id, new_source_id,
    new_statement_id, new_user_id,
)


# ── Content Events ──

@dataclass
class ArticleFetched(DomainEvent):
    article_id: ArticleId = field(default_factory=new_article_id)
    source_id: SourceId = field(default_factory=new_source_id)
    url: str = ""
    url_hash: str = ""
    title: str = ""
    language: str = ""
    published_at: str = ""
    content_type: ContentType = ContentType.ARTICLE
    word_count: int = 0

    @property
    def event_type(self) -> str:
        return "ArticleFetched"

    @property
    def aggregate_id(self) -> str:
        return self.article_id


@dataclass
class ArticlePublished(DomainEvent):
    article_id: ArticleId = field(default_factory=new_article_id)
    source_id: SourceId = field(default_factory=new_source_id)
    title: str = ""
    language: str = ""
    categories: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    @property
    def event_type(self) -> str:
        return "ArticlePublished"

    @property
    def aggregate_id(self) -> str:
        return self.article_id


# ── Knowledge Events ──

@dataclass
class EntityCreated(DomainEvent):
    entity_id: EntityId = field(default_factory=new_entity_id)
    canonical_name: str = ""
    entity_type: EntityType = EntityType.CONCEPT
    language: str = ""
    statement_ids: list[StatementId] = field(default_factory=list)

    @property
    def event_type(self) -> str:
        return "EntityCreated"

    @property
    def aggregate_id(self) -> str:
        return self.entity_id


@dataclass
class EntityUpdated(DomainEvent):
    entity_id: EntityId = field(default_factory=new_entity_id)
    changed_fields: list[str] = field(default_factory=list)

    @property
    def event_type(self) -> str:
        return "EntityUpdated"

    @property
    def aggregate_id(self) -> str:
        return self.entity_id


@dataclass
class RelationCreated(DomainEvent):
    relation_id: RelationId = field(default_factory=new_relation_id)
    relation_type: RelationType = RelationType.RELATED_TO
    source_entity_id: EntityId = field(default_factory=new_entity_id)
    target_entity_id: EntityId = field(default_factory=new_entity_id)
    confidence: float = 0.5
    statement_ids: list[StatementId] = field(default_factory=list)

    @property
    def event_type(self) -> str:
        return "RelationCreated"

    @property
    def aggregate_id(self) -> str:
        return self.relation_id


# ── Search Events ──

@dataclass
class SearchPerformed(DomainEvent):
    query_text: str = ""
    search_mode: SearchMode = SearchMode.HYBRID
    result_count: int = 0
    latency_ms: int = 0
    user_id: UserId | None = None
    language: str = ""

    @property
    def event_type(self) -> str:
        return "SearchPerformed"

    @property
    def aggregate_id(self) -> str:
        return self.query_text


# ── AI Events ──

@dataclass
class TaskStarted(DomainEvent):
    task_id: str = ""
    prompt_name: str = ""
    model: str = ""
    task_type: str = ""
    target_article_id: ArticleId | None = None

    @property
    def event_type(self) -> str:
        return "TaskStarted"

    @property
    def aggregate_id(self) -> str:
        return self.task_id


@dataclass
class TaskCompleted(DomainEvent):
    task_id: str = ""
    output: dict = field(default_factory=dict)
    tokens_used: int = 0
    cost_amount: float = 0.0
    cost_currency: str = "USD"
    latency_ms: int = 0

    @property
    def event_type(self) -> str:
        return "TaskCompleted"

    @property
    def aggregate_id(self) -> str:
        return self.task_id


# ── User Events ──

@dataclass
class UserRegistered(DomainEvent):
    user_id: UserId = field(default_factory=new_user_id)
    email: str = ""

    @property
    def event_type(self) -> str:
        return "UserRegistered"

    @property
    def aggregate_id(self) -> str:
        return self.user_id
