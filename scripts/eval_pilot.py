#!/usr/bin/env python3
"""
Turtleneck Phase C Pilot Evaluation Harness.

Runs or evaluates controlled 3-arm comparison runs:
  Arm 1: Baseline (No Turtleneck)
  Arm 2: Current (v2.0.0 additive mandates)
  Arm 3: Candidate (Autonomous decision loop + non-negotiables)

Across 4 domain briefs:
  1. Product Proof: Turtleneck Landing Page
  2. Expressive Cultural / Event: Archipelago 2027 Biennial
  3. High-Density Operational Dashboard: Water Treatment Telemetry
  4. Mobile-First Booking Flow: Dental Studio Appointment
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

try:
    import check_examples
    from check_contrast import contrast_ratio
except ImportError:
    check_examples = None
    contrast_ratio = None


BRIEFS = {
    "brief-1-landing": {
        "title": "Turtleneck Landing Page (Product Proof)",
        "prompt": (
            "Create a landing page for Turtleneck, a product design intelligence skill for AI coding agents. "
            "Demonstrate how it improves agent decision-making. Include install snippets, core principles, "
            "and an authentic product surface demo. Avoid decorative terminal chrome, calipers, or audit chips."
        ),
        "domain": "developer-tooling",
        "forbidden_patterns": [
            r"PASS/FAIL",
            r"SFX:\s*ON",
            r"8PT\s*GRID",
            r"cluster-04",
            r"p99\s*latency",
        ],
    },
    "brief-2-cultural": {
        "title": "Archipelago 2027 Biennial (Expressive Cultural)",
        "prompt": (
            "Build a promotional and ticketing landing page for 'Archipelago 2027', an international experimental "
            "architecture and sound biennial held across five volcanic islands. Needs atmosphere, strong typography, "
            "curatorial statement, program lineup, and ticket tier selector. Make it distinctive and expressive "
            "WITHOUT defaulting to dark developer starlight, terminal windows, or atelier drafting workbench tropes."
        ),
        "domain": "cultural-event",
        "forbidden_patterns": [
            r"PASS/FAIL",
            r"cluster-",
            r"req/s",
            r"p99",
            r"git\s+clone",
            r"npm\s+install",
            r"Atelier",
        ],
    },
    "brief-3-dashboard": {
        "title": "Water Treatment Telemetry (Dense Operational)",
        "prompt": (
            "Build a real-time operations telemetry dashboard for a municipal water treatment plant monitoring "
            "pump pressures (PSI), chemical filtration stages (pH, chlorine, turbidity NTU), and flow rates (MGD) "
            "across 12 zones. Needs urgent threshold alerts, filter controls, dense scannable tables, and zone breakdown. "
            "Legitimate industrial operational telemetry — no generic decorative cards or marketing fluff."
        ),
        "domain": "industrial-telemetry",
        "forbidden_patterns": [
            r"PASS/FAIL",
            r"SFX:\s*ON",
            r"Unleash\s+AI",
            r"revolutionary",
            r"10x\s+your",
        ],
    },
    "brief-4-mobile": {
        "title": "Dental Studio Appointment Booking (Mobile-First)",
        "prompt": (
            "Build a mobile-first appointment booking flow for 'Alabaster Dental Studio' (viewport: 390x844). "
            "Include service selection (cleaning, whitening, consultation), dentist preference, interactive date/time slot picker, "
            "patient contact details, and a booking confirmation step with state preservation and error handling. "
            "Thumb-friendly touch ergonomics (>=44px), zero horizontal overflow, clear progress indicator."
        ),
        "domain": "consumer-healthcare",
        "forbidden_patterns": [
            r"PASS/FAIL",
            r"p99",
            r"latency",
            r"req/s",
            r"cluster-",
            r"terminal",
        ],
    },
}


@dataclass
class EvalResult:
    target_path: str
    brief_id: str
    arm_id: str
    gate_passed: bool
    gate_violations: list[str]
    forbidden_pattern_hits: list[str]
    has_focus_visible: bool
    has_reduced_motion: bool
    has_compositor_transitions: bool
    text_contrast_pass: bool
    touch_target_pass: bool
    score: float


def evaluate_html_file(path: Path, brief_id: str, arm_id: str = "unknown") -> EvalResult:
    text = path.read_text(encoding="utf-8")
    brief_meta = BRIEFS.get(brief_id, {})
    forbidden = brief_meta.get("forbidden_patterns", [])

    gate_violations: list[str] = []
    if check_examples:
        gate_violations = check_examples.check_example(path)

    forbidden_hits: list[str] = []
    for pat in forbidden:
        if re.search(pat, text, re.IGNORECASE):
            forbidden_hits.append(pat)

    has_focus = ":focus-visible" in text and "outline-offset: 2px" in text
    has_motion = "prefers-reduced-motion" in text
    has_transitions = not bool(re.search(r"transition:\s*all\b", text))
    text_contrast = not any("needs >= 4.5:1" in v for v in gate_violations)
    touch_pass = not any("accessible name" in v for v in gate_violations)

    # Compute objective score out of 100
    points = 100.0
    if not has_focus:
        points -= 20.0
    if not has_motion:
        points -= 15.0
    if not has_transitions:
        points -= 15.0
    if not text_contrast:
        points -= 20.0
    if forbidden_hits:
        points -= len(forbidden_hits) * 10.0
    if gate_violations:
        points -= min(len(gate_violations) * 5.0, 30.0)

    score = max(0.0, points)
    gate_passed = len(gate_violations) == 0 and len(forbidden_hits) == 0

    return EvalResult(
        target_path=str(path),
        brief_id=brief_id,
        arm_id=arm_id,
        gate_passed=gate_passed,
        gate_violations=gate_violations,
        forbidden_pattern_hits=forbidden_hits,
        has_focus_visible=has_focus,
        has_reduced_motion=has_motion,
        has_compositor_transitions=has_transitions,
        text_contrast_pass=text_contrast,
        touch_target_pass=touch_pass,
        score=score,
    )


def print_scorecard(results: list[EvalResult]) -> None:
    print("\n" + "=" * 80)
    print("TURTLENECK CONTROLLED PILOT SCORECARD")
    print("=" * 80)
    header = f"{'Brief':<22} | {'Arm':<12} | {'Score':<6} | {'Gate':<6} | {'Forbidden Hits':<14} | {'Violations'}"
    print(header)
    print("-" * 80)

    for r in results:
        gate_str = "PASS" if r.gate_passed else "FAIL"
        f_hits = str(len(r.forbidden_pattern_hits))
        v_count = str(len(r.gate_violations))
        print(f"{r.brief_id:<22} | {r.arm_id:<12} | {r.score:>5.1f} | {gate_str:<6} | {f_hits:<14} | {v_count}")
    print("=" * 80 + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Turtleneck Pilot Eval Harness")
    parser.add_argument("--eval-file", type=Path, help="Evaluate a single HTML file")
    parser.add_argument("--brief", choices=list(BRIEFS.keys()), help="Brief ID for single file eval")
    parser.add_argument("--arm", choices=["baseline", "current", "candidate"], default="candidate")
    parser.add_argument("--dir", type=Path, help="Directory containing pilot outputs")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    results: list[EvalResult] = []

    if args.eval_file:
        brief = args.brief or "brief-1-landing"
        res = evaluate_html_file(args.eval_file, brief, args.arm)
        results.append(res)
    elif args.dir and args.dir.exists():
        for path in sorted(args.dir.rglob("*.html")):
            # deduce brief from parent dirs
            parent_name = path.parent.name
            matched_brief = "brief-1-landing"
            for b in BRIEFS:
                if b in str(path):
                    matched_brief = b
                    break
            arm = "candidate"
            for a in ["baseline", "current", "candidate"]:
                if a in str(path):
                    arm = a
                    break
            res = evaluate_html_file(path, matched_brief, arm)
            results.append(res)
    else:
        # Default self-eval on repo index.html
        res = evaluate_html_file(ROOT / "index.html", "brief-1-landing", "candidate")
        results.append(res)

    if args.json:
        print(json.dumps([asdict(r) for r in results], indent=2))
    else:
        print_scorecard(results)

    return 0 if all(r.gate_passed for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
