# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

Community: RealGM General NBA Board

Candidate distinctions I saw while reading:
1. Some posts are structured around asking questions to spark discussions, while others are statement based expressing their opinions, takes, or predictions 
2. Some posts are more into business aspect of the NBA this includes front office mechanics including proposed trades while others are more general commentary on the player or teams performances
3. Some are more extensive breakdowns on the team/players performances while others are short one liners or brief commentary.


---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `stat_backed`

**Definition:** A take on a player, team, or move that is supported by a specific number, stat, or record you could look up.

**Example 1:**
> "IDK why there is this narrative that IQ can't stay healthy. He has played 68+ games in every season, except for playing 64 games in 2021 (which was a 72-game season, and playing 64/72 games is the equivalent of 73 games in a full 82-game season), and then 33 games in 2025 when the Raptors were tanking. So he had one year of injuries. That is it."

**Example 2:**
> "In last night's pre season game Gonzalez had 17 points in 21 minutes, 6-7 from the floor, including a perfect 4-4 from beyond the arc, 6 rebounds, 2 assists and a steal. The Celtics had a large lead when he came in, so there was no pressure, but even so it was a strong, mistake-free performance. And he doesn't turn 21 until February."

### `hot_take`

**Definition:** A confident opinion or prediction about a player, team, or move with no evidence offered. It might be true, but it isn't argued.

**Example 1:**
> "His ceiling is the greatest baller to ever play the game. Don't @ me if you disagree"

**Example 2:**
> "Myles Turner is a bucket of ass. Is he the softest big in the league? Hate that he's on my team..."

### `neutral`

**Definition:** A post that takes no position on who is good or bad, like a question, news, logistics, or general excitement.

**Example 1:**
> "I just got my NBA league pass, what you all use to watch games on?"

**Example 2:**
> "Got league pass a couple hours ago, cannot wait for the first preseason game."

### The hardest boundary

**Which two labels:** `stat_backed` vs. `neutral`

**The borderline post:**
> "Last year Ty Jerome dealt with injuries and only played in 15 games. He averaged 19.7 points in 22.4 minutes per game with a .474 FG% and .420 from three. The previous year he played in 70 games and averaged 12.5 points per game with a .516 FG% and .435 from three. 19.9 minutes per game. How good is he? I've barely watched him play."

**The decision rule I used every time:**
<!-- e.g. "If the post names a specific checkable fact, it's `analysis`, even
     if the tone is heated." -->
If the post doesn't take a position on whether a player, team, or move is good or bad, it's `neutral`, even if it's full of stats. Stats only make a post `stat_backed` when they're being used to support a take.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** Every post is from the RealGM General NBA Board, copied from threads about the preseason, trades, contracts, rookies and team outlooks. My first collection had 365 rows, but 21 of them came from somewhere else (20 from another forum plus one Rookie of the Year post), so I deleted those and was left with 344 RealGM posts.

**How I labelled them:** I did 20 posts first completely on my own, with no AI and no tools, just my definitions and decision rule. Those are marked `cold` in the note column. After that I gave Claude my label definitions and my stat_backed vs. neutral decision rule and had it pre-label the other 324 posts. Those rows are marked `pre-labelled` in the note column, and I went through them myself and changed any label I disagreed with.

Once everything had a label, hot_take was 66% of the data (227 of 344) and stat_backed was only 9% (32 posts). That was too lopsided. A model could get most of the way there by guessing hot_take every time, and it wouldn't see enough stat_backed posts to learn the label I actually care about. So instead of keeping all 344, I kept all 20 cold rows, every stat_backed and neutral post, and a random set of hot_take posts, which brought me to 200 rows. I picked the hot_take rows randomly so I wouldn't just keep the easy ones.

I'd rather have 200 rows I actually read than 344 I rushed through. stat_backed is still my smallest label at 33 posts, which means only about 5 of them will land in the test set. If the model struggles on that label next unit, that's the first thing I'll look at.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `neutral` | 84 | 42% |
| `hot_take` | 83 | 41.5% |
| `stat_backed` | 33 | 16.5% |
| **Total** | **200** | 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* "Doesn't need to be. He's a high impact player on a $3m contract. You don't give those away. Depth and versatility is what is needed"
>
> *Could have been:* `stat_backed` or `hot_take`
>
> *I chose, because:* `hot_take`. The $3m is a real number you could look up, so at first I wanted to call it stat_backed. But the salary isn't the proof here. The actual claim is that he's "high impact," and nothing in the post backs that up. The contract number just explains why he's cheap, not why he's good.

**2.**
> *The post:* "These 2 were actually going to be my mentions. For the Cavs: Mario Hezonja hasn't played an NBA game since August 2020 and he has a real chance to be the Cavs first big off the bench this season. He put up 20 points in the wine & gold scrimmage. Then the back-up PG battle is between rookie Meleek Thomas and 1 year pro Tyrese Proctor..."
>
> *Could have been:* `stat_backed` or `neutral`
>
> *I chose, because:* `stat_backed`. A lot of this reads like news about who's fighting for minutes, which pushed me toward neutral. What tipped it is that the poster does take a position, that Hezonja has a real chance to be the first big off the bench, and the 20 points in the scrimmage is the evidence for it. My rule says stats count when they support a take, and here they do.

**3.**
> *The post:* "For a guy that played 54 games last season at 9 minutes per game, plus 10 playoff games at 7 minutes per game. He also played 5 minutes this game and then got injured. I just really don't know how you stop that from happening, except reverting back to the old style of play..."
>
> *Could have been:* `stat_backed` or `neutral`
>
> *I chose, because:* `neutral`. This one is full of numbers, which is exactly the trap my decision rule is for. The stats aren't being used to say the player is good or bad. They're just describing how little he played before getting hurt, and the rest of the post is about how the modern game causes injuries like this. No position on the player, so it's neutral even with all the stats.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128, seed 42. I trained on my laptop's CPU (torch 2.2.2).

**Anything I changed from the defaults, and why:** Nothing. I left every setting at the default because this is my first run and I wanted a baseline to compare against next unit before changing anything.

**Split sizes:** 139 train / 31 validation / 30 test.

| Label | Train | Val | Test |
|---|---|---|---|
| `hot_take` | 58 | 13 | 12 |
| `neutral` | 58 | 13 | 13 |
| `stat_backed` | 23 | 5 | 5 |

stat_backed only has 5 posts in the test set, which is under the 8 or so you'd want. That means every single stat_backed post changes its F1 by a lot, so I expect that number to jump around between seeds. On this first run the model got all 5 of them wrong (F1 0.00), which lines up with what I worried about when I was building the dataset.


---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* I asked Claude to help me design my labels. My first idea was positive / negative / neutral, plus a label for posts backed by stats.
- *What came back:* Claude pointed out that this mixes two different things. Positive and negative are about how someone feels, while "backed by stats" is about whether they give evidence, so one post could fit two labels at once. It suggested picking one axis and offered an evidence-based set: stat_backed, hot_take, neutral.
- *What I changed:* I dropped the sentiment labels and went with the evidence-based set. That's also why my hardest boundary ended up being stat_backed vs. neutral, since a post can be full of numbers without actually arguing anything.

**Moment 2**

- *What I asked for:* I wrote my own draft of the five acceptance criteria and asked Claude to fix it.
- *What came back:* Claude caught that my draft still talked about four labels and sentiment, used a two-person consistency check I don't actually have, and had a confidence target the notebook doesn't measure. It rewrote all five so each one uses a number the notebook really reports (accuracy, per-label F1, predicted share, agreement with the staff set, and most-sure vs. least-sure third).
- *What I changed:* I kept the structure of my original five areas but used the rewritten versions, so every target is something I can actually check next unit across all three seeds.

**Pre-labelling disclosure:** 180 of my 200 rows were pre-labelled by Claude using my label definitions and decision rule, and they're marked `pre-labelled, checked` in the note column. I read those rows and corrected the labels I disagreed with. The other 20 rows are marked `cold` and I labelled them myself with no AI help.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
