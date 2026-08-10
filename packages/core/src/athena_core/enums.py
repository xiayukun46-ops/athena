"""Shared enumerations for Athena Knowledge Platform."""

from __future__ import annotations

from enum import StrEnum


class EntityType(StrEnum):
    """Types of knowledge entities. See Knowledge Canon Section 3.1."""
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    EVENT = "event"
    CONCEPT = "concept"
    PRODUCT = "product"
    WORK = "work"
    NATURAL_ENTITY = "natural_entity"


class EntityStatus(StrEnum):
    """Lifecycle states for KnowledgeEntity."""
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    MERGED = "merged"


class RelationStatus(StrEnum):
    """Lifecycle states for KnowledgeRelation."""
    ACTIVE = "active"
    DEPRECATED = "deprecated"


class RelationType(StrEnum):
    """Types of relationships between entities."""
    # Hierarchical
    INSTANCE_OF = "INSTANCE_OF"
    SUBCLASS_OF = "SUBCLASS_OF"
    PART_OF = "PART_OF"
    MEMBER_OF = "MEMBER_OF"
    # Organizational
    WORKS_FOR = "WORKS_FOR"
    FOUNDED = "FOUNDED"
    LED_BY = "LED_BY"
    COLLABORATED_WITH = "COLLABORATED_WITH"
    COMPETES_WITH = "COMPETES_WITH"
    ACQUIRED = "ACQUIRED"
    INVESTED_IN = "INVESTED_IN"
    # Geographic
    LOCATED_IN = "LOCATED_IN"
    BORDERS = "BORDERS"
    NEAR = "NEAR"
    TRAVELED_TO = "TRAVELED_TO"
    # Event
    PARTICIPATED_IN = "PARTICIPATED_IN"
    ORGANIZED = "ORGANIZED"
    CAUSED = "CAUSED"
    PRECEDED = "PRECEDED"
    OCCURRED_AT = "OCCURRED_AT"
    # Knowledge
    RELATED_TO = "RELATED_TO"
    SIMILAR_TO = "SIMILAR_TO"
    OPPOSITE_OF = "OPPOSITE_OF"
    CITED = "CITED"
    INFLUENCED = "INFLUENCED"
    # Content
    PUBLISHED_BY = "PUBLISHED_BY"
    MENTIONS = "MENTIONS"
    EXTRACTS = "EXTRACTS"
    SUPPORTS = "SUPPORTS"
    BELONGS_TO = "BELONGS_TO"
    # Property
    HAS_PROPERTY = "HAS_PROPERTY"
    PRODUCES = "PRODUCES"
    OWNS = "OWNS"
    REGULATED_BY = "REGULATED_BY"


class StatementType(StrEnum):
    """Types of statements."""
    ENTITY_EXTRACTION = "entity_extraction"
    RELATION_EXTRACTION = "relation_extraction"
    MANUAL = "manual"


class ReviewStatus(StrEnum):
    """Review states for statements."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class SourceType(StrEnum):
    """Types of content sources."""
    OFFICIAL_WEBSITE = "official_website"
    SCIENTIFIC_JOURNAL = "scientific_journal"
    GOVERNMENT = "government"
    RESEARCH_INSTITUTION = "research_institution"
    REPOSITORY = "repository"
    DATASET = "dataset"
    API = "api"
    RSS = "rss"
    SCRAPER = "scraper"
    MANUAL = "manual"


class SourceStatus(StrEnum):
    """Lifecycle states for content sources."""
    ACTIVE = "active"
    PAUSED = "paused"
    ERROR = "error"
    DEPRECATED = "deprecated"


class ArticleStatus(StrEnum):
    """Lifecycle states for articles."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DELETED = "deleted"


class ContentType(StrEnum):
    """Types of content."""
    ARTICLE = "article"
    PAPER = "paper"
    REPORT = "report"
    SOCIAL_POST = "social_post"
    TRANSCRIPT = "transcript"


class PropertyValueType(StrEnum):
    """Data types for entity property values."""
    STRING = "string"
    NUMBER = "number"
    DATE = "date"
    BOOLEAN = "boolean"
    JSON = "json"
    URI = "uri"


class AliasType(StrEnum):
    """Types of entity aliases."""
    ACRONYM = "acronym"
    FORMER_NAME = "former_name"
    NICKNAME = "nickname"
    TRANSLITERATION = "transliteration"
    COMMON_MISSPELLING = "common_misspelling"


class SearchMode(StrEnum):
    """Search modes."""
    FULLTEXT = "fulltext"
    VECTOR = "vector"
    HYBRID = "hybrid"


class TaskStatus(StrEnum):
    """Lifecycle states for AI completion tasks."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowStage(StrEnum):
    """Stages in the knowledge pipeline."""
    SCHEDULED = "scheduled"
    FETCHING = "fetching"
    NORMALIZING = "normalizing"
    VERIFYING = "verifying"
    DEDUPLICATING = "deduplicating"
    PUBLISHING = "publishing"
    EXTRACTING = "extracting"
    BUILDING = "building"
    EMBEDDING = "embedding"
    INDEXING = "indexing"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowStageStatus(StrEnum):
    """Status of a workflow stage execution."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"
    DEAD_LETTER = "dead_letter"


class AuthorityLevel(StrEnum):
    """Authority tier for content sources."""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"
    UNVERIFIED = "unverified"


class EvidenceType(StrEnum):
    """Types of evidence supporting knowledge claims."""
    ARTICLE_EXCERPT = "article_excerpt"
    RESEARCH_PAPER = "research_paper"
    DATASET = "dataset"
    OFFICIAL_STATEMENT = "official_statement"
    GOVERNMENT_RECORD = "government_record"
    API_RESPONSE = "api_response"
    IMAGE = "image"
    VIDEO = "video"


class VerificationStatus(StrEnum):
    """Verification state for source authority."""
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    EXPIRED = "expired"


class LicenseType(StrEnum):
    """Content license types for sources."""
    OPEN_ACCESS = "open_access"
    CREATIVE_COMMONS = "creative_commons"
    PUBLIC_DOMAIN = "public_domain"
    COPYRIGHT = "copyright"
    UNKNOWN = "unknown"
