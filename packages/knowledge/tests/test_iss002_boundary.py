"""ISS-002 Revision 1: Domain Boundary Tests.

Validates that:
1. KnowledgeObject references source by source_id only
2. KnowledgeSource is sole authority/trust source of truth
3. No source authority state duplication in KnowledgeObject
"""

from athena_core.identity import SourceId, new_source_id
from athena_core.enums import SourceType
from athena_knowledge.knowledge_object import KnowledgeObject
from athena_knowledge.knowledge_source import KnowledgeSource, Authority


class TestBoundarySourceIdReference:
    """KnowledgeObject only stores source_id, not full authority."""

    def test_ko_has_source_id_not_authority(self):
        sid = new_source_id()
        ko = KnowledgeObject(source_id=sid)
        assert ko.source_id == sid
        # No source authority attributes on KnowledgeObject
        assert not hasattr(ko, "source_authority")
        assert not hasattr(ko, "credibility_score")

    def test_ko_default_source_id_is_set(self):
        ko = KnowledgeObject()
        assert ko.source_id is not None
        assert ko.source_id.startswith("src_")


class TestBoundaryNoAggregateHolding:
    """KnowledgeObject does not hold a KnowledgeSource aggregate."""

    def test_ko_does_not_hold_source_aggregate(self):
        ko = KnowledgeObject()
        assert not hasattr(ko, "knowledge_source")

    def test_source_authority_lives_only_in_knowledge_source(self):
        ks = KnowledgeSource(
            name="Nature", source_type=SourceType.SCIENTIFIC_JOURNAL,
            authority=Authority(name="Nature Publishing"),
        )
        assert ks.authority.name == "Nature Publishing"
        # Authority info is NOT in KnowledgeObject
        ko = KnowledgeObject(source_id=ks.id)
        assert ko.source_id == ks.id
        # Cannot access authority through KnowledgeObject
        assert not hasattr(ko, "authority")


class TestBoundarySingleSourceOfTruth:
    """KnowledgeSource is the sole domain source for authority/trust."""

    def test_trust_score_only_in_source(self):
        ks = KnowledgeSource(name="WHO")
        ko = KnowledgeObject(source_id=ks.id)
        assert hasattr(ks, "trust_score")
        assert not hasattr(ko, "trust_score")

    def test_verification_only_in_source(self):
        ks = KnowledgeSource()
        ko = KnowledgeObject(source_id=ks.id)
        assert hasattr(ks, "verification_policy")
        assert not hasattr(ko, "verification_policy")

    def test_publisher_only_in_source(self):
        ks = KnowledgeSource(authority=Authority(publisher="Springer"))
        ko = KnowledgeObject(source_id=ks.id)
        assert ks.authority.publisher == "Springer"
        assert not hasattr(ko, "publisher")
