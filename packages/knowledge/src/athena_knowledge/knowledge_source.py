"""KnowledgeSource aggregate — authoritative content source management.

Defines the complete KnowledgeSource domain model including authority
verification, trust scoring, collector configuration, and lifecycle.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from athena_core.base import AggregateRoot, ValueObject
from athena_core.enums import (
    AuthorityLevel, LicenseType, SourceType, SourceStatus, VerificationStatus,
)
from athena_core.identity import SourceId, new_source_id
from athena_core.metadata import StandardMetadata


# ── Value Objects ──

@dataclass(frozen=True)
class Authority(ValueObject):
    """The publishing authority behind a source.

    Defines who published the content, their trustworthiness level,
    and verification status.
    """
    name: str = ""
    url: str = ""
    publisher: str = ""
    level: AuthorityLevel = AuthorityLevel.UNVERIFIED
    verification: VerificationStatus = VerificationStatus.PENDING
    score: float = 0.5

    def _validate(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("Authority score must be in [0.0, 1.0]")

    def verify(self) -> "Authority":
        """Return a verified copy of this authority."""
        return Authority(
            name=self.name, url=self.url, publisher=self.publisher,
            level=self.level, verification=VerificationStatus.VERIFIED,
            score=self.score,
        )

    def reject(self) -> "Authority":
        """Return a rejected copy of this authority."""
        return Authority(
            name=self.name, url=self.url, publisher=self.publisher,
            level=self.level, verification=VerificationStatus.REJECTED,
            score=self.score,
        )


@dataclass(frozen=True)
class TrustScore(ValueObject):
    """Extensible trust evaluation for a source.

    Algorithm-agnostic design: new scoring dimensions can be added
    without modifying existing consumers.
    """
    credibility: float = 0.5
    accuracy: float = 0.5
    transparency: float = 0.5
    consistency: float = 0.5
    timeliness: float = 0.5
    domain_authority: float = 0.5
    dimensions: dict[str, float] = field(default_factory=dict)

    def _validate(self) -> None:
        for name, val in [
            ("credibility", self.credibility), ("accuracy", self.accuracy),
            ("transparency", self.transparency), ("consistency", self.consistency),
            ("timeliness", self.timeliness), ("domain_authority", self.domain_authority),
        ]:
            if not 0.0 <= val <= 1.0:
                raise ValueError(f"{name} must be in [0.0, 1.0]")

    @property
    def overall(self) -> float:
        """Weighted overall trust score including extension dimensions."""
        base = [self.credibility, self.accuracy, self.transparency,
                self.consistency, self.timeliness, self.domain_authority]
        all_dims = base + list(self.dimensions.values())
        return round(sum(all_dims) / len(all_dims), 4) if all_dims else 0.0

    def with_dimension(self, name: str, value: float) -> "TrustScore":
        """Add an extension dimension without modifying the base schema."""
        dims = dict(self.dimensions)
        dims[name] = value
        return TrustScore(
            credibility=self.credibility, accuracy=self.accuracy,
            transparency=self.transparency, consistency=self.consistency,
            timeliness=self.timeliness, domain_authority=self.domain_authority,
            dimensions=dims,
        )


@dataclass(frozen=True)
class CollectorConfig(ValueObject):
    """Configuration for the collector pipeline."""
    interval_seconds: int = 300
    timeout_seconds: int = 30
    max_items_per_fetch: int = 100
    user_agent: str = "Athena/1.0"
    respect_robots_txt: bool = True
    custom_headers: dict[str, str] = field(default_factory=dict)

    def _validate(self) -> None:
        if self.interval_seconds < 0:
            raise ValueError("Interval must be >= 0")
        if self.timeout_seconds <= 0:
            raise ValueError("Timeout must be > 0")


@dataclass(frozen=True)
class VerificationPolicy(ValueObject):
    """Policy for verifying a source's authority and content."""
    require_human_review: bool = False
    auto_verify_threshold: float = 0.8
    recheck_interval_days: int = 90
    max_consecutive_errors: int = 10
    allowed_content_types: list[str] = field(default_factory=list)

    def _validate(self) -> None:
        if not 0.0 <= self.auto_verify_threshold <= 1.0:
            raise ValueError("Threshold must be in [0.0, 1.0]")
        if self.recheck_interval_days < 1:
            raise ValueError("Recheck interval must be >= 1 day")


# ── Aggregate Root ──

@dataclass
class KnowledgeSource(AggregateRoot):
    """A global authoritative knowledge source.

    Manages the full lifecycle of a content source: identity, authority
    verification, trust scoring, collection configuration, and status.

    This is an independent Aggregate Root — not a component of KnowledgeObject.
    """
    id: SourceId = field(default_factory=new_source_id)
    name: str = ""
    source_type: SourceType = SourceType.OFFICIAL_WEBSITE
    authority: Authority = field(default_factory=Authority)
    trust_score: TrustScore = field(default_factory=TrustScore)
    verification_policy: VerificationPolicy = field(default_factory=VerificationPolicy)
    collector_config: CollectorConfig = field(default_factory=CollectorConfig)

    # Metadata
    language: str = "en"
    region: str = ""
    license_type: LicenseType = LicenseType.UNKNOWN
    tags: list[str] = field(default_factory=list)
    description: str = ""

    # Lifecycle
    status: SourceStatus = SourceStatus.ACTIVE
    error_count: int = 0
    metadata: StandardMetadata = field(default_factory=StandardMetadata)

    @property
    def version(self) -> int:
        return self.metadata.version

    # ── Authority ──

    def verify_authority(self) -> None:
        """Mark source authority as verified."""
        self.authority = self.authority.verify()
        self._touch()

    def reject_authority(self) -> None:
        """Mark source authority as rejected."""
        self.authority = self.authority.reject()
        self._touch()

    def update_trust(self, score: TrustScore) -> None:
        """Update trust evaluation with a new score."""
        self.trust_score = score
        self._touch()

    # ── Lifecycle ──

    def pause(self) -> None:
        """Pause content collection."""
        if self.status != SourceStatus.ACTIVE:
            raise ValueError(f"Cannot pause source in {self.status.value} status")
        self.status = SourceStatus.PAUSED
        self._touch()

    def resume(self) -> None:
        """Resume content collection."""
        if self.status != SourceStatus.PAUSED:
            raise ValueError(f"Cannot resume source in {self.status.value} status")
        self.status = SourceStatus.ACTIVE
        self._touch()

    def record_error(self) -> None:
        """Record a collection error. Auto-mark as error after threshold."""
        self.error_count += 1
        if self.error_count >= self.verification_policy.max_consecutive_errors:
            self.status = SourceStatus.ERROR
        self._touch()

    def recover_from_error(self) -> None:
        """Recover from error state back to active."""
        if self.status != SourceStatus.ERROR:
            raise ValueError(f"Cannot recover source in {self.status.value} status")
        self.status = SourceStatus.ACTIVE
        self.error_count = 0
        self._touch()

    def deprecate(self) -> None:
        """Deprecate this source permanently."""
        self.status = SourceStatus.DEPRECATED
        self._touch()

    @property
    def is_collectable(self) -> bool:
        """Whether this source is ready for collection."""
        return self.status == SourceStatus.ACTIVE

    @property
    def is_verified(self) -> bool:
        """Whether the authority has been verified."""
        return self.authority.verification == VerificationStatus.VERIFIED

    # ── Internal ──

    def __repr__(self) -> str:
        return f"KnowledgeSource(id={self.id}, name={self.name!r}, type={self.source_type.value})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, KnowledgeSource):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def _touch(self) -> None:
        self.metadata = self.metadata.increment_version()
