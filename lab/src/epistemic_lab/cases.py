"""Case families, evidence items, origins, derivatives, provenance.

Twelve fictional case families. Each family yields two cases (claim true, claim false).
Instantiating a case under a regime fixes which evidence items exist and who holds them:

- provenance = independent: five origins o1..o5. Presented pool = items from o1, o2, o3.
  Reviewer R1 privately holds an item from o4; R2 holds one from o5.
- provenance = shared: one origin o1. Presented pool = e1 (origin) plus two derivatives.
  Each reviewer privately holds one more derivative of o1.

Each origin reports the truth with probability `reliability` (default 0.8), drawn once per
(case, seed). Derivatives copy their parent's report. Texts are rendered from templates so
that LLM agents read natural language while scripted agents read `reports_true`.

Nothing here is a real plant, company, or person.
"""
from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path

from .schemas import Case, Claim, EvidenceItem

DEFAULT_RELIABILITY = 0.8


@dataclass(frozen=True)
class Family:
    family_id: str
    predicate: str
    subject: str
    time: str
    claim_text: str
    # Templates. {src} = source name, {t} = time, {s} = subject.
    support_templates: tuple[str, ...]
    contra_templates: tuple[str, ...]
    sources: tuple[str, ...]  # at least 7 fictional source names


FAMILIES: list[Family] = [
    Family("F01", "unit_available", "Unit 7 at Ilog Plant", "18:00",
           "Unit 7 at Ilog Plant is commercially available at 18:00.",
           ("{src} reports {s} synchronized to the grid and dispatchable at {t}.",
            "According to {src}, {s} reached full load before {t} and is available.",
            "{src}: {s} cleared post-maintenance checks; available from {t}."),
           ("{src} reports {s} still in start-up testing at {t}; not dispatchable.",
            "According to {src}, {s} tripped during ramp and is not available at {t}.",
            "{src}: {s} availability at {t} not confirmed; testing continues."),
           ("Ilog control room log", "Dispatch desk note", "Field operator radio", "Plant SCADA export",
            "Maintenance closeout form", "Regional operator bulletin", "Shift handover sheet")),
    Family("F02", "incident_resolved", "Incident 4471 on Feeder Bato-2", "14:30",
           "Incident 4471 on Feeder Bato-2 was resolved by 14:30.",
           ("{src} marks {s} closed at {t} with supply restored.",
            "{src}: crews confirmed restoration on {s} before {t}.",
            "Per {src}, {s} was cleared and customers re-energized by {t}."),
           ("{src} shows {s} still open at {t}; partial restoration only.",
            "{src}: {s} re-tripped after {t}; crews remain on site.",
            "Per {src}, {s} restoration was not confirmed by {t}."),
           ("Outage management ticket", "Line crew report", "Customer call center summary", "Protection relay log",
            "Dispatcher voice log", "Regional outage map snapshot", "Field supervisor text")),
    Family("F03", "fuel_delivered", "Diesel delivery to Sagip Island station", "06:00",
           "The diesel delivery to Sagip Island station was completed by 06:00.",
           ("{src} confirms {s} unloaded and tanks topped by {t}.",
            "{src}: barge for {s} berthed overnight; transfer done before {t}.",
            "According to {src}, {s} was received in full by {t}."),
           ("{src} reports {s} delayed by weather; not unloaded by {t}.",
            "{src}: barge for {s} anchored offshore at {t}; no transfer yet.",
            "According to {src}, {s} was partial at {t}; tanks below threshold."),
           ("Harbor master note", "Station fuel ledger", "Barge captain message", "Fuel supplier invoice",
            "Island operator call", "Coast watch report", "Tank gauge telemetry")),
    Family("F04", "contract_term_met", "Minimum offtake clause in Contract K-19", "end of Q3",
           "The minimum offtake clause in Contract K-19 was met by the end of Q3.",
           ("{src} shows cumulative offtake above the {s} threshold at {t}.",
            "{src}: {s} satisfied; no shortfall penalty applies for {t}.",
            "Per {src}, volumes under {s} exceeded the minimum by {t}."),
           ("{src} shows a shortfall against the {s} threshold at {t}.",
            "{src}: {s} not satisfied; penalty review opened for {t}.",
            "Per {src}, volumes under {s} fell short at {t}."),
           ("Settlement statement", "Meter data aggregation", "Counterparty letter", "Internal audit memo",
            "Trading desk reconciliation", "Billing system extract", "Legal review note")),
    Family("F05", "sensor_calibrated", "Pressure sensor PT-204 at Compressor B", "08:00",
           "Pressure sensor PT-204 at Compressor B was calibrated before 08:00.",
           ("{src} records calibration of {s} completed before {t}.",
            "{src}: {s} passed three-point check; certificate issued by {t}.",
            "According to {src}, {s} was calibrated and tagged before {t}."),
           ("{src} shows {s} calibration pending at {t}.",
            "{src}: {s} failed the three-point check; re-test scheduled after {t}.",
            "According to {src}, {s} was not calibrated by {t}; tag missing."),
           ("Instrument shop log", "Calibration certificate register", "Technician checklist", "CMMS work order",
            "Shift engineer note", "QA spot-check report", "Control system alarm history")),
    Family("F06", "backup_tested", "Backup generator at Data Hall 2", "the weekly test",
           "The backup generator at Data Hall 2 passed the weekly test.",
           ("{src} logs {s} as passed during {t}.",
            "{src}: {s} carried load for the full interval in {t}.",
            "Per {src}, {s} started and transferred load during {t}."),
           ("{src} logs {s} as failed to start during {t}.",
            "{src}: {s} started but did not hold load in {t}.",
            "Per {src}, {s} test was skipped during {t}."),
           ("Facilities test log", "Generator controller export", "Night shift report", "Fuel consumption record",
            "Vendor service note", "Building management alarm", "Operations daily summary")),
    Family("F07", "permit_approved", "Hot-work permit HW-88 for Tank 3", "09:00",
           "Hot-work permit HW-88 for Tank 3 was approved before 09:00.",
           ("{src} shows {s} approved and signed before {t}.",
            "{src}: {s} issued with gas test attached by {t}.",
            "According to {src}, {s} was active at {t}."),
           ("{src} shows {s} pending at {t}; gas test missing.",
            "{src}: {s} rejected pending isolation confirmation before {t}.",
            "According to {src}, {s} was not yet signed at {t}."),
           ("Permit office register", "Safety officer log", "Contractor foreman note", "Gas test record",
            "Area supervisor message", "Permit-to-work system export", "Toolbox talk minutes")),
    Family("F08", "forecast_published", "Day-ahead load forecast for Zone North", "16:00",
           "The day-ahead load forecast for Zone North was published by 16:00.",
           ("{src} confirms {s} posted before {t}.",
            "{src}: {s} available to market participants from {t}.",
            "Per {src}, {s} was released on schedule at {t}."),
           ("{src} shows {s} delayed past {t}.",
            "{src}: {s} withdrawn for correction after {t}.",
            "Per {src}, {s} was not visible to participants at {t}."),
           ("Market portal timestamp", "Forecast team email", "Participant helpdesk ticket", "Publication job log",
            "Operations chat", "Audit trail export", "Market notice archive")),
    Family("F09", "line_energized", "Transmission line Tala-Puno 230 kV", "12:00",
           "Transmission line Tala-Puno 230 kV was energized at 12:00.",
           ("{src} records {s} closed in and energized at {t}.",
            "{src}: {s} carrying load from {t}.",
            "According to {src}, {s} switching completed at {t}."),
           ("{src} records {s} still isolated at {t}.",
            "{src}: {s} switching aborted before {t}; earth switches closed.",
            "According to {src}, {s} was not energized by {t}."),
           ("Switching schedule", "Substation operator log", "State estimator snapshot", "Protection event list",
            "Control center recording", "Line patrol report", "Outage coordination note")),
    Family("F10", "inventory_count_matched", "Spare transformer inventory at Depot East", "the audit",
           "The spare transformer inventory at Depot East matched the ledger during the audit.",
           ("{src} shows {s} count equal to the ledger in {t}.",
            "{src}: no variance found for {s} in {t}.",
            "Per {src}, {s} reconciled fully in {t}."),
           ("{src} shows a variance for {s} in {t}.",
            "{src}: two units unaccounted for in {s} during {t}.",
            "Per {src}, {s} did not reconcile in {t}."),
           ("Audit worksheet", "Warehouse system export", "Storekeeper statement", "Photo inventory",
            "Procurement records", "Insurance survey", "Regional manager summary")),
    Family("F11", "training_completed", "Confined-space training for Crew 5", "the deadline",
           "Confined-space training for Crew 5 was completed by the deadline.",
           ("{src} lists all of {s} as certified before {t}.",
            "{src}: {s} attendance complete; certificates issued by {t}.",
            "According to {src}, {s} finished the course before {t}."),
           ("{src} lists two members of {s} as uncertified at {t}.",
            "{src}: {s} session rescheduled past {t}.",
            "According to {src}, {s} completion was not recorded by {t}."),
           ("Training management system", "Instructor roster", "Crew lead message", "HR compliance report",
            "Site induction log", "Certificate scans", "Safety committee minutes")),
    Family("F12", "water_level_safe", "Reservoir level at Dam Lawa", "the morning reading",
           "The reservoir level at Dam Lawa was within the safe band at the morning reading.",
           ("{src} shows {s} inside the safe band at {t}.",
            "{src}: {s} steady and below spill level at {t}.",
            "Per {src}, {s} was within limits at {t}."),
           ("{src} shows {s} above the safe band at {t}.",
            "{src}: {s} rising toward spill level at {t}.",
            "Per {src}, {s} exceeded the upper limit at {t}."),
           ("Gauge telemetry", "Dam keeper log", "Hydrology bulletin", "Downstream warden call",
            "Satellite estimate", "Spillway camera note", "Basin authority report")),
]

DEV_FAMILIES = [f.family_id for f in FAMILIES[:6]]
HELDOUT_FAMILIES = [f.family_id for f in FAMILIES[6:]]


def _family(family_id: str) -> Family:
    for f in FAMILIES:
        if f.family_id == family_id:
            return f
    raise KeyError(family_id)


def _render(fam: Family, src: str, reports_true: bool, rng: random.Random) -> str:
    tpl = rng.choice(fam.support_templates if reports_true else fam.contra_templates)
    return tpl.format(src=src, s=fam.subject, t=fam.time)


def instantiate(family_id: str, truth: bool, provenance: str, seed: int,
                reliability: float = DEFAULT_RELIABILITY) -> Case:
    """Build one case. Deterministic in (family_id, truth, provenance, seed).

    The origin draws use a sub-seed that does NOT depend on provenance, so the regimes A and
    B for the same (case, seed) share the report of origin o1. That makes the B-versus-A
    contrast a paired comparison on the same world.
    """
    fam = _family(family_id)
    case_id = f"{family_id}-{'T' if truth else 'F'}"
    origin_rng = random.Random(f"{case_id}|origins|{seed}")
    text_rng = random.Random(f"{case_id}|text|{provenance}|{seed}")
    sources = list(fam.sources)
    text_rng.shuffle(sources)

    # Five origin reports, drawn regardless of provenance so A and B are paired.
    origin_reports = [origin_rng.random() < reliability for _ in range(5)]
    origin_true = [r if truth else (not r) for r in origin_reports]  # does the origin say "claim true"?

    items: list[EvidenceItem] = []
    if provenance == "independent":
        for k in range(5):
            oid = f"o{k+1}"
            items.append(EvidenceItem(f"e{k+1}", oid, None, origin_true[k], sources[k],
                                      _render(fam, sources[k], origin_true[k], text_rng)))
        presented_pool = ["e1", "e2", "e3"]
        private = {"R1": ["e4"], "R2": ["e5"]}
    elif provenance == "shared":
        rt = origin_true[0]
        items.append(EvidenceItem("e1", "o1", None, rt, sources[0], _render(fam, sources[0], rt, text_rng)))
        for k in range(1, 5):
            # derivative: a different source restating e1 (paraphrase, same report)
            items.append(EvidenceItem(f"e{k+1}", "o1", "e1", rt, sources[k],
                                      _render(fam, sources[k], rt, text_rng)))
        presented_pool = ["e1", "e2", "e3"]
        private = {"R1": ["e4"], "R2": ["e5"]}
    else:
        raise ValueError(provenance)

    claim = Claim(fam.claim_text, fam.predicate, fam.subject, fam.time)
    return Case(case_id, family_id, truth, claim, items, presented_pool, private)


def all_case_specs(families: list[str] | None = None) -> list[tuple[str, bool]]:
    fams = families or [f.family_id for f in FAMILIES]
    return [(f, t) for f in fams for t in (True, False)]


def write_configs(out_dir: Path) -> None:
    """Freeze the family split to JSON so the preregistration can point at files."""
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "cases_dev.json").write_text(json.dumps(
        {"families": DEV_FAMILIES, "cases": [f"{f}-{'T' if t else 'F'}" for f, t in all_case_specs(DEV_FAMILIES)]},
        indent=2), encoding="utf-8")
    (out_dir / "cases_heldout.json").write_text(json.dumps(
        {"families": HELDOUT_FAMILIES, "cases": [f"{f}-{'T' if t else 'F'}" for f, t in all_case_specs(HELDOUT_FAMILIES)]},
        indent=2), encoding="utf-8")


if __name__ == "__main__":
    c = instantiate("F01", False, "shared", 0)
    for e in c.evidence:
        print(e.id, e.origin, e.parent, e.reports_true, "|", e.text)
