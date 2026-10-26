"""Data structures. Each class names the glossary term it implements."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Literal, Optional

Vote = Literal["endorse", "reject", "abstain"]
Action = Literal["approve", "defer", "reject"]
Channel = Literal["public", "private"]


@dataclass
class EvidenceItem:
    """Glossary: evidence item. `origin` groups items that carry the same information.
    `parent` is None for an origin observation and the parent's id for a derivative."""
    id: str
    origin: str
    parent: Optional[str]
    reports_true: bool
    source_name: str
    text: str


@dataclass
class Claim:
    """Glossary: claim. A proposition that is true or false in the case world."""
    text: str
    predicate: str
    subject: str
    time: str


@dataclass
class Case:
    """Glossary: case. One claim, its ground truth, and its evidence pool with provenance.
    `presented_pool` are the ids the proposer may present; `private_slices` are the ids each
    reviewer holds privately. Both depend on the regime's provenance factor."""
    case_id: str
    family: str
    truth: bool
    claim: Claim
    evidence: list[EvidenceItem]
    presented_pool: list[str]
    private_slices: dict[str, list[str]]

    def item(self, item_id: str) -> EvidenceItem:
        for e in self.evidence:
            if e.id == item_id:
                return e
        raise KeyError(item_id)

    def origins_of(self, ids: list[str]) -> set[str]:
        return {self.item(i).origin for i in ids}


@dataclass
class Message:
    sender: str
    to: str
    channel: Channel
    text: str


@dataclass
class Endorsement:
    """Glossary: endorsement (vote='endorse'), rejection, or abstention."""
    vote: Vote
    cited: list[str]
    reason: str
    p_true: float


@dataclass
class Decision:
    """Glossary: approval (action='approve'), deferral, or rejection by the decider."""
    action: Action
    p_true: float


@dataclass
class RegimeFactors:
    provenance: Literal["independent", "shared"]
    exposure: bool
    channel: Literal["none", "public", "private"]
    payoff_P: Literal["accuracy", "approval"]
    payoff_R: Literal["accuracy", "approval", "approval_pivotal"]  # pivotal: a lone endorser of a false claim is blamed
    scripted_talk: bool = False  # regime F: inject scripted coordination proposals
    proposer_knows_reviewer_rule: bool = False  # regime E1q: the proposer is told the reviewers' blame rule


@dataclass
class Trajectory:
    """Glossary: trajectory. The complete log of one run. The auditor sees a slice of this;
    the regime label is never part of any slice."""
    run_id: str
    case_id: str
    family: str
    regime: str
    seed: int
    truth: bool
    claim: Claim
    evidence: list[EvidenceItem]
    regime_factors: RegimeFactors
    presented: list[str]
    private_slices: dict[str, list[str]]
    messages: list[Message]
    endorsements: dict[str, Endorsement]
    exposure_order: list[tuple[str, list[str]]]
    decision: Decision
    payoffs: dict[str, float]
    invalid_approval: bool
    agents: dict[str, str]
    counterfactual_of: Optional[str] = None
    dropped_reason: Optional[str] = None
    extra: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    @property
    def key(self) -> str:
        return f"{self.case_id}:{self.regime}:{self.seed}"
