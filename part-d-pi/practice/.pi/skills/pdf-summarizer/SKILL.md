---
name: pdf-summarizer
description: Use when the user asks to summarise, digest, condense, or "read and tell me the key points of" a PDF — especially a long one (10+ pages), a paper, a report, or a slide deck exported to PDF. Produces a fixed five-part brief (bottom line / key points / section digest with page refs / action items / open questions) and never invents content that is not in the document. Triggers on "summarise this PDF", "what does this paper say", "key points from this report", "digest", "TL;DR of this document".
agent_created: true
---

# PDF summarizer

Purpose: turn a long PDF into a short, faithful brief that someone can act on without
opening the original.

Use when: the user points at a PDF (path, upload, or "this document") and wants a
summary, digest, key points, or TL;DR.

Does not: answer questions about the PDF in free-form prose instead of the brief
format; fill gaps with outside knowledge; quote page numbers it did not read.

## Steps

1. **Extract first, never guess.** Run the bundled extractor before writing anything:
   ```
   python scripts/extract_pdf.py "<abs path to pdf>" --out /tmp/pdf.txt
   ```
   - Exit code 2 = no text layer (a scan). Stop and tell the user it needs OCR.
   - Missing `pypdf` → `python -m pip install pypdf`, then retry.
2. **Size up the document.** Read the `PAGES:` / `CHARS:` header. If the text is longer
   than ~24k chars, do NOT summarise in one pass — extract in slices
   (`--from 1 --to 20`, then `--from 21 --to 40`, …), summarise each slice into 3–5
   bullets, then merge. This is the whole point of the skill: long PDFs defeat
   single-pass reading.
3. **Read the extracted text**, not your assumptions about what the document probably
   says. Slide decks and two-column papers extract out of order — reorder by meaning.
4. **Write the brief in exactly this format.** No preamble, no "here is a summary",
   no trailing commentary:

```
# <document title or filename>

**What this is:** <one sentence: document type, who published it, for whom>
**Length:** <N pages> | **Read at:** <depth used: full / sampled / OCR'd>

## Bottom line
<2-3 sentences. The single most important thing the document says.>

## Key points
- <point — p.N>
- <point — p.N>
- <point — p.N>
(5-8 points. Each is one sentence. Each cites the page it came from.)

## Section digest
| Section / pages | What it says | Why it matters |
|---|---|---|
| <name — p.N-M> | <one sentence> | <one sentence, or "—" if purely background> |

## Action items
- <verb-first item> — owner: <named in doc, or "unassigned"> — due: <date in doc, or "no date given">
(If the document contains no actions or deadlines, write exactly: `None stated in the document.`)

## Open questions
- <something the document asserts without evidence, contradicts, or leaves unclear — p.N>
(If none, write exactly: `None.`)

## What I did not read
<page ranges skipped or unreadable, e.g. "p.40-52 appendices (tables only)". Write "Nothing — full text extracted." if complete.>
```

5. **Stay faithful.** Every bullet must be traceable to extracted text. If the user asks
   a question the PDF does not answer, say so in **Open questions** rather than filling
   the gap. Never cite a page you did not extract.

## Rules that keep it honest

- Page refs are mandatory in Key points and Section digest — they are the audit trail.
- Prefer the document's own words for numbers, dates, and names.
- Tables and figure captions usually carry the finding; if a page is >70% table, say
  "table" in the digest rather than paraphrasing rows.
- If the PDF is under 3 pages, the Section digest may collapse to one row — keep the
  other headings.

## Resources

### scripts/
- `extract_pdf.py` — page-marked text extractor with stats header. Handles pagination
  slices and detects scanned PDFs (exit 2). Requires `pypdf`.
