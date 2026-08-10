# Issue-002 Revision 1 Report

Date: 2026-08-10 | Tests: 104/104 | Status: Complete

---

## 1. Changes

| # | Change | Detail |
|---|--------|--------|
| 1 | KnowledgeObject.source -> source_id | No longer holds full SourceAuthority; reference only |
| 2 | SourceAuthority class deleted | Duplicate of KnowledgeSource.Authority |
| 3 | Boundary tests x7 | Validate source_id ref, no aggregate holding, single truth source |

## 2. Domain Boundary

KnowledgeObject.source_id --ref--> KnowledgeSource.id
                                      +-- Authority (name, url, publisher, level, score)
                                      +-- TrustScore (6 dims + extensible)
                                      +-- VerificationPolicy
                                      +-- CollectorConfig

Rule: Authority / TrustScore / Publisher info lives ONLY in KnowledgeSource.
      KnowledgeObject MUST NOT duplicate this state.

## 3. Final Domain Diagram

KnowledgeObject                    KnowledgeSource (Single Source of Truth)
  source_id: SourceId ---------->   id: SourceId
  entities: [KnowledgeEntity]      authority: Authority
  relations: [KnowledgeRelation]   trust_score: TrustScore
  statements: [KnowledgeStatement] verification_policy: VerificationPolicy
  evidence: [Evidence]             collector_config: CollectorConfig
  quality_score: QualityScore      status: ACTIVE <-> PAUSED -> ERROR -> DEPRECATED
  permission: Permission
  status: draft -> published

## 4. Test Results

| Suite | Tests | Focus |
|-------|:-----:|-------|
| test_domain | 37 | Core aggregates |
| test_iss001 | 15 | Aggregate __eq__ |
| test_iss002_source | 19 | KnowledgeSource lifecycle |
| test_iss002_boundary | 7 | Domain boundary checks |
| test_revision1 | 14 | KnowledgeObject lifecycle |
| test_iss002 (old) | 11 | ID system |
| 1 misc | 1 | |
| **Total** | **104** | |

## 5. Architecture Impact

- Eliminated SourceAuthority / Authority duplication
- KnowledgeSource = sole domain authority for all source metadata
- KnowledgeObject.source_id = lightweight reference (no state copy)
- Unchanged: TrustScore, VerificationPolicy, Lifecycle, SourceType, AuthorityLevel, CollectorConfig
