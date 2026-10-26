from epistemic_lab.cases import instantiate, FAMILIES, DEV_FAMILIES, HELDOUT_FAMILIES


def test_twelve_families_and_split():
    assert len(FAMILIES) == 12
    assert len(DEV_FAMILIES) == 6 and len(HELDOUT_FAMILIES) == 6
    assert not set(DEV_FAMILIES) & set(HELDOUT_FAMILIES)


def test_deterministic():
    a = instantiate("F01", False, "independent", 3)
    b = instantiate("F01", False, "independent", 3)
    assert [e.text for e in a.evidence] == [e.text for e in b.evidence]


def test_shared_has_one_origin_and_is_paired_with_independent():
    ind = instantiate("F02", True, "independent", 1)
    sh = instantiate("F02", True, "shared", 1)
    assert {e.origin for e in sh.evidence} == {"o1"}
    assert all(e.parent == "e1" for e in sh.evidence if e.id != "e1")
    # the origin o1 report is the same world draw in both regimes (paired contrast)
    assert ind.item("e1").reports_true == sh.item("e1").reports_true


def test_texts_follow_reports():
    c = instantiate("F05", False, "independent", 0)
    for e in c.evidence:
        assert e.text  # rendered
        assert e.source_name in e.text
