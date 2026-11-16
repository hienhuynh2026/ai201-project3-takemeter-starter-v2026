# Acceptance criteria: TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit, *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in. A criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind. It is stricter than it first sounds.

---

## 1.

<!-- Your criterion. It must name a number. -->

Overall accuracy: at least 0.65 on the held-out test set, on all three seeds.

**Why this target:**

I have three labels (`stat_backed`, `hot_take`, `neutral`), so guessing gets about 33%. 0.65 is roughly double chance. Many RealGM posts are short one-liners that give the model little text to work with, so I don't expect much higher, and the target has to hold on every seed, not just the best one.

---

## 2.

<!-- Your criterion. -->

Per-label performance: every label has an F1 of at least 0.55 on the held-out test set, on all three seeds.

**Why this target:**

My hardest boundary is `stat_backed` vs. `neutral`. Posts that list stats but only ask a question, like the Ty Jerome post, will pull both labels' F1 down. `stat_backed` will probably be my smallest label, so its test-split F1 will jump around between seeds. 0.55 is the floor where neither label is being ignored.

---

## 3.

<!-- Your criterion. -->

Balance: each label's share of the model's test-set predictions is within 10 percentage points of its true share in the test set.

**Why this target:**

Many RealGM posts are short, unsupported opinions, so `hot_take` will likely be my biggest label. I want to catch the model falling back on `hot_take` for anything ambiguous instead of learning the other two labels.

---

## 4.

<!-- Your criterion. -->

Consistency: at least 70% agreement (21 of 30) with the staff labels on the agreement set.

**Why this target:**

Several of the 30 staff posts are deliberately ambiguous, and I'm applying the staff taxonomy instead of my own, so some disagreement is expected. Below 70% would suggest I apply written decision rules loosely, which would also put my own 200 labels in doubt.

---

## 5.

<!-- Your criterion. -->

Confidence: accuracy on the most-confident third of test predictions is at least 0.15 higher than accuracy on the least-confident third.

**Why this target:**

Clear-cut posts (a full stat line, or a "don't @ me" take) should be easy and confident, while stat-heavy questions on my `stat_backed`/`neutral` boundary should be the uncertain ones. If confidence doesn't separate right from wrong by at least 0.15, it can't be used to flag posts for review.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6: read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Capstone criteria: TakeMeter, running

Written and committed before any capstone trial was run. Drafted by the AI agent at my request (see **How I Used AI** in the README). Criteria 1 to 4 test the extension (`takemeter.py` and its log); 2 and 3 test bad paths. Each is checked three times, and a target only counts as MET if it holds on all three.

## 1. Every post leaves a complete record

One run of `python takemeter.py` on the 30 posts in `test_split.csv` writes exactly 30 `prediction` records with `status: "ok"`, each with a `timestamp`, a non-empty `input`, an `output` that is one of `hot_take`, `neutral`, `stat_backed`, and a `duration_s` above 0, plus exactly one `run` record with `n_ok: 30`. Target: 30 of 30 post records and 1 run record, on each of the 3 runs.

**Why this target:** the cost and accuracy numbers in the README are computed by reading this log back. If even one post goes missing or gets logged without a label, those numbers are wrong and nothing would tell me. So the only acceptable count is all of them.

## 2. A bad input fails fast and says why

Three bad inputs: `--input` pointing at a file that doesn't exist, `--input` pointing at a CSV with no `text` column, and `--text ""`. For each one the command must (a) write a `run` record that names the failure (`status: "error"` with `error_stage: "read_input"` for the two file errors; a `rejected` prediction record and `n_rejected: 1` for the empty post), (b) exit with code 1 for the two file errors and 0 for the empty post, and (c) finish in under 2.0 seconds of wall time measured from the shell. Target: 3 of 3 bad inputs pass all three parts, on each of the 3 trials.

**Why this target:** none of these inputs ever needs the model, so there's nothing heavy to wait for. Starting Python and importing pandas is well under a second. If someone mistypes a filename, they should hear about it about as fast as `ls` would tell them. The Milestone 3 log already shows the missing-file run taking 5.8 s, so I expect this one to miss as written. The number is where it should be, not where the code currently is.

## 3. One blank row doesn't sink a batch

A CSV of 10 posts where 3 rows are blank or whitespace only. The run must classify the 7 real posts (`status: "ok"`), write a `rejected` record for each of the 3 blank rows, end with a `run` record of `status: "ok"`, `n_ok: 7`, `n_rejected: 3`, and exit with code 0. Target: exactly those counts and that exit code, on each of the 3 runs.

**Why this target:** scraped forum posts come with empty rows (deleted posts, image-only posts). A batch tool that throws away 7 good posts because of 3 empty ones is useless on real data, and one that silently skips them makes the counts in the log lie.

## 4. A 30-post run stays inside its measured budget

One run of `python takemeter.py` on `test_split.csv` finishes in at most 60.0 s of wall time (`wall_s` in the run record), with a per-post p95 latency of at most 3.0 s and `peak_rss_mb` at most 1,800 MB. Target: all three limits, on each of the 3 runs.

**Why this target:** these are the numbers in the README and RUNNING.md (54.9 s mean, 2.48 s p95, 1.75 GB). 60 s gives about 10% headroom over the mean, and 1,800 MB is the figure RUNNING.md tells people they need. One of the ten Milestone 3 runs took 61.6 s, so this isn't guaranteed to hold. If it doesn't, the cost I'm reporting is too optimistic.

## 5. The labels are worth reading

At least 15 of the 30 held-out posts (0.50) get the same label as `gold` (`correct: true` in the post records), on each of the 3 runs.

**Why this target:** with three labels, guessing gets about 10 of 30. The zero-shot baseline in Unit 6 got 12 of 30 (0.40) and never got a `neutral` or `stat_backed` post right. Running it from a clean command with logging doesn't make it better by itself, and this criterion is here so the capstone doesn't confuse "it runs and logs" with "its output is useful". 0.50 is the lowest number where more than half of what the log says is right.
