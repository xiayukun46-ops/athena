"""Evidence entity — the foundation of verifiable knowledge.

Evidence is a Domain Entity (NOT a ValueObject) that links knowledge
claims to their original sources with verifiable content references.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from athena_core.base import Entity, ValueObject
from athena_core.enums import EvidenceType, VerificationStatus
from athena_core.identity import SourceId, new_source_id
from athena_core.metadata import StandardMetadata


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class ContentReference(ValueObject):
    """Extensible reference to the original content source.

    Supports multiple reference types beyond URL: DOI, dataset IDs,
    document IDs, page references, timestamps in video/audio.
    """
    url: str = ""
    doi: str = ""
    dataset_id: str = ""
    document_id: str = ""
    page: str = ""
    section: str = ""
    timestamp: str = ""
    extra: dict[str, str] = field(default_factory=dict)

    @property
    def primary_ref(self) -> str:
        """Best available primary reference."""
        return self.url or self.doi or self.dataset_id or self.document_id or ""

    @property
    def has_exact_location(self) -> bool:
        """Whether a precise location (page/section/timestamp) is available."""
        return bool(self.page or self.section or self.timestamp)


@dataclass
class Evidence(Entity):
    """A verifiable piece of evidence linking a knowledge claim to its source.

    Evidence is an ENTITY — it has a unique identity and its own lifecycle.
    It is NOT a simple value object. Each piece of evidence can be
    independently verified, challenged, or found to be expired.
    """
    id: str = field(default_factory=lambda: f"evid_{__import__('uuid').uuid4().hex[:8]}")
    knowledge_object_id: str = ""
    source_id: SourceId = field(default_factory=new_source_id)

    evidence_type: EvidenceType = EvidenceType.ARTICLE_EXCERPT
    content_ref: ContentReference = field(default_factory=ContentReference)

    original_quote: str = ""
    location_description: str = ""
    captured_at: datetime = field(default_factory=utcnow)

    verification: VerificationStatus = VerificationStatus.PENDING
    verified_by: str = ""
    verified_at: datetime | None = None
    rejection_reason: str = ""

    metadata: StandardMetadata = field(default_factory=StandardMetadata)

    # ── Verification ──

    def verify(self, verified_by: str = "") -> None:
        """Mark evidence as verified."""
        if self.verification not in (VerificationStatus.PENDING, VerificationStatus.EXPIRED):
            raise ValueError(f"Cannot verify evidence in {self.verification.value} status")
        self.verification = VerificationStatus.VERIFIED
        self.verified_by = verified_by
        self.verified_at = utcnow()
        self._touch()

    def reject(self, reason: str = "") -> None:
        """Reject evidence with a reason."""
        if self.verification != VerificationStatus.PENDING:
            raise ValueError(f"Cannot reject evidence in {self.verification.value} status")
        self.verification = VerificationStatus.REJECTED
        self.rejection_reason = reason
        self._touch()

    def mark_expired(self) -> None:
        """Mark evidence as expired (e.g., content no longer accessible)."""
        self.verification = VerificationStatus.EXPIRED
        self._touch()

    # ── Properties ──

    @property
    def is_verified(self) -> bool:
        return self.verification == VerificationStatus.VERIFIED

    @property
    def is_accessible(self) -> bool:
        """Whether the evidence has an accessible primary reference."""
        return self.verification != VerificationStatus.EXPIRED and bool(self.content_ref.primary_ref)

    @property
    def version(self) -> int:
        return self.metadata.version

    # ── Dunder ──

    def __repr__(self) -> str:
        return f"Evidence(id={self.id}, type={self.evidence_type.value}, status={self.verification.value})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Evidence):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def _touch(self) -> None:
        self.metadata = self.metadata.increment_version()
