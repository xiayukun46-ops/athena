"""ISS-004 Tests: Workflow Engine Foundation."""

import pytest
from athena_knowledge.workflow import (
    WorkflowState, Transition, RetryPolicy, WorkflowStep,
    WorkflowDefinition, WorkflowInstance, AuditEntry,
)


class TestWorkflowState:
    def test_create(self):
        s = WorkflowState(name="COLLECTED", description="Content collected")
        assert s.name == "COLLECTED"

    def test_empty_name_raises(self):
        with pytest.raises(ValueError):
            WorkflowState(name="")


class TestTransition:
    def test_valid(self):
        t = Transition("COLLECTED", "VERIFIED")
        assert t.from_state == "COLLECTED"

    def test_self_transition_raises(self):
        with pytest.raises(ValueError):
            Transition("X", "X")


class TestRetryPolicy:
    def test_should_retry(self):
        rp = RetryPolicy(max_retries=3)
        assert rp.should_retry("NetworkError", 0) is True
        assert rp.should_retry("NetworkError", 3) is False

    def test_non_retryable(self):
        rp = RetryPolicy()
        assert rp.should_retry("ParseError", 0) is False


class TestWorkflowDefinition:
    def test_knowledge_pipeline(self):
        wd = WorkflowDefinition.knowledge_pipeline()
        assert len(wd.steps) == 6
        assert wd.steps[0].state == "COLLECTED"
        assert wd.steps[-1].state == "PUBLISHED"
        assert wd.can_transition("COLLECTED", "VERIFIED") is True
        assert wd.can_transition("PUBLISHED", "COLLECTED") is False


class TestWorkflowInstance:
    def test_full_pipeline(self):
        wf = WorkflowInstance()
        assert wf.current_state == "COLLECTED"
        steps = ["COLLECTED", "VERIFIED", "NORMALIZED", "ENRICHED", "INDEXED", "PUBLISHED"]
        for i, expected in enumerate(steps):
            assert wf.current_state == expected
            if i < len(steps) - 1:
                assert wf.advance() is True
        # At last step, advance returns False
        assert wf.advance() is False

    def test_transition_to_invalid(self):
        wf = WorkflowInstance()
        assert wf.transition_to("PUBLISHED") is False

    def test_complete(self):
        wf = WorkflowInstance()
        wf.complete()
        assert wf.is_completed is True

    def test_failure_and_recovery(self):
        wf = WorkflowInstance()
        assert wf.record_failure("NetworkError", "timeout") is True
        assert wf.retry_count == 1
        # 3rd retry fails
        wf.record_failure("NetworkError", "timeout")
        wf.record_failure("NetworkError", "timeout")
        assert wf.retry_count == 3
        assert wf.record_failure("NetworkError", "timeout") is False
        assert wf.is_failed is True

    def test_recover(self):
        wf = WorkflowInstance()
        for _ in range(4):
            wf.record_failure("NetworkError", "x")
        assert wf.is_failed is True
        wf.recover()
        assert wf.is_failed is False
        assert wf.retry_count == 0

    def test_audit_history(self):
        wf = WorkflowInstance()
        wf.advance()
        entries = wf.audit_history
        assert len(entries) == 1
        assert entries[0].from_state == "COLLECTED"
        assert entries[0].to_state == "VERIFIED"

    def test_validate_empty(self):
        wf = WorkflowInstance()
        assert wf.validate_current_step() == []
