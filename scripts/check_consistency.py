#!/usr/bin/env python3
"""
Turtleneck consistency gate.

The same protocol is stated in README.md, SKILL.md and six per-agent rules files. Those copies
had already drifted apart once (rules/AGENTS.md had silently lost the Requirements Interview
phase entirely). This gate makes that class of bug a build failure.

Checks
------
1. The canonical 4-phase pipeline line is byte-identical everywhere it is stated.
2. The phase names are exactly the canonical four, in order.
3. Every rules file actually contains the Requirements Interview / JTBD step.
4. Every rules file points agents into the knowledge base.
5. Every `.turtleneck/references/*.md` path cited anywhere resolves to a real file in
   references/ — so an installed rule can never cite a document that does not ship.
6. No references/*.md file is orphaned: each one is reachable from SKILL.md.
7. No LaTeX math delimiters in prompt-facing markdown (agents do not render TeX).

Exit code 0 = consistent. Non-zero = at least one violation.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CANONICAL_PIPELINE = (
    "1. Workspace Analysis \u2500\u2500\u25ba 2. Requirements Interview "
    "\u2500\u2500\u25ba 3. Blueprint Alignment \u2500\u2500\u25ba 4. Production Build"
)
PHASES = ["Workspace Analysis", "Requirements Interview", "Blueprint Alignment", "Production Build"]

PIPELINE_FILES = ["README.md", "SKILL.md"] + [
    f"rules/{p.name}" for p in sorted((ROOT / "rules").iterdir())
]

RULES_FILES = [f"rules/{p.name}" for p in sorted((ROOT / "rules").iterdir())]

INTERVIEW_MARKERS = ("Requirements Interview", "Job-To-Be-Done", "JTBD")
REFERENCE_MARKER = ".turtleneck/references/"

REF_PATH_RE = re.compile(r"`(\.turtleneck/references/[A-Za-z0-9_./-]+\.md)`")
SKILL_LINK_RE = re.compile(r"\]\(\./references/([A-Za-z0-9_.-]+\.md)")
LATEX_RE = re.compile(r"\$\\|\$\$|\\ge\b|\\le\b|\\text\{|\\frac\{|R_\{\\text")


def _read(rel: str) -> str:
    path = ROOT / rel
    return path.read_text(encoding="utf-8") if path.exists() else ""


def check() -> int:
    failures: list[str] = []

    # 1 + 2 : canonical pipeline
    for rel in PIPELINE_FILES:
        body = _read(rel)
        if not body:
            failures.append(f"{rel}: file missing")
            continue
        if CANONICAL_PIPELINE not in body:
            stated = next(
                (ln.strip() for ln in body.splitlines() if re.match(r"^\s*1\.\s+\w+.*\u25ba", ln)),
                "<no pipeline line found>",
            )
            failures.append(
                f"{rel}: pipeline line is not canonical\n"
                f"        expected: {CANONICAL_PIPELINE}\n"
                f"        found:    {stated}"
            )
            continue
        order = [p for p in PHASES if p in CANONICAL_PIPELINE]
        if order != PHASES:
            failures.append(f"{rel}: phase order is {order}, expected {PHASES}")
    print(f"[1-2] canonical pipeline checked in {len(PIPELINE_FILES)} files")

    # 3 : interview step survives into every rules file
    for rel in RULES_FILES:
        body = _read(rel)
        if not any(m in body for m in INTERVIEW_MARKERS):
            failures.append(
                f"{rel}: no Requirements Interview / JTBD step "
                f"(this phase was previously lost from every rules file)"
            )
    print(f"[3]   Requirements Interview present in {len(RULES_FILES)} rules files")

    # 4 + 5 : knowledge base links resolve
    cited: set[str] = set()
    for rel in PIPELINE_FILES:
        body = _read(rel)
        hits = REF_PATH_RE.findall(body)
        if rel in RULES_FILES and not hits:
            failures.append(f"{rel}: cites no {REFERENCE_MARKER} paths; installed rules would be "
                            f"cut off from the knowledge base")
        for token in hits:
            cited.add(token)
            real = ROOT / token.replace(".turtleneck/", "", 1)
            if not real.exists():
                failures.append(f"{rel}: cites {token} but {real.relative_to(ROOT)} does not exist")
    print(f"[4-5] {len(cited)} knowledge base paths cited, all resolved"
          if not any("does not exist" in f for f in failures)
          else f"[4-5] {len(cited)} knowledge base paths cited")

    # 6 : no orphaned reference docs
    ref_dir = ROOT / "references"
    all_refs = {p.name for p in ref_dir.glob("*.md")}
    linked = set(SKILL_LINK_RE.findall(_read("SKILL.md")))
    orphans = sorted(all_refs - linked)
    if orphans:
        failures.append(
            "orphaned reference docs (never linked from SKILL.md, so progressive "
            "disclosure never reaches them): " + ", ".join(orphans)
        )
    dangling = sorted(linked - all_refs)
    if dangling:
        failures.append("SKILL.md links to missing files: " + ", ".join(dangling))
    print(f"[6]   {len(all_refs)} reference docs, {len(linked)} reachable from SKILL.md")

    # 6b : reference implementations stay wired into the skill
    ex_dir = ROOT / "examples"
    ex_all = {p.name for p in ex_dir.glob("*.html")}
    skill_txt = _read("SKILL.md")
    # examples are cited as inline-code spans in SKILL.md, so match any ./examples/*.html mention
    ex_linked = set(re.findall(r"\./examples/([A-Za-z0-9_.-]+\.html)", skill_txt))
    ex_orphan = sorted(ex_all - ex_linked)
    if ex_orphan:
        failures.append(
            "reference implementations not wired into SKILL.md (the skill would tell, not "
            "show): " + ", ".join(ex_orphan)
        )
    ex_dangling = sorted(ex_linked - ex_all)
    if ex_dangling:
        failures.append("SKILL.md links to missing examples: " + ", ".join(ex_dangling))
    print(f"[6b]  {len(ex_all)} example files, {len(ex_linked)} reachable from SKILL.md")

    # 7 : no LaTeX in prompt-facing markdown
    md_files = [ROOT / "README.md", ROOT / "SKILL.md"]
    md_files += sorted((ROOT / "rules").iterdir())
    md_files += sorted(ref_dir.glob("*.md"))
    latex_hits = []
    for path in md_files:
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if LATEX_RE.search(line):
                latex_hits.append(f"{path.relative_to(ROOT)}:{n}")
    if latex_hits:
        failures.append("LaTeX math in prompt markdown (agents do not render TeX): "
                        + ", ".join(latex_hits[:12])
                        + (" ..." if len(latex_hits) > 12 else ""))
    print(f"[7]   LaTeX-free check across {len(md_files)} markdown files")

    print()
    if failures:
        print(f"{len(failures)} consistency violation(s):")
        for f in failures:
            print(f"  x {f}")
        return 1

    print("Pipeline, interview step, knowledge base links and reference graph are consistent.")
    return 0


def main() -> int:
    print("Turtleneck consistency gate")
    print("-" * 60)
    return check()


if __name__ == "__main__":
    sys.exit(main())
