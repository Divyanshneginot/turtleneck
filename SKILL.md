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

### Phase 1: Workspace Analysis & Stack Profiling
Before asking questions or drafting UI, inspect the repository:

1. **Stack & Tooling Detection**:
   * Inspect package files (`package.json`, `requirements.txt`, `composer.json`, etc.).
   * Identify frontend framework (React, Next.js, Vue, Svelte, HTML/CSS).
   * Identify styling engine (Tailwind CSS, Vanilla CSS, CSS Modules, Radix UI, Shadcn, PandaCSS).
   * Identify icon libraries in use (Lucide, Heroicons, Radix Icons, FontAwesome).
2. **Component Tree & Token Discovery**:
   * Check existing component patterns (`src/components/`, `components/ui/`, `lib/`).
   * Read existing design tokens (`tailwind.config.*`, `globals.css`, theme files).
   * Map existing layout routes (`app/`, `pages/`, `views/`).
3. **Synthesize Workspace Profile**:
   * Summarize detected stack, theme conventions, and reuse opportunities.
   * Refer to [Workspace Scanner Guide](./references/workspace-scanner-guide.md).

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

### Phase 4: Production Implementation & Verification
1. **Component Engineering**:
   * Generate modular, clean components following discovered repo conventions.
   * Support 5 component states (`default`, `hover`, `active`, `focus-visible`, `disabled`).
   * Ensure min `44x44px` touch targets on interactive elements.
2. **Accessibility Audit**:
   * Verify WCAG 2.2 AA contrast (4.5:1 text, 3:1 UI).
   * Semantic landmarks (`<nav>`, `<main>`, `<section>`), visible 2px focus outlines, keyboard escape handling.
3. **Walkthrough & Verification**:
   * Verify component renders cleanly in browser.
   * Present summary of files changed and architectural decisions to user.
