"""Statement aggregate — the provenance layer of Athena.

Defines Statement as defined in the Knowledge Canon
(docs/domain/knowledge-canon.md Section 3.3).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from athena_core.base import AggregateRoot, DomainEvent, ValueObject
from athena_core.enums import ReviewStatus, StatementType
from athena_core.identity import (
    ArticleId, EntityId, StatementId, UserId, new_article_id,
    new_entity_id, new_statement_id, new_user_id,
)
from athena_core.metadata import StandardMetadata


@dataclass(frozen=True)
class StatementSource(ValueObject):
    """The provenance information for a statement.

    As defined in Knowledge Canon Section 3.3.
    """
    article_id: ArticleId = field(default_factory=new_article_id)
    snippet: str = ""
    position: int = 0

    def _validate(self) -> None:
        if self.position < 0:
            raise ValueError("Position must be >= 0")


@dataclass
class Statement(AggregateRoot):
    """A traceable assertion about an entity or relation.

    Statements form the provenance layer of Athena's Knowledge Triangle.
    Every piece of structured knowledge must be traceable back to one or
    more statements, which in turn reference original source articles.

    As defined in Knowledge Canon Section 3.3.
    """
    id: StatementId = field(default_factory=new_statement_id)
    statement_type: StatementType = StatementType.ENTITY_EXTRACTION
    subject_id: EntityId = field(default_factory=new_entity_id)
    predicate: str = ""
    object_value: str = ""
    confidence: float = 0.5
    extraction_method: str = ""
    source: StatementSource = field(default_factory=StatementSource)
    reviewer_id: UserId | None = None
    review_status: ReviewStatus = ReviewStatus.PENDING
    review_comment: str = ""
    metadata: StandardMetadata = field(default_factory=StandardMetadata)

    def __post_init__(self) -> None:
        if not self.predicate.strip():
            raise ValueError("Statement predicate cannot be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be in [0.0, 1.0]")

    @property
    def version(self) -> int:
        return self.metadata.version

    def approve(self, reviewer_id: UserId, comment: str = "") -> None:
        """Approve this statement."""
        if self.review_status != ReviewStatus.PENDING:
            raise ValueError(f"Cannot approve statement in {self.review_status} status")
        self.reviewer_id = reviewer_id
        self.review_status = ReviewStatus.APPROVED
        self.review_comment = comment
        self._touch()
        self.add_event(StatementApproved(
            statement_id=self.id, reviewer_id=reviewer_id, comment=comment,
        ))

    def reject(self, reviewer_id: UserId, reason: str) -> None:
        """Reject this statement."""
        if self.review_status != ReviewStatus.PENDING:
            raise ValueError(f"Cannot reject statement in {self.review_status} status")
        self.reviewer_id = reviewer_id
        self.review_status = ReviewStatus.REJECTED
        self.review_comment = reason
        self._touch()
        self.add_event(StatementRejected(
            statement_id=self.id, reviewer_id=reviewer_id, reason=reason,
        ))

    @property
    def is_approved(self) -> bool:
        return self.review_status == ReviewStatus.APPROVED

    @property
    def is_rejected(self) -> bool:
        return self.review_status == ReviewStatus.REJECTED

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Statement):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"Statement(id={self.id}, predicate={self.predicate!r}, status={self.review_status.value})"

    def _touch(self) -> None:
        self.metadata = self.metadata.increment_version()


@dataclass
class StatementApproved(DomainEvent):
    statement_id: StatementId = field(default_factory=new_statement_id)
    reviewer_id: UserId = field(default_factory=new_user_id)
    comment: str = ""

    @property
    def event_type(self) -> str:
        return "StatementApproved"

    @property
    def aggregate_id(self) -> str:
        return self.statement_id


@dataclass
class StatementRejected(DomainEvent):
    statement_id: StatementId = field(default_factory=new_statement_id)
    reviewer_id: UserId = field(default_factory=new_user_id)
    reason: str = ""

    @property
    def event_type(self) -> str:
        return "StatementRejected"

    @property
    def aggregate_id(self) -> str:
        return self.statement_id
