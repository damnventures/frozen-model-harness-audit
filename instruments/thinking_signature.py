#!/usr/bin/env python3
"""The thinking-length signature (§286/§288): per assistant turn, chars of reasoning_content in a run's request logs.
A form whose thinking has collapsed reads a median of a few hundred chars (most turns under 300) against the stock
player's 1,660–1,766. BAR (pre-registered §287 D): median >= 1000 chars AND turns under 300 chars <= 25% = PASS.
Reads partial runs (the first ~50 turns suffice), so it gates in minutes. usage: thinking_signature.py RUN_DIR [...]"""
import glob, json, os, statistics as st, sys

def read(d):
    lens = []
    for f in sorted(glob.glob(os.path.join(d, '*requests.jsonl'))):
        last = 0
        for l in open(f, errors='ignore'):
            try: r = json.loads(l)
            except Exception: continue
            a = [m for m in (r.get('messages') or []) if m.get('role') == 'assistant']
            if len(a) > last:
                for m in a[last:]: lens.append(len(m.get('reasoning_content') or m.get('reasoning') or ''))
                last = len(a)
    return lens

def main(dirs):
    for d in dirs:
        L = sorted(read(d))
        if not L: print(f"{d}: no assistant turns yet"); continue
        med = L[len(L)//2]; short = sum(1 for x in L if x < 300) / len(L)
        verdict = 'PASS' if (med >= 1000 and short <= 0.25) else 'MISS'
        print(f"SIGNATURE {os.path.basename(d.rstrip('/'))}: turns {len(L)} | thinking chars p25 {L[len(L)//4]} median {med} p75 {L[3*len(L)//4]} | under 300: {100*short:.0f}% | bar median>=1000 & short<=25% -> {verdict}")

if __name__ == '__main__': main(sys.argv[1:])
