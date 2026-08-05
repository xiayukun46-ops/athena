"""Lifecycle state machines for domain objects.

Defines the valid state transitions for all domain aggregates.
"""

from __future__ import annotations

from enum import StrEnum
from typing import ClassVar


class StateMachine:
    """Generic state machine with transition validation."""

    transitions: ClassVar[dict[str, set[str]]] = {}

    @classmethod
    def can_transition(cls, from_state: str, to_state: str) -> bool:
        """Check if a transition is valid."""
        valid_targets = cls.transitions.get(from_state, set())
        return to_state in valid_targets

    @classmethod
    def validate_transition(cls, from_state: str, to_state: str, object_type: str = "Object") -> None:
        """Validate a state transition, raising ValueError if invalid."""
        if not cls.can_transition(from_state, to_state):
            raise ValueError(
                f"{object_type} cannot transition from {from_state} to {to_state}"
            )


class EntityLifecycle(StateMachine):
    """Lifecycle for KnowledgeEntity.

    DRAFT → ACTIVE → DEPRECATED → MERGED
    """
    transitions: ClassVar[dict[str, set[str]]] = {
        "draft": {"active", "merged"},
        "active": {"deprecated", "merged"},
        "deprecated": {"merged"},
        "merged": set(),
    }


class RelationLifecycle(StateMachine):
    """Lifecycle for KnowledgeRelation.

    ACTIVE → DEPRECATED
    """
    transitions: ClassVar[dict[str, set[str]]] = {
        "active": {"deprecated"},
        "deprecated": set(),
    }


class StatementLifecycle(StateMachine):
    """Lifecycle for Statement.

    PENDING → APPROVED | REJECTED
    """
    transitions: ClassVar[dict[str, set[str]]] = {
        "pending": {"approved", "rejected"},
        "approved": set(),
        "rejected": set(),
    }


class ArticleLifecycle(StateMachine):
    """Lifecycle for Article.

    DRAFT → PUBLISHED → ARCHIVED → DELETED
    """
    transitions: ClassVar[dict[str, set[str]]] = {
        "draft": {"published", "deleted"},
        "published": {"archived", "deleted"},
        "archived": {"deleted"},
        "deleted": set(),
    }


class SourceLifecycle(StateMachine):
    """Lifecycle for Source.

    ACTIVE ⇄ PAUSED → ERROR → DEPRECATED
    """
    transitions: ClassVar[dict[str, set[str]]] = {
        "active": {"paused", "error", "deprecated"},
        "paused": {"active", "error", "deprecated"},
        "error": {"active", "deprecated"},
        "deprecated": set(),
    }


class TaskLifecycle(StateMachine):
    """Lifecycle for CompletionTask.

    PENDING → RUNNING → COMPLETED | FAILED
    """
    transitions: ClassVar[dict[str, set[str]]] = {
        "pending": {"running"},
        "running": {"completed", "failed"},
        "completed": set(),
        "failed": {"pending"},
    }
