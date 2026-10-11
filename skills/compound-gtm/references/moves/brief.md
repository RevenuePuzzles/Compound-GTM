# brief — plan a motion so it can teach you something

A motion is any campaign, launch, ABM push, event, partner push or strategic deal. The brief makes it testable: what we expect, how we'll know, and when we'll stop.

## Use when

- "Plan a campaign", "we're launching X", "ABM for these 20 accounts", "deal strategy for Y".
- Before `play`, `sequence` or `asset` for anything bigger than a single email.

## Reads

`ICP.md`, `POSITIONING.md`, `PLAYS.md` (has something like this been run before? what happened?), `COMPANY.md` (capacity, offer).

## Steps

1. **Check the library first.** If `PLAYS.md` has a similar play, start from it and its results. If it was retired, say why and what is different this time.
2. **Write the brief:**
   - **Goal** — one business outcome (meetings, pipeline, renewals, a signed deal), not activity.
   - **Audience** — the segment and situation from `ICP.md`, list size, how the list is built.
   - **Hypothesis** — "We believe [audience] will [respond] because [reason], as shown by [evidence or 'untested']."
   - **Message** — which pillar from `POSITIONING.md`, which proof from `PROOF.md`.
   - **Channels and steps** — high level; `play` designs the detail.
   - **Success criterion** — a number, a denominator and a date: "≥ 8 qualified meetings from 250 contacts by 30 Nov".
   - **Kill criterion** — the result that means stop or change: "< 2 positive replies after first 100 contacts".
   - **What we'll learn either way** — the question this motion answers.
   - **Owner, budget, capacity, dates.**
   - **Risks** — reputation, deliverability, data, legal (consent rules for the regions targeted).
3. **Size it honestly.** If the list is too small for the success criterion to mean anything, say so and adjust the goal to learning.
4. **Create the motion folder** `motions/<yyyy-mm>-<slug>/` with `BRIEF.md` when a home exists (with a shell: `python scripts/create_home.py <home> --motion "<name>"`).

## Output

`BRIEF.md`, plus the one assumption most likely to break the motion.

## Could compound

Usually nothing yet. The brief is what `results` and `retro` will compare reality against.
