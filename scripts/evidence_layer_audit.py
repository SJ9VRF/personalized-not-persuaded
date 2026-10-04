from pathlib import Path
import json, re, sys
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
errors=[]
required=[
 'evidence/README.md','evidence/index.html','evidence/EXPERIMENT_JOURNAL.md','evidence/FAILED_EXPERIMENTS.md',
 'evidence/DECISION_LOG.md','evidence/REAL_EVAL_TABLES.md','evidence/UNEXPECTED_FINDINGS.md','evidence/GIT_HISTORY.md',
 'artifacts/evidence/EVIDENCE_MANIFEST.json','artifacts/evidence/experiment_logs/experiment_registry.csv',
 'artifacts/evidence/eval_runs/provenancebench_method_summary.csv','artifacts/evidence/failure_examples/provenancebench_errors.csv',
 'artifacts/evidence/qualitative_cases/recorded_trial_examples.json','artifacts/evidence/ablations/standing_ablation_table.csv',
 'artifacts/evidence/configs/canonical_eval_config.json',
 'artifacts/evidence/git/git-log.txt','artifacts/evidence/git/personalized-not-persuaded-history.bundle',
 'artifacts/evidence/EVIDENCE_HASH_LEDGER.csv','evidence/FAILURE_TRACE.md',
 'artifacts/evidence/qualitative_cases/PI-0000-1_failure_trace.json',
]
for rel in required:
    if not (ROOT/rel).exists(): errors.append(f'missing evidence artifact: {rel}')

if (ROOT/'artifacts/evidence/experiment_logs/experiment_registry.csv').exists():
    df=pd.read_csv(ROOT/'artifacts/evidence/experiment_logs/experiment_registry.csv')
    needed={'experiment_id','name','status','hypothesis','setup','result','interpretation','next_decision','evidence_type','source_artifacts','reproduction_command','journal_provenance'}
    if len(df)!=12: errors.append(f'expected 12 logged experiments, found {len(df)}')
    if not needed.issubset(df.columns): errors.append(f'experiment registry missing columns: {sorted(needed-set(df.columns))}')
    for exp in df.experiment_id:
        if not (ROOT/f'artifacts/evidence/experiment_logs/{exp}.json').exists(): errors.append(f'missing individual log {exp}.json')

checks=[('evidence/FAILED_EXPERIMENTS.md', r'^## [1-6]\. ', 6, 'failed/revised ideas'),
        ('evidence/DECISION_LOG.md', r'^## D-\d{3} ', 8, 'decisions'),
        ('evidence/UNEXPECTED_FINDINGS.md', r'^## [1-5]\. ', 5, 'unexpected findings')]
for rel,pat,n,label in checks:
    p=ROOT/rel
    if p.exists():
        count=len(re.findall(pat,p.read_text(),re.M))
        if count!=n: errors.append(f'expected {n} {label}, found {count}')

for d in ['experiment_logs','eval_runs','failure_examples','plots','configs','qualitative_cases','ablations','git']:
    if not (ROOT/'artifacts/evidence'/d).is_dir(): errors.append(f'missing raw evidence directory: {d}')

home=(ROOT/'index.html').read_text(errors='ignore') if (ROOT/'index.html').exists() else ''
for phrase in ['Inside the research process','12</b><span>logged experiments','6</b><span>failed or revised research ideas','8</b><span>material technical decisions','5</b><span>unexpected findings','View experiment journal','What didn\'t work','Decision log','Trace one failure end to end','Reproduce results']:
    if phrase.lower() not in home.lower(): errors.append(f'homepage evidence-layer requirement missing: {phrase}')

errp=ROOT/'results/provenancebench_errors.csv'
if errp.exists() and len(pd.read_csv(errp))!=392: errors.append('frozen error count drifted from 392; update evidence narrative before release')
trial=ROOT/'results/trial_eval_summary.json'
if trial.exists():
    t=json.loads(trial.read_text())
    if int(t.get('n_trials',-1))!=2600: errors.append('trial count drifted from 2600')


# Verify the evidence hash ledger against current canonical source files.
ledger=ROOT/'artifacts/evidence/EVIDENCE_HASH_LEDGER.csv'
if ledger.exists():
    import hashlib
    ldf=pd.read_csv(ledger)
    for row in ldf.itertuples():
        p=ROOT/row.path
        if not p.exists():
            errors.append(f'hash-ledger source missing: {row.path}')
            continue
        actual=hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != row.sha256:
            errors.append(f'evidence source hash drifted: {row.path}')

# Verify the explicit real failure trace remains anchored to the same case.
tracep=ROOT/'artifacts/evidence/qualitative_cases/PI-0000-1_failure_trace.json'
if tracep.exists():
    tr=json.loads(tracep.read_text())
    if tr.get('case_id')!='PI-0000-1': errors.append('failure trace case id drifted')
    trial=tr.get('trial') or {}
    if trial.get('passed') is not False: errors.append('failure trace no longer records a failed trial')
    curr=tr.get('failure_curriculum_record') or {}
    if 'evidence:starvation' not in curr.get('failure_types',[]): errors.append('failure trace taxonomy drifted from evidence:starvation')

if errors:
    print('EVIDENCE LAYER AUDIT: FAIL')
    for e in errors: print('-',e)
    sys.exit(1)
print('EVIDENCE LAYER AUDIT: PASS')
print('12 experiments · 6 failed/revised ideas · 8 decisions · 5 unexpected findings')
print('raw evals, failures, plots, configs, trajectories, ablations and Git evidence contract verified')
