#!/usr/bin/env python3
"""Extract text from a PDF for summarising, with page markers and stats.

Usage:
    python extract_pdf.py <file.pdf> [--out out.txt] [--from N] [--to M] [--max-chars 24000]

Prints a header with page count + character count, then the text as
    --- page N ---
    <text>
so the summariser can cite page numbers. Exits with code 2 if the PDF has no
extractable text layer (i.e. it is a scan and needs OCR).
"""

import argparse
import sys

try:
    from pypdf import PdfReader
except ImportError:
    sys.stderr.write(
        "pypdf is missing. Install it first:\n"
        "  python -m pip install pypdf\n"
    )
    raise SystemExit(3)

NO_TEXT_THRESHOLD = 20  # chars per page below which we call it a scan


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--out", help="write output to this file instead of stdout")
    ap.add_argument("--from", dest="start", type=int, default=1, help="first page (1-based)")
    ap.add_argument("--to", dest="end", type=int, default=0, help="last page (0 = last)")
    ap.add_argument("--max-chars", type=int, default=0, help="truncate output (0 = no limit)")
    args = ap.parse_args()

    reader = PdfReader(args.pdf)
    total = len(reader.pages)
    end = args.end or total
    end = min(end, total)

    chunks = []
    empty_pages = 0
    for i in range(args.start - 1, end):
        text = reader.pages[i].extract_text() or ""
        text = text.strip()
        if len(text) < NO_TEXT_THRESHOLD:
            empty_pages += 1
        chunks.append(f"--- page {i + 1} ---\n{text}")

    body = "\n\n".join(chunks)
    chars = len(body)

    if empty_pages == (end - args.start + 1):
        sys.stderr.write(
            "No extractable text layer found in the requested page range. "
            "This is probably a scanned PDF - run OCR first.\n"
        )
        return 2

    header = (
        f"SOURCE: {args.pdf}\n"
        f"PAGES: {total} (extracting {args.start}-{end})\n"
        f"CHARS: {chars}\n"
        f"PAGES WITH (ALMOST) NO TEXT: {empty_pages}\n"
        f"{'-' * 40}\n\n"
    )

    out = header + body
    if args.max_chars and len(out) > args.max_chars:
        out = out[: args.max_chars] + f"\n\n[... TRUNCATED at {args.max_chars} chars ...]"

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"wrote {len(out)} chars to {args.out}")
    else:
        sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
