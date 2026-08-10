"""Revision 1 Tests: KnowledgeObject and KnowledgeSource."""

from athena_core.enums import EntityType, RelationType, ReviewStatus
from athena_core.identity import EntityId

from athena_knowledge.knowledge_object import (
    KnowledgeObject, KnowledgeEntity, KnowledgeRelation, KnowledgeStatement,
    EntityName, EntityProperty, StatementSource, Evidence,
    KnowledgeVerified, KnowledgePublished, KnowledgeArchived,
)
from athena_knowledge.knowledge_source import (
    KnowledgeSource, Authority, TrustScore, CollectorConfig,
)


class TestKnowledgeObject:
    """KnowledgeObject as top-level aggregate root."""

    def test_create_empty(self):
        ko = KnowledgeObject(canonical_name="Test Knowledge")
        assert ko.canonical_name == "Test Knowledge"
        assert ko.status == "draft"
        assert len(ko.entities) == 0

    def test_add_entity(self):
        ko = KnowledgeObject()
        e = KnowledgeEntity(canonical_name="Apple", entity_type=EntityType.ORGANIZATION)
        ko.add_entity(e)
        assert len(ko.entities) == 1
        assert ko.find_entity(e.id) is not None

    def test_add_entity_with_names(self):
        ko = KnowledgeObject()
        e = KnowledgeEntity(canonical_name="Apple")
        e.add_name("Apple Inc.", "en", is_preferred=True)
        e.add_name("苹果公司", "zh")
        ko.add_entity(e)
        found = ko.find_entity(e.id)
        assert found is not None
        assert found.get_preferred_name("en") == "Apple Inc."
        assert found.get_preferred_name("zh") == "苹果公司"

    def test_add_relation(self):
        ko = KnowledgeObject()
        e1 = ko.add_entity(KnowledgeEntity(canonical_name="Tim Cook", entity_type=EntityType.PERSON))
        e2 = ko.add_entity(KnowledgeEntity(canonical_name="Apple", entity_type=EntityType.ORGANIZATION))
        r = KnowledgeRelation(
            relation_type=RelationType.WORKS_FOR,
            source_entity_id=e1.id,
            target_entity_id=e2.id,
        )
        ko.add_relation(r)
        assert len(ko.relations) == 1

    def test_add_statement_creates_evidence(self):
        ko = KnowledgeObject()
        sid = EntityId("stmt_test")
        s = KnowledgeStatement(
            id=sid,
            predicate="birth_date",
            object_value="1964",
            source=StatementSource(article_id=EntityId("art_test")),
        )
        ko.add_statement(s)
        assert len(ko.statements) == 1
        assert len(ko.evidence) == 1
        assert ko.evidence[0].knowledge_object_id == ko.id

    def test_lifecycle_verify(self):
        ko = KnowledgeObject()
        ko.verify()
        assert ko.status == "verified"
        events = ko.collect_events()
        assert isinstance(events[0], KnowledgeVerified)

    def test_lifecycle_publish(self):
        ko = KnowledgeObject()
        ko.publish()
        assert ko.status == "published"
        assert isinstance(ko.collect_events()[0], KnowledgePublished)

    def test_lifecycle_archive(self):
        ko = KnowledgeObject()
        ko.publish()
        ko.archive("outdated")
        assert ko.status == "archived"
        e = ko.collect_events()
        assert isinstance(e[-1], KnowledgeArchived)

    def test_cannot_publish_archived(self):
        import pytest
        ko = KnowledgeObject()
        ko.publish()
        ko.archive()
        with pytest.raises(ValueError):
            ko.publish()


class TestKnowledgeSource:
    """KnowledgeSource aggregate."""

    def test_create_default(self):
        ks = KnowledgeSource()
        assert ks.authority.name == ""
        assert ks.status.value == "active"

    def test_pause_and_resume(self):
        ks = KnowledgeSource()
        ks.pause()
        assert ks.status.value == "paused"
        ks.resume()
        assert ks.status.value == "active"

    def test_trust_score(self):
        ts = TrustScore(credibility=0.8, accuracy=0.9, domain_authority=0.7)
        assert 0.6 < ts.overall < 0.75  # (0.8+0.9+0.5+0.5+0.5+0.7)/6 ≈ 0.65

    def test_cannot_pause_non_active(self):
        import pytest
        ks = KnowledgeSource()
        ks.pause()
        with pytest.raises(ValueError):
            ks.pause()

    def test_deprecate(self):
        ks = KnowledgeSource()
        ks.deprecate()
        assert ks.status.value == "deprecated"
