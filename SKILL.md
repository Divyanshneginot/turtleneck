---
name: ui-ux-design
description: >-
  Agentic UI/UX design engine. Use when tasked with designing or building interfaces
  requiring real-world benchmark research, extracting design systems from modern apps
  (e.g., Linear, Stripe, Vercel, Raycast), synthesizing visual DNA, and generating production UI.
---

# Agentic UI/UX Research & Implementation Engine

Transforms raw interface requests into bespoke, research-backed products by autonomously benchmarking top-tier references, extracting visual DNA, and generating production code.

---

## 3-Phase Execution Pipeline

```
Phase 1: Deep Design Research ──► Phase 2: Design DNA Synthesis ──► Phase 3: High-Fidelity Implementation
```

---

### Phase 1: Autonomous Design Research
Do NOT guess or use generic templates. Research best-in-class products in the target category:

1. **Benchmark Identification**:
   * Identify 2-3 category leaders (e.g., Developer Tools -> *Linear / Raycast*; Fintech -> *Stripe / Ramp*; Consumer -> *Airbnb / Notion*).
   * Search web for design breakdowns, teardowns, and UI patterns for target niche.
2. **Structural Extraction**:
   * **Information Architecture**: Layout density, navigation model (sidebar vs command bar vs top tabs).
   * **Visual Tone**: Atmospheric backdrop, border sharpness, shadow depth, glassmorphism vs brutalism.
   * **Signature Components**: Hero treatments, data tables, metrics cards, filter widgets.

---

### Phase 2: Learn & Synthesize Design DNA
Distill research into a concrete, reproducible Design Manifest:

1. **Palette Extraction**:
   * Canvas background (deep dark `#08090A` or warm neutral `#FAFAF9`).
   * Surface tiers (base, raised, overlay).
   * Accent color (high-chroma signature action color).
   * Contrast ratios validated against WCAG AA.
2. **Typography DNA**:
   * Font stack (geometric sans, clean humanist, or technical mono).
   * Density and tracking rules (tight tracking `-0.02em` on bold display headings).
3. **Component DNA**:
   * Corner radiuses (`4px` surgical vs `12px` modern soft).
   * Border stroke treatments (`1px solid rgba(255,255,255,0.08)` for dark themes).
   * Micro-interaction cues (hover state latency, spring transforms).

---

### Phase 3: Generative Implementation
Produce production frontend code matching the learned Design Manifest:

1. **Semantic Foundation**: Clean HTML5 semantic tags with ARIA accessibility primitives.
2. **CSS Token Embed**: Declare extracted tokens as CSS custom variables at `:root`.
3. **Interactive Fidelity**:
   * 5 component states (`default`, `hover`, `active`, `focus-visible`, `disabled`).
   * Fluid responsive breakpoints (mobile drawer to desktop grid).
   * Micro-interactions (smooth transitions under `150ms`, keyboard shortcuts).
4. **Anti-Slop Quality Gate (Mandatory)**:
   * Reject purple/cyan nebula blur blobs, fake glassmorphism, and buzzword copy ("quantum synergy").
   * Audit against [Anti-Slop Manifesto](./references/anti-slop-manifesto.md): enforce high information density, sub-50ms responsiveness, real operational microcopy, and keyboard ergonomics.
   * Verify WCAG AA contrast and keyboard trap prevention.
