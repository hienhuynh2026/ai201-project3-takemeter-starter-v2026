# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first**: setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder**, in VS Code, or with
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

**Staff set disclosure:** For the Milestone 3 agreement check, I labelled 11 of the 30 staff posts myself (posts 1 to 10 and post 19). With my instructor's OK, Claude labelled the other 19 (posts 11 to 18 and 20 to 30) using the staff taxonomy in `data/staff_taxonomy.md`. That matters for how much the agreement rate says about me, and I come back to it in the Agreement Report.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.400 | 0.533 | +0.133 |
| Macro F1 | 0.190 | 0.384 | +0.193 |
| F1: `hot_take` | 0.571 | 0.606 | +0.035 |
| F1: `neutral` | 0.000 | 0.545 | +0.545 |
| F1: `stat_backed` | 0.000 | 0.000 | +0.000 |

The baseline is `facebook/bart-large-mnli` run zero-shot with my definitions from `label_definitions.txt`, scored on the same 30 held-out posts as my trained model (seed 42).

**What I predicted before I looked:**
To be upfront, I had already seen my trained model's seed 42 numbers at the end of unit 5, so this wasn't a blind guess. My prediction was that the trained model would beat the baseline mostly on `neutral`, because a general model reading my definitions would see opinions everywhere on a sports forum, and that neither model would get `stat_backed` right.

**What the gap actually means:**
The baseline called all 30 posts `hot_take`. That's why it gets 0.40 accuracy (12 of the 30 really are hot takes) and a 0 on both other labels. So the whole gap comes from one place: my trained model learned to recognize some `neutral` posts (F1 went from 0 to 0.55) and the baseline never did. On `hot_take` the two are basically tied, and on `stat_backed` fine-tuning added nothing at all. Both models scored 0. My training taught the model one of my two harder labels but not the other.



---

## Run Log: Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

All three runs were on my laptop's CPU (Intel i5, torch 2.2.2), default settings: 3 epochs, learning rate 2e-5, batch size 16, max length 128.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.65 | 0.533 | 0.600 | 0.633 | MISSED |
| 2. Lowest per-label F1 | ≥ 0.55 | 0.000 (stat_backed) | 0.000 (stat_backed) | 0.000 (stat_backed) | MISSED |
| 3. Biggest gap between predicted and true share | ≤ 10 pts | 30 pts (hot_take) | 17 pts (stat_backed) | 23 pts (hot_take) | MISSED |
| 4. Agreement with staff labels | ≥ 70% | 100% (30 of 30), one number for all seeds | | | MET |
| 5. Most-confident third minus least-confident third | ≥ +0.15 | +0.80 (0.9 vs 0.1) | +0.20 (0.6 vs 0.4) | -0.30 (0.5 vs 0.8) | MISSED |

The full spread across seeds:

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.533 | 0.600 | 0.633 | 0.100 |
| Macro F1 | 0.384 | 0.436 | 0.465 | 0.081 |
| F1: `hot_take` | 0.606 | 0.593 | 0.645 | 0.053 |
| F1: `neutral` | 0.545 | 0.714 | 0.750 | 0.205 |
| F1: `stat_backed` | 0.000 | 0.000 | 0.000 | 0.000 |

Accuracy moved 10 points just from changing the seed, which is a lot. It tells me 30 test posts isn't enough to pin down a single number, and `neutral` F1 swinging by 0.2 is the same problem.

### Confusion matrix

Seed 42:

| true \ predicted | hot_take | neutral | stat_backed |
|---|---|---|---|
| **hot_take** | 10 | 2 | 0 |
| **neutral** | 7 | 6 | 0 |
| **stat_backed** | 4 | 1 | 0 |

**My biggest off-diagonal number, and what it means:**
7 real `neutral` posts got called `hot_take`, and only 2 went the other way, so the model leans hard toward `hot_take` whenever a post isn't clearly a question or news. The second thing that jumps out is the whole `stat_backed` row: the model never predicted `stat_backed` on any seed, and 4 or 5 of those 5 posts became `hot_take` every time, which means it treats a stat-backed take as just a take and ignores the numbers.



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.65 on all three seeds | MISSED | Best seed was 0.633, worst was 0.533. None of the three got there. |
| 2 | Every label F1 | ≥ 0.55 on all three seeds | MISSED | `stat_backed` was 0.000 on every seed. `hot_take` and `neutral` cleared 0.55 on all three. |
| 3 | Balance | Every label's predicted share within 10 pts of its true share | MISSED | `stat_backed` is 17% of the test set and got 0% of predictions on every seed, so it fails by 17 points no matter what. `hot_take` was also over-predicted by 30 and 23 points on seeds 42 and 2024. |
| 4 | Agreement with staff | ≥ 70% (21 of 30) | MET | I matched staff on all 30 posts. It doesn't depend on seeds, so it holds across all three. |
| 5 | Confidence | Most-sure third beats least-sure third by ≥ 0.15 | MISSED | It passed on seeds 42 (+0.80) and 7 (+0.20) but flipped on seed 2024 (-0.30), and the target has to hold on all three. |

**Diagnoses**

**Criterion 2 (stat_backed F1) and criterion 3 (balance): too few examples for a label.** This is the main one, and criteria 1 and 3 mostly fall out of it. `stat_backed` has 33 posts total, which leaves only 23 to train on and 5 to test on. The model never predicted it once across 90 test predictions, and 13 of the 15 `stat_backed` test posts across the three seeds were called `hot_take`. That fits with how my labels work: a stat_backed post is a take that also has numbers in it, so with only 23 examples the model learned the "take" part and never learned that the numbers are supposed to matter. It was also barely trained. Average confidence sat around 0.40 when chance is 0.33, after only 27 training steps.

**Criterion 1 (accuracy): mostly a consequence of the above plus a lopsided `neutral` / `hot_take` boundary.** Losing all 5 `stat_backed` posts caps accuracy at 25 of 30 (0.83) before anything else goes wrong. The rest of the misses are mostly real `neutral` posts called `hot_take` (7 on seed 42, 3 on seed 7, 4 on seed 2024), while far fewer go the other way. That direction is a sign this could be a labelling problem and not just a model problem, and my agreement report is how I check that. Also worth saying honestly: 180 of my 200 labels started as AI pre-labels, so if my `neutral` vs. `hot_take` line drifted, that's one place it could have come from.

**Criterion 5 (confidence): small test set, not a real pattern.** Each "third" is only 10 posts, so one or two posts flip the result. Seed 42 looked great (+0.80) and seed 2024 went backwards (-0.30). With confidence values all bunched around 0.40, the model isn't really separating sure from unsure, and 10 posts per bucket can't show it either way.

**What the agreement report adds:** Less than I hoped. I matched staff on all 30 posts, which says I can apply a written rule the way its authors meant it when the posts are clear. But the staff set came in clean blocks of ten per label and most posts were obvious examples, and an AI labelled 19 of my 30. So it doesn't really test the line that matters for my model, which is `neutral` vs. `hot_take` on NBA posts. I can't use it to rule out a labelling problem behind the 7 `neutral` posts called `hot_take`. What it does make less likely is that I'm sloppy with rules in general, so I still think the `stat_backed` failure is mostly a data size problem and not a labelling one.


---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** 30 / 30 = 100%

**Disagreements**

There weren't any. `agreement.py` found 30 matches and 0 disagreements, so there's nothing to adjudicate or sort into piles.

**Was the set easy, or is my reading of the rule tight?** Mostly easy, I think. Posts 1 to 10 all argue from a number that carries the argument (splits, percentages, a remeasured course), posts 11 to 20 are all flat confident claims, and posts 21 to 30 are all about something that just happened to the writer. Only a handful needed the decision rules:

- **Post 14** ("Times are down about 3% since the shoe rules changed, so obviously the shoes are the whole story") is almost word for word the Rule 1 example, so the 3% is decoration and it's `hot_take`.
- **Posts 17 and 18** have a year ("about 2015") and a pace ("8 minute miles"), but neither number is the reason for the claim, so Rule 1 makes them `hot_take`.
- **Post 27** mentions leaning "about 20 degrees" in the wind, but it's describing how the run felt, not arguing anything, so it's `reaction`.
- **Post 29** (setting every PB in shoes bought in the wrong size) could be read as a quiet jab that shoes don't matter. It's written as a "just realised" moment about the writer, so Rule 2 makes it `reaction`.
- **Posts 5 and 10** are the ones I expected to lose. They argue from one runner and from three runners, which is a tiny sample. But the taxonomy asks whether the fact is load-bearing, not whether it's a good sample, and in both the numbers are the whole argument, so they're `analysis`. Staff agreed.

**What the pattern in my disagreements tells me:**
With no disagreements there's no pattern to read, so I want to be careful not to oversell this. A 100% on a clean set says the staff rules are clear and I didn't apply any of them loosely, so pile (a) is empty. It doesn't tell me much about my own 200 NBA labels. Those have messier boundaries, especially between `neutral` and `hot_take`, and 180 of them started as AI pre-labels. Also, Claude labelled 19 of these 30, so the 100% is partly a measure of the AI applying the rules, not just me. The 11 I did myself (posts 1 to 10 and 19) all matched, and that's the part I can actually claim.


---

## The Improvement

**What I changed:** One training parameter. I raised epochs from 3 to 8 and left everything else the same: same 200 labels, same three seeds, learning rate 2e-5, batch size 16. The change is in the notebook's settings cell with a comment saying why.

**Which diagnosis pointed at it:** The model looked undertrained. With 139 training posts and batch size 16, three epochs is only 27 training steps, and the "before" model's confidence averaged around 0.40 when random guessing is 0.33, so it was close to guessing even when it was right. My first choice would have been adding more `stat_backed` posts, since too few examples is the bigger diagnosis, but I'd already used every RealGM post I collected that fit that label. Training longer was the one change I could make cleanly and test on the same data.

### Run Log: After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.65 | 0.667 | 0.500 | 0.633 | MISSED |
| 2. Lowest per-label F1 | ≥ 0.55 | 0.000 (stat_backed) | 0.000 (stat_backed) | 0.000 (stat_backed) | MISSED |
| 3. Biggest gap between predicted and true share | ≤ 10 pts | 17 pts | 10 pts | 17 pts | MISSED |
| 4. Agreement with staff labels | ≥ 70% | 100% (30 of 30), labels didn't change so same as before | | | MET |
| 5. Most-confident third minus least-confident third | ≥ +0.15 | +0.50 (0.8 vs 0.3) | +0.90 (0.9 vs 0.0) | +0.20 (0.7 vs 0.5) | MET |

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.667 | 0.500 | 0.633 | 0.167 |
| Macro F1 | 0.486 | 0.377 | 0.461 | 0.109 |
| F1: `hot_take` | 0.690 | 0.560 | 0.643 | 0.130 |
| F1: `neutral` | 0.769 | 0.571 | 0.741 | 0.198 |
| F1: `stat_backed` | 0.000 | 0.000 | 0.000 | 0.000 |

**Did it help, and how do I know:**
Only a little, and not on the thing I most needed. The clearest win is confidence: criterion 5 went from MISSED to MET, because the model is now more sure when it's right (about 0.59) than when it's wrong (about 0.50), and the most-confident third beat the least-confident third on all three seeds. It also stopped dumping `neutral` posts into `hot_take` as much. On seed 42 that confusion dropped from 7 posts to 3, and `neutral` F1 went up on two of the three seeds.

But the overall numbers barely moved. Average accuracy across the three seeds went from 0.589 to 0.600, and seed 7 actually got worse (0.600 to 0.500). The spread between seeds got bigger, from 10 points to almost 17, so the gains on seeds 42 and 2024 are smaller than the noise. And `stat_backed` is still 0 on every seed. With more training it finally guessed `stat_backed` twice on seed 7, but both were wrong. So training longer helped the model use the data it had, but it couldn't fix a label it only had 23 examples of.


---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->

**Criterion 2 (every label F1 ≥ 0.55) and criterion 3 (balance).** Both still fail because of `stat_backed`. The fix I'd try next is collecting about 50 more `stat_backed` posts from RealGM, looking specifically for threads where people argue with numbers (contract debates, stat comparisons, injury history). That would roughly double what the model learns from and push the label to around 8 posts in the test set. I stopped here because it means going back to collect and label new posts, which is a bigger job than one change in this unit, and the assignment asked for exactly one fix.

**Criterion 1 (accuracy ≥ 0.65).** It hit 0.667 on one seed but dropped to 0.500 on another. With only 30 test posts, one post is worth 3.3 points of accuracy, so I can't tell a real improvement from a lucky split. More data overall would help the most here too. I'd also want the extra `stat_backed` posts first, since losing all 5 of them every run caps the score.

**Criterion 4 (agreement).** This one is MET, so there's nothing to fix, but the evidence behind it is thinner than 100% sounds. The staff set was easy and an AI labelled 19 of my 30. What I'd actually want is a check on my own data: have a second person label 30 of my NBA posts, especially ones near the `neutral` / `hot_take` line, and see if we agree. That would tell me whether the model's `neutral` to `hot_take` mistakes come from my labels. I stopped here because I don't have a second labeller for my corpus, and it's outside what this unit asked for.

**The gap between what I meant my labels to capture and what the model learned:**
I meant `stat_backed` to mean "a take that is argued with numbers," but the model learned something closer to "has an opinion, so it's `hot_take`," and every seed sent 4 or 5 of the 5 `stat_backed` posts straight into `hot_take`. It learned the difference between having an opinion and not having one pretty well, but it never learned that the numbers in a post are what make it a different kind of post.


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
       [ ] Run Log: Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log: After
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

---

## Capstone

**The Shape**

Shape A, deploy and instrument. Until now TakeMeter was a notebook plus three scripts that each printed to the screen and left nothing behind, so there was no way to look back at what it did. The capstone adds `takemeter.py`, one command that loads the classifier, labels a batch of posts (the 30 held-out posts in `test_split.csv` by default, one post with `--text`, or any CSV with `--input`), and appends a JSON record for every post and every run to `logs/takemeter.jsonl`. Post records carry the timestamp, the input, the predicted label, the score, and how long it took. Run records carry model load time, wall and CPU seconds, and peak memory. Runs that go wrong (an empty post, a missing file, a model that won't load) write a record too, and `python takemeter.py --report` reads the log back into cost and latency numbers.

The classifier it runs is the zero-shot one, `facebook/bart-large-mnli` with my label definitions from `label_definitions.txt` (the same setup `baseline.py` scores). The fine-tuned DistilBERT from Project 3 was trained in memory and never saved (`takemeter_out/` is gitignored and empty), so the zero-shot model is the part of TakeMeter that actually runs from a clean checkout.

Run path is Path B, local with logs. The model needs about 2 GB of RAM, roughly four times a free hosting tier's 512 MB, and nothing in TakeMeter listens on a port anyway. The start command and environment are in [RUNNING.md](RUNNING.md).

**Out of Scope**

- Hosting. No Render, no server, no web page or HTTP endpoint (an endpoint would be a new capability, Shape C, not this).
- Retraining or saving the fine-tuned DistilBERT. The capstone wraps the classifier that already runs; it doesn't build a new one.
- Changing my labels, label definitions, or data. The 0.40 accuracy from Unit 6 is a known weakness, and fixing it would be a different project.

**Instrumentation**

`takemeter.py` writes one JSON object per line to `logs/takemeter.jsonl`, appended by `RunLog.write()`. There are two kinds of record. A `prediction` record is written once per post by `run()`, with `timestamp`, `input` (first 280 characters), `output` (the label), `duration_s`, plus the internal fields that matter for this classifier: `score` and the full `scores` spread across the three labels, the `gold` label when the CSV has one, `correct`, and `status` (`ok`, `rejected`, or `error`). A `run` record is written once per run by `main()`, and it's written even when the run fails, because the run record is the one that says what went wrong (`error_stage`, `error`). It also carries the counts and the cost numbers: `model_load_s`, `inference_s`, `wall_s`, `cpu_s`, `peak_rss_mb`.

The committed log (`logs/takemeter.jsonl`) is from one session on 2026-11-16: ten runs of `python takemeter.py` on the 30 held-out posts, then two bad inputs on purpose. `python takemeter.py --report` reads it back without any new code.

The first three post records from the first run (post 1 is a broadcast schedule the model called a `hot_take`; gold says `neutral`):

```json
{"timestamp": "2026-11-16T02:34:09.826+00:00", "run_id": "17a088bb", "event": "prediction", "input_id": 0, "input": "I like Kyrie on this Dallas team but he doesn't match the timeline. If Dallas gets a decent offer that meshes more with Flagg (a younger player, picks or both) they should move him, imo.", "input_chars": 186, "model": "facebook/bart-large-mnli", "status": "ok", "output": "hot_take", "score": 0.8415, "scores": {"hot_take": 0.8415, "stat_backed": 0.1068, "neutral": 0.0517}, "gold": "hot_take", "correct": true, "duration_s": 6.176}
{"timestamp": "2026-11-16T02:34:11.501+00:00", "run_id": "17a088bb", "event": "prediction", "input_id": 1, "input": "15 free Cavs games with the ol' bunny ears over the airwaves on RESN and 3 more additional Cavs games the same way via NBC National broadcast.", "input_chars": 142, "model": "facebook/bart-large-mnli", "status": "ok", "output": "hot_take", "score": 0.7527, "scores": {"hot_take": 0.7527, "stat_backed": 0.212, "neutral": 0.0354}, "gold": "neutral", "correct": false, "duration_s": 1.674}
{"timestamp": "2026-11-16T02:34:13.049+00:00", "run_id": "17a088bb", "event": "prediction", "input_id": 2, "input": "We'll see how season 2 goes. He was playing with house money last year. Everything was upside. Its not a contract year, but eventually a guard in San Antonio will have to make a decision to embrace the 6th man role, force a trade, or wait to be traded.", "input_chars": 252, "model": "facebook/bart-large-mnli", "status": "ok", "output": "hot_take", "score": 0.7324, "scores": {"hot_take": 0.7324, "stat_backed": 0.1898, "neutral": 0.0778}, "gold": "hot_take", "correct": true, "duration_s": 1.547}
```

The run records for all ten measured runs, one line each:

```json
{"timestamp": "2026-11-16T02:34:49.318+00:00", "run_id": "17a088bb", "event": "run", "status": "ok", "input": "test_split.csv", "model": "facebook/bart-large-mnli", "n_inputs": 30, "n_ok": 30, "n_rejected": 0, "n_error": 0, "model_load_s": 13.853, "inference_s": 45.657, "wall_s": 61.568, "cpu_s": 178.038, "peak_rss_mb": 1751.6, "device": "cpu", "torch_threads": 4, "python": "3.12.15", "torch": "2.2.2", "transformers": "4.57.6", "machine": "Darwin x86_64"}
{"timestamp": "2026-11-16T02:35:43.305+00:00", "run_id": "a0a392bd", "event": "run", "status": "ok", "input": "test_split.csv", "model": "facebook/bart-large-mnli", "n_inputs": 30, "n_ok": 30, "n_rejected": 0, "n_error": 0, "model_load_s": 11.049, "inference_s": 40.306, "wall_s": 52.649, "cpu_s": 169.312, "peak_rss_mb": 1750.3, "device": "cpu", "torch_threads": 4, "python": "3.12.15", "torch": "2.2.2", "transformers": "4.57.6", "machine": "Darwin x86_64"}
{"timestamp": "2026-11-16T02:36:37.711+00:00", "run_id": "540bf26d", "event": "run", "status": "ok", "input": "test_split.csv", "model": "facebook/bart-large-mnli", "n_inputs": 30, "n_ok": 30, "n_rejected": 0, "n_error": 0, "model_load_s": 8.199, "inference_s": 44.372, "wall_s": 53.526, "cpu_s": 175.862, "peak_rss_mb": 1750.1, "device": "cpu", "torch_threads": 4, "python": "3.12.15", "torch": "2.2.2", "transformers": "4.57.6", "machine": "Darwin x86_64"}
{"timestamp": "2026-11-16T02:37:34.138+00:00", "run_id": "69aa3f26", "event": "run", "status": "ok", "input": "test_split.csv", "model": "facebook/bart-large-mnli", "n_inputs": 30, "n_ok": 30, "n_rejected": 0, "n_error": 0, "model_load_s": 9.282, "inference_s": 45.133, "wall_s": 55.478, "cpu_s": 181.279, "peak_rss_mb": 1752.2, "device": "cpu", "torch_threads": 4, "python": "3.12.15", "torch": "2.2.2", "transformers": "4.57.6", "machine": "Darwin x86_64"}
{"timestamp": "2026-11-16T02:38:30.820+00:00", "run_id": "7b57d8e3", "event": "run", "status": "ok", "input": "test_split.csv", "model": "facebook/bart-large-mnli", "n_inputs": 30, "n_ok": 30, "n_rejected": 0, "n_error": 0, "model_load_s": 8.519, "inference_s": 46.215, "wall_s": 55.759, "cpu_s": 184.194, "peak_rss_mb": 1750.8, "device": "cpu", "torch_threads": 4, "python": "3.12.15", "torch": "2.2.2", "transformers": "4.57.6", "machine": "Darwin x86_64"}
{"timestamp": "2026-11-16T02:39:23.521+00:00", "run_id": "78af78c0", "event": "run", "status": "ok", "input": "test_split.csv", "model": "facebook/bart-large-mnli", "n_inputs": 30, "n_ok": 30, "n_rejected": 0, "n_error": 0, "model_load_s": 8.369, "inference_s": 42.046, "wall_s": 51.699, "cpu_s": 172.701, "peak_rss_mb": 1750.1, "device": "cpu", "torch_threads": 4, "python": "3.12.15", "torch": "2.2.2", "transformers": "4.57.6", "machine": "Darwin x86_64"}
{"timestamp": "2026-11-16T02:40:15.938+00:00", "run_id": "c356d5a9", "event": "run", "status": "ok", "input": "test_split.csv", "model": "facebook/bart-large-mnli", "n_inputs": 30, "n_ok": 30, "n_rejected": 0, "n_error": 0, "model_load_s": 8.511, "inference_s": 42.001, "wall_s": 51.442, "cpu_s": 174.128, "peak_rss_mb": 1752.4, "device": "cpu", "torch_threads": 4, "python": "3.12.15", "torch": "2.2.2", "transformers": "4.57.6", "machine": "Darwin x86_64"}
{"timestamp": "2026-11-16T02:41:09.692+00:00", "run_id": "86b20dbd", "event": "run", "status": "ok", "input": "test_split.csv", "model": "facebook/bart-large-mnli", "n_inputs": 30, "n_ok": 30, "n_rejected": 0, "n_error": 0, "model_load_s": 9.907, "inference_s": 41.526, "wall_s": 52.749, "cpu_s": 173.963, "peak_rss_mb": 1751.5, "device": "cpu", "torch_threads": 4, "python": "3.12.15", "torch": "2.2.2", "transformers": "4.57.6", "machine": "Darwin x86_64"}
{"timestamp": "2026-11-16T02:42:05.701+00:00", "run_id": "3b2955ec", "event": "run", "status": "ok", "input": "test_split.csv", "model": "facebook/bart-large-mnli", "n_inputs": 30, "n_ok": 30, "n_rejected": 0, "n_error": 0, "model_load_s": 9.662, "inference_s": 44.014, "wall_s": 55.009, "cpu_s": 177.724, "peak_rss_mb": 1750.5, "device": "cpu", "torch_threads": 4, "python": "3.12.15", "torch": "2.2.2", "transformers": "4.57.6", "machine": "Darwin x86_64"}
{"timestamp": "2026-11-16T02:43:05.549+00:00", "run_id": "4068410d", "event": "run", "status": "ok", "input": "test_split.csv", "model": "facebook/bart-large-mnli", "n_inputs": 30, "n_ok": 30, "n_rejected": 0, "n_error": 0, "model_load_s": 11.964, "inference_s": 45.459, "wall_s": 58.829, "cpu_s": 183.796, "peak_rss_mb": 1750.0, "device": "cpu", "torch_threads": 4, "python": "3.12.15", "torch": "2.2.2", "transformers": "4.57.6", "machine": "Darwin x86_64"}
```

The bad path. A file that doesn't exist (`--input posts_that_dont_exist.csv`) fails at `read_input` and the run record says so. A blank post (`--text "   "`) is rejected without loading the model, so it gets a `rejected` prediction record and a run record with `n_rejected: 1`:

```json
{"timestamp": "2026-11-16T02:43:12.467+00:00", "run_id": "736ed268", "event": "run", "status": "error", "error_stage": "read_input", "error": "No file at posts_that_dont_exist.csv", "input": "posts_that_dont_exist.csv", "model": "facebook/bart-large-mnli", "n_inputs": 0, "n_ok": 0, "n_rejected": 0, "n_error": 0, "model_load_s": null, "inference_s": 0.0, "wall_s": 5.836, "cpu_s": 5.709, "peak_rss_mb": 220.5, "device": "cpu", "torch_threads": 4, "python": "3.12.15", "torch": "2.2.2", "transformers": "4.57.6", "machine": "Darwin x86_64"}
{"timestamp": "2026-11-16T02:43:12.997+00:00", "run_id": "d2b44fc8", "event": "prediction", "input_id": 0, "input": "", "input_chars": 0, "model": "facebook/bart-large-mnli", "status": "rejected", "error": "empty post", "output": null, "score": null, "gold": null, "duration_s": 0.0}
{"timestamp": "2026-11-16T02:43:16.118+00:00", "run_id": "d2b44fc8", "event": "run", "status": "ok", "input": "--text", "model": "facebook/bart-large-mnli", "n_inputs": 1, "n_ok": 0, "n_rejected": 1, "n_error": 0, "model_load_s": null, "inference_s": 0.0, "wall_s": 3.12, "cpu_s": 3.779, "peak_rss_mb": 175.8, "device": "cpu", "torch_threads": 4, "python": "3.12.15", "torch": "2.2.2", "transformers": "4.57.6", "machine": "Darwin x86_64"}
```

Two things in these records that I wouldn't have known without the log. The first post of every run is slow (6.18 s in run `17a088bb` against a median of 1.38 s), which is torch warming up, not that post being hard. And the bad-path runs are slower than they should be: the missing-file run took 5.8 s to report a typo, and the blank post's prediction record is stamped 02:43:12.997 while its run record is stamped 02:43:16.118, so 3.1 s went by after the work was already done.

**What It Costs**

TakeMeter makes no API calls, so the cost is compute time on my own machine: an Intel Core i5-8257U (4 cores, torch using 4 threads), 16 GB RAM, macOS, Python 3.12.15, CPU only, model already in the Hugging Face cache.

How it was measured: `main()` takes `time.perf_counter()` (wall) and `time.process_time()` (CPU, summed across threads) at the start of the run and again when it writes the run record, and `resource.getrusage()` for peak memory. Model load and per-post inference are timed separately inside `run()`. I ran `python takemeter.py` ten times back to back with nothing else running, then `python takemeter.py --report --last 12` averaged the run records:

```
Successful runs on test_split.csv: 10 (posts per run: [30])
  wall per run           mean    54.87s  min    51.44s  max    61.57s
  CPU per run            mean   177.10s  min   169.31s  max   184.19s
  model load             mean     9.93s  min     8.20s  max    13.85s
  inference total        mean    43.67s  min    40.31s  max    46.22s
  peak RSS               mean  1750.95 MB  min  1750.00 MB  max  1752.40 MB
  per-post latency       p50 1.38s  p95 2.48s  max 6.18s  (n=300)
```

So one run of TakeMeter on 30 posts costs **54.9 s of wall time, 177.1 s of CPU time, and 1.75 GB of memory at peak**. Per post that's about 1.83 s of wall time (54.87 / 30) or 1.46 s if you leave out the one-time model load (43.67 / 30). CPU time is about 3.2 times wall time because the four cores work in parallel. Model load is 18% of the run (9.93 / 54.87); the rest is inference, which runs one forward pass per label, three per post.

**Run Log and Verdicts**

I ran `python capstone_trials.py --trials 3 --log logs/trials_before.jsonl --out trials_before.json`. Each trial runs `takemeter.py` as a fresh process, the same way I would by hand: one normal run on `test_split.csv` (criteria 1, 4 and 5), three bad inputs (criterion 2) and the 10-row file with 3 blank rows (criterion 3). No code changed between trials. A criterion is MET only if it held on all three.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every post leaves a complete record | 30/30 complete prediction records and 1 run record with n_ok 30 | 30/30, 1 run record | 30/30, 1 run record | 30/30, 1 run record | MET |
| 2. A bad input fails fast and says why | 3/3 bad inputs named, right exit code, under 2.0 s | 0/3 (named and right exit on all 3, but 6.29 s, 4.36 s, 4.70 s) | 0/3 (5.21 s, 3.26 s, 2.60 s) | 0/3 (5.68 s, 4.29 s, 2.50 s) | MISSED |
| 3. One blank row doesn't sink a batch | 7 ok, 3 rejected, run ok, exit 0 | 7 ok, 3 rejected, ok, exit 0 | 7 ok, 3 rejected, ok, exit 0 | 7 ok, 3 rejected, ok, exit 0 | MET |
| 4. A 30-post run stays inside its measured budget | wall ≤ 60.0 s, p95 ≤ 3.0 s, peak ≤ 1800 MB | 64.57 s, 2.85 s, 1751.9 MB | 59.73 s, 2.91 s, 1749.5 MB | 51.27 s, 2.54 s, 1748.5 MB | MISSED |
| 5. The labels are worth reading | at least 15/30 correct | 12/30 | 12/30 | 12/30 | MISSED |

The times in row 2 are measured from the shell (missing file, no text column, empty post, in that order). The raw log lines behind each row are below. Every line in `logs/trials_before.jsonl` is written by `RunLog.write()` in `takemeter.py`; the function named is the one that calls it.

Criterion 1, run 1. A prediction record from `run()` in `takemeter.py` (one of 30) and the run record from `main()` in `takemeter.py`:

```json
{"timestamp": "2026-11-16T02:46:23.400+00:00", "run_id": "3cd343a0", "event": "prediction", "input_id": 0, "input": "I like Kyrie on this Dallas team but he doesn't match the timeline. If Dallas gets a decent offer that meshes more with Flagg (a younger player, picks or both) they should move him, imo.", "input_chars": 186, "model": "facebook/bart-large-mnli", "status": "ok", "output": "hot_take", "score": 0.8415, "scores": {"hot_take": 0.8415, "stat_backed": 0.1068, "neutral": 0.0517}, "gold": "hot_take", "correct": true, "duration_s": 1.906}
{"timestamp": "2026-11-16T02:47:15.265+00:00", "run_id": "3cd343a0", "event": "run", "status": "ok", "input": "test_split.csv", "model": "facebook/bart-large-mnli", "n_inputs": 30, "n_ok": 30, "n_rejected": 0, "n_error": 0, "model_load_s": 9.681, "inference_s": 53.762, "wall_s": 64.574, "cpu_s": 189.31, "peak_rss_mb": 1751.9, "device": "cpu", "torch_threads": 4, "python": "3.12.15", "torch": "2.2.2", "transformers": "4.57.6", "machine": "Darwin x86_64"}
```

Criterion 2, run 1. The run records from `main()` in `takemeter.py` for the missing file and the CSV with no text column, then the rejected prediction from `run()` and the run record from `main()` for `--text ""`. Every failure is named correctly. What misses is the time: `wall_s` is 5.6 s, 3.9 s and 4.3 s, and the shell times that `trial()` in `capstone_trials.py` measured around the whole process (in `trials_before.json`) are 6.29 s, 4.36 s and 4.70 s:

```json
{"timestamp": "2026-11-16T02:47:22.113+00:00", "run_id": "dcc900ad", "event": "run", "status": "error", "error_stage": "read_input", "error": "No file at capstone_tests/this_file_does_not_exist.csv", "input": "capstone_tests/this_file_does_not_exist.csv", "model": "facebook/bart-large-mnli", "n_inputs": 0, "n_ok": 0, "n_rejected": 0, "n_error": 0, "model_load_s": null, "inference_s": 0.0, "wall_s": 5.625, "cpu_s": 5.276, "peak_rss_mb": 220.6, "device": "cpu", "torch_threads": 4, "python": "3.12.15", "torch": "2.2.2", "transformers": "4.57.6", "machine": "Darwin x86_64"}
{"timestamp": "2026-11-16T02:47:26.536+00:00", "run_id": "7c91ea88", "event": "run", "status": "error", "error_stage": "read_input", "error": "capstone_tests/no_text_column.csv has no 'text' column (found: post, label)", "input": "capstone_tests/no_text_column.csv", "model": "facebook/bart-large-mnli", "n_inputs": 0, "n_ok": 0, "n_rejected": 0, "n_error": 0, "model_load_s": null, "inference_s": 0.0, "wall_s": 3.861, "cpu_s": 4.615, "peak_rss_mb": 221.2, "device": "cpu", "torch_threads": 4, "python": "3.12.15", "torch": "2.2.2", "transformers": "4.57.6", "machine": "Darwin x86_64"}
{"timestamp": "2026-11-16T02:47:27.005+00:00", "run_id": "615683c1", "event": "prediction", "input_id": 0, "input": "", "input_chars": 0, "model": "facebook/bart-large-mnli", "status": "rejected", "error": "empty post", "output": null, "score": null, "gold": null, "duration_s": 0.0}
{"timestamp": "2026-11-16T02:47:47.475+00:00", "run_id": "615683c1", "event": "run", "status": "ok", "input": "--text", "model": "facebook/bart-large-mnli", "n_inputs": 1, "n_ok": 0, "n_rejected": 1, "n_error": 0, "model_load_s": null, "inference_s": 0.0, "wall_s": 4.303, "cpu_s": 3.126, "peak_rss_mb": 176.1, "device": "cpu", "torch_threads": 4, "python": "3.12.15", "torch": "2.2.2", "transformers": "4.57.6", "machine": "Darwin x86_64"}
```

Criterion 3, run 1. The three rejected prediction records from `run()` in `takemeter.py` (rows 2, 6 and 9 are the blank, spaces-only and tab-only rows) and the run record from `main()`:

```json
{"timestamp": "2026-11-16T02:48:21.940+00:00", "run_id": "3b0a520f", "event": "prediction", "input_id": 2, "input": "", "input_chars": 0, "model": "facebook/bart-large-mnli", "status": "rejected", "error": "empty post", "output": null, "score": null, "gold": "neutral", "duration_s": 0.0}
{"timestamp": "2026-11-16T02:48:34.024+00:00", "run_id": "3b0a520f", "event": "prediction", "input_id": 6, "input": "", "input_chars": 0, "model": "facebook/bart-large-mnli", "status": "rejected", "error": "empty post", "output": null, "score": null, "gold": "hot_take", "duration_s": 0.0}
{"timestamp": "2026-11-16T02:49:14.545+00:00", "run_id": "3b0a520f", "event": "prediction", "input_id": 9, "input": "", "input_chars": 0, "model": "facebook/bart-large-mnli", "status": "rejected", "error": "empty post", "output": null, "score": null, "gold": "neutral", "duration_s": 0.0}
{"timestamp": "2026-11-16T02:49:14.545+00:00", "run_id": "3b0a520f", "event": "run", "status": "ok", "input": "capstone_tests/mixed_blank.csv", "model": "facebook/bart-large-mnli", "n_inputs": 10, "n_ok": 7, "n_rejected": 3, "n_error": 0, "model_load_s": 18.827, "inference_s": 38.378, "wall_s": 58.254, "cpu_s": 100.105, "peak_rss_mb": 1739.9, "device": "cpu", "torch_threads": 4, "python": "3.12.15", "torch": "2.2.2", "transformers": "4.57.6", "machine": "Darwin x86_64"}
```

Criterion 4. The run record from `main()` in `takemeter.py` for run 1 is the one under criterion 1: `"wall_s": 64.574` is over the 60.0 s limit, while p95 (2.85 s, computed by `trial()` in `capstone_trials.py` from the 30 `duration_s` values) and `"peak_rss_mb": 1751.9` are inside theirs. Runs 2 and 3 were inside on all three (`"wall_s": 59.726` and `"wall_s": 51.271`).

Criterion 5. `trial()` in `capstone_trials.py` counts `"correct": true` across the 30 prediction records that `run()` in `takemeter.py` wrote. It came to 12 on all three runs, the same 12 posts each time, because the model is deterministic on CPU. 12/30 is exactly the zero-shot baseline from Project 3.

One thing in these lines looks wrong and isn't. The empty-post run's prediction is stamped 02:47:27.005 and its run record 02:47:47.475, 20 s apart, but `wall_s` says 4.3 s. The Mac's power log (`pmset -g log`) shows the lid closing at 02:47:24 UTC and the machine sleeping until 02:47:47. `timestamp` comes from the wall clock, while `wall_s` comes from `time.perf_counter()`, which on macOS doesn't count time asleep. So both are right: 4.3 s of work, with 20 s of real time around it. The same log shows the Mac on battery at 33% until that moment, which matters for criterion 4 below.

No criterion needed revising. All five could be measured from the log as written, so every target above is the original one.

**The Improvement**

What missed, where, and why:

- **Criterion 2 (bad input fails fast).** Stage: writing the run record at the end of `main()` in `takemeter.py`, after the run had already failed or finished. Mechanism: `main()` ran `import torch` and `import transformers` unconditionally, only to put two version strings and a thread count into the run record. Importing those two packages costs 4.0 s on this machine (`time python -c "import torch, transformers"`: 4.042 s total). A run that never loaded the model was paying for it anyway. The failure was always named correctly; only the clock missed.
- **Criterion 4 (30-post budget).** Stage: inference in `run()`. Run 1 spent 53.8 s on inference, against 46.2 s and 42.7 s in runs 2 and 3. Mechanism: run 1 was the only one on battery, at 33% charge (power log), and the CPU did the same work slower. Runs 2 and 3 passed. Nothing in the code caused this miss.
- **Criterion 5 (labels worth reading).** Stage: classification in `run()`. Mechanism: the zero-shot model labels every one of the 30 posts `hot_take`. The 12 correct are exactly the 12 posts whose gold label is `hot_take`; all 13 `neutral` and 5 `stat_backed` posts are wrong. The model is reading `"This post is a confident opinion or prediction..."` as the most entailed hypothesis for nearly any sports post. It's a constant classifier wearing a model's clothes.

The one fix, for criterion 2: `main()` now reads the torch and transformers versions with `importlib.metadata.version()`, which reads the installed package's metadata without importing it, and it only asks torch for its thread count if torch is already in `sys.modules` (meaning the model was loaded this run). That's an 8-line change in `takemeter.py`. Then I re-ran all five criteria three times with `python capstone_trials.py --trials 3 --log logs/trials_after.jsonl --out trials_after.json`, with the lid open and the Mac on AC power.

Before the fix (`trials_before.json`):

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every post leaves a complete record | 30/30 complete prediction records and 1 run record with n_ok 30 | 30/30, 1 run record | 30/30, 1 run record | 30/30, 1 run record | MET |
| 2. A bad input fails fast and says why | 3/3 bad inputs named, right exit code, under 2.0 s | 0/3 (6.29 s, 4.36 s, 4.70 s) | 0/3 (5.21 s, 3.26 s, 2.60 s) | 0/3 (5.68 s, 4.29 s, 2.50 s) | MISSED |
| 3. One blank row doesn't sink a batch | 7 ok, 3 rejected, run ok, exit 0 | 7 ok, 3 rejected, ok, exit 0 | 7 ok, 3 rejected, ok, exit 0 | 7 ok, 3 rejected, ok, exit 0 | MET |
| 4. A 30-post run stays inside its measured budget | wall ≤ 60.0 s, p95 ≤ 3.0 s, peak ≤ 1800 MB | 64.57 s, 2.85 s, 1751.9 MB | 59.73 s, 2.91 s, 1749.5 MB | 51.27 s, 2.54 s, 1748.5 MB | MISSED |
| 5. The labels are worth reading | at least 15/30 correct | 12/30 | 12/30 | 12/30 | MISSED |

After the fix (`trials_after.json`):

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every post leaves a complete record | 30/30 complete prediction records and 1 run record with n_ok 30 | 30/30, 1 run record | 30/30, 1 run record | 30/30, 1 run record | MET |
| 2. A bad input fails fast and says why | 3/3 bad inputs named, right exit code, under 2.0 s | 3/3 (0.88 s, 0.82 s, 0.13 s) | 3/3 (1.02 s, 0.84 s, 0.15 s) | 3/3 (0.85 s, 0.82 s, 0.14 s) | MET |
| 3. One blank row doesn't sink a batch | 7 ok, 3 rejected, run ok, exit 0 | 7 ok, 3 rejected, ok, exit 0 | 7 ok, 3 rejected, ok, exit 0 | 7 ok, 3 rejected, ok, exit 0 | MET |
| 4. A 30-post run stays inside its measured budget | wall ≤ 60.0 s, p95 ≤ 3.0 s, peak ≤ 1800 MB | 41.72 s, 1.94 s, 1751.6 MB | 44.20 s, 1.80 s, 1750.3 MB | 44.54 s, 1.76 s, 1748.8 MB | MET |
| 5. The labels are worth reading | at least 15/30 correct | 12/30 | 12/30 | 12/30 | MISSED |

The missing-file run record from `main()` in `takemeter.py`, after the fix, next to the 5.625 s one above:

```json
{"timestamp": "2026-11-16T02:54:03.470+00:00", "run_id": "04d47883", "event": "run", "status": "error", "error_stage": "read_input", "error": "No file at capstone_tests/this_file_does_not_exist.csv", "input": "capstone_tests/this_file_does_not_exist.csv", "model": "facebook/bart-large-mnli", "n_inputs": 0, "n_ok": 0, "n_rejected": 0, "n_error": 0, "model_load_s": null, "inference_s": 0.0, "wall_s": 0.653, "cpu_s": 1.388, "peak_rss_mb": 77.7, "device": "cpu", "torch_threads": null, "python": "3.12.15", "torch": "2.2.2", "transformers": "4.57.6", "machine": "Darwin x86_64"}
```

What the fix actually did. Criterion 2 went from 0/9 to 9/9 bad inputs inside the limit. A typo in a file name now costs 0.65 s instead of 5.6 s, and peak memory on that path dropped from 221 MB to 78 MB because torch never loads. The 0.6 s that's left is mostly importing pandas to read the CSV. The empty post is down to 0.001 s logged and 0.14 s from the shell, which is basically Python starting up.

What it didn't do, even though the table makes it look that way. Criterion 4 flipped to MET, but the fix had nothing to do with it. On a normal run the model loads, torch is already imported, and the new code takes the same path the old code did. The 30-post runs got faster (41.7 to 44.5 s, against 51.3 to 64.6 s before and a 54.9 s average in Milestone 3) because the Mac was plugged in with the lid open this time, not because of anything I changed. I'm reporting criterion 4 as MET because it held on three trials, but I wouldn't trust it on battery. It's a real result about the machine, not an improvement to TakeMeter.

Trade-offs. A run that fails before loading the model now logs `"torch_threads": null` instead of 4, so that field only means something on runs that classified posts. And `importlib.metadata` reports what's installed, not what got imported; if two copies of torch were on the path those could differ. Neither seems likely to matter here, and both are visible in the log if they ever do.
