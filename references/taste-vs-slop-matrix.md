# Taste vs. Slop: Modern UI Execution Matrix & Quality Gate

Distinguishes high-craft modern design from low-effort AI slop. Modern trends are permitted and encouraged, but only within strict execution thresholds.

---

## 1. Execution Rubric: Tasteful Craft vs. Forbidden Slop

| Modern Trend | Done Right (Tasteful Craft) | Slop (Forbidden — Immediate Rejection) |
| :--- | :--- | :--- |
| **Glassmorphism (Frosted Glass)** | **Strictly for floating chrome** (sticky navs, modal overlays, dropdowns).<br>• High fill opacity: `80% - 92%` tint (`rgba(16, 18, 22, 0.85)` or `rgba(255, 255, 255, 0.88)`).<br>• Blur: `12px - 20px`.<br>• Border: Razor-thin `1px solid rgba(255, 255, 255, 0.08)`.<br>• Contrast: Guaranteed >= 4.5:1 text contrast. | Low opacity (10% - 30%) cards placed over chaotic backgrounds where text becomes unreadable.<br>• Multiple nested glass layers.<br>• Heavy tinted neon borders. |
| **Gradients & Lighting** | **Subtle rim light or single focal accent**.<br>• Micro-mesh or top-edge highlight (`linear-gradient(to bottom, rgba(255,255,255,0.06), transparent)`).<br>• Directional light guiding attention to primary action. | Huge saturated purple/cyan/magenta radial nebula blobs floating haphazardly across the background. |
| **Layout & Rhythm** | **Asymmetric tension & single dominant centerpiece**.<br>• Generous negative space (60%+ breathing room).<br>• One unforgettable interactive instrument users can test with their hands. | **Safe Template Slop**: Centered hero + 3-box feature grid + generic card container with zero point of view.<br>• Symmetrical Bootstrap/Tailwind clichés. |
| **Light-Mode & Editorial** | **Modern High-Precision Editorial**.<br>• Crisp off-white canvas (`#fafafa` / `#f8fafc`).<br>• Deep slate ink text (`#0f172a`, >= 14:1 contrast).<br>• Sharp 1px hairline borders (`#e2e8f0`).<br>• Tight tracking (`-0.03em`), snappy 80ms interactions. | **Dusty Museum Slop**: Faded yellowed paper, tiny unreadable serif manifestos, academic exhibition tags (`01 // THE MANIFESTO`), static non-interactive print brochure layouts. |
| **Borders & Separation** | Hairline `1px` subtle borders using alpha channels (`rgba(255,255,255,0.08)` for dark, `rgba(0,0,0,0.08)` for light). | Thick, high-contrast, multi-colored neon gradient borders around every card. |
| **Motion & Transitions** | Snappy, tactile micro-transitions under `150ms` (`cubic-bezier(0.16, 1, 0.3, 1)`). Respects `prefers-reduced-motion`. | 800ms sluggish spring animations, scroll-hijacking, 5MB Three.js canvas lag, or cards that tilt drastically on mouse movement. |
| **Copy & Point of View** | **Biting, memorable Aesthetic Thesis**.<br>• Directly rejects a dominant industry cliché (e.g. *"Good design is not purple"*).<br>• Operational, domain-authentic microcopy. | Hollow buzzword filler: *"Unleash autonomous neural synergy"*, *"10x your cognitive velocity"*, or *"Next-gen AI magic"*. |
| **Interaction Ergonomics** | **Sub-50ms tactile feedback**: Full keyboard navigability (`Tab`, `Esc`, `Cmd+K`, hotkeys), 2px focus rings with 3:1 contrast. | Mouse-only traps, missing focus outlines, raw unstyled browser `alert()` popups. |

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

## 3. The 6 Quality Gate Checks Before Approval

1. **The Readability Test**: Can every line of text be read effortlessly against whatever background sits behind it? If blurred content obscures text, raise the surface opacity to 90%+ (solid slate).
2. **The Utility Test**: Does every bento cell, badge, and card provide operational information or actions? If purely decorative, cut it.
3. **The Restraint Test**: Is lighting used to emphasize a single focal point, or is the screen competing with itself via multi-color neon glows?
4. **The Ergonomics Test**: Can every primary flow be completed via keyboard with active focus indication and zero jarring layout shifts?
5. **The Vernacular Harmony Test**: Does the entire surface adhere strictly to ONE design dialect (one archetype)? Are all card radiuses, border tokens, and font families speaking the exact same visual language without aesthetic collage?
6. **The Frequency Gating Test**: Are high-frequency tools (command palettes, shortcuts, list toggles) free of laggy animations (0ms execution)? Do button micro-interactions settle in 80–120ms with custom ease-out curves?

