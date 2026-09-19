# Turtleneck

> **Design taste, encoded — and enforced.**

A senior UI/UX architect for your AI coding agent.

Most design prompts *describe* good taste and hope. Turtleneck is a working system: it profiles
your codebase, interviews you about the job to be done, aligns on a layout, and ships
accessible, anti-slop interfaces — and the repository ships its own exam, failing the build the
moment its docs, tokens, or examples violate the rules they teach.

```
1. Workspace Analysis ──► 2. Requirements Interview ──► 3. Blueprint Alignment ──► 4. Production Build
```

---

## Why this exists

AI-generated UI has a tell: purple nebula blobs, unreadable 10%-opacity glass, 800ms animations,
hollow bento cards, buttons with two states. Turtleneck's job is to make that impossible by
giving your agent the instincts of a senior design engineer — and the discipline to check
itself.

It is built on three ideas:

1. **Interview before building — but never over-interview.** Never assume a dark developer
   aesthetic on a vague brief: confirm the archetype, the job-to-be-done, and the density; pitch
   2–3 layouts; wait for a choice. For a small tweak or an explicit brief, take the fast path or
   go straight to Phase 4 — a full interview on a two-minute fix is a protocol violation.
2. **Show, don't tell.** The `examples/` are live reference implementations the skill mirrors —
   not decoration.
3. **Prove, don't promise.** Every hard rule (contrast, focus states, motion budgets) is asserted
   by a script, so "WCAG AA" is a test result, not a vibe.

---

## Quick start

Run the installer in your project root. It auto-detects your tooling and **never overwrites a
file you already own.**

```bash
python path/to/turtleneck/scripts/install.py          # auto-detect
python path/to/turtleneck/scripts/install.py --all    # every supported agent
```

| Your tool | Install flag | What you get |
| :--- | :--- | :--- |
| Any / generic (Codex, Aider, OpenHands) | *(default)* | `AGENTS.md` |
| Claude Code | `--claude` / `--claude-skill` | rules, or the full skill |
| Cursor | `--cursor` | `.cursorrules` |
| Windsurf / Cascade | `--windsurf` | `.windsurfrules` |
| GitHub Copilot | `--copilot` | `.github/copilot-instructions.md` |
| Cline | `--cline` | `.clinerules` |
| Google Antigravity | `--antigravity` | global skill install |

### Compatibility

| Component | Runtime requirements |
| :--- | :--- |
| `scripts/install.py` + all three gates | Python **3.9+**, standard library only |
| `tests/` | Python **3.9+**, `pytest` (CI pins `pytest==9.1.1` on 3.11 and 3.12; also passes on Windows, Python 3.13 tested) |
| Agent rules (`rules/`, `SKILL.md`) | Markdown/plain-text consumers — no runtime; framework detection covers React/Next.js, Vue 3, Svelte 5, Tailwind CSS, vanilla HTML/CSS, plus React Native / Flutter / SwiftUI via `references/mobile-touch-and-native.md` |
| Playwright scrapers (maintainer-only) | `python 3.x` + `requirements-dev.txt` (Playwright) — not part of any install |

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

**Phase 2 — Requirements Interview.** Four questions: archetype, job-to-be-done, density, and a
choice between 2–3 concrete layouts. See
`references/requirements-interview-framework.md`. The interview is the *ceiling*, not the default:
a **fast path** skips it when your brief already names the archetype, surface, density, and layout
direction — the skill restates the inferred constraints in one preflight, raises at most one
genuine ambiguity, and builds. A **time-boxed** run compresses Phases 1–2 the same way, and a
small/one-component request skips straight to Phase 4. Every build's Output Contract records which
mode it used, so skipping the interview is auditable, not silent.

**Phase 3 — Blueprint Alignment.** Locks realistic mock data and design tokens drawn from your
existing patterns, then runs the anti-slop gate (`references/taste-vs-slop-matrix.md`).

**Phase 4 — Production Build.** Five-state controls, `44×44px` targets, `80–120ms` feedback,
compositor-only motion, `prefers-reduced-motion` fallbacks, and WCAG 2.2 AA contrast — then
verifies the palette with `scripts/check_contrast.py` before claiming compliance.

### The five archetypes

Every design decision starts from one of five fully-tokened archetypes
(`references/design-archetypes.md`):

| Archetype | Feel |
| :--- | :--- |
| High-Trust Corporate | Clean slate, fintech clarity |
| Warm Editorial Paper | Cream canvas, serif headlines |
| Fluid Organics | Soft squircles, tactile controls |
| High-Density Starlight | Dark engineering, keyboard-first |
| Stark Geometric Minimal | Monochrome, zero ornament |

---

## Proof over promises

Three zero-dependency gates assert the repository obeys its own protocol. CI runs all three plus
`pytest`.

```bash
python scripts/check_consistency.py   # pipeline parity, interview step, reference graph, no LaTeX
python scripts/check_contrast.py      # all 46 declared colour pairs vs WCAG 2.2 AA
python scripts/check_examples.py      # examples honour focus-visible, reduced-motion, no `transition: all`
pytest tests/ -q                      # installer safety contract + gates (74 tests)
```

`check_contrast.py` fails if the documentation ever drifts from the values it verifies, so a
token can't be quietly weakened. `check_examples.py` keeps the reference implementations honest.

### What this guarantees — and what it does not

The gates are scoped, heuristic checks on *declared* inputs, not a certification of an arbitrary
product UI:

* **Guaranteed:** this repository's declared colour pairs meet WCAG 2.2 AA thresholds; the
  reference examples carry the `:focus-visible`, `prefers-reduced-motion`, compositor-only
  transitions, and accessible names the protocol mandates; and the protocol text is consistent
  across every prompt file.
* **Not guaranteed:** that any UI an agent later generates is WCAG 2.2 AA compliant. The example
  checker is regex-based — it does not validate semantic structure, keyboard behaviour, runtime
  states, ARIA correctness, responsive layouts, DOM-computed contrast, or visual regressions; and
  the contrast gate only sees colour pairs someone declared. Do not claim "WCAG compliant" off a
  token/example gate — claim only what a specific check actually ran.

The full statement of scope, plus the fast-path rules for skipping the interview on an explicit
brief, lives in `references/verification-scope.md`.

---

## Repository layout

```text
turtleneck/
├── SKILL.md              # skill entrypoint (Agent Skills / Antigravity spec)
├── rules/                # drop-in rules for Claude, Cursor, Windsurf, Copilot, Cline, AGENTS.md
├── references/           # the knowledge base: tokens, archetypes, craft, a11y, heuristics
│   ├── deep_research/    # committed headless benchmark captures (authoritative)
│   └── award_research/   # award-site synthesis (authoritative)
├── examples/             # live reference implementations the skill mirrors
├── scripts/              # install.py + the three verification gates (+ maintainer-only scrapers)
└── tests/                # installer + gate test suite
```

---

## Maintainer notes

The Playwright scrapers in `scripts/` are **not** part of a normal build — the committed captures
are authoritative and `SKILL.md` tells agents not to run scrapers. To regenerate:

```bash
pip install -r requirements-dev.txt
playwright install chromium
python scripts/research_award_sites.py
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
