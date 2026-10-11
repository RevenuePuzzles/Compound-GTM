# audit — check the GTM home is still trustworthy

A home that is wrong is worse than no home: every motion inherits its mistakes. Run this monthly, before a big launch, or when inheriting someone else's home.

## Use when

- "Is our ICP still right?", "clean up the GTM home", "we haven't looked at this in months".
- Before `positioning` or a major campaign.
- Taking over a client's or predecessor's GTM documentation.

## Checks

For each file, report findings in plain language, not codes.

1. **Belief load.** What share of lines are `Believed`? Over half in `ICP.md` or `POSITIONING.md` means the strategy rests on hunches — name the three most consequential ones.
2. **Staleness.** Lines with no date; `Reported` sources older than 18 months; `proven` plays not reviewed in 6 months (demote to `working`).
3. **Contradictions.** Lines in different files that disagree (ICP says mid-market, plays only target enterprise; positioning claims speed, proof has nothing on speed).
4. **Orphan claims.** Claims used in `POSITIONING.md` or in shipped assets with no entry in `PROOF.md`.
5. **Permission risk.** Named customers in anything not tagged `public`; anonymised proof that is still guessable.
6. **Dead weight.** Retired plays without a reason; duplicates; generic lines that would fit any company ("we put the customer first").
7. **Coverage gaps.** Buying-committee roles with no known pain; alternatives with no counter-message; disqualifiers missing entirely.

## Output

- A one-paragraph verdict: can the next campaign trust this home, partly, or not yet?
- Findings grouped by **fix now** (risk of wrong or embarrassing claims), **fix soon** (staleness, gaps), **nice to have**.
- Proposed edits as exact before/after lines. Write them only after confirmation.
- The single test or research task that would most improve the home.

## Could compound

Audit findings are edits to the home itself. Run `compound` on the confirmed ones.
