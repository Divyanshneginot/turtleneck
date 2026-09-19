#!/usr/bin/env python3
"""
Turtleneck Universal Installer

Installs Turtleneck rules and the agent skill into any repository or agent
environment: Claude Code, Cursor, Windsurf, GitHub Copilot, Cline, Google
Antigravity, or generic AGENTS.md consumers.

Safety contract
---------------
`AGENTS.md`, `CLAUDE.md` and `.github/copilot-instructions.md` are shared
standards that a project may already own. This installer therefore never
destroys foreign content:

  * A destination that does not exist is created.
  * A destination that already holds Turtleneck content is refreshed silently.
  * A destination holding anyone else's content is REFUSED by default, and the
    existing first line is printed so you can see what was protected.
  * `--force` overwrites, but only after writing `<dest>.turtleneck.bak`.
  * `--append` inserts a marker-delimited block and leaves all surrounding
    content untouched. It is idempotent.
  * `--dry-run` prints the plan and writes nothing.
  * `--uninstall` removes marker blocks, restores backups, and deletes files
    only when it can prove Turtleneck owns them.

Full-skill installation (`--claude-skill`, `--antigravity`) obeys the same
contract. Ownership of the skill directory is proven with a durable manifest
(`turtleneck-skill-manifest.json`, schema-versioned, one SHA-256 per shipped
relative path) rather than by guessing:

  * An existing skill directory whose files are Turtleneck-owned is refreshed;
    stale manifest-owned files are reconciled (removed), and the manifest is
    rewritten.
  * An existing skill directory holding foreign or mixed content is REFUSED by
    default, listing the exact protected paths.
  * `--force` snapshots the whole directory to a numbered `.turtleneck.bak`,
    never overwriting an existing backup suffix.
  * `--dry-run` parity: nothing is written, every planned action is printed.
  * `--uninstall` removes only manifest-owned files whose content still matches
    the recorded hash, restores the newest backup without overwriting any
    surviving foreign addition, and never deletes a file it cannot prove it owns.

Nothing in this module imports anything outside the standard library.
"""

from __future__ import annotations

import argparse
import filecmp
import hashlib
import json
import os
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
RULES_DIR = ROOT_DIR / "rules"

MARK_BEGIN = "<!-- turtleneck:begin -->"
MARK_END = "<!-- turtleneck:end -->"
BACKUP_SUFFIX = ".turtleneck.bak"
SKILL_MANIFEST = "turtleneck-skill-manifest.json"
MANIFEST_VERSION = 1

# platform -> (destination relative to project root, source relative to repo root)
TARGETS: dict[str, tuple[str, str]] = {
    "agents": ("AGENTS.md", "rules/AGENTS.md"),
    "claude": ("CLAUDE.md", "rules/CLAUDE.md"),
    "cursor": (".cursorrules", "rules/.cursorrules"),
    "windsurf": (".windsurfrules", "rules/.windsurfrules"),
    "copilot": (".github/copilot-instructions.md", "rules/copilot-instructions.md"),
    "cline": (".clinerules", "rules/.clinerules"),
}

RULE_PLATFORMS = ["agents", "claude", "cursor", "windsurf", "copilot", "cline"]

# directories present in the repo that must never be copied into a user's project
SKILL_IGNORES = (".git", "__pycache__", "node_modules", ".venv", ".pytest_cache", "tests")

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

# auto-detect: a marker in the target project implies this platform
AUTODETECT = {
    ".cursor": "cursor",
    ".github": "copilot",
    ".windsurf": "windsurf",
    ".claude": "claude",
    ".clinerules": "cline",
}

CREATE = "create"
REFRESH = "refresh"
APPEND = "append"
REFUSED = "refused"
BACKED_UP = "backed-up"
SKIPPED = "skipped"
DELETED = "deleted"
RESTORED = "restored"


@dataclass
class Outcome:
    """One planned or executed filesystem action."""

    platform: str
    path: Path
    action: str
    detail: str = ""


@dataclass
class Report:
    outcomes: list[Outcome] = field(default_factory=list)
    dry_run: bool = False

    def add(self, platform: str, path: Path, action: str, detail: str = "") -> Outcome:
        o = Outcome(platform, path, action, detail)
        self.outcomes.append(o)
        return o

    @property
    def refused(self) -> list[Outcome]:
        return [o for o in self.outcomes if o.action == REFUSED]

    def print(self) -> None:
        verb = "Would write" if self.dry_run else "Wrote"
        for o in self.outcomes:
            rel = _rel(o.path)
            if o.action == REFUSED:
                print(f"  ! [{o.platform}] REFUSED {rel}")
                print(f"      {o.detail}")
                if o.platform == "skill":
                    print("      Re-run with --force to replace it (the old tree is kept in a .bak).")
                else:
                    print("      Re-run with --force to replace, or --append to merge.")
            elif o.action == BACKED_UP:
                print(f"  + [{o.platform}] backed up {rel} -> {rel}{BACKUP_SUFFIX}")
            else:
                print(f"  {'~' if self.dry_run else '✓'} [{o.platform}] {verb.split()[0].lower()} "
                      f"{o.action} {rel}")


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def _join_paths(rel_paths: list[str], limit: int = 12) -> str:
    shown = rel_paths[:limit]
    text = ", ".join(shown)
    if len(rel_paths) > limit:
        text += f", ... and {len(rel_paths) - limit} more"
    return text


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


# --------------------------------------------------------------------------
# ownership detection (rule files)
# --------------------------------------------------------------------------

def shipped_source(platform: str) -> Path:
    return ROOT_DIR / TARGETS[platform][1]


def owns_content(path: Path) -> bool:
    """True if `path` was written by Turtleneck (verbatim copy or marker block)."""
    if not path.exists():
        return False
    try:
        body = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    if MARK_BEGIN in body:
        return True
    for platform in RULE_PLATFORMS:
        src = shipped_source(platform)
        if src.exists() and filecmp.cmp(path, src, shallow=False):
            return True
    return False


def is_foreign(path: Path) -> bool:
    return path.exists() and not owns_content(path)


def first_line(path: Path) -> str:
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                return line.strip()[:80]
    except (OSError, UnicodeDecodeError):
        return "<unreadable>"
    return "<empty>"


# --------------------------------------------------------------------------
# writing (rule files)
# --------------------------------------------------------------------------

def _backup(path: Path, report: Report, platform: str, dry_run: bool) -> Path:
    """Copy `path` aside before overwriting it.

    Never overwrites an existing backup: the plain `.turtleneck.bak` is reserved for the
    oldest copy, and later ones are numbered so no version is ever silently lost.
    """
    bak = path.with_name(path.name + BACKUP_SUFFIX)
    n = 1
    while bak.exists():
        bak = path.with_name(f"{path.name}{BACKUP_SUFFIX}.{n}")
        n += 1
    if not dry_run:
        shutil.copy2(path, bak)
    report.add(platform, path, BACKED_UP, f"saved to {bak.name}")
    return bak


def _compose(head: str, block: str, tail: str) -> str:
    """Deterministically rebuild a file from its head, marker block and tail.

    Used by both the first append and every later one, so re-running is a no-op.
    """
    parts = [p for p in (head.rstrip(), block.rstrip("\n"), tail.strip()) if p]
    return "\n\n".join(parts) + "\n"


def write_file(
    platform: str,
    dest: Path,
    content: str,
    *,
    force: bool,
    append: bool,
    dry_run: bool,
    report: Report,
) -> Outcome:
    """Create, refresh, append to, or refuse a single destination file."""
    if append:
        block = f"{MARK_BEGIN}\n{content.rstrip()}\n{MARK_END}"
        if dest.exists():
            existing = dest.read_text(encoding="utf-8")
            if MARK_BEGIN in existing and MARK_END in existing:
                head, rest = existing.split(MARK_BEGIN, 1)
                _, tail = rest.split(MARK_END, 1)
                merged = _compose(head, block, tail)
                if merged == existing:
                    return report.add(platform, dest, SKIPPED, "marker block already current")
                if not dry_run:
                    dest.write_text(merged, encoding="utf-8")
                return report.add(platform, dest, APPEND, "marker block replaced in place")
            if is_foreign(dest):
                _backup(dest, report, platform, dry_run)
            merged = _compose(existing, block, "")
            if not dry_run:
                dest.write_text(merged, encoding="utf-8")
            return report.add(platform, dest, APPEND, "block appended, existing content kept")
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(block + "\n", encoding="utf-8")
        return report.add(platform, dest, APPEND, "new file with marker block")

    if dest.exists() and is_foreign(dest):
        if not force:
            return report.add(
                platform,
                dest,
                REFUSED,
                f"existing file is not Turtleneck's (starts: {first_line(dest)!r})",
            )
        _backup(dest, report, platform, dry_run)

    fresh = not dest.exists()
    if dest.exists() and not dry_run:
        if dest.read_text(encoding="utf-8") == content:
            return report.add(platform, dest, SKIPPED, "already up to date")
    if not dry_run:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
    return report.add(platform, dest, CREATE if fresh else REFRESH)


# --------------------------------------------------------------------------
# skill payload + manifest
# --------------------------------------------------------------------------

def skill_payload(with_assets: bool) -> dict[str, Path]:
    """Map every shipped skill file's relative destination to its source path."""
    mapping: dict[str, Path] = {}

    skill_md = ROOT_DIR / "SKILL.md"
    if skill_md.exists():
        mapping["SKILL.md"] = skill_md

    # references/ and examples/ both ship by default — SKILL.md links to both and is hollow
    # without them. Only the heavy image captures are opt-in via --with-assets.
    for sub in ("references", "examples"):
        base = ROOT_DIR / sub
        if not base.exists():
            continue
        for src in sorted(base.rglob("*")):
            if src.is_dir():
                continue
            if any(part in SKILL_IGNORES for part in src.parts):
                continue
            if src.suffix.lower() in IMAGE_SUFFIXES and not with_assets:
                continue
            mapping[f"{sub}/{src.relative_to(base).as_posix()}"] = src
    return mapping


def build_skill_manifest(mapping: dict[str, Path]) -> dict:
    """The durable ownership record written into an installed skill directory."""
    return {
        "schema_version": MANIFEST_VERSION,
        "files": {
            rel: {"sha256": _sha256(src)} for rel, src in sorted(mapping.items())
        },
    }


def manifest_path(dest_root: Path) -> Path:
    return dest_root / SKILL_MANIFEST


def write_skill_manifest(dest_root: Path, mapping: dict[str, Path]) -> None:
    data = build_skill_manifest(mapping)
    dest_root.mkdir(parents=True, exist_ok=True)
    manifest_path(dest_root).write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def read_skill_manifest(dest_root: Path) -> dict | None:
    """Return the installed manifest, or None when absent, tampered or schema-mismatched."""
    path = manifest_path(dest_root)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    if data.get("schema_version") != MANIFEST_VERSION:
        return None
    if not isinstance(data.get("files"), dict):
        return None
    return data


def skill_foreign_paths(
    dest_root: Path, mapping: dict[str, Path], manifest: dict | None
) -> list[str]:
    """Relative paths under an existing skill dir that Turtleneck cannot prove it owns.

    With a manifest, ownership is path level: anything the manifest lists is ours, anything
    else (except the manifest file itself) is foreign. Without a manifest we only trust a
    file that is byte-identical to today's shipped payload.
    """
    if not dest_root.exists():
        return []
    foreign: list[str] = []
    owned = set(manifest["files"]) if manifest else set()
    for p in sorted(dest_root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(dest_root).as_posix()
        if rel == SKILL_MANIFEST:
            continue
        if manifest is not None:
            if rel in owned:
                continue
        else:
            if rel in mapping and _sha256(p) == _sha256(mapping[rel]):
                continue
        foreign.append(rel)
    return foreign


def _backup_tree(dest_root: Path, report: Report, dry_run: bool) -> Path:
    """Snapshot an existing skill directory aside, never reusing a backup suffix."""
    bak = dest_root.with_name(dest_root.name + BACKUP_SUFFIX)
    n = 1
    while bak.exists():
        bak = dest_root.with_name(f"{dest_root.name}{BACKUP_SUFFIX}.{n}")
        n += 1
    if not dry_run:
        shutil.copytree(dest_root, bak)
    report.add("skill", dest_root, BACKED_UP, f"saved to {bak.name}")
    return bak


def latest_skill_backup(dest_root: Path) -> Path | None:
    """The newest backup (`.bak.N` preferred over the oldest plain `.bak`)."""
    base = dest_root.with_name(dest_root.name + BACKUP_SUFFIX)
    if not base.exists():
        return None
    best = base
    n = 1
    while True:
        cand = dest_root.with_name(f"{dest_root.name}{BACKUP_SUFFIX}.{n}")
        if not cand.exists():
            break
        best = cand
        n += 1
    return best


def _restore_tree(
    bak: Path, dest_root: Path, mapping: dict[str, Path], report: Report, dry_run: bool
) -> None:
    """Restore only foreign content from a backup — never reinstall Turtleneck.

    Uninstall removes manifest-owned files first, so any path that still exists after that
    step is a foreign addition and must never be overwritten (nor deleted). A backup file is
    skipped when it is provably Turtleneck's (its hash matches the backup's own manifest, or
    it is byte-identical to today's shipped payload), so restoring never resurrects an old
    Turtleneck tree — only the user's own files lost to `--force`.
    """
    if not bak.exists():
        return
    bak_manifest = read_skill_manifest(bak)
    for src in sorted(bak.rglob("*")):
        if src.is_dir():
            continue
        rel = src.relative_to(bak)
        if rel.name == SKILL_MANIFEST:
            continue
        rel_posix = rel.as_posix()
        if bak_manifest is not None:
            rec = bak_manifest.get("files", {}).get(rel_posix)
            if isinstance(rec, dict) and rec.get("sha256") == _sha256(src):
                continue  # provably Turtleneck-owned in that snapshot
        elif rel_posix in mapping and _sha256(src) == _sha256(mapping[rel_posix]):
            continue  # byte-identical to the shipped payload
        dest = dest_root / rel
        if dest.exists():
            continue
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
        report.add("skill", dest, RESTORED, f"recovered from {bak.name}")


def _remove_empty_dirs(root: Path, protect: set[Path]) -> None:
    """Remove empty directories left behind, never touching a protected path's ancestry."""
    for dirpath, _dirnames, _filenames in os.walk(str(root), topdown=False):
        d = Path(dirpath)
        if d == root or not d.exists():
            continue
        if any(p == d or d in p.parents for p in protect):
            continue
        try:
            d.rmdir()
        except OSError:
            pass


# --------------------------------------------------------------------------
# skill installation
# --------------------------------------------------------------------------

def install_skill(
    dest_root: Path,
    *,
    dry_run: bool = False,
    with_assets: bool = False,
    force: bool = False,
    report: Report | None = None,
) -> Report:
    """Install the full skill behind the same safety contract as rule files.

    Ownership is proven with a durable, schema-versioned manifest. Foreign or mixed content
    is refused unless `force` is set, the whole tree is backed up first, and upgrades
    reconcile stale manifest-owned files instead of leaving them behind.
    """
    report = report or Report(dry_run=dry_run)
    if dry_run:
        report.dry_run = True
    mapping = skill_payload(with_assets)
    manifest = read_skill_manifest(dest_root)
    cleared = False

    if dest_root.exists():
        foreign = skill_foreign_paths(dest_root, mapping, manifest)
        if foreign:
            if not force:
                report.add(
                    "skill",
                    dest_root,
                    REFUSED,
                    "foreign or mixed content present — protected: "
                    + _join_paths(foreign),
                )
                return report
            _backup_tree(dest_root, report, dry_run)
            if not dry_run:
                for child in sorted(dest_root.iterdir()):
                    if child.is_dir():
                        shutil.rmtree(child)
                    else:
                        child.unlink()
            cleared = True

    # Reconcile stale manifest-owned files (they are ours; safe to remove). Skipped after a
    # forced clear, which already emptied the directory.
    if manifest is not None and not cleared:
        current = set(mapping)
        for rel in sorted(manifest["files"]):
            if rel in current:
                continue
            dest = dest_root / rel
            if dest.exists():
                if not dry_run:
                    dest.unlink()
                report.add("skill", dest, DELETED, "stale manifest-owned file removed")

    for rel, src in sorted(mapping.items()):
        dest = dest_root / rel
        if not src.exists():
            report.add("skill", dest, SKIPPED, f"missing source {src.relative_to(ROOT_DIR)}")
            continue
        if dest.exists():
            if _sha256(dest) == _sha256(src):
                report.add("skill", dest, SKIPPED, "up to date")
                continue
            action = REFRESH
        else:
            action = CREATE
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
        report.add("skill", dest, action, f"from {src.relative_to(ROOT_DIR)}")

    mp = manifest_path(dest_root)
    report.add(
        "skill",
        mp,
        REFRESH if manifest else CREATE,
        f"ownership manifest (schema v{MANIFEST_VERSION}, {len(mapping)} files)",
    )
    if not dry_run:
        write_skill_manifest(dest_root, mapping)
    return report


def uninstall_skill(dest_root: Path, *, dry_run: bool = False,
                    report: Report | None = None) -> Report:
    """Remove a skill install using only manifest-proof ownership, then restore any backup.

    Only files listed in the manifest whose current content still matches the recorded hash
    are deleted. Foreign additions (or files modified since install) are never touched, and
    backup restoration never overwrites a surviving file.
    """
    report = report or Report(dry_run=dry_run)
    if dry_run:
        report.dry_run = True
    if not dest_root.exists():
        report.add("skill", dest_root, SKIPPED, "not installed")
        return report

    # Broad payload lets us prove ownership by byte-identity for pre-manifest installs.
    mapping = skill_payload(with_assets=True)
    manifest = read_skill_manifest(dest_root)
    bak = latest_skill_backup(dest_root)

    if manifest is None:
        foreign = skill_foreign_paths(dest_root, mapping, None)
        if foreign:
            report.add(
                "skill",
                dest_root,
                SKIPPED,
                "no manifest — cannot prove ownership of: " + _join_paths(foreign),
            )
            return report

    # Determine the exact set of files we may delete, plus everything we must protect.
    if manifest is not None:
        to_remove: list[Path] = []
        for rel in sorted(manifest["files"]):
            dest = dest_root / rel
            if not dest.exists():
                continue
            recorded = manifest["files"][rel]
            if not isinstance(recorded, dict) or recorded.get("sha256") != _sha256(dest):
                report.add("skill", dest, SKIPPED, "modified since install; left in place")
                continue
            to_remove.append(dest)
    else:
        to_remove = [
            dest_root / rel
            for rel in sorted(mapping)
            if (dest_root / rel).is_file()
        ]

    protect = {
        dest_root / rel
        for rel in skill_foreign_paths(dest_root, mapping, manifest)
    }
    protect |= {dest_root / rel for rel in skill_foreign_paths(dest_root, mapping, None)}
    for dest in to_remove:
        if not dry_run:
            dest.unlink()
        report.add("skill", dest, DELETED, "manifest-owned file removed")

    if manifest_path(dest_root).exists():
        if not dry_run:
            manifest_path(dest_root).unlink()
        report.add("skill", manifest_path(dest_root), DELETED, "ownership manifest removed")

    if not dry_run:
        _remove_empty_dirs(dest_root, protect)
        try:
            dest_root.rmdir()
        except OSError:
            pass

    if bak:
        _restore_tree(bak, dest_root, mapping, report, dry_run)
    return report


# --------------------------------------------------------------------------
# uninstall (rule files)
# --------------------------------------------------------------------------

def uninstall(target_dir: Path, platforms: list[str], *, dry_run: bool, report: Report) -> None:
    for platform in platforms:
        rel_dest, _ = TARGETS[platform]
        dest = target_dir / rel_dest
        bak = dest.with_name(dest.name + BACKUP_SUFFIX)

        if dest.exists():
            body = dest.read_text(encoding="utf-8")
            if MARK_BEGIN in body and MARK_END in body:
                head, rest = body.split(MARK_BEGIN, 1)
                _, tail = rest.split(MARK_END, 1)
                remainder = f"{head.rstrip()}\n{tail.lstrip()}".strip()
                if remainder:
                    if not dry_run:
                        dest.write_text(remainder + "\n", encoding="utf-8")
                    report.add(platform, dest, APPEND, "marker block removed, rest kept")
                else:
                    if not dry_run:
                        dest.unlink()
                    report.add(platform, dest, DELETED, "only the marker block was present")
            elif owns_content(dest):
                if not dry_run:
                    dest.unlink()
                report.add(platform, dest, DELETED, "file was Turtleneck-owned")
            else:
                report.add(platform, dest, SKIPPED, "foreign file left untouched")

        if bak.exists():
            if not dry_run:
                shutil.move(str(bak), str(dest))
            report.add(platform, bak, RESTORED, f"restored to {dest.name}")


# --------------------------------------------------------------------------
# orchestration
# --------------------------------------------------------------------------

def install_references(
    target_dir: Path,
    *,
    dry_run: bool = False,
    with_assets: bool = False,
    force: bool = False,
    report: Report | None = None,
) -> Report:
    """Copy the markdown knowledge base to <target>/.turtleneck/references/.

    Every rules file points agents at `.turtleneck/references/...`. Without this step those
    paths dangle and the installed rules lose the entire craft knowledge base. Existing files
    that differ from the shipped copy are refused unless `force` is set (with a backup).
    """
    report = report or Report(dry_run=dry_run)
    base = ROOT_DIR / "references"
    dest_root = target_dir / ".turtleneck" / "references"

    for src in sorted(base.rglob("*")):
        if src.is_dir():
            continue
        if any(part in SKILL_IGNORES for part in src.parts):
            continue
        if src.suffix.lower() in IMAGE_SUFFIXES and not with_assets:
            continue
        dest = dest_root / src.relative_to(base)
        if dest.exists():
            if not src.exists():
                continue
            if _sha256(dest) == _sha256(src):
                report.add("references", dest, SKIPPED, "up to date")
                continue
            if not force:
                report.add(
                    "references",
                    dest,
                    REFUSED,
                    "existing file differs from the shipped copy",
                )
                continue
            _backup(dest, report, "references", dry_run)
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
        report.add("references", dest, CREATE, f"from references/{src.relative_to(base)}")
    return report


def install_to_project(
    target_dir: Path,
    platforms: list[str],
    *,
    force: bool = False,
    append: bool = False,
    dry_run: bool = False,
    report: Report | None = None,
) -> Report:
    report = report or Report(dry_run=dry_run)
    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    for platform in platforms:
        if platform not in TARGETS:
            continue
        rel_dest, rel_src = TARGETS[platform]
        src = ROOT_DIR / rel_src
        if not src.exists():
            report.add(platform, target_dir / rel_dest, SKIPPED, f"missing source {rel_src}")
            continue
        write_file(
            platform,
            target_dir / rel_dest,
            src.read_text(encoding="utf-8"),
            force=force,
            append=append,
            dry_run=dry_run,
            report=report,
        )
    return report


def detect_platforms(target_dir: Path) -> list[str]:
    found = ["agents"]
    for marker, platform in AUTODETECT.items():
        if (target_dir / marker).exists():
            found.append(platform)
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="install.py",
        description="Install Turtleneck across any AI agent environment, without clobbering "
                    "files you already own.",
    )
    parser.add_argument("--target", "-t", default=".", help="target project directory (default: cwd)")
    parser.add_argument("--all", "-a", action="store_true", help="install rules for every supported agent")
    for platform in RULE_PLATFORMS:
        parser.add_argument(f"--{platform}", action="store_true", help=f"install {TARGETS[platform][0]}")
    parser.add_argument("--claude-skill", action="store_true",
                        help="install the full skill into <target>/.claude/skills/turtleneck/")
    parser.add_argument("--antigravity", action="store_true",
                        help="install the full skill into ~/.gemini/config/skills/turtleneck/")
    parser.add_argument("--with-assets", action="store_true",
                        help="include examples/ and image captures in a skill install")
    parser.add_argument("--no-references", action="store_true",
                        help="do not copy references/ into <target>/.turtleneck/references/")
    parser.add_argument("--force", "-f", action="store_true",
                        help=f"overwrite foreign files/skill dirs after writing a numbered {BACKUP_SUFFIX}")
    parser.add_argument("--append", action="store_true",
                        help="merge into existing files using marker comments instead of replacing")
    parser.add_argument("--dry-run", "-n", action="store_true", help="print the plan, write nothing")
    parser.add_argument("--uninstall", action="store_true",
                        help="remove what Turtleneck installed (pass --claude-skill/--antigravity "
                             "to also remove a skill)")
    args = parser.parse_args(argv)

    target_dir = Path(args.target).resolve()
    report = Report(dry_run=args.dry_run)

    explicit_rules = [p for p in RULE_PLATFORMS if getattr(args, p)]
    skill_only = args.claude_skill or args.antigravity
    if args.all:
        requested = list(RULE_PLATFORMS)
    elif explicit_rules:
        requested = explicit_rules
    elif args.uninstall:
        requested = list(RULE_PLATFORMS)
    elif skill_only:
        # a pure skill install must not quietly drop rules files into the project
        requested = []
    else:
        requested = detect_platforms(target_dir)

    if args.uninstall:
        uninstall(target_dir, requested, dry_run=args.dry_run, report=report)
        kb = target_dir / ".turtleneck"
        if kb.exists():
            if not args.dry_run:
                shutil.rmtree(kb)
            report.add("references", kb, DELETED, "knowledge base removed")
        if args.claude_skill:
            uninstall_skill(target_dir / ".claude" / "skills" / "turtleneck",
                            dry_run=args.dry_run, report=report)
        if args.antigravity:
            uninstall_skill(Path.home() / ".gemini" / "config" / "skills" / "turtleneck",
                            dry_run=args.dry_run, report=report)
    else:
        if requested:
            install_to_project(target_dir, requested, force=args.force,
                               append=args.append, dry_run=args.dry_run, report=report)
        if not args.no_references:
            install_references(target_dir, dry_run=args.dry_run,
                               with_assets=args.with_assets, force=args.force,
                               report=report)

    if args.claude_skill:
        install_skill(target_dir / ".claude" / "skills" / "turtleneck",
                      dry_run=args.dry_run, with_assets=args.with_assets,
                      force=args.force, report=report)

    if args.antigravity:
        install_skill(Path.home() / ".gemini" / "config" / "skills" / "turtleneck",
                      dry_run=args.dry_run, with_assets=args.with_assets,
                      force=args.force, report=report)

    if not report.outcomes:
        print("Nothing to do. Pass a platform flag, --all, --claude-skill or --antigravity.")
        return 0

    print(f"{'Planned' if args.dry_run else 'Installing'} Turtleneck in: {target_dir}")
    report.print()

    if report.refused:
        print(f"\n{len(report.refused)} item(s) left untouched because Turtleneck does not own them.")
        print("Use --force to replace them (a numbered .bak is kept), or --append to merge rule files.")
        return 2

    print("\nTurtleneck installation complete. Senior UI/UX Architect mode active.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
