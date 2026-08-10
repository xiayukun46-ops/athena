"""Workflow Engine — domain workflow model for knowledge lifecycle.

Defines WorkflowDefinition, WorkflowInstance, WorkflowStep,
state transitions, retry policy, failure handling, and audit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from athena_core.base import ValueObject
from athena_core.metadata import StandardMetadata


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


# ── Workflow States ──

@dataclass(frozen=True)
class WorkflowState(ValueObject):
    """A named state in a workflow."""
    name: str
    description: str = ""

    def _validate(self) -> None:
        if not self.name.strip():
            raise ValueError("State name cannot be empty")


# ── Transition ──

@dataclass(frozen=True)
class Transition(ValueObject):
    """A valid transition between two workflow states."""
    from_state: str
    to_state: str
    name: str = ""
    requires_validation: bool = True

    def _validate(self) -> None:
        if self.from_state == self.to_state:
            raise ValueError("Transition from and to must be different")


# ── RetryPolicy ──

@dataclass(frozen=True)
class RetryPolicy(ValueObject):
    """Exponential backoff retry policy."""
    max_retries: int = 3
    backoff_base: float = 1.0
    backoff_multiplier: float = 2.0
    retryable_errors: tuple[str, ...] = ("NetworkError", "TimeoutError", "RateLimitError")

    def _validate(self) -> None:
        if self.max_retries < 0:
            raise ValueError("max_retries must be >= 0")

    def delay_for(self, attempt: int) -> float:
        return self.backoff_base * (self.backoff_multiplier ** attempt)

    def should_retry(self, error_type: str, attempt: int) -> bool:
        return error_type in self.retryable_errors and attempt < self.max_retries


# ── WorkflowStep ──

@dataclass(frozen=True)
class WorkflowStep(ValueObject):
    """A step within a workflow definition."""
    name: str
    state: str
    description: str = ""
    is_required: bool = True
    timeout_seconds: int = 300

    def _validate(self) -> None:
        if not self.name.strip():
            raise ValueError("Step name cannot be empty")


# ── WorkflowDefinition ──

@dataclass(frozen=True)
class WorkflowDefinition(ValueObject):
    """Immutable definition of a workflow process."""
    name: str
    version: str = "1.0"
    description: str = ""
    steps: list[WorkflowStep] = field(default_factory=list)
    transitions: list[Transition] = field(default_factory=list)
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)

    def _validate(self) -> None:
        if not self.name.strip():
            raise ValueError("Workflow name cannot be empty")
        if not self.steps:
            raise ValueError("Workflow must have at least one step")

    def get_step(self, name: str) -> WorkflowStep | None:
        for s in self.steps:
            if s.name == name:
                return s
        return None

    def can_transition(self, from_state: str, to_state: str) -> bool:
        for t in self.transitions:
            if t.from_state == from_state and t.to_state == to_state:
                return True
        return False

    @staticmethod
    def knowledge_pipeline() -> "WorkflowDefinition":
        """Standard knowledge lifecycle workflow."""
        return WorkflowDefinition(
            name="KnowledgePipeline",
            version="1.0",
            description="COLLECTED -> VERIFIED -> NORMALIZED -> ENRICHED -> INDEXED -> PUBLISHED",
            steps=[
                WorkflowStep(name="collect", state="COLLECTED"),
                WorkflowStep(name="verify", state="VERIFIED"),
                WorkflowStep(name="normalize", state="NORMALIZED"),
                WorkflowStep(name="enrich", state="ENRICHED"),
                WorkflowStep(name="index", state="INDEXED"),
                WorkflowStep(name="publish", state="PUBLISHED"),
            ],
            transitions=[
                Transition("COLLECTED", "VERIFIED"),
                Transition("VERIFIED", "NORMALIZED"),
                Transition("NORMALIZED", "ENRICHED"),
                Transition("ENRICHED", "INDEXED"),
                Transition("INDEXED", "PUBLISHED"),
            ],
        )


# ── AuditEntry ──

@dataclass(frozen=True)
class AuditEntry(ValueObject):
    """Immutable audit record of a workflow event."""
    id: str = field(default_factory=lambda: f"audit_{__import__('uuid').uuid4().hex[:8]}")
    instance_id: str = ""
    step_name: str = ""
    from_state: str = ""
    to_state: str = ""
    status: str = "success"
    error_message: str = ""
    duration_ms: int = 0
    timestamp: datetime = field(default_factory=utcnow)


# ── WorkflowInstance ──

@dataclass
class WorkflowInstance:
    """A running instance of a workflow definition.

    Tracks current state, step transitions, retries, and audit history.
    """
    id: str = field(default_factory=lambda: f"wf_{__import__('uuid').uuid4().hex[:8]}")
    definition: WorkflowDefinition = field(default_factory=WorkflowDefinition.knowledge_pipeline)
    current_state: str = "COLLECTED"
    step_index: int = 0
    retry_count: int = 0
    audit_history: list[AuditEntry] = field(default_factory=list)
    metadata: StandardMetadata = field(default_factory=StandardMetadata)
    is_completed: bool = False
    is_failed: bool = False

    # ── State Transitions ──

    def transition_to(self, to_state: str) -> bool:
        """Attempt to transition to a new state. Returns True if valid."""
        if not self.definition.can_transition(self.current_state, to_state):
            return False
        from_state = self.current_state
        self.current_state = to_state
        self.step_index += 1
        self.retry_count = 0
        self._audit(from_state, to_state, "success")
        return True

    def advance(self) -> bool:
        """Advance to the next step in the workflow definition."""
        if self.step_index >= len(self.definition.steps) - 1:
            self.is_completed = True
            return False
        next_step = self.definition.steps[self.step_index + 1]
        return self.transition_to(next_step.state)

    def complete(self) -> None:
        """Mark the workflow as successfully completed."""
        self.is_completed = True

    # ── Failure Handling ──

    def record_failure(self, error_type: str, error_message: str) -> bool:
        """Record a failure. Returns True if should retry."""
        self._audit(self.current_state, self.current_state, "failure", error_message)
        if self.definition.retry_policy.should_retry(error_type, self.retry_count):
            self.retry_count += 1
            return True
        self.is_failed = True
        return False

    def recover(self) -> None:
        """Recover from failure state."""
        if not self.is_failed:
            raise ValueError("Cannot recover a non-failed workflow")
        self.is_failed = False
        self.retry_count = 0

    # ── Validation ──

    def validate_current_step(self) -> list[str]:
        """Validate the current step. Returns list of errors."""
        current = self.definition.steps[self.step_index]
        errors = []
        if current.is_required and not self.current_state:
            errors.append(f"Step '{current.name}' is required but state is empty")
        return errors

    # ── Properties ──

    @property
    def current_step(self) -> WorkflowStep | None:
        if self.step_index < len(self.definition.steps):
            return self.definition.steps[self.step_index]
        return None

    # ── Audit ──

    def _audit(self, from_state: str, to_state: str, status: str, error: str = "") -> None:
        self.audit_history.append(AuditEntry(
            instance_id=self.id,
            step_name=self.current_step.name if self.current_step else "",
            from_state=from_state,
            to_state=to_state,
            status=status,
            error_message=error,
        ))

    # ── Dunder ──

    def __repr__(self) -> str:
        return f"WorkflowInstance(id={self.id}, state={self.current_state}, step={self.step_index})"
