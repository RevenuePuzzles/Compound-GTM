# proof — build, check and anonymise the claims we make

Every claim in a sequence, page or deck should trace to something real. This move maintains `PROOF.md` as the single ledger of what the company can prove, how strongly, and where it may be used.

## Use when

- "Write a case study", "do we have proof for this?", "check this deck's claims", "we can't name the client".
- Before any asset ships, as a claim check.

## Reads

`PROOF.md`, the draft or asset being checked, source material (results, contracts, quotes, reports).

## Modes

### Check a draft

1. List every material claim in the draft: numbers, outcomes, comparisons, customer references, "the only", "the first", "the leading".
2. Match each to a `PROOF.md` entry. Report: **backed** (level and permission fit the use), **weak** (backed but stale, `Believed`, or one anecdote presented as a pattern), **unverified** (no entry and no source given yet — ask for it; this does not mean the claim is false), **cut** (unprovable by nature, like "the leading", or implausible as written). With no `PROOF.md` at all, every claim starts as unverified.
3. For weak and unbacked claims, propose a fix: soften, reframe as a question or hypothesis, replace with a backed claim, or cut.
4. Check permissions: anything `anonymised` or `internal` used with names or guessable details is a stop.

### Build proof

1. Gather the raw evidence (results file, before/after numbers, a buyer quote).
2. Write the entry: claim, level, source, date, permission, where it is used, and the context needed to keep it honest ("in a 6-week pilot, one business unit").
3. For case studies: situation → what they tried before → what changed → result with numbers and period → quote. Mark every gap rather than filling it.

### Anonymise

Replace the name **and** identifying details: exact size → band, unique market → region, distinctive quote → paraphrase. Ask: could a competitor or journalist identify them in five minutes? If yes, generalise further.

## Output

A claim-by-claim table for checks; new or updated `PROOF.md` entries for builds; a before/after for anonymisation.

## Don't

- Don't round up, extrapolate from a pilot to "customers see", or turn a single result into "on average".
- Don't invent quotes, logos, metrics or testimonials — not even as placeholders that might ship. Use `[NEEDS PROOF]`.

## Could compound

New entries and usage notes into `PROOF.md`; claims that buyers challenged into `POSITIONING.md`.
