"""DDD base classes for Athena Knowledge Platform.

Provides AggregateRoot, Entity, ValueObject, and DomainEvent base classes
as defined in the Shared Kernel (docs/domain/shared-kernel.md).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from .identity import EventId, new_event_id


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class DomainEvent(ABC):
    """Base class for all domain events.

    Events are immutable records of something that happened.
    They are the only means of communication between bounded contexts.
    """
    event_id: EventId = field(default_factory=new_event_id)
    occurred_at: datetime = field(default_factory=utcnow)

    @property
    @abstractmethod
    def event_type(self) -> str:
        """Event type identifier (e.g., 'ArticleFetched')."""
        ...

    @property
    @abstractmethod
    def aggregate_id(self) -> str:
        """ID of the aggregate root that emitted this event."""
        ...

    @property
    def aggregate_type(self) -> str:
        """Type name of the aggregate root."""
        return self.__class__.__name__.replace("Event", "")


@dataclass
class EventMetadata:
    """Metadata for domain events."""
    correlation_id: UUID = field(default_factory=uuid4)
    causation_id: UUID | None = None
    source_context: str = ""
    version: int = 1


@dataclass
class AggregateRoot(ABC):
    """Base class for aggregate roots.

    Aggregates are the transactional consistency boundary.
    All changes to entities within an aggregate must go through the root.
    """
    _events: list[DomainEvent] = field(default_factory=list, init=False, repr=False)

    def add_event(self, event: DomainEvent) -> None:
        """Record a domain event to be published after the transaction."""
        self._events.append(event)

    def collect_events(self) -> list[DomainEvent]:
        """Collect and clear pending domain events."""
        events = self._events.copy()
        self._events.clear()
        return events

    @property
    def pending_events(self) -> list[DomainEvent]:
        """Get pending events without clearing them."""
        return self._events.copy()



@dataclass
class Entity(ABC):
    """Base class for domain entities.

    Entities have a unique identity that persists through state changes.
    Unlike value objects, two entities with identical attributes are not equal
    unless they share the same identity.
    """

    @property
    @abstractmethod
    def id(self) -> Any:
        """Entity unique identifier."""
        ...

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass(frozen=True)
class ValueObject(ABC):
    """Base class for immutable value objects.

    Value objects have no identity and are compared by their attribute values.
    Two value objects with the same attributes are considered equal.
    """

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        """Override to add validation logic."""
        pass
