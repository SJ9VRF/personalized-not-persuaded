from behavior_lab.methods.plp import UserSignal, license_signal

def test_unsupported_user_world_belief_is_not_evidence():
    s=UserSignal('I believe X','world_claim','explicit_user')
    d=license_signal(s,'factual_world')
    assert not d.evidentiary

def test_verified_world_claim_is_evidence():
    s=UserSignal('Tool verified X','world_claim','tool_verified')
    assert license_signal(s,'factual_world').evidentiary

def test_explicit_personal_state_is_licensed_for_personal_task():
    s=UserSignal('My appointment is Friday','personal_state','explicit_user')
    assert license_signal(s,'personal_state').evidentiary

def test_personal_state_does_not_prove_world_claim():
    s=UserSignal('I feel X','personal_state','explicit_user')
    assert not license_signal(s,'factual_world').evidentiary

def test_preference_personalizes_but_is_not_evidence():
    s=UserSignal('I prefer concise answers','preference','explicit_user')
    d=license_signal(s,'recommendation')
    assert d.personalization and not d.evidentiary
