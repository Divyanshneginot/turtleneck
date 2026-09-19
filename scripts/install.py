#!/usr/bin/env python3
"""
Turtleneck Universal Installer
Installs Turtleneck rules and skills into any repository or agent environment:
Claude Code, Cursor, Windsurf, GitHub Copilot, Cline, Google Antigravity, or generic AGENTS.md.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
RULES_DIR = ROOT_DIR / "rules"

TARGETS = {
    "agents": ("AGENTS.md", "rules/AGENTS.md"),
    "claude": ("CLAUDE.md", "rules/CLAUDE.md"),
    "cursor": (".cursorrules", "rules/.cursorrules"),
    "windsurf": (".windsurfrules", "rules/.windsurfrules"),
    "copilot": (".github/copilot-instructions.md", "rules/copilot-instructions.md"),
}

def install_to_project(target_dir: Path, platforms: list[str]) -> None:
    print(f"Installing Turtleneck into: {target_dir}")
    target_dir.mkdir(parents=True, exist_ok=True)

    for plat in platforms:
        if plat not in TARGETS:
            continue
        rel_dest, rel_src = TARGETS[plat]
        dest_path = target_dir / rel_dest
        src_path = ROOT_DIR / rel_src

        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dest_path)
        print(f"  ✓ [{plat}] Created {dest_path.relative_to(target_dir)}")

def install_antigravity_global() -> None:
    home = Path.home()
    dest = home / ".gemini" / "config" / "skills" / "turtleneck"
    print(f"Installing Turtleneck to Antigravity global skills: {dest}")
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT_DIR, dest, ignore=shutil.ignore_patterns(".git", "__pycache__", "node_modules"))
    print("  ✓ Antigravity skill installed.")

def main():
    parser = argparse.ArgumentParser(description="Install Turtleneck across any AI agent environment.")
    parser.add_argument("--target", "-t", default=".", help="Target project directory (default: current directory)")
    parser.add_argument("--all", "-a", action="store_true", help="Install rules for all supported agents")
    parser.add_argument("--claude", action="store_true", help="Install CLAUDE.md for Claude Code")
    parser.add_argument("--cursor", action="store_true", help="Install .cursorrules for Cursor")
    parser.add_argument("--windsurf", action="store_true", help="Install .windsurfrules for Windsurf")
    parser.add_argument("--copilot", action="store_true", help="Install .github/copilot-instructions.md")
    parser.add_argument("--antigravity", action="store_true", help="Install globally for Google Antigravity")

    args = parser.parse_args()
    target_path = Path(args.target).resolve()

    if args.antigravity:
        install_antigravity_global()
        return

    platforms = []
    if args.all:
        platforms = ["agents", "claude", "cursor", "windsurf", "copilot"]
    else:
        if args.claude: platforms.append("claude")
        if args.cursor: platforms.append("cursor")
        if args.windsurf: platforms.append("windsurf")
        if args.copilot: platforms.append("copilot")
        if not platforms:
            # Auto-detect or default to AGENTS.md + any existing configs
            platforms.append("agents")
            if (target_path / ".cursor").exists(): platforms.append("cursor")
            if (target_path / ".github").exists(): platforms.append("copilot")
            if (target_path / ".windsurf").exists(): platforms.append("windsurf")

    install_to_project(target_path, platforms)
    print("\nTurtleneck installation complete! Senior UI/UX Architect mode active.")

if __name__ == "__main__":
    main()
