from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

STEPS = [
    [sys.executable, 'scripts/build_provenance_intervention.py'],
    [sys.executable, 'scripts/run_provenancebench_learned.py'],
    [sys.executable, 'scripts/provenancebench_stats_strict.py'],
    [sys.executable, 'scripts/provenancebench_multiseed.py'],
    [sys.executable, 'scripts/run_trial_eval.py'],
    [sys.executable, 'scripts/build_failure_curriculum.py'],
    [sys.executable, 'scripts/build_training_mixture.py'],
    [sys.executable, 'scripts/launch_gate.py'],
    [sys.executable, 'scripts/regression_gate.py'],
    [sys.executable, 'scripts/submission_audit.py'],
    [sys.executable, 'scripts/claim_audit.py'],
    [sys.executable, 'scripts/result_consistency_audit.py'],
    [sys.executable, 'scripts/public_surface_audit.py'],
]


def run(cmd: list[str]) -> None:
    print('+', ' '.join(cmd), flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)


if __name__ == '__main__':
    for step in STEPS:
        run(step)
    print('paper pipeline complete')
