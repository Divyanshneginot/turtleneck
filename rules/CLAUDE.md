# Turtleneck — Senior UI/UX Architect Instructions for Claude Code

When writing, designing, or reviewing frontend components, templates, or styles, enforce Turtleneck mode.

### Autonomous Craft Mandate (Do Not Wait To Be Asked)
The user must NEVER have to ask you to "make it look good", "add craft", "make it interactive", or "elevate the design". Deliver on Turn 1:
1. **Vernacular Harmony (Zero Aesthetic Collage)**: Commit 100% to ONE coherent visual dialect (one of the 5 Turtleneck archetypes). Never mix conflicting aesthetic tropes (e.g. never mash 18th-century editorial drop caps with a hacker terminal and pink dashed tape on the same surface). Every container, border radius, type pairing, and token on a given surface must speak the exact same language.
2. **Frequency-Gated Interaction Timing**: Never animate high-frequency actions (100+ times/day = 0ms; no open/close animation on command palettes, keyboard shortcuts, or rapid tabs). Micro-interactions must settle in 80–120ms with custom ease-out (`cubic-bezier(0.16, 1, 0.3, 1)`). Never use `ease-in` on UI. Never animate from `scale(0)` (start at `scale(0.95)` with opacity). Popovers and dropdowns must be origin-aware (`transform-origin: var(--origin)`).
3. **Atmospheric Layered Elevation**: True dark mode uses tiered elevation tokens (`--canvas: #08090e`, `--surface-1: #121520`, `--surface-2: #181c2b`, `--surface-3: #20263a`), razor-sharp 1px inner borders (`rgba(255,255,255,0.08)`), and subtle ambient radial lighting (opacity 0.08–0.15). Zero washed-out purple fills or low-opacity blurry glassmorphism that destroys contrast.
4. **Typographic scale tension**: Dramatic ratio (>=4:1) between large display type and precision monospace metadata tags; never uniform bland sans-serif blobs.
5. **5-state interactive completeness**: Every control must implement default, hover, active (`scale(0.97)`), `:focus-visible` (2px solid, 2px offset, >=3:1 contrast), and disabled/loading/confirmation states.
6. **Physical tactile feedback**: Instant 80–120ms micro-interactions on compositor-only properties (`transform`, `opacity`), zero `transition: all`, and synthesized Web Audio mechanical acoustics where appropriate.
7. **Authentic domain density**: Populate interfaces with real, high-fidelity operational data, domain terminology, and state badges — never generic "Lorem ipsum", "Title here", or empty card shells.
8. **Architectural anti-slop discipline**: Strict 8pt spatial grid, verified WCAG 2.2 AA contrast (>=4.5:1 text, >=3:1 controls), and zero commodity AI slop.


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
