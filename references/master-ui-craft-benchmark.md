# Master Technical Benchmark: Modern UI Craft & Interaction

The definitive engineering reference for modern interface craft, micro-interactions, typography, color architecture, and accessibility standards.

---

## 1. Motion Craft & Micro-Interaction Timing

### Perceptual Timing Limits
* **Instantaneous state feedback (press/check/toggle)**: `80ms – 120ms`.
* **Small floating surface enter (dropdown/tooltip)**: `120ms – 160ms`.
* **Structural surface enter (dialog/sheet/modal)**: `200ms – 240ms`.
* **Full view transition**: `300ms – 360ms`.
* **The Asymmetric Exit Rule**: Dismissals and exits must be **30%–50% faster** than entrances (`100ms – 140ms`). The user has finished their intent; the UI must clear the path immediately.

### Timing Curves & Spring Parameters
* **Expo Out (Starlight Console Enter)**: `cubic-bezier(0.16, 1, 0.3, 1)` — Instant velocity, long smooth deceleration, zero bounce.
* **Sharp Exit / Dismiss**: `cubic-bezier(0.4, 0, 1, 1)`
* **Spring Damping Ratio**: `zeta = c / (2 * sqrt(k * m))`, held in `[0.85, 1.0]`. Never underdamped (`zeta < 0.7`) in utility UI.
  * *Micro-toggles*: `{ stiffness: 450, damping: 32, mass: 0.8 }` (settles in ~140ms, 0 overshoot).
  * *Modals/Dialogs*: `{ stiffness: 320, damping: 28, mass: 1 }` (settles in ~220ms).

### GPU Compositing & Reduced Motion
* Mutate only `transform` and `opacity`.
* Apply `will-change: transform` only on active hover/press states; remove on idle to avoid VRAM leaks.
* Always provide `@media (prefers-reduced-motion: reduce)` fallbacks with zero displacement.

---

## 2. Typography Craft & Precision

### Mathematical Tracking Formula (Negative Letter-Spacing)
```
Letter-Spacing (em) = -0.022 * log10( Font Size (px) / 16 )
```

* **Display Hero (`48px – 64px+`)**: `-0.035em` to `-0.025em`
* **Headings (`24px – 36px`)**: `-0.02em` to `-0.015em`
* **Body UI (`14px – 16px`)**: `0em`
* **All-Caps Micro Labels (`10px – 12px`)**: `+0.05em` to `+0.08em` (`uppercase`)

### Tabular Numbers & Line-Heights
* Headings line-height: `1.05 – 1.15`
* Body line-height: `1.45 – 1.55`
* Data tables and timers must use tabular monospaced figures:
  ```css
  font-variant-numeric: tabular-nums slashed-zero;
  font-feature-settings: "tnum" 1, "zero" 1;
  ```
* Balanced text wrap: `text-wrap: balance` on all headings; `text-wrap: pretty` on paragraphs.

---

## 3. Color Architecture & Elevated Lighting

### OKLCH Perceptual Uniformity
Use OKLCH for predictable lightness across all hues:
```css
:root {
  --color-canvas: oklch(0.99 0.002 260);
  --color-surface: oklch(1.0 0 0);
  --color-text-primary: oklch(0.18 0.01 260);
}
.dark {
  /* Blue-slate undertone; never flat pure gray */
  --color-canvas: oklch(0.13 0.015 258);
  --color-surface: oklch(0.16 0.018 258);
  --color-surface-elevated: oklch(0.20 0.02 258);
  --color-border: oklch(0.24 0.018 258);
  --color-text-primary: oklch(0.96 0.005 260);
}
```

### Elevated Dark Mode: Specular Highlights & Layered Alphas
In dark mode, convey elevation via fill lightness steps and top-edge specular highlights:
```css
.dark .craft-card {
  background-color: rgba(255, 255, 255, 0.035);
  border: 1px solid rgba(255, 255, 255, 0.08);
  /* Directional top-down ambient highlight */
  box-shadow: 
    inset 0 1px 0 0 rgba(255, 255, 255, 0.12),
    0 4px 12px -2px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(16px);
}
```

---

## 4. Spatial Rhythm & Concentric Geometry

### 4pt / 8pt Spatial Scale
* Primary unit: `4px`.
* Scale: `4px` (micro/icon-gap), `8px` (component internal), `12px` (input padding y/x), `16px` (container internal), `24px` (card gap), `32px` (section separation), `48px` (layout block), `64px+` (page margin).

### Concentric Corner Radius Rule
To prevent distorted nested margins, inner and outer radiuses must share concentric center points:
```
R_outer = R_inner + Padding
```
*(e.g., if inner badge radius is `8px` and card padding is `12px`, card radius must be `20px`).*

### Fluid Clamp Formula
```css
/* Fluid body: 14px at 375px viewport -> 16px at 1280px viewport */
--text-fluid-body: clamp(0.875rem, 0.823rem + 0.221vw, 1rem);
```

---

## 5. Complete 5-State Component Architecture

Every interactive element must define 5 states:
1. **Default**: Clear visual affordance.
2. **Hover** (pointer-fine only): Subtle `translateY(-1px)` and background elevation.
3. **Active / Pressed**: Snappy `scale(0.98)` with `60ms` duration.
4. **Focus-Visible** (keyboard only): `2px solid` outline with `2px offset`, minimum 3:1 contrast.
5. **Disabled**: `opacity: 0.48`, `cursor: not-allowed`, `pointer-events: none`.

### Touch Ergonomics
* Minimum tap boundary: **44px × 44px** (Fluid Organics System) / **48px × 48px** (Material System).
* Compact icons must use `::after` pseudo-elements to expand touch bounds to 44px.

---

## 6. WCAG 2.2 AA Accessibility Standards

* **Contrast**: Minimum `4.5:1` for normal text, `3:1` for large text and UI boundaries.
* **Focus Visibility (SC 2.4.11/13)**: 2px thickness visible focus rings with guaranteed 3:1 contrast against both element and canvas.
* **Zero Keyboard Traps (SC 2.1.2)**: Modals must trap focus inside and release focus back to trigger on `Escape`.
* **Sticky Header Safety (SC 2.4.11)**: Use `scroll-margin-top: 80px` on focusable elements to prevent fixed navigation from obscuring active fields.
