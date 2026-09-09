# AILT9019 · Week 2 — Build Start (T-II Agents, Skills & Context)

Everything here runs locally. No API keys, no backend, no network required except where
noted.

```
ailt9019-week2/
├── part-a-context/     context engineering: same task, two instructions
├── part-b-skill/       the pdf-summarizer skill + proof it was used
├── part-c-mcp/         a tiny stdio MCP server (today / current_time / days_until)
├── part-d-pi/          Pi Agent install + .pi/skills/ port of the same skill
├── part-e-github/      git setup + push/clone runbook
├── prototype/          Bin-finder — one page that answers one question + its tests
└── proposal/           2-3 direction shortlist + draft proposal (due Fri 25 Sep)
```

## Lab checkpoints

| Part | Done when | Status |
|---|---|---|
| A · Context | You can predict how an instruction change changes the answer | **done** — `part-a-context/notes.md` |
| B · Skills | The tool reproduces your SKILL.md format unprompted | **done** — `part-b-skill/test-output.md` |
| C · MCP | You can point at output that came from a tool, not the model | **done** — `part-c-mcp/tool-output.txt` |
| D · Pi Agent | Pi runs locally and follows your skill | **partly** — installed (v0.85.1) + skill copied to `.pi/skills/`; needs an API key for the session |
| E · GitHub | A fresh clone contains everything you built | **pending** — needs GitHub auth |

## Two things need you (about 7 minutes total)

Both are interactive and use *your* credentials, so I stopped rather than guess.

**1 · GitHub (Part E).** `gh` v2.100.0 is installed:
```bash
GH="C:/Users/sohan/.workbuddy-ai/binaries/gh/bin/gh.exe"
cd "C:/Users/sohan/WorkBuddy AI/2026-09-09-21-42-04/ailt9019-week2"
"$GH" auth login
"$GH" repo create ailt9019-week2 --private --source=. --remote=origin --push
```
Then clone into a second folder to prove a fresh clone has everything.

**2 · Pi Agent provider (Part D).** Every provider reports `not_ready`. Set one key:
```bash
export GEMINI_API_KEY=...      # or ANTHROPIC_API_KEY / OPENAI_API_KEY
cd part-d-pi/practice && pi --approve
```
Then `/skill:pdf-summarizer` to run the Part B skill inside Pi.

## Quick start

```bash
# Prototype — just open it, no server needed
start prototype/index.html          # Windows
open prototype/index.html           # macOS

# MCP server — real handshake, lists tools, calls each one
python part-c-mcp/test_client.py

# PDF summarizer skill
python part-b-skill/my-skill/scripts/extract_pdf.py <file.pdf> --out out.txt

# Prototype evaluation — 42 checks, exits non-zero on failure
node prototype/evaluate.js
```

## What each part concluded

- **A** — Changing *only* the session instruction (adding "always include a usage
  example") turned a 40-line documented library function into a 12-line runnable script.
  Context is the spec the model resolves ambiguity against.
- **B** — `pdf-summarizer` turns a long PDF into a fixed five-part brief. Its value is the
  constraints, not the instruction: extract before writing, cite every page, declare what
  you skipped, refuse to fill gaps.
- **C** — `today` returned `2026-09-09 (Wednesday), ISO year 2026 week 37`, read from this
  machine's clock. The model supplied only the words around it.
- **D** — The same `SKILL.md` worked in Pi with zero edits, which is the actual lesson:
  a skill is a file, not a feature of one tool.
- **E** — repo committed locally; push + fresh-clone verification pending GitHub login.

## Notes

- The prototype's rule data is **seed data** — self-curated placeholder, labelled as such
  in the UI. It must be replaced with rules transcribed from the published campus
  recycling guide before Week 4.
- The MCP server is stdlib-only Python (no pip install) so it cannot break on a
  dependency.
