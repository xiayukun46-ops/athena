"""ISS-003 Tests: Evidence Chain Foundation."""

import pytest
from datetime import datetime, timezone
from athena_core.enums import EvidenceType, VerificationStatus
from athena_knowledge.evidence import Evidence, ContentReference


class TestContentReference:
    """ContentReference value object."""

    def test_primary_ref_prefers_url(self):
        cr = ContentReference(url="https://example.com", doi="10.1234/x")
        assert cr.primary_ref == "https://example.com"

    def test_primary_ref_falls_back_to_doi(self):
        cr = ContentReference(doi="10.1234/x")
        assert cr.primary_ref == "10.1234/x"

    def test_has_exact_location(self):
        cr = ContentReference(url="x", page="42", section="Methods")
        assert cr.has_exact_location is True

    def test_no_location(self):
        cr = ContentReference(url="x")
        assert cr.has_exact_location is False


class TestEvidence:
    """Evidence as a Domain Entity."""

    def test_create_default(self):
        e = Evidence(knowledge_object_id="ko_1", source_id="src_1")
        assert e.evidence_type == EvidenceType.ARTICLE_EXCERPT
        assert e.verification == VerificationStatus.PENDING
        assert e.id.startswith("evid_")

    def test_verify(self):
        e = Evidence(knowledge_object_id="ko_1", source_id="src_1")
        e.verify(verified_by="reviewer_1")
        assert e.verification == VerificationStatus.VERIFIED
        assert e.verified_by == "reviewer_1"

    def test_reject(self):
        e = Evidence(knowledge_object_id="ko_1", source_id="src_1")
        e.reject("source not found")
        assert e.verification == VerificationStatus.REJECTED
        assert e.rejection_reason == "source not found"

    def test_mark_expired(self):
        e = Evidence(knowledge_object_id="ko_1", source_id="src_1")
        e.verify()
        e.mark_expired()
        assert e.verification == VerificationStatus.EXPIRED

    def test_cannot_verify_rejected(self):
        e = Evidence(knowledge_object_id="ko_1", source_id="src_1")
        e.reject("bad")
        with pytest.raises(ValueError):
            e.verify()

    def test_is_accessible(self):
        e = Evidence(knowledge_object_id="ko_1", source_id="src_1",
                      content_ref=ContentReference(url="https://x.com"))
        assert e.is_accessible is True

    def test_not_accessible_when_expired(self):
        e = Evidence(knowledge_object_id="ko_1", source_id="src_1",
                      content_ref=ContentReference(url="https://x.com"))
        e.mark_expired()
        assert e.is_accessible is False

    def test_eq_by_id(self):
        e1 = Evidence(id="evid_test", knowledge_object_id="ko_1", source_id="src_1")
        e2 = Evidence(id="evid_test", knowledge_object_id="ko_2", source_id="src_2")
        assert e1 == e2


class TestEvidenceTypes:
    """All 8 evidence types."""

    def test_all_types(self):
        for t in EvidenceType:
            e = Evidence(knowledge_object_id="ko_1", source_id="src_1", evidence_type=t)
            assert e.evidence_type == t
