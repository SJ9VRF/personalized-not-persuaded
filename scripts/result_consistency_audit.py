from pathlib import Path
import csv, re, sys

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / 'results' / 'provenancebench_method_summary.csv'

METHODS = ['naive','firewall','provenance_only','learned_plp','hybrid_plp','oracle']
DISPLAY = {
    'naive': {'README.md':'Naive','RESULTS_CARD.md':'Naive personalization','paper/PAPER_DRAFT.md':'Naive personalization'},
    'firewall': {'README.md':'Firewall','RESULTS_CARD.md':'Fixed firewall','paper/PAPER_DRAFT.md':'Fixed firewall'},
    'provenance_only': {'README.md':'Provenance-only','RESULTS_CARD.md':'Provenance-only','paper/PAPER_DRAFT.md':'Provenance-only'},
    'learned_plp': {'README.md':'Learned PLP','RESULTS_CARD.md':'Learned PLP','paper/PAPER_DRAFT.md':'Learned PLP'},
    'hybrid_plp': {'README.md':'Hybrid PLP','RESULTS_CARD.md':'Hybrid PLP','paper/PAPER_DRAFT.md':'Hybrid PLP'},
    'oracle': {'README.md':'Oracle','RESULTS_CARD.md':'Oracle','paper/PAPER_DRAFT.md':'Oracle'},
}
TEX_DISPLAY = {
    'naive':'Naive personalization','firewall':'Fixed firewall','provenance_only':'Provenance-only',
    'learned_plp':'Learned PLP','hybrid_plp':'Hybrid PLP','oracle':'Oracle'
}

with SUMMARY.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
by = {(r['method'], r['split']): r for r in rows}

def r3(x): return f'{float(x):.3f}'
def expected(method):
    idr=by[(method,'test')]; ood=by[(method,'ood_test')]; comp=by[(method,'compositional_test')]
    return [r3(idr['exact_license_match']), r3(ood['exact_license_match']),
            r3(comp['exact_license_match']), r3(ood['evidence_uptake']),
            r3(ood['unsupported_leakage'])]

def strip_md(s): return s.replace('**','').strip()

def markdown_row(text,label):
    clean=text.replace('**','')
    pat=re.compile(r'^\|\s*'+re.escape(label)+r'\s*\|([^\n]+)$', re.M)
    m=pat.search(clean)
    if not m: return None
    return [v.strip() for v in m.group(1).split('|') if v.strip()][:5]

def strip_tex(s):
    s=re.sub(r'\\textbf\{([^}]*)\}', r'\1', s)
    return s.strip()

def latex_row(tex,label):
    # Remove bold wrapper around method labels before matching.
    clean=re.sub(r'\\textbf\{([^}]*)\}', r'\1', tex)
    m=re.search(r'^'+re.escape(label)+r'\s*&\s*(.*?)\\\\', clean, flags=re.M)
    if not m: return None
    vals=[]
    for raw in m.group(1).split('&')[:5]:
        v=raw.strip()
        if v.startswith('.'): v='0'+v
        vals.append(f'{float(v):.3f}')
    return vals

errors=[]
for rel in ['README.md','RESULTS_CARD.md','paper/PAPER_DRAFT.md']:
    text=(ROOT/rel).read_text(encoding='utf-8')
    for method in METHODS:
        label=DISPLAY[method][rel]
        got=markdown_row(text,label); exp=expected(method)
        if got is None: errors.append(f'{rel}: missing results row for {label}')
        elif got != exp: errors.append(f'{rel}: {label} row {got} != source-of-truth {exp}')

tex=(ROOT/'paper/main.tex').read_text(encoding='utf-8')
for method in METHODS:
    got=latex_row(tex,TEX_DISPLAY[method]); exp=expected(method)
    if got is None: errors.append(f'paper/main.tex: missing results row for {TEX_DISPLAY[method]}')
    elif got != exp: errors.append(f'paper/main.tex: {TEX_DISPLAY[method]} row {got} != source-of-truth {exp}')

if not (ROOT/'reports'/'PROVENANCEBENCH_EXECUTABLE.md').exists():
    errors.append('missing canonical reports/PROVENANCEBENCH_EXECUTABLE.md')
for stale in ['PROVENANCEBENCH_LEARNED_PLP.md','PROVENANCEBENCH_STATISTICS.md']:
    if (ROOT/'reports'/stale).exists():
        errors.append(f'superseded report still in active reports/: {stale}')


# Homepage executive table must agree with canonical OOD results and the measured runtime summary.
import json
home=(ROOT/'index.html').read_text(encoding='utf-8')
runtime=json.loads((ROOT/'results/homepage_runtime_summary.json').read_text())
exec_labels={
    'naive':'Naive personalization','firewall':'Fixed firewall','provenance_only':'Provenance-only',
    'learned_plp':'Learned PLP','hybrid_plp':'Hybrid PLP'
}
for method,label in exec_labels.items():
    ood=by[(method,'ood_test')]
    success=f"{100*float(ood['exact_license_match']):.1f}%"
    recovery=f"{100*float(runtime['methods'][method]['recovery_on_naive_failures']):.1f}%"
    latency=f"{float(runtime['methods'][method]['median_us_per_item']):.1f} µs/item" if float(runtime['methods'][method]['median_us_per_item']) >= 10 else f"{float(runtime['methods'][method]['median_us_per_item']):.2f} µs/item"
    # Match the executive row by its displayed label.
    clean=home.replace('<strong>','').replace('</strong>','')
    m=re.search(r'<tr><td>'+re.escape(label)+r'</td><td[^>]*>([^<]+)</td><td[^>]*>([^<]+)</td><td>([^<]+)</td><td>\$0</td></tr>', clean)
    if not m:
        errors.append(f'index.html: missing executive results row for {label}')
    else:
        got=[x.strip() for x in m.groups()]
        exp=[success,recovery,latency]
        if got != exp:
            errors.append(f'index.html: {label} executive row {got} != source-of-truth {exp}')

if errors:
    print('RESULT CONSISTENCY AUDIT: FAIL')
    for e in errors: print('-',e)
    sys.exit(1)
print('RESULT CONSISTENCY AUDIT: PASS')
