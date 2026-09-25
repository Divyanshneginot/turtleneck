---
name: turtleneck
description: >-
  Use when designing, building, restyling, or reviewing a user-facing web or
  native interface where visual direction, interaction quality, accessibility,
  responsive behavior, or design-system consistency matters. Skip for non-visual
  backend/CLI work and exact reproduction of an already supplied design.
---

# Autonomous UI/UX Architect Protocol

Transforms user UI requests into bespoke, production-ready interfaces by first scanning the local workspace, conducting a structured requirement interview with the user, aligning on architecture, and implementing anti-slop code.

---

## When to use (and when not to)

Use this skill when the task is to **design, build, restyle, or review a user-facing surface** —
a page, component, dashboard, form, or design system. It earns its keep when the brief is vague
("make it look professional") or when layout, density, and feel are genuinely undecided.

Do not use it for:

* Pure backend, CLI, or data-pipeline work with no user-facing surface.
* A one-line styling tweak — a full interview would be ceremony. Apply the Phase 4 craft rules
  directly instead.
* Pixel-perfect replication of a supplied design. Follow the supplied design; borrow only the
  accessibility, motion, and state-completeness rules from Phase 4.

### Execution modes (tempo)

Always pick the **least ceremony the brief earns** — internalize the full pipeline as the ceiling,
not the default:

| Mode | When | What to do |
| :--- | :--- | :--- |
| **Direct Phase 4** | One component, one style tweak, a fix, or the user says "just do it" | Skip Phases 1–3; apply Phase 4 craft rules directly; emit compact completion report. |
| **Time-boxed Fast Path** | Hard deadline, or a brief that already names scope + stack | Skip the interview. Infer archetype/density from codebase + request; state call + 1 alternative in 1 line; build. |
| **Fast Path** | Explicit brief supplying surface, density, layout, and direction | Skip multi-question interview. Restate inferred constraints in 1 preflight line; surface <= 1 ambiguity; build. |
| **Full Pipeline** | Vague, greenfield, or consequential surface (flagship page, design system) | Run all four phases end-to-end, including structured interview and blueprint alignment. |

Under time pressure, self-check *tempo* explicitly: if the task is a small or well-scoped change,
say so in one line and take the Direct Phase 4 / Time-boxed route. Burning a full interview cycle
on a two-minute fix is a protocol violation.

---

## Reference implementations (show, don't tell)

Before building, open the reference implementation closest to your target and mirror its craft.
These files are the executable form of this protocol — the gates in `scripts/` assert that they
obey it.

| File | What it demonstrates |
| :--- | :--- |
| `./examples/index.html` | The 5-archetype workbench. Switch `data-archetype` between corporate / editorial / fluid / starlight / minimal and compare token systems, density, and chrome. |
| `./examples/high-density-tracker.html` | High-Density Starlight, keyboard-first operational UI: dense tables, command palette, hotkeys, tab and focus states. |
| `./examples/creative-craft.html` | Editorial / instrument craft: serif display tension, tactile button physics, warm dark surfaces. |
| `./examples/accessible-dialog-palette.html` | Accessible dialogs & command palette: focus trapping, Escape dismissal, trigger restoration, 5-state buttons. |
| `./examples/form-validation-states.html` | Accessible form validation: error summary, inline field states, aria-describedby links, and tap targets. |

---

## 4-Phase Operational Pipeline

```
1. Workspace Analysis ──► 2. Requirements Interview ──► 3. Blueprint Alignment ──► 4. Production Build
```

This pipeline is identical in `README.md`, `SKILL.md` and every file in `rules/`.
`scripts/check_consistency.py` fails the build if the phase names diverge.

Read a reference only when its phase applies — never preload the whole set.

---

### Phase 1: Workspace Analysis & Research Review
Before asking questions or drafting UI, inspect the repository and the committed benchmarks:

1. **Stack & Tooling Detection** — refer to the [Workspace Scanner Guide](./references/workspace-scanner-guide.md) and [Framework Integrations](./references/framework-integrations.md):
   * Inspect package files (`package.json`, `requirements.txt`, lockfiles).
   * Identify the frontend framework (React, Next.js, Vue, Svelte, HTML/CSS — or a native stack:
     React Native, Flutter, SwiftUI). Web rules are not native rules; when the target is a phone
     or a native app, also load the [Mobile, Touch & Native Ergonomics](./references/mobile-touch-and-native.md)
     reference.
   * Identify the styling engine (Tailwind CSS, Vanilla CSS, Radix UI, CSS Modules).
   * Record existing theme tokens and component directory conventions.
   * Match code generation directly to the discovered framework idioms.
2. **Review Existing Headless Research & Feel**:
   * The committed captures in `references/deep_research/` and `references/award_research/` are
     authoritative. Do NOT run scrapers against live sites during a build. The scripts in
     `scripts/` are an optional maintainer-only regeneration path and need Playwright
     (see `requirements-dev.txt`).
   * Pick category benchmarks and record a synthesis manifest using the
     [Design Research Playbook](./references/design-research-playbook.md).
   * Feel the soul of the benchmarks — narrative pacing, visual weight, spatial breathing, and
     micro-tactility — not just hex codes. The
     [Creative Direction Guide](./references/creative-direction-guide.md) covers authentic
     personality and materiality.
   * Enforce the **Creative Synthesis Protocol** — refer to the
     [Award-Winning Craft Playbook](./references/award-winning-craft-playbook.md) and the
     [Creative Synthesis Protocol](./references/creative-synthesis-protocol.md):
     * Blend atmosphere, interaction physics, typography tension, and layout density from 4+
       different sources into something new. Never lean on one reference.
     * Forbid 1:1 cloning of metaphors, copy, diff blocks, terminal cursors, or recognizable
       brand gimmicks. Extract the WHY, invent a new HOW.

---

### Phase 2: Requirements Interview & Architectural Direction

The authoritative Execution Modes table determines whether this phase runs. Do not run a multi-question
interview when the brief earns a fast path or Direct Phase 4. Never assume a dark developer aesthetic by
default. See [Verification Scope & Fast Path](./references/verification-scope.md).

1. **Derive Direction from Subject Matter First (Before Archetypes)**:
   * **Audience & Context**: Who uses this interface, in what physical/cognitive environment, and under what load?
   * **Primary Job-To-Be-Done**: Identify the single decisive outcome (monitoring, triage, editing, onboarding).
   * **Domain Materials & Vernacular**: Ground visual choices in the product's real-world subject matter (e.g. clinical precision, financial ledger clarity, technical telemetry, physical publication). Spend boldness in one intentional place.
   * **Genericity Check**: *Could this visual direction and layout be reused unchanged for another product in this category?* If yes, revise it. Reject interchangeable template defaults.
2. **Archetypes as Constraint Lenses (Not Themes or Presets)** — refer to the [Design Archetypes Catalog](./references/design-archetypes.md):
   Use archetypes as diagnostic constraint lenses to govern trust, density, chrome, and interaction physics—never as cosmetic skins or theme presets:
   * **A. High-Trust Corporate**: Lens for institutional trust, clean slate canvas (`#f6f9fc`), crisp borders, fintech/SaaS clarity.
   * **B. Warm Editorial Paper**: Lens for reading focus, warm cream canvas (`#fbfbfa`), serif headlines, minimal chrome.
   * **C. Fluid Organics**: Lens for mobile ergonomics, squircle geometry (`10-14px`), tactile segmented controls.
   * **D. High-Density Starlight**: Lens for keyboard-first telemetry, deep dark canvas (`#08090a`), dense tables, hotkeys.
   * **E. Stark Geometric Minimal**: Lens for architectural discipline, pitch black canvas (`#000000`), razor borders, monochrome semaphores.
3. **Present 2-3 Concrete Architecture Options** (Full Pipeline):
   * Confirm target density: high-density operational vs balanced SaaS vs consumer guided flow.
   * Use the [Requirements Interview Framework](./references/requirements-interview-framework.md) to pitch 2-3 concrete layout options and wait for user selection before building.

---

### Phase 3: Blueprint & Token Alignment
Once the user approves a layout choice:

1. Formulate the exact data schema for UI components (mock realistic, domain-accurate data).
2. Lock in design tokens compatible with the scanned workspace:
   * Spacing grid, type scale, semantic colour roles and elevation — see
     [Design Tokens](./references/design-tokens.md).
   * Surface patterns and accessible primitives for the six product surfaces — see
     [Full Product Design System](./references/full-product-design-system.md).
3. **Validate Against the Taste vs. Slop Matrix** — refer to the
   [Taste vs. Slop Matrix](./references/taste-vs-slop-matrix.md):
   * **Modern patterns encouraged when done right**:
     * Glassmorphism: strictly for floating chrome, high fill opacity (`80-90%`), hairline
       border, text contrast >= 4.5:1.
     * Bento layouts: high data density, real functional widgets, zero decorative 3D balls.
     * Gradients: subtle single-source rim lighting guiding attention to primary actions.
   * **Slop strictly rejected**: illegible 10% glass opacity, giant saturated nebula blobs,
     800ms sluggish animations, buzzword copy.

---

### Phase 4: Production Implementation & Master Craft Verification
1. **Component Engineering** — refer to the
   [Master Craft Benchmark](./references/master-ui-craft-benchmark.md),
   [Engineering Craft Recipes](./references/engineering-craft-recipes.md) and
   [Framework Integrations](./references/framework-integrations.md):
   * Emit idiomatic code matching the detected stack: React (TSX/hooks), Vue (`<script setup>`),
     Svelte 5 (runes), or Vanilla Web Platform (zero-dependency HTML/CSS/JS). When targeting
     mobile/desktop native (React Native, Flutter, SwiftUI), apply platform mappings from
     [Mobile, Touch & Native Ergonomics](./references/mobile-touch-and-native.md).
   * Generate modular, clean components following the discovered repo conventions.
   * **Motion & Timing**: `80-120ms` state feedback, `200-240ms` enter, `100-140ms` exit
     (asymmetric exit rule), `cubic-bezier(0.16, 1, 0.3, 1)` or critical springs (damping ratio
     `zeta >= 0.85`). GPU compositor thread isolation — animate `transform`/`opacity` only,
     never `transition: all`.
   * **Reduced Motion**: always ship a `@media (prefers-reduced-motion: reduce)` fallback.
   * **Typography Precision**: negative tracking on headings, `font-variant-numeric: tabular-nums`
     for data cells, `text-wrap: balance` on headlines.
   * **Concentric Radiuses**: `R_outer = R_inner + Padding`.
   * **5-State Completeness**: `default`, `hover`, `active` (scale 0.98), `focus-visible`
     (2px ring), `disabled`.
   * **Touch Ergonomics**: minimum `44x44px` physical tap targets.
2. **Usability & Accessibility Audit (WCAG 2.2 AA)** — refer to
   [UX Heuristics](./references/ux-heuristics.md) and the
   [Accessibility Checklist](./references/accessibility-checklist.md):
   * 4.5:1 text contrast, 3:1 on UI component boundaries and graphical objects.
   * Focus rings with 3:1 contrast against both the element and the background canvas.
   * Trap-free modal keyboard navigation with `Escape` dismiss and trigger focus restoration.
   * Honour response-latency budgets and never convey state by colour alone.
3. **Walkthrough & Verification**:
   * Verify zero console errors and zero layout shifts.
   * Verify the emitted palette with `scripts/check_contrast.py` before claiming AA compliance.
   * Acknowledge the limits: the gates check *declared* tokens and *textual* markers — they do not
     certify an arbitrary generated UI as WCAG 2.2 AA compliant. Do not claim WCAG compliance off
     a token/example gate; claim only what a specific check actually ran
     ([Verification Scope & Fast Path](./references/verification-scope.md)).
   * Close with the **Output Contract** or **Compact Completion Report** below — no un-audited claims.

### Output Contract

End consequential builds (Full Pipeline, Fast Path, Time-boxed) with this audit contract:

```text
Archetype Lens   : <chosen lens> — and the one-line rationale
Stack detected   : <framework> + <styling engine>
Layout           : <option picked or inferred architecture>
Density          : operational / balanced / guided
Tokens           : canvas <hex> · surface <hex> · accent <hex> · muted <hex> (<ratio>:1, verified)
Accessibility    : focus-visible [yes] · reduced-motion [yes] · tap targets >=44px [yes]
                   · text contrast >=4.5:1 [verified by scripts/check_contrast.py]
Reference used   : <examples/*.html mirrored, if any>
Files changed    : <list>
Deliberate breaks: <any rule intentionally violated, and why — empty is the goal>
Execution mode   : full-pipeline / fast-path / time-boxed — and why
Interview        : conducted [yes/no] · if skipped, reason: <one line>
```

#### Compact Completion Report (Direct Phase 4)

For single components, one-line style tweaks, and direct fixes, do not emit the full 11-line contract. Use this compact report:

```text
Mode             : Direct Phase 4 (<one-line reason>)
Files changed    : <list>
Checks run       : contrast (<ratio>:1, verified) · focus-visible [yes] · reduced-motion [yes]
Deliberate breaks: <any rule intentionally violated, or "none">
```
