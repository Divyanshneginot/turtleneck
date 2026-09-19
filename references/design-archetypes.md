# Universal Design Archetypes Catalog

Token specifications and layout guidelines for major design paradigms beyond dark developer tools.

---

## 1. The 5 Core Visual Archetypes

```
1. Stripe Enterprise (Light) ──► 2. Notion Workspace (Paper) ──► 3. Apple HIG (Fluid) ──► 4. Linear (Dark) ──► 5. Vercel (Monochrome)
```

---

### Archetype 1: Stripe Enterprise (Clean High-Trust Light)
* **Best for**: Fintech, billing, B2B SaaS, enterprise dashboards, checkout flows.
* **Canvas**: `#f6f9fc` (soft cool neutral, never blinding #fff).
* **Card Surface**: `#ffffff` with subtle 1px border `#e3e8ee` and soft diffuse shadow `0 2px 4px rgba(0,0,0,0.04)`.
* **Primary Accent**: `#635bff` (Stripe Blurple), hover `#4f46e5`.
* **Typography**: Clean humanist/geometric sans (`Inter`, `Segoe UI`), high contrast `#0a2540` text, slate `#425466` secondary.
* **Radii**: `6px` controls, `8px` cards.
* **Vibe**: Authoritative, rock-solid, crystal-clear banking clarity.

---

### Archetype 2: Notion Editorial (Warm Paper Workspace)
* **Best for**: Knowledge bases, document tools, collaborative workspaces, creative apps.
* **Canvas**: `#fbfbfa` (warm cream paper tone, calming eye comfort).
* **Card Surface**: `#ffffff` with warm subtle divider `#e9e9e8`.
* **Primary Accent**: `#2383e2` (Soft Cerulean) or `#37352f` (Ink Black).
* **Typography**: Serif headlines (`Newsreader`, `Georgia`, `Domaine`) paired with warm humanist sans for UI.
* **Radii**: `4px` subtle corners, minimal chrome, generous line spacing (1.6).
* **Vibe**: Organic, thoughtful, distraction-free, print-editorial confidence.

---

### Archetype 3: Apple Human Interface (Fluid & Tactile)
* **Best for**: Mobile-first web apps, media apps, consumer utilities, macOS-style web tools.
* **Canvas**: `#f2f2f7` (light) / `#1c1c1e` (dark) with `#ffffff` / `#2c2c2e` cards.
* **Primary Accent**: `#007aff` (iOS System Blue).
* **Typography**: `system-ui`, `-apple-system`, `SF Pro Display`, `SF Pro Text`.
* **Radii**: Smooth squircles (`10px – 14px`), generous touch targets (`44px+`), tactile segmented controls.
* **Vibe**: Seamless, natural, highly physical, thumb-ergonomic.

---

### Archetype 4: Linear / Raycast (Starlight Engineering)
* **Best for**: Developer platforms, telemetry consoles, issue trackers, terminal companions.
* **Canvas**: `#08090a` pitch dark, `#0e1013` surfaces.
* **Primary Accent**: `#5e6ad2` (Electric Indigo).
* **Typography**: `Inter Variable` with negative tracking, monospaced tabular numbers.
* **Radii**: Tight `6px` controls, `8px` windows.
* **Vibe**: Dense, laser-focused, sub-100ms keyboard-first speed.

---

### Archetype 5: Vercel / Monochrome (Stark Geometric Minimal)
* **Best for**: Cloud infrastructure, AI developer tools, CLI frontends, headless engines.
* **Canvas**: `#000000` (dark) or `#ffffff` (light). Zero color except status indicators.
* **Borders**: Sharp 1px `#222222` dividers.
* **Typography**: `Geist Sans` and `Geist Mono`, ultra-tight tracking, all-caps micro metadata.
* **Radii**: Razor-sharp `4px` or `2px`.
* **Vibe**: Hyper-modern, minimal, architectural, zero ornamentation.
