---
name: ui-ux-design
description: >-
  Expert UI/UX design workflow for web and mobile interfaces. Use when designing
  layouts, wireframes, component systems, color palettes, typography hierarchies,
  responsive interfaces, micro-interactions, or conducting accessibility (WCAG) and UX audits.
---

# UI/UX Design Protocol

Systematic, production-grade interface design workflow. Adhere to progressive disclosure and token efficiency.

## Core Execution Flow

```
1. Layout & Hierarchy ──► 2. Design Tokens ──► 3. Component States ──► 4. Responsiveness ──► 5. Usability & WCAG
```

---

### Step 1: Information Architecture & Layout Grid
* Establish primary, secondary, tertiary visual focal points before writing markup.
* Base all spatial layout on an **8pt grid** (use 4pt for micro-spacing and icons).
* Define container max-widths:
  * Compact / Mobile: `360px` - `480px`
  * Tablet: `768px` - `1024px`
  * Desktop content wells: `1200px` - `1440px` (avoid edge-to-edge text lines; cap line length at 65-75 characters).

---

### Step 2: Design Tokens & Visual Hierarchy
* Refer to [Design Tokens Reference](./references/design-tokens.md) for full scales.
* Apply **60-30-10 Color Rule**:
  * `60%`: Base / Background / Neutral surfaces.
  * `30%`: Structural content, typography, borders, card backgrounds.
  * `10%`: Primary interactive accent (actions, active links, highlights).
* Maintain strict contrast ratios (WCAG 2.2):
  * Body text: min `4.5:1` against background.
  * Large headings / icons / UI borders: min `3:1`.

---

### Step 3: Component State Completeness
Never produce static, single-state components. Every interactive element must define 5 core states:
1. **Default**: Clear affordance and identifiable hit area.
2. **Hover**: Visual elevation change, color shift, or subtle border transition (desktop only).
3. **Active / Pressed**: Subtle scale down (e.g. `scale(0.98)`) or darkened shade.
4. **Focus-visible**: High-contrast outline (`2px solid`, `2px offset`) for keyboard navigation.
5. **Disabled**: Reduced opacity (`40-50%`), `not-allowed` cursor, removed pointer events, `aria-disabled="true"`.

Touch target rule: Interactive elements must measure minimum **44x44 CSS pixels** on touch-capable viewports.

---

### Step 4: Responsive & Touch Ergonomics
* Prioritize content flow using mobile-first layout:
  * Phone: Single-column stack, thumbs-reachable bottom actions/navigation.
  * Tablet: 2-column adaptive grids.
  * Desktop: Multi-column dashboards, persistent navigation rails.
* Never use fixed heights on content containers—use min-height and fluid flex/grid.

---

### Step 5: Usability & Accessibility Verification
* Audit layout against [UX Heuristics](./references/ux-heuristics.md):
  * Provide feedback within 100ms for user interactions.
  * Clear error prevention and destructive action confirmations.
* Verify compliance against [Accessibility Checklist](./references/accessibility-checklist.md):
  * Semantic HTML tags (`<nav>`, `<main>`, `<article>`, `<button>`, `<dialog>`).
  * Explicit ARIA labels where visual labels are omitted (e.g., icon-only buttons).
  * Logical tab order and keyboard trap prevention.
