"""KnowledgeObject — the single top-level Aggregate Root of Athena.

KnowledgeObject is the central domain concept. It represents a complete
unit of knowledge that encompasses source, entities, relations, statements,
evidence, timeline, versioning, quality scoring, permissions, and lifecycle.

All other domain objects (Entity, Relation, Statement) are components of
a KnowledgeObject, not independent aggregates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from athena_core.base import AggregateRoot, DomainEvent, ValueObject
from athena_core.enums import EntityType, RelationType, ReviewStatus
from athena_core.identity import (
    EntityId, RelationId, StatementId, SourceId, UserId, ArticleId,
    new_entity_id, new_relation_id, new_statement_id, new_source_id, new_user_id,
)
from athena_core.metadata import StandardMetadata

from .quality import QualityScore
from .permission import Permission
from .evidence import Evidence, ContentReference


# ── Value Objects ──

@dataclass(frozen=True)
class EntityName(ValueObject):
    name: str
    language: str
    is_preferred: bool = False
    def _validate(self) -> None:
        if not self.name.strip(): raise ValueError("Name cannot be empty")


@dataclass(frozen=True)
class EntityAlias(ValueObject):
    alias: str
    alias_type: str
    def _validate(self) -> None:
        if not self.alias.strip(): raise ValueError("Alias cannot be empty")


@dataclass(frozen=True)
class EntityProperty(ValueObject):
    key: str
    value: str
    value_type: str = "string"
    confidence: float = 0.5
    source_statement_id: StatementId | None = None
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    needs_arbitration: bool = False
    def _validate(self) -> None:
        if not self.key.strip(): raise ValueError("Key cannot be empty")
        if not 0.0 <= self.confidence <= 1.0: raise ValueError("Confidence 0.0-1.0")


@dataclass(frozen=True)
class StatementSource(ValueObject):
    article_id: ArticleId
    snippet: str = ""
    position: int = 0


# ── Knowledge Components (not aggregates) ──

@dataclass
class KnowledgeEntity:
    id: EntityId = field(default_factory=new_entity_id)
    canonical_name: str = ""
    entity_type: EntityType = EntityType.CONCEPT
    names: list[EntityName] = field(default_factory=list)
    aliases: list[EntityAlias] = field(default_factory=list)
    description: str = ""
    properties: list[EntityProperty] = field(default_factory=list)

    def add_name(self, name: str, language: str, *, is_preferred: bool = False) -> None:
        if is_preferred:
            for n in self.names:
                if n.language == language:
                    object.__setattr__(n, "is_preferred", False)
        self.names.append(EntityName(name=name, language=language, is_preferred=is_preferred))

    def get_preferred_name(self, language: str = "en") -> str:
        for n in self.names:
            if n.language == language and n.is_preferred:
                return n.name
        for n in self.names:
            if n.language == language:
                return n.name
        return self.canonical_name


@dataclass
class KnowledgeRelation:
    id: RelationId = field(default_factory=new_relation_id)
    relation_type: RelationType = RelationType.RELATED_TO
    source_entity_id: EntityId = field(default_factory=new_entity_id)
    target_entity_id: EntityId = field(default_factory=new_entity_id)
    properties: dict = field(default_factory=dict)
    confidence: float = 0.5
    valid_from: datetime | None = None
    valid_until: datetime | None = None

    def is_active_at(self, timestamp: datetime) -> bool:
        if self.valid_from and timestamp < self.valid_from: return False
        if self.valid_until and timestamp > self.valid_until: return False
        return True


@dataclass
class KnowledgeStatement:
    id: StatementId = field(default_factory=new_statement_id)
    predicate: str = ""
    object_value: str = ""
    confidence: float = 0.5
    source: StatementSource = field(default_factory=lambda: StatementSource(article_id=ArticleId("")))
    review_status: ReviewStatus = ReviewStatus.PENDING

    def __post_init__(self) -> None:
        if not self.predicate.strip(): raise ValueError("Predicate cannot be empty")
        if not 0.0 <= self.confidence <= 1.0: raise ValueError("Confidence 0.0-1.0")


# ── Domain Events ──

@dataclass
class KnowledgeCreated(DomainEvent):
    knowledge_id: str = ""
    @property
    def event_type(self) -> str: return "KnowledgeCreated"
    @property
    def aggregate_id(self) -> str: return self.knowledge_id

@dataclass
class KnowledgeVerified(DomainEvent):
    knowledge_id: str = ""
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


# ── KnowledgeObject (Top-Level Aggregate Root) ──

@dataclass
class KnowledgeObject(AggregateRoot):
    id: str = field(default_factory=lambda: f"kobj_{__import__('uuid').uuid4().hex[:8]}")
    canonical_name: str = ""
    description: str = ""

    # Source information
    source_id: SourceId = field(default_factory=new_source_id)

    # Core components
    entities: list[KnowledgeEntity] = field(default_factory=list)
    relations: list[KnowledgeRelation] = field(default_factory=list)
    statements: list[KnowledgeStatement] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)

    # Quality & Permissions
    quality_score: QualityScore = field(default_factory=QualityScore)
    permission: Permission = field(default_factory=Permission.reader)

    # Lifecycle
    status: str = "draft"
    metadata: StandardMetadata = field(default_factory=StandardMetadata)

    @property
    def version(self) -> int:
        return self.metadata.version

    # ── Entity operations ──

    def add_entity(self, entity: KnowledgeEntity) -> KnowledgeEntity:
        self.entities.append(entity)
        self._touch()
        return entity

    def find_entity(self, entity_id: EntityId) -> KnowledgeEntity | None:
        for e in self.entities:
            if e.id == entity_id:
                return e
        return None

    # ── Relation operations ──

    def add_relation(self, relation: KnowledgeRelation) -> KnowledgeRelation:
        if relation.source_entity_id == relation.target_entity_id:
            raise ValueError("Self-referencing relation not allowed")
        self.relations.append(relation)
        self._touch()
        return relation

    # ── Statement operations ──

    def add_statement(self, statement: KnowledgeStatement) -> KnowledgeStatement:
        self.statements.append(statement)
        self.evidence.append(Evidence(
            knowledge_object_id=self.id,
            source_id=self.source_id,
            evidence_type="article_excerpt",
            content_ref=ContentReference(url=str(statement.source.article_id)),
            original_quote=statement.source.snippet,
            location_description=f"position {statement.source.position}",
        ))
        self._touch()
        return statement

    def get_approved_statements(self) -> list[KnowledgeStatement]:
        return [s for s in self.statements if s.review_status == ReviewStatus.APPROVED]

    # ── Lifecycle ──

    def verify(self) -> None:
        if self.status != "draft": raise ValueError(f"Cannot verify in {self.status}")
        self.status = "verified"
        self._touch()
        self.add_event(KnowledgeVerified(knowledge_id=self.id))

    def publish(self) -> None:
        if self.status not in ("draft", "verified"): raise ValueError(f"Cannot publish in {self.status}")
        self.status = "published"
        self._touch()
        self.add_event(KnowledgePublished(knowledge_id=self.id))

    def archive(self, reason: str = "") -> None:
        self.status = "archived"
        self._touch()
        self.add_event(KnowledgeArchived(knowledge_id=self.id, reason=reason))

    def recalculate_quality(self) -> None:
        self.quality_score = QualityScore.compute(
            properties=[p for e in self.entities for p in e.properties],
            source_count=len({e.source_id for e in self.evidence}),
        )
        self._touch()

    def _touch(self) -> None:
        self.metadata = self.metadata.increment_version()
