---
name: compound-gtm
description: Context-first go-to-market toolbox where every campaign, sequence, deal and launch makes the next one easier. Keeps a GTM home (ICP, positioning, proof ledger, play library, voice, motions) and runs Plan → Run → Review → Compound, grading every claim by evidence. Use whenever someone works on B2B go-to-market — ICP or personas, why-now triggers, positioning, offers, proof or case studies, outbound sequences, landing pages or one-pagers, discovery prep, campaign or ABM plays, reviewing copy as a buyer, CFO, competitor or buying committee, reading results, win/loss, retros, or "remember what worked". Also on Polish phrasings ("ICP", "pozycjonowanie", "sekwencja", "kampania", "co zadziałało", "win/loss"). Not for CRM data entry or pipeline hygiene (use a CRM skill) or one-off writing unrelated to selling.
---

# Compound GTM

Most GTM work is forgotten the week after it ships. The replies, objections, lost-deal reasons and conversion numbers end up in Slack threads, CRM notes and people's heads, so the next campaign starts from zero. Compound GTM keeps one **GTM home** — a small set of plain Markdown files — and ends every motion by writing what was learned back into it, graded by how much evidence stands behind it.

Built by Emil Krzemiński · [Revenue Puzzles](https://revenuepuzzles.com/?utm_source=github&utm_medium=skill&utm_campaign=compound-gtm). Inspired by Every's Compound Writing (MIT).

## The loop

```
PLAN  →  RUN  →  REVIEW  →  COMPOUND
brief    play      results    write lessons back into the GTM home
         sequence  win/loss   (ICP · positioning · proof · plays · voice)
         asset     retro
```

The loop is a map, not a gate. Jump in wherever the person is. The one non-negotiable: substantial work ends by offering the **compound** step.

## Before any move

1. Read `references/evidence.md` — evidence levels, permission tags, honest numbers. Every move uses them.
2. Read `references/context-contract.md` whenever a GTM home exists or anything will be written. For a quick one-off review with no home, its "Write safety" section is enough.
3. Locate the GTM home (see "Find the starting point"). Load only the files the move needs.

## Find the starting point

- **They brought material** (a draft, call notes, a CSV of results, a deck, a URL): do the work on it now. Do not block on setup. Offer to start a GTM home afterwards if it would help future work.
- **A GTM home exists** (look for `ICP.md`, `POSITIONING.md`, `PLAYS.md` together, or a folder the person names): load it and route.
- **Nothing exists and there is nothing to work on**: explain in two sentences why one GTM home helps (future campaigns start from what is already known instead of re-explaining the company), ask where it should live, then run `setup` → `onboard`.

Never create files until the destination is explicit or safely resolved. In claude.ai with no file system, keep the home as Markdown in the conversation or an artifact and say so.

## Route by outcome

Pick the smallest route. Load the move file from `references/moves/` before running it.

| The person wants to… | Move |
|---|---|
| Check a draft before it ships ("is this good?", "check this email") | **Review** — see below |
| Turn new call notes or replies into home updates | `signals` (short form) → `compound` |
| Start a GTM home | `setup` → `onboard` |
| Write a lesson, preference or result into the home | `compound` |
| Check whether the home is still trustworthy | `audit` |
| Define or sharpen who buys | `icp` |
| Find why-now moments and the signals that reveal them | `why-now` |
| Mine calls, emails, replies, reviews for buyer language | `signals` |
| Map what buyers do instead of buying from us | `alternatives` |
| Decide what we say and why we win | `positioning` |
| Package what we sell into an offer people can say yes to | `offer` |
| Build, check or anonymise proof and case studies | `proof` |
| Plan a campaign, launch, ABM push or deal strategy | `brief` → `play` |
| Write outbound or nurture sequences | `sequence` |
| Write a landing page, one-pager, post, deck outline, ad | `asset` |
| Prepare discovery questions or a call plan | `discovery` |
| Read copy as the target buyer | `buyer` |
| Stress-test the business case | `cfo` |
| Read it as the competitor's best salesperson | `rival` |
| Test whether it survives a crowded inbox | `inbox` |
| Run the whole buying committee at once | `committee` |
| Read campaign or funnel numbers honestly | `results` |
| Work out why deals were won or lost | `winloss` |
| Close out a motion and decide what compounds | `retro` → `compound` |

Common compositions:

- **New campaign:** `brief` → `play` → `sequence` / `asset` → `buyer` + `inbox` → ship → `results` → `retro` → `compound`
- **Positioning reset:** `signals` → `alternatives` → `positioning` → `proof` → `committee` → `compound`
- **Strategic deal:** `icp` (fit check) → `discovery` → `committee` → `cfo` → after close, `winloss` → `compound`
- **First week with a new client:** `setup` → `onboard` → `audit` → `icp` → `positioning`

When the request is vague ("help with our GTM"), ask one question: what is the next thing going out the door, or the next decision to make? Route from the answer.

### Review — checking a draft before it ships

Pick lenses by asset: cold email or message → `buyer` + `inbox`; page, post or one-pager → `buyer`; proposal, deck or business case → `committee` + `cfo`; competitive deal → add `rival`. Always add the `proof` claim check. Run each lens, then merge into **one** response — never stack the lenses' templates:

```
Verdict: ship / fix first / rethink — the deciding reason
What the reader does: [the lens reactions that matter, quoted line → reaction]
Claims: [each material claim once — backed / weak / unverified / cut]
Fix list: [ordered, deduplicated, each tied to the lens that found it]
Fixed version: [for a single email, message or short post, include a rewrite; for longer assets, offer one]
```

Lenses diagnose; the review delivers the fix. For a single short piece, write the fixed version straight away using `sequence` or `asset` rules, with `[NEEDS PROOF]` wherever a claim lacks backing.

### Scale to the input

Move steps and output templates are the ceiling, not the floor. Three call notes don't need a full theme table; one email doesn't need a full sequence brief. Run the short form when the input is small, and say what was skipped only if it matters.

## Rules every move follows

- **Evidence over eloquence.** Tag claims with their evidence level. A `Believed` claim never appears as fact in customer-facing copy; write it as a hypothesis or cut it.
- **Buyer words beat our words.** When the home holds verbatim buyer language (`Heard`), use it before inventing phrasing.
- **Respect permissions.** Proof tagged `anonymised` or `internal` never leaves the building with names attached. When unsure, anonymise.
- **Small numbers are signals, not results.** Say how many, out of how many, over what period. Do not declare a winner on a handful of replies.
- **The person owns the strategy.** Moves can push hard; they do not quietly replace an ICP, a positioning or a price. Propose, show the evidence, let them decide.
- **No invented facts.** No made-up statistics, customers, quotes, reply rates or benchmarks. If a number is needed and missing, say what would produce it.
- **Never send, publish or change a live system** (CRM, ad account, email tool, website) without explicit approval for that action.

## Finishing a move

End with, briefly:

1. What was produced or decided.
2. What still needs the person's judgment.
3. **What could compound** — the one to three lessons worth writing into the home, each with its proposed file and evidence level. Offer to run `compound`; do not write durable rules without confirmation.

With no home yet, make that one offer, not two: "These are worth keeping — want me to start a GTM home so the next campaign starts from them?"

**Talk like a colleague, not a schema.** With no home, translate the vocabulary: "untested — your view, not buyer evidence" rather than "Believed"; "your proof list" rather than `PROOF.md`. Once a home exists, use the tags — the person has seen them.

## Files in this skill

- `references/context-contract.md` — load order, home layout, write safety
- `references/evidence.md` — evidence levels, permission tags, play status
- `references/moves/*.md` — one file per move (24 moves)
- `references/templates/` — starter files for a GTM home and a motion folder
- `scripts/create_home.py` — creates a GTM home without overwriting anything
