#!/usr/bin/env python3
"""
Turtleneck Adaptive Taste Ledger CLI.

Manages persistent aesthetic profiles, rejected tropes, and user design feedback
across agent sessions.

Storage locations:
  1. Project profile: <project>/.turtleneck/taste-profile.json
  2. Global profile:  ~/.turtleneck/taste-profile.json
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_PROFILE: Dict[str, Any] = {
    "version": "1.0.0",
    "updated_at": "",
    "preferred_vernacular": [
        "modern_high_precision_editorial",
        "asymmetric_layout",
        "generous_whitespace",
    ],
    "rejected_tropes": [
        "purple_neon_blur",
        "centered_3_cards",
        "dusty_retro_serif",
        "fake_diagnostics_telemetry",
    ],
    "typography": {
        "headline_family": "Plus Jakarta Sans",
        "mono_family": "JetBrains Mono",
        "tracking": "-0.03em",
    },
    "contrast_floor": 7.0,
    "notes": [],
}


def get_global_path() -> Path:
    return Path.home() / ".turtleneck" / "taste-profile.json"


def get_project_path(project_dir: Optional[Path] = None) -> Path:
    base = project_dir.resolve() if project_dir else Path.cwd().resolve()
    return base / ".turtleneck" / "taste-profile.json"


def load_profile(path: Path) -> Optional[Dict[str, Any]]:
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return None


def resolve_profile(project_dir: Optional[Path] = None) -> Dict[str, Any]:
    global_p = load_profile(get_global_path())
    project_p = load_profile(get_project_path(project_dir))

    # Base profile
    resolved = dict(DEFAULT_PROFILE)

    if global_p:
        resolved.update({k: v for k, v in global_p.items() if k != "version"})
        # Merge lists
        for key in ("preferred_vernacular", "rejected_tropes", "notes"):
            if key in global_p and isinstance(global_p[key], list):
                merged = list(dict.fromkeys(resolved.get(key, []) + global_p[key]))
                resolved[key] = merged

    if project_p:
        resolved.update({k: v for k, v in project_p.items() if k != "version"})
        for key in ("preferred_vernacular", "rejected_tropes", "notes"):
            if key in project_p and isinstance(project_p[key], list):
                merged = list(dict.fromkeys(resolved.get(key, []) + project_p[key]))
                resolved[key] = merged

    return resolved


def save_project_profile(data: Dict[str, Any], project_dir: Optional[Path] = None) -> Path:
    target = get_project_path(project_dir)
    target.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return target


def cmd_init(args: argparse.Namespace) -> int:
    target = get_project_path(args.project)
    if target.is_file() and not args.force:
        print(f"Taste profile already exists at {target}")
        return 0
    profile = dict(DEFAULT_PROFILE)
    saved = save_project_profile(profile, args.project)
    print(f"Initialized taste profile at {saved}")
    return 0


def cmd_reject(args: argparse.Namespace) -> int:
    current = load_profile(get_project_path(args.project)) or resolve_profile(args.project)
    trope = args.trope.strip().lower().replace(" ", "_")
    current.setdefault("rejected_tropes", [])
    if trope not in current["rejected_tropes"]:
        current["rejected_tropes"].append(trope)
    if args.note:
        current.setdefault("notes", []).append(
            f"{datetime.date.today().isoformat()}: Rejected '{trope}' - {args.note}"
        )
    saved = save_project_profile(current, args.project)
    print(f"Added '{trope}' to rejected tropes in {saved}")
    return 0


def cmd_prefer(args: argparse.Namespace) -> int:
    current = load_profile(get_project_path(args.project)) or resolve_profile(args.project)
    style = args.style.strip().lower().replace(" ", "_")
    current.setdefault("preferred_vernacular", [])
    if style not in current["preferred_vernacular"]:
        current["preferred_vernacular"].append(style)
    if args.note:
        current.setdefault("notes", []).append(
            f"{datetime.date.today().isoformat()}: Preferred '{style}' - {args.note}"
        )
    saved = save_project_profile(current, args.project)
    print(f"Added '{style}' to preferred styles in {saved}")
    return 0


def cmd_note(args: argparse.Namespace) -> int:
    current = load_profile(get_project_path(args.project)) or resolve_profile(args.project)
    current.setdefault("notes", []).append(
        f"{datetime.date.today().isoformat()}: {args.text}"
    )
    saved = save_project_profile(current, args.project)
    print(f"Recorded critique note in {saved}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    resolved = resolve_profile(args.project)
    print("Turtleneck Active Taste Profile")
    print("=" * 60)
    print("Preferred Styles:")
    for p in resolved.get("preferred_vernacular", []):
        print(f"  + {p}")
    print("\nRejected Tropes:")
    for r in resolved.get("rejected_tropes", []):
        print(f"  x {r}")
    print("\nTypography & Contrast:")
    typo = resolved.get("typography", {})
    print(f"  Headline: {typo.get('headline_family', 'Default')} (tracking: {typo.get('tracking', '0')})")
    print(f"  Mono:     {typo.get('mono_family', 'Default')}")
    print(f"  Contrast: >= {resolved.get('contrast_floor', 4.5)}:1")
    notes = resolved.get("notes", [])
    if notes:
        print("\nCritique History:")
        for n in notes[-5:]:
            print(f"  * {n}")
    return 0


def cmd_json(args: argparse.Namespace) -> int:
    resolved = resolve_profile(args.project)
    print(json.dumps(resolved, indent=2, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Turtleneck Adaptive Taste Ledger CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--project",
        type=Path,
        default=None,
        help="Path to project directory (default: current working directory)",
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)

    # init
    p_init = sub.add_parser("init", help="Initialize local .turtleneck/taste-profile.json")
    p_init.add_argument("--force", action="store_true", help="Overwrite existing profile")
    p_init.set_defaults(func=cmd_init)

    # reject
    p_rej = sub.add_parser("reject", help="Add a trope to rejected tropes")
    p_rej.add_argument("trope", type=str, help="Trope name (e.g. 'purple_neon_blur')")
    p_rej.add_argument("--note", type=str, default="", help="Contextual critique rationale")
    p_rej.set_defaults(func=cmd_reject)

    # prefer
    p_pref = sub.add_parser("prefer", help="Add a style to preferred vernacular")
    p_pref.add_argument("style", type=str, help="Style name (e.g. 'modern_high_precision_editorial')")
    p_pref.add_argument("--note", type=str, default="", help="Contextual preference rationale")
    p_pref.set_defaults(func=cmd_prefer)

    # note
    p_note = sub.add_parser("note", help="Record a human critique note")
    p_note.add_argument("text", type=str, help="Critique text")
    p_note.set_defaults(func=cmd_note)

    # show
    p_show = sub.add_parser("show", help="Display resolved human-readable taste profile")
    p_show.set_defaults(func=cmd_show)

    # json
    p_json = sub.add_parser("json", help="Output resolved taste profile as JSON for agent context")
    p_json.set_defaults(func=cmd_json)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
