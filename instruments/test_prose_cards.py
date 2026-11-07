"""Fixture for v44: with ARC3_CROSS_GAME_CARD_FORMAT=prose the block carries the same rules, counts and actions as the
stock block, with no '- game' card lines; unset = stock bytes. Applies the two hunks textually to the live cross_game.py."""
import os, sys, re
sys.path.insert(0, "runs/field/franzen-milestone2/tree/ARC3-Inference")
import inference.agent.cross_game as cg
src = open(cg.__file__).read()
a1 = '    header = ("Other games already played in this run (your own record from OTHER games; their mechanics often recur, "\n              "so treat these as hypotheses to check cheaply here, never as facts about this game):")\n'
a2 = '        same = bool(mine and g.get("valid") and set(g["valid"]) == set(mine.get("valid") or []))\n'
assert a1 in src and a2 in src, "anchors not found"
diff = open("runs/field/ours/deploy/patches/v44-prose/cross_game_prose.diff").read()
h1, h2 = diff.split("@@ render_block: the per-game line @@")
add1 = "\n".join(l[1:] for l in h1.split("\n") if l.startswith("+") and not l.startswith("+++")) + "\n"
add2 = "\n".join(l[1:] for l in h2.split("\n") if l.startswith("+") and not l.startswith("+++")) + "\n"
patched = src.replace(a1, a1 + add1, 1).replace(a2, a2 + add2, 1)
ns = {}; exec(compile(patched, cg.__file__, "exec"), ns)
cards = [{"key": "cn04-aaaa", "level": 1, "kind": "cleared", "rule": "GOAL: push the blue block onto the mark", "actions": ["UP", "UP", "LEFT"], "n_actions": 3, "valid": None, "palette": [], "t": 1, "levels_total": 6},
         {"key": "lp85-bbbb", "level": 2, "kind": "stuck", "rule": "the red door never opened", "actions": [], "n_actions": 0, "valid": None, "palette": [], "t": 2, "levels_total": 4}]
os.environ.pop("ARC3_CROSS_GAME_CARD_FORMAT", None); stock = ns["render_block"](cards)
os.environ["ARC3_CROSS_GAME_CARD_FORMAT"] = "prose"; prose = ns["render_block"](cards)
assert stock.count("- game ") == 2 and "- game " not in prose, "prose must drop the card lines"
for s in ("push the blue block onto the mark", "red door never opened", "3 actions", "cn04", "lp85", "of 6"):
    assert s in prose, f"prose lost: {s}"
assert "1 level of 6" in prose and "not cleared" in prose
os.environ.pop("ARC3_CROSS_GAME_CARD_FORMAT"); assert ns["render_block"](cards) == stock, "unset must be stock bytes"
print("prose fixture PASS: same rules, counts and actions; no card lines; unset = stock")
