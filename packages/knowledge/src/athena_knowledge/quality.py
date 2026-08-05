"""Quality scoring for knowledge objects.

Defines QualityScore as defined in the Knowledge Canon
(docs/domain/knowledge-canon.md Section 3.10).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from athena_core.base import ValueObject


@dataclass(frozen=True)
class QualityScore(ValueObject):
    """Multi-dimensional quality score for a knowledge object.

    As defined in Knowledge Canon Section 3.10.
    """
    completeness: float = 0.0
    consistency: float = 1.0
    freshness: float = 1.0
    confidence: float = 0.0
    provenance: float = 0.0
    diversity: float = 0.0
    overall: float = 0.0

    def _validate(self) -> None:
        for name, value in [
            ("completeness", self.completeness),
            ("consistency", self.consistency),
            ("freshness", self.freshness),
            ("confidence", self.confidence),
            ("provenance", self.provenance),
            ("diversity", self.diversity),
            ("overall", self.overall),
        ]:
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0.0, 1.0]")

    @staticmethod
    def compute(
        properties: list,
        source_count: int = 0,
        *,
        weights: dict[str, float] | None = None,
    ) -> "QualityScore":
        """Compute a quality score from entity data.

        Args:
            properties: List of EntityProperty objects
            source_count: Number of unique sources
            weights: Optional dimension weights (defaults to equal weight)
        """
        from athena_core.enums import ReviewStatus

        if not properties:
            return QualityScore()

        w = weights or {
            "completeness": 0.20,
            "consistency": 0.15,
            "freshness": 0.15,
            "confidence": 0.25,
            "provenance": 0.15,
            "diversity": 0.10,
        }

        unique_keys = len({p.key for p in properties})
        completeness = min(unique_keys / 10.0, 1.0)

        approved = [p for p in properties if getattr(p, "source_statement_id", None)]
        provenance_ratio = len(approved) / len(properties) if properties else 0.0

        confidences = [p.confidence for p in properties]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        now = datetime.now(timezone.utc)
        freshness_scores = []
        for p in properties:
            if hasattr(p, "valid_from") and p.valid_from:
                age_days = (now - p.valid_from).days
                freshness_scores.append(max(0.0, 1.0 - age_days / 365.0))
        freshness = sum(freshness_scores) / len(freshness_scores) if freshness_scores else 0.5

        diversity = min(source_count / 5.0, 1.0)

        conflicts = sum(1 for p in properties if getattr(p, "needs_arbitration", False))
        consistency = max(0.0, 1.0 - conflicts / len(properties))

        overall = (
            w["completeness"] * completeness
            + w["consistency"] * consistency
            + w["freshness"] * freshness
            + w["confidence"] * avg_confidence
            + w["provenance"] * provenance_ratio
            + w["diversity"] * diversity
        )

        return QualityScore(
            completeness=round(completeness, 4),
            consistency=round(consistency, 4),
            freshness=round(freshness, 4),
            confidence=round(avg_confidence, 4),
            provenance=round(provenance_ratio, 4),
            diversity=round(diversity, 4),
            overall=round(overall, 4),
        )
