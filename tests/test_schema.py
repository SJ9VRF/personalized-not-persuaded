import json
from pathlib import Path

from behavior_lab.data.schema import BehaviorScenario
from behavior_lab.data.validate import validate_jsonl


def test_seed_dataset_valid():
    path = Path("datasets/canonical/seed_scenarios.jsonl")
    count, errors = validate_jsonl(path)
    assert count >= 12
    assert errors == []


def test_first_scenario_parses():
    line = Path("datasets/canonical/seed_scenarios.jsonl").read_text(encoding="utf-8").splitlines()[0]
    scenario = BehaviorScenario.from_dict(json.loads(line))
    assert scenario.scenario_id
    assert scenario.metadata["split"] == "pilot"
