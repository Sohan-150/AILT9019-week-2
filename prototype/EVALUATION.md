# Bin-finder · evaluation

Run it: `node evaluate.js` (exit 0 = all gates passed, 1 = something failed).

## What it checks

The harness loads the **real** `lookup()` and `norm()` out of `index.html` — it does not
reimplement them — and tests them against **hand-written** expected answers in
`tasks.json`. Those expected answers are deliberately *not* derived from `rules.js`: if
someone mis-edits the rule table, the test has to disagree rather than agree with it.

| # | Group | n | Gate |
|---|---|---|---|
| 1 | Task set — correct bin **and** a citable rule | 30 | ≥90% |
| 2 | Hazardous refusals — must refuse, never assign a bin | 5 | 100% |
| 3 | Unknown-item refusals — must return no match | 3 | 100% |
| 4 | Input robustness — casing / whitespace / punctuation | 4 | 100% |
| 5 | Every rule carries a `rule` and a `source` line | 41 | 100% |

Refusals are gated at 100% on purpose: a missed refusal is worse than a missed bin. One
battery in a general bin is a real incident; one cardboard box in the wrong bin is not.

## Current result (seed data)

```
rule set: 41 rules | hazardous: 5

1. Task set (correct bin + citation)   30/30 (100%)
2. Hazardous refusals                  5/5 (100%)
3. Unknown-item refusals               3/3 (100%)
4. Input robustness                    4/4 (100%)
5. Every rule carries a source line    41/41

RESULT: ALL GATES PASSED
```

Full output: `eval-results.txt`.

## Can the test actually fail? Yes — verified by mutation

A green test proves nothing until you have watched it go red. I copied the prototype to a
scratch folder, injected two realistic errors, and re-ran:

| Injected mutation | Caught? |
|---|---|
| `pizza box` → `Paper` (the classic grease-contamination mistake) | **yes** — task set 29/30, and the `pizza-box` variant also failed |
| Removed `hazardous: true` from `battery` | **yes** — refusal gate dropped to 4/5 and the run exited 1 |

Both mutations were caught and the run exited 1. The scratch folder was deleted and
`rules.js` verified unchanged (5 hazardous rules, `pizza box` → `General waste`).

## Honest limitation

This is a 100% pass **on seed data I wrote myself**, so it proves the *mechanism* works,
not that the *rules are right*. The number only becomes meaningful once `rules.js` is
transcribed from the published campus guide — that is Week 3 work, and re-running this
harness afterwards is how we will know the transcription is correct.
