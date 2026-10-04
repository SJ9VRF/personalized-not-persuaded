from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = [
    'README.md','PORTFOLIO_BRIEF.md','RESULTS_CARD.md','REVIEWER_GUIDE.md',
    'index.html','site/index.html','paper/PAPER_DRAFT.md','paper/main.tex','CITATION.cff',
    'docs/MODEL_CARD.md'
]
REQUIRED_TITLE = 'Learning When Personal Context Counts as Evidence'
BANNED = {
    'Learning Evidentiary Standing for Personal Context': 'stale paper subtitle',
    'public URL is not fabricated': 'defensive public wording',
    'No human labels are fabricated': 'defensive public wording',
    'complete research system': 'promotional wording',
    'best candidate': 'promotional wording',
    'state-of-the-art personalization method': 'unsupported SOTA wording',
    'repository ships three deterministic policies solely': 'stale pre-learned-method model-card wording',
}

errors=[]
for rel in PUBLIC:
    p=ROOT/rel
    if not p.exists():
        errors.append(f'missing public artifact: {rel}')
        continue
    text=p.read_text(encoding='utf8',errors='ignore')
    for phrase, reason in BANNED.items():
        if phrase.lower() in text.lower():
            errors.append(f'{rel}: {reason}: {phrase!r}')

# title must be consistent on the main public surfaces
for rel in ['README.md','index.html','site/index.html','paper/PAPER_DRAFT.md','paper/main.tex','CITATION.cff']:
    text=(ROOT/rel).read_text(encoding='utf8',errors='ignore')
    if REQUIRED_TITLE.lower() not in text.lower():
        errors.append(f'{rel}: missing current subtitle')


# Homepage contract also requires the requested citation year and 60-second summary.
home=(ROOT/'index.html').read_text(encoding='utf8',errors='ignore')
for phrase in ['60-second project summary','Recovery on naive failures','Median latency','External API cost','GitHub','Recorded passing trial','2026']:
    if phrase.lower() not in home.lower():
        errors.append(f'index.html: missing homepage requirement: {phrase}')
if 'year   = {2026}' not in home:
    errors.append('index.html: BibTeX citation year must be 2026')

if errors:
    print('PUBLIC SURFACE AUDIT: FAIL')
    for e in errors: print('-',e)
    sys.exit(1)
print('PUBLIC SURFACE AUDIT: PASS')
