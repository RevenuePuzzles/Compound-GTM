# Context Contract

Every Compound GTM move follows this contract before it reads, writes or recommends anything.

## The GTM home

A GTM home is a folder of plain Markdown. Small on purpose: six files, one folder, and a short README that explains the tags to teammates.

```
gtm-home/
├── README.md         What the home is and how to read a line — for teammates opening the folder
├── ICP.md            Who buys, who doesn't, and what makes now the moment
├── POSITIONING.md    What buyers do instead of us, why we win, what we say
├── PROOF.md          Every claim we make, its evidence level, source and permission
├── PLAYS.md          Motions we run, their status (testing → working → proven → retired)
├── VOICE.md          How we sound, sentence by sentence
├── COMPANY.md        Facts about what we sell: offers, prices, terms, motion, team
└── motions/
    └── 2026-10-outbound-holdco-cfos/
        ├── BRIEF.md      Goal, audience, hypothesis, success and kill criteria
        ├── assets/       Sequences, pages, decks, posts for this motion
        ├── RESULTS.md    Numbers, with counts and dates
        └── RETRO.md      What happened, why, and what compounds
```

Optional, only when the work calls for it: `accounts/<company>.md` for named-account plans, `field/` for raw call notes, transcripts and win/loss interviews waiting to be mined.

### What goes where

| File | Governing question | Belongs here | Does not belong here |
|---|---|---|---|
| `ICP.md` | Who should we sell to, and when? | Firmographics, buying committee, pains in buyer words, triggers, disqualifiers, fit evidence | Messaging, offer design |
| `POSITIONING.md` | Why us, against what? | Alternatives (including doing nothing), differentiators, value, message pillars, objections and answers | Raw proof, sentence style |
| `PROOF.md` | What can we prove? | Claims, evidence level, source, date, permission, where it's used | Opinions about the market |
| `PLAYS.md` | What works? | Named plays: who, trigger, channel, steps, status, results to date, last reviewed | One-off campaign notes |
| `VOICE.md` | How should it sound? | Tone, words we use and avoid, sentence habits, formatting habits per channel | Claims, strategy |
| `COMPANY.md` | What do we actually sell? | Offers, packaging, price ranges, contract terms, sales motion, capacity | Aspirations |

A lesson that mixes two concerns is split into two entries, not duplicated.

## Load order

When sources disagree, the higher one wins. Do not average incompatible rules into mush — surface the conflict.

1. What the person says in this conversation, and material they supply.
2. Workspace instructions (`CLAUDE.md`, `AGENTS.md`, a README in the home).
3. The motion's own `BRIEF.md` when working inside a motion.
4. The GTM home files the move needs.
5. Curated examples in the home (winning emails, best pages), used to interpret rules — never copied word for word.
6. Raw material: call notes, transcripts, CRM exports, results files, competitor pages.
7. This skill's defaults — only for gaps nothing above resolves.

Load only what the move needs. `sequence` needs `ICP.md`, `POSITIONING.md`, `PROOF.md`, `VOICE.md` and the brief; it does not need `COMPANY.md` pricing detail.

## When the home is missing or thin

- A missing or sparse file never blocks work. Use what the conversation gives you, mark gaps, and keep going.
- Do not run `onboard` just because a file is empty. Offer it when the gap materially weakens the output.
- An existing workspace with its own conventions (a client's Notion export, a GTM brain repo) is a real starting point. Map onto it; do not impose this layout retroactively unless asked.

## Write safety

- Read a file before editing it. Preserve everything the person wrote.
- Propose durable changes; write them only when the person confirms or has asked to save.
- Add the date and source to every durable line: `(Heard ×1 · call w/ VP Finance, mid-market holdco · 2026-10-02 · internal)` — full format in `evidence.md`.
- Never write lessons into this skill's own files or an installed plugin copy.
- Never send emails, publish pages, launch ads, or edit a CRM or other live system without explicit approval for that specific action.
- Keep client names out of anything tagged `anonymised`. When working across several clients, never let one client's data appear in another's home.

## Handoff

Every substantial move ends with: what was produced, what needs judgment, and what could compound (file + evidence level).
