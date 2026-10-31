# Evidence, Permission and Status

Compounding only works if the home stays trustworthy. Four small vocabularies keep it that way: evidence levels, permission tags, play status and lesson lifecycle.

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

## Lesson lifecycle

Lessons in the GTM home — lines in `ICP.md`, `POSITIONING.md`, `PROOF.md`, `VOICE.md` and `COMPANY.md` — follow a lifecycle that matches how much evidence backs them. This prevents a home that grows without bound and prevents provisional hunches from hardening into unquestioned rules.

| Status | Meaning | Bar to reach it |
|---|---|---|
| **provisional** | The lesson comes from a single source or a single motion; it may compound further or may not hold | One cited incident, with date and source |
| **validated** | The lesson has been confirmed by independent evidence: a second source, a repeated outcome, or an external metric | Two or more independent sources, or one source plus a measurable outcome that confirmed the prediction |
| **retired** | The lesson no longer applies, was superseded, or was found wrong | Evidence of changed conditions, contradicting data, or 6 months without use |

Rules:

- A lesson needs a **cited incident** — a verifiable observation, conversation or result — before it is written. "We believe X" without an incident is an open hypothesis, not a rule.
- Lessons enter at `provisional` unless they already meet the `validated` bar. A single observation, a single buyer quote, a single campaign result all start provisional.
- Promotion to `validated` requires evidence **the person did not generate themselves**: an external test passed, a buyer confirmed it independently, a later campaign reproduced the outcome. Model-generated agreement does not count.
- Retirement is first-class: a lesson that stopped being true is more valuable as a dated, explained removal than as a silent gap. Mark it `retired` with the reason and date rather than deleting.
- Contradictions are resolved by keeping both lines and flagging the tension, then seeking the evidence that will settle it. Do not silently pick one.

### Tracking usage

When a lesson is loaded and applied — during `sequence`, `asset`, `buyer`, or any drafting or review move — note the motion or date in a lightweight way (a `last used` annotation, or a tally in the lesson's source line). Lessons that are never retrieved provide no value and may be noise.

### Caps and retirement

A home that grows without bound becomes harder to trust and slower to load. Unbounded accumulation can degrade retrieval until injecting lessons is worse than starting fresh.

- **Target caps:** aim for roughly 30–50 active lines per file in `ICP.md`, `POSITIONING.md` and `VOICE.md`. `PROOF.md` may be larger but should still be pruned.
- **Retirement triggers:**
  - A `provisional` lesson not validated within 6 months → review for retirement or test.
  - A `validated` lesson not used or referenced for 6 months → review for retirement.
  - A lesson contradicted by newer evidence → retire with the reason.
  - A lesson made redundant by a more specific or more evidenced line → merge or retire the weaker one.
- At each `audit`, count lessons by status and flag any file over its cap or any lesson overdue for review.

### Lesson annotation format (optional)

For teams that want explicit tracking, a lesson can carry a parenthetical lifecycle annotation:

```
- Agency ops leaders care about client-reporting hours. (Heard ×4 · discovery · 2026-09 · validated · last used 2026-10)
```

The annotation extends the standard tag with `provisional` / `validated` / `retired` and optionally `last used <date>`. Teams not ready for this can rely on the count and date to infer lifecycle.

## Honest numbers

- Always report counts, not just rates: "4 replies / 60 sent (6.7%)".
- Under ~30 conversions per variant, treat differences as directional. Say so.
- Compare like with like: same segment, same period, same channel.
- Attribute cautiously. "Opportunities created after the campaign" is not "opportunities created by the campaign".
- When data is missing, say what would produce it rather than estimating.
