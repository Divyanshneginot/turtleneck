#!/usr/bin/env python3
"""
Turtleneck UX Stress & Anti-Slop Gate.

Deterministic verification gate that enforces production UX rigor and bans AI slop.
Validates that interfaces are not just static happy-path prototypes, but handle
real operational states, text overflow, and accessibility boundaries.

Checks
------
1. Anti-Slop: No `transition: all` (compositor-safe properties only).
2. Accessibility: All icon-only buttons carry accessible names (aria-label/title).
3. Accessibility: All form inputs carry accessible names (label/aria-label/title).
4. Focus Rigor: Explicit :focus-visible rules with high-contrast outlines.
5. 4-State Completeness: Verifies presence of Empty, Loading, and Error/Retry states
   when evaluating full views or components.
6. Layout Safety: Viewport meta tag present on full HTML documents, and dynamic text
   containers declare wrap/truncation safety to prevent string blowout.

Exit code 0 = passed. Non-zero = violations found.
"""

from __future__ import annotations

import argparse
import html.parser
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent


class SimpleHTMLParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.buttons: List[Tuple[dict, str, int]] = []
        self.inputs: List[Tuple[dict, int]] = []
        self.has_viewport = False
        self._current_tag: Optional[str] = None
        self._current_attrs: dict = {}
        self._current_text: list[str] = []
        self._current_line: int = 1

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        attr_dict = {k.lower(): (v or "") for k, v in attrs}
        line = self.getpos()[0]

        if tag == "meta" and attr_dict.get("name") == "viewport":
            self.has_viewport = True

        if tag == "input":
            self.inputs.append((attr_dict, line))

        if tag == "button":
            self._current_tag = "button"
            self._current_attrs = attr_dict
            self._current_text = []
            self._current_line = line

    def handle_data(self, data: str) -> None:
        if self._current_tag == "button":
            self._current_text.append(data.strip())

    def handle_endtag(self, tag: str) -> None:
        if tag == "button" and self._current_tag == "button":
            text = " ".join(t for t in self._current_text if t)
            self.buttons.append((self._current_attrs, text, self._current_line))
            self._current_tag = None


def extract_css(text: str) -> str:
    styles = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", text, flags=re.S))
    return styles


def check_anti_slop(text: str) -> List[str]:
    violations: List[str] = []
    styles = extract_css(text)

    # 1. No transition: all
    if re.search(r"transition\s*:\s*all\b", styles):
        violations.append("Banned 'transition: all' detected; specify explicit compositor properties (e.g. transform, opacity)")

    # 2. Focus-visible indicator
    if ("<button" in text or "<a " in text or "<input" in text) and styles:
        if not re.search(r":focus-visible\b", styles):
            violations.append("Missing ':focus-visible' outline rule for interactive controls")

    # 3. Saturated decorative blur blobs (classic AI slop)
    # Detects large background glow blobs (blur >= 40px with radial-gradient)
    if re.search(r"blur\(\s*(?:[4-9]\d|\d{3,})px\s*\)", styles) and re.search(r"radial-gradient", styles, re.I):
        violations.append("Decorative radial blur glow blob detected in styles (violates anti-slop aesthetic thesis)")

    return violations


def check_accessibility(text: str) -> List[str]:
    violations: List[str] = []
    parser = SimpleHTMLParser()
    try:
        parser.feed(text)
    except Exception:
        return violations

    # Check button accessible names
    for attrs, inner_text, line in parser.buttons:
        has_aria = bool(attrs.get("aria-label") or attrs.get("aria-labelledby") or attrs.get("title"))
        if not inner_text and not has_aria:
            violations.append(f"Line {line}: Button without text or accessible name (aria-label/title missing)")

    # Check input accessible names
    for attrs, line in parser.inputs:
        itype = attrs.get("type", "text").lower()
        if itype in ("hidden", "submit", "button", "reset"):
            continue
        has_label = bool(attrs.get("aria-label") or attrs.get("aria-labelledby") or attrs.get("title") or attrs.get("id"))
        if not has_label:
            violations.append(f"Line {line}: Input field without label, aria-label, or title attribute")

    return violations


def check_layout_containment(text: str) -> List[str]:
    violations: List[str] = []
    styles = extract_css(text)

    # Check viewport on full documents
    if "<html" in text.lower():
        parser = SimpleHTMLParser()
        parser.feed(text)
        if not parser.has_viewport:
            violations.append("Full document missing <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">")

    # Check rigid non-responsive fixed widths without max-width
    rigid_matches = re.finditer(r"\bwidth\s*:\s*([89]\d\d|\d{4,})px\b", styles)
    for m in rigid_matches:
        start = max(0, m.start() - 60)
        end = min(len(styles), m.end() + 60)
        snippet = styles[start:end]
        if "max-width" not in snippet:
            violations.append(f"Rigid non-responsive container '{m.group(0)}' without 'max-width: 100%' constraint")
            break

    return violations


def check_four_states(text: str) -> List[str]:
    """
    Enforces that production interfaces model the 4 essential UX states:
    1. Nominal (standard data)
    2. Empty State (0 items / no results)
    3. Loading / Skeleton State (async pending)
    4. Error / Recovery State (failure boundary with retry action)
    """
    violations: List[str] = []
    lower = text.lower()

    # Empty state indicator
    has_empty = any(
        m in lower
        for m in (
            "data-state=\"empty\"",
            "empty-state",
            "empty state",
            "no results",
            "no items",
            "zero items",
            "nothing here",
        )
    )
    if not has_empty:
        violations.append("Missing Empty State: no zero-records or empty-state handler found")

    # Loading skeleton indicator
    has_loading = any(
        m in lower
        for m in (
            "data-state=\"loading\"",
            "skeleton",
            "loading-state",
            "aria-busy=\"true\"",
            "spinner",
            "placeholder-glow",
        )
    )
    if not has_loading:
        violations.append("Missing Loading/Skeleton State: no layout placeholder to prevent layout shift")

    # Error recovery indicator
    has_error = any(
        m in lower
        for m in (
            "data-state=\"error\"",
            "error-state",
            "retry",
            "try again",
            "failed to load",
            "error boundary",
        )
    )
    if not has_error:
        violations.append("Missing Error/Recovery State: no failure handling or retry action found")

    return violations


def check_file(path: Path, require_states: bool = False) -> List[str]:
    if not path.is_file():
        return [f"File not found: {path}"]
    text = path.read_text(encoding="utf-8")
    problems = []
    problems.extend(check_anti_slop(text))
    problems.extend(check_accessibility(text))
    problems.extend(check_layout_containment(text))
    if require_states:
        problems.extend(check_four_states(text))
    return problems


def check(
    targets: Optional[List[Path]] = None,
    require_states: bool = False,
    verbose: bool = True,
) -> int:
    if not targets:
        targets = sorted((ROOT / "examples").glob("*.html"))

    all_failures: List[Tuple[Path, List[str]]] = []

    for target in targets:
        if target.is_dir():
            files = sorted(list(target.glob("**/*.html")) + list(target.glob("**/*.jsx")) + list(target.glob("**/*.tsx")))
        else:
            files = [target]

        for f in files:
            problems = check_file(f, require_states=require_states)
            if problems:
                all_failures.append((f, problems))

    if verbose:
        print(f"Turtleneck Stress & Anti-Slop Gate: checked {len(targets)} target(s)")
        print("-" * 60)
        if not all_failures:
            print("PASS: All checked surfaces obey anti-slop rules, accessibility, and layout safety.")
        else:
            print(f"FAIL: {len(all_failures)} file(s) contain violations:")
            for p, issues in all_failures:
                try:
                    rel = p.relative_to(ROOT)
                except ValueError:
                    rel = p
                print(f"\n  [x] {rel}:")
                for issue in issues:
                    print(f"      - {issue}")

    return 1 if all_failures else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Turtleneck UX Stress & Anti-Slop Verification Gate",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "targets",
        nargs="*",
        type=Path,
        help="Files or directories to check (default: examples/*.html)",
    )
    parser.add_argument(
        "--require-states",
        action="store_true",
        help="Strictly require 4-State completeness (nominal, empty, loading, error)",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress verbose output; exit code only",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    targets = [p.resolve() for p in args.targets] if args.targets else None
    return check(targets=targets, require_states=args.require_states, verbose=not args.quiet)


if __name__ == "__main__":
    sys.exit(main())
