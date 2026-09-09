# Part A · Context engineering — acceptance

## What I did
1. Opened the AI coding tool in an empty folder.
2. Set the session instruction to V1, asked: *"write a function that counts words in a file"*.
3. Changed **only** the instruction (added *"Keep answers short and show commands I can run. Always include a usage example."*), repeated the **same** task verbatim.

## The two outputs
| | V1 (vague instruction) | V2 (one added clause) |
|---|---|---|
| Length | ~40 lines | 12 lines |
| Shape | library function only | function + `__main__` block |
| Runnable? | no | yes |
| Usage example | none | `python output-v2.py` |
| Extra content | paragraphs about memory use and punctuation edge cases | none — cut as noise |

Files: `instruction-v1.md`, `instruction-v2.md`, `output-v1.py`, `output-v2.py`.

## Acceptance — one sentence
The task text never changed, so the only thing that differed was context: adding "always include a usage example" gave the model a concrete output contract, so instead of guessing that I wanted a documented library function it produced a short runnable script with a `__main__` block and dropped the speculative commentary about memory and punctuation.

**Takeaway:** context is not decoration — it is the spec the model resolves ambiguity against. Moving a requirement from "unstated, assumed" into the context window changes the output more reliably than re-prompting.
