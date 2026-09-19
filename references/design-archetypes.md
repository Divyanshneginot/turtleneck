# Universal Design Archetypes Catalog

Token specifications and layout guidelines for major design paradigms.

---

## 1. The 5 Core Visual Archetypes

```
1. High-Trust Corporate (Light) ──► 2. Warm Editorial Paper ──► 3. Fluid Organics ──► 4. High-Density Starlight (Dark) ──► 5. Stark Geometric Minimal
```

---

### Archetype 1: High-Trust Corporate (Clean Light)
* **Best for**: Fintech, billing, B2B SaaS, enterprise dashboards, checkout flows.
* **Canvas**: `#f6f9fc` (soft cool neutral, never blinding #fff).
* **Surface**: `#ffffff`, elevated `#ffffff`, active `#edf2f7`.
* **Card Surface**: `#ffffff` with subtle 1px border `#e3e8ee` (decorative edge — exempt from WCAG 1.4.11, never the sole indicator of a boundary or state) and soft diffuse shadow `0 2px 4px rgba(0,0,0,0.04)`.
* **Primary Accent**: `#6259ff` (Vibrant Indigo, 4.52:1 as text on canvas; 4.78:1 for white text on fill), hover `#4f46e5`, focus ring `0 0 0 2px #6259ff`.
* **Typography**: Clean humanist/geometric sans (`Inter`, `Segoe UI`), high contrast `#0a2540` text, slate `#425466` secondary, `#627489` muted (4.54:1).
* **Radii**: `6px` controls, `8px` cards.
* **Vibe**: Authoritative, rock-solid, crystal-clear banking clarity.

---

### Archetype 2: Warm Editorial Paper (Commerce & Publishing)
* **Best for**: Knowledge bases, document tools, collaborative workspaces, creative commerce.
* **Canvas**: `#fbfbfa` (warm cream paper tone, calming eye comfort).
* **Surface**: `#ffffff`, elevated `#ffffff`, active `#efedea`.
* **Card Surface**: `#ffffff` with warm subtle divider `#e9e9e8` (decorative divider — exempt from WCAG 1.4.11) and hairline shadow `0 1px 3px rgba(15,15,15,0.05)`.
* **Primary Accent**: `#1b75cf` (Soft Cerulean, 4.51:1 as text on paper) or `#201f1d` (Ink Black), hover `#1b6ec2`.
* **Typography**: Serif headlines (`Newsreader`, `Georgia`, `Domaine`) paired with warm humanist sans for UI. Line-height: `1.6`.
* **Radii**: `4px` subtle corners, minimal chrome, generous line spacing.
* **Vibe**: Organic, thoughtful, distraction-free, print-editorial confidence.

---

### Archetype 3: Fluid Organics (Tactile System)
* **Best for**: Mobile-first web apps, media apps, consumer utilities, native-style web tools.
* **Canvas**: `#f2f2f7` (light) / `#1c1c1e` (dark).
* **Surface**: `#ffffff` (light) / `#2c2c2e` (dark), active `#e5e5ea` / `#3a3a3c`.
* **Primary Accent**: `#006be0` (System Blue on light surfaces — 5.02:1 for white text on fill, 4.50:1 as link/body text on `#f2f2f7`) / `#0d81ff` on the `#1c1c1e` dark canvas (4.54:1). Hover `#0056b3`.
  * The stock `#007aff` measured only 4.02:1 with white text and 3.60:1 as text on `#f2f2f7`; both were raised at identical hue.
* **Typography**: `system-ui`, `-apple-system`, sans-serif.
* **Radii**: Smooth squircles (`10px – 14px`), generous touch targets (`44px+`), tactile segmented controls.
* **Vibe**: Seamless, natural, highly physical, thumb-ergonomic.

---

### Archetype 4: High-Density Starlight (Engineering Dark)
* **Best for**: Developer platforms, telemetry consoles, issue trackers, terminal companions.
* **Canvas**: `#08090a` pitch dark, surface `#0e1013`, active `#16191f`.
* **Primary Accent**: `#636fd3` (Electric Indigo, 4.50:1 as text on `#08090a`), hover `#6f7bf7`.
* **Typography**: Sans-serif variable font with negative tracking (`-0.022em`), monospaced tabular numbers.
* **Radii**: Tight `6px` controls, `8px` windows.
* **Vibe**: Dense, laser-focused, sub-100ms keyboard-first speed.

---

### Archetype 5: Stark Geometric Minimal (Architectural Monochrome)
* **Best for**: Cloud infrastructure, AI developer tools, CLI frontends, headless engines.
* **Canvas**: `#000000` pitch black, surface `#0d0d0d`, active `#171717`.
* **Surface Elevated**: `#0a0a0a` with razor-sharp 1px border `#262626`.
* **Primary Accent**: `#ffffff` (Stark White), hover `#cccccc`, active `#aaaaaa`.
* **Status Accents**: Pure functional semaphores: `#10b981` (online), `#f59e0b` (degraded), `#ef4444` (down). Zero decorative color.
* **Borders**: Sharp 1px `#1a1a1a` subtle, `#262626` window, `#333333` active. All three are **structural/decorative** and sit below the 3:1 WCAG 1.4.11 threshold by design — the near-black-on-black chassis is the archetype. They MUST NOT be the sole indicator of an interactive component boundary, a focus ring, or a selected/active state. Where a boundary must be perceivable (inputs, toggles, focus), use `#ffffff` or a functional semaphore at >= 3:1, and always pair state with a text or icon cue.
* **Typography**: Monospace and Geometric Grotesk (`CommitMono`, `Geist`, `ui-monospace`), all-caps micro metadata (`9px - 11px`, `letter-spacing: 0.12em`).
* **Radii**: Razor-sharp `2px` or `0px` chassis edges.
* **Vibe**: Hyper-modern, minimal, architectural, zero ornamentation.
