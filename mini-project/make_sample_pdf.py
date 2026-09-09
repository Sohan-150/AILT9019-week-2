#!/usr/bin/env python3
"""Generate sample.pdf — a tiny 2-page PDF used to demo the pdf-summarizer
skill without needing an external file. Run once; the output is committed
alongside this script so a fresh clone can try the assistant immediately.

    python make_sample_pdf.py
"""

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

OUT = Path(__file__).resolve().parent / "sample.pdf"

PAGE_1 = [
    "AILT9019 Recycling Rules — Hall Notice",
    "",
    "This notice explains what goes in which bin in student halls, effective",
    "this semester. It replaces all earlier printed notices.",
    "",
    "Blue bin: paper, cardboard, flattened boxes. Rinse before binning.",
    "Green bin: glass bottles and jars only. No ceramics or window glass.",
    "Yellow bin: plastic bottles and clean food containers, caps removed.",
    "",
    "Hazardous items (batteries, paint, electronics) do not go in any hall",
    "bin. Drop them at the Facilities Office, Block C, weekdays 9am-5pm.",
    "",
    "Action: floor representatives must relabel bins by Friday, 25 Sep.",
    "Owner: Floor Rep. Due: 2026-09-25.",
]

PAGE_2 = [
    "Frequently asked questions",
    "",
    "Q: What if a bin is already full?",
    "A: Use the nearest overflow bin in the ground-floor lobby, not the floor.",
    "",
    "Q: Are pizza boxes recyclable?",
    "A: Only if free of grease and food residue; otherwise general waste.",
    "",
    "Q: Who do I ask if a rule is not covered here?",
    "A: Building staff at the ground-floor desk, not Facilities Office.",
    "",
    "This document does not cover hazardous-waste disposal procedures or",
    "override any instruction given directly by building staff.",
]


def draw_page(c, lines, page_no, total):
    c.setFont("Helvetica", 11)
    y = 800
    for line in lines:
        c.drawString(60, y, line)
        y -= 18
    c.setFont("Helvetica", 8)
    c.drawString(60, 40, f"page {page_no} of {total}")
    c.showPage()


def main():
    c = canvas.Canvas(str(OUT), pagesize=A4)
    draw_page(c, PAGE_1, 1, 2)
    draw_page(c, PAGE_2, 2, 2)
    c.save()
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
