#!/usr/bin/env python3
"""
TakeMeter, running. <- CAPSTONE

One command that is "the system running": load the classifier, label a batch of
posts, and leave a structured record of every post behind in a log file.

    python takemeter.py                      # the 30 held-out posts in test_split.csv
    python takemeter.py --text "Luka is washed"
    python takemeter.py --input some_posts.csv
    python takemeter.py --report             # cost and latency, read back from the log

The classifier is the zero-shot model from baseline.py (facebook/bart-large-mnli)
using the label definitions in label_definitions.txt. Everything runs locally.

Every record is one JSON object per line in logs/takemeter.jsonl. Two kinds:

  event "prediction"  one per post: input, output label, score, duration_s,
                      status ok | rejected | error
  event "run"         one per run, written last, even when the run fails:
                      model_load_s, inference_s, wall_s, cpu_s, peak_rss_mb,
                      counts, status ok | error
"""

import argparse
import json
import platform
import resource
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from baseline import HYPOTHESIS, ZERO_SHOT_MODEL, load_definitions

DEFAULT_INPUT = "test_split.csv"
DEFAULT_LOG = "logs/takemeter.jsonl"
INPUT_PREVIEW_CHARS = 280


def now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def peak_rss_mb():
    """Peak resident memory of this process so far. macOS reports bytes, Linux KB."""
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return round(peak / (1024 * 1024) if sys.platform == "darwin" else peak / 1024, 1)


class RunLog:
    """Appends one JSON record per line. Every record carries the run id."""

    def __init__(self, path, run_id):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.run_id = run_id

    def write(self, event, **fields):
        record = {"timestamp": now(), "run_id": self.run_id, "event": event, **fields}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record


class RunFailed(Exception):
    """A failure that ends the whole run (as opposed to one bad post)."""

    def __init__(self, stage, message):
        super().__init__(message)
        self.stage = stage


def read_posts(args):
    """Return a list of (input_id, text, gold_or_None)."""
    if args.text is not None:
        return [(0, args.text, None)]

    import pandas as pd

    path = Path(args.input)
    if not path.exists():
        raise RunFailed("read_input", f"No file at {path}")
    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise RunFailed("read_input", f"Could not read {path} as CSV: {type(e).__name__}: {e}")
    if "text" not in df.columns:
        raise RunFailed("read_input", f"{path} has no 'text' column (found: {', '.join(df.columns)})")
    if len(df) == 0:
        raise RunFailed("read_input", f"{path} has no rows")

    gold = df["label"].astype(str).str.strip() if "label" in df.columns else None
    return [
        (i, df["text"].iloc[i], gold.iloc[i] if gold is not None else None)
        for i in range(len(df))
    ]


def is_blank(text):
    return text is None or (isinstance(text, float) and text != text) or not str(text).strip()


def run(args, log, stats):
    definitions = load_definitions(args.definitions)
    if not definitions:
        raise RunFailed("load_definitions", f"No label definitions found in {args.definitions}")
    labels = sorted(definitions)
    candidates = [definitions[label] for label in labels]
    back = dict(zip(candidates, labels))

    posts = read_posts(args)
    stats["n_inputs"] = len(posts)

    # Nothing worth classifying: reject every post without paying for the model.
    if all(is_blank(text) for _, text, _ in posts):
        for input_id, text, gold in posts:
            log.write("prediction", input_id=input_id, input="", input_chars=0,
                      model=args.model, status="rejected", error="empty post",
                      output=None, score=None, gold=gold, duration_s=0.0)
            stats["n_rejected"] += 1
            print(f"{input_id:>3}  REJECTED     empty post")
        return

    t0 = time.perf_counter()
    try:
        from transformers import pipeline

        classifier = pipeline("zero-shot-classification", model=args.model, device=-1)
    except Exception as e:
        raise RunFailed("load_model", f"{type(e).__name__}: {e}")
    finally:
        stats["model_load_s"] = round(time.perf_counter() - t0, 3)

    for input_id, text, gold in posts:
        common = {
            "input_id": input_id,
            "input": "" if is_blank(text) else str(text)[:INPUT_PREVIEW_CHARS],
            "input_chars": 0 if is_blank(text) else len(str(text)),
            "model": args.model,
        }
        t0 = time.perf_counter()

        if is_blank(text):
            log.write("prediction", **common, status="rejected", error="empty post",
                      output=None, score=None, gold=gold, duration_s=0.0)
            stats["n_rejected"] += 1
            print(f"{input_id:>3}  REJECTED     empty post")
            continue

        try:
            result = classifier(str(text), candidate_labels=candidates,
                                hypothesis_template=HYPOTHESIS)
        except Exception as e:
            duration = time.perf_counter() - t0
            stats["inference_s"] += duration
            log.write("prediction", **common, status="error",
                      error=f"{type(e).__name__}: {e}", output=None, score=None,
                      gold=gold, duration_s=round(duration, 3))
            stats["n_error"] += 1
            print(f"{input_id:>3}  ERROR        {type(e).__name__}")
            continue

        duration = time.perf_counter() - t0
        stats["inference_s"] += duration
        scores = {back[c]: round(s, 4) for c, s in zip(result["labels"], result["scores"])}
        output = back[result["labels"][0]]
        log.write("prediction", **common, status="ok", output=output,
                  score=scores[output], scores=scores, gold=gold,
                  correct=(output == gold) if gold is not None else None,
                  duration_s=round(duration, 3))
        stats["n_ok"] += 1
        print(f"{input_id:>3}  {output:<12} {scores[output]:.2f}  {duration:.2f}s")


def percentile(values, p):
    values = sorted(values)
    if not values:
        return None
    k = (len(values) - 1) * p / 100
    lo, hi = int(k), min(int(k) + 1, len(values) - 1)
    return values[lo] + (values[hi] - values[lo]) * (k - lo)


def report(log_path, last=None):
    """Read the log back and summarise cost and latency per input source."""
    path = Path(log_path)
    if not path.exists():
        print(f"No log at {path}. Run `python takemeter.py` first.", file=sys.stderr)
        return 1
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    runs = [r for r in records if r["event"] == "run"]
    if last:
        runs = runs[-last:]
    keep = {r["run_id"] for r in runs}
    preds = [r for r in records if r["event"] == "prediction" and r["run_id"] in keep]

    def stat_line(name, values, unit="s"):
        values = [v for v in values if v is not None]
        if not values:
            return f"  {name:<22} n/a"
        mean = sum(values) / len(values)
        return (f"  {name:<22} mean {mean:8.2f}{unit}  min {min(values):8.2f}{unit}  "
                f"max {max(values):8.2f}{unit}")

    failed = [r for r in runs if r["status"] != "ok"]
    print(f"{path}: {len(runs)} runs ({len(failed)} failed), {len(preds)} post records\n")

    by_input = {}
    for r in runs:
        if r["status"] == "ok":
            by_input.setdefault(r["input"], []).append(r)
    for source, group in by_input.items():
        print(f"Successful runs on {source}: {len(group)} (posts per run: "
              f"{sorted({g['n_inputs'] for g in group})})")
        print(stat_line("wall per run", [g["wall_s"] for g in group]))
        print(stat_line("CPU per run", [g["cpu_s"] for g in group]))
        print(stat_line("model load", [g["model_load_s"] for g in group]))
        print(stat_line("inference total", [g["inference_s"] for g in group]))
        print(stat_line("peak RSS", [g["peak_rss_mb"] for g in group], " MB"))
        ids = {g["run_id"] for g in group}
        lat = [p["duration_s"] for p in preds if p["run_id"] in ids and p["status"] == "ok"]
        if lat:
            print(f"  {'per-post latency':<22} p50 {percentile(lat, 50):.2f}s  "
                  f"p95 {percentile(lat, 95):.2f}s  max {max(lat):.2f}s  (n={len(lat)})")
        print()

    for r in failed:
        print(f"  failed run {r['run_id']} at {r['timestamp']}: "
              f"{r.get('error_stage')}: {r.get('error', '')[:100]}")
    statuses = {}
    for p in preds:
        statuses[p["status"]] = statuses.get(p["status"], 0) + 1
    print(f"\nPost records by status: {statuses}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Run TakeMeter and log every post.")
    parser.add_argument("--input", default=DEFAULT_INPUT, help="CSV with a 'text' column")
    parser.add_argument("--text", default=None, help="classify one post instead of a file")
    parser.add_argument("--definitions", default="label_definitions.txt")
    parser.add_argument("--model", default=ZERO_SHOT_MODEL)
    parser.add_argument("--log", default=DEFAULT_LOG)
    parser.add_argument("--report", action="store_true",
                        help="don't classify; summarise cost and latency from the log")
    parser.add_argument("--last", type=int, default=None,
                        help="with --report: only the last N runs")
    args = parser.parse_args()

    if args.report:
        sys.exit(report(args.log, args.last))

    log = RunLog(args.log, uuid.uuid4().hex[:8])
    wall0, cpu0 = time.perf_counter(), time.process_time()
    stats = {"n_inputs": 0, "n_ok": 0, "n_rejected": 0, "n_error": 0,
             "model_load_s": None, "inference_s": 0.0}
    status, failure = "ok", {}

    try:
        run(args, log, stats)
    except RunFailed as e:
        status, failure = "error", {"error_stage": e.stage, "error": str(e)}
        print(f"Run failed at {e.stage}: {e}", file=sys.stderr)
    except KeyboardInterrupt:
        status, failure = "error", {"error_stage": "interrupted", "error": "KeyboardInterrupt"}

    import torch
    import transformers

    record = log.write(
        "run",
        status=status,
        **failure,
        input="--text" if args.text is not None else args.input,
        model=args.model,
        **{k: (round(v, 3) if isinstance(v, float) else v) for k, v in stats.items()},
        wall_s=round(time.perf_counter() - wall0, 3),
        cpu_s=round(time.process_time() - cpu0, 3),
        peak_rss_mb=peak_rss_mb(),
        device="cpu",
        torch_threads=torch.get_num_threads(),
        python=platform.python_version(),
        torch=torch.__version__,
        transformers=transformers.__version__,
        machine=f"{platform.system()} {platform.machine()}",
    )
    print(f"\nrun {log.run_id}: {status}, {stats['n_ok']}/{stats['n_inputs']} classified, "
          f"{record['wall_s']}s wall, {record['cpu_s']}s CPU, "
          f"peak {record['peak_rss_mb']} MB. Logged to {args.log}")
    sys.exit(0 if status == "ok" else 1)


if __name__ == "__main__":
    main()
