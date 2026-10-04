from pathlib import Path
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
required=[
 'paper/main.tex','paper/PAPER_DRAFT.md','artifacts/personalized-not-persuaded-paper.pdf',
 'datasets/provenance/provenancebench.csv','datasets/human_eval/blinded_license_packet.csv',
 'behavior_lab/methods/learned_plp.py','scripts/run_provenancebench_learned.py',
 'docs/HUMAN_EVAL_PROTOCOL.md','docs/SUBMISSION_READINESS.md','docs/THREATS_TO_VALIDITY.md',
 'reports/PROVENANCEBENCH_EXECUTABLE.md','results/provenancebench_method_summary.csv',
 'scripts/claim_audit.py','docs/CLAIM_LEDGER.md','scripts/evaluate_generation_adapter.py',
 'scripts/aggregate_human_eval.py','docs/GENERATION_EVAL_PROTOCOL.md'
]
missing=[p for p in required if not (ROOT/p).exists()]
if missing:
 print('MISSING',missing); sys.exit(1)
# project-date guard outside bibliography-like sources: no release-date fields.
for p in ['README.md','RESULTS_CARD.md','PORTFOLIO_BRIEF.md','RELEASE_NOTES.md','index.html']:
 txt=(ROOT/p).read_text(errors='ignore')
 if re.search(r'date-released|built on|release date',txt,re.I):
  print('DATE FIELD',p); sys.exit(2)
print('submission audit PASS:',len(required),'required artifacts present')
