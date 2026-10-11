# results — read the numbers honestly

Turn campaign, sequence, page or funnel data into what actually happened — with counts, denominators and the right amount of doubt — and compare it to what the brief predicted.

## Use when

- "How did the campaign do?", "which variant won?", "why is pipeline down?", a results CSV or dashboard export is attached.

## Reads

The motion's `BRIEF.md` (success and kill criteria), results files, CRM or email-tool exports, analytics, `PLAYS.md` for past runs.

## Steps

1. **Check the data before reading it.** Period covered, list size, what's missing, duplicates, tracking breaks, bot opens or clicks. Say what can't be trusted. With a file, compute in code rather than estimating.
2. **Lay out the funnel with counts:** reached → delivered → opened (treat as unreliable) → replied → positive reply → meeting → qualified → opportunity → won. Rates beside counts, never instead of them.
3. **Compare to the brief.** Did it hit the success criterion, the kill criterion, or neither? Quote both.
4. **Compare to the past** — the same play in `PLAYS.md`, same segment, similar period. Like with like only.
5. **Split by what varied:** segment, role, trigger, variant, channel, sender. Flag every split under ~30 conversions as directional.
6. **Separate correlation from cause.** Name the other things that changed in the same period (seasonality, a price change, a big event, a new rep).
7. **Read the replies, not just the rates.** If reply text exists, run a quick `signals` pass: what did people say, including the negatives?

## Output

- One-line verdict against the brief: hit / missed / inconclusive.
- The funnel table with counts.
- What we learned, each with its evidence level and confidence.
- What we did **not** learn, and what would answer it next time.
- Recommended status change for the play (`evidence.md` bars).

## Don't

- Don't declare winners on small samples. Don't celebrate open rates.
- Don't credit the campaign for pipeline it merely preceded.

## Could compound

Play status and result lines into `PLAYS.md`; segment-level observations into `ICP.md`; hand off to `retro`.
