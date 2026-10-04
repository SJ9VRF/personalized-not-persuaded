from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(prog="behavior-lab", description="Model Behavior Lab command line interface")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("all", help="Run the complete reproducible research pipeline")
    sub.add_parser("test", help="Run unit tests")
    sub.add_parser("benchmark", help="Regenerate and evaluate BehaviorBench")
    sub.add_parser("dashboard", help="Rebuild the static dashboard")
    args = parser.parse_args()

    py = sys.executable
    if args.command == "all":
        run([py, "scripts/run_all.py"])
    elif args.command == "test":
        run([py, "-m", "pytest", "-q"])
    elif args.command == "benchmark":
        run([py, "-m", "behavior_lab.generation.generate"])
        run([py, "-m", "behavior_lab.data.validate", "datasets/behaviorbench/behaviorbench_v1.jsonl"])
        run([py, "scripts/run_benchmark.py"])
    elif args.command == "dashboard":
        run([py, "scripts/build_dashboard.py"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
