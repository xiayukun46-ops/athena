"""Athena Knowledge — domain models for the Knowledge bounded context.

This package implements the Knowledge Canon (docs/domain/knowledge-canon.md)
as pure Python domain objects with no framework dependencies.
"""

from .entity import (
    KnowledgeEntity, EntityName, EntityAlias, EntityProperty,
    EntityActivated, EntityDeprecated, EntityMerged,
)
from .relation import KnowledgeRelation, RelationDeprecated
from .statement import Statement, StatementSource, StatementApproved, StatementRejected
from .quality import QualityScore
from .permission import Permission, PermissionScope
from .lifecycle import (
    StateMachine,
    EntityLifecycle, RelationLifecycle, StatementLifecycle,
    ArticleLifecycle, SourceLifecycle, TaskLifecycle,
)
from .workflow import (
    RetryPolicy, WorkflowStageResult, WorkflowContext, WorkflowAuditEntry,
)
from .events import (
    ArticleFetched, ArticlePublished,
    EntityCreated, EntityUpdated,
    RelationCreated,
    SearchPerformed,
    TaskStarted, TaskCompleted,
    UserRegistered,
)

__all__ = [
    # Entity
    "KnowledgeEntity", "EntityName", "EntityAlias", "EntityProperty",
    "EntityActivated", "EntityDeprecated", "EntityMerged",
    # Relation
    "KnowledgeRelation", "RelationDeprecated",
    # Statement
    "Statement", "StatementSource", "StatementApproved", "StatementRejected",
    # Quality
    "QualityScore",
    # Permission
    "Permission", "PermissionScope",
    # Lifecycle
    "StateMachine",
    "EntityLifecycle", "RelationLifecycle", "StatementLifecycle",
    "ArticleLifecycle", "SourceLifecycle", "TaskLifecycle",
    # Workflow
    "RetryPolicy", "WorkflowStageResult", "WorkflowContext", "WorkflowAuditEntry",
    # Events
    "ArticleFetched", "ArticlePublished",
    "EntityCreated", "EntityUpdated",
    "RelationCreated",
    "SearchPerformed",
    "TaskStarted", "TaskCompleted",
    "UserRegistered",
]
