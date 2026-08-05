"""Metadata value objects for Athena domain objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from .base import ValueObject, utcnow


@dataclass(frozen=True)
class StandardMetadata(ValueObject):
    """Standard metadata attached to every domain object.

    As defined in Knowledge Canon Section 3.9.
    """
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)
    deleted_at: datetime | None = None
    version: int = 1

    def _validate(self) -> None:
        if self.version < 1:
            raise ValueError("Version must be >= 1")
        if self.updated_at < self.created_at:
            raise ValueError("updated_at must be >= created_at")

    def touch(self) -> "StandardMetadata":
        """Return a new metadata with updated timestamp."""
        return StandardMetadata(
            created_at=self.created_at,
            updated_at=utcnow(),
            deleted_at=self.deleted_at,
            version=self.version,
        )

    def increment_version(self) -> "StandardMetadata":
        """Return a new metadata with incremented version."""
        return StandardMetadata(
            created_at=self.created_at,
            updated_at=utcnow(),
            deleted_at=self.deleted_at,
            version=self.version + 1,
        )

    def soft_delete(self) -> "StandardMetadata":
        """Return a new metadata with deleted_at set."""
        return StandardMetadata(
            created_at=self.created_at,
            updated_at=utcnow(),
            deleted_at=utcnow(),
            version=self.version,
        )

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
