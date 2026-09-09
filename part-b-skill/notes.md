# Part B · My first skill — acceptance

## The skill
`pdf-summarizer` — summarises long PDFs into a fixed five-part brief.

Two copies exist on purpose:
| Location | Why |
|---|---|
| `~/.workbuddy-ai/skills/pdf-summarizer/SKILL.md` | the installed one the tool actually loads |
| `my-skill/SKILL.md` (this folder) | the hand-built one the lab asks for |

They are identical, which is the point of Part D: a skill is a portable file, not a
feature of one tool.

## What the SKILL.md specifies
- **Purpose:** turn a long PDF into a short faithful brief.
- **Use when:** user points at a PDF and wants a summary / digest / key points / TL;DR.
- **Does not:** answer in free-form prose; invent content; cite pages it did not read.
- **Steps:** extract text first with `scripts/extract_pdf.py` → check size → slice any
  document over ~24k chars → write the brief in the exact 7-heading template.
- **Hard rule:** every key point carries a page reference (`— p.N`) as an audit trail.

## Test run
Ran it on `Week_02_Build_Start.pdf` (6 pages, 12,557 chars):

```
python scripts/extract_pdf.py ".../Week_02_Build_Start.pdf" --out extracted-week2.txt
```
→ `wrote 12726 chars`, exit 0, `PAGES WITH (ALMOST) NO TEXT: 0`.

Output: `test-output.md`.

Edge cases verified:
- **Scanned / no-text-layer PDF** → extractor exits with code **2** and says "run OCR
  first" instead of hallucinating a summary. (Tested with a deliberately blank PDF.)
- **Long-document slicing** → `--from 5 --to 6` extracted only 4,208 chars, so a 200-page
  PDF can be chunked. Output: `slice-p5-6.txt`.

## Acceptance
The output in `test-output.md` follows the SKILL.md template exactly — `Bottom line`,
`Key points` (each with a page ref), `Section digest` table, `Action items` in
`verb — owner — due` form, `Open questions`, and `What I did not read` — with no
preamble and no trailing commentary. The `Action items` and `Open questions` headings
used the literal fallback strings the skill defines ("None stated in the document." /
"Nothing — full text extracted.") where they applied.

**What I learned:** the value is not "a prompt that says summarise". It's the
*constraints* — extract before writing, cite pages, declare what you skipped. Those turn
a plausible-sounding summary into a checkable one.
