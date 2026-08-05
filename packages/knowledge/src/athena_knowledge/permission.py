"""Permission model for Athena domain objects.

Defines the permission system as specified in Knowledge Canon Section 3.12.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from athena_core.base import ValueObject


class PermissionScope(StrEnum):
    """Scopes of access control."""
    READ_SOURCES = "read:sources"
    WRITE_SOURCES = "write:sources"
    READ_ARTICLES = "read:articles"
    WRITE_ARTICLES = "write:articles"
    READ_ENTITIES = "read:entities"
    WRITE_ENTITIES = "write:entities"
    MERGE_ENTITIES = "merge:entities"
    READ_RELATIONS = "read:relations"
    WRITE_RELATIONS = "write:relations"
    READ_STATEMENTS = "read:statements"
    WRITE_STATEMENTS = "write:statements"
    APPROVE_STATEMENTS = "approve:statements"
    SEARCH = "search"
    AI_CHAT = "ai:chat"
    AI_SUMMARIZE = "ai:summarize"
    AI_TRANSLATE = "ai:translate"
    AI_EXTRACT = "ai:extract"
    MANAGE_PLUGINS = "manage:plugins"
    MANAGE_USERS = "manage:users"
    VIEW_ANALYTICS = "view:analytics"


@dataclass(frozen=True)
class Permission(ValueObject):
    """A permission definition for an agent or user.

    As defined in Knowledge Canon Section 3.12.
    """
    scope: list[PermissionScope] = field(default_factory=list)
    constraints: dict[str, str] = field(default_factory=dict)

    def allows(self, scope: PermissionScope) -> bool:
        """Check if this permission allows a specific scope."""
        return scope in self.scope

    def allows_any(self, scopes: list[PermissionScope]) -> bool:
        """Check if this permission allows any of the given scopes."""
        return any(s in self.scope for s in scopes)

    @staticmethod
    def reader() -> "Permission":
        """Create a read-only permission set."""
        return Permission(scope=[
            PermissionScope.READ_SOURCES,
            PermissionScope.READ_ARTICLES,
            PermissionScope.READ_ENTITIES,
            PermissionScope.READ_RELATIONS,
            PermissionScope.READ_STATEMENTS,
            PermissionScope.SEARCH,
        ])

    @staticmethod
    def contributor() -> "Permission":
        """Create a contributor permission set (read + write entities/relations)."""
        return Permission(scope=Permission.reader().scope + [
            PermissionScope.WRITE_ENTITIES,
            PermissionScope.WRITE_RELATIONS,
            PermissionScope.WRITE_STATEMENTS,
        ])

    @staticmethod
    def moderator() -> "Permission":
        """Create a moderator permission set."""
        return Permission(scope=Permission.contributor().scope + [
            PermissionScope.MERGE_ENTITIES,
            PermissionScope.APPROVE_STATEMENTS,
        ])

    @staticmethod
    def admin() -> "Permission":
        """Create an admin permission set."""
        return Permission(scope=list(PermissionScope))
