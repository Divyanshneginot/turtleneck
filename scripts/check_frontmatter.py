#!/usr/bin/env python3
"""
Turtleneck frontmatter gate.

Asserts that SKILL.md adheres to the trigger-only discovery format:
1. Valid YAML frontmatter block starting and ending with '---'.
2. Expected skill name ('turtleneck').
3. Concise description (<= 500 characters).
4. Trigger-only phrasing: starts with 'Use when'.
5. Covers key domains: design/build/restyle/review, accessibility, responsive, design-system.
6. Explicitly excludes non-visual backend/CLI work and exact supplied-design replication.
7. Avoids workflow narration (e.g. 'analyzes...', 'conducts...', 'implements...').

Exit code 0 = valid frontmatter. Non-zero = violation.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

WORKFLOW_NARRATION_MARKERS = [
    r"\banalyzes\b",
    r"\bconducts\b",
    r"\baligns on\b",
    r"\bimplements\b",
]

DOMAIN_REQUIRED_PATTERNS = [
    (r"\b(design|build|restyle|review)\b", "UI action (design/build/restyle/review)"),
    (r"\b(accessibility|a11y)\b", "accessibility concern"),
    (r"\bresponsive\b", "responsive concern"),
    (r"\b(design-system|design system|tokens)\b", "design-system concern"),
]

EXCLUSION_REQUIRED_PATTERNS = [
    (r"\b(backend|CLI)\b", "backend/CLI exclusion"),
    (r"\b(supplied design|supplied-design|reproduction)\b", "supplied-design replication exclusion"),
]


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    """Parse simple YAML frontmatter without external dependencies."""
    errors: list[str] = []
    lines = text.splitlines()

    if not lines or lines[0].strip() != "---":
        errors.append("File does not start with '---' frontmatter fence on line 1")
        return {}, errors

    closing_index = -1
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            closing_index = idx
            break

    if closing_index == -1:
        errors.append("No closing '---' fence found for frontmatter")
        return {}, errors

    raw_block = lines[1:closing_index]
    data: dict[str, str] = {}
    current_key: str | None = None
    current_val: list[str] = []

    for line in raw_block:
        # Match top-level key: value
        match = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", line)
        if match:
            if current_key is not None:
                data[current_key] = " ".join(" ".join(current_val).split())
            current_key = match.group(1).strip()
            rest = match.group(2).strip()
            if rest in (">", ">-", "|", "|-"):
                current_val = []
            elif rest:
                current_val = [rest]
            else:
                current_val = []
        elif current_key is not None:
            # Continuation line
            val = line.strip()
            if val:
                current_val.append(val)

    if current_key is not None:
        data[current_key] = " ".join(" ".join(current_val).split())

    return data, errors


def check_skill_frontmatter(path: Path | None = None, verbose: bool = True) -> int:
    target = path or (ROOT / "SKILL.md")
    if not target.exists():
        print(f"FAIL: target file not found: {target}")
        return 1

    content = target.read_text(encoding="utf-8")
    data, parse_errors = parse_frontmatter(content)
    if parse_errors:
        for err in parse_errors:
            print(f"FAIL: {err}")
        return 1

    failures: list[str] = []

    # Expected name
    name = data.get("name", "").strip()
    if name != "turtleneck":
        failures.append(f"Expected skill name 'turtleneck', got {name!r}")

    # Description checks
    desc = data.get("description", "").strip()
    if not desc:
        failures.append("Missing or empty 'description' in frontmatter")
    else:
        if not desc.startswith("Use when"):
            failures.append("Description must start with 'Use when' (trigger-only condition)")

        if len(desc) > 500:
            failures.append(f"Description too long ({len(desc)} chars > 500 max limit)")

        for pattern, label in DOMAIN_REQUIRED_PATTERNS:
            if not re.search(pattern, desc, re.IGNORECASE):
                failures.append(f"Description missing {label} (pattern {pattern!r})")

        for pattern, label in EXCLUSION_REQUIRED_PATTERNS:
            if not re.search(pattern, desc, re.IGNORECASE):
                failures.append(f"Description missing {label} (pattern {pattern!r})")

        for pattern in WORKFLOW_NARRATION_MARKERS:
            hit = re.search(pattern, desc, re.IGNORECASE)
            if hit:
                failures.append(
                    f"Description contains workflow narration {hit.group(0)!r}; "
                    "frontmatter must be trigger-only"
                )

    if failures:
        print(f"Frontmatter check failed for {target.name}:")
        for f in failures:
            print(f"  x {f}")
        return 1

    if verbose:
        print(f"PASS: {target.name} frontmatter is valid, trigger-only, and within bounds.")
        print(f"  Name       : {name}")
        print(f"  Description: {desc[:80]}... ({len(desc)} chars)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify SKILL.md frontmatter.")
    parser.add_argument(
        "--file",
        type=Path,
        default=ROOT / "SKILL.md",
        help="Path to SKILL.md (defaults to repo root SKILL.md)",
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress detailed output on pass")
    args = parser.parse_args(argv)

    print("Turtleneck frontmatter gate")
    print("-" * 60)
    return check_skill_frontmatter(path=args.file, verbose=not args.quiet)


if __name__ == "__main__":
    sys.exit(main())
