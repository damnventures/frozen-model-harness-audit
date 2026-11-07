"""Fixture for v43: the stagger helper parses its envs; unset = 0 for every game; the solver anchor exists for the hook."""
import os, re
S = open("runs/field/franzen-milestone2/tree/ARC3-Inference/inference/framework/solver.py").read()
anchor = "                viewer_data_path=viewer_data_path,\n            )\n            session.play()\n"
assert anchor in S, "anchor for the _play_one hook not found"
assert "import time" in S or "time.monotonic" in S, "solver must import time"
helper = open("runs/field/ours/deploy/patches/v43-stagger/solver_stagger.diff").read().split("@@ _play_one")[0]
code = "\n".join(l[1:] for l in helper.split("\n") if l.startswith("+") and not l.startswith("+++"))
ns = {"os": os}; exec(code, ns); f = ns["_stagger_delay_s"]
for k in ("ARC3_START_DELAY_S","ARC3_START_DELAY_GAMES","ARC3_START_DELAY_HALF"): os.environ.pop(k, None)
assert f("sp80-abc", 0) == 0.0 and f("sp80-abc", 1) == 0.0
os.environ["ARC3_START_DELAY_S"] = "3000"; os.environ["ARC3_START_DELAY_GAMES"] = "sp80,wa30"
assert f("sp80-abc", 0) == 3000.0 and f("wa30-x", 5) == 3000.0 and f("ar25-x", 1) == 0.0
os.environ.pop("ARC3_START_DELAY_GAMES"); os.environ["ARC3_START_DELAY_HALF"] = "1"
assert f("ar25-x", 0) == 0.0 and f("ar25-x", 1) == 3000.0
print("stagger fixture PASS: unset = 0; named list and odd-half both gate the delay")
