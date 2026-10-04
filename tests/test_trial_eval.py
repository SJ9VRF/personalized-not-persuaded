from behavior_lab.evals.trials import build_trial

def row(**kw):
    r = dict(case_id="X", split_eval="test", task_kind="personal_state", signal_content="Calendar says 3pm", scope="personal_fact", provenance="tool_verified", confidence=0.95, current=1, relevant=1,
             presentation_license=0, personalization_license=0, evidence_license=1,
             hybrid_presentation_license=0, hybrid_personalization_license=0, hybrid_evidence_license=1)
    r.update(kw); return r

def test_trial_passes_when_state_matches():
    t=build_trial(row())
    assert t.passed and t.weighted_score == 1.0
    assert any(e["event"] == "state_verification" for e in t.trajectory)

def test_evidence_error_is_weighted():
    t=build_trial(row(hybrid_evidence_license=0))
    assert not t.passed
    assert t.weighted_score == 0.5
