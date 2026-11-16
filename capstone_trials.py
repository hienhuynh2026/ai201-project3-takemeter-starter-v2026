#!/usr/bin/env python3
"""
Capstone trials: run the five criteria in criteria.md once per trial and score
them from the log (and, for wall time from the shell, from the outside).

    python capstone_trials.py --trials 3 --log logs/trials_before.jsonl --out trials_before.json

Each trial runs takemeter.py as a separate process, exactly as a user would:
  criteria 1, 4, 5  one run on test_split.csv
  criterion 2       three bad inputs, each timed from the shell
  criterion 3       capstone_tests/mixed_blank.csv (10 rows, 3 blank)
No code changes between trials.
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

LABELS = {"hot_take", "neutral", "stat_backed"}
MISSING = "capstone_tests/this_file_does_not_exist.csv"
NO_TEXT = "capstone_tests/no_text_column.csv"
MIXED = "capstone_tests/mixed_blank.csv"


def run_takemeter(log, *extra):
    """Run takemeter.py, return (exit code, shell wall seconds, records it wrote)."""
    path = Path(log)
    before = len(path.read_text(encoding="utf-8").splitlines()) if path.exists() else 0
    t0 = time.perf_counter()
    proc = subprocess.run([sys.executable, "takemeter.py", "--log", log, *extra],
                          capture_output=True, text=True)
    wall = time.perf_counter() - t0
    lines = path.read_text(encoding="utf-8").splitlines()[before:]
    return proc.returncode, wall, [json.loads(l) for l in lines if l.strip()]


def split(records):
    run = [r for r in records if r["event"] == "run"]
    preds = [r for r in records if r["event"] == "prediction"]
    return run, preds


def p95(values):
    values = sorted(values)
    k = (len(values) - 1) * 0.95
    lo, hi = int(k), min(int(k) + 1, len(values) - 1)
    return values[lo] + (values[hi] - values[lo]) * (k - lo)


def trial(log):
    out = {}

    # Criteria 1, 4, 5: one normal run on the held-out posts.
    code, shell_wall, recs = run_takemeter(log)
    runs, preds = split(recs)
    good = [p for p in preds if p["status"] == "ok" and p.get("timestamp") and p.get("input")
            and p.get("output") in LABELS and (p.get("duration_s") or 0) > 0]
    run = runs[0] if len(runs) == 1 else {}
    c1 = len(good) == 30 and len(preds) == 30 and len(runs) == 1 and run.get("n_ok") == 30
    out["c1"] = {"pass": c1, "complete_post_records": len(good), "post_records": len(preds),
                 "run_records": len(runs), "n_ok": run.get("n_ok"), "run_id": run.get("run_id")}

    lat = [p["duration_s"] for p in preds if p["status"] == "ok"]
    wall, rss, lat95 = run.get("wall_s"), run.get("peak_rss_mb"), (p95(lat) if lat else None)
    c4 = wall is not None and wall <= 60.0 and lat95 <= 3.0 and rss <= 1800
    out["c4"] = {"pass": c4, "wall_s": wall, "p95_s": round(lat95, 2) if lat95 else None,
                 "peak_rss_mb": rss, "model_load_s": run.get("model_load_s"),
                 "cpu_s": run.get("cpu_s"), "run_id": run.get("run_id")}

    correct = sum(1 for p in preds if p.get("correct"))
    out["c5"] = {"pass": correct >= 15, "correct": correct, "of": len(preds),
                 "run_id": run.get("run_id")}

    # Criterion 2: three bad inputs.
    bad = []
    for name, extra, want_code in [("missing_file", ["--input", MISSING], 1),
                                   ("no_text_column", ["--input", NO_TEXT], 1),
                                   ("empty_text", ["--text", ""], 0)]:
        code, shell_wall, recs = run_takemeter(log, *extra)
        runs, preds = split(recs)
        r = runs[0] if runs else {}
        if name == "empty_text":
            named = (r.get("n_rejected") == 1 and len(preds) == 1
                     and preds[0]["status"] == "rejected")
        else:
            named = r.get("status") == "error" and r.get("error_stage") == "read_input"
        ok = named and code == want_code and shell_wall < 2.0
        bad.append({"input": name, "pass": ok, "failure_named": named, "exit": code,
                    "shell_wall_s": round(shell_wall, 2), "logged_wall_s": r.get("wall_s"),
                    "run_id": r.get("run_id")})
    out["c2"] = {"pass": all(b["pass"] for b in bad), "passed": sum(b["pass"] for b in bad),
                 "inputs": bad}

    # Criterion 3: a batch with blank rows.
    code, shell_wall, recs = run_takemeter(log, "--input", MIXED)
    runs, preds = split(recs)
    r = runs[0] if runs else {}
    n_ok = sum(p["status"] == "ok" for p in preds)
    n_rej = sum(p["status"] == "rejected" for p in preds)
    c3 = (n_ok == 7 and n_rej == 3 and r.get("status") == "ok" and r.get("n_ok") == 7
          and r.get("n_rejected") == 3 and code == 0)
    out["c3"] = {"pass": c3, "ok_records": n_ok, "rejected_records": n_rej,
                 "run_status": r.get("status"), "exit": code, "run_id": r.get("run_id")}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=3)
    ap.add_argument("--log", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    results = []
    for i in range(1, args.trials + 1):
        res = trial(args.log)
        results.append(res)
        print(f"trial {i}: " + "  ".join(f"{k}={'PASS' if res[k]['pass'] else 'fail'}"
                                         for k in ("c1", "c2", "c3", "c4", "c5")), flush=True)
    Path(args.out).write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    for k in ("c1", "c2", "c3", "c4", "c5"):
        print(f"{k}: {'MET' if all(r[k]['pass'] for r in results) else 'MISSED'}")


if __name__ == "__main__":
    main()
