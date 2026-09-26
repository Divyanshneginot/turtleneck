"""Tests for scripts/taste.py (Adaptive Taste Ledger CLI)."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _load_taste():
    spec = importlib.util.spec_from_file_location("taste_cli", ROOT / "scripts" / "taste.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["taste_cli"] = mod
    spec.loader.exec_module(mod)
    return mod


taste = _load_taste()


def test_init_creates_profile(tmp_path: Path):
    rc = taste.main(["--project", str(tmp_path), "init"])
    assert rc == 0
    target = tmp_path / ".turtleneck" / "taste-profile.json"
    assert target.is_file()

    data = json.loads(target.read_text(encoding="utf-8"))
    assert "rejected_tropes" in data
    assert "preferred_vernacular" in data
    assert "typography" in data
    assert data["contrast_floor"] == 7.0


def test_reject_appends_trope_and_note(tmp_path: Path):
    taste.main(["--project", str(tmp_path), "init"])
    rc = taste.main([
        "--project", str(tmp_path),
        "reject", "purple neon glow",
        "--note", "Hate saturated purple radial blobs"
    ])
    assert rc == 0

    data = json.loads((tmp_path / ".turtleneck" / "taste-profile.json").read_text(encoding="utf-8"))
    assert "purple_neon_glow" in data["rejected_tropes"]
    assert any("purple_neon_glow" in n for n in data["notes"])


def test_prefer_appends_style(tmp_path: Path):
    taste.main(["--project", str(tmp_path), "init"])
    rc = taste.main([
        "--project", str(tmp_path),
        "prefer", "monochrome_swiss_poster",
        "--note", "User requested bold minimalist layout"
    ])
    assert rc == 0

    data = json.loads((tmp_path / ".turtleneck" / "taste-profile.json").read_text(encoding="utf-8"))
    assert "monochrome_swiss_poster" in data["preferred_vernacular"]


def test_note_records_critique(tmp_path: Path):
    taste.main(["--project", str(tmp_path), "init"])
    rc = taste.main([
        "--project", str(tmp_path),
        "note", "Need more negative space on hero container"
    ])
    assert rc == 0

    data = json.loads((tmp_path / ".turtleneck" / "taste-profile.json").read_text(encoding="utf-8"))
    assert any("Need more negative space" in n for n in data["notes"])


def test_json_and_show_output(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    taste.main(["--project", str(tmp_path), "init"])
    taste.main(["--project", str(tmp_path), "reject", "test_trope"])
    capsys.readouterr()  # Flush setup output

    rc = taste.main(["--project", str(tmp_path), "json"])
    assert rc == 0
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert "test_trope" in parsed["rejected_tropes"]

    rc = taste.main(["--project", str(tmp_path), "show"])
    assert rc == 0
    captured_show = capsys.readouterr()
    assert "test_trope" in captured_show.out
