# audit — check the GTM home is still trustworthy

A home that is wrong is worse than no home: every motion inherits its mistakes. Run this monthly, before a big launch, or when inheriting someone else's home.

## Use when

- "Is our ICP still right?", "clean up the GTM home", "we haven't looked at this in months".
- Before `positioning` or a major campaign.
- Taking over a client's or predecessor's GTM documentation.

## Checks

For each file, report findings in plain language, not codes.

1. **Belief load.** What share of lines are `Believed`? Over half in `ICP.md` or `POSITIONING.md` means the strategy rests on hunches — name the three most consequential ones.
2. **Staleness.** Lines with no date; `Reported` sources older than 18 months; `proven` plays not reviewed in 6 months (demote to `working`); `provisional` lessons older than 6 months without validation.
3. **Contradictions.** Lines in different files that disagree (ICP says mid-market, plays only target enterprise; positioning claims speed, proof has nothing on speed).
4. **Orphan claims.** Claims used in `POSITIONING.md` or in shipped assets with no entry in `PROOF.md`.
5. **Permission risk.** Named customers in anything not tagged `public`; anonymised proof that is still guessable.
6. **Dead weight.** Retired plays without a reason; duplicates; generic lines that would fit any company ("we put the customer first").
7. **Coverage gaps.** Buying-committee roles with no known pain; alternatives with no counter-message; disqualifiers missing entirely.
8. **Lifecycle health.** Count lessons by status (`provisional` / `validated` / `retired`) in each file.
   - A file with mostly `provisional` lessons is untested — flag the three most load-bearing ones for validation.
   - A file with lessons that have no `last used` annotation and date from more than 6 months ago may contain dead weight — flag for retirement review.
   - If usage tracking is in place, identify lessons retrieved zero times in the past 6 months.
9. **Size and cap.** Count active (non-retired) lines per file.
   - `ICP.md`, `POSITIONING.md`, `VOICE.md`: target ~30–50 active lines. Over 50 → flag for pruning.
   - `PROOF.md`: may be larger, but review anything over 100 entries.
   - `PLAYS.md`: no hard cap, but retired plays should explain why.
   - If over cap, recommend the weakest or oldest lessons to retire.

## Output

- A one-paragraph verdict: can the next campaign trust this home, partly, or not yet?
- **Lifecycle summary:** line counts by file and status (provisional / validated / retired), plus any files over cap.
- Findings grouped by **fix now** (risk of wrong or embarrassing claims), **fix soon** (staleness, gaps, over-cap files), **nice to have** (minor duplicates, formatting).
- **Retirement candidates:** lessons flagged for removal, each with the reason (unused, stale, contradicted, redundant).
- Proposed edits as exact before/after lines. Write them only after confirmation.
- The single test or research task that would most improve the home.

## Could compound

Audit findings are edits to the home itself. Run `compound` on the confirmed ones.
