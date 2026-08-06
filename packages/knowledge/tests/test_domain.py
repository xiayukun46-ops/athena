"""Tests for the athena_knowledge domain models — Phase 1 Knowledge Core."""

from athena_core.identity import EntityId, new_entity_id, new_relation_id, new_statement_id, new_user_id, is_valid_id
from athena_core.enums import EntityType, EntityStatus, RelationType, ReviewStatus, AliasType, PropertyValueType
from athena_core.metadata import StandardMetadata

from athena_knowledge.entity import KnowledgeEntity, EntityName, EntityAlias, EntityProperty, EntityActivated, EntityDeprecated, EntityMerged
from athena_knowledge.relation import KnowledgeRelation, RelationDeprecated
from athena_knowledge.statement import Statement, StatementSource, StatementApproved, StatementRejected
from athena_knowledge.quality import QualityScore
from athena_knowledge.permission import Permission, PermissionScope
from athena_knowledge.lifecycle import EntityLifecycle, RelationLifecycle, StatementLifecycle
from athena_knowledge.workflow import RetryPolicy, WorkflowContext, WorkflowStageResult
from athena_knowledge.events import EntityCreated, RelationCreated


# ═══════════════════════════════════════════════════════════════
# Identity Tests
# ═══════════════════════════════════════════════════════════════

class TestIdentity:
    def test_generated_id_has_correct_prefix(self):
        eid = new_entity_id()
        assert eid.startswith("ent_")
        assert len(eid) > 5

    def test_is_valid_id(self):
        assert is_valid_id("ent_abc12345", "ent") is True
        assert is_valid_id("art_xyz", "art") is False  # too short
        assert is_valid_id("ent_abc", "art") is False  # wrong prefix

    def test_ids_are_unique(self):
        ids = {new_entity_id() for _ in range(100)}
        assert len(ids) == 100


# ═══════════════════════════════════════════════════════════════
# Entity Tests
# ═══════════════════════════════════════════════════════════════

class TestKnowledgeEntity:
    def test_create_entity_with_defaults(self):
        e = KnowledgeEntity(canonical_name="Apple Inc.", entity_type=EntityType.ORGANIZATION)
        assert e.canonical_name == "Apple Inc."
        assert e.entity_type == EntityType.ORGANIZATION
        assert e.status == EntityStatus.DRAFT

    def test_add_name_preferred_replaces_previous(self):
        e = KnowledgeEntity(canonical_name="Apple")
        e.add_name("苹果公司", "zh", is_preferred=True)
        e.add_name("Apple Inc.", "en", is_preferred=True)
        e.add_name("アップル", "ja")
        assert e.get_preferred_name("en") == "Apple Inc."
        assert e.get_preferred_name("zh") == "苹果公司"
        assert e.get_preferred_name("ja") == "アップル"

    def test_get_preferred_name_fallback(self):
        e = KnowledgeEntity(canonical_name="CANONICAL")
        e.add_name("名称", "zh")
        assert e.get_preferred_name("fr") == "CANONICAL"

    def test_add_alias(self):
        e = KnowledgeEntity(canonical_name="Apple")
        e.add_alias("AAPL", AliasType.ACRONYM)
        assert len(e.aliases) == 1
        assert e.aliases[0].alias == "AAPL"

    def test_add_property_marks_conflict(self):
        e = KnowledgeEntity(canonical_name="Apple")
        prop1 = EntityProperty(key="founded", value="1976", confidence=0.9)
        prop2 = EntityProperty(key="founded", value="1977", confidence=0.7)
        e.add_property(prop1)
        e.add_property(prop2)
        found = e.get_property("founded")
        assert len(found) == 2
        assert found[1].needs_arbitration is True

    def test_activate_from_draft(self):
        e = KnowledgeEntity(canonical_name="Test")
        e.activate()
        assert e.status == EntityStatus.ACTIVE
        events = e.collect_events()
        assert len(events) == 1
        assert isinstance(events[0], EntityActivated)

    def test_cannot_activate_non_draft(self):
        e = KnowledgeEntity(canonical_name="Test")
        e.activate()
        import pytest
        with pytest.raises(ValueError):
            e.activate()

    def test_deprecate(self):
        e = KnowledgeEntity(canonical_name="Test")
        e.activate()
        e.deprecate("outdated info")
        assert e.status == EntityStatus.DEPRECATED
        # Check deprecation reason property was added
        reasons = [p.value for p in e.get_property("deprecation_reason")]
        assert "outdated info" in reasons

    def test_merge_into(self):
        target = new_entity_id()
        e = KnowledgeEntity(canonical_name="Test")
        e.merge_into(target)
        assert e.status == EntityStatus.MERGED
        assert e.merged_into == target

    def test_entity_name_validation(self):
        import pytest
        with pytest.raises(ValueError):
            EntityName(name="", language="en")
        with pytest.raises(ValueError):
            EntityName(name="X", language="e")


# ═══════════════════════════════════════════════════════════════
# Relation Tests
# ═══════════════════════════════════════════════════════════════

class TestKnowledgeRelation:
    def test_create_relation(self):
        r = KnowledgeRelation(
            relation_type=RelationType.WORKS_FOR,
            source_entity_id=EntityId("ent_11111111"),
            target_entity_id=EntityId("ent_22222222"),
        )
        assert r.relation_type == RelationType.WORKS_FOR
        assert r.status.value == "active"

    def test_self_relation_not_allowed(self):
        import pytest
        eid = EntityId("ent_11111111")
        with pytest.raises(ValueError):
            KnowledgeRelation(
                relation_type=RelationType.WORKS_FOR,
                source_entity_id=eid,
                target_entity_id=eid,
            )

    def test_add_statement(self):
        r = KnowledgeRelation(
            source_entity_id=EntityId("ent_11111111"),
            target_entity_id=EntityId("ent_22222222"),
        )
        sid = new_statement_id()
        r.add_statement(sid)
        assert len(r.statements) == 1
        assert r.statements[0] == sid

    def test_deprecate(self):
        r = KnowledgeRelation(
            source_entity_id=EntityId("ent_11111111"),
            target_entity_id=EntityId("ent_22222222"),
        )
        r.deprecate("no longer valid")
        assert r.status.value == "deprecated"
        assert r.properties["deprecation_reason"] == "no longer valid"


# ═══════════════════════════════════════════════════════════════
# Statement Tests
# ═══════════════════════════════════════════════════════════════

class TestStatement:
    def test_create_statement(self):
        s = Statement(predicate="birth_date", object_value="1964-01-07")
        assert s.review_status == ReviewStatus.PENDING

    def test_approve_statement(self):
        s = Statement(predicate="test", object_value="value")
        reviewer = new_user_id()
        s.approve(reviewer, "looks correct")
        assert s.review_status == ReviewStatus.APPROVED
        assert s.reviewer_id == reviewer
        events = s.collect_events()
        assert isinstance(events[0], StatementApproved)

    def test_reject_statement(self):
        s = Statement(predicate="test", object_value="value")
        reviewer = new_user_id()
        s.reject(reviewer, "inaccurate")
        assert s.review_status == ReviewStatus.REJECTED
        events = s.collect_events()
        assert isinstance(events[0], StatementRejected)

    def test_cannot_approve_already_approved(self):
        import pytest
        s = Statement(predicate="test", object_value="value")
        s.approve(new_user_id())
        with pytest.raises(ValueError):
            s.approve(new_user_id())


# ═══════════════════════════════════════════════════════════════
# Quality Tests
# ═══════════════════════════════════════════════════════════════

class TestQualityScore:
    def test_default_score_is_zero(self):
        q = QualityScore()
        assert q.overall == 0.0

    def test_compute_with_properties(self):
        props = [
            EntityProperty(key="name", value="X", confidence=0.9, source_statement_id=new_statement_id()),
            EntityProperty(key="founded", value="2000", confidence=0.8, source_statement_id=new_statement_id()),
        ]
        q = QualityScore.compute(props, source_count=3)
        assert 0.0 < q.overall <= 1.0
        assert q.completeness > 0.0
        assert q.confidence > 0.0

    def test_compute_empty(self):
        q = QualityScore.compute([], source_count=0)
        assert q.overall == 0.0

    def test_validation(self):
        import pytest
        with pytest.raises(ValueError):
            QualityScore(completeness=1.5)


# ═══════════════════════════════════════════════════════════════
# Permission Tests
# ═══════════════════════════════════════════════════════════════

class TestPermission:
    def test_reader_cannot_write(self):
        p = Permission.reader()
        assert p.allows(PermissionScope.READ_ENTITIES) is True
        assert p.allows(PermissionScope.WRITE_ENTITIES) is False

    def test_admin_can_do_anything(self):
        p = Permission.admin()
        for scope in list(PermissionScope):
            assert p.allows(scope) is True

    def test_moderator_can_approve(self):
        p = Permission.moderator()
        assert p.allows(PermissionScope.APPROVE_STATEMENTS) is True
        assert p.allows(PermissionScope.MERGE_ENTITIES) is True


# ═══════════════════════════════════════════════════════════════
# Lifecycle Tests
# ═══════════════════════════════════════════════════════════════

class TestLifecycle:
    def test_entity_valid_transitions(self):
        assert EntityLifecycle.can_transition("draft", "active") is True
        assert EntityLifecycle.can_transition("active", "deprecated") is True
        assert EntityLifecycle.can_transition("deprecated", "merged") is True

    def test_entity_invalid_transition(self):
        assert EntityLifecycle.can_transition("active", "draft") is False
        assert EntityLifecycle.can_transition("merged", "active") is False

    def test_validate_transition_raises(self):
        import pytest
        with pytest.raises(ValueError):
            EntityLifecycle.validate_transition("active", "draft", "Entity")


# ═══════════════════════════════════════════════════════════════
# Workflow Tests
# ═══════════════════════════════════════════════════════════════

class TestWorkflow:
    def test_retry_policy(self):
        rp = RetryPolicy(max_retries=3, backoff_base=1.0, backoff_multiplier=2.0)
        assert rp.should_retry("NetworkError", 0) is True
        assert rp.should_retry("NetworkError", 3) is False
        assert rp.should_retry("ParseError", 0) is False
        assert rp.delay_for(0) == 1.0
        assert rp.delay_for(1) == 2.0
        assert rp.delay_for(2) == 4.0

    def test_workflow_context(self):
        ctx = WorkflowContext()
        from athena_core.enums import WorkflowStage
        ctx.transition_to(WorkflowStage.FETCHING)
        assert ctx.current_stage == WorkflowStage.FETCHING
        assert ctx.elapsed_ms >= 0


# ═══════════════════════════════════════════════════════════════
# Event Tests
# ═══════════════════════════════════════════════════════════════

class TestEvents:
    def test_entity_created_event(self):
        e = EntityCreated(
            entity_id=EntityId("ent_test0001"),
            canonical_name="Test Entity",
            entity_type=EntityType.ORGANIZATION,
        )
        assert e.event_type == "EntityCreated"
        assert e.canonical_name == "Test Entity"

    def test_event_has_timestamp(self):
        e = EntityCreated(canonical_name="X")
        assert e.occurred_at is not None
        assert e.event_id is not None


# ═══════════════════════════════════════════════════════════════
# Metadata Tests
# ═══════════════════════════════════════════════════════════════

class TestMetadata:
    def test_touch_updates_timestamp(self):
        m = StandardMetadata()
        m2 = m.touch()
        assert m2.updated_at > m.updated_at

    def test_increment_version(self):
        m = StandardMetadata(version=1)
        m2 = m.increment_version()
        assert m2.version == 2

    def test_soft_delete(self):
        m = StandardMetadata()
        m2 = m.soft_delete()
        assert m2.is_deleted is True
