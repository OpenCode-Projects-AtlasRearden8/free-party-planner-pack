# STATUS — Free Party Planner Pack

Last updated: 2026-10-27

## What was built

A complete, local-first pack of eight warm, print-ready party-planning
printables for small, tender celebrations. Each PDF opens with a friendly
"how to use it" page, then the sheet itself (3 pages per PDF). The PDFs in
`printables/` are unbranded — no names, no logos, no links — and print
cleanly in black & white on US Letter.

| Sheet (in `printables/`) | Purpose |
| --- | --- |
| `six-week-countdown.pdf` | Week-by-week pace from six weeks out to day-of: one focus + one big job per week, with a fill-in detail page |
| `guest-contact-tracker.pdf` | Guest grid (name, contact, RSVP, headcount, notes) + nudges, dietary summary, rides & parking |
| `potluck-sign-up-card.pdf` | Pass-around sign-up card with a "still needed most" strip + host's tally card by category |
| `party-budget-one-pager.pdf` | Estimate/actual/difference budget on one page + friendly trades and a per-person check |
| `menu-shopping-grid.pdf` | Dish menu (whose kitchen, serve time, needs) + shopping grid sorted by aisle with Got-ticks |
| `run-of-show.pdf` | Day-of card: loose time line, the party's arc, first-hour jobs, sideways-moment pockets, good-bye plan |
| `thank-you-note-tracker.pdf` | One row per kind deed after the party (written/sent ticks) + one-sentence openers |
| `okay-to-cancel-card.pdf` | Printed permission for the party to get smaller, move, or pause + short kind messages to send |

Project layout:

- `src/*.html` + `src/base.css` — plain HTML/CSS sources, shared warm styling,
  CSS-drawn checkboxes and write-in lines (no images, no web fonts, no network).
- `build.py` — the one build script: renders every sheet to PDF with
  WeasyPrint, runs per-PDF sanity checks (header, page count, title metadata).
- `tests/test_build.py` — pytest suite that builds every sheet from source and
  verifies valid PDFs (36 tests).
- `printables/` — the generated, ready-to-print PDFs (committed).
- `README.md`, `LICENSE` (MIT), `requirements.txt`, `.gitignore`.

## How to run it

```bash
pip install -r requirements.txt   # weasyprint, pypdf, pytest
python3 build.py                  # build all PDFs into printables/
python3 build.py --out DIR        # build into another directory
python3 build.py --only run-of-show   # build selected sheets (file stems)
python3 -m pytest                 # run the test suite
```

Everything runs offline; nothing signs up, phones home, or fetches a font.

## Verification results

- `python3 build.py` — built all 8 PDFs (3 pages each), no warnings, exit 0.
- `python3 -m pytest` — **36 passed**, including:
  - every sheet rebuilds from source into a valid `%PDF` with 2–4 pages,
  - expected title metadata on every PDF,
  - a "How to use it" usage page naming the sheet, with the print tip,
  - unbranded-content check (no Asdale/Dylan/brand/URL text in any PDF),
  - `SHEETS` in `build.py` matches `src/*.html` exactly,
  - CLI and in-process builds agree; missing-sheet request fails cleanly.
- Spot-rendered pages (potluck card, cancel card, shopping grid, countdown
  detail) via `pdftoppm` and visually checked layout — clean, warm, ink-friendly.

## How it complements the sibling pack

Together with **Calmer Gifting Printables**, there is no overlap: that pack
owns gifts (idea log, gift budget, wish lists, full thank-you note templates,
holiday-week checklist, card/address tracker); this pack owns party planning
(countdown, guests, potluck, party budget, menu/shop, day-of, thanks-tracking,
and the cancel permission card). The packs reference each other by name in the
READMEs only — the PDFs stay standalone and unbranded.

## Known gaps

- No half-letter (A5) variants; sheets are US Letter portrait only (works
  fine with "fit to page" on A4).
- The shopping grid holds 2 item rows per aisle; print the page twice for
  long lists (the sheet itself says so).
- PDFs are text-only by design — no decorative art, no fillable form fields
  (pen-and-paper first).
- No i18n; all sheets are US-English with US Letter geometry.
