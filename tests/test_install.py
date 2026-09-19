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
    (project / "AGENTS.md").write_text("# MY EXISTING PROJECT AGENTS.md - do not delete\n", encoding="utf-8")

    report = install.install_to_project(project, ["agents"])

    assert (project / "AGENTS.md").read_text(encoding="utf-8").startswith("# MY EXISTING PROJECT AGENTS.md")
    assert actions(report)["agents"] == install.REFUSED
    assert not (project / "AGENTS.md.turtleneck.bak").exists()


def test_refusal_reports_what_it_protected(project: Path):
    (project / "AGENTS.md").write_text("# MY EXISTING PROJECT AGENTS.md\n", encoding="utf-8")
    report = install.install_to_project(project, ["agents"])
    assert "MY EXISTING PROJECT AGENTS.md" in report.refused[0].detail


def test_fresh_install_creates_file(project: Path):
    report = install.install_to_project(project, ["agents"])
    assert (project / "AGENTS.md").exists()
    assert actions(report)["agents"] == install.CREATE
    assert "Turtleneck" in (project / "AGENTS.md").read_text(encoding="utf-8")


def test_reinstalling_own_file_is_a_noop(project: Path):
    install.install_to_project(project, ["agents"])
    first = (project / "AGENTS.md").read_text(encoding="utf-8")

    report = install.install_to_project(project, ["agents"])

    assert (project / "AGENTS.md").read_text(encoding="utf-8") == first
    assert actions(report)["agents"] == install.SKIPPED


def test_copilot_instructions_are_also_protected(project: Path):
    (project / ".github").mkdir()
    (project / ".github" / "copilot-instructions.md").write_text("# MY COPILOT RULES\n", encoding="utf-8")
    install.install_to_project(project, ["copilot"])
    assert (project / ".github" / "copilot-instructions.md").read_text(encoding="utf-8") == "# MY COPILOT RULES\n"


# --------------------------------------------------------------------------
# --force
# --------------------------------------------------------------------------

def test_force_backs_up_before_overwriting(project: Path):
    (project / "AGENTS.md").write_text("# MINE\n", encoding="utf-8")
    install.install_to_project(project, ["agents"], force=True)

    assert (project / "AGENTS.md").read_text(encoding="utf-8").startswith("# Turtleneck")
    assert (project / "AGENTS.md.turtleneck.bak").read_text(encoding="utf-8") == "# MINE\n"


def test_force_never_loses_data_on_repeat_runs(project: Path):
    """A second --force must not silently discard the previous version."""
    (project / "AGENTS.md").write_text("# VERSION ONE\n", encoding="utf-8")
    install.install_to_project(project, ["agents"], force=True)

    (project / "AGENTS.md").write_text("# VERSION TWO\n", encoding="utf-8")
    install.install_to_project(project, ["agents"], force=True)

    saved = {p.name: p.read_text(encoding="utf-8") for p in project.glob("AGENTS.md.turtleneck.bak*")}
    assert "# VERSION ONE\n" in saved.values()
    assert "# VERSION TWO\n" in saved.values()
    assert len(saved) == 2


# --------------------------------------------------------------------------
# --append
# --------------------------------------------------------------------------

def test_append_preserves_existing_content(project: Path):
    (project / "AGENTS.md").write_text("# MY RULES\n\nDo my things.\n", encoding="utf-8")
    install.install_to_project(project, ["agents"], append=True)

    body = (project / "AGENTS.md").read_text(encoding="utf-8")
    assert body.startswith("# MY RULES")
    assert "Do my things." in body
    assert install.MARK_BEGIN in body and install.MARK_END in body
    assert "Turtleneck" in body


def test_append_is_idempotent(project: Path):
    (project / "AGENTS.md").write_text("# MY RULES\n", encoding="utf-8")
    install.install_to_project(project, ["agents"], append=True)
    once = (project / "AGENTS.md").read_text(encoding="utf-8")

    report = install.install_to_project(project, ["agents"], append=True)
    twice = (project / "AGENTS.md").read_text(encoding="utf-8")

    assert twice == once, "re-running --append must not grow the file"
    assert once.count(install.MARK_BEGIN) == 1
    assert actions(report)["agents"] == install.SKIPPED


def test_append_refreshes_block_without_duplicating(project: Path):
    (project / "AGENTS.md").write_text("# MY RULES\n", encoding="utf-8")
    install.install_to_project(project, ["agents"], append=True)

    stale = (project / "AGENTS.md").read_text(encoding="utf-8").replace("Turtleneck", "Stale")
    (project / "AGENTS.md").write_text(stale, encoding="utf-8")
    install.install_to_project(project, ["agents"], append=True)

    body = (project / "AGENTS.md").read_text(encoding="utf-8")
    assert body.count(install.MARK_BEGIN) == 1
    assert body.startswith("# MY RULES")
    assert "Turtleneck" in body


# --------------------------------------------------------------------------
# --dry-run
# --------------------------------------------------------------------------

def test_dry_run_writes_nothing(project: Path):
    (project / "AGENTS.md").write_text("# MINE\n", encoding="utf-8")
    install.install_to_project(project, ["agents", "cursor"], dry_run=True)

    assert [p.name for p in project.iterdir()] == ["AGENTS.md"]
    assert (project / "AGENTS.md").read_text(encoding="utf-8") == "# MINE\n"


def test_dry_run_still_reports_refusals(project: Path):
    (project / "AGENTS.md").write_text("# MINE\n", encoding="utf-8")
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


def test_skill_install_refuses_foreign_content_by_default(project: Path):
    """A pre-existing skill dir with foreign content must not be clobbered silently.

    This replaced the old behaviour (unconditional backup + overwrite) with the same
    refuse-by-default contract the rule files get.
    """
    dest = project / "turtleneck"
    dest.mkdir()
    (dest / "SKILL.md").write_text("# OLD SKILL\n", encoding="utf-8")

    report = install.install_skill(dest, dry_run=False, with_assets=False,
                                   report=install.Report())

    assert report.refused
    assert (dest / "SKILL.md").read_text(encoding="utf-8") == "# OLD SKILL\n"
    assert not (project / "turtleneck.turtleneck.bak").exists()


def test_skill_install_force_backs_up_previous_version(project: Path):
    dest = project / "turtleneck"
    dest.mkdir()
    (dest / "SKILL.md").write_text("# OLD SKILL\n", encoding="utf-8")

    install.install_skill(dest, dry_run=False, with_assets=False, force=True,
                          report=install.Report())

    assert (project / "turtleneck.turtleneck.bak" / "SKILL.md").read_text(encoding="utf-8") == "# OLD SKILL\n"
    assert "OLD SKILL" not in (dest / "SKILL.md").read_text(encoding="utf-8")


def test_claude_skill_flag_does_not_drop_rules_files(project: Path):
    """--claude-skill alone must not quietly create AGENTS.md."""
    rc = install.main(["--target", str(project), "--claude-skill"])
    assert rc == 0
    assert (project / ".claude" / "skills" / "turtleneck" / "SKILL.md").exists()
    assert not (project / "AGENTS.md").exists()
    assert not (project / ".cursorrules").exists()


# --------------------------------------------------------------------------
# skill safety contract (manifest ownership, refusal, backups, uninstall)
# --------------------------------------------------------------------------

def _skill_dest(project: Path) -> Path:
    return project / "turtleneck"


def _install_skill(project: Path, **kwargs) -> "install.Report":
    return install.install_skill(_skill_dest(project), report=install.Report(), **kwargs)


def test_skill_install_writes_ownership_manifest(project: Path):
    _install_skill(project)
    data = install.read_skill_manifest(_skill_dest(project))
    assert data is not None
    assert data["schema_version"] == install.MANIFEST_VERSION
    assert "SKILL.md" in data["files"]
    assert set(data["files"]["SKILL.md"]) == {"sha256"}


def test_skill_install_refreshes_own_files_without_backup_or_refusal(project: Path):
    _install_skill(project)
    report = _install_skill(project)
    assert not report.refused
    assert all(o.action != install.BACKED_UP for o in report.outcomes)
    actions = {o.action for o in report.outcomes}
    assert install.REFRESH in actions or install.SKIPPED in actions


def test_skill_install_refuses_foreign_file(project: Path):
    dest = _skill_dest(project)
    dest.mkdir()
    (dest / "SKILL.md").write_text("# MY EXISTING SKILL\n", encoding="utf-8")

    report = _install_skill(project)

    assert report.refused
    assert "SKILL.md" in report.refused[0].detail
    assert (dest / "SKILL.md").read_text(encoding="utf-8") == "# MY EXISTING SKILL\n"
    assert not (project / "turtleneck.turtleneck.bak").exists()


def test_skill_install_refuses_mixed_content_and_names_protected_paths(project: Path):
    """A dir that's mostly ours plus one foreign addition must be refused by default."""
    _install_skill(project)
    dest = _skill_dest(project)
    foreign_file = dest / "references" / "my-own-capture.png"
    foreign_file.parent.mkdir(parents=True, exist_ok=True)
    foreign_file.write_bytes(b"user bytes")

    report = _install_skill(project)

    assert report.refused
    assert "my-own-capture.png" in report.refused[0].detail
    assert foreign_file.read_bytes() == b"user bytes"


def test_skill_install_force_backs_up_whole_tree(project: Path):
    dest = _skill_dest(project)
    dest.mkdir()
    (dest / "SKILL.md").write_text("# OLD SKILL\n", encoding="utf-8")
    (dest / "team-notes.md").write_text("keep me\n", encoding="utf-8")

    install.install_skill(dest, force=True, report=install.Report())

    bak = project / "turtleneck.turtleneck.bak"
    assert (bak / "SKILL.md").read_text(encoding="utf-8") == "# OLD SKILL\n"
    assert (bak / "team-notes.md").read_text(encoding="utf-8") == "keep me\n"
    assert (dest / "SKILL.md").read_text(encoding="utf-8").startswith("---")


def test_skill_install_force_never_overwrites_an_existing_backup(project: Path):
    def foreign_install(tag: str) -> None:
        dest = _skill_dest(project)
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "sentinel.md").write_text(f"# {tag}\n", encoding="utf-8")
        report = install.install_skill(dest, force=True, report=install.Report())
        assert not report.refused

    foreign_install("FIRST")
    foreign_install("SECOND")

    baks = sorted(p.name for p in project.glob("turtleneck.turtleneck.bak*"))
    assert baks == ["turtleneck.turtleneck.bak", "turtleneck.turtleneck.bak.1"]
    assert (project / "turtleneck.turtleneck.bak" / "sentinel.md").read_text(encoding="utf-8") == "# FIRST\n"
    assert (project / "turtleneck.turtleneck.bak.1" / "sentinel.md").read_text(encoding="utf-8") == "# SECOND\n"


def test_skill_install_dry_run_writes_nothing_and_reports_refusals(project: Path):
    dest = _skill_dest(project)
    dest.mkdir()
    (dest / "notes.md").write_text("mine\n", encoding="utf-8")

    report = install.install_skill(dest, dry_run=True, report=install.Report())

    assert report.dry_run and report.refused
    assert [p.name for p in project.iterdir()] == ["turtleneck"]
    assert [p.name for p in dest.iterdir()] == ["notes.md"]


def test_skill_install_dry_run_fresh_reports_plan_only(project: Path):
    report = install.install_skill(_skill_dest(project), dry_run=True, report=install.Report())
    assert report.dry_run
    assert not _skill_dest(project).exists()
    assert {o.action for o in report.outcomes} == {install.CREATE}


def test_skill_install_reconciles_stale_owned_files(project: Path):
    """Files the manifest still lists but that no longer ship must be removed."""
    dest = _skill_dest(project)
    _install_skill(project)

    stale = dest / "references" / "removed-in-newer-release.md"
    stale.parent.mkdir(parents=True, exist_ok=True)
    stale.write_text("# obsolete\n", encoding="utf-8")
    data = install.read_skill_manifest(dest)
    data["files"]["references/removed-in-newer-release.md"] = {
        "sha256": install._sha256(stale),
    }
    install.manifest_path(dest).write_text(
        __import__("json").dumps(data, sort_keys=True) + "\n", encoding="utf-8"
    )

    report = _install_skill(project)

    assert not stale.exists()
    assert any("stale" in o.detail for o in report.outcomes)
    # the stale entry is gone from the rewritten manifest
    assert "references/removed-in-newer-release.md" not in install.read_skill_manifest(dest)["files"]


def test_skill_install_treats_tampered_manifest_as_no_manifest(project: Path):
    """A tampered/malformed manifest must not grant false ownership."""
    _install_skill(project)
    dest = _skill_dest(project)
    assert install.read_skill_manifest(dest) is not None
    (install.manifest_path(dest)).write_text('{"schema_version": 999, "files": {}}\n', encoding="utf-8")
    assert install.read_skill_manifest(dest) is None


def test_skill_install_tampered_manifest_never_deletes_foreign_file(project: Path):
    """Tampering the manifest to claim a foreign path must not cause its deletion."""
    _install_skill(project)
    dest = _skill_dest(project)
    victim = dest / "victim.md"
    victim.write_text("# do not delete\n", encoding="utf-8")

    manifest = install.read_skill_manifest(dest)
    manifest["files"]["victim.md"] = {"sha256": "0" * 64}
    install.manifest_path(dest).write_text(
        __import__("json").dumps(manifest, sort_keys=True) + "\n", encoding="utf-8"
    )

    install.uninstall_skill(dest, report=install.Report())

    assert victim.read_text(encoding="utf-8") == "# do not delete\n"


def test_skill_uninstall_removes_only_owned_files_and_preserves_foreign(project: Path):
    _install_skill(project)
    dest = _skill_dest(project)
    (dest / "team-notes.md").write_text("team\n", encoding="utf-8")

    install.uninstall_skill(dest, report=install.Report())

    assert not (dest / "SKILL.md").exists()
    assert not (dest / "references").exists()
    assert not (dest / "examples").exists()
    assert (dest / "team-notes.md").read_text(encoding="utf-8") == "team\n"
    assert not (dest / install.SKILL_MANIFEST).exists()


def test_skill_uninstall_leaves_modified_files_in_place(project: Path):
    _install_skill(project)
    dest = _skill_dest(project)
    (dest / "SKILL.md").write_text("# user edited after install\n", encoding="utf-8")

    install.uninstall_skill(dest, report=install.Report())

    assert (dest / "SKILL.md").read_text(encoding="utf-8") == "# user edited after install\n"


def test_skill_uninstall_restores_foreign_content_from_backup(project: Path):
    """Uninstall after --force returns the user's old files and removes Turtleneck's."""
    dest = _skill_dest(project)
    dest.mkdir()
    (dest / "SKILL.md").write_text("# MY SKILL\n", encoding="utf-8")
    (dest / "team-notes.md").write_text("team\n", encoding="utf-8")

    install.install_skill(dest, force=True, report=install.Report())
    install.uninstall_skill(dest, report=install.Report())

    assert (dest / "SKILL.md").read_text(encoding="utf-8") == "# MY SKILL\n"
    assert (dest / "team-notes.md").read_text(encoding="utf-8") == "team\n"
    assert not (dest / "references").exists()
    assert not (dest / install.SKILL_MANIFEST).exists()


def test_skill_uninstall_needs_manifest_for_an_unknown_tree(project: Path):
    """Without a manifest, uninstall cannot prove ownership and must touch nothing."""
    dest = _skill_dest(project)
    dest.mkdir()
    (dest / "keep.md").write_text("keep\n", encoding="utf-8")

    report = install.uninstall_skill(dest, report=install.Report())

    assert all(o.action == install.SKIPPED for o in report.outcomes)
    assert (dest / "keep.md").read_text(encoding="utf-8") == "keep\n"
    assert (dest / install.SKILL_MANIFEST).exists() is False


def test_skill_uninstall_dry_run_touches_nothing(project: Path):
    _install_skill(project)
    dest = _skill_dest(project)
    (dest / "team-notes.md").write_text("team\n", encoding="utf-8")

    report = install.uninstall_skill(dest, dry_run=True, report=install.Report())

    assert report.dry_run
    assert (dest / "SKILL.md").exists()
    assert (dest / "team-notes.md").read_text(encoding="utf-8") == "team\n"


def test_skill_uninstall_never_deletes_an_unrelated_file_at_dest_parent(project: Path):
    """Only the skill dir is affected; siblings (including backups) stay untouched."""
    _install_skill(project)
    dest = _skill_dest(project)
    sibling = project / "unrelated.md"
    sibling.write_text("sibling\n", encoding="utf-8")

    install.uninstall_skill(dest, report=install.Report())

    assert sibling.read_text(encoding="utf-8") == "sibling\n"


def test_skill_is_deterministic_and_idempotent(project: Path):
    """Two identical installs onto an empty dir produce byte-identical trees and manifests."""
    dest = _skill_dest(project)

    install.install_skill(dest, report=install.Report())
    first = {p: p.read_bytes() for p in dest.rglob("*") if p.is_file()}

    install.install_skill(dest, report=install.Report())
    second = {p: p.read_bytes() for p in dest.rglob("*") if p.is_file()}

    assert first == second
    assert install.read_skill_manifest(dest) == install.read_skill_manifest(dest)


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
    (project / "AGENTS.md").write_text("# MY RULES\n", encoding="utf-8")
    install.install_to_project(project, ["agents"], append=True)

    install.uninstall(project, ["agents"], dry_run=False, report=install.Report())

    body = (project / "AGENTS.md").read_text(encoding="utf-8")
    assert install.MARK_BEGIN not in body
    assert body.startswith("# MY RULES")


def test_uninstall_deletes_a_wholly_turtleneck_file(project: Path):
    install.install_to_project(project, ["agents"])
    install.uninstall(project, ["agents"], dry_run=False, report=install.Report())
    assert not (project / "AGENTS.md").exists()


def test_uninstall_leaves_foreign_files_alone(project: Path):
    (project / "AGENTS.md").write_text("# NOT MINE TO DELETE\n", encoding="utf-8")
    install.uninstall(project, ["agents"], dry_run=False, report=install.Report())
    assert (project / "AGENTS.md").read_text(encoding="utf-8") == "# NOT MINE TO DELETE\n"


def test_uninstall_restores_backup(project: Path):
    (project / "AGENTS.md").write_text("# MINE\n", encoding="utf-8")
    install.install_to_project(project, ["agents"], force=True)
    assert (project / "AGENTS.md").read_text(encoding="utf-8").startswith("# Turtleneck")

    install.uninstall(project, ["agents"], dry_run=False, report=install.Report())

    assert (project / "AGENTS.md").read_text(encoding="utf-8") == "# MINE\n"
    assert not (project / "AGENTS.md.turtleneck.bak").exists()


def test_cli_reports_refusal_with_exit_code_2(project: Path, capsys):
    (project / "AGENTS.md").write_text("# MINE\n", encoding="utf-8")
    rc = install.main(["--target", str(project), "--agents", "--no-references"])
    assert rc == 2
    assert "REFUSED" in capsys.readouterr().out


def test_cli_happy_path_returns_zero(project: Path):
    rc = install.main(["--target", str(project), "--agents", "--no-references"])
    assert rc == 0
    assert (project / "AGENTS.md").exists()
