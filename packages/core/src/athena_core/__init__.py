"""Athena Core — shared domain primitives.

This package provides the foundational types used by all bounded contexts:
- Identity types (EntityId, ArticleId, etc.)
- DDD base classes (AggregateRoot, Entity, ValueObject, DomainEvent)
- Shared enumerations (EntityType, RelationType, etc.)
- Standard metadata (StandardMetadata)
"""

from .base import AggregateRoot, DomainEvent, Entity, EventMetadata, ValueObject
from .enums import (
    EntityType, EntityStatus, RelationType, RelationStatus,
    StatementType, ReviewStatus, SourceType, SourceStatus,
    ArticleStatus, ContentType, PropertyValueType, AliasType,
    SearchMode, TaskStatus, WorkflowStage, WorkflowStageStatus,
)
from .identity import (
    EntityId, RelationId, StatementId, ArticleId, SourceId,
    UserId, TaskId, IndexId, PluginId, EventId,
    new_entity_id, new_relation_id, new_statement_id,
    new_article_id, new_source_id, new_user_id, new_task_id,
    new_event_id, generate_id, is_valid_id,
)
from .metadata import StandardMetadata

__all__ = [
    # Base classes
    "AggregateRoot", "DomainEvent", "Entity", "EventMetadata", "ValueObject",
    # Identity
    "EntityId", "RelationId", "StatementId", "ArticleId", "SourceId",
    "UserId", "TaskId", "IndexId", "PluginId", "EventId",
    "new_entity_id", "new_relation_id", "new_statement_id",
    "new_article_id", "new_source_id", "new_user_id", "new_task_id",
    "new_event_id", "generate_id", "is_valid_id",
    # Metadata
    "StandardMetadata",
    # Enums - Entity
    "EntityType", "EntityStatus",
    # Enums - Relation
    "RelationType", "RelationStatus",
    # Enums - Statement
    "StatementType", "ReviewStatus",
    # Enums - Source
    "SourceType", "SourceStatus",
    # Enums - Article
    "ArticleStatus", "ContentType",
    # Enums - Other
    "PropertyValueType", "AliasType", "SearchMode",
    "TaskStatus", "WorkflowStage", "WorkflowStageStatus",
]
