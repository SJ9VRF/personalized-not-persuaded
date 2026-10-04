from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    'README.md','PORTFOLIO_BRIEF.md','RESULTS_CARD.md','REVIEWER_GUIDE.md','site/index.html','index.html','paper/PAPER_DRAFT.md',
    'dashboard/index.html','behavior_lab','datasets/behaviorbench/behaviorbench_v1.jsonl',
    'scripts/run_all.py','tests','.github/workflows/ci.yml','.github/workflows/pages.yml','results/summary.json',
    'docs/HUMAN_EVAL_PROTOCOL.md','docs/REAL_MODEL_ADAPTER.md','docs/GENERATION_EVAL_PROTOCOL.md','docs/BENCHMARK_CARD.md','docs/FROZEN_PROTOCOL.md','docs/THREATS_TO_VALIDITY.md','docs/ETHICS_AND_MISUSE.md','datasets/contracts/counterfactual_personalization_contracts_v1.jsonl','reports/COUNTERFACTUAL_CONTRACTS.md','reports/CGSP_ABLATIONS.md','reports/CONTRACT_STATISTICS.md','results/counterfactual_contract_summary.csv','results/cgsp_ablation_summary.csv','results/contract_bootstrap_ci.csv','results/protocol_manifest.json','behavior_lab/methods/learned_plp.py','tests/test_learned_plp.py','reports/PROVENANCEBENCH_EXECUTABLE.md','results/provenancebench_method_summary.csv','datasets/provenance/provenance_intervention_test.csv','datasets/human_eval/heldout_answer_key.csv','artifacts/personalized-not-persuaded-paper.pdf','artifacts/personalized-not-persuaded-source.zip','media/personalized-not-persuaded-walkthrough.mp4','site/demo.html','docs/PLP_TECHNICAL_REPORT.md','docs/BLOG_POST.md','docs/HOMEPAGE_CHECKLIST.md','results/homepage_runtime_summary.json','results/homepage_trial_examples.json','scripts/build_homepage_assets.py'
]
errors=[]
for rel in required:
    if not (ROOT/rel).exists(): errors.append(f'MISSING: {rel}')

# Local markdown-link audit.
md_link = re.compile(r'\[[^\]]+\]\(([^)]+)\)')
for p in ROOT.rglob('*.md'):
    text=p.read_text(encoding='utf-8', errors='replace')
    for target in md_link.findall(text):
        if target.startswith(('http://','https://','#','mailto:')): continue
        clean=target.split('#',1)[0]
        if not clean: continue
        dest=(p.parent/clean).resolve()
        if not dest.exists(): errors.append(f'BROKEN LINK: {p.relative_to(ROOT)} -> {target}')


# Local HTML href audit.
href = re.compile(r'href=["\']([^"\']+)["\']')
for p in ROOT.rglob('*.html'):
    text=p.read_text(encoding='utf-8', errors='replace')
    for target in href.findall(text):
        if target.startswith(('http://','https://','#','mailto:','javascript:')): continue
        clean=target.split('#',1)[0].split('?',1)[0]
        if not clean: continue
        dest=(p.parent/clean).resolve()
        if not dest.exists(): errors.append(f'BROKEN HTML LINK: {p.relative_to(ROOT)} -> {target}')


# Flagship homepage contract: exactly 14 numbered sections plus the requested citation year.
home=(ROOT/'index.html').read_text(encoding='utf-8', errors='replace')
labels=re.findall(r'<div class="tag">(\d{2}) ·', home)
expected=[f'{i:02d}' for i in range(1,15)]
if labels != expected:
    errors.append(f'HOMEPAGE SECTIONS: expected {expected}, got {labels}')
for phrase in ['year   = {n.d.}', 'project date intentionally', 'release date']:
    if phrase.lower() in home.lower(): errors.append(f'PROJECT DATE PLACEHOLDER IN HOMEPAGE: {phrase}')
for must in ['Paper','Code','Demo','Benchmark','Video','Domain-OOD exact','provenance intervention','Irreversible external actions','Human escalation','BibTeX','year   = {2026}','GitHub','Recovery on naive failures','Median latency','External API cost','Recorded passing trial']:
    if must not in home: errors.append(f'HOMEPAGE MISSING REQUIRED CONTENT: {must}')

# Scientific-boundary wording guard.
forbidden = {
    'paper/PAPER_DRAFT.md': ['human-authored benchmark translations'],
}
for rel, phrases in forbidden.items():
    text=(ROOT/rel).read_text(encoding='utf-8', errors='replace')
    for phrase in phrases:
        if phrase in text: errors.append(f'FORBIDDEN CLAIM: {rel}: {phrase}')

# Ensure release is substantive, not a presentation-only shell.
file_count=sum(1 for p in ROOT.rglob('*') if p.is_file() and '.pytest_cache' not in p.parts)
if file_count < 80: errors.append(f'INCOMPLETE RELEASE: only {file_count} files')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'PASS release audit: {file_count} files; required artifacts present; local links valid; scientific-boundary guards clean.')
