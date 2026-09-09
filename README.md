# AILT9019 · Week 2 — Build Start (T-II Agents, Skills & Context)

Everything here runs locally. No API keys, no backend, no network required except where
noted.

```
ailt9019-week2/
├── part-a-context/     context engineering: same task, two instructions
├── part-b-skill/       the pdf-summarizer skill + proof it was used
├── part-c-mcp/         a tiny stdio MCP server (today / current_time / days_until)
├── mini-project/       Course Buddy — small interactive CLI using the skill + MCP together
└── proposal/           2-3 direction shortlist + draft proposal (due Fri 25 Sep)
```

## Lab checkpoints

| Part | Done when | Status |
|---|---|---|
| A · Context | You can predict how an instruction change changes the answer | **done** — `part-a-context/notes.md` |
| B · Skills | The tool reproduces your SKILL.md format unprompted | **done** — `part-b-skill/test-output.md` |
| C · MCP | You can point at output that came from a tool, not the model | **done** — `part-c-mcp/tool-output.txt` |
| E · GitHub | A fresh clone contains everything you built | **done** — this repo; verified by cloning into a second folder |

Part D (Pi Agent) isn't tracked in this repo — `mini-project/` covers the same "skill +
tool, running locally" idea without needing a model provider key.

## mini-project — Course Buddy

A small interactive CLI that wires Part B and Part C together instead of leaving them as
separate demos:

- calls the real MCP server (`part-c-mcp/server.py`) over stdio JSON-RPC for today's date
  and "days until a deadline"
- runs the `pdf-summarizer` skill's own extractor
  (`part-b-skill/my-skill/scripts/extract_pdf.py`) on a PDF and writes the result in the
  skill's exact five-part brief format

No LLM, no API key — this is a deterministic, extractive pass (first sentence per page),
and the output says so up front ("Read at: sampled"). It's a mechanical stand-in for what
the skill does when an AI coding tool actually follows `SKILL.md` itself.

```bash
cd mini-project
python assistant.py       # or: python3 assistant.py
```

Or run the packaged launcher instead of typing the python command — same program, easier
to hand to someone else:

- **Windows:** double-click `mini-project/run.bat` (or `run.bat` from cmd)
- **macOS/Linux:** `./mini-project/run.sh`

Both just find a Python 3 on `PATH` and start `assistant.py`; `assistant.py` itself is
also directly executable on macOS/Linux (`./assistant.py`, shebang included). If option 3
fails with an import error, `pip install -r mini-project/requirements.txt` (just `pypdf`,
the skill's own dependency).

Pick option 3 and press Enter with no path to summarise the bundled `sample.pdf` (a fake
hall recycling notice — regenerate it any time with `python make_sample_pdf.py`).

## Quick start

```bash
# Mini project - interactive, uses the skill + MCP server together
cd mini-project && ./run.sh      # Windows: run.bat

# MCP server on its own - real handshake, lists tools, calls each one
python part-c-mcp/test_client.py

# PDF summarizer skill on its own
python part-b-skill/my-skill/scripts/extract_pdf.py <file.pdf> --out out.txt
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
- **E** — pushed to GitHub; a second, independent clone confirmed every file is present,
  including `mini-project/assistant.py`.

## Notes

- `mini-project/` deliberately skips the LLM step so it runs with zero setup — the point
  is proving the skill and the MCP server are real, callable pieces, not asking a model to
  role-play them.
- The MCP server is stdlib-only Python (no pip install) so it cannot break on a
  dependency.
- `mini-project/sample.pdf` is generated seed data (see `make_sample_pdf.py`), not a real
  campus document.
