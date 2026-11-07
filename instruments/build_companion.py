"""Assemble the companion PDF: Part I the writeup (draft 6), Part II the long form (draft 5 with the training chapter replaced
and the duplicated T2b/§5 block removed), appendices A–H from the record. Render: markdown -> HTML -> Chrome headless PDF."""
import re, os, subprocess, sys, datetime, json
sys.path.insert(0, '/Users/vanya/work/arc/ops/.venv/lib/python3.12/site-packages')
import glob
for p in glob.glob('/Users/vanya/work/arc/ops/.venv/lib/python3*/site-packages'): sys.path.insert(0, p)
import markdown
R='/Users/vanya/work/arc/runs'; OUT=f'{R}/paper-companion'; os.makedirs(OUT, exist_ok=True)
import sys; sys.path.insert(0,f'{R}/lib'); from update_counts import NOT_RUN
rd=lambda p: open(p, encoding='utf-8').read()
d6=rd(f'{R}/PAPER-2026-10-25-DRAFT6.md').split('\n',2)[2]           # drop the title + italic header line
d5=rd(f'{R}/PAPER-2026-10-22-DRAFT5.md')
# the tag list printed in Appendix A: only the tags the writeup uses (a tag of a row the writeup no longer cites is not listed)
TAGS_USED='; '.join(k+' → '+v for k,v in json.load(open(f'{R}/ledger/tag-map.json')).items() if re.search(r'\[[^\]]*'+re.escape(k)+r'[^\]]*\]', d6))
lines=d5.split('\n')
def idx(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix): return i
    return None
# replace T4 + T5 + 4.4 (lines from '## T4.' up to '## T3b.') with the final chapter
a=idx('## T4.'); b=idx('## T3b.')
chapter=rd(f'{R}/lib/companion_training_chapter.md').split('\n')
lines=lines[:a]+chapter+['']+lines[b:]
# drop the duplicated second 'T2b' + '## 5. The boundary claim' block if present twice
firsts=[i for i,l in enumerate(lines) if l.startswith('## T2b.')]
if len(firsts)==2:
    end=idx('## 5. What the conditions say', firsts[1]) or firsts[1]
    lines=lines[:firsts[1]]+lines[end:]
# drop draft-5's own appendix stubs and figure list (replaced by real appendices below)
fa=idx('## Figures (to render)'); refs=idx('## References')
body5='\n'.join(lines[:fa]) if fa else '\n'.join(lines)
refs5='\n'.join(lines[refs:]) if refs else ''
figs=''.join(f'\n\n![{n}]({R}/paper-figures/v7-draft/{f})\n' for n,f in (('F1 Adoption channels','F1-adoption-channels.png'),('F2 The budget curve','F3-budget-curve.png'),('F3 The floor, measured: who can write a replay-exact simulator','F4-discriminator.png'),('F4 The design-law map (schematic)','F5-design-law-map.png')))
ts=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%MZ')
doc=f"""# What a Frozen Model Takes From Its Harness
## Companion document to the ARC Prize 2026 Paper Track entry (assembled {ts})
*Part I is the Kaggle writeup (≤ 1,500 words). Part II is the long form. Appendices A to H are the campaign record: every number in Parts I and II traces to a row, a section or a mirror listed there. Licence: MIT for code, CC BY 4.0 for documents, data and figures.*

# Part I. The writeup
{d6}
{figs}

# Part II. The long form
{rd(f'{R}/lib/companion_part2.md')}

# Part IIb. The notes channel as a pre-registered equivalence study
{rd(f'{R}/PAPER-2026-11-02-EQUIVALENCE.md')}

# Part III. The paper in the program's frame
{rd(f'{R}/PAPER-2026-10-28-POSITIONING-LAB.md').split(chr(10),2)[2]}

# Appendix A. The register ({len(json.load(open(f'{R}/ledger/bets.json'))['bets'])} rows, bar filed before every read)
*A row counts as read when a run produced its number (a miss, null, void, pass, conversion, or a measured value); rows parked, held, filed, running, or closed without a run do not: {', '.join(sorted(NOT_RUN))}. Counted by runs/lib/update_counts.py.*
*Short tags used in the writeup map to register ids as follows: {TAGS_USED}.*

{rd(f'{R}/../../docs/arc/register/bets.md') if os.path.exists(f'{R}/../../docs/arc/register/bets.md') else rd('/Users/vanya/work/docs/arc/register/bets.md')}

# Appendix B. Pre-registration log
*The bar and read texts below are verbatim register rows; internal names in them (e.g. "the Studio") refer to the Lab's conversational program.*

{rd(f'{R}/PAPER-2026-10-27-PREREG-LOG.md')}

# Appendix C. Audit of the drafts against the record, with corrections
*A dated record (2026-10-25/27). Register counts and numbers inside it are as of its date; the register at submission is Appendix A.*

{rd(f'{R}/PAPER-2026-10-25-AUDIT.md')}

# Appendix D. Research-grade review: claim grades and intervals
*A dated record (2026-10-27); the grades current at submission are in Part III and the direction note. Register counts inside are as of its date.*

{rd(f'{R}/PAPER-2026-10-27-RESEARCH-GRADE.md')}

# Appendix E. The public board read as best-of-N, and the private-board forecast filed before the reveal
{rd(f'{R}/ledger/board-forecast-2026-10-28.md')}

# Appendix F. Mirrors index (96 mirror folders; 90 with played sessions, the rest superseded attempts kept for the record)
{rd(f'{R}/field/pod-mirror/MIRRORS.md')}

# Appendix G. Data availability
- Register: runs/ledger/bets.json ({len(json.load(open(f'{R}/ledger/bets.json'))['bets'])} rows) and the pre-registration log (Appendix B, with the bar text per row). The operator journal is internal; every claim's bar and read are in the log.
- Harness patch (v39 base + v41 allocation + v42 provenance), instruments (runs/lib: rhae_pair_read.py, pair_cap_read.py, thinking_signature.py, failure_read.py, wm_replay_probe.py, paper_figures_v7.py), probe outputs (runs/field/ours/probe/*.jsonl, 23-cell transition set included) and the per-game benchmark.json of every pair and read are released with the flown notebook franzen-b1b (code MIT, data CC BY 4.0). Full request traces (≈ 100 GB) on request.
- The notes corpus: about twenty thousand self-written notes (11,875 cleared-level notes by the open model over 256 game-levels, 407 by GPT-6.1 Sol, the rest stuck-level notes and other families), each with its game, level, kind and the run it came from (runs/field/pod-mirror/*/cross_game_cards.jsonl and runs/field/local-reads/*/cross_game_cards.jsonl), released with the register under the same licence as the data (CC BY 4.0); the writer-consistency read (Part IIb §2b) is computed from it and is reproducible from the files.
- Kaggle: the hidden draws, their submission IDs and classes are listed in Appendix H.
- Compute and its prices. The campaign ran on rented GPUs (RunPod, one RTX PRO 6000 per pod; the pods ledger runs/ledger/pods.csv lists each pod with its hours and cost through 10-17) and metered API calls (OpenRouter) plus Kaggle's free GPU quota; the two providers' invoice totals are available on request. What a unit of evidence costs here is measured: a 25-game one-pass pair ≈ $25 and resolves 5 to 7 RHAE; four passes ≈ $60 and resolve 2.3 (measured 10-29); resolution scales as 1/√passes; the format question was declined at seven pairs (≈ $170) for a 95% exclusion; a screen places a new model above or below the floor for ≈ $10 and an hour. The contemplated training climb was costed at $1,300 to $8,000 (PLAN-2026-10-20) and not flown by the campaign's own rule (row 51, 'unread by decision, not by budget').

# Appendix H. The hidden draws
{rd('/Users/vanya/work/docs/arc/submission/draws.md')}

{refs5}
"""
md=markdown.markdown(doc, extensions=['tables','fenced_code','toc'])
css="""body{font-family:-apple-system,Helvetica,Arial,sans-serif;font-size:10.5pt;line-height:1.35;max-width:7.2in;margin:0.6in auto;color:#111}
h1{font-size:18pt;margin-top:1.4em;page-break-before:always}h1:first-of-type{page-break-before:auto}h2{font-size:13.5pt;margin-top:1.2em}h3{font-size:11.5pt}
table{border-collapse:collapse;font-size:7.6pt;width:100%;margin:0.6em 0}th,td{border:1px solid #bbb;padding:2px 4px;vertical-align:top;word-break:break-word}
img{max-width:100%;height:auto;margin:0.4em 0}code{font-size:9pt}p{margin:0.45em 0}li{margin:0.15em 0}"""
html=f"<!doctype html><html><head><meta charset='utf-8'><title>Companion</title><style>{css}</style></head><body>{md}</body></html>"
open(f'{OUT}/companion.html','w',encoding='utf-8').write(html); open(f'{OUT}/companion.md','w',encoding='utf-8').write(doc)
subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--disable-gpu','--no-sandbox','--no-pdf-header-footer',f'--print-to-pdf={OUT}/companion.pdf',f'file://{OUT}/companion.html'],capture_output=True,timeout=300)
print('written', OUT, os.path.getsize(f'{OUT}/companion.pdf')//1024, 'KB', 'words', len(re.findall(r'\S+', doc)))
