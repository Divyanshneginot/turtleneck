"""
Turtleneck contrast gate.

Verifies every colour pair declared in the design token documentation against
WCAG 2.2 AA, and refuses to let the docs drift away from the values it checks.

Also supports verifying arbitrary generated palettes supplied via `--tokens <path.json>`.

Minimal JSON Schema for `--tokens`
----------------------------------
A JSON file containing an object with a `"pairs"` array (or a top-level array):

  {
    "pairs": [
      {
        "name": "text-primary",
        "foreground": "#0F172A",
        "background": "#FFFFFF",
        "role": "body text",
        "threshold": "text",
        "exemption_rationale": ""
      },
      {
        "name": "card-border",
        "foreground": "#E2E8F0",
        "background": "#FFFFFF",
        "role": "decorative border",
        "threshold": "decorative",
        "exemption_rationale": "non-interactive card container edge"
      }
    ]
  }

Fields:
  name                 string, required. Identifier for the token pair.
  foreground           string, required. Hex colour (#RGB or #RRGGBB).
  background           string, required. Hex colour (#RGB or #RRGGBB).
  role                 string, required. Semantic role description.
  threshold            string, required. One of:
                         - "text": requires contrast >= 4.5:1 (normal text)
                         - "ui": requires contrast >= 3.0:1 (UI boundaries / graphical objects)
                         - "decorative": exempt from ratio, requires non-empty exemption_rationale.
  exemption_rationale  string, required if threshold is "decorative".

Exit code 0 = all pairs pass. Non-zero = at least one violation or malformed input.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

TEXT_MIN = 4.5
UI_MIN = 3.0

TEXT_CLASSES = {"text", "text-aa", "normal-text"}
UI_CLASSES = {"ui", "large-text", "ui-component", "graphical"}
DECORATIVE_CLASSES = {"decorative", "exempt"}
HEX_COLOR_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

# label, foreground, background, kind, source file, locate substring
PAIRS: list[tuple[str, str, str, str, str, str]] = [
    # ---- references/design-tokens.md : light theme (canvas #FFFFFF) ----
    ("tokens L text-primary", "#0F172A", "#FFFFFF", "text", "references/design-tokens.md", "`text-primary`"),
    ("tokens L text-secondary", "#475569", "#FFFFFF", "text", "references/design-tokens.md", "`text-secondary`"),
    ("tokens L text-muted", "#637896", "#FFFFFF", "text", "references/design-tokens.md", "`text-muted`"),
    ("tokens L border-subtle", "#E2E8F0", "#FFFFFF", "decorative", "references/design-tokens.md", "`border-subtle`"),
    ("tokens L border-strong", "#7F97B5", "#FFFFFF", "ui", "references/design-tokens.md", "`border-strong`"),
    ("tokens L on action-primary", "#FFFFFF", "#2563EB", "text", "references/design-tokens.md", "on-action-primary"),
    ("tokens L on action-primary-hover", "#FFFFFF", "#1D4ED8", "text", "references/design-tokens.md", "on-action-primary"),
    ("tokens L action-primary as link text", "#2563EB", "#FFFFFF", "text", "references/design-tokens.md", "`action-primary`"),
    ("tokens L status-success", "#16A34A", "#FFFFFF", "ui", "references/design-tokens.md", "`status-success`"),
    ("tokens L status-warning", "#D97706", "#FFFFFF", "ui", "references/design-tokens.md", "`status-warning`"),
    ("tokens L status-danger", "#DC2626", "#FFFFFF", "ui", "references/design-tokens.md", "`status-danger`"),
    # ---- references/design-tokens.md : dark theme (canvas #090D16, surface #111827) ----
    ("tokens D text-primary", "#F9FAFB", "#090D16", "text", "references/design-tokens.md", "`text-primary`"),
    ("tokens D text-secondary", "#9CA3AF", "#090D16", "text", "references/design-tokens.md", "`text-secondary`"),
    ("tokens D text-muted", "#737A89", "#090D16", "text", "references/design-tokens.md", "`text-muted`"),
    ("tokens D border-subtle", "#1F2937", "#111827", "decorative", "references/design-tokens.md", "`border-subtle`"),
    ("tokens D border-strong", "#56657E", "#111827", "ui", "references/design-tokens.md", "`border-strong`"),
    ("tokens D on action-primary", "#090D16", "#3B82F6", "text", "references/design-tokens.md", "on-action-primary"),
    ("tokens D on action-primary-hover", "#090D16", "#60A5FA", "text", "references/design-tokens.md", "on-action-primary"),
    ("tokens D action-primary as link text", "#3B82F6", "#090D16", "text", "references/design-tokens.md", "`action-primary`"),
    ("tokens D status-success", "#22C55E", "#090D16", "ui", "references/design-tokens.md", "`status-success`"),
    ("tokens D status-warning", "#F59E0B", "#090D16", "ui", "references/design-tokens.md", "`status-warning`"),
    ("tokens D status-danger", "#EF4444", "#090D16", "ui", "references/design-tokens.md", "`status-danger`"),
    # ---- references/design-archetypes.md : Archetype 1, High-Trust Corporate ----
    ("A1 body ink", "#0a2540", "#f6f9fc", "text", "references/design-archetypes.md", "Typography"),
    ("A1 secondary", "#425466", "#f6f9fc", "text", "references/design-archetypes.md", "Typography"),
    ("A1 muted", "#627489", "#f6f9fc", "text", "references/design-archetypes.md", "Typography"),
    ("A1 accent as text", "#6259ff", "#f6f9fc", "text", "references/design-archetypes.md", "Primary Accent"),
    ("A1 white on accent fill", "#ffffff", "#6259ff", "text", "references/design-archetypes.md", "Primary Accent"),
    ("A1 hover accent as text", "#4f46e5", "#f6f9fc", "text", "references/design-archetypes.md", "Primary Accent"),
    ("A1 card border", "#e3e8ee", "#f6f9fc", "decorative", "references/design-archetypes.md", "Card Surface"),
    # ---- Archetype 2, Warm Editorial Paper ----
    ("A2 accent as text", "#1b75cf", "#fbfbfa", "text", "references/design-archetypes.md", "Primary Accent"),
    ("A2 ink accent", "#201f1d", "#fbfbfa", "text", "references/design-archetypes.md", "Primary Accent"),
    ("A2 hover accent as text", "#1b6ec2", "#fbfbfa", "text", "references/design-archetypes.md", "Primary Accent"),
    ("A2 divider", "#e9e9e8", "#fbfbfa", "decorative", "references/design-archetypes.md", "Card Surface"),
    # ---- Archetype 3, Fluid Organics ----
    ("A3 white on accent fill", "#ffffff", "#006be0", "text", "references/design-archetypes.md", "Primary Accent"),
    ("A3 accent as text on light", "#006be0", "#f2f2f7", "text", "references/design-archetypes.md", "Primary Accent"),
    ("A3 accent as text on dark", "#0d81ff", "#1c1c1e", "text", "references/design-archetypes.md", "Primary Accent"),
    ("A3 hover as text", "#0056b3", "#f2f2f7", "text", "references/design-archetypes.md", "Primary Accent"),
    # ---- Archetype 4, High-Density Starlight ----
    ("A4 accent as text", "#636fd3", "#08090a", "text", "references/design-archetypes.md", "Primary Accent"),
    ("A4 hover accent as text", "#6f7bf7", "#08090a", "text", "references/design-archetypes.md", "Primary Accent"),
    # ---- Archetype 5, Stark Geometric Minimal ----
    ("A5 white accent on black", "#ffffff", "#000000", "text", "references/design-archetypes.md", "Primary Accent"),
    ("A5 status online", "#10b981", "#000000", "ui", "references/design-archetypes.md", "Status Accents"),
    ("A5 status degraded", "#f59e0b", "#000000", "ui", "references/design-archetypes.md", "Status Accents"),
    ("A5 status down", "#ef4444", "#000000", "ui", "references/design-archetypes.md", "Status Accents"),
    ("A5 border subtle", "#1a1a1a", "#000000", "decorative", "references/design-archetypes.md", "Borders"),
    ("A5 border window", "#262626", "#000000", "decorative", "references/design-archetypes.md", "Borders"),
    ("A5 border active", "#333333", "#000000", "decorative", "references/design-archetypes.md", "Borders"),
]

EXEMPTION_MARKERS = ("exempt", "decorative", "structural")


def _channel(c: float) -> float:
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    v = value.lstrip("#")
    if len(v) == 3:
        v = "".join(ch * 2 for ch in v)
    if len(v) != 6 or not re.fullmatch(r"[0-9a-fA-F]{6}", v):
        raise ValueError(f"not a hex colour: {value!r}")
    return int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16)


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = (_channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg: str, bg: str) -> float:
    a, b = relative_luminance(hex_to_rgb(fg)), relative_luminance(hex_to_rgb(bg))
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def locate_line(source: Path, fg: str, locate: str) -> str | None:
    """Return the source line that declares `fg` for the role named by `locate`."""
    for raw in source.read_text(encoding="utf-8").splitlines():
        if fg.lower() in raw.lower() and locate.lower() in raw.lower():
            return raw
    return None


def check(verbose: bool = True) -> int:
    failures: list[str] = []
    checked = 0

    for label, fg, bg, kind, rel_source, locate in PAIRS:
        source = ROOT / rel_source
        if not source.exists():
            failures.append(f"{label}: source file missing: {rel_source}")
            continue

        line = locate_line(source, fg, locate)
        if line is None:
            failures.append(
                f"{label}: {fg} not found on any {locate!r} line of {rel_source} "
                f"(the docs drifted away from the gate)"
            )
            continue

        checked += 1
        ratio = contrast_ratio(fg, bg)

        if kind == "decorative":
            if not any(m in line.lower() for m in EXEMPTION_MARKERS):
                failures.append(
                    f"{label}: classified decorative but {rel_source} carries no "
                    f"exemption note on the declaring line"
                )
            if verbose:
                print(f"  exempt  {label:<36} {ratio:>6.2f}:1  (decorative, annotated)")
            continue

        required = TEXT_MIN if kind == "text" else UI_MIN
        ok = ratio >= required
        if not ok:
            failures.append(f"{label}: {fg} on {bg} = {ratio:.2f}:1, needs >= {required}:1")
        if verbose:
            print(f"  {'PASS' if ok else 'FAIL'}    {label:<36} {ratio:>6.2f}:1  (needs {required}:1)")

    print()
    if failures:
        print(f"{len(failures)} of {checked} pairs FAILED:")
        for f in failures:
            print(f"  x {f}")
        return 1

    print(f"All {checked} declared colour pairs meet WCAG 2.2 AA.")
    return 0



def validate_token_pairs(data: Any) -> tuple[list[dict[str, Any]], list[str]]:
    """Validate JSON data against the minimal token pairs schema.

    Returns:
        (valid_pairs, validation_errors)
    """
    errors: list[str] = []
    pairs_list: list[Any]

    if isinstance(data, dict):
        if "pairs" in data:
            pairs_list = data["pairs"]
        elif "tokens" in data:
            pairs_list = data["tokens"]
        else:
            errors.append("Invalid schema root: object must contain 'pairs' or 'tokens' list")
            return [], errors
    elif isinstance(data, list):
        pairs_list = data
    else:
        errors.append("Invalid schema root: expected list or object with 'pairs'")
        return [], errors

    if not isinstance(pairs_list, list) or len(pairs_list) == 0:
        errors.append("Empty input: no token pairs found to verify")
        return [], errors

    validated: list[dict[str, Any]] = []

    for idx, item in enumerate(pairs_list):
        prefix = f"pair[{idx}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: expected object, got {type(item).__name__}")
            continue

        name = item.get("name") or item.get("label") or f"pair-{idx+1}"
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{prefix}: missing or empty 'name'")
            name = f"pair-{idx+1}"
        else:
            name = name.strip()

        role = item.get("role")
        if not isinstance(role, str) or not role.strip():
            errors.append(f"{name}: missing or empty 'role'")
            role = ""
        else:
            role = role.strip()

        fg = item.get("foreground") or item.get("fg")
        if not isinstance(fg, str) or not HEX_COLOR_RE.match(fg.strip()):
            errors.append(f"{name}: malformed foreground color: {fg!r} (expected #RGB or #RRGGBB)")
            fg = ""
        else:
            fg = fg.strip()

        bg = item.get("background") or item.get("bg")
        if not isinstance(bg, str) or not HEX_COLOR_RE.match(bg.strip()):
            errors.append(f"{name}: malformed background color: {bg!r} (expected #RGB or #RRGGBB)")
            bg = ""
        else:
            bg = bg.strip()

        raw_thresh = item.get("threshold") or item.get("threshold_class") or item.get("class") or item.get("kind")
        if not isinstance(raw_thresh, str):
            errors.append(f"{name}: missing or non-string threshold class")
            threshold = ""
        else:
            threshold = raw_thresh.strip().lower()

        exemption = item.get("exemption_rationale") or item.get("rationale") or item.get("exemption")
        exemption_str = str(exemption).strip() if exemption is not None else ""

        if threshold in TEXT_CLASSES:
            kind = "text"
        elif threshold in UI_CLASSES:
            kind = "ui"
        elif threshold in DECORATIVE_CLASSES:
            kind = "decorative"
            if not exemption_str:
                errors.append(
                    f"{name}: classified decorative/exempt but missing exemption rationale (unjustified exemption)"
                )
                kind = "unknown"
        else:
            errors.append(f"{name}: unknown threshold class {raw_thresh!r} (expected 'text', 'ui', or 'decorative')")
            kind = "unknown"

        if fg and bg and kind != "unknown":
            validated.append({
                "name": name,
                "role": role,
                "foreground": fg,
                "background": bg,
                "kind": kind,
                "exemption_rationale": exemption_str,
            })

    return validated, errors


def check_tokens_file(path: Path, verbose: bool = True) -> int:
    """Check a custom tokens JSON file against WCAG 2.2 AA."""
    if not path.exists():
        print(f"FAIL: tokens file not found: {path}")
        return 1

    try:
        raw_text = path.read_text(encoding="utf-8")
        if not raw_text.strip():
            print("FAIL: Empty input: tokens file is empty")
            return 1
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        print(f"FAIL: malformed JSON in {path}: {exc}")
        return 1

    pairs, validation_errors = validate_token_pairs(data)
    if validation_errors:
        print()
        print(f"{len(validation_errors)} validation error(s) found in {path.name}:")
        for f in validation_errors:
            print(f"  x {f}")
        return 1

    failures: list[str] = []
    checked = 0

    for item in pairs:
        name = item["name"]
        fg = item["foreground"]
        bg = item["background"]
        kind = item["kind"]
        rationale = item["exemption_rationale"]

        checked += 1
        try:
            ratio = contrast_ratio(fg, bg)
        except ValueError as err:
            failures.append(f"{name}: {err}")
            continue

        if kind == "decorative":
            if verbose:
                print(f"  exempt  {name:<36} {ratio:>6.2f}:1  (decorative: {rationale})")
            continue

        required = TEXT_MIN if kind == "text" else UI_MIN
        ok = ratio >= required
        if not ok:
            failures.append(f"{name}: {fg} on {bg} = {ratio:.2f}:1, needs >= {required:.1f}:1")
        if verbose:
            print(f"  {'PASS' if ok else 'FAIL'}    {name:<36} {ratio:>6.2f}:1  (needs {required:.1f}:1)")

    print()
    if failures:
        print(f"{len(failures)} failure(s) found in {path.name}:")
        for f in failures:
            print(f"  x {f}")
        return 1

    print(f"All {checked} token pair(s) in {path.name} meet WCAG 2.2 AA.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Turtleneck contrast gate (WCAG 2.2 AA) - verifies declared pairs or custom token JSON."
    )
    parser.add_argument(
        "--tokens",
        metavar="PATH",
        type=Path,
        help="Path to JSON file containing color pairs to verify against WCAG 2.2 AA.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-pair output on pass.",
    )
    args = parser.parse_args(argv)

    print("Turtleneck contrast gate (WCAG 2.2 AA)")
    print("-" * 60)

    if args.tokens is not None:
        return check_tokens_file(args.tokens, verbose=not args.quiet)
    return check(verbose=not args.quiet)


if __name__ == "__main__":
    sys.exit(main())
