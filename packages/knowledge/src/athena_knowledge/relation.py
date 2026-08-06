"""Knowledge Relation aggregate.

Defines KnowledgeRelation as defined in the Knowledge Canon
(docs/domain/knowledge-canon.md Section 3.2).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from athena_core.base import AggregateRoot, DomainEvent, ValueObject
from athena_core.enums import RelationStatus, RelationType
from athena_core.identity import (
    EntityId, RelationId, StatementId, new_entity_id, new_relation_id,
)
from athena_core.metadata import StandardMetadata


@dataclass
class KnowledgeRelation(AggregateRoot):
    """A directed relationship between two knowledge entities.

    As defined in Knowledge Canon Section 3.2.
    """
    id: RelationId = field(default_factory=new_relation_id)
    relation_type: RelationType = RelationType.RELATED_TO
    source_entity_id: EntityId = field(default_factory=new_entity_id)
    target_entity_id: EntityId = field(default_factory=new_entity_id)
    properties: dict[str, str] = field(default_factory=dict)
    statements: list[StatementId] = field(default_factory=list)
    confidence: float = 0.5
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    status: RelationStatus = RelationStatus.ACTIVE
    metadata: StandardMetadata = field(default_factory=StandardMetadata)

    def __post_init__(self) -> None:
        if self.source_entity_id == self.target_entity_id:
            raise ValueError("Source and target entity must be different")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be in [0.0, 1.0]")

    @property
    def version(self) -> int:
        return self.metadata.version

    def add_statement(self, statement_id: StatementId) -> None:
        """Add a supporting statement."""
        if statement_id not in self.statements:
            self.statements.append(statement_id)
            self._recalculate_confidence()
            self._touch()

    def deprecate(self, reason: str = "") -> None:
        """Deprecate this relation."""
        self.status = RelationStatus.DEPRECATED
        if reason:
            self.properties["deprecation_reason"] = reason
        self._touch()
        self.add_event(RelationDeprecated(relation_id=self.id, reason=reason))

    def is_active_at(self, timestamp: datetime) -> bool:
        """Check if this relation is active at a given point in time."""
        if self.valid_from and timestamp < self.valid_from:
            return False
        if self.valid_until and timestamp > self.valid_until:
            return False
        return self.status == RelationStatus.ACTIVE

    def _recalculate_confidence(self) -> None:
        """Recalculate confidence based on supporting statements."""
        if not self.statements:
            self.confidence = 0.0
            return
        decay = min(1.0, 1.0 / (len(self.statements) ** 0.3))
        self.confidence = min(0.5 + 0.1 * len(self.statements), 1.0) * decay

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, KnowledgeRelation):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"KnowledgeRelation(id={self.id}, type={self.relation_type.value}, status={self.status.value})"

    def _touch(self) -> None:
        self.metadata = self.metadata.increment_version()


@dataclass
class RelationDeprecated(DomainEvent):
    relation_id: RelationId = field(default_factory=new_relation_id)
    reason: str = ""

    @property
    def event_type(self) -> str:
        return "RelationDeprecated"

    @property
    def aggregate_id(self) -> str:
        return self.relation_id
