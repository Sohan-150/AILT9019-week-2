# Project Proposal — Bin-finder: recycling rules helper

*(Draft, Week 2. Section titles follow AILT9019_Project_Proposal_Template.docx. No group
names or personal information appear in this content.)*

---

## 1. Background

**Primary user group:** students living in university halls of residence.

**Concrete task:** they are holding one item and need to know which bin it goes in under
the published campus recycling rules.

**Current pain:** the rules exist but are spread across a webpage and PDF signage that
nobody reads at the bin. In practice people guess, and guessing wrong contaminates an
entire load — one greasy pizza box or one battery can downgrade or endanger a whole
collection. The information need is one second long and happens at the point of disposal,
which is exactly where a long document is useless.

**Why worth building this semester:** it is small enough to finish and evaluate honestly,
and its central design problem is refusal — knowing what it does *not* know — which is
the most transferable thing in this course.

**Target / non-target:** it is for hall residents disposing of ordinary household items at
hall bins. It is **not** for hazardous-waste disposal, not for commercial or lab waste,
and not for any item outside the published hall rules.

**Idea source:** adapted from topic-list idea **#2 "Recycling rules helper" (Easy)**. The
user group and the "does not" are kept as given; the change is that we treat the
no-match case as a first-class product behaviour rather than an error message, and we
scope the dataset strictly to hall bins rather than campus-wide rules.

## 2. Project pipeline

```
item name (typed)
      │
      ▼
[1] normalise ──► lowercase, strip punctuation, collapse whitespace
      │
      ▼
[2] exact match against rule table ──── hit ──► [5]
      │ no hit
      ▼
[3] substring match (both directions) ── hit ──► [5] (marked "closest match")
      │ no hit
      ▼
[4] NO MATCH ──► refuse: "not in the published rules, ask building staff"
      │
      ▼
[5] hazardous flag? ── yes ──► refuse: hand to staff / collection point (hard stop)
      │ no
      ▼
[6] render bin + the rule text + the source line
```

What the team will actually build: a single-page web app (no backend) over a
**self-curated rule table** (`rules.js`), where each row is one item with its bin, the
rule sentence, and the `source` line it was transcribed from. No model call is needed and
none is made — the value is in retrieval plus honest refusal, not generation.

**Data:** the rule table, transcribed line-by-line from the published campus recycling
guide (public). Prototype currently runs on **seed data** that is self-curated and
explicitly labelled as such in the UI; replacing it with the transcribed real source is
Week 3 work. Permission: source is public; the derived table is self-curated.

**Pipeline figure:** see the ASCII diagram above; a drawn version goes in the final draft.

## 3. Evaluation and test

Test style: **a fixed task set with expected bins, plus explicit refusal cases. Already
built and passing — see `prototype/EVALUATION.md`.**

| # | Group | n | Gate |
|---|---|---|---|
| 1 | Task set — correct bin **and** a citable rule | 30 | ≥90% |
| 2 | Hazardous refusals — must refuse, never assign a bin | 5 | 100% |
| 3 | Unknown-item refusals — must return no match | 3 | 100% |
| 4 | Input robustness — casing / whitespace / punctuation | 4 | 100% |
| 5 | Every rule carries a `rule` and a `source` line | 41 | 100% |

- The task set covers every bin plus every contamination trap (greasy cardboard, thermal
  receipts, drinking glass, soft film plastic, bones).
- **Refusal cases (must refuse, must not guess):** an item absent from the rules
  (asbestos, ceramic mug); any hazardous item (battery, paint, light bulb, aerosol,
  medicine) even on an exact match; and a near-miss that must not silently fuzzy-match
  into a different bin.
- Expected answers in `tasks.json` are **written by hand, independently of the rule
  table**, so a bad edit to the rules is caught rather than agreed with.

**Current result: 100% on all five groups** (`prototype/eval-results.txt`).

**"Good enough" means:** ≥90% on the task set, **100%** on refusal cases — a missed
refusal is worse than a missed bin, because one battery in a general bin is an incident
while one mis-binned box is not — and zero cases where the app states a bin without
citing a rule.

**We checked the test can fail.** A green test proves nothing until you have watched it go
red, so we mutated the rule table twice: sending `pizza box` to *Paper* (the classic
grease-contamination error), and removing the hazardous flag from `battery`. Both were
caught and the run exited non-zero.

**Method is runnable this semester** — `node evaluate.js`, no model, no API cost, no
human labelling at scale.

**Honest limitation:** this is 100% on **seed data we wrote ourselves**, so it proves the
mechanism, not that the rules are right. It only becomes meaningful once the table is
transcribed from the published guide; re-running the harness after transcription is how
we will know the transcription is correct.

## 4. Distribution and accessibility

1. **No model or API to set up.** The prototype is one `index.html` plus one `rules.js`.
   Opening the file in a browser works with no install, no server, and no network — this
   deliberately sidesteps the hardest part of hand-off.
2. **A non-coder can succeed from the README.** The README will show three copy-paste
   examples and a screenshot. First successful use = open the page, type one item, read
   the bin. There is no configuration step.
3. **Lives in more than one agent environment.** Yes, and this is already partly proven:
   the *authoring* workflow runs in two. A `SKILL.md` governs how the rule table is
   transcribed and checked, installed for WorkBuddy at
   `~/.workbuddy-ai/skills/` and for Pi at `~/.pi/agent/skills/` (identical file, zero
   edits). A tiny MCP server (`part-c-mcp/server.py`) exposes tools over stdio. If scope
   allows, a rules-lookup MCP tool would let any agent answer "which bin does X go in"
   without opening the page.

## 5. Ethics and risks

**Explicit "does not" (quotable in two lines):**

> Bin-finder does not advise on hazardous waste, and does not invent a bin for any item
> that is not written in the published campus rules — it says it doesn't know and hands
> you to building staff.

**Misuse and failure risks, and mitigation:**

| Risk | Mitigation |
|---|---|
| Wrong bin confidently stated → contaminated load | Every answer cites its rule; no citation, no answer |
| Hazardous item given a normal bin → real danger | Hard-coded hazardous flag, refuses even on exact match |
| Item not in rules → plausible guess | No fuzzy matching beyond substring; unknown → refusal |
| Outdated rules (source changes) | Rule table is one file, each row carries its source line; UI shows a "seed data" banner until transcription is done |
| Users treat it as authoritative over staff | Prominent "does not override building staff" panel; staff word wins |
| Overtrust because it looks official | Footer + data-status banner state provenance on every screen |

## 6. Checkpoints

**(A) Acceptance items**

*Must-have (the demo fails without these):*
- Rule table transcribed from the real published guide, every row with a source line
- Lookup returns a bin **with** its cited rule for any item in the table
- Hard refusal on all hazardous items
- Honest "not in the rules" refusal for unknown items, with staff hand-off
- "Does not" panel visible in the UI

*Should-have (only if time allows):*
- Photo / barcode input instead of typing
- Per-hall rule variants (different halls, different bins)
- Rules-lookup MCP tool so other agents can call it
- Editable rule table in the UI with an export-to-JSON button

**(B) Timeline**

| Week | Milestone |
|---|---|
| 2 (Sep 7–13) | Prototype running on seed data; directions shortlisted; repo pushed |
| 3 (Sep 14–20) | Transcribe real rule table; build the task set; run first evaluation |
| 4 (Sep 21–27) | **Proposal draft due Fri 25 Sep**; evaluation results in; refusals hardened |
| 5–6 | Real-user walkthrough with hall residents; fix what the task set missed |
| 7+ | Should-have items only if must-haves are solid |

```
                    W2   W3   W4   W5   W6   W7+
                    ───  ───  ───  ───  ───  ───
Prototype (seed)    ███
Evaluation harness  ███  ███
Transcribe rules         ███  ███
Real evaluation               ███
Proposal draft                ███▌◄─ Fri 25 Sep
User walkthrough                   ███  ███
Should-haves                                 ███
                    ───  ───  ───  ───  ───  ───
                    done done done
```

The critical path is the transcription: everything after Week 3 depends on real rules
being in the table, and it is the one task we cannot shortcut by writing more code.

---

### Quick self-check
- [x] One user group + one task in a single sentence: *hall residents need to know which bin a specific item goes in.*
- [x] Dataset source and permission in one line: *rule table transcribed from the published campus recycling guide (public); derived table self-curated.*
- [x] Core workflow small enough to run end-to-end this semester.
- [x] At least one clear "does not" written (quotable in two lines).
- [x] Background states the idea source (topic-list idea #2, adapted).
- [x] No group names, member names, UIDs, or emails in the content.
