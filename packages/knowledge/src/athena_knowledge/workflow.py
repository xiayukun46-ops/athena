"""Workflow Engine — domain workflow model for knowledge lifecycle.

WorkflowDefinition, WorkflowInstance, WorkflowStep, Transition,
WorkflowState, RetryPolicy, AuditEntry.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from athena_core.base import ValueObject
from athena_core.metadata import StandardMetadata


def utcnow() -> datetime:
    return datetime.now(timezone.utc)

_uid = lambda prefix: f"{prefix}_{__import__('uuid').uuid4().hex[:8]}"


# ── Standard States ──

class WorkflowStates:
    """Standard workflow state constants."""
    CREATED = "CREATED"
    COLLECTING = "COLLECTING"
    VERIFYING = "VERIFYING"
    NORMALIZING = "NORMALIZING"
    ENRICHING = "ENRICHING"
    INDEXING = "INDEXING"
    PUBLISHED = "PUBLISHED"
    FAILED = "FAILED"

    @classmethod
    def all_states(cls) -> list[str]:
        return [cls.CREATED, cls.COLLECTING, cls.VERIFYING, cls.NORMALIZING,
                cls.ENRICHING, cls.INDEXING, cls.PUBLISHED, cls.FAILED]


@dataclass(frozen=True)
class WorkflowState(ValueObject):
    name: str
    description: str = ""
    def _validate(self) -> None:
        if not self.name.strip(): raise ValueError("State name cannot be empty")


# ── WorkflowStep ──

@dataclass(frozen=True)
class WorkflowStep(ValueObject):
    id: str = field(default_factory=lambda: _uid("step"))
    name: str = ""
    description: str = ""
    order: int = 0
    required: bool = True
    def _validate(self) -> None:
        if self.order < 0: raise ValueError("Order must be >= 0")


# ── Transition ──

@dataclass(frozen=True)
class Transition(ValueObject):
    from_state: str
    to_state: str
    condition: str = ""
    def _validate(self) -> None:
        if self.from_state == self.to_state:
            raise ValueError("Self-transition not allowed")


# ── RetryPolicy ──

@dataclass(frozen=True)
class RetryPolicy(ValueObject):
    max_retries: int = 3
    backoff_base: float = 1.0
    backoff_multiplier: float = 2.0
    retryable_errors: tuple[str, ...] = ("NetworkError", "TimeoutError", "RateLimitError")
    def _validate(self) -> None:
        if self.max_retries < 0: raise ValueError("max_retries >= 0")
    def delay_for(self, attempt: int) -> float:
        return self.backoff_base * (self.backoff_multiplier ** attempt)
    def should_retry(self, error_type: str, attempt: int) -> bool:
        return error_type in self.retryable_errors and attempt < self.max_retries


# ── AuditEntry ──

@dataclass(frozen=True)
class AuditEntry(ValueObject):
    id: str = field(default_factory=lambda: _uid("audit"))
    actor: str = ""
    action: str = ""
    from_state: str = ""
    to_state: str = ""
    metadata: dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=utcnow)


# ── WorkflowDefinition ──

@dataclass(frozen=True)
class WorkflowDefinition(ValueObject):
    id: str = field(default_factory=lambda: _uid("wfd"))
    name: str = ""
    description: str = ""
    steps: list[WorkflowStep] = field(default_factory=list)
    initial_state: str = WorkflowStates.CREATED
    allowed_transitions: list[Transition] = field(default_factory=list)
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)

    def _validate(self) -> None:
        if not self.steps: raise ValueError("At least one step required")

    def can_transition(self, from_state: str, to_state: str) -> bool:
        for t in self.allowed_transitions:
            if t.from_state == from_state and t.to_state == to_state:
                return True
        return False

    def get_step_by_order(self, order: int) -> WorkflowStep | None:
        for s in self.steps:
            if s.order == order: return s
        return None

    @staticmethod
    def knowledge_pipeline() -> "WorkflowDefinition":
        return WorkflowDefinition(
            id="wfd_knowledge_pipeline",
            name="KnowledgePipeline",
            description="CREATED->COLLECTING->VERIFYING->NORMALIZING->ENRICHING->INDEXING->PUBLISHED",
            initial_state=WorkflowStates.CREATED,
            steps=[
                WorkflowStep(id="step_create", name="create", order=0),
                WorkflowStep(id="step_collect", name="collect", order=1),
                WorkflowStep(id="step_verify", name="verify", order=2),
                WorkflowStep(id="step_normalize", name="normalize", order=3),
                WorkflowStep(id="step_enrich", name="enrich", order=4),
                WorkflowStep(id="step_index", name="index", order=5),
                WorkflowStep(id="step_publish", name="publish", order=6),
            ],
            allowed_transitions=[
                Transition(WorkflowStates.CREATED, WorkflowStates.COLLECTING),
                Transition(WorkflowStates.COLLECTING, WorkflowStates.VERIFYING),
                Transition(WorkflowStates.VERIFYING, WorkflowStates.NORMALIZING),
                Transition(WorkflowStates.NORMALIZING, WorkflowStates.ENRICHING),
                Transition(WorkflowStates.ENRICHING, WorkflowStates.INDEXING),
                Transition(WorkflowStates.INDEXING, WorkflowStates.PUBLISHED),
            ],
        )


# ── WorkflowInstance ──

@dataclass
class WorkflowInstance:
    id: str = field(default_factory=lambda: _uid("wf"))
    workflow_definition_id: str = ""
    entity_id: str = ""
    current_state: str = WorkflowStates.CREATED
    step_order: int = 0
    retry_count: int = 0
    created_at: datetime = field(default_factory=utcnow)
    completed_at: datetime | None = None
    is_completed: bool = False
    is_failed: bool = False
    audit_history: list[AuditEntry] = field(default_factory=list)
    metadata: StandardMetadata = field(default_factory=StandardMetadata)

    def transition(self, definition: WorkflowDefinition, to_state: str) -> bool:
        if not definition.can_transition(self.current_state, to_state):
            return False
        self._audit("system", "transition", self.current_state, to_state)
        self.current_state = to_state
        self.step_order += 1
        self.retry_count = 0
        return True

    def can_transition(self, definition: WorkflowDefinition, to_state: str) -> bool:
        return definition.can_transition(self.current_state, to_state)

    def complete(self) -> None:
        self.is_completed = True
        self.completed_at = utcnow()

    def fail(self, error_type: str, error_message: str, definition: WorkflowDefinition) -> bool:
        self._audit("system", "fail", self.current_state, WorkflowStates.FAILED,
                     metadata={"error_type": error_type, "error_message": error_message})
        if definition.retry_policy.should_retry(error_type, self.retry_count):
            self.retry_count += 1
            return True
        self.is_failed = True
        self.current_state = WorkflowStates.FAILED
        return False

    def recover(self) -> None:
        if not self.is_failed: raise ValueError("Not failed")
        self.is_failed = False
        self.retry_count = 0

    def _audit(self, actor: str, action: str, from_s: str, to_s: str, metadata: dict | None = None) -> None:
        self.audit_history.append(AuditEntry(
            actor=actor, action=action, from_state=from_s, to_state=to_s,
            metadata=metadata or {},
        ))

    @property
    def current_step(self) -> int:
        return self.step_order

    def __repr__(self) -> str:
        return f"WorkflowInstance(id={self.id}, state={self.current_state}, failed={self.is_failed})"
