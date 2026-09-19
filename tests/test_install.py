"""Tests for the Turtleneck installer's safety contract.

Run with:  pytest tests/ -q
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("tn_install", ROOT / "scripts" / "install.py")
install = importlib.util.module_from_spec(spec)
sys.modules["tn_install"] = install
spec.loader.exec_module(install)


@pytest.fixture
def project(tmp_path: Path) -> Path:
    p = tmp_path / "proj"
    p.mkdir()
    return p


def actions(report) -> dict[str, str]:
    return {o.platform: o.action for o in report.outcomes}


# --------------------------------------------------------------------------
# refusal / non-destructiveness
# --------------------------------------------------------------------------

def test_bare_install_refuses_foreign_agents_md(project: Path):
    """The headline bug: a pre-existing AGENTS.md must survive a bare install."""
    (project / "AGENTS.md").write_text("# MY EXISTING PROJECT AGENTS.md - do not delete\n")

    report = install.install_to_project(project, ["agents"])

    assert (project / "AGENTS.md").read_text().startswith("# MY EXISTING PROJECT AGENTS.md")
    assert actions(report)["agents"] == install.REFUSED
    assert not (project / "AGENTS.md.turtleneck.bak").exists()


def test_refusal_reports_what_it_protected(project: Path):
    (project / "AGENTS.md").write_text("# MY EXISTING PROJECT AGENTS.md\n")
    report = install.install_to_project(project, ["agents"])
    assert "MY EXISTING PROJECT AGENTS.md" in report.refused[0].detail


def test_fresh_install_creates_file(project: Path):
    report = install.install_to_project(project, ["agents"])
    assert (project / "AGENTS.md").exists()
    assert actions(report)["agents"] == install.CREATE
    assert "Turtleneck" in (project / "AGENTS.md").read_text()


def test_reinstalling_own_file_is_a_noop(project: Path):
    install.install_to_project(project, ["agents"])
    first = (project / "AGENTS.md").read_text()

    report = install.install_to_project(project, ["agents"])

    assert (project / "AGENTS.md").read_text() == first
    assert actions(report)["agents"] == install.SKIPPED


def test_copilot_instructions_are_also_protected(project: Path):
    (project / ".github").mkdir()
    (project / ".github" / "copilot-instructions.md").write_text("# MY COPILOT RULES\n")
    install.install_to_project(project, ["copilot"])
    assert (project / ".github" / "copilot-instructions.md").read_text() == "# MY COPILOT RULES\n"


# --------------------------------------------------------------------------
# --force
# --------------------------------------------------------------------------

def test_force_backs_up_before_overwriting(project: Path):
    (project / "AGENTS.md").write_text("# MINE\n")
    install.install_to_project(project, ["agents"], force=True)

    assert (project / "AGENTS.md").read_text().startswith("# Turtleneck")
    assert (project / "AGENTS.md.turtleneck.bak").read_text() == "# MINE\n"


def test_force_never_loses_data_on_repeat_runs(project: Path):
    """A second --force must not silently discard the previous version."""
    (project / "AGENTS.md").write_text("# VERSION ONE\n")
    install.install_to_project(project, ["agents"], force=True)

    (project / "AGENTS.md").write_text("# VERSION TWO\n")
    install.install_to_project(project, ["agents"], force=True)

    saved = {p.name: p.read_text() for p in project.glob("AGENTS.md.turtleneck.bak*")}
    assert "# VERSION ONE\n" in saved.values()
    assert "# VERSION TWO\n" in saved.values()
    assert len(saved) == 2


# --------------------------------------------------------------------------
# --append
# --------------------------------------------------------------------------

def test_append_preserves_existing_content(project: Path):
    (project / "AGENTS.md").write_text("# MY RULES\n\nDo my things.\n")
    install.install_to_project(project, ["agents"], append=True)

    body = (project / "AGENTS.md").read_text()
    assert body.startswith("# MY RULES")
    assert "Do my things." in body
    assert install.MARK_BEGIN in body and install.MARK_END in body
    assert "Turtleneck" in body


def test_append_is_idempotent(project: Path):
    (project / "AGENTS.md").write_text("# MY RULES\n")
    install.install_to_project(project, ["agents"], append=True)
    once = (project / "AGENTS.md").read_text()

    report = install.install_to_project(project, ["agents"], append=True)
    twice = (project / "AGENTS.md").read_text()

    assert twice == once, "re-running --append must not grow the file"
    assert once.count(install.MARK_BEGIN) == 1
    assert actions(report)["agents"] == install.SKIPPED


def test_append_refreshes_block_without_duplicating(project: Path):
    (project / "AGENTS.md").write_text("# MY RULES\n")
    install.install_to_project(project, ["agents"], append=True)

    stale = (project / "AGENTS.md").read_text().replace("Turtleneck", "Stale")
    (project / "AGENTS.md").write_text(stale)
    install.install_to_project(project, ["agents"], append=True)

    body = (project / "AGENTS.md").read_text()
    assert body.count(install.MARK_BEGIN) == 1
    assert body.startswith("# MY RULES")
    assert "Turtleneck" in body


# --------------------------------------------------------------------------
# --dry-run
# --------------------------------------------------------------------------

def test_dry_run_writes_nothing(project: Path):
    (project / "AGENTS.md").write_text("# MINE\n")
    install.install_to_project(project, ["agents", "cursor"], dry_run=True)

    assert [p.name for p in project.iterdir()] == ["AGENTS.md"]
    assert (project / "AGENTS.md").read_text() == "# MINE\n"


def test_dry_run_still_reports_refusals(project: Path):
    (project / "AGENTS.md").write_text("# MINE\n")
    report = install.install_to_project(project, ["agents"], dry_run=True)
    assert report.refused and report.dry_run


# --------------------------------------------------------------------------
# knowledge base
# --------------------------------------------------------------------------

def test_references_are_installed_so_rule_paths_resolve(project: Path):
    """Every `.turtleneck/references/...` path cited in rules/ must exist after install."""
    install.install_references(project)

    missing = []
    for rule in (ROOT / "rules").iterdir():
        for line in rule.read_text(encoding="utf-8").splitlines():
            for token in line.split("`"):
                if token.startswith(".turtleneck/references/") and token.endswith(".md"):
                    if not (project / token).exists():
                        missing.append(f"{rule.name}: {token}")
    assert missing == [], "rules files cite knowledge base paths that were not installed"


def test_references_exclude_image_captures_by_default(project: Path):
    install.install_references(project)
    assert not list((project / ".turtleneck").rglob("*.png"))
    assert (project / ".turtleneck" / "references" / "design-tokens.md").exists()


def test_with_assets_includes_image_captures(project: Path):
    install.install_references(project, with_assets=True)
    assert list((project / ".turtleneck").rglob("*.png"))


# --------------------------------------------------------------------------
# skill install
# --------------------------------------------------------------------------

def test_skill_install_ships_skill_and_references(project: Path):
    dest = project / ".claude" / "skills" / "turtleneck"
    install.install_skill(dest, dry_run=False, with_assets=False, report=install.Report())

    assert (dest / "SKILL.md").exists()
    assert (dest / "references" / "taste-vs-slop-matrix.md").exists()
    # SKILL.md links to examples/, so they must ship with the skill by default.
    assert (dest / "examples" / "index.html").exists()
    assert not list(dest.rglob("*.png"))
    assert not (dest / ".git").exists()
    assert not (dest / "scripts").exists()


def test_skill_install_with_assets_includes_captures(project: Path):
    dest = project / "turtleneck"
    install.install_skill(dest, dry_run=False, with_assets=True, report=install.Report())
    assert list(dest.rglob("*.png")), "--with-assets should carry the image captures"


def test_skill_install_backs_up_previous_version(project: Path):
    dest = project / "turtleneck"
    dest.mkdir()
    (dest / "SKILL.md").write_text("# OLD SKILL\n")

    install.install_skill(dest, dry_run=False, with_assets=False, report=install.Report())

    assert (project / "turtleneck.turtleneck.bak" / "SKILL.md").read_text() == "# OLD SKILL\n"
    assert "OLD SKILL" not in (dest / "SKILL.md").read_text()


def test_claude_skill_flag_does_not_drop_rules_files(project: Path):
    """--claude-skill alone must not quietly create AGENTS.md."""
    rc = install.main(["--target", str(project), "--claude-skill"])
    assert rc == 0
    assert (project / ".claude" / "skills" / "turtleneck" / "SKILL.md").exists()
    assert not (project / "AGENTS.md").exists()
    assert not (project / ".cursorrules").exists()


# --------------------------------------------------------------------------
# auto-detection
# --------------------------------------------------------------------------

@pytest.mark.parametrize("marker,expected,is_dir", [
    (".cursor", "cursor", True),
    (".github", "copilot", True),
    (".windsurf", "windsurf", True),
    (".claude", "claude", True),
    (".clinerules", "cline", False),
])
def test_autodetect(project: Path, marker: str, expected: str, is_dir: bool):
    path = project / marker
    path.mkdir() if is_dir else path.touch()
    assert expected in install.detect_platforms(project)


def test_autodetect_always_includes_agents(project: Path):
    assert install.detect_platforms(project)[0] == "agents"


# --------------------------------------------------------------------------
# uninstall
# --------------------------------------------------------------------------

def test_uninstall_removes_marker_block_and_keeps_the_rest(project: Path):
    (project / "AGENTS.md").write_text("# MY RULES\n")
    install.install_to_project(project, ["agents"], append=True)

    install.uninstall(project, ["agents"], dry_run=False, report=install.Report())

    body = (project / "AGENTS.md").read_text()
    assert install.MARK_BEGIN not in body
    assert body.startswith("# MY RULES")


def test_uninstall_deletes_a_wholly_turtleneck_file(project: Path):
    install.install_to_project(project, ["agents"])
    install.uninstall(project, ["agents"], dry_run=False, report=install.Report())
    assert not (project / "AGENTS.md").exists()


def test_uninstall_leaves_foreign_files_alone(project: Path):
    (project / "AGENTS.md").write_text("# NOT MINE TO DELETE\n")
    install.uninstall(project, ["agents"], dry_run=False, report=install.Report())
    assert (project / "AGENTS.md").read_text() == "# NOT MINE TO DELETE\n"


def test_uninstall_restores_backup(project: Path):
    (project / "AGENTS.md").write_text("# MINE\n")
    install.install_to_project(project, ["agents"], force=True)
    assert (project / "AGENTS.md").read_text().startswith("# Turtleneck")

    install.uninstall(project, ["agents"], dry_run=False, report=install.Report())

    assert (project / "AGENTS.md").read_text() == "# MINE\n"
    assert not (project / "AGENTS.md.turtleneck.bak").exists()


def test_cli_reports_refusal_with_exit_code_2(project: Path, capsys):
    (project / "AGENTS.md").write_text("# MINE\n")
    rc = install.main(["--target", str(project), "--agents", "--no-references"])
    assert rc == 2
    assert "REFUSED" in capsys.readouterr().out


def test_cli_happy_path_returns_zero(project: Path):
    rc = install.main(["--target", str(project), "--agents", "--no-references"])
    assert rc == 0
    assert (project / "AGENTS.md").exists()
