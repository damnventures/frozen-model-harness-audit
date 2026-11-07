"""Regenerate the pre-registration appendix from the register: for every row, the bar/read text, the book sections it cites,
and the stamps of the first (filed) and last (read) cited sections, taken from the book's section headers."""
import json, re, os
R='/Users/vanya/work/arc/runs'
book=open(f'{R}/RUNNER-INSTRUCTIONS-2026-09-24.md',encoding='utf-8').read()
stamps={}
for m in re.finditer(r'^#{2,4} §(\d+[a-z]?)[^\n]*?\((\d{4}-\d{2}-\d{2}(?: \d{2}:\d{2}Z)?)', book, re.M):
    stamps.setdefault(m.group(1), m.group(2))
b=json.load(open(f'{R}/ledger/bets.json')); rows=b['bets'] if 'bets' in b else [v for v in b.values() if isinstance(v,list)][0]
def secs(r):
    txt=' '.join(str(r.get(k,'')) for k in ('where','status','read','number'))
    found=re.findall(r'§(\d+[a-z]?)', txt)
    out=[]; [out.append(x) for x in found if x not in out]
    return out
def key(s):
    m=re.match(r'(\d+)([a-z]?)', s); return (int(m.group(1)), m.group(2))
lines=["# Appendix: pre-registration log (register row → the book sections that filed and read it, with the sections' own stamps)","",
       f"Regenerated from runs/ledger/bets.json ({len(rows)} rows) by runs/lib/prereg_log.py. 'filed' is the stamp of the earliest cited section, 'read' of the latest; rows citing one section were filed and read in it; rows citing none were registered before the book's section stamps began (September) and carry the register's own status text.","",
       "| # | row | status | bar / read (as registered) | sections | filed | read |","|---|---|---|---|---|---|---|"]
def c(x): return str(x).replace('|','\\|').replace('\n',' ')
for i,r in enumerate(rows,1):
    ss=sorted(secs(r), key=key); f=stamps.get(ss[0],'') if ss else ''; rd=stamps.get(ss[-1],'') if ss else ''
    lines.append(f"| {i} | `{c(r['id'])}` | {c(r.get('status',''))[:60]} | {c(r.get('number',''))[:160]} | {' '.join('§'+x for x in ss)} | {f} | {rd} |")
open(f'{R}/PAPER-2026-10-27-PREREG-LOG.md','w',encoding='utf-8').write('\n'.join(lines)+'\n')
print('prereg log:', len(rows), 'rows;', sum(1 for r in rows if secs(r)), 'with sections;', len(stamps), 'section stamps')
