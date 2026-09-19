# Taste vs. Slop: Modern UI Execution Matrix

Distinguishes high-craft modern design from low-effort AI slop. Modern trends are permitted and encouraged, but only within strict execution thresholds.

---

## 1. Execution Rubric: Tasteful vs. Slop

| Modern Trend | Done Right (Tasteful Craft) | Slop (Forbidden) |
| :--- | :--- | :--- |
| **Glassmorphism (Frosted Glass)** | **Strictly for floating chrome** (sticky navs, modal overlays, dropdowns).<br>• High fill opacity: `80% - 92%` tint (`rgba(16, 18, 22, 0.85)` or `rgba(255, 255, 255, 0.88)`).<br>• Blur: `12px - 20px`.<br>• Border: Razor-thin `1px solid rgba(255, 255, 255, 0.08)`.<br>• Contrast: Guaranteed $\ge 4.5:1$ text contrast. | Low opacity ($10\% - 30\%$) cards placed over chaotic backgrounds where text becomes unreadable.<br>• Multiple nested glass layers.<br>• Heavy tinted neon borders. |
| **Gradients & Lighting** | **Subtle rim light or single focal accent**.<br>• Micro-mesh or top-edge highlight (`linear-gradient(to bottom, rgba(255,255,255,0.06), transparent)`).<br>• Directional light guiding attention to primary action. | Huge saturated purple/cyan/magenta radial nebula blobs floating haphazardly across the background. |
| **Bento Grids** | **High information density**.<br>• Every cell houses a real functional tool, interactive metric, or structured data.<br>• Asymmetrical hierarchy reflecting actual content priority. | Ornamental boxes filled with decorative 3D spheres, spinning rings, or generic stock icons with no user utility. |
| **Borders & Separation** | Hairline `1px` subtle borders using alpha channels (`rgba(255,255,255,0.08)` for dark, `rgba(0,0,0,0.08)` for light). | Thick, high-contrast, multi-colored neon gradient borders around every card. |
| **Motion & Transitions** | Snappy, tactile micro-transitions under `150ms` (`cubic-bezier(0.16, 1, 0.3, 1)`). Respects `prefers-reduced-motion`. | 800ms sluggish spring animations, scroll-hijacking, or cards that tilt drastically on mouse movement. |

---

## 2. Tasteful Glassmorphism Recipe (CSS Standard)

When implementing frosted glass, use this calibrated baseline:

```css
/* Dark Mode Tasteful Glass */
.glass-surface-dark {
  background-color: rgba(13, 17, 23, 0.85); /* 85% opacity prevents bleed-through */
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.08); /* Hairline edge highlight */
  box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4);
}

/* Light Mode Tasteful Glass */
.glass-surface-light {
  background-color: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05);
}
```

---

## 3. The 3 Quality Gate Checks Before Approval

1. **The Readability Test**: Can every line of text be read effortlessly against whatever background sits behind it? If blurred content obscures text, raise the surface opacity to $90\%+$.
2. **The Utility Test**: Does every bento cell, badge, and card provide operational information or actions? If purely decorative, cut it.
3. **The Restraint Test**: Is lighting used to emphasize a single focal point, or is the screen competing with itself via multi-color neon glows?
