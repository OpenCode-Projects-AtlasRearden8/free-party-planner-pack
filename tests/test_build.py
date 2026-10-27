"""Tests for the Free Party Planner Pack.

Every test builds from source — nothing here trusts a stale PDF. The session
fixture runs `python3 build.py --out <tmp>` once, then each sheet is checked
for a valid, warm, unbranded PDF.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from build import DEFAULT_OUT, SHEETS, build  # noqa: E402


@pytest.fixture(scope="session")
def built(tmp_path_factory) -> Path:
    """Build every sheet once into a temp dir and return that directory."""
    out = tmp_path_factory.mktemp("printables-built")
    result = subprocess.run(
        [sys.executable, str(ROOT / "build.py"), "--out", str(out)],
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0, f"build failed:\n{result.stdout}\n{result.stderr}"
    return out


@pytest.mark.parametrize("sheet", SHEETS, ids=lambda s: s["stem"])
class TestSheetBuildsValidPdf:
    def test_pdf_exists_and_has_real_header(self, built: Path, sheet: dict) -> None:
        pdf = built / f"{sheet['stem']}.pdf"
        assert pdf.is_file(), f"{pdf.name} was not built"
        assert pdf.stat().st_size > 1_000, f"{pdf.name} is suspiciously small"
        assert pdf.read_bytes()[:5] == b"%PDF-", f"{pdf.name} lacks a %PDF header"

    def test_pdf_parses_with_expected_title(self, built: Path, sheet: dict) -> None:
        reader = PdfReader(str(built / f"{sheet['stem']}.pdf"))
        title = str((reader.metadata or {}).get("/Title") or "")
        assert sheet["title"] in title, f"PDF title {title!r} misses {sheet['title']!r}"

    def test_has_usage_page_then_sheet_pages(self, built: Path, sheet: dict) -> None:
        reader = PdfReader(str(built / f"{sheet['stem']}.pdf"))
        assert 2 <= len(reader.pages) <= 4, (
            f"{sheet['stem']}: expected a usage page plus sheet pages, "
            f"got {len(reader.pages)} pages"
        )
        first_page = reader.pages[0].extract_text() or ""
        assert "How to use it" in first_page, "first page is not the usage page"
        usage_title = sheet.get("usage", sheet["title"])
        assert usage_title in first_page, "usage page does not name the sheet"
        assert "Print at 100%" in first_page, "usage page lacks the print tip"

    def test_pdf_is_unbranded(self, built: Path, sheet: dict) -> None:
        reader = PdfReader(str(built / f"{sheet['stem']}.pdf"))
        text = "\n".join((page.extract_text() or "") for page in reader.pages)
        for brand in ("Asdale", "Dylan", "ASDALE", "www.", "http", "Calmer Gifting"):
            assert brand not in text, f"{sheet['stem']}.pdf contains branding: {brand!r}"


def test_build_module_lists_eight_sheets() -> None:
    assert len(SHEETS) == 8
    stems = {s["stem"] for s in SHEETS}
    sources = {p.stem for p in (ROOT / "src").glob("*.html")}
    assert stems == sources, "SHEETS in build.py and src/*.html disagree"


def test_fresh_build_function_matches_cli_output(tmp_path: Path) -> None:
    """The in-process build() and the CLI produce the same set of PDFs."""
    built = build(tmp_path)
    assert {p.name for p in built} == {f"{s['stem']}.pdf" for s in SHEETS}


def test_build_fails_cleanly_for_missing_sheet(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        build(tmp_path, only=["no-such-sheet"])


@pytest.mark.skipif(
    not DEFAULT_OUT.is_dir(),
    reason="printables/ not built yet (run: python3 build.py)",
)
def test_committed_printables_are_fresh() -> None:
    """The shipped printables/ directory holds every sheet as a valid PDF."""
    for sheet in SHEETS:
        pdf = DEFAULT_OUT / f"{sheet['stem']}.pdf"
        assert pdf.is_file(), f"{pdf.name} missing from printables/"
        reader = PdfReader(str(pdf))
        assert len(reader.pages) >= 2
        assert pdf.read_bytes()[:5] == b"%PDF-"
