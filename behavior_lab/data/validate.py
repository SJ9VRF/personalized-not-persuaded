from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

from .schema import BehaviorScenario


def validate_jsonl(path: str | Path) -> tuple[int, list[str]]:
    path = Path(path)
    errors: list[str] = []
    ids: set[str] = set()
    count = 0

    with path.open("r", encoding="utf-8") as f:
        for line_no, raw in enumerate(f, start=1):
            if not raw.strip():
                continue
            count += 1
            try:
                obj = json.loads(raw)
                scenario = BehaviorScenario.from_dict(obj)
                if scenario.scenario_id in ids:
                    raise ValueError(f"duplicate scenario_id: {scenario.scenario_id}")
                ids.add(scenario.scenario_id)
            except Exception as exc:  # validation boundary
                errors.append(f"line {line_no}: {exc}")

    return count, errors


def main(argv: Iterable[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("usage: python -m behavior_lab.data.validate <file.jsonl>")
        return 2
    count, errors = validate_jsonl(args[0])
    if errors:
        print(f"INVALID: {len(errors)} error(s) across {count} scenario(s)")
        for err in errors:
            print(f"- {err}")
        return 1
    print(f"VALID: {count} scenario(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
