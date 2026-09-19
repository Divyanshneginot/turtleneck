#!/usr/bin/env python3
"""
Turtleneck examples gate.

examples/ is the only executable proof this repository ships, and it used to break the skill's
own non-negotiable rules: zero :focus-visible across 34 interactive elements, zero
prefers-reduced-motion blocks, seven `transition: all` declarations, one aria attribute in total,
and archetype colours that had drifted away from references/design-archetypes.md.

This gate asserts the examples obey the protocol they demonstrate. It reuses the contrast maths
from check_contrast.py rather than reimplementing it.

Checks
------
1. Every example declares a :focus-visible rule with a 2px outline and 2px offset.
2. That ring colour clears 3:1 against the file's canvas and every surface token.
3. Every example honours prefers-reduced-motion.
4. No `transition: all` anywhere (compositor-only properties).
5. Every icon-only button carries an accessible name.
6. Every <input> carries an accessible name.
7. Every --text-* token clears 4.5:1 against the --canvas of the block that declares it.
8. Archetype accents in examples/index.html match references/design-archetypes.md.

Exit code 0 = the examples obey the protocol.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location("tn_contrast", ROOT / "scripts" / "check_contrast.py")
_contrast = importlib.util.module_from_spec(_spec)
sys.modules["tn_contrast"] = _contrast
_spec.loader.exec_module(_contrast)
C = _contrast.contrast_ratio

EXAMPLES = sorted((ROOT / "examples").glob("*.html"))

HEX = r"#[0-9a-fA-F]{6}"
BLOCK_RE = re.compile(r"(?::root|body\[data-archetype=\"(?P<name>[a-z]+)\"\])\s*\{(?P<body>[^}]*)\}")
CANVAS_RE = re.compile(r"--(?:canvas|bg-canvas|bg):\s*(" + HEX + r")")
TEXT_TOKEN_RE = re.compile(r"--((?:text|fg)-[a-z]+):\s*(" + HEX + r")")
SURFACE_RE = re.compile(r"--(?:surface[a-z-]*|window-bg|sidebar-bg|bg-surface[a-z-]*):\s*(" + HEX + r")")
OUTLINE_RE = re.compile(r"outline:\s*2px\s+solid\s+(?P<color>" + HEX + r"|var\(--[a-z-]+\))")

# index.html archetype -> accent declared in references/design-archetypes.md
DOC_ACCENTS = {
    "starlight": "#636fd3",
    "corporate": "#6259ff",
    "editorial": "#1b75cf",
    "fluid": "#006be0",
    "minimal": "#ffffff",
}

def css_and_body(text: str) -> tuple[str, str]:
    styles = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", text, re.S))
    markup = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.S)
    markup = re.sub(r"<script[^>]*>.*?</script>", "", markup, flags=re.S)
    return styles, markup


def check_example(path: Path) -> list[str]:
    problems: list[str] = []
    text = path.read_text(encoding="utf-8")
    styles, markup = css_and_body(text)
    name = path.name

    # 1 + 2 : focus-visible ring, and a ring that is actually visible
    if ":focus-visible" not in styles:
        problems.append(f"{name}: no :focus-visible rule (5-state completeness requires one)")
    else:
        if "outline-offset: 2px" not in styles:
            problems.append(f"{name}: :focus-visible has no `outline-offset: 2px`")
        if not re.search(r"outline:\s*2px\s+solid", styles):
            problems.append(f"{name}: :focus-visible outline is not `2px solid`")

        canvases = [m.group(1) for m in CANVAS_RE.finditer(styles)]
        surfaces = [m.group(1) for m in SURFACE_RE.finditer(styles)]
        rings = [m.group("color") for m in OUTLINE_RE.finditer(styles)]

        # Resolve the ring per CSS block: this file redefines tokens for each archetype, so a
        # single global variable lookup would test one archetype's ring against every canvas.
        checks: list[tuple[str, list[str], str]] = []
        for ring in rings:
            var_name = re.match(r"var\((--[a-z-]+)\)", ring)
            if not var_name:
                checks.append((ring, canvases + surfaces, "file"))
                continue
            prop = var_name.group(1)
            declared = False
            for block in BLOCK_RE.finditer(styles):
                body = block.group("body")
                vm = re.search(re.escape(prop) + r":\s*(" + HEX + r")", body)
                if not vm:
                    continue
                declared = True
                label = block.group("name") or "root"
                bgs = [m.group(1) for m in CANVAS_RE.finditer(body)]
                bgs += [m.group(1) for m in SURFACE_RE.finditer(body)]
                checks.append((vm.group(1), bgs, label))
            if not declared:
                problems.append(f"{name}: focus ring {ring} is not defined in any CSS block")
                continue
            # every theme block that sets a canvas must also set the ring, or that theme
            # silently falls back to an inherited (possibly invisible) colour
            themed = [b for b in BLOCK_RE.finditer(styles) if CANVAS_RE.search(b.group("body"))]
            missing = [
                (b.group("name") or "root")
                for b in themed
                if not re.search(re.escape(prop) + r":\s*" + HEX, b.group("body"))
            ]
            if missing:
                problems.append(
                    f"{name}: {ring} is undefined in theme block(s): {', '.join(missing)}"
                )

        for colour, bgs, label in checks:
            if not re.fullmatch(HEX, colour or ""):
                problems.append(f"{name}: cannot resolve focus ring colour {colour!r}")
                continue
            for bg in bgs:
                ratio = C(colour, bg)
                if ratio < 3.0:
                    problems.append(
                        f"{name}: [{label}] focus ring {colour} is {ratio:.2f}:1 on {bg}, needs >= 3:1"
                    )

    # 3 : reduced motion
    if "prefers-reduced-motion" not in styles:
        problems.append(f"{name}: no @media (prefers-reduced-motion: reduce) fallback")

    # 4 : compositor-only transitions
    for n, line in enumerate(text.splitlines(), 1):
        if re.search(r"transition:\s*all\b", line):
            problems.append(f"{name}:{n}: `transition: all` (animate transform/opacity/etc. explicitly)")

    # 5 : icon-only buttons need an accessible name.
    # A one-character label ("x", "✕", "+") is announced as a bare glyph by screen readers, so it
    # counts as icon-only even though it is technically text.
    for m in re.finditer(r"<button\b(?P<attrs>[^>]*)>(?P<body>.*?)</button>", markup, re.S):
        attrs, body = m.group("attrs"), m.group("body")
        text_body = re.sub(r"<[^>]+>", "", body).strip()
        if len(text_body) <= 1 and "aria-label" not in attrs and "aria-labelledby" not in attrs:
            problems.append(
                f"{name}: icon-only button <button>{text_body or '(empty)'}</button> "
                f"has no accessible name"
            )

    # 6 : inputs need an accessible name
    labels = set(re.findall(r"<label[^>]*\bfor=[\"']([^\"']+)[\"']", markup))
    for m in re.finditer(r"<input\b(?P<attrs>[^>]*)/?>", markup):
        attrs = m.group("attrs")
        if 'type="hidden"' in attrs:
            continue
        ident = re.search(r"\bid=[\"']([^\"']+)[\"']", attrs)
        named = (
            "aria-label" in attrs
            or "aria-labelledby" in attrs
            or (ident and ident.group(1) in labels)
        )
        if not named:
            problems.append(f"{name}: <input {attrs.strip()[:60]}> has no accessible name")

    # 7 : text tokens clear 4.5:1 on the canvas of their own block
    for block in BLOCK_RE.finditer(styles):
        body = block.group("body")
        cm = CANVAS_RE.search(body)
        if not cm:
            continue
        canvas = cm.group(1)
        label = block.group("name") or "root"
        for tm in TEXT_TOKEN_RE.finditer(body):
            token, value = tm.group(1), tm.group(2)
            ratio = C(value, canvas)
            if ratio < 4.5:
                problems.append(
                    f"{name}: [{label}] --{token} {value} is {ratio:.2f}:1 on {canvas}, needs >= 4.5:1"
                )

    # 8 : archetype accents stay in sync with the documentation
    if name == "index.html":
        for block in BLOCK_RE.finditer(styles):
            label = block.group("name") or "starlight"
            am = re.search(r"--accent-indigo:\s*(" + HEX + r")", block.group("body"))
            if not am or label not in DOC_ACCENTS:
                continue
            want = DOC_ACCENTS[label]
            if am.group(1).lower() != want.lower():
                problems.append(
                    f"{name}: [{label}] --accent-indigo is {am.group(1)} but "
                    f"references/design-archetypes.md declares {want}"
                )
    return problems


def main() -> int:
    print("Turtleneck examples gate")
    print("-" * 60)
    if not EXAMPLES:
        print("no examples found")
        return 1

    all_problems: list[str] = []
    for path in EXAMPLES:
        problems = check_example(path)
        status = "ok" if not problems else f"{len(problems)} problem(s)"
        print(f"  {path.name:<30} {status}")
        all_problems.extend(problems)

    print()
    if all_problems:
        print(f"{len(all_problems)} violation(s) of the Turtleneck protocol:")
        for p in all_problems:
            print(f"  x {p}")
        return 1

    print(f"All {len(EXAMPLES)} examples honour focus-visible, reduced motion, "
          f"compositor-only transitions, accessible names and WCAG 2.2 AA text contrast.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
