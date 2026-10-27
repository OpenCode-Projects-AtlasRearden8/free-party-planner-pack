#!/usr/bin/env python3
"""Build every printable in this pack: src/*.html -> printables/*.pdf.

One script, fully local: WeasyPrint renders the HTML/CSS to print-ready,
unbranded PDFs. No network access is needed at build time, and the PDFs
contain no external links, fonts, or images.

Usage:
    python3 build.py                 # build all sheets into printables/
    python3 build.py --out DIR       # build into a different directory
    python3 build.py --only run-of-show six-week-countdown
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pypdf import PdfReader
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
DEFAULT_OUT = ROOT / "printables"

# The single source of truth for the pack's contents and ordering.
SHEETS = [
    {"stem": "six-week-countdown", "title": "Six-Week Countdown"},
    {"stem": "guest-contact-tracker", "title": "Guest & Contact Tracker"},
    {"stem": "potluck-sign-up-card", "title": "Potluck Sign-Up Card"},
    {"stem": "party-budget-one-pager", "title": "Party Budget One-Pager"},
    {"stem": "menu-shopping-grid", "title": "Menu & Shopping Grid"},
    {"stem": "run-of-show", "title": "Day-of Run of Show"},
    {"stem": "thank-you-note-tracker", "title": "Thank-You-Note Tracker"},
    {"stem": "okay-to-cancel-card", "title": "It Is Okay to Cancel"},
]


def verify_pdf(pdf_path: Path, title: str) -> int:
    """Cheap post-build checks: real PDF, enough pages, correct title."""
    data = pdf_path.read_bytes()
    if not data.startswith(b"%PDF-"):
        raise RuntimeError(f"{pdf_path.name}: does not start with a %PDF header")
    if len(data) < 1000:
        raise RuntimeError(f"{pdf_path.name}: suspiciously small ({len(data)} bytes)")

    reader = PdfReader(str(pdf_path))
    page_count = len(reader.pages)
    if page_count < 2:
        raise RuntimeError(
            f"{pdf_path.name}: expected at least 2 pages (usage + sheet), got {page_count}"
        )

    meta = reader.metadata or {}
    pdf_title = str(meta.get("/Title") or "")
    if title not in pdf_title:
        raise RuntimeError(
            f"{pdf_path.name}: PDF title {pdf_title!r} does not contain {title!r}"
        )
    return page_count


def build(out_dir: Path = DEFAULT_OUT, only: list[str] | None = None) -> list[Path]:
    """Render each sheet to PDF. Returns the list of PDFs built."""
    if not SRC.is_dir():
        raise FileNotFoundError(f"missing source directory: {SRC}")

    wanted = [s for s in SHEETS if only is None or s["stem"] in only]
    if not wanted:
        raise ValueError(f"no sheets match --only {only}")

    out_dir.mkdir(parents=True, exist_ok=True)
    built: list[Path] = []
    for sheet in wanted:
        stem, title = sheet["stem"], sheet["title"]
        html_path = SRC / f"{stem}.html"
        if not html_path.is_file():
            raise FileNotFoundError(f"missing source: {html_path}")
        pdf_path = out_dir / f"{stem}.pdf"

        HTML(filename=str(html_path)).write_pdf(target=str(pdf_path))
        pages = verify_pdf(pdf_path, title)
        print(f"  built {stem}.pdf  ({pages} pages)")
        built.append(pdf_path)
    return built


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                        help=f"output directory (default: {DEFAULT_OUT})")
    parser.add_argument("--only", nargs="+", metavar="STEM",
                        help="build only these sheets (file stems)")
    args = parser.parse_args(argv)

    print("Free Party Planner Pack — building PDFs (fully local)...")
    try:
        build(args.out, args.only)
    except Exception as exc:  # surface a clean error, non-zero exit
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Done — {len(args.only) if args.only else len(SHEETS)} PDF(s) in {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
