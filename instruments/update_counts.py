"""Rewrite every register count in the paper texts from bets.json: N rows, M with a verdict. Run at the freeze."""
import json,re
R='/Users/vanya/work/arc'; rows=json.load(open(f'{R}/runs/ledger/bets.json'))['bets']; N=len(rows)
# A row is READ when a run produced its number (a MISS, NULL, VOID, PASS, CONVERTS, or a measured value). Rows parked,
# held, registered, filed, running, or closed without a run are not. The list is explicit so the count is reproducible;
# Appendix A marks these rows.
NOT_RUN={
    'terra-play-screen',
    'pod-samegame-own-notes',
    'sol-tn36-coverage-vs-verdict','power','B1f-card-v2','B1g-assistant-channel','B3-deep-drain','B7-temperature','S5-slot-priority-dprime','L2-goal-ledger-switch',
 'T-lane','S6-reap','S7a-fp8-ple-numerics','S7b-streams-at-context','training-mechanism-packing','Sol-economy',
 'board-forecast-private','spec-steps-cell','submission-hour','mercury3-bo30-curve','cards-fourth-read-conditional',}
def verdict(r): return r['id'] not in NOT_RUN
def main():
    M=sum(1 for r in rows if verdict(r))
    edits=[(f'{R}/runs/PAPER-2026-10-25-DRAFT6.md',[(r'\b1\d\d (?:bets|registered experiments), 1\d\d read\b',f'{N} registered experiments, {M} read'),(r'Register \(1\d\d rows\)',f'Register ({N} rows)')]),
           (f'{R}/runs/PAPER-2026-10-28-POSITIONING-LAB.md',[(r'Appendix A; 1\d\d rows on 10-28',f'Appendix A; {N} rows')]),
           (f'{R}/runs/PAPER-2026-10-28-DIRECTION-FINAL.md',[(r'Appendix A; 1\d\d rows on 10-28',f'Appendix A; {N} rows')]),
           ('/Users/vanya/work/docs/arc/README.md',[(r'1\d\d registered bets, 1?\d\d closed with a number',f'{N} registered bets, {M} with a verdict'),(r'register rendered \(1\d\d rows',f'register rendered ({N} rows')]),
           ('/Users/vanya/work/docs/arc/TRANSPORT.md',[(r'register \(1\d\d rows\)',f'register ({N} rows)'),(r'\b131 pre-registered experiments',f'{N} pre-registered experiments')]),
           ('/Users/vanya/work/docs/field/direction-of-work.md',[(r'Appendix A; 1\d\d rows on 2026-10-28',f'Appendix A; {N} rows')]),
           ('/Users/vanya/work/docs/seed/research-thesis.md',[(r'Appendix A; 1\d\d rows on 2026-10-28',f'Appendix A; {N} rows')]),
           ('/Users/vanya/work/docs/seed/world-view-and-bets.md',[(r'Appendix A; 1\d\d rows on 2026-10-28',f'Appendix A; {N} rows')])]
    for p,subs in edits:
        try: s=open(p).read()
        except FileNotFoundError: continue
        t=s
        for a,b in subs: t=re.sub(a,b,t)
        if t!=s: open(p,'w').write(t); print('counts updated in',p.split('/')[-1])
    print(f'register {N} rows, {M} with a verdict')
if __name__=='__main__': main()
