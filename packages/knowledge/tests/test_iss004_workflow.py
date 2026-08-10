"""ISS-004 Tests: Workflow Engine Foundation."""

import pytest
from athena_knowledge.workflow import (
    WorkflowStates, WorkflowState, Transition, RetryPolicy, WorkflowStep,
    WorkflowDefinition, WorkflowInstance, AuditEntry,
)


class TestWorkflowState:
    def test_create(self):
        s = WorkflowState(name="COLLECTING", description="Collecting content")
        assert s.name == "COLLECTING"

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            WorkflowState(name="")


class TestTransition:
    def test_valid(self):
        t = Transition("CREATED", "COLLECTING")
        assert t.from_state == "CREATED"

    def test_self_raises(self):
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
        assert len(wd.steps) == 7
        assert wd.initial_state == WorkflowStates.CREATED
        assert wd.can_transition("CREATED", "COLLECTING") is True
        assert wd.can_transition("PUBLISHED", "CREATED") is False


class TestWorkflowInstance:
    def test_full_pipeline(self):
        wd = WorkflowDefinition.knowledge_pipeline()
        wf = WorkflowInstance(workflow_definition_id=wd.id)
        assert wf.current_state == WorkflowStates.CREATED
        states = ["COLLECTING", "VERIFYING", "NORMALIZING", "ENRICHING", "INDEXING", "PUBLISHED"]
        for s in states:
            assert wf.transition(wd, s) is True
        assert wf.current_state == "PUBLISHED"
        wf.complete()
        assert wf.is_completed is True

    def test_invalid_transition(self):
        wd = WorkflowDefinition.knowledge_pipeline()
        wf = WorkflowInstance(workflow_definition_id=wd.id)
        assert wf.transition(wd, "PUBLISHED") is False

    def test_failure_and_retry(self):
        wd = WorkflowDefinition.knowledge_pipeline()
        wf = WorkflowInstance(workflow_definition_id=wd.id)
        assert wf.fail("NetworkError", "timeout", wd) is True
        assert wf.retry_count == 1
        wf.fail("NetworkError", "x", wd)
        wf.fail("NetworkError", "x", wd)
        assert wf.retry_count == 3
        assert wf.fail("NetworkError", "x", wd) is False
        assert wf.is_failed is True
        assert wf.current_state == WorkflowStates.FAILED

    def test_recover(self):
        wd = WorkflowDefinition.knowledge_pipeline()
        wf = WorkflowInstance(workflow_definition_id=wd.id)
        for _ in range(4):
            wf.fail("NetworkError", "x", wd)
        assert wf.is_failed is True
        wf.recover()
        assert wf.is_failed is False
        assert wf.retry_count == 0

    def test_audit_history(self):
        wd = WorkflowDefinition.knowledge_pipeline()
        wf = WorkflowInstance(workflow_definition_id=wd.id)
        wf.transition(wd, "COLLECTING")
        assert len(wf.audit_history) == 1
        assert wf.audit_history[0].from_state == "CREATED"
        assert wf.audit_history[0].to_state == "COLLECTING"

    def test_entity_id(self):
        wf = WorkflowInstance(entity_id="ent_123")
        assert wf.entity_id == "ent_123"

    def test_all_states(self):
        states = WorkflowStates.all_states()
        assert len(states) == 8
        assert "FAILED" in states
