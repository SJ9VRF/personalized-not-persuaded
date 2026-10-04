def test_gate_semantics_are_documented():
    from pathlib import Path
    p=Path('scripts/launch_gate.py').read_text()
    assert 'research_candidate' in p
    assert 'Not a production launch approval' in p
