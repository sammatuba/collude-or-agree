"""Evidence independence and double counting, in numbers.

Glossary: prior odds, likelihood ratio, posterior odds, conditional independence,
derivative, double counting.

The one fact this module teaches: under conditional independence given the claim's truth
value, likelihood ratios multiply. A derivative of an evidence item has likelihood ratio 1
once its origin is known, so it must not multiply again.
"""
from __future__ import annotations

from dataclasses import dataclass


def likelihood_ratio(reliability: float, reports_true: bool) -> float:
    """LR of one origin observation for the claim H = 'claim is true'.

    An origin with reliability r reports the truth with probability r.
    If it reports true:  P(report true | H) / P(report true | not H) = r / (1 - r).
    If it reports false: (1 - r) / r.
    """
    if not 0.0 < reliability < 1.0:
        raise ValueError("reliability must be strictly between 0 and 1")
    return reliability / (1 - reliability) if reports_true else (1 - reliability) / reliability


def odds(p: float) -> float:
    return p / (1 - p)


def prob(o: float) -> float:
    return o / (1 + o)


@dataclass
class Report:
    """One evidence item for the Bayesian demo. `origin` groups derivatives."""
    origin: str
    reliability: float
    reports_true: bool


def posterior_naive(prior: float, reports: list[Report]) -> float:
    """Treat every report as conditionally independent. This is double counting when two
    reports share an origin."""
    o = odds(prior)
    for r in reports:
        o *= likelihood_ratio(r.reliability, r.reports_true)
    return prob(o)


def posterior_provenance_aware(prior: float, reports: list[Report]) -> float:
    """Multiply one likelihood ratio per distinct origin. Derivatives contribute nothing
    beyond their origin, because P(derivative | origin, H) = P(derivative | origin, not H)."""
    seen: set[str] = set()
    o = odds(prior)
    for r in reports:
        if r.origin in seen:
            continue
        seen.add(r.origin)
        o *= likelihood_ratio(r.reliability, r.reports_true)
    return prob(o)


def worked_example() -> dict[str, float]:
    """The example from the research starter: prior 0.5, reliability 0.8.

    Three independent true reports: odds 1 * 4 * 4 * 4 = 64 -> 64/65 = 0.9846.
    Three copies of one true report:  odds 1 * 4 = 4 -> 4/5 = 0.80.
    """
    independent = [Report(f"o{i}", 0.8, True) for i in range(3)]
    copies = [Report("o1", 0.8, True) for _ in range(3)]
    return {
        "independent_naive": posterior_naive(0.5, independent),
        "independent_aware": posterior_provenance_aware(0.5, independent),
        "copies_naive": posterior_naive(0.5, copies),
        "copies_aware": posterior_provenance_aware(0.5, copies),
    }


if __name__ == "__main__":
    for k, v in worked_example().items():
        print(f"{k:20s} {v:.4f}")
