"""ISS-002 Tests: KnowledgeSource Foundation."""

import pytest
from athena_core.enums import (
    AuthorityLevel, LicenseType, SourceType, VerificationStatus,
)
from athena_knowledge.knowledge_source import (
    KnowledgeSource, Authority, TrustScore, CollectorConfig, VerificationPolicy,
)


class TestAuthority:
    """Authority value object."""

    def test_default_unverified(self):
        a = Authority(name="Nature Publishing")
        assert a.level == AuthorityLevel.UNVERIFIED
        assert a.verification == VerificationStatus.PENDING

    def test_verify_returns_new_instance(self):
        a = Authority(name="WHO")
        v = a.verify()
        assert v is not a
        assert v.verification == VerificationStatus.VERIFIED
        assert a.verification == VerificationStatus.PENDING  # immutable

    def test_reject(self):
        a = Authority(name="Fake News Org")
        r = a.reject()
        assert r.verification == VerificationStatus.REJECTED


class TestTrustScore:
    """TrustScore extensible scoring model."""

    def test_default_overall(self):
        ts = TrustScore()
        assert ts.overall == 0.5

    def test_high_trust(self):
        ts = TrustScore(credibility=0.9, accuracy=0.95, transparency=0.8,
                        consistency=0.9, timeliness=0.7, domain_authority=0.85)
        assert ts.overall > 0.8

    def test_with_dimension_extensible(self):
        ts = TrustScore(credibility=0.8, accuracy=0.9)
        extended = ts.with_dimension("peer_review_ratio", 0.95)
        assert "peer_review_ratio" in extended.dimensions
        assert extended.dimensions["peer_review_ratio"] == 0.95
        # Original immutable
        assert "peer_review_ratio" not in ts.dimensions

    def test_validation_rejects_out_of_range(self):
        with pytest.raises(ValueError):
            TrustScore(credibility=1.5)


class TestKnowledgeSourceLifecycle:
    """KnowledgeSource lifecycle state machine."""

    def test_create_default(self):
        ks = KnowledgeSource(name="arXiv", source_type=SourceType.REPOSITORY)
        assert ks.name == "arXiv"
        assert ks.source_type == SourceType.REPOSITORY
        assert ks.status.value == "active"
        assert ks.is_collectable is True

    def test_pause_resume(self):
        ks = KnowledgeSource()
        ks.pause()
        assert ks.status.value == "paused"
        assert ks.is_collectable is False
        ks.resume()
        assert ks.status.value == "active"

    def test_record_error_auto_mark(self):
        ks = KnowledgeSource(
            verification_policy=VerificationPolicy(max_consecutive_errors=3),
        )
        ks.record_error()
        ks.record_error()
        assert ks.status.value == "active"  # not yet
        ks.record_error()
        assert ks.status.value == "error"

    def test_recover_from_error(self):
        ks = KnowledgeSource(
            verification_policy=VerificationPolicy(max_consecutive_errors=1),
        )
        ks.record_error()
        assert ks.status.value == "error"
        ks.recover_from_error()
        assert ks.status.value == "active"
        assert ks.error_count == 0

    def test_deprecate(self):
        ks = KnowledgeSource()
        ks.deprecate()
        assert ks.status.value == "deprecated"

    def test_cannot_pause_non_active(self):
        ks = KnowledgeSource()
        ks.deprecate()
        with pytest.raises(ValueError):
            ks.pause()


class TestKnowledgeSourceTypes:
    """All 10 SourceType values work."""

    def test_all_types(self):
        types = [
            SourceType.OFFICIAL_WEBSITE, SourceType.SCIENTIFIC_JOURNAL,
            SourceType.GOVERNMENT, SourceType.RESEARCH_INSTITUTION,
            SourceType.REPOSITORY, SourceType.DATASET, SourceType.API,
            SourceType.RSS, SourceType.SCRAPER, SourceType.MANUAL,
        ]
        for t in types:
            ks = KnowledgeSource(name=t.value, source_type=t)
            assert ks.source_type == t


class TestKnowledgeSourceAuthority:
    """Authority verification workflow."""

    def test_verify_authority(self):
        ks = KnowledgeSource(authority=Authority(name="NASA", level=AuthorityLevel.PRIMARY))
        assert ks.is_verified is False
        ks.verify_authority()
        assert ks.is_verified is True

    def test_reject_authority(self):
        ks = KnowledgeSource()
        ks.reject_authority()
        assert ks.authority.verification == VerificationStatus.REJECTED


class TestKnowledgeSourceIdentity:
    """Identity and metadata."""

    def test_eq_by_id(self):
        from athena_core.identity import SourceId
        sid = SourceId("src_test")
        ks1 = KnowledgeSource(id=sid, name="A")
        ks2 = KnowledgeSource(id=sid, name="B")
        assert ks1 == ks2

    def test_repr(self):
        ks = KnowledgeSource(name="PubMed", source_type=SourceType.SCIENTIFIC_JOURNAL)
        r = repr(ks)
        assert "PubMed" in r
        assert "KnowledgeSource" in r

    def test_metadata_fields(self):
        ks = KnowledgeSource(
            name="WHO", language="en", region="global",
            license_type=LicenseType.OPEN_ACCESS, tags=["health", "official"],
            description="World Health Organization",
        )
        assert ks.language == "en"
        assert ks.region == "global"
        assert ks.license_type == LicenseType.OPEN_ACCESS
        assert "health" in ks.tags
