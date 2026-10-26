"""Exercise the LLM code path with a fake client: no network, no key. Catches format-string
and parse bugs before the first paid call."""
import json

from epistemic_lab.agents import llm_roster
from epistemic_lab.auditors import LLMJudgeAuditor, features, render_slice
from epistemic_lab.game import run_trajectory
from epistemic_lab.prompts import parse_json


class FakeClient:
    model = "fake/model"

    def __init__(self):
        self.prompts = []

    def chat_agent(self, prompt: str) -> str:
        self.prompts.append(prompt)
        if prompt.startswith("You are the PROPOSER"):
            pm = "Let's both endorse and cite e1, e2." if "ONE private message" in prompt else None
            return json.dumps({"present": ["e1", "e2"], "public_message": "Two reports support it.", "private_message": pm})
        if prompt.startswith("You are REVIEWER") and "sent you this private message" in prompt:
            return json.dumps({"reply": "Agreed."})
        if prompt.startswith("You are REVIEWER"):
            return '```json\n' + json.dumps({"vote": "endorse", "cited": ["e1", "e2"], "reason": "ok", "p_true": 0.8}) + '\n```'
        if prompt.startswith("You are the DECIDER"):
            return json.dumps({"action": "approve", "p_true": 0.85})
        raise AssertionError("unexpected prompt")

    def chat_judge(self, prompt: str) -> str:
        assert prompt.startswith("You are an AUDITOR")
        return json.dumps({"p_collusion": 0.7, "strongest_evidence": "x", "strongest_innocent_explanation": "y"})


def test_llm_roster_runs_all_regimes_and_renders_slices():
    c = FakeClient()
    trajs = {}
    for r in ("A", "B", "C", "D", "E0", "E1", "F", "P"):
        t = run_trajectory("F01", False, r, llm_roster(c, r), seed=0, run_id="fake")
        trajs[r] = t
        assert t.decision.action in ("approve", "defer", "reject")
        assert set(t.endorsements) == {"R1", "R2"}
        assert t.presented and all(i in {e.id for e in t.evidence} for i in t.presented)
        json.dumps(t.to_dict())  # serializable
    # F proposer saw no channel: its prompt equals A's prompt, so presented sets match
    assert trajs["F"].presented == trajs["A"].presented
    assert any(m.channel == "private" for m in trajs["F"].messages)
    assert not any(m.channel == "private" for m in trajs["E0"].messages)
    assert any(m.channel == "private" and m.sender == "P" for m in trajs["E1"].messages)
    # features and every slice render on an LLM trajectory
    f = features(trajs["E1"], trajs["E0"])
    assert f["coord_talk"] == 1 and f["followed_plan"] == 1
    for s in ("S1", "S2", "S3", "S4d", "S4"):
        text = render_slice(trajs["E1"], s, trajs["E0"])
        assert "CLAIM:" in text
    out = LLMJudgeAuditor(c, "S4").judge(trajs["E1"], trajs["E0"])
    assert 0 <= out["score"] <= 1


def test_parse_json_variants():
    assert parse_json('{"a": 1}') == {"a": 1}
    assert parse_json('text before ```json\n{"a": 2}\n``` after') == {"a": 2}
    assert parse_json('noise {"a": 3} trailing') == {"a": 3}
