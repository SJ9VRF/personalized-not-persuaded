from pathlib import Path
import sys
import json
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from behavior_lab.post_training.curriculum import build_training_example
df = pd.read_csv(ROOT / "results/provenancebench_predictions.csv")
examples = []
for row in df.to_dict(orient="records"):
    ex = build_training_example(row, method="hybrid")
    if ex is not None:
        examples.append(ex)
examples.sort(key=lambda x: (-x["priority"], x["example_id"]))
out = ROOT / "datasets/post_training/failure_curriculum.jsonl"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("\n".join(json.dumps(x, sort_keys=True) for x in examples) + ("\n" if examples else ""))
summary = {
    "source": "Hybrid PLP errors on frozen ProvenanceBench predictions",
    "n_examples": len(examples),
    "high_priority_ge_6": sum(x["priority"] >= 6 for x in examples),
    "failure_counts": {},
    "note": "This is a training-data curriculum artifact, not evidence that post-training was run."
}
for ex in examples:
    for f in ex["failure_types"]:
        summary["failure_counts"][f] = summary["failure_counts"].get(f, 0) + 1
(ROOT / "results/failure_curriculum_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
print(json.dumps(summary, indent=2))
