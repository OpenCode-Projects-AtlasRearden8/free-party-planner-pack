# Free Party Planner Pack

Free, warm, print-ready PDF helpers for planning small, tender celebrations.
Eight printable sheets you can print at home, fill in with a pen, and lose
gracefully to a dropped slice of cake. The PDFs are unbranded, work in black
& white, and everything is built locally from plain HTML/CSS — no accounts,
no tracking, nothing to sign up for, nothing online.

## What's inside (`printables/`)

| PDF | What it's for |
| --- | --- |
| `six-week-countdown.pdf` | Week-by-week pace from six weeks out to the day of — one focus and one big job per week. |
| `guest-contact-tracker.pdf` | Names, contact, RSVPs, headcounts and dietary notes, plus rides & parking planning. |
| `potluck-sign-up-card.pdf` | A pass-around sign-up card for guests, plus your own category-by-category tally page. |
| `party-budget-one-pager.pdf` | Estimate vs. actual for the whole party on one page, with friendly trades for tight weeks. |
| `menu-shopping-grid.pdf` | The dish menu (who's cooking it, what it needs) and a shopping grid sorted by aisles. |
| `run-of-show.pdf` | The day-of card: a loose time line, first-hour jobs, plan-B pockets, and a good-bye plan. |
| `thank-you-note-tracker.pdf` | One row per kind deed after the party — written and sent — with one-sentence openers. |
| `okay-to-cancel-card.pdf` | Printed permission for the party to get smaller, move, or pause, plus kind words to send. |

Every PDF starts with a warm "how to use it" page, then the sheet itself.

## Pairs with the Calmer Gifting Printables

This pack covers *planning* a small party. The companion pack
**Calmer Gifting Printables** covers the *gift* side of celebrating —
gift-idea logs, gift budgets, kids' wish lists, fill-in-the-blank thank-you
note templates, and an address book for holiday cards — so the two packs
overlap on purpose about zero percent. Keep one on the fridge and one in the
kitchen folder; between them, a whole season stays calm.

## Building the PDFs

One script builds every sheet from `src/*.html` + `src/base.css` using
[WeasyPrint](https://weasyprint.org/):

```bash
pip install -r requirements.txt   # weasyprint, pypdf, pytest
python3 build.py                  # renders all sheets into printables/
```

Options:

```bash
python3 build.py --out somedir                # build somewhere else
python3 build.py --only run-of-show           # build selected sheets (file stems)
```

The build is fully local: no network requests, no web fonts, no images.
PDFs are US Letter — print at 100% ("Actual size"), portrait.

## Running the tests

```bash
python3 -m pytest
```

The suite builds every sheet from source into a temp directory and verifies
that each one produces a valid PDF with a usage page, correct title metadata,
and no branding anywhere in the text.

## Editing a sheet

Sources are plain HTML in `src/`, sharing `src/base.css`. Change the words or
rows you like, run `python3 build.py`, and the PDFs regenerate. The list of
sheets in `build.py` (`SHEETS`) is the single source of truth for what gets
built and in what order.

## License & credits

Released under the MIT License — see [LICENSE](LICENSE).
Copyright (c) 2026 Asdale Dynamics, LLC.

Built with care by **Asdale Dynamics, LLC** — beginner-friendly AI guides,
books, and practical tools from Dylan Asdale (*The Massive AI Manual*), at
[dylanasdale.github.io](https://dylanasdale.github.io).
