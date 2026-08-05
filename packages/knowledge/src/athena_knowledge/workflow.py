"""Workflow engine domain model.

Defines the workflow state machine, stages, retry policy, and plugin hooks
as specified in docs/architecture/workflow-engine.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from athena_core.base import DomainEvent, ValueObject, utcnow
from athena_core.enums import WorkflowStage, WorkflowStageStatus
from athena_core.identity import ArticleId, EventId, new_article_id, new_event_id, new_task_id, TaskId


@dataclass(frozen=True)
class RetryPolicy(ValueObject):
    """Exponential backoff retry policy.

    As defined in Workflow Engine Section 5.1.
    """
    max_retries: int = 3
    backoff_base: float = 1.0
    backoff_multiplier: float = 2.0

    def _validate(self) -> None:
        if self.max_retries < 0:
            raise ValueError("max_retries must be >= 0")
        if self.backoff_base <= 0:
            raise ValueError("backoff_base must be positive")
        if self.backoff_multiplier < 1.0:
            raise ValueError("backoff_multiplier must be >= 1.0")

    def delay_for(self, attempt: int) -> float:
        """Calculate delay in seconds for a given attempt number (0-indexed)."""
        return self.backoff_base * (self.backoff_multiplier ** attempt)

    def should_retry(self, error_type: str, attempt: int) -> bool:
        """Determine if a retry should be attempted."""
        retryable = {"NetworkError", "TimeoutError", "RateLimitError"}
        return error_type in retryable and attempt < self.max_retries


@dataclass(frozen=True)
class WorkflowStageResult(ValueObject):
    """Result of executing a workflow stage."""
    stage: WorkflowStage
    status: WorkflowStageStatus
    duration_ms: int = 0
    error_message: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class WorkflowContext:
    """Context carried through the workflow pipeline.

    Tracks the state of an article as it moves through stages.
    """
    article_id: ArticleId = field(default_factory=new_article_id)
    correlation_id: str = field(default_factory=lambda: new_task_id())
    current_stage: WorkflowStage = WorkflowStage.SCHEDULED
    stage_results: list[WorkflowStageResult] = field(default_factory=list)
    retry_count: int = 0
    started_at: datetime = field(default_factory=utcnow)

    def transition_to(self, stage: WorkflowStage) -> None:
        """Move to a new workflow stage."""
        self.current_stage = stage

    def record_result(self, result: WorkflowStageResult) -> None:
        """Record the result of a stage execution."""
        self.stage_results.append(result)
        if result.status == WorkflowStageStatus.FAILED:
            self.retry_count += 1

    @property
    def is_complete(self) -> bool:
        return self.current_stage == WorkflowStage.COMPLETED

    @property
    def is_failed(self) -> bool:
        return self.current_stage == WorkflowStage.FAILED

    @property
    def elapsed_ms(self) -> int:
        return int((utcnow() - self.started_at).total_seconds() * 1000)


@dataclass
class WorkflowAuditEntry:
    """An audit log entry for a workflow stage execution."""
    id: EventId = field(default_factory=new_event_id)
    event_type: str = ""
    stage: WorkflowStage = WorkflowStage.SCHEDULED
    article_id: ArticleId | None = None
    entity_id: str | None = None
    status: WorkflowStageStatus = WorkflowStageStatus.PENDING
    duration_ms: int = 0
    error_message: str = ""
    metadata: dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=utcnow)
