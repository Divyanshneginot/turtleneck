---
name: turtleneck
description: >-
  Autonomous Senior UI/UX Architect agent skill. Use when asked to design, build, or modernize
  interfaces. Autonomously analyzes the current workspace stack (Tailwind, React, Vue,
  CSS tokens, component trees), conducts interactive requirement interviews with the user,
  aligns on layout architecture, and implements production-grade anti-slop UI.
---

# Autonomous UI/UX Architect Protocol

Transforms user UI requests into bespoke, production-ready interfaces by first scanning the local workspace, conducting a structured requirement interview with the user, aligning on architecture, and implementing anti-slop code.

---

## 4-Phase Operational Pipeline

```
1. Workspace Analysis ──► 2. Requirements Interview ──► 3. Blueprint Alignment ──► 4. Production Build
```

---

### Phase 1: Workspace Analysis & Research Review
Before asking questions or drafting UI, inspect the repository and live benchmarks:

1. **Stack & Tooling Detection (Refer to [Framework Integrations](./references/framework-integrations.md))**:
   * Inspect package files (`package.json`, `requirements.txt`, etc.).
   * Identify frontend framework (React, Next.js, Vue, Svelte, HTML/CSS).
   * Identify styling engine (Tailwind CSS, Vanilla CSS, Radix UI, CSS Modules).
   * Match code generation directly to discovered framework idioms.
2. **Review Existing Headless Research & Feel**:
   * Do NOT run scrapers. Analyze existing headless captures in `references/deep_research/` and `references/award_research/`.
   * Feel the soul of the benchmarks—narrative pacing, visual weight, spatial breathing, and micro-tactility—not just hex codes.
   * Enforce the **Creative Synthesis Protocol** (Refer to [Award-Winning Craft Playbook](./references/award-winning-craft-playbook.md) and [Creative Synthesis Protocol](./references/creative-synthesis-protocol.md)):
     * Blend atmosphere, interaction physics, typography tension, and layout density from 4+ different sources into something new. Never lean on one reference.
     * Forbid 1:1 cloning of metaphors, copy, diff blocks, terminal cursors, or recognizable brand gimmicks. Extract the WHY, invent a new HOW.

---

### Phase 2: Interactive Requirements & Archetype Selection
Engage the user to clarify intent, archetype, and layout before writing code:

1. **Visual Archetype Selection (Refer to [Design Archetypes Catalog](./references/design-archetypes.md))**:
   * Do NOT assume dark mode or developer aesthetic. Confirm the product archetype:
     * **A. High-Trust Corporate**: Clean high-trust light mode (`#f6f9fc`), crisp slate borders, fintech/SaaS clarity.
     * **B. Warm Editorial Paper**: Warm paper canvas (`#fbfbfa`), serif headlines, minimal chrome, distraction-free docs.
     * **C. Fluid Organics**: Fluid system UI, tactile segmented controls, soft squircle radiuses (`10-14px`).
     * **D. High-Density Starlight**: Dark starlight engineering (`#08090a`), high data density, keyboard hotkeys.
     * **E. Stark Geometric Minimal**: Stark black/white minimalism, zero ornamentation, monospaced metadata.
2. **Core Job-To-Be-Done & Target Density**:
   * Identify primary outcome (monitoring, triage, editing, onboarding).
   * Confirm density: High-density operational vs balanced SaaS vs consumer guided flow.
3. **Present 2-3 Concrete Architecture Options**:
   * Refer to [Requirements Interview Framework](./references/requirements-interview-framework.md) to pitch layout options.

---

### Phase 3: Blueprint & Token Alignment
Once user approves layout choice:
1. Formulate exact data schema for UI components (mock realistic, domain-accurate data).
2. Lock in design tokens (colors, typography, spacing) compatible with the scanned workspace.
3. **Validate Against Taste vs. Slop Matrix**:
   * Refer to [Taste vs. Slop Matrix](./references/taste-vs-slop-matrix.md).
   * **Modern patterns encouraged when done right**:
     * Glassmorphism: strictly for floating chrome, high fill opacity (`80-90%`), hairline border, text contrast $\ge 4.5:1$.
     * Bento layouts: high data density, real functional widgets, zero decorative 3D balls.
     * Gradients: subtle single-source rim lighting guiding attention to primary actions.
   * **Slop strictly rejected**: illegible $10\%$ glass opacity, giant saturated nebula blobs, 800ms sluggish animations, buzzword copy.

---

### Phase 4: Production Implementation & Master Craft Verification
1. **Component Engineering (Refer to [Master Craft Benchmark](./references/master-ui-craft-benchmark.md) & [Framework Integrations](./references/framework-integrations.md))**:
   * Emit idiomatic code matching detected stack: React (TSX/hooks), Vue (`<script setup>`), Svelte 5 (runes), or Native Platform (zero-dependency HTML/CSS/JS).
   * Generate modular, clean components following discovered repo conventions.
   * **Motion & Timing**: `80-120ms` state feedback, `200-240ms` enter, `100-140ms` exit (asymmetric exit rule), `cubic-bezier(0.16, 1, 0.3, 1)` or critical springs ($\zeta \ge 0.85$). GPU compositor thread isolation (`transform`/`opacity` only).
   * **Typography Precision**: Negative tracking on headings, `font-variant-numeric: tabular-nums` for data cells, `text-wrap: balance` on headlines.
   * **Concentric Radiuses**: $R_{\text{outer}} = R_{\text{inner}} + \text{Padding}$.
   * **5-State Completeness**: (`default`, `hover`, `active` scale 0.98, `focus-visible` 2px ring, `disabled`).
   * **Touch Ergonomics**: Minimum `44x44px` physical tap targets.
2. **Accessibility Audit (WCAG 2.2 AA)**:
   * 4.5:1 text contrast, 3:1 UI boundaries.
   * Focus rings with 3:1 contrast against element and background canvas.
   * Trap-free modal keyboard navigation with `Escape` dismiss and trigger focus restoration.
3. **Walkthrough & Verification**:
   * Verify zero console errors and zero layout shifts.
   * Present summary of files changed and architectural decisions to user.
