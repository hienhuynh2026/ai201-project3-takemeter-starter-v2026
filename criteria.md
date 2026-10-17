# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
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
form to fill in — a criterion that fits none of them is fine if it names a
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
  Pick with that in mind — it is stricter than it first sounds.

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
     UNIT 6 — read this before you change anything above.

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
