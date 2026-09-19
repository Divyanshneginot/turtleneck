"""Tests for the three verification gates.

The gates are the mechanism that stops this repository drifting away from its own protocol,
so they are tested too: each one must pass on the real tree, and must fail when a specific
violation is introduced.

Run with:  pytest tests/ -q
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


contrast = _load("tn_gate_contrast", "check_contrast.py")
consistency = _load("tn_gate_consistency", "check_consistency.py")
examples = _load("tn_gate_examples", "check_examples.py")


# --------------------------------------------------------------------------
# contrast maths
# --------------------------------------------------------------------------

@pytest.mark.parametrize("fg,bg,expected", [
    ("#000000", "#ffffff", 21.0),
    ("#ffffff", "#000000", 21.0),
    ("#777777", "#ffffff", 4.48),
    ("#767676", "#ffffff", 4.54),
])
def test_contrast_ratio_matches_reference_values(fg: str, bg: str, expected: float):
    assert contrast.contrast_ratio(fg, bg) == pytest.approx(expected, abs=0.01)


def test_contrast_ratio_is_symmetric():
    assert contrast.contrast_ratio("#0a2540", "#f6f9fc") == pytest.approx(
        contrast.contrast_ratio("#f6f9fc", "#0a2540")
    )


def test_shorthand_hex_is_accepted():
    assert contrast.contrast_ratio("#fff", "#000") == pytest.approx(21.0)


def test_invalid_hex_raises():
    with pytest.raises(ValueError):
        contrast.hex_to_rgb("not-a-colour")


# --------------------------------------------------------------------------
# gates pass on the real tree
# --------------------------------------------------------------------------

def test_contrast_gate_passes_on_repository():
    assert contrast.check(verbose=False) == 0


def test_consistency_gate_passes_on_repository():
    assert consistency.check() == 0


def test_examples_gate_passes_on_repository():
    assert examples.EXAMPLES, "no examples discovered"
    for path in examples.EXAMPLES:
        assert examples.check_example(path) == [], f"{path.name} violates the protocol"


# --------------------------------------------------------------------------
# contrast gate refuses to let the docs drift
# --------------------------------------------------------------------------

def test_contrast_gate_fails_when_docs_drift(monkeypatch):
    """A pair citing a hex the docs no longer contain must fail, not silently pass."""
    drifted = list(contrast.PAIRS)
    label, _fg, bg, kind, source, locate = drifted[0]
    drifted[0] = (label, "#123456", bg, kind, source, locate)
    monkeypatch.setattr(contrast, "PAIRS", drifted)
    assert contrast.check(verbose=False) == 1


def test_contrast_gate_fails_on_unannotated_decorative_token(monkeypatch, tmp_path):
    doc = tmp_path / "tokens.md"
    doc.write_text("| `border-subtle` | dividers | `#E2E8F0` | `#111827` |\n")
    monkeypatch.setattr(contrast, "ROOT", tmp_path)
    monkeypatch.setattr(
        contrast, "PAIRS",
        [("drifted", "#E2E8F0", "#111827", "decorative", "tokens.md", "`border-subtle`")],
    )
    assert contrast.check(verbose=False) == 1


# --------------------------------------------------------------------------
# examples gate detects specific violations
# --------------------------------------------------------------------------

GOOD_HTML = """<!DOCTYPE html>
<html lang="en">
<head><style>
  :root {
    --canvas: #000000;
    --surface: #111111;
    --text-primary: #f0f0f0;
    --text-muted: #757575;
    --focus-ring: #ffffff;
  }
  button { transition: background-color 0.1s ease, color 0.1s ease; }
  button:focus-visible { outline: 2px solid var(--focus-ring); outline-offset: 2px; }
  @media (prefers-reduced-motion: reduce) {
    *, ::before, ::after { transition-duration: 0.01ms !important; }
  }
</style></head>
<body>
  <button aria-label="Close">x</button>
  <label for="q">Query</label>
  <input id="q" type="text">
</body>
</html>
"""


def _write(tmp_path: Path, html: str) -> Path:
    p = tmp_path / "sample.html"
    p.write_text(html, encoding="utf-8")
    return p


def test_good_example_passes(tmp_path: Path):
    assert examples.check_example(_write(tmp_path, GOOD_HTML)) == []


def test_missing_focus_visible_is_flagged(tmp_path: Path):
    html = GOOD_HTML.replace("button:focus-visible { outline: 2px solid var(--focus-ring); outline-offset: 2px; }", "")
    problems = examples.check_example(_write(tmp_path, html))
    assert any(":focus-visible" in p for p in problems)


def test_invisible_focus_ring_is_flagged(tmp_path: Path):
    html = GOOD_HTML.replace("--focus-ring: #ffffff;", "--focus-ring: #010101;")
    problems = examples.check_example(_write(tmp_path, html))
    assert any("needs >= 3:1" in p for p in problems)


def test_missing_reduced_motion_is_flagged(tmp_path: Path):
    html = GOOD_HTML.replace("@media (prefers-reduced-motion: reduce)", "@media (min-width: 0)")
    problems = examples.check_example(_write(tmp_path, html))
    assert any("prefers-reduced-motion" in p for p in problems)


def test_transition_all_is_flagged(tmp_path: Path):
    html = GOOD_HTML.replace("transition: background-color 0.1s ease, color 0.1s ease;",
                             "transition: all 0.1s ease;")
    problems = examples.check_example(_write(tmp_path, html))
    assert any("transition: all" in p for p in problems)


def test_unnamed_icon_button_is_flagged(tmp_path: Path):
    html = GOOD_HTML.replace('<button aria-label="Close">x</button>', "<button>x</button>")
    problems = examples.check_example(_write(tmp_path, html))
    assert any("accessible name" in p for p in problems)


def test_labelled_input_passes_and_unnamed_input_is_flagged(tmp_path: Path):
    assert examples.check_example(_write(tmp_path, GOOD_HTML)) == []
    html = GOOD_HTML.replace('<label for="q">Query</label>', "<label>Query</label>")
    problems = examples.check_example(_write(tmp_path, html))
    assert any("<input" in p and "accessible name" in p for p in problems)


def test_low_contrast_text_token_is_flagged(tmp_path: Path):
    html = GOOD_HTML.replace("--text-muted: #757575;", "--text-muted: #555555;")
    problems = examples.check_example(_write(tmp_path, html))
    assert any("needs >= 4.5:1" in p for p in problems)


def test_theme_block_missing_focus_ring_is_flagged(tmp_path: Path):
    """A second theme that forgets the ring token must not silently inherit an invisible one."""
    html = GOOD_HTML.replace(
        "</style>",
        '  body[data-archetype="light"] { --canvas: #ffffff; --surface: #f2f2f2; '
        '--text-primary: #000000; }\n</style>',
    )
    problems = examples.check_example(_write(tmp_path, html))
    assert any("undefined in theme block" in p for p in problems)


# --------------------------------------------------------------------------
# consistency gate internals
# --------------------------------------------------------------------------

def test_canonical_pipeline_appears_in_every_pipeline_file():
    for rel in consistency.PIPELINE_FILES:
        body = (ROOT / rel).read_text(encoding="utf-8")
        assert consistency.CANONICAL_PIPELINE in body, rel


def test_every_rules_file_mentions_the_interview():
    for rel in consistency.RULES_FILES:
        body = (ROOT / rel).read_text(encoding="utf-8")
        assert any(m in body for m in consistency.INTERVIEW_MARKERS), rel


def test_no_reference_doc_is_orphaned():
    import re
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    linked = set(re.findall(r"\]\(\./references/([A-Za-z0-9_.-]+\.md)", skill))
    on_disk = {p.name for p in (ROOT / "references").glob("*.md")}
    assert on_disk - linked == set(), "orphaned reference docs"
    assert linked - on_disk == set(), "SKILL.md links to missing docs"
