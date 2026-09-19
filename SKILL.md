---
name: ui-ux-design
description: >-
  Autonomous UI/UX architect agent skill. Use when asked to design, build, or modernize
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

### Phase 1: Workspace Analysis & Live Browser Extraction
Before asking questions or drafting UI, inspect the repository and live benchmarks:

1. **Stack & Tooling Detection**:
   * Inspect package files (`package.json`, `requirements.txt`, etc.).
   * Identify frontend framework (React, Next.js, Vue, Svelte, HTML/CSS).
   * Identify styling engine (Tailwind CSS, Vanilla CSS, Radix UI, Shadcn).
2. **Live Browser Benchmark Extraction**:
   * When targeting a reference design or URL, run the built-in browser extractor:
     ```bash
     python scripts/extract_design.py <target-url> references/
     ```
   * Extracts exact computed styles: dominant backgrounds, text colors, font stacks, optical radii, and specular box-shadows directly into JSON.

---

### Phase 2: Interactive Requirements Interview
Engage the user to clarify intent and resolve design ambiguities before writing code. Follow [Requirements Interview Framework](./references/requirements-interview-framework.md):

1. **Core Problem & Target Audience**:
   * What is the primary Job-To-Be-Done (JTBD) on this view?
   * Who is the user (domain expert needing high density vs casual consumer needing guided flow)?
2. **Layout & Density Preference**:
   * Density level: High (data tables, compact controls) vs Moderate (cards, balanced spacing).
   * Navigation model: Sidebar navigation, top header tabs, or command-driven (`Cmd+K`).
3. **Present 2-3 Concrete Approaches**:
   * Pitch distinct layout archetypes (e.g., Option A: Split-pane master-detail vs Option B: Focused feed with slide-over drawer).
   * Solicit user preference or confirmation.

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
1. **Component Engineering (Refer to [Master Craft Benchmark](./references/master-ui-craft-benchmark.md))**:
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
