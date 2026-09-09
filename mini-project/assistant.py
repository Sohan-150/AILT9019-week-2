#!/usr/bin/env python3
"""Course Buddy — a small interactive local assistant.

Wires together the two pieces built earlier this week instead of leaving
them as separate demos:

  - part-c-mcp/server.py     a tiny MCP server -> real date/deadline answers
  - part-b-skill/my-skill/   the pdf-summarizer skill -> a formatted PDF brief

No API key, no network call, no LLM. Everything here is deterministic code
run locally, same spirit as the rest of this week's build.

Run it:
    python mini-project/assistant.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MCP_SERVER = ROOT / "part-c-mcp" / "server.py"
SKILL_DIR = ROOT / "part-b-skill" / "my-skill"
EXTRACTOR = SKILL_DIR / "scripts" / "extract_pdf.py"
SAMPLE_PDF = Path(__file__).resolve().parent / "sample.pdf"


# --------------------------------------------------------------------------
# Part C reused for real: talk to the actual MCP server over stdio JSON-RPC.
# --------------------------------------------------------------------------
class MCPClient:
    """Minimal client for the week2-tiny-tools MCP server (part-c-mcp/server.py)."""

    def __init__(self, server_path: Path):
        self.proc = subprocess.Popen(
            [sys.executable, str(server_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
        )
        self._id = 0
        self._request("initialize", {})
        self._notify("notifications/initialized", {})

    def _request(self, method, params):
        self._id += 1
        msg = {"jsonrpc": "2.0", "id": self._id, "method": method, "params": params}
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()
        line = self.proc.stdout.readline()
        if not line:
            raise RuntimeError("MCP server closed the connection unexpectedly.")
        return json.loads(line)

    def _notify(self, method, params):
        msg = {"jsonrpc": "2.0", "method": method, "params": params}
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()

    def call(self, name: str, arguments: dict | None = None) -> str:
        resp = self._request("tools/call", {"name": name, "arguments": arguments or {}})
        if "error" in resp:
            return f"MCP error: {resp['error']['message']}"
        return resp["result"]["content"][0]["text"]

    def close(self):
        try:
            self.proc.stdin.close()
        except Exception:
            pass
        self.proc.terminate()


# --------------------------------------------------------------------------
# Part B reused for real: run the skill's own extractor, then write the
# brief in the exact format SKILL.md specifies. This is an extractive
# heuristic (first sentence per page), not an LLM reading the document -
# the "Read at" line says so, same honesty rule the skill itself sets out.
# --------------------------------------------------------------------------
PAGE_RE = re.compile(r"^--- page (\d+) ---$")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
DUE_RE = re.compile(r"\b(due|deadline)\b[^.\n]*", re.IGNORECASE)


def _first_sentence(text: str) -> str:
    text = " ".join(text.split())
    if not text:
        return ""
    parts = SENTENCE_RE.split(text)
    return parts[0].strip()


def _parse_pages(extracted: str) -> list[tuple[int, str]]:
    pages: list[tuple[int, str]] = []
    current_no = None
    buf: list[str] = []
    for line in extracted.splitlines():
        m = PAGE_RE.match(line.strip())
        if m:
            if current_no is not None:
                pages.append((current_no, "\n".join(buf).strip()))
            current_no = int(m.group(1))
            buf = []
        else:
            buf.append(line)
    if current_no is not None:
        pages.append((current_no, "\n".join(buf).strip()))
    return pages


def skill_digest(pdf_path: str) -> str:
    if not EXTRACTOR.exists():
        return f"Can't find the skill's extractor at {EXTRACTOR}"
    if not Path(pdf_path).exists():
        return f"No such file: {pdf_path}"

    with tempfile.TemporaryDirectory() as tmp:
        out_path = Path(tmp) / "extracted.txt"
        result = subprocess.run(
            [sys.executable, str(EXTRACTOR), pdf_path, "--out", str(out_path)],
            capture_output=True,
            text=True,
        )
        if result.returncode == 2:
            return "This PDF has no extractable text layer (looks like a scan) - it needs OCR first."
        if result.returncode != 0:
            return f"Extractor failed:\n{result.stderr.strip()}"
        extracted = out_path.read_text(encoding="utf-8")

    header, _, body = extracted.partition("-" * 40)
    total_pages = 0
    for line in header.splitlines():
        if line.startswith("PAGES:"):
            m = re.search(r"PAGES:\s*(\d+)", line)
            if m:
                total_pages = int(m.group(1))

    pages = _parse_pages(body)
    non_empty = [(n, t) for n, t in pages if t]

    title = Path(pdf_path).stem.replace("_", " ").replace("-", " ")

    bottom_line = _first_sentence(non_empty[0][1]) if non_empty else "No text extracted."

    key_points = []
    for page_no, text in non_empty[:8]:
        s = _first_sentence(text)
        if s:
            key_points.append(f"- {s} — p.{page_no}")
    if not key_points:
        key_points = ["- (nothing extracted)"]

    digest_rows = []
    for page_no, text in non_empty:
        s = _first_sentence(text)
        digest_rows.append(f"| p.{page_no} | {s or '—'} | — |")
    if not digest_rows:
        digest_rows = ["| — | — | — |"]

    actions = []
    for page_no, text in non_empty:
        for m in DUE_RE.finditer(text):
            actions.append(f"- {m.group(0).strip()} — p.{page_no}")
    actions_block = "\n".join(actions) if actions else "None stated in the document."

    skipped_pages = total_pages - len(non_empty)
    what_skipped = (
        "Nothing — full text extracted."
        if skipped_pages <= 0
        else f"{skipped_pages} page(s) had no extractable text."
    )

    return f"""# {title}

**What this is:** PDF, extractive digest (no LLM), produced by mini-project/assistant.py
**Length:** {total_pages} pages | **Read at:** sampled — first sentence per page (see notes)

## Bottom line
{bottom_line}

## Key points
{chr(10).join(key_points)}

## Section digest
| Section / pages | What it says | Why it matters |
|---|---|---|
{chr(10).join(digest_rows)}

## Action items
{actions_block}

## Open questions
None. — this pass is mechanical (first-sentence extraction), not a real
read, so it cannot judge what the document leaves unclear. Use an AI
coding tool with SKILL.md loaded for the full five-part brief.

## What I did not read
{what_skipped}
"""


# --------------------------------------------------------------------------
# Interactive loop
# --------------------------------------------------------------------------
MENU = """
Course Buddy — Week 2 mini project
Uses: part-c-mcp/server.py (real MCP tool calls) + part-b-skill's pdf-summarizer skill

1) What's today's date?
2) Days until a deadline (e.g. the proposal, due 2026-09-25)
3) Summarize a PDF (skill-format digest; Enter for the bundled sample.pdf)
4) Quit
"""


def main() -> None:
    print(MENU)
    mcp = MCPClient(MCP_SERVER)
    try:
        while True:
            choice = input("> ").strip()
            if choice == "1":
                print(mcp.call("today"))
            elif choice == "2":
                target = input("Date (YYYY-MM-DD): ").strip()
                print(mcp.call("days_until", {"date": target}))
            elif choice == "3":
                path = input(f"PDF path [{SAMPLE_PDF.name}]: ").strip() or str(SAMPLE_PDF)
                print(skill_digest(path))
            elif choice in ("4", "q", "quit", "exit"):
                break
            else:
                print("Pick 1-4.")
            print(MENU)
    except (EOFError, KeyboardInterrupt):
        pass
    finally:
        mcp.close()


if __name__ == "__main__":
    main()
