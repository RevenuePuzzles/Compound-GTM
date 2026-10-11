# winloss — find out why deals were really won or lost

CRM "lost reasons" are mostly guesses typed in a hurry ("price", "timing"). This move gets to the real reasons and turns them into changes in targeting, positioning, offer and process.

## Use when

- "Why are we losing?", "win/loss analysis", "review closed-lost", "prepare win/loss interviews", a batch of closed deals or interview notes is supplied.

## Reads

Closed-won and closed-lost exports, deal notes, call transcripts, interview notes in `field/`, `ICP.md`, `POSITIONING.md`, `COMPANY.md`.

## Modes

### Analyse deal data

1. **Describe the sample:** how many wins and losses, period, segments, deal sizes, who logged the reasons. Note bias (only big deals, one rep).
2. **Compare wins and losses** on fit (did lost deals match `ICP.md`?), source, cycle length, stage reached, committee engagement (single-threaded vs multi-threaded), competitor or alternative, discounting.
3. **Test the logged reasons.** Where notes or transcripts exist, check whether "price" was really price, or unclear value, wrong buyer, bad timing, a scope mismatch.
4. **Find the patterns** with counts. Separate losses we could have prevented (process, message, offer) from losses we shouldn't have pursued (fit).

### Prepare interviews

Write a short guide for 20-minute calls with recent buyers and non-buyers (ideally run by someone outside the sales team): how they first noticed the problem, what they considered, how they decided, what almost stopped them, what the deciding moment was, what we could have done differently. No defending, no selling.

### Synthesise interviews

Run a `signals`-style extraction across the notes, then map each finding to the part of GTM it implicates: targeting, message, proof, offer, sales process, product.

## Output

- Top reasons we win and lose, each with count and evidence level.
- Preventable vs fit-related losses.
- Recommended changes by area, each tied to its evidence.
- The single change with the biggest likely effect.

## Could compound

Disqualifiers and fit signals into `ICP.md`; why-we-win and objections into `POSITIONING.md`; offer and terms issues into `COMPANY.md`; quotes into `PROOF.md` with permission tags.
