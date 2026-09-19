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

Nothing in this module imports anything outside the standard library.
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
RULES_DIR = ROOT_DIR / "rules"

MARK_BEGIN = "<!-- turtleneck:begin -->"
MARK_END = "<!-- turtleneck:end -->"
BACKUP_SUFFIX = ".turtleneck.bak"

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
                print(f"      Re-run with --force to replace, or --append to merge.")
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


# --------------------------------------------------------------------------
# ownership detection
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
# writing
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
# skill installation
# --------------------------------------------------------------------------

def install_skill(dest_root: Path, *, dry_run: bool, with_assets: bool, report: Report) -> None:
    """Copy SKILL.md + references/ + examples/ into an agent skills catalog.

    Image captures are excluded unless `with_assets` is set.
    """
    payload: list[tuple[Path, Path]] = []

    skill_md = ROOT_DIR / "SKILL.md"
    payload.append((skill_md, dest_root / "SKILL.md"))

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
            if src.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp"} and not with_assets:
                continue
            payload.append((src, dest_root / sub / src.relative_to(base)))

    if dest_root.exists():
        bak = dest_root.with_name(dest_root.name + BACKUP_SUFFIX)
        if not bak.exists():
            if not dry_run:
                shutil.copytree(dest_root, bak)
            report.add("skill", dest_root, BACKED_UP)

    for src, dest in payload:
        if not src.exists():
            continue
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
        report.add("skill", dest, CREATE, f"from {src.relative_to(ROOT_DIR)}")


# --------------------------------------------------------------------------
# uninstall
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
    report: Report | None = None,
) -> Report:
    """Copy the markdown knowledge base to <target>/.turtleneck/references/.

    Every rules file points agents at `.turtleneck/references/...`. Without this step those
    paths dangle and the installed rules lose the entire craft knowledge base.
    """
    report = report or Report(dry_run=dry_run)
    base = ROOT_DIR / "references"
    dest_root = target_dir / ".turtleneck" / "references"

    for src in sorted(base.rglob("*")):
        if src.is_dir():
            continue
        if any(part in SKILL_IGNORES for part in src.parts):
            continue
        if src.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp"} and not with_assets:
            continue
        dest = dest_root / src.relative_to(base)
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
                        help=f"overwrite foreign files after writing <dest>{BACKUP_SUFFIX}")
    parser.add_argument("--append", action="store_true",
                        help="merge into existing files using marker comments instead of replacing")
    parser.add_argument("--dry-run", "-n", action="store_true", help="print the plan, write nothing")
    parser.add_argument("--uninstall", action="store_true", help="remove what Turtleneck installed")
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
    else:
        if requested:
            install_to_project(target_dir, requested, force=args.force,
                               append=args.append, dry_run=args.dry_run, report=report)
        if not args.no_references:
            install_references(target_dir, dry_run=args.dry_run,
                               with_assets=args.with_assets, report=report)

    if args.claude_skill:
        install_skill(target_dir / ".claude" / "skills" / "turtleneck",
                      dry_run=args.dry_run, with_assets=args.with_assets, report=report)

    if args.antigravity:
        install_skill(Path.home() / ".gemini" / "config" / "skills" / "turtleneck",
                      dry_run=args.dry_run, with_assets=args.with_assets, report=report)

    if not report.outcomes:
        print("Nothing to do. Pass a platform flag, --all, --claude-skill or --antigravity.")
        return 0

    print(f"{'Planned' if args.dry_run else 'Installing'} Turtleneck in: {target_dir}")
    report.print()

    if report.refused:
        print(f"\n{len(report.refused)} file(s) left untouched because Turtleneck does not own them.")
        print("Use --append to merge alongside your content, or --force to replace it (a .bak is kept).")
        return 2

    print("\nTurtleneck installation complete. Senior UI/UX Architect mode active.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
