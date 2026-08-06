"""KnowledgeSource aggregate — content source configuration and trust.

Defines the authoritative source of knowledge content including
authority, trust scoring, and collector configuration.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from athena_core.base import AggregateRoot, ValueObject
from athena_core.enums import SourceType, SourceStatus
from athena_core.identity import SourceId, new_source_id
from athena_core.metadata import StandardMetadata


@dataclass(frozen=True)
class Authority(ValueObject):
    """The publishing authority behind a source."""
    name: str = ""
    url: str = ""
    publisher: str = ""
    license_type: str = ""
    language: str = "en"
    region: str = ""


@dataclass(frozen=True)
class TrustScore(ValueObject):
    """Multi-dimensional trust evaluation for a source."""
    credibility: float = 0.5
    accuracy: float = 0.5
    bias_leaning: str = ""
    fact_check_rating: str = ""
    domain_authority: float = 0.5

    def _validate(self) -> None:
        for v in [self.credibility, self.accuracy, self.domain_authority]:
            if not 0.0 <= v <= 1.0:
                raise ValueError("Trust dimensions must be in [0.0, 1.0]")

    @property
    def overall(self) -> float:
        return round((self.credibility + self.accuracy + self.domain_authority) / 3, 4)


@dataclass(frozen=True)
class CollectorConfig(ValueObject):
    """Configuration for the content collector pipeline."""
    interval_seconds: int = 300
    timeout_seconds: int = 30
    max_items_per_fetch: int = 100
    user_agent: str = "Athena/1.0"
    respect_robots_txt: bool = True
    custom_headers: dict = field(default_factory=dict)

    def _validate(self) -> None:
        if self.interval_seconds < 0:
            raise ValueError("Interval must be >= 0")
        if self.timeout_seconds <= 0:
            raise ValueError("Timeout must be > 0")


@dataclass
class KnowledgeSource(AggregateRoot):
    """A content source aggregate.

    Represents an authoritative source of knowledge that the Collector
    pipeline can ingest from. Tracks trust metrics and lifecycle.

    As defined in Knowledge Canon Section 3.6.
    """
    id: SourceId = field(default_factory=new_source_id)
    authority: Authority = field(default_factory=Authority)
    source_type: SourceType = SourceType.RSS
    trust_score: TrustScore = field(default_factory=TrustScore)
    collector_config: CollectorConfig = field(default_factory=CollectorConfig)
    status: SourceStatus = SourceStatus.ACTIVE
    metadata: StandardMetadata = field(default_factory=StandardMetadata)

    @property
    def version(self) -> int:
        return self.metadata.version

    def update_trust(self, score: TrustScore) -> None:
        """Update trust evaluation."""
        self.trust_score = score
        self._touch()

    def pause(self) -> None:
        """Pause content collection from this source."""
        if self.status != SourceStatus.ACTIVE:
            raise ValueError(f"Cannot pause source in {self.status} status")
        self.status = SourceStatus.PAUSED
        self._touch()

    def resume(self) -> None:
        """Resume content collection."""
        if self.status != SourceStatus.PAUSED:
            raise ValueError(f"Cannot resume source in {self.status} status")
        self.status = SourceStatus.ACTIVE
        self._touch()

    def mark_error(self) -> None:
        """Mark source as errored."""
        self.status = SourceStatus.ERROR
        self._touch()

    def deprecate(self) -> None:
        """Deprecate this source."""
        self.status = SourceStatus.DEPRECATED
        self._touch()

    def _touch(self) -> None:
        self.metadata = self.metadata.increment_version()
