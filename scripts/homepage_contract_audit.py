from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / 'index.html'
MIRROR = ROOT / 'site' / 'index.html'

errors = []

if not HOME.exists():
    errors.append('missing index.html')
    text = ''
else:
    text = HOME.read_text(encoding='utf8', errors='ignore')

required_sections = [
    ('01', 'Hero'),
    ('02', 'Why this problem matters'),
    ('03', 'Core idea'),
    ('04', 'Architecture'),
    ('05', 'My contribution'),
    ('06', 'Experiments'),
    ('07', 'Results'),
    ('08', 'Failure analysis'),
    ('09', 'Interactive demo'),
    ('10', 'Scaling'),
    ('11', 'Safety / limitations'),
    ('12', 'Technical deep dive'),
    ('13', 'Artifacts'),
    ('14', 'Citation'),
]

positions = []
for number, title in required_sections:
    marker = f'{number} · {title}'
    pos = text.find(marker)
    if pos < 0:
        errors.append(f'missing homepage section marker: {marker}')
    else:
        positions.append((number, pos))

if len(positions) == len(required_sections):
    actual = [n for n, _ in sorted(positions, key=lambda x: x[1])]
    expected = [n for n, _ in required_sections]
    if actual != expected:
        errors.append(f'homepage sections out of order: {actual} != {expected}')

# Hero contract.
hero_requirements = [
    'Personalized,',
    'Learning When Personal Context Counts as Evidence',
    'Main result:',
    '>Paper<',
    '>Code<',
    '>Demo<',
    '>Benchmark<',
    '>Video<',
    '60-second project summary',
]
for phrase in hero_requirements:
    if phrase.lower() not in text.lower():
        errors.append(f'hero requirement missing: {phrase}')

# Problem / contribution / architecture contract.
semantic_requirements = [
    'The problem', 'Why it is hard', 'Why simple methods fail',
    'Novelty', 'Three independent licenses',
    'Training / recovery loop:',
    'Designed', 'Implemented', 'Technical choice owned by Aura Yavary:',
    'Datasets / tasks', 'Baselines', 'Ablations', 'Setup',
]
for phrase in semantic_requirements:
    if phrase.lower() not in text.lower():
        errors.append(f'homepage content missing: {phrase}')

# Executive results table contract.
result_requirements = [
    'Success ↑', 'Recovery on naive failures ↑', 'Median latency ↓', 'External API cost',
    'Naive personalization', 'Fixed firewall', 'Provenance-only', 'Learned PLP', 'Hybrid PLP',
]
for phrase in result_requirements:
    if phrase.lower() not in text.lower():
        errors.append(f'results contract missing: {phrase}')

# Failure/demo/scaling/safety contract.
required_phrases = [
    'Case 0 · User belief becomes world evidence',
    'Case 6 · Personal state leaks into unrelated fact',
    'Evidence starvation',
    'Recorded passing trial', 'Recorded OOD failure', 'raw trajectories',
    'Model size', 'Task horizon', 'Tool count', 'Cost / latency', 'Robustness',
    'Irreversible external actions', 'Permission boundaries', 'Human escalation',
    'engineering report', 'Training / post-training details', 'eval methodology',
]
for phrase in required_phrases:
    if phrase.lower() not in text.lower():
        errors.append(f'homepage requirement missing: {phrase}')

# Evidence-layer contract below the polished research story.
for phrase in [
    'Inside the research process', 'View experiment journal', "What didn't work",
    'Decision log', 'Unexpected findings', 'Real eval tables', 'Reproduce results',
]:
    if phrase.lower() not in text.lower():
        errors.append(f'evidence-layer homepage requirement missing: {phrase}')

# Artifact contract. Public GitHub may be unpublished, but status + exact source must be explicit.
artifact_requirements = [
    'Paper', 'GitHub', 'Benchmark', 'Dataset', 'Demo', 'Video',
    'Technical report', 'Blog post', 'Source snapshot',
]
for phrase in artifact_requirements:
    if phrase.lower() not in text.lower():
        errors.append(f'artifact requirement missing: {phrase}')

# Citation contract requested by the project owner.
for phrase in ['Aura Yavary', '2026', '@software{yavary_personalized_not_persuaded']:
    if phrase.lower() not in text.lower():
        errors.append(f'citation requirement missing: {phrase}')
if 'year   = {2026}' not in text:
    errors.append('BibTeX year must be 2026')

# Essential local targets must exist.
local_targets = [
    'artifacts/personalized-not-persuaded-paper.pdf',
    'behavior_lab/methods/learned_plp.py',
    'site/demo.html',
    'datasets/provenance/provenancebench.csv',
    'media/personalized-not-persuaded-walkthrough.mp4',
    'results/trial_trajectories.jsonl',
    'docs/PLP_TECHNICAL_REPORT.md',
    'docs/BLOG_POST.md',
]
for rel in local_targets:
    if not (ROOT / rel).exists():
        errors.append(f'homepage target missing from release: {rel}')

# Mirror must contain the same 14-section contract, while allowing relative-link differences.
if not MIRROR.exists():
    errors.append('missing site/index.html mirror')
else:
    mirror = MIRROR.read_text(encoding='utf8', errors='ignore')
    for number, title in required_sections:
        if f'{number} · {title}' not in mirror:
            errors.append(f'site/index.html missing section: {number} · {title}')

if errors:
    print('HOMEPAGE CONTRACT AUDIT: FAIL')
    for e in errors:
        print('-', e)
    sys.exit(1)

print('HOMEPAGE CONTRACT AUDIT: PASS')
print('14/14 required sections present and ordered')
print('Hero CTAs, results schema, demo trajectory, scaling, safety, artifacts and citation verified')
