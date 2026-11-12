#!/usr/bin/env python3
"""
TakeMeter, running. <- CAPSTONE

One command that is "the system running": load the classifier, label a batch of
posts, and leave a structured record of every post behind in a log file.

    python takemeter.py                      # the 30 held-out posts in test_split.csv
    python takemeter.py --text "Luka is washed"
    python takemeter.py --input some_posts.csv

The classifier is the zero-shot model from baseline.py (facebook/bart-large-mnli)
using the label definitions in label_definitions.txt. Everything runs locally.

Every record is one JSON object per line in logs/takemeter.jsonl.
"""

import argparse
import json
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


def read_posts(args):
    """Return a list of (input_id, text, gold_or_None)."""
    if args.text is not None:
        return [(0, args.text, None)]

    import pandas as pd

    df = pd.read_csv(args.input)
    gold = df["label"].astype(str).str.strip() if "label" in df.columns else None
    return [
        (i, df["text"].iloc[i], gold.iloc[i] if gold is not None else None)
        for i in range(len(df))
    ]


def main():
    parser = argparse.ArgumentParser(description="Run TakeMeter and log every post.")
    parser.add_argument("--input", default=DEFAULT_INPUT, help="CSV with a 'text' column")
    parser.add_argument("--text", default=None, help="classify one post instead of a file")
    parser.add_argument("--definitions", default="label_definitions.txt")
    parser.add_argument("--log", default=DEFAULT_LOG)
    args = parser.parse_args()

    log = RunLog(args.log, uuid.uuid4().hex[:8])

    definitions = load_definitions(args.definitions)
    labels = sorted(definitions)
    candidates = [definitions[label] for label in labels]
    back = dict(zip(candidates, labels))

    posts = read_posts(args)

    from transformers import pipeline

    classifier = pipeline("zero-shot-classification", model=ZERO_SHOT_MODEL, device=-1)

    for input_id, text, gold in posts:
        t0 = time.perf_counter()
        result = classifier(str(text), candidate_labels=candidates,
                            hypothesis_template=HYPOTHESIS)
        duration = time.perf_counter() - t0
        scores = {back[c]: round(s, 4) for c, s in zip(result["labels"], result["scores"])}
        output = back[result["labels"][0]]
        log.write(
            "prediction",
            input_id=input_id,
            input=str(text)[:INPUT_PREVIEW_CHARS],
            output=output,
            score=scores[output],
            scores=scores,
            gold=gold,
            duration_s=round(duration, 3),
            model=ZERO_SHOT_MODEL,
        )
        print(f"{input_id:>3}  {output:<12} {scores[output]:.2f}  {duration:.2f}s")


if __name__ == "__main__":
    main()
