# compound — write what was learned back into the home

The signature move. Turn a confirmed lesson, result or preference into a durable, dated, evidence-graded line in the right file, so the next motion starts from it.

## Use when

- At the end of any substantial move, retro, results read or win/loss.
- The person says "remember this", "save that", "make that a rule", "this keeps happening".
- A correction repeats ("I told you, we never lead with price").

## Steps

1. **Collect candidate lessons** from the current work. For each, write one atomic sentence.
2. **Classify the destination.**

   | Lesson about… | Goes to |
   |---|---|
   | Who buys, who doesn't, triggers, disqualifiers, buying committee | `ICP.md` |
   | Alternatives, why we win or lose, message that landed or flopped, objection and answer | `POSITIONING.md` |
   | A claim and its backing (stat, quote, case result) | `PROOF.md` |
   | A motion that worked, failed or needs a rule change | `PLAYS.md` |
   | Tone, words, sentence and format habits | `VOICE.md` |
   | Offer, price, terms, capacity | `COMPANY.md` |
   | A one-off decision for this motion only | The motion's `RETRO.md` |
   | Raw notes not tied to a motion (calls, replies, interviews) | `field/<yyyy-mm-dd>-<topic>.md`, with a line `mined: <date> → <files updated>` once processed |
   | A live sales opportunity spotted in the material | Not the home — flag it to the person for their CRM. It counts as trigger evidence only after the deal's outcome is known |

   Mixed lessons are split. "CFOs ignored the ROI email because it opened with our funding round" becomes a `VOICE.md` or `POSITIONING.md` line about openers and an `ICP.md` line about what CFOs respond to — if each has evidence.

3. **Require a cited incident.** Every lesson needs a verifiable source: a specific conversation, a campaign result with dates and counts, a buyer quote, or an explicit correction from the person. Lessons without incidents — "we think X", "it seems like Y" — are hypotheses, not rules.
   - If the only evidence is model reasoning or general knowledge, do not write it as a lesson. Either find the incident or move it to **Open hypotheses**.
   - If the person asks to save something without an incident, ask what happened that showed it.
4. **Grade it.** Assign the evidence level, count and permission from `evidence.md`, following its counting rules — separate claims stay separate lines, and check what an existing count already covers before adding to it.
5. **Assign lifecycle status.** See `evidence.md` for the full rules.
   - **provisional**: one cited incident, one source, one motion — the default for new lessons.
   - **validated**: two or more independent sources, or one source plus a later outcome that confirmed the prediction.
   - Most new lessons enter at `provisional`. Promotion to `validated` needs evidence the person did not generate.
6. **Decide whether it generalises.**
   - Explicit enduring preference from the person → durable once confirmed.
   - Pattern across several sources → durable, with the count.
   - Single observation → record it as provisional, written as a single observation ("one buyer…") or keep it in `RETRO.md`.
   - Inference without an incident → show it as a proposed hypothesis and ask before writing.

   When the person has already said "write the changes", that covers what they told you and what the evidence directly shows. Your own inferences may still be written, but only under **Open hypotheses**, tagged `Believed`, each with a test — and list them by name in your reply so the person can strike them.
7. **Check for conflict and consistency.** Read the destination file before writing.
   - If the new line contradicts an existing one, do not overwrite: show both, ask which stands, or keep both and flag the tension.
   - If the new line duplicates an existing one, update the existing line's count and date rather than adding a second entry.
   - If the new line would push the file over the recommended cap (~30–50 active lines for most files), flag it and ask whether a weaker or older lesson should be retired to make room.
8. **Write narrowly.** Add or revise the smallest relevant line, with date and source:
   `- Ops leaders at holdco-owned agencies care about client-reporting hours, not media efficiency. (Heard ×4 · discovery calls · 2026-09→10 · internal · provisional)`
9. **Update status where earned.** If a play now meets the `working` or `proven` bar, update its status and results line.

## Output

A short list: each lesson, its destination, evidence level, and whether it was written or is awaiting confirmation. Show the exact lines written.

## Don't

- Don't write lessons without cited incidents. A lesson needs a verifiable source — a conversation, a result, a quote, a correction. "We think X" or "it seems like Y" are hypotheses, not lessons.
- Don't write `Believed` lessons as rules. Store them as hypotheses under an "Open hypotheses" heading, or not at all.
- Don't skip the conflict check. Read the file before writing. Contradictions must be surfaced, not silently overwritten.
- Don't promote lessons to `validated` based on model agreement. External evidence — a second source, a later outcome, a test — is required.
- Don't save lessons into this skill's files.
- Don't let one client's lessons into another client's home.
- Don't pad the home. If a lesson is already there, update its count and date instead of adding a duplicate. If the file is over cap, retire something first.
