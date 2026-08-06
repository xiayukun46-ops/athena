"""ISS-001 Tests: Aggregates __eq__, Statement validation, Relation is_active_at."""

from datetime import datetime, timedelta, timezone
from athena_core.identity import EntityId, new_entity_id, new_statement_id
from athena_core.enums import EntityType, RelationType
from athena_knowledge.entity import KnowledgeEntity
from athena_knowledge.relation import KnowledgeRelation
from athena_knowledge.statement import Statement


class TestISSOO1EntityEq:
    """ISS-001: KnowledgeEntity __eq__ based on ID."""

    def test_same_id_equal(self):
        eid = new_entity_id()
        e1 = KnowledgeEntity(id=eid, canonical_name="A")
        e2 = KnowledgeEntity(id=eid, canonical_name="B")
        assert e1 == e2

    def test_different_id_not_equal(self):
        e1 = KnowledgeEntity(canonical_name="A")
        e2 = KnowledgeEntity(canonical_name="A")
        assert e1 != e2

    def test_eq_with_non_entity(self):
        e = KnowledgeEntity(canonical_name="A")
        assert e != "not an entity"
        assert (e == 42) is False

    def test_repr_contains_id_and_name(self):
        e = KnowledgeEntity(canonical_name="Apple", entity_type=EntityType.ORGANIZATION)
        r = repr(e)
        assert "KnowledgeEntity" in r
        assert "Apple" in r

    def test_str_returns_canonical_name(self):
        e = KnowledgeEntity(canonical_name="Apple")
        assert str(e) == "Apple"

    def test_hash_consistent_with_eq(self):
        eid = new_entity_id()
        e1 = KnowledgeEntity(id=eid)
        e2 = KnowledgeEntity(id=eid)
        assert hash(e1) == hash(e2)
        s = {e1, e2}
        assert len(s) == 1


class TestISSOO1RelationIsActiveAt:
    """ISS-001: KnowledgeRelation is_active_at boundary tests."""

    def test_active_within_range(self):
        now = datetime.now(timezone.utc)
        r = KnowledgeRelation(
            source_entity_id=EntityId("ent_a"),
            target_entity_id=EntityId("ent_b"),
            valid_from=now - timedelta(days=1),
            valid_until=now + timedelta(days=1),
        )
        assert r.is_active_at(now) is True

    def test_inactive_before_start(self):
        now = datetime.now(timezone.utc)
        r = KnowledgeRelation(
            source_entity_id=EntityId("ent_a"),
            target_entity_id=EntityId("ent_b"),
            valid_from=now + timedelta(days=1),
        )
        assert r.is_active_at(now) is False

    def test_inactive_after_end(self):
        now = datetime.now(timezone.utc)
        r = KnowledgeRelation(
            source_entity_id=EntityId("ent_a"),
            target_entity_id=EntityId("ent_b"),
            valid_until=now - timedelta(days=1),
        )
        assert r.is_active_at(now) is False

    def test_active_no_time_bounds(self):
        r = KnowledgeRelation(
            source_entity_id=EntityId("ent_a"),
            target_entity_id=EntityId("ent_b"),
        )
        assert r.is_active_at(datetime.now(timezone.utc)) is True

    def test_inactive_when_deprecated(self):
        r = KnowledgeRelation(
            source_entity_id=EntityId("ent_a"),
            target_entity_id=EntityId("ent_b"),
        )
        r.deprecate()
        assert r.is_active_at(datetime.now(timezone.utc)) is False


class TestISSOO1StatementValidation:
    """ISS-001: Statement __post_init__ validates predicate."""

    def test_empty_predicate_raises(self):
        import pytest
        with pytest.raises(ValueError, match="predicate cannot be empty"):
            Statement(predicate="", object_value="val")

    def test_whitespace_predicate_raises(self):
        import pytest
        with pytest.raises(ValueError, match="predicate cannot be empty"):
            Statement(predicate="   ", object_value="val")

    def test_valid_predicate_ok(self):
        s = Statement(predicate="birth_date", object_value="1964")
        assert s.predicate == "birth_date"

    def test_eq_by_id(self):
        sid = new_statement_id()
        s1 = Statement(id=sid, predicate="a", object_value="x")
        s2 = Statement(id=sid, predicate="b", object_value="y")
        assert s1 == s2
