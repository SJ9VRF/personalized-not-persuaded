from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parents[1]
FILES=[
'datasets/behaviorbench/behaviorbench_v1.jsonl',
'datasets/contracts/counterfactual_personalization_contracts_v1.jsonl',
'behavior_lab/eval/scorer.py',
'behavior_lab/methods/cgsp.py',
'scripts/build_contract_benchmark.py',
'scripts/contract_eval.py',
]
def sha(p):
    return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
manifest={'protocol_version':'1.3.1','frozen_files':{p:sha(p) for p in FILES},'notes':[
'Hashes freeze the benchmark inputs and automatic evaluator used for the bundled proxy results.',
'Any future modification to a frozen file requires a protocol version bump and fresh results.',
'Human-labeled or real-model extensions should preserve the frozen benchmark split for comparable reporting.'
]}
(ROOT/'results/protocol_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
lines=['# Frozen Evaluation Protocol','',f"**Protocol version:** `{manifest['protocol_version']}`",'',
'This file makes post-hoc changes auditable. The bundled proxy results are tied to the following SHA-256 hashes.','',
'| Artifact | SHA-256 |','|---|---|']
for p,h in manifest['frozen_files'].items(): lines.append(f'| `{p}` | `{h}` |')
lines += ['', '## Change policy','',
'- Changes to any frozen artifact require a protocol version bump.',
'- Results from different protocol versions must not be pooled without re-running the full pipeline.',
'- New human/model adapters may be added without changing the frozen scenarios or split.',
'- Automatic-grader revisions should be reported as a new grader version and calibrated independently.']
(ROOT/'docs/FROZEN_PROTOCOL.md').write_text('\n'.join(lines)+'\n')
print('wrote frozen protocol manifest')
