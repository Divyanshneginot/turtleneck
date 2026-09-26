# Turtleneck

[![CI](https://github.com/Divyanshneginot/turtleneck/actions/workflows/ci.yml/badge.svg)](https://github.com/Divyanshneginot/turtleneck/actions)
![Python](https://img.shields.io/badge/python-3.9%2B-blue?logo=python)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

> **Product Design Intelligence for AI coding agents.** Version 2.0.0.
> Decide, then make. Do not decorate an undefined product.

Turtleneck is not merely a styling checklist. It is a product-design decision system: it turns an outcome into an information architecture, interaction model, visual direction, state model, and implementation plan before writing the UI across Claude Code, Cursor, Windsurf, Copilot, Cline, Codex, OpenHands, and all AI coding agents.

```
1. Workspace Analysis ──► 2. Requirements Interview ──► 3. Blueprint Alignment ──► 4. Production Build
```

---

## Why this exists

AI-generated UI has a tell: arbitrary purple gradients, floating glass cards, excessive pills, meaningless charts, and uniform card grids. Turtleneck makes that impossible by giving your agent the instincts of a senior product designer — and the discipline to verify itself.

It is built on three core tenets:

1. **Decide, then make — with adaptive tempo.** First determine what the user is trying to accomplish, what they must decide, and choose the archetype from the job. Select the smallest process that produces a sound decision: Direct mode for tiny changes, Fast path for known scopes, Discovery for vague or greenfield surfaces.
2. **Specialized capabilities for decisions.** When users don't know what they need, make the interface help them decide with guided recommenders, quizzes, and template builders that explain rationale and reveal cause and effect.
3. **Prove, don't promise.** Automated test gates assert WCAG 2.2 AA contrast, `:focus-visible` rings, reduced-motion fallbacks, and compositor-only transitions before code is claimed complete.

---

## Quick start

Run the installer in your project root. It auto-detects your tooling and **never overwrites a
file you already own.**

```bash
python path/to/turtleneck/scripts/install.py          # auto-detect
python path/to/turtleneck/scripts/install.py --all    # every supported agent
python path/to/turtleneck/scripts/install.py --skill  # universal agent skill (.agents/skills/)
```

| Your tool | Install flag | What you get |
| :--- | :--- | :--- |
| Universal Agent Skill (any agent) | `--skill` / `--global-skill` | full skill in `.agents/skills/` or `~/.agents/skills/` |
| Any repository (`AGENTS.md`) | *(default)* | `AGENTS.md` (Codex, Aider, OpenHands) |
| Claude Code | `--claude` / `--claude-skill` | rules, or the full skill |
| Cursor | `--cursor` | `.cursorrules` |
| Windsurf / Cascade | `--windsurf` | `.windsurfrules` |
| GitHub Copilot | `--copilot` | `.github/copilot-instructions.md` |
| Cline & Roo Code | `--cline` | `.clinerules` |
| Google Antigravity | `--antigravity` | global skill install (`~/.gemini/`) |

### Compatibility

| Component | Runtime requirements |
| :--- | :--- |
| `scripts/install.py` + all gates | Python **3.9+**, standard library only |
| `tests/` | Python **3.9+**, `pytest` (standard library + pytest alone) |
| Agent rules (`rules/`, `SKILL.md`) | Markdown/plain-text consumers — zero runtime dependencies |

**Safety first.** If a destination already holds *your* content, the installer refuses (exit 2)
and prints the protected line. Escapes: `--dry-run` (plan only), `--append` (merge between
`<!-- turtleneck:begin/end -->` markers, idempotent), `--force` (after writing a
`.turtleneck.bak`), `--uninstall` (restore, remove only what it owns).

Rules installs also copy the knowledge base to `.turtleneck/references/` so the rules' links
resolve. `--no-references` skips it.

**See it rendered.** Open `examples/index.html` in a browser and flip the archetype — it's the
spec, running.

---

## How it works

**Phase 1 — Workspace Analysis.** Detects your framework and styling engine (React, Next.js,
Vue, Svelte, Tailwind, CSS Modules, Radix — or React Native, Flutter, SwiftUI) and emits idiomatic
code for what it finds. It reads the committed benchmark captures — it never scrapes live sites.
Mobile and native targets additionally load `references/mobile-touch-and-native.md` for thumb
zones, touch targets, gesture timing, and the native-stack token mapping.

**Phase 2 — Requirements Interview & Architectural Direction.** The interview is the *ceiling*, not the default.
The four modes govern tempo:
* **Direct Phase 4:** Small fixes or single components skip Phases 1–3 and emit a 4-line Compact Completion Report.
* **Time-boxed Fast Path:** Deadlines skip the interview; infer archetype/density and proceed with a 1-line call + alternative.
* **Fast Path:** Explicit briefs (surface, density, layout, direction) skip the multi-question interview via a 1-line preflight.
* **Full Pipeline:** Vague, greenfield, or consequential surfaces run the full interview and pitch 2–3 concrete layouts.

Before choosing an archetype, the agent derives direction from the product's **real-world subject matter, audience, and job-to-be-done**, then runs the **Genericity Check** (*"Could this direction be reused unchanged for another product in this category?"*). The five archetypes serve as **diagnostic constraint lenses** for density, chrome, and physics—not interchangeable cosmetic themes.

**Phase 3 — Blueprint Alignment.** Locks realistic mock data and design tokens drawn from your
existing patterns, then runs the anti-slop gate (`references/taste-vs-slop-matrix.md`).

**Phase 4 — Production Build.** Five-state controls, `44×44px` targets, `80–120ms` feedback,
compositor-only motion, `prefers-reduced-motion` fallbacks, and WCAG 2.2 AA contrast — then
verifies the palette with `scripts/check_contrast.py` before claiming compliance.

### The five archetype lenses

Archetypes act as constraint lenses (`references/design-archetypes.md`):

| Archetype Lens | Feel & Constraint |
| :--- | :--- |
| High-Trust Corporate | Clean slate (`#f6f9fc`), crisp borders, fintech clarity |
| Warm Editorial Paper | Cream canvas (`#fbfbfa`), serif display, reading focus |
| Fluid Organics | Soft squircles (`10-14px`), tactile segmented controls |
| High-Density Starlight | Dark engineering (`#08090a`), dense tables, hotkeys |
| Stark Geometric Minimal | Monochrome (`#000000`), zero ornament, razor chassis |

---

## Proof over promises

Four zero-dependency gates assert the repository obeys its own protocol. CI runs all four across
Python 3.11 and 3.12, alongside the pytest suite.

```bash
python scripts/check_frontmatter.py   # SKILL.md trigger-only discovery format & length
python scripts/check_consistency.py   # pipeline parity, interview step, reference graph, no LaTeX
python scripts/check_contrast.py      # all 46 declared colour pairs vs WCAG 2.2 AA
python scripts/check_contrast.py --tokens <path.json>  # verify arbitrary generated palettes
python scripts/check_examples.py      # examples honour focus-visible, reduced-motion, no `transition: all`
pytest tests/ -q                      # installer safety contract + gates (86 tests)
```

`check_contrast.py` fails if the documentation ever drifts from the values it verifies, so a
token can't be quietly weakened. Passing `--tokens <json>` validates generated palettes against
the minimal contrast schema. `check_examples.py` keeps the reference implementations honest.

### Behavioral evaluations (`evals/`)

Turtleneck includes a 10-brief evaluation benchmark in `evals/cases/` and an observable 9-dimension scoring rubric in `evals/rubric.md`:
* **Cases:** Vague greenfield UI, dense telemetry dashboard, mobile form, tiny CSS fix, exact supplied-design replication, modal keyboard behavior, low-contrast regression, explicit time-box, non-UI task (negative trigger test), and accessibility review.
* **Status:** Scaffold and test cases published; initial comparative baseline-vs-treatment benchmark runs are pending execution. Claims remain strictly scoped to what automated gates prove.

### What this guarantees — and what it does not

The gates are scoped, heuristic checks on *declared* inputs, not a certification of an arbitrary
product UI:

* **Guaranteed:** this repository's declared colour pairs meet WCAG 2.2 AA thresholds; custom palettes
  checked via `--tokens` meet mathematical contrast thresholds; the reference examples carry the
  `:focus-visible`, `prefers-reduced-motion`, compositor-only transitions, and accessible names the
  protocol mandates; and the protocol text is consistent across every prompt file.
* **Not guaranteed:** that any UI an agent later generates is WCAG 2.2 AA compliant. The example
  checker is regex-based — it does not validate semantic structure, keyboard behaviour, runtime
  states, ARIA correctness, responsive layouts, DOM-computed contrast, or visual regressions; and
  the contrast gate only sees colour pairs someone declared. Do not claim "WCAG compliant" off a
  token/example gate — claim only what a specific check actually ran.

The full statement of scope, schema specification, and fast-path rules live in `references/verification-scope.md`.

---

## Repository layout

```text
turtleneck/
├── SKILL.md              # universal skill entrypoint (Agent Skills spec for all coding agents)
├── rules/                # drop-in rules for Claude, Cursor, Windsurf, Copilot, Cline, AGENTS.md
├── references/           # the knowledge base: tokens, archetypes, craft, a11y, heuristics
│   ├── deep_research/    # committed headless benchmark captures (authoritative)
│   └── award_research/   # award-site synthesis (authoritative)
├── examples/             # live reference implementations the skill mirrors
├── evals/                # behavioral evaluation suite: 10 test cases, rubric, protocol
├── scripts/              # install.py + the four verification gates (+ maintainer scrapers)
└── tests/                # installer + gate test suite
```

---

## Contributing

The whole point of this repo is that its rules are mechanically enforced, so contributions are
cheap to check. Before you open a PR, make the gates pass:

```bash
python -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/pytest tests/ -q
python scripts/check_consistency.py && python scripts/check_contrast.py && python scripts/check_examples.py
```

The drift-proofs you must respect:

* **Change a colour token?** Update the matching pair in `scripts/check_contrast.py` — it fails if
  the docs and the gate disagree.
* **Add a reference doc?** Link it from `SKILL.md`, or `check_consistency.py` flags it as orphaned.
* **Add an example?** Wire it into `SKILL.md`'s reference table, or the gate calls it out.
* **Touch the pipeline?** The exact line `1. Workspace Analysis ──► … ──► 4. Production Build` must
  stay identical in `README.md`, `SKILL.md` and every file under `rules/`.

---

## License

MIT — see [LICENSE](./LICENSE).
