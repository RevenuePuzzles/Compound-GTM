# Evidence, Permission and Status

Compounding only works if the home stays trustworthy. Three small vocabularies keep it that way.

## Evidence levels

Every durable line in the home, and every material claim in a draft, carries one of four levels.

| Level | Meaning | Typical source | Can it appear in customer-facing copy? |
|---|---|---|---|
| **Observed** | We saw it in our own data | CRM report, campaign results, product analytics, signed contract | Yes, with the number and period |
| **Heard** | A buyer or customer said it, in their words | Call recording, email reply, interview, review | Yes, quoted or paraphrased, within its permission |
| **Reported** | A third party published it | Analyst report, public filing, survey, news | Yes, with source and date; check it is still current |
| **Believed** | Our hypothesis, not yet tested | Team intuition, a single anecdote, a generated idea | **No.** Phrase as a question or test, or cut it |

Rules:

- One anecdote is `Heard`, not a pattern. Write "one VP Finance said…", not "finance leaders say…".
- Three or more independent `Heard` sources pointing the same way can support a rule in `ICP.md` or `POSITIONING.md`; say how many.
- `Observed` needs a count, a denominator and a period: "9 meetings from 212 contacts, Sept 2026".
- `Reported` facts go stale. Record the publication date; `audit` flags anything older than 18 months.
- Model output is never evidence. A claim Claude generated is `Believed` until something above confirms it.
- When levels conflict (buyers say X, the data shows Y), keep both lines and flag the tension. Do not silently pick one.
- When sources at the same level disagree (four buyers say X, one says the opposite), keep the majority line and add the minority as a **counter-signal** with its own count. It becomes a rule only if it reaches three sources.
- General knowledge about a role or industry ("heads of client services usually own client relationships") is fine for framing and lens reads, but it is `Believed` and labelled as such. It never becomes a home line without real evidence.

### Counting

- Count **independent sources making the same claim**. "Governance came up" and "governance is the real blocker" are different claims at different strength: keep separate lines and counts, don't add them together.
- One person in two conversations is one source. Two people from the same company count as one source for company-level claims.
- When adding to an existing count, check what the original count covered (dates, sources) so nothing is counted twice. If you can't tell, add a new line rather than updating the count.

### Tag format

```
(Level ×count · source · date · permission)
```

- **Date:** `YYYY-MM-DD` for a single event, `YYYY-MM` for a month, `YYYY-MM→MM` for a range, `wk of YYYY-MM-DD` when the person only says "this week".
- **Permission:** required on `Heard` lines and on `PROOF.md` entries; optional elsewhere. Default `internal`.

```
Mid-market holdcos re-tender measurement vendors every 2–3 years (Heard ×4 · discovery calls · 2026-08→10 · internal)
```

## Permission tags (for proof)

| Tag | Meaning |
|---|---|
| **public** | Named, approved for external use |
| **anonymised** | Usable externally only with names and identifying details removed ("a top-5 holding company") |
| **internal** | Never leaves the team; use to inform strategy only |

When permission is unknown, treat it as `internal`. Anonymising means removing the name **and** details that make the company guessable (exact headcount, unique market, distinctive quotes).

Buyer quotes stored in `ICP.md`, `POSITIONING.md` or `field/` are `internal` by default. They inform copy — the words, the pains, the framing — but a verbatim quote only appears in customer-facing material when it is in `PROOF.md` with `public` or `anonymised` permission. Keep identifying details (city, exact headcount, client names) out of home lines; they stay in the raw note.

## Play status

Plays in `PLAYS.md` move through four statuses. Promotion needs evidence, not enthusiasm.

| Status | Bar to reach it |
|---|---|
| **testing** | A brief exists with a hypothesis and success and kill criteria |
| **working** | Hit its success criterion at least once, with the counts recorded |
| **proven** | Hit it at least twice, in separate runs or segments, with no failed run since |
| **retired** | Missed its kill criterion, or the market changed. Keep the entry and the reason — a retired play is a lesson |

Every play records `last reviewed`. A `proven` play not run or reviewed in 6 months drops back to `working` at the next `audit`.

## Honest numbers

- Always report counts, not just rates: "4 replies / 60 sent (6.7%)".
- Under ~30 conversions per variant, treat differences as directional. Say so.
- Compare like with like: same segment, same period, same channel.
- Attribute cautiously. "Opportunities created after the campaign" is not "opportunities created by the campaign".
- When data is missing, say what would produce it rather than estimating.
