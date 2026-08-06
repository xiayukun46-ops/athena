"""Domain events for the Knowledge bounded context.

True domain events only. Infrastructure events (ArticleFetched,
CollectorStarted, CrawlerFinished) belong in the infrastructure layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from athena_core.base import DomainEvent
from athena_core.enums import EntityType, RelationType, SearchMode
from athena_core.identity import (
    EntityId, RelationId, StatementId, UserId,
    new_entity_id, new_relation_id, new_statement_id, new_user_id,
)


# ── Knowledge Lifecycle Events ──

@dataclass
class KnowledgeCreated(DomainEvent):
    knowledge_id: str = ""
    canonical_name: str = ""
    entity_type: EntityType = EntityType.CONCEPT

    @property
    def event_type(self) -> str: return "KnowledgeCreated"
    @property
    def aggregate_id(self) -> str: return self.knowledge_id


@dataclass
class KnowledgeVerified(DomainEvent):
    knowledge_id: str = ""
    reviewer_id: UserId = field(default_factory=new_user_id)

    @property
    def event_type(self) -> str: return "KnowledgeVerified"
    @property
    def aggregate_id(self) -> str: return self.knowledge_id


@dataclass
class KnowledgePublished(DomainEvent):
    knowledge_id: str = ""

    @property
    def event_type(self) -> str: return "KnowledgePublished"
    @property
    def aggregate_id(self) -> str: return self.knowledge_id


@dataclass
class KnowledgeArchived(DomainEvent):
    knowledge_id: str = ""
    reason: str = ""

    @property
    def event_type(self) -> str: return "KnowledgeArchived"
    @property
    def aggregate_id(self) -> str: return self.knowledge_id


# ── Entity Events ──

@dataclass
class EntityCreated(DomainEvent):
    entity_id: EntityId = field(default_factory=new_entity_id)
    canonical_name: str = ""
    entity_type: EntityType = EntityType.CONCEPT

    @property
    def event_type(self) -> str: return "EntityCreated"
    @property
    def aggregate_id(self) -> str: return self.entity_id


@dataclass
class EntityUpdated(DomainEvent):
    entity_id: EntityId = field(default_factory=new_entity_id)
    changed_fields: list[str] = field(default_factory=list)

    @property
    def event_type(self) -> str: return "EntityUpdated"
    @property
    def aggregate_id(self) -> str: return self.entity_id


# ── Relation Events ──

@dataclass
class RelationCreated(DomainEvent):
    relation_id: RelationId = field(default_factory=new_relation_id)
    relation_type: RelationType = RelationType.RELATED_TO
    source_entity_id: EntityId = field(default_factory=new_entity_id)
    target_entity_id: EntityId = field(default_factory=new_entity_id)

    @property
    def event_type(self) -> str: return "RelationCreated"
    @property
    def aggregate_id(self) -> str: return self.relation_id


# ── Statement Events ──

@dataclass
class StatementApproved(DomainEvent):
    statement_id: StatementId = field(default_factory=new_statement_id)
    reviewer_id: UserId = field(default_factory=new_user_id)

    @property
    def event_type(self) -> str: return "StatementApproved"
    @property
    def aggregate_id(self) -> str: return self.statement_id


@dataclass
class StatementRejected(DomainEvent):
    statement_id: StatementId = field(default_factory=new_statement_id)
    reviewer_id: UserId = field(default_factory=new_user_id)
    reason: str = ""

    @property
    def event_type(self) -> str: return "StatementRejected"
    @property
    def aggregate_id(self) -> str: return self.statement_id


# ── Infrastructure Events (moved to infrastructure layer in Phase 2) ──
# ArticleFetched, ArticlePublished → content infrastructure
# TaskStarted, TaskCompleted → AI infrastructure
# SearchPerformed → search infrastructure
# CollectorStarted, CrawlerFinished → collector infrastructure
