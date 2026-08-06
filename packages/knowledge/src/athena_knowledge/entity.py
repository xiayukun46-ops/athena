"""Knowledge Entity aggregate - the central domain object of Athena.

Defines KnowledgeEntity as defined in the Knowledge Canon
(docs/domain/knowledge-canon.md Section 3.1).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from athena_core.base import AggregateRoot, DomainEvent, ValueObject
from athena_core.enums import (
    AliasType, EntityStatus, EntityType, PropertyValueType,
)
from athena_core.identity import EntityId, StatementId, new_entity_id
from athena_core.metadata import StandardMetadata

from .quality import QualityScore


@dataclass(frozen=True)
class EntityName(ValueObject):
    """A name for an entity in a specific language."""
    name: str
    language: str
    is_preferred: bool = False

    def _validate(self) -> None:
        if not self.name.strip():
            raise ValueError("Entity name cannot be empty")
        if len(self.language) < 2:
            raise ValueError("Language must be ISO 639-1 code")


@dataclass(frozen=True)
class EntityAlias(ValueObject):
    """An alternative name for an entity."""
    alias: str
    alias_type: AliasType

    def _validate(self) -> None:
        if not self.alias.strip():
            raise ValueError("Alias cannot be empty")


@dataclass(frozen=True)
class EntityProperty(ValueObject):
    """A property of an entity using EAV pattern."""
    key: str
    value: str
    value_type: PropertyValueType = PropertyValueType.STRING
    confidence: float = 0.5
    source_statement_id: StatementId | None = None
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    needs_arbitration: bool = False

    def _validate(self) -> None:
        if not self.key.strip():
            raise ValueError("Property key cannot be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be in [0.0, 1.0]")
        if (
            self.valid_from is not None
            and self.valid_until is not None
            and self.valid_until < self.valid_from
        ):
            raise ValueError("valid_until must be >= valid_from")


@dataclass
class KnowledgeEntity(AggregateRoot):
    """A knowledge entity representing a thing in the world."""
    id: EntityId = field(default_factory=new_entity_id)
    canonical_name: str = ""
    entity_type: EntityType = EntityType.CONCEPT
    names: list[EntityName] = field(default_factory=list)
    aliases: list[EntityAlias] = field(default_factory=list)
    description: str = ""
    properties: list[EntityProperty] = field(default_factory=list)
    status: EntityStatus = EntityStatus.DRAFT
    merged_into: EntityId | None = None
    quality_score: QualityScore = field(default_factory=QualityScore)
    metadata: StandardMetadata = field(default_factory=StandardMetadata)

    @property
    def version(self) -> int:
        return self.metadata.version

    def add_name(self, name: str, language: str, *, is_preferred: bool = False) -> None:
        if is_preferred:
            for n in self.names:
                if n.language == language:
                    object.__setattr__(n, "is_preferred", False)
        self.names.append(EntityName(name=name, language=language, is_preferred=is_preferred))
        self._touch()

    def get_preferred_name(self, language: str = "en") -> str:
        for n in self.names:
            if n.language == language and n.is_preferred:
                return n.name
        for n in self.names:
            if n.language == language:
                return n.name
        return self.canonical_name

    def add_alias(self, alias: str, alias_type: AliasType) -> None:
        self.aliases.append(EntityAlias(alias=alias, alias_type=alias_type))
        self._touch()

    def add_property(self, prop: EntityProperty) -> None:
        existing = [p for p in self.properties if p.key == prop.key]
        if existing:
            new_prop = EntityProperty(
                key=prop.key, value=prop.value, value_type=prop.value_type,
                confidence=prop.confidence, source_statement_id=prop.source_statement_id,
                valid_from=prop.valid_from, valid_until=prop.valid_until,
                needs_arbitration=True,
            )
        else:
            new_prop = prop
        self.properties.append(new_prop)
        self._touch()

    def get_property(self, key: str) -> list[EntityProperty]:
        return [p for p in self.properties if p.key == key]

    def activate(self) -> None:
        if self.status != EntityStatus.DRAFT:
            raise ValueError(f"Cannot activate entity in {self.status} status")
        self.status = EntityStatus.ACTIVE
        self._touch()
        self.add_event(EntityActivated(entity_id=self.id))

    def deprecate(self, reason: str = "") -> None:
        self.status = EntityStatus.DEPRECATED
        if reason:
            self.add_property(EntityProperty(
                key="deprecation_reason", value=reason,
                value_type=PropertyValueType.STRING, confidence=1.0,
            ))
        self._touch()
        self.add_event(EntityDeprecated(entity_id=self.id, reason=reason))

    def merge_into(self, target_id: EntityId) -> None:
        self.status = EntityStatus.MERGED
        self.merged_into = target_id
        self._touch()
        self.add_event(EntityMerged(source_id=self.id, target_id=target_id))

    def recalculate_quality(self) -> None:
        self.quality_score = QualityScore.compute(
            properties=self.properties,
            source_count=len({p.source_statement_id for p in self.properties if p.source_statement_id}),
        )
        self._touch()

    def __repr__(self) -> str:
        return f"KnowledgeEntity(id={self.id}, name={self.canonical_name!r}, type={self.entity_type.value})"

    def __str__(self) -> str:
        return self.canonical_name or str(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, KnowledgeEntity):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def _touch(self) -> None:
        self.metadata = self.metadata.increment_version()


@dataclass
class EntityActivated(DomainEvent):
    entity_id: EntityId = field(default_factory=new_entity_id)
    @property
    def event_type(self) -> str: return "EntityActivated"
    @property
    def aggregate_id(self) -> str: return self.entity_id


@dataclass
class EntityDeprecated(DomainEvent):
    entity_id: EntityId = field(default_factory=new_entity_id)
    reason: str = ""
    @property
    def event_type(self) -> str: return "EntityDeprecated"
    @property
    def aggregate_id(self) -> str: return self.entity_id


@dataclass
class EntityMerged(DomainEvent):
    source_id: EntityId = field(default_factory=new_entity_id)
    target_id: EntityId = field(default_factory=new_entity_id)
    @property
    def event_type(self) -> str: return "EntityMerged"
    @property
    def aggregate_id(self) -> str: return self.source_id
