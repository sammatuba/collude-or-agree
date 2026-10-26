from epistemic_lab.bayes import worked_example, likelihood_ratio, posterior_naive, posterior_provenance_aware, Report


def test_worked_example_matches_starter():
    ex = worked_example()
    assert abs(ex["independent_naive"] - 64 / 65) < 1e-9
    assert abs(ex["copies_naive"] - 64 / 65) < 1e-9          # naive double counts copies
    assert abs(ex["copies_aware"] - 0.8) < 1e-9              # one origin -> 4/5
    assert abs(ex["independent_aware"] - 64 / 65) < 1e-9


def test_likelihood_ratio_symmetry():
    assert abs(likelihood_ratio(0.8, True) * likelihood_ratio(0.8, False) - 1.0) < 1e-12


def test_contradicting_copy_does_not_cancel():
    # Two derivatives of one origin cannot disagree; a provenance-aware update uses the first.
    reps = [Report("o1", 0.8, True), Report("o1", 0.8, True)]
    assert posterior_provenance_aware(0.5, reps) == posterior_naive(0.5, reps[:1])
