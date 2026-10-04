from behavior_lab.post_training.curriculum import build_training_example

def test_build_failure_curriculum_item():
    r=dict(case_id="X", split_eval="ood_test", task_kind="personal_state", signal_content="Calendar says 3pm", scope="personal_fact", provenance="tool_verified", confidence=0.95, current=1, relevant=1,
           presentation_license=0, personalization_license=0, evidence_license=1,
           hybrid_presentation_license=0, hybrid_personalization_license=0, hybrid_evidence_license=0)
    ex=build_training_example(r)
    assert ex is not None
    assert "evidence:starvation" in ex["failure_types"]
    assert ex["target_licenses"]["evidence"] == 1
    assert ex["priority"] >= 5
