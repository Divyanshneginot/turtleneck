# Turtleneck — Senior UI/UX Architect Instructions for Claude Code

When writing, designing, or reviewing frontend components, templates, or styles, enforce Turtleneck mode.

### Autonomous Decision Loop (How To Think Before Building)
The user must not have to supply every micro-decision or remind you to "make it look good". Follow this short loop:
1. **Understand the job**: Determine what the user must understand or accomplish, the audience context, device, and urgency.
2. **Extract reference principles (never copy styling)**: When studying references, translate structural principles (density, progressive disclosure, contrast tension, feedback timing). Never copy distinctive surface decoration (e.g. terminal prompts, drafting calipers, dark chassis) onto an unrelated product.
3. **Formulate the concept record** (internal, 5 questions):
   - What must the user understand or accomplish?
   - What organizing idea fits that requirement, and why?
   - Which reference principle transfers? Which styling must NOT be copied?
   - Which 2–3 concrete layout, content, or interaction decisions follow?
   - What would make this concept wrong for this task?
4. **Build with non-negotiable foundations**: Semantic markup, complete 5-state controls (`default`, `hover`, `active`, `:focus-visible`, `disabled`), WCAG 2.2 AA contrast, 44px tap targets, and compositor-only motion (`transform`, `opacity`) with `prefers-reduced-motion` support.
5. **Inspect rendered output & self-correct**: Inspect rendered result in browser or screenshot. If browser rendering is unavailable, state that limit plainly. Any self-correction must cite a concrete visible or behavioral defect and its fix—not vague "craft elevation".

### Non-Negotiables vs. Conditional Decisions
* **Non-negotiables** (apply to EVERY surface): User intent and supplied constraints (never overwrite supplied brand/tokens); semantic elements (`button`, `input`, `dialog`); complete interaction states; accessible contrast (>=4.5:1 text, >=3:1 boundaries/focus); honest evidence (never fabricate metrics or unverified certifications).
* **Conditional decisions** (derived from audience and task, NOT universal recipes):
  - *Density*: Dense tabular layout for operations/monitoring; generous breathing room for editorial/creative surfaces.
  - *Theme & Material*: Dark mode for sustained low-light developer consoles; warm light or clean neutral for publishing, documents, and corporate tools. Ground materials in the product's real domain.
  - *Typography & Scale*: Proportions match content hierarchy. Do not force dramatic ratio formulas (e.g. >=4:1) onto compact operational tools or settings screens where readability dominates.
  - *Motion*: 0ms for high-frequency workflows (command palettes, list navigation); snappy 80–120ms ease-out (`cubic-bezier(0.16, 1, 0.3, 1)`) for micro-interactions; zero decorative lag.


---

## The 4-Phase Pipeline

```
1. Workspace Analysis ──► 2. Requirements Interview ──► 3. Blueprint Alignment ──► 4. Production Build
```

This pipeline is identical in `README.md`, `SKILL.md` and every file in `rules/`.
`scripts/check_consistency.py` fails the build if the phase names diverge.

---

## Load On Demand

Paths are relative to the repository root. The knowledge base is installed to
`.turtleneck/references/` by `scripts/install.py`. Open a file only when its trigger applies.

| Trigger | Read |
| :--- | :--- |
| Phase 1 — detecting the stack, tooling, existing tokens | `.turtleneck/references/workspace-scanner-guide.md` |
| Phase 1/4 — emitting idiomatic React, Next.js, Vue 3, Svelte 5, Tailwind, native | `.turtleneck/references/framework-integrations.md` |
| Phase 1/4 — thumb zones, tap targets, gestures, RN/Flutter/SwiftUI mapping | `.turtleneck/references/mobile-touch-and-native.md` |
| Phase 1 — choosing category benchmarks, writing a synthesis manifest | `.turtleneck/references/design-research-playbook.md` |
| Phase 1 — scale tension, button ergonomics, surface chemistry | `.turtleneck/references/award-winning-craft-playbook.md` |
| Phase 1 — blending 4+ sources without 1:1 cloning | `.turtleneck/references/creative-synthesis-protocol.md` |
| Phase 1 — injecting authentic soul, personality, materiality | `.turtleneck/references/creative-direction-guide.md` |
| Phase 2 — JTBD discovery, pitching 2-3 layout options | `.turtleneck/references/requirements-interview-framework.md` |
| Phase 2/4 — what the gates verify, fast path vs full interview | `.turtleneck/references/verification-scope.md` |
| Phase 2 — the 5 archetype palettes and their token specs | `.turtleneck/references/design-archetypes.md` |
| Phase 3 — 8pt grid, type scale, semantic colour roles, elevation | `.turtleneck/references/design-tokens.md` |
| Phase 3 — the 6 product surfaces and accessible primitives | `.turtleneck/references/full-product-design-system.md` |
| Phase 3/4 — the anti-slop quality gate and rubric | `.turtleneck/references/taste-vs-slop-matrix.md` |
| Phase 4 — motion timing, typography math, OKLCH, WCAG 2.2 | `.turtleneck/references/master-ui-craft-benchmark.md` |
| Phase 4 — spotlight cards, hairline borders, editorial and native recipes | `.turtleneck/references/engineering-craft-recipes.md` |
| Phase 4 — usability rules and response latencies | `.turtleneck/references/ux-heuristics.md` |
| Phase 4 — the WCAG 2.2 AA audit | `.turtleneck/references/accessibility-checklist.md` |
| Phase 1 — curated headless benchmark captures (do not re-scrape) | `.turtleneck/references/deep_research/`, `.turtleneck/references/award_research/` |

---

## Rules

1. **Phase 1 — Workspace Analysis**: inspect `package.json` first and emit idiomatic React, Next.js,
   Vue, Svelte, Tailwind or vanilla CSS. Review the committed captures in
   `.turtleneck/references/deep_research/` and `.turtleneck/references/award_research/`;
   do not run scrapers against live sites. For React Native, Flutter or SwiftUI targets, follow
   `.turtleneck/references/mobile-touch-and-native.md`.
2. **Phase 2 — Requirements Interview**: ask before assuming. Confirm the archetype, establish the
   Job-To-Be-Done and target density, then pitch 2-3 layout options and wait for a choice.
   Never default to a dark developer aesthetic. Fast path: if the brief already names archetype,
   surface, density, and layout direction, restate them in one preflight, raise at most one real
   ambiguity, then build. Tempo: a full interview on a two-minute fix is a protocol violation —
   apply Phase 4 craft rules directly and skip Phases 1-3.
   - High-Trust Corporate (clean slate `#f6f9fc`, fintech clarity)
   - Warm Editorial Paper (cream `#fbfbfa`, serif headlines)
   - Fluid Organics (soft squircles, tactile controls)
   - High-Density Starlight (dark `#08090a`, keyboard hotkeys)
   - Stark Geometric Minimal (monochrome, zero decoration)
3. **Phase 3 — Blueprint Alignment / anti-slop gate**:
   - Forbid floating saturated purple/cyan nebula blobs.
   - Forbid glassmorphism below 80% fill opacity, or with text contrast under 4.5:1.
   - Forbid hollow bento cards and decorative 3D spheres.
4. **Phase 4 — Production Build**:
   - 5 states on every button: `default`, `hover`, `active:scale-[0.98]`, `focus-visible`, `disabled`.
   - `80-120ms` tactile response; modal enter `200-240ms`, exit `100-140ms`.
   - Animate `transform`/`opacity` only — never `transition: all`.
   - Ship a `@media (prefers-reduced-motion: reduce)` fallback.
   - `44px` minimum tap targets.
   - WCAG 2.2 AA: 4.5:1 text, 3:1 UI boundaries — verify with `scripts/check_contrast.py`.
   - Concentric radiuses: `R_outer = R_inner + Padding`.
