"""Tests for scripts/check_stress.py (UX Stress & Anti-Slop Gate)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _load_stress():
    spec = importlib.util.spec_from_file_location("stress_gate", ROOT / "scripts" / "check_stress.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["stress_gate"] = mod
    spec.loader.exec_module(mod)
    return mod


stress = _load_stress()


def test_transition_all_is_rejected():
    bad_html = "<style>button { transition: all 0.2s ease; }</style><button>Click</button>"
    problems = stress.check_anti_slop(bad_html)
    assert any("transition: all" in p for p in problems)

    good_html = "<style>button { transition: transform 0.15s ease, opacity 0.15s ease; :focus-visible { outline: 2px solid #000; } }</style><button>Click</button>"
    problems_good = stress.check_anti_slop(good_html)
    assert not any("transition: all" in p for p in problems_good)


def test_missing_focus_visible_is_rejected():
    bad_html = "<style>button { background: red; }</style><button>Test</button>"
    problems = stress.check_anti_slop(bad_html)
    assert any(":focus-visible" in p for p in problems)

    good_html = "<style>button:focus-visible { outline: 2px solid blue; }</style><button>Test</button>"
    problems_good = stress.check_anti_slop(good_html)
    assert not any(":focus-visible" in p for p in problems_good)


def test_radial_blur_blob_is_rejected():
    bad_html = "<style>.blob { background: radial-gradient(#9333ea, transparent); filter: blur(60px); }</style>"
    problems = stress.check_anti_slop(bad_html)
    assert any("blur glow blob" in p for p in problems)

    clean_glass = "<style>.nav { backdrop-filter: blur(20px); }</style>"
    problems_clean = stress.check_anti_slop(clean_glass)
    assert not any("blur glow blob" in p for p in problems_clean)


def test_unlabelled_interactive_controls_rejected():
    bad_button = "<div><button><svg></svg></button></div>"
    problems = stress.check_accessibility(bad_button)
    assert any("Button without text or accessible name" in p for p in problems)

    good_button = "<div><button aria-label='Close menu'><svg></svg></button></div>"
    problems_good = stress.check_accessibility(good_button)
    assert not any("Button without text" in p for p in problems_good)

    bad_input = "<form><input type='text'></form>"
    problems_input = stress.check_accessibility(bad_input)
    assert any("Input field without label" in p for p in problems_input)

    good_input = "<form><input type='text' aria-label='Search queries'></form>"
    problems_input_good = stress.check_accessibility(good_input)
    assert not any("Input field without label" in p for p in problems_input_good)


def test_viewport_meta_required_on_full_documents():
    bad_doc = "<!DOCTYPE html><html><head><title>Test</title></head><body>Hello</body></html>"
    problems = stress.check_layout_containment(bad_doc)
    assert any("missing <meta name=\"viewport\"" in p for p in problems)

    good_doc = "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'><title>Test</title></head><body>Hello</body></html>"
    problems_good = stress.check_layout_containment(good_doc)
    assert not any("missing <meta name=\"viewport\"" in p for p in problems_good)


def test_rigid_width_rejected():
    bad_layout = "<style>.container { width: 1200px; margin: 0 auto; }</style>"
    problems = stress.check_layout_containment(bad_layout)
    assert any("Rigid non-responsive container" in p for p in problems)

    good_layout = "<style>.container { width: 1200px; max-width: 100%; margin: 0 auto; }</style>"
    problems_good = stress.check_layout_containment(good_layout)
    assert not any("Rigid non-responsive container" in p for p in problems_good)


def test_four_states_enforcement():
    partial_html = "<div>Nominal state with list items</div>"
    problems = stress.check_four_states(partial_html)
    assert any("Missing Empty State" in p for p in problems)
    assert any("Missing Loading/Skeleton State" in p for p in problems)
    assert any("Missing Error/Recovery State" in p for p in problems)

    complete_html = """
    <div class="user-list">
      <div data-state="loading" class="skeleton-row">Loading...</div>
      <div data-state="empty" class="empty-state">No items found. Create one.</div>
      <div data-state="error" class="error-state">Failed to load. <button>Retry</button></div>
      <div data-state="nominal" class="item">Item 1</div>
    </div>
    """
    problems_complete = stress.check_four_states(complete_html)
    assert len(problems_complete) == 0


def test_check_gate_passes_on_repository_examples():
    rc = stress.check(verbose=False)
    assert rc == 0
