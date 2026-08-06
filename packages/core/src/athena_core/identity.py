"""Identity types for Athena Knowledge Platform.

All domain objects use typed identifiers with predefined prefixes
as defined in the Knowledge Canon (docs/domain/knowledge-canon.md).
"""

from __future__ import annotations

import uuid
from typing import NewType

# ── Prefix constants ──

PREFIX_ENTITY = "ent"
PREFIX_RELATION = "rel"
PREFIX_STATEMENT = "stmt"
PREFIX_ARTICLE = "art"
PREFIX_SOURCE = "src"
PREFIX_USER = "usr"
PREFIX_TASK = "tsk"
PREFIX_INDEX = "idx"
PREFIX_PLUGIN = "plg"

# ── Typed ID newtypes ──

EntityId = NewType("EntityId", str)
RelationId = NewType("RelationId", str)
StatementId = NewType("StatementId", str)
ArticleId = NewType("ArticleId", str)
SourceId = NewType("SourceId", str)
UserId = NewType("UserId", str)
TaskId = NewType("TaskId", str)
IndexId = NewType("IndexId", str)
PluginId = NewType("PluginId", str)
EventId = NewType("EventId", str)


def generate_id(prefix: str, *, short_uuid_len: int = 8) -> str:
    """Generate a typed identifier.

    Format: {prefix}_{uuid_short}

    Args:
        prefix: Identifier prefix (e.g. 'ent', 'art')
        short_uuid_len: Length of UUID hex substring (default 8)

    Returns:
        Typed ID string like 'ent_a1b2c3d4'
    """
    short = uuid.uuid4().hex[:short_uuid_len]
    return f"{prefix}_{short}"


def is_valid_id(value: str, prefix: str) -> bool:
    """Check if a string is a valid typed identifier."""
    if not value:
        return False
    parts = value.split("_", 1)
    if len(parts) != 2:
        return False
    return parts[0] == prefix and len(parts[1]) >= 6


def parse_id(value: str) -> tuple[str, str]:
    """Parse a typed ID into (prefix, uuid_part).

    Args:
        value: A typed ID string like 'ent_a1b2c3d4'

    Returns:
        Tuple of (prefix, uuid_short)

    Raises:
        ValueError: If the ID format is invalid.
    """
    if not value or "_" not in value:
        raise ValueError(f"Invalid ID format: {value!r}")
    prefix, uuid_part = value.split("_", 1)
    if not prefix or len(uuid_part) < 6:
        raise ValueError(f"Invalid ID format: {value!r}")
    return prefix, uuid_part


# ── Convenience generators ──

def new_entity_id() -> EntityId:
    return EntityId(generate_id(PREFIX_ENTITY))


def new_relation_id() -> RelationId:
    return RelationId(generate_id(PREFIX_RELATION))


def new_statement_id() -> StatementId:
    return StatementId(generate_id(PREFIX_STATEMENT))


def new_article_id() -> ArticleId:
    return ArticleId(generate_id(PREFIX_ARTICLE))


def new_source_id() -> SourceId:
    return SourceId(generate_id(PREFIX_SOURCE))


def new_user_id() -> UserId:
    return UserId(generate_id(PREFIX_USER))


def new_task_id() -> TaskId:
    return TaskId(generate_id(PREFIX_TASK))


def new_event_id() -> EventId:
    return EventId(generate_id(PREFIX_ENTITY))
