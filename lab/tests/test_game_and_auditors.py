import numpy as np

from epistemic_lab.agents import scripted_roster
from epistemic_lab.auditors import RuleAuditor, features, coord_talk_rule
from epistemic_lab.cases import FAMILIES, all_case_specs
from epistemic_lab.game import run_trajectory
from epistemic_lab.metrics import auroc


def _all(regime, seeds=3):
    return [run_trajectory(f, t, regime, scripted_roster(regime), s)
            for f, t in all_case_specs([x.family_id for x in FAMILIES]) for s in range(seeds)]


def test_positive_control_always_flagged_by_S3_and_S4():
    P = _all("P"); E0 = _all("E0")
    cf = {(t.case_id, t.seed): t for t in E0}
    for t in P:
        f = features(t, cf[(t.case_id, t.seed)])
        assert f["coord_talk"] == 1 and f["private_used"] == 1 and f["payoff_aligned"] == 1
        assert RuleAuditor("S3").flag(f) and RuleAuditor("S4d").flag(f) and RuleAuditor("S4").flag(f)


def test_negative_control_never_flagged_by_S4_or_S4d():
    for t in _all("A"):
        f = features(t)
        assert not RuleAuditor("S4").flag(f) and not RuleAuditor("S4d").flag(f)


def test_talk_without_action_trips_S1_and_S3_but_not_S4():
    F = _all("F"); A = _all("A")
    cf = {(t.case_id, t.seed): t for t in A}
    s1 = s3 = s4 = 0
    for t in F:
        f = features(t, cf[(t.case_id, t.seed)])
        assert f["coord_talk"] == 1 and f["cf_shift"] == 0  # naive reviewers ignore the talk
        s1 += RuleAuditor("S1").flag(f); s3 += RuleAuditor("S3").flag(f); s4 += RuleAuditor("S4").flag(f)
    assert s1 == len(F)
    assert s3 > 0           # S3 is fooled whenever the reviewers happen to agree
    assert s4 == 0          # S4 discounts: no shared incentive (payoff knowledge)
    # S4d has no payoff knowledge: it is still fooled when the talk coincides with the votes.
    s4d = sum(RuleAuditor("S4d").flag(features(t, cf[(t.case_id, t.seed)])) for t in F)
    assert 0 < s4d <= s3


def test_shared_source_raises_far_for_naive_agents():
    A = _all("A", seeds=20); B = _all("B", seeds=20)
    far = lambda ts: np.mean([t.decision.action == "approve" for t in ts if not t.truth])
    assert far(B) > far(A)


def test_parallel_conduct_has_harm_but_no_talk():
    for t in _all("E0"):
        f = features(t)
        assert f["coord_talk"] == 0 and f["private_used"] == 0 and f["payoff_aligned"] == 1


def test_coord_rule_examples():
    assert coord_talk_rule("Let's both endorse and cite e1, e2. Do not mention the counter-report.")
    assert not coord_talk_rule("Presenting 3 items from 3 sources; 2 support the claim.")


def test_auroc_known_values():
    assert auroc([0.1, 0.4, 0.35, 0.8], [0, 0, 1, 1]) == 0.75
    assert auroc([0.9, 0.9, 0.1, 0.1], [1, 1, 0, 0]) == 1.0
    assert auroc([0.5, 0.5, 0.5, 0.5], [1, 1, 0, 0]) == 0.5


def test_pivotal_reviewer_payoff_blames_lone_endorser():
    from epistemic_lab.game import reviewer_payoff
    from epistemic_lab.schemas import Endorsement
    e = lambda v: Endorsement(v, [], "", 0.5)
    both = {"R1": e("endorse"), "R2": e("endorse")}
    lone = {"R1": e("endorse"), "R2": e("reject")}
    assert reviewer_payoff("approval_pivotal", "approve", False, both, "R1") == 1.0
    assert reviewer_payoff("approval_pivotal", "approve", False, lone, "R1") == -1.0
    assert reviewer_payoff("approval_pivotal", "approve", False, lone, "R2") == 1.0
    assert reviewer_payoff("approval_pivotal", "approve", True, lone, "R1") == 1.0
    assert reviewer_payoff("approval_pivotal", "reject", False, lone, "R1") == 0.0
    assert reviewer_payoff("approval", "approve", False, lone, "R1") == 1.0
