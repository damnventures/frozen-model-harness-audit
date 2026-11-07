#!/usr/bin/env python
"""wm_replay_probe — can THIS model reach an exact-replay world model from recorded transitions? (§224.F, the Memento-3 loop
in miniature, offline, on our own recorded play.)

  python runs/lib/wm_replay_probe.py --transitions T.jsonl --arm flash|sol|opus --out OUT.jsonl [--cells "sp80:2,wa30:2,..."]
                                     [--k 20] [--m 20] [--iters 4] [--workers 3] [--dry]
  python runs/lib/wm_replay_probe.py --fixture            # synthetic deterministic game + a mock model: must print 100% held-out

Per cell (game, level): the first K transitions of one session at that level are shown IN FULL (board before, action, board
after, 64 ASCII lines each, the harness's colour letters); the model writes world_model.md (rules in language) and a Python
predict(board_lines, action) -> board_lines. The probe replays the K transitions cell-exactly; on the first mismatch it feeds
back the counterexample (transition index, action, the mismatched cells: predicted vs actual, first 40) and asks for a
revision (rulebook first, then code), up to --iters rounds. Score = exact-frame rate and cell accuracy on the next M
held-out transitions of the same session and level, against two baselines: nothing-changes and last-diff (re-apply the
previous transition's cell changes when the action repeats, else nothing). The model's code runs in a subprocess (python -I,
10 s per prediction batch, no network). Keys from .secrets, never printed. Printed lines (pre-registered §224.F):
  CELL game:Lk  arm  iters_used  train_exact K'/K  heldout_exact x/M  heldout_cell_acc  baseline_nothing x/M  baseline_lastdiff x/M
  SUMMARY arm: cells N | cells where heldout_exact - nothing >= +20 points: n | median heldout_exact | median nothing
  BAR §224.F.1 (Flash-Next: >= 12 of 24 cells beat nothing-changes by >= 20 points): PASS/MISS
"""
import threading
_TL = threading.local()   # §347b: per-thread wall-clock accumulators (one cell per worker thread)
import argparse, json, os, random, re, subprocess, sys, tempfile, time, urllib.request, concurrent.futures as cf

ARC = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEGEND = ("Color legend: W=white, w=light gray, g=gray, G=dark gray, c=charcoal, B=black, M=magenta, P=pink, R=red, b=blue, "
          "S=sky blue, Y=yellow, O=orange, r=dark red, N=light green, p=purple.")
DEFAULT_CELLS = ("sp80:2,wa30:2,bp35:2,tn36:2,sk48:2,lf52:3,g50t:3,su15:4,ls20:5,cn04:5,dc22:5,ka59:6,sc25:6,re86:7,s5i5:7,tu93:9,"
                 "ft09:1,ft09:2,lp85:1,lp85:2,ar25:1,ar25:2,cd82:1,cd82:2")

SYSTEM = ("You are building an exact world model of a 64x64 grid game from recorded transitions. " + LEGEND + "\n"
          "Boards are given as 64 lines of 64 colour letters. Actions are named (UP, DOWN, LEFT, RIGHT, SPACE, UNDO, or MOUSE(r,c)).\n"
          "Deliver TWO things, in this order: (1) world_model.md: numbered rules in plain language describing objects, what each action does, "
          "the dynamics, and what you believe the goal is; (2) a Python code block defining predict(board_lines, action) -> board_lines that "
          "returns the COMPLETE next board (64 strings of 64 chars). The code must be pure Python 3 standard library, deterministic, and "
          "fast (under 1 s per call). It will be replayed cell-exactly against every recorded transition; a model that predicts 'no change' "
          "where cells changed fails. Prefer the simplest rules that reproduce every transition shown.")

TOOL_NOTE = ("\nYou can run Python to EXPLORE before delivering: write a fenced ```python block that does NOT define predict (plain text, no "
             "function-call syntax: there is no function-calling interface here, only fenced code blocks). It is executed with a variable "
             "`transitions` = list of {board_before: [64 strings], action: str, board_after: [64 strings]} in order, and whatever it prints "
             "(up to 4,000 characters) is returned to you in the next message. Use it to diff boards, locate objects, test hypotheses. "
             "Up to 6 exploration blocks per round; then deliver world_model.md and the predict code block.")

def board_lines(s):
    return s.split("\n") if isinstance(s, str) else list(s)

def diff_cells(a, b, cap=40):
    out = []
    for r in range(min(len(a), len(b))):
        if a[r] == b[r]:
            continue
        for c in range(min(len(a[r]), len(b[r]))):
            if a[r][c] != b[r][c]:
                out.append((r, c, a[r][c], b[r][c]))
                if len(out) >= cap:
                    return out, True
    return out, False

def render_transition(i, t):
    return (f"### transition {i}\naction: {t['action_display'] or t['action_name']}\nboard before:\n" + "\n".join(board_lines(t['board_before'])) +
            "\nboard after:\n" + "\n".join(board_lines(t['board_after'])) + "\n")

def render_compact(trans):
    """The harness's own shape: the first board in full, then per transition the action and the changed cells (row,col,before->after)."""
    out = ["board at the start (64 lines):"] + board_lines(trans[0]['board_before']) + [""]
    for i, t in enumerate(trans):
        dc, more = diff_cells(board_lines(t['board_before']), board_lines(t['board_after']), cap=400)
        cells = "; ".join(f"({r},{c},{a}->{b})" for r, c, a, b in dc) + (" ... (more cells changed)" if more else "")
        out.append(f"### transition {i}: action {t['action_display'] or t['action_name']} -> {len(dc)}{'+' if more else ''} cells changed" + (f": {cells}" if dc else " (no change)"))
    return "\n".join(out)


def components(board, cells):
    """Connected components (4-neighbour, same colour) covering the given cell set."""
    cells = set(cells); seen = set(); comps = []
    for start in sorted(cells):
        if start in seen:
            continue
        col = board[start[0]][start[1]]; stack = [start]; comp = []
        seen.add(start)
        while stack:
            r, c = stack.pop(); comp.append((r, c))
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (r + dr, c + dc)
                if n in cells and n not in seen and board[n[0]][n[1]] == col:
                    seen.add(n); stack.append(n)
        comps.append((col, frozenset(comp)))
    return comps

def describe(comp):
    col, cells = comp
    rs = [r for r, _ in cells]; cs = [c for _, c in cells]
    return f"{col} x{len(cells)} rows {min(rs)}-{max(rs)} cols {min(cs)}-{max(cs)}"

def board_inventory(board, cap=40):
    """§237 objects-only input: the start board as an object list (colour, size, bounding box), background excluded —
    no raw grid, so the model cannot re-derive by hand and must work from the harness's structure."""
    bg = max(set("".join(board)), key="".join(board).count)
    cells = [(r, c) for r in range(64) for c in range(64) if board[r][c] != bg]
    objs = sorted(components(board, cells), key=lambda o: -len(o[1]))
    lines = [f"board 64x64, background {bg}; {len(objs)} objects (largest first):"]
    for o in objs[:cap]:
        lines.append("  " + describe(o))
    if len(objs) > cap:
        lines.append(f"  ... (+{len(objs) - cap} smaller objects)")
    return "\n".join(lines)

def render_objects(trans, cap=12, raw_board=True):
    """§234 I9: the HARNESS does the bookkeeping. Per transition: connected objects that MOVED (same colour, same shape,
    translated), APPEARED, VANISHED, or RECOLOURED, computed from the changed cells — the start board in full as before."""
    out = (["board at the start (64 lines):"] + board_lines(trans[0]['board_before']) + [""]) if raw_board else \
          ["board at the start, as objects:", board_inventory(board_lines(trans[0]['board_before'])), ""]
    for i, t in enumerate(trans):
        a = board_lines(t['board_before']); b = board_lines(t['board_after'])
        changed = [(r, c) for r in range(64) for c in range(64) if a[r][c] != b[r][c]]
        act = t['action_display'] or t['action_name']
        if not changed:
            out.append(f"### transition {i}: action {act} -> no change"); continue
        # cells that lost a colour (before-side objects) and gained one (after-side objects), by colour
        # the board's background colour (its most frequent) is not an object: its changes are the shadow of the objects' moves
        bg = max(set("".join(a)), key="".join(a).count)
        before_objs = [o for o in components(a, changed) if o[0] != bg]   # what was there, grouped by its old colour
        after_objs = [o for o in components(b, changed) if o[0] != bg]    # what is there now, grouped by its new colour
        def bbox(cells):
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]; return (min(rs), min(cs), max(rs) - min(rs), max(cs) - min(cs))
        events = []; used_after = set()
        for col, cells in before_objs:
            # a move: an after-object of the same colour, same shape translated (exact), else same bounding-box size within 15% cells (approx)
            shape = {(r - min(r for r, _ in cells), c - min(c for _, c in cells)) for r, c in cells}
            match = None; approx = False
            for j, (col2, cells2) in enumerate(after_objs):
                if j in used_after or col2 != col:
                    continue
                if len(cells2) == len(cells) and {(r - min(r for r, _ in cells2), c - min(c for _, c in cells2)) for r, c in cells2} == shape:
                    match = j; approx = False; break
            if match is None:
                for j, (col2, cells2) in enumerate(after_objs):
                    if j in used_after or col2 != col:
                        continue
                    b1, b2 = bbox(cells), bbox(cells2)
                    if b1[2:] == b2[2:] and abs(len(cells2) - len(cells)) <= 0.15 * len(cells):
                        match = j; approx = True; break
            if match is not None:
                used_after.add(match); c2 = after_objs[match][1]
                dr = bbox(c2)[0] - bbox(cells)[0]; dc = bbox(c2)[1] - bbox(cells)[1]
                events.append(f"{'MOVED~' if approx else 'MOVED'} {describe((col, cells))} by ({dr:+d},{dc:+d})")
            else:
                events.append(f"GONE {describe((col, cells))}")
        for j, (col2, cells2) in enumerate(after_objs):
            if j not in used_after:
                events.append(f"NEW {describe((col2, cells2))}")
        more = len(events) - cap
        out.append(f"### transition {i}: action {act} -> {len(changed)} cells changed; objects: " + "; ".join(events[:cap]) + (f" ... (+{more} more)" if more > 0 else ""))
    return "\n".join(out)

def code_blocks(text):
    """Every code block the model wrote: fenced ```python blocks, plus the bodies of Qwen-style <function=python>…</function>
    tool calls (§234 I8: Flash-Next emits its native function-call tokens when told it can run Python, even with no tools
    declared; the body is raw code or a JSON object with a "code" key)."""
    blocks = re.findall(r"```(?:python)?\n(.*?)```", text or "", re.S)
    for body in re.findall(r"<function=\w+>(.*?)</function>", text or "", re.S):
        body = body.strip()
        if body.startswith("{"):
            try:
                body = json.loads(body).get("code", "")
            except Exception:
                body = re.sub(r'^\{\s*"code"\s*:\s*"', "", body)
        if body:
            blocks.append(body)
    return blocks

def extract_code(text):
    for block in reversed(code_blocks(text)):
        if "def predict" in block:
            return block
    return None

RUNNER = r'''
import sys, json
src = open(sys.argv[1]).read()
ns = {}
exec(compile(src, "wm_model", "exec"), ns)
pred = ns.get("predict")
data = json.load(open(sys.argv[2]))
out = []
for board, action in data:
    try:
        nb = pred(list(board), action)
        nb = [str(x) for x in nb]
        out.append(nb)
    except Exception as e:
        out.append({"error": repr(e)[:200]})
json.dump(out, open(sys.argv[3], "w"))
'''


EXPLORE_RUNNER = r"""
import sys, json, io, contextlib
transitions = json.load(open(sys.argv[2]))
src = open(sys.argv[1]).read()
buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        exec(compile(src, "explore", "exec"), {"transitions": transitions, "__name__": "__main__"})
except Exception as e:
    buf.write("\nEXPLORE ERROR: " + repr(e)[:300])
open(sys.argv[3], "w").write(buf.getvalue()[:4000])
"""

def run_explore(code, trans, timeout=30):
    """§234 I8: the tool-augmented arm — the model's exploration snippet runs over the transitions (board_before/action/board_after
    as 64-line lists) in the same sandbox as predict; stdout (≤ 4,000 chars) goes back as the next user turn."""
    d = tempfile.mkdtemp(prefix="wmexplore-")
    src = os.path.join(d, "explore.py"); inp = os.path.join(d, "trans.json"); outp = os.path.join(d, "out.txt"); rp = os.path.join(d, "run.py")
    open(src, "w").write(code); open(rp, "w").write(EXPLORE_RUNNER)
    json.dump([{"board_before": board_lines(t["board_before"]), "action": (t["action_display"] or t["action_name"]), "board_after": board_lines(t["board_after"])} for t in trans], open(inp, "w"))
    try:
        subprocess.run([sys.executable, "-I", rp, src, inp, outp], timeout=timeout, capture_output=True, cwd=d)
        return open(outp).read()
    except Exception as e:
        return "EXPLORE ERROR: " + repr(e)[:200]

def run_model_code(code, pairs, timeout=60):
    d = tempfile.mkdtemp(prefix="wmprobe-")
    src = os.path.join(d, "model.py"); inp = os.path.join(d, "in.json"); outp = os.path.join(d, "out.json"); rp = os.path.join(d, "run.py")
    open(src, "w").write(code); json.dump(pairs, open(inp, "w")); open(rp, "w").write(RUNNER)
    try:
        subprocess.run([sys.executable, "-I", rp, src, inp, outp], timeout=timeout, capture_output=True, cwd=d)
        return json.load(open(outp))
    except Exception as e:
        return [{"error": f"runner: {repr(e)[:160]}"}] * len(pairs)

def score(preds, trans):
    exact = 0; cells_ok = 0; cells_all = 0; first_mismatch = None
    for i, (p, t) in enumerate(zip(preds, trans)):
        actual = board_lines(t["board_after"])
        if isinstance(p, dict) or len(p) != 64:
            if first_mismatch is None:
                first_mismatch = (i, "model error or wrong shape: " + (p.get("error", "") if isinstance(p, dict) else f"{len(p)} lines"))
            cells_all += 64 * 64; continue
        ok = all(p[r] == actual[r] for r in range(64))
        exact += ok
        for r in range(64):
            for c in range(64):
                cells_all += 1; cells_ok += (r < len(p) and c < len(p[r]) and p[r][c] == actual[r][c])
        if not ok and first_mismatch is None:
            dc, more = diff_cells(p, actual)
            first_mismatch = (i, "action " + str(t["action_display"] or t["action_name"]) + "; mismatched cells (row,col,predicted,actual): " +
                              "; ".join(f"({r},{c},{a}->{b})" for r, c, a, b in dc) + (" ..." if more else ""))
    return exact, cells_ok / max(1, cells_all), first_mismatch

def baseline_nothing(trans):
    return sum(board_lines(t["board_before"]) == board_lines(t["board_after"]) for t in trans)

def baseline_lastdiff(trans):
    exact = 0; prev = None
    for t in trans:
        b = board_lines(t["board_before"]); a = board_lines(t["board_after"]); pred = list(b)
        if prev is not None and prev[0] == (t["action_display"] or t["action_name"]):
            pb, pa = prev[1], prev[2]
            pred = [list(row) for row in b]
            for r in range(64):
                for c in range(64):
                    if pb[r][c] != pa[r][c]:
                        pred[r][c] = pa[r][c]
            pred = ["".join(row) for row in pred]
        exact += pred == a
        prev = ((t["action_display"] or t["action_name"]), b, a)
    return exact

REASONING_BUDGET = 0   # §237: > 0 sets OpenRouter reasoning.max_tokens on the thinking arms (0 = provider default)
LAST_REASONING_TOKENS = 0

def call_model(arm, messages, keys, max_tokens=8000):
    if arm == "flash":
        body = {"model": "qwen/qwen3.8-flash", "messages": messages, "max_tokens": max_tokens, "temperature": 0.7, "top_p": 0.95}
        url = "https://openrouter.ai/api/v1/chat/completions"; key = keys["openrouter"]; hdr = {"X-Title": "ARC3 wm replay probe"}
    elif arm == "flash-nothink":
        # the model with its reasoning disabled: it then writes the deliverable (the thinking arm spends the whole cap reasoning)
        body = {"model": "qwen/qwen3.8-flash", "messages": messages, "max_tokens": max_tokens, "temperature": 0.7, "top_p": 0.95, "reasoning": {"enabled": False}}
        url = "https://openrouter.ai/api/v1/chat/completions"; key = keys["openrouter"]; hdr = {"X-Title": "ARC3 wm replay probe"}
    elif arm == "sol":
        # the capability reference when Opus 5 is unreachable: GPT-6.1 Sol (52.7 standard-harness on the verified semi-private board), reasoning high
        body = {"model": "openai/gpt-6.1-sol", "messages": messages, "max_tokens": max_tokens, "temperature": 0.7, "reasoning": {"effort": "high"}}
        url = "https://openrouter.ai/api/v1/chat/completions"; key = keys["openrouter"]; hdr = {"X-Title": "ARC3 wm replay probe"}
    elif arm.startswith("local:"):
        # the $0 read (§306): a model WE serve (sglang/vLLM OpenAI-compatible), arm = local:<base_url>; model id from LOCAL_MODEL (default 'served')
        body = {"model": os.environ.get("LOCAL_MODEL", "served"), "messages": messages, "max_tokens": max_tokens, "temperature": 0.7, "top_p": 0.95,
                "chat_template_kwargs": {"enable_thinking": os.environ.get("LOCAL_THINKING", "1") != "0"}}   # §329: LOCAL_THINKING=0 = the no-thinking regime
        url = arm[6:].rstrip("/") + "/chat/completions"; key = os.environ.get("LOCAL_KEY", "none"); hdr = {"X-Title": "ARC3 wm replay probe"}
    elif arm.startswith("or:"):
        # §234: any OpenRouter model id as an arm (the capability curve between Flash-Next and Sol); provider defaults for reasoning
        body = {"model": arm[3:], "messages": messages, "max_tokens": max_tokens, "temperature": 0.7, "top_p": 0.95}
        if os.environ.get("OR_REASONING_EFFORT"):   # §338: or: arms only — OpenRouter reasoning.effort (low/medium/high) or "none" to disable
            eff = os.environ["OR_REASONING_EFFORT"].strip().lower()
            body["reasoning"] = {"enabled": False} if eff == "none" else {"effort": eff}
        url = "https://openrouter.ai/api/v1/chat/completions"; key = keys["openrouter"]; hdr = {"X-Title": "ARC3 wm replay probe"}
    else:
        body = {"model": "claude-opus-5", "messages": messages, "max_tokens": max_tokens, "temperature": 0.7}
        url = "https://api.inference.net/v1/chat/completions"; key = keys["inference"]; hdr = {"User-Agent": "curl/8.4.0"}
    if REASONING_BUDGET > 0 and "reasoning" not in body:
        body["reasoning"] = {"max_tokens": REASONING_BUDGET}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", **hdr})
    for attempt in range(6):
        try:
            _t0 = time.perf_counter()
            with urllib.request.urlopen(req, timeout=900) as r:
                d = json.load(r)
            _TL.calls = getattr(_TL, "calls", []) + [round(time.perf_counter() - _t0, 2)]   # §347b: API seconds per call
            ch = d["choices"][0]; msg = ch["message"]; u = d.get("usage") or {}
            content = str(msg.get("content") or "")
            if not content and ch.get("finish_reason") == "length":
                content = ""  # the model spent the whole cap on reasoning; logged by the caller as content 0 chars
            global LAST_REASONING_TOKENS
            LAST_REASONING_TOKENS = int(((u.get("completion_tokens_details") or {}).get("reasoning_tokens")) or 0)
            return content, int(u.get("prompt_tokens") or 0), int(u.get("completion_tokens") or 0)
        except urllib.error.HTTPError as e:
            if e.code in (403, 408, 429, 500, 502, 503, 504) and attempt < 5:
                time.sleep(min(120, 5 * 2 ** attempt)); continue
            return f"HTTP_ERROR {e.code}: {e.read()[:200].decode(errors='ignore')}", 0, 0
        except Exception as e:
            if attempt < 5:
                time.sleep(min(120, 5 * 2 ** attempt)); continue
            return f"ERROR {repr(e)[:200]}", 0, 0

RULEBOOKS = {}   # §339: cell -> a stronger player's rulebook, handed to the model when --rulebook-from is set


def _rulebook_prefix(cell):
    key = f"{cell[0]}:L{cell[1]}"
    rb = RULEBOOKS.get(key)
    if not rb:
        return ""
    return ("A stronger player already worked out the rules of this exact level. Its rulebook follows; treat it as true and "
            "write the predictor from it rather than re-deriving the rules.\n\n" + rb + "\n\n")

def run_cell(arm, cell, trans_train, trans_held, iters, keys, model_fn=None, compact=False, max_tokens=8000, tool=False, explore_calls=6, objects=False, objects_only=False, label="", samples=1):
    _TL.calls = []; _cell_t0 = time.perf_counter()   # §347b: timing
    shown = render_objects(trans_train, raw_board=not objects_only) if (objects or objects_only) else (render_compact(trans_train) if compact else "\n".join(render_transition(i, t) for i, t in enumerate(trans_train)))
    messages = [{"role": "system", "content": SYSTEM + (TOOL_NOTE if tool else "")},
                {"role": "user", "content": f"{_rulebook_prefix(cell)}Game {cell[0]}, level {cell[1]}. {len(trans_train)} recorded transitions follow.\n\n{shown}\n\nWrite world_model.md, then the predict code block."}]
    code = None; used = 0; tokens = [0, 0]; train_exact = 0; log = []
    final_text = None   # the last deliverable (rulebook + code), kept (§303 B4)
    sample_least_code = None   # §237a: the least-reasoning sample's code from the last sampled iteration
    for it in range(1, iters + 1):
        used = it
        if model_fn:
            text = model_fn(messages); pt = ct = 0
        else:
            text, pt, ct = call_model(arm, messages, keys, max_tokens=max_tokens)
        tokens[0] += pt; tokens[1] += ct
        log.append(f"iter {it}: content {len(text)} chars, completion {ct} tok, reasoning {LAST_REASONING_TOKENS} tok")
        if samples > 1 and not model_fn:
            # §237a Factor S: N samples per iteration; the replay checker on the SHOWN transitions selects the one that
            # continues (best-of-N); the least-reasoning sample with code is recorded as the second selector
            cands = [(text, ct, LAST_REASONING_TOKENS)]
            for _ in range(samples - 1):
                t2, p2, c2 = call_model(arm, messages, keys, max_tokens=max_tokens)
                tokens[0] += p2; tokens[1] += c2; cands.append((t2, c2, LAST_REASONING_TOKENS))
            scored = []
            for t2, c2, r2 in cands:
                cd = extract_code(t2)
                if cd:
                    pr = run_model_code(cd, [(board_lines(t["board_before"]), (t["action_display"] or t["action_name"])) for t in trans_train])
                    ex, _, _ = score(pr, trans_train)
                else:
                    ex = -1
                scored.append((ex, r2, t2))
            log.append(f"iter {it}: samples {samples}: shown-exact per sample {[x[0] for x in scored]}, reasoning tok {[x[1] for x in scored]}")
            with_code = [x for x in scored if x[0] >= 0]
            if with_code:
                least = min(with_code, key=lambda x: x[1]); sample_least_code = extract_code(least[2])
            best = max(scored, key=lambda x: x[0]); text = best[2]
        if tool:
            # §234 I8: exploration turns — any code block WITHOUT def predict is run over the transitions and its output returned
            n_explore = 0
            while n_explore < explore_calls and not text.startswith("HTTP_ERROR") and not text.startswith("ERROR"):
                ex = [b for b in code_blocks(text) if "def predict" not in b]
                if not ex or extract_code(text):
                    break
                n_explore += 1
                out = run_explore(ex[-1], trans_train)
                log.append(f"iter {it}: explore {n_explore}: {len(ex[-1])} chars code -> {len(out)} chars out")
                messages += [{"role": "assistant", "content": text or "(empty)"},
                             {"role": "user", "content": f"Output of your exploration code ({n_explore} of {explore_calls}):\n```\n{out}\n```\nContinue: explore again, or deliver world_model.md and the predict code block now."}]
                if model_fn:
                    text = model_fn(messages); pt = ct = 0
                else:
                    text, pt, ct = call_model(arm, messages, keys, max_tokens=max_tokens)
                tokens[0] += pt; tokens[1] += ct
                log.append(f"iter {it}: content {len(text)} chars, completion {ct} tok (after explore)")
        if text.startswith("HTTP_ERROR") or text.startswith("ERROR"):
            log.append(text[:200]); break
        code = extract_code(text)
        if code: final_text = text
        if not code:
            hint = ("You wrote function-call syntax (<tool_call>); there is no function-calling interface here. Put your Python in a fenced ```python block instead. " if "<tool_call>" in (text or "") else "")
            messages += [{"role": "assistant", "content": text or "(empty)"}, {"role": "user", "content": hint + "No Python code block with def predict was found. Keep your reasoning short; the deliverable is world_model.md and the code block. Return them now."}]
            log.append("no code"); continue
        preds = run_model_code(code, [(board_lines(t["board_before"]), (t["action_display"] or t["action_name"])) for t in trans_train])
        train_exact, _, fm = score(preds, trans_train)
        log.append(f"iter {it}: train exact {train_exact}/{len(trans_train)}")
        if fm is None:
            break
        messages += [{"role": "assistant", "content": text},
                     {"role": "user", "content": f"Replay check: {train_exact} of {len(trans_train)} transitions reproduced exactly. First mismatch at transition {fm[0]}: {fm[1]}\n"
                                                 "Decide whether a RULE is wrong (revise world_model.md first) or the CODE fails to implement a rule (repair the code). "
                                                 "Then return the full world_model.md and the full predict code block again."}]
    held_exact = 0; held_acc = 0.0
    if code:
        preds = run_model_code(code, [(board_lines(t["board_before"]), (t["action_display"] or t["action_name"])) for t in trans_held])
        held_exact, held_acc, _ = score(preds, trans_held)
    least_held = None
    if sample_least_code:
        pr = run_model_code(sample_least_code, [(board_lines(t["board_before"]), (t["action_display"] or t["action_name"])) for t in trans_held])
        least_held, _, _ = score(pr, trans_held)
        log.append(f"least-reasoning selector: held-out exact {least_held}/{len(trans_held)}")
    return {"least_reasoning_heldout": least_held, "samples": samples, "cell": f"{cell[0]}:L{cell[1]}", "arm": arm + (f"+s{samples}" if samples > 1 else "") + ("+tool" if tool else "") + ("+objects" if objects else "") + ("+objonly" if objects_only else "") + (f"+rb{REASONING_BUDGET}" if REASONING_BUDGET else "") + label, "iters_used": used, "train_exact": train_exact, "train_n": len(trans_train),
            "heldout_exact": held_exact, "heldout_n": len(trans_held), "heldout_cell_acc": round(held_acc, 4),
            "baseline_nothing": baseline_nothing(trans_held), "baseline_lastdiff": baseline_lastdiff(trans_held),
            "tokens": tokens, "log": log, "code": code, "final_text": final_text, "train_exact": train_exact, "k": len(trans_train),
            "elapsed_s": round(time.perf_counter() - _cell_t0, 1), "api_calls_s": list(getattr(_TL, "calls", []))}


# ---------------------------------------------------------------------------------------------------------------------
# §240 BET 2 — the harness compiles object by object. The level's moving colours are found from the shown transitions;
# for each colour the model sees only that colour's object events and writes predict_<c>(board_lines, action) that
# updates that colour's cells; each predictor is verified on its colour's mask alone (best-of-N per colour by that
# score); the harness composes the survivors into one predictor (each writes only the cells it changed; larger colour
# classes first). The composed model is scored exactly as the joint attempt (held-out exact vs nothing-changes).
# ---------------------------------------------------------------------------------------------------------------------
def moving_colours(trans):
    bg = max(set("".join(board_lines(trans[0]["board_before"]))), key="".join(board_lines(trans[0]["board_before"])).count)
    cnt = {}
    for t in trans:
        a = board_lines(t["board_before"]); b = board_lines(t["board_after"])
        for r in range(64):
            for c in range(64):
                if a[r][c] != b[r][c]:
                    for col in (a[r][c], b[r][c]):
                        if col != bg:
                            cnt[col] = cnt.get(col, 0) + 1
    return bg, [c for c, _ in sorted(cnt.items(), key=lambda kv: -kv[1])]

def render_colour_events(trans, colour, bg):
    """Object events of ONE colour per transition (MOVED/GONE/NEW for that colour only), plus that colour's start inventory."""
    start = board_lines(trans[0]["board_before"])
    cells = [(r, c) for r in range(64) for c in range(64) if start[r][c] == colour]
    inv = [describe(o) for o in sorted(components(start, cells), key=lambda o: -len(o[1]))][:20]
    out = [f"Colour {colour} at the start: " + ("; ".join(inv) if inv else "none on the board")]
    full = render_objects(trans, cap=40, raw_board=False).split("\n")
    for line in full:
        if not line.startswith("### transition"):
            continue
        head, _, rest = line.partition("objects:")
        evs = [e.strip() for e in rest.split(";") if re.search(r"\b(MOVED~?|GONE|NEW) " + re.escape(colour) + r" x", e)]
        out.append(head + ("colour-" + colour + " events: " + "; ".join(evs) if evs else "no change to colour " + colour))
    return "\n".join(out)

def colour_mask_score(preds, trans, colour):
    """Exact per transition on the cells where the actual before/after or the prediction carries `colour`."""
    exact = 0; first = None
    for i, (p, t) in enumerate(zip(preds, trans)):
        a = board_lines(t["board_before"]); b = board_lines(t["board_after"])
        if isinstance(p, dict) or len(p) != 64:
            if first is None: first = (i, "model error or wrong shape")
            continue
        wrong = [(r, c, p[r][c], b[r][c]) for r in range(64) for c in range(64)
                 if (a[r][c] == colour or b[r][c] == colour or p[r][c] == colour) and p[r][c] != b[r][c]]
        if not wrong:
            exact += 1
        elif first is None:
            first = (i, "action " + str(t["action_display"] or t["action_name"]) + "; colour-" + colour + " cells wrong (row,col,predicted,actual): " +
                     "; ".join(f"({r},{c},{x}->{y})" for r, c, x, y in wrong[:30]) + (" ..." if len(wrong) > 30 else ""))
    return exact, first

COMPOSE_RUNNER = r"""
import sys, json
mods = json.load(open(sys.argv[1]))   # list of (colour, code) in application order
fns = []
for colour, src in mods:
    ns = {}
    exec(compile(src, "wm_" + colour, "exec"), ns)
    fns.append((colour, ns.get("predict")))
data = json.load(open(sys.argv[2]))
out = []
for board, action in data:
    cur = list(board)
    try:
        for colour, fn in fns:
            nb = [str(x) for x in fn(list(board), action)]
            if len(nb) != 64: continue
            # take only the cells this predictor changed relative to the ORIGINAL board
            cur = ["".join(nb[r][c] if nb[r][c] != board[r][c] else cur[r][c] for c in range(64)) for r in range(64)]
        out.append(cur)
    except Exception as e:
        out.append({"error": repr(e)[:200]})
json.dump(out, open(sys.argv[3], "w"))
"""

def run_composed(mods, pairs, timeout=90):
    d = tempfile.mkdtemp(prefix="wmcompose-")
    mp = os.path.join(d, "mods.json"); inp = os.path.join(d, "in.json"); outp = os.path.join(d, "out.json"); rp = os.path.join(d, "run.py")
    json.dump(mods, open(mp, "w")); json.dump(pairs, open(inp, "w")); open(rp, "w").write(COMPOSE_RUNNER)
    try:
        subprocess.run([sys.executable, "-I", rp, mp, inp, outp], timeout=timeout, capture_output=True, cwd=d)
        return json.load(open(outp))
    except Exception as e:
        return [{"error": f"runner: {repr(e)[:160]}"}] * len(pairs)

def run_cell_per_object(arm, cell, trans_train, trans_held, iters, keys, model_fn=None, max_tokens=8000, samples=1, label="", max_colours=6):
    bg, colours = moving_colours(trans_train)
    colours = colours[:max_colours]
    pairs_train = [(board_lines(t["board_before"]), (t["action_display"] or t["action_name"])) for t in trans_train]
    pairs_held = [(board_lines(t["board_before"]), (t["action_display"] or t["action_name"])) for t in trans_held]
    log = [f"colours (moving, by changed cells): {colours}; background {bg}"]; tokens = [0, 0]; mods = []; per_colour = {}
    for colour in colours:
        shown = render_colour_events(trans_train, colour, bg)
        sysmsg = (SYSTEM + f"\nThis call is about ONE colour only: '{colour}'. Write world_model.md for colour {colour}'s objects and a "
                  f"Python predict(board_lines, action) that updates ONLY the cells of colour {colour} (where they go, appear, vanish) and "
                  f"leaves every other cell exactly as it is. Other colours' rules are handled elsewhere.")
        messages = [{"role": "system", "content": sysmsg},
                    {"role": "user", "content": f"Game {cell[0]}, level {cell[1]}, colour {colour}. {len(trans_train)} recorded transitions follow.\n\n{shown}\n\nWrite world_model.md for colour {colour}, then the predict code block."}]
        best = (-1, None); used = 0
        for it in range(1, iters + 1):
            used = it
            cands = []
            for _ in range(samples):
                if model_fn:
                    text = model_fn(messages); pt = ct = 0
                else:
                    text, pt, ct = call_model(arm, messages, keys, max_tokens=max_tokens)
                tokens[0] += pt; tokens[1] += ct
                code = extract_code(text)
                if not code:
                    cands.append((-1, None, text)); continue
                preds = run_model_code(code, pairs_train)
                ex, fm = colour_mask_score(preds, trans_train, colour)
                cands.append((ex, code, text, fm))
            top = max(cands, key=lambda x: x[0])
            log.append(f"colour {colour} iter {it}: per-sample colour-exact {[c[0] for c in cands]}/{len(trans_train)}")
            if top[0] > best[0]:
                best = (top[0], top[1])
            if top[0] >= len(trans_train) or top[1] is None:
                if top[1] is None:
                    messages += [{"role": "assistant", "content": top[2] or "(empty)"}, {"role": "user", "content": "No Python code block with def predict was found. Return world_model.md and the predict code block."}]
                    continue
                break
            fm = top[3]
            messages += [{"role": "assistant", "content": top[2]},
                         {"role": "user", "content": f"Replay check for colour {colour}: {top[0]} of {len(trans_train)} transitions reproduced exactly on colour {colour}'s cells. First mismatch at transition {fm[0]}: {fm[1]}\n"
                                                     f"Decide whether a RULE is wrong (revise world_model.md first) or the CODE fails to implement it; return the full world_model.md and the full predict code block again."}]
        per_colour[colour] = {"best_colour_exact": best[0], "iters": used}
        if best[1]:
            mods.append((colour, best[1]))
    log.append("composed from colours: " + ",".join(c for c, _ in mods))
    preds_train = run_composed(mods, pairs_train) if mods else [{"error": "no modules"}] * len(pairs_train)
    train_exact, _, _ = score(preds_train, trans_train)
    preds_held = run_composed(mods, pairs_held) if mods else [{"error": "no modules"}] * len(pairs_held)
    held_exact, held_acc, _ = score(preds_held, trans_held)
    return {"cell": f"{cell[0]}:L{cell[1]}", "arm": arm + (f"+s{samples}" if samples > 1 else "") + "+perobject" + label, "iters_used": max((v["iters"] for v in per_colour.values()), default=0),
            "train_exact": train_exact, "train_n": len(trans_train), "heldout_exact": held_exact, "heldout_n": len(trans_held),
            "heldout_cell_acc": held_acc, "baseline_nothing": baseline_nothing(trans_held), "baseline_lastdiff": baseline_lastdiff(trans_held),
            "tokens": tokens, "log": log, "per_colour": per_colour, "code": json.dumps(mods)}

def pick_cells(transitions, cells, k, m):
    by = {}
    for t in transitions:
        by.setdefault((t["game"], t["level"], t["session"]), []).append(t)
    out = {}
    for g, lv in cells:
        cands = [(s, rows) for (gg, ll, s), rows in by.items() if gg == g and ll == lv and len(rows) >= k + m]
        if not cands:
            cands = [(s, rows) for (gg, ll, s), rows in by.items() if gg == g and ll == lv and len(rows) >= k + 5]
        if not cands:
            continue
        cands.sort(key=lambda x: -len(x[1]))
        rank = int(os.environ.get("WM_SESSION_RANK", "1"))   # (§322 D.2) WM_SESSION_RANK=2 takes the second-longest session of the cell
        if len(cands) < rank: continue
        s, rows = cands[rank - 1]
        rows = sorted(rows, key=lambda r: r["action_num"] or 0)
        out[(g, lv)] = (rows[:k], rows[k:k + m])
    return out

def print_rows(results, arm, bar_cells=12, bar_points=20):
    beat = 0; he = []; bn = []
    for r in results:
        print(f"CELL {r['cell']:9s} {arm:5s} iters {r['iters_used']}  train_exact {r['train_exact']}/{r['train_n']}  heldout_exact {r['heldout_exact']}/{r['heldout_n']}  "
              f"cell_acc {r['heldout_cell_acc']:.3f}  baseline_nothing {r['baseline_nothing']}/{r['heldout_n']}  baseline_lastdiff {r['baseline_lastdiff']}/{r['heldout_n']}")
        n = max(1, r['heldout_n']); he.append(100 * r['heldout_exact'] / n); bn.append(100 * r['baseline_nothing'] / n)
        beat += (100 * (r['heldout_exact'] - r['baseline_nothing']) / n) >= bar_points
    import statistics as st
    if results:
        print(f"SUMMARY {arm}: cells {len(results)} | cells beating nothing-changes by >= {bar_points} points: {beat} | median heldout_exact {st.median(he):.0f}% | median nothing {st.median(bn):.0f}%")
        if arm == "flash":
            print(f"BAR §224.F.1 (>= {bar_cells} of 24 cells beat nothing-changes by >= 20 points): {'PASS' if beat >= bar_cells else 'MISS'}")

def fixture():
    # a yellow pixel moves one cell per action on a black 64x64 board with a white border; it stops at the border
    random.seed(7); r, c = 10, 10; trans = []
    def board(r, c):
        g = [["B"] * 64 for _ in range(64)]
        for i in range(64):
            g[0][i] = g[63][i] = g[i][0] = g[i][63] = "W"
        g[r][c] = "Y"; return ["".join(x) for x in g]
    for i in range(40):
        a = random.choice(["UP", "DOWN", "LEFT", "RIGHT"]); b = board(r, c)
        nr, nc = r + (a == "DOWN") - (a == "UP"), c + (a == "RIGHT") - (a == "LEFT")
        if 1 <= nr <= 62 and 1 <= nc <= 62:
            r, c = nr, nc
        trans.append({"game": "fx01", "level": 1, "session": "fx01_p0", "action_num": i + 1, "action_name": a, "action_display": a,
                      "board_before": "\n".join(b), "board_after": "\n".join(board(r, c))})
    good = '''
def predict(board_lines, action):
    g = [list(x) for x in board_lines]
    pos = [(r, c) for r in range(64) for c in range(64) if g[r][c] == "Y"]
    if not pos: return ["".join(x) for x in g]
    r, c = pos[0]
    nr = r + (action == "DOWN") - (action == "UP"); nc = c + (action == "RIGHT") - (action == "LEFT")
    if 1 <= nr <= 62 and 1 <= nc <= 62:
        g[r][c] = "B"; g[nr][nc] = "Y"
    return ["".join(x) for x in g]
'''
    mock = lambda messages: "world_model.md\n1. A yellow pixel moves one cell per action inside a white border.\n```python\n" + good + "\n```"
    res = run_cell("mock", ("fx01", 1), trans[:20], trans[20:40], 2, {}, model_fn=mock)
    print_rows([res], "mock")
    print("fixture expectation: heldout_exact 20/20, baseline_nothing well below 20")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--transitions"); ap.add_argument("--arm", default="flash"); ap.add_argument("--out", default="")
    ap.add_argument("--cells", default=DEFAULT_CELLS); ap.add_argument("--k", type=int, default=20); ap.add_argument("--m", type=int, default=20)
    ap.add_argument("--iters", type=int, default=4); ap.add_argument("--workers", type=int, default=3); ap.add_argument("--dry", action="store_true"); ap.add_argument("--fixture", action="store_true"); ap.add_argument("--compact", action="store_true"); ap.add_argument("--max-tokens", type=int, default=8000)
    ap.add_argument("--tool", action="store_true", help="§234 I8: exploration code turns over the transitions before the deliverable")
    ap.add_argument("--objects", action="store_true", help="§234 I9: the harness does the bookkeeping — transitions rendered as object events (MOVED/GONE/NEW)")
    ap.add_argument("--objects-only", action="store_true", help="§237: object events AND the start board as an object inventory (no raw grid)")
    ap.add_argument("--reasoning-budget", type=int, default=0, help="§237: OpenRouter reasoning.max_tokens for the thinking arms (0 = default)")
    ap.add_argument("--label", default="", help="suffix for the arm label in the rows")
    ap.add_argument("--rulebook-from", default="", help="§339: a probe JSONL whose final_text holds a stronger player's rulebook per cell (text before the first code fence); it is handed to the model and only the predictor is asked for")
    ap.add_argument("--samples", type=int, default=1, help="§237a Factor S: N samples per iteration, best-of-N by shown-transition replay; least-reasoning selector recorded")
    ap.add_argument("--per-object", action="store_true", help="§240 bet 2: one predictor per moving colour, verified per colour, composed by the harness")
    a = ap.parse_args()
    global REASONING_BUDGET
    REASONING_BUDGET = max(0, a.reasoning_budget)
    if a.fixture:
        fixture(); return
    rk = lambda n: (open(os.path.join(ARC, n)).read().strip() if os.path.exists(os.path.join(ARC, n)) else "")
    keys = {"openrouter": rk(".secrets/openrouter_key"), "inference": rk(".secrets/inference_net_key")}
    cells = [(x.split(":")[0], int(x.split(":")[1])) for x in a.cells.split(",") if x.strip()]
    if a.rulebook_from:
        global RULEBOOKS
        RULEBOOKS = {}
        for line in open(a.rulebook_from):
            try: r = json.loads(line)
            except Exception: continue
            t = (r.get("final_text") or "")
            if not t: continue
            i = t.find("```")
            rb = (t[:i] if i > 0 else t).strip()
            if len(rb) > 400: RULEBOOKS[r["cell"]] = rb
        print(f"rulebooks loaded: {len(RULEBOOKS)} cells from {a.rulebook_from}")
    transitions = [json.loads(l) for l in open(a.transitions)]
    picked = pick_cells(transitions, cells, a.k, a.m)
    print(f"cells requested {len(cells)}, with data {len(picked)}: {', '.join(f'{g}:L{l}' for g, l in picked)}")
    if a.dry:
        return
    def work(item):
        (g, lv), (tr, held) = item
        if a.per_object:
            return run_cell_per_object(a.arm, (g, lv), tr, held, a.iters, keys, max_tokens=a.max_tokens, samples=a.samples, label=a.label)
        return run_cell(a.arm, (g, lv), tr, held, a.iters, keys, compact=a.compact, max_tokens=a.max_tokens, tool=a.tool, objects=a.objects, objects_only=a.objects_only, label=a.label, samples=a.samples)
    results = []
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for r in ex.map(work, list(picked.items())):
            results.append(r)
            if a.out:
                with open(a.out, "a") as f:
                    f.write(json.dumps(r) + "\n")
    print_rows(results, a.arm)
    tok = [sum(r["tokens"][0] for r in results), sum(r["tokens"][1] for r in results)]
    print(f"tokens prompt {tok[0]:,} completion {tok[1]:,}")

if __name__ == "__main__":
    main()
