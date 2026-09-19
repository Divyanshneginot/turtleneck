# Design Research & Pattern Extraction Playbook

Runbook for conducting automated design research and synthesizing interface DNA.

---

## 1. Category Benchmark Map

| Category | Benchmark References | Key Visual Signatures |
| :--- | :--- | :--- |
| **Developer Tools & Infrastructure** | Linear, Raycast, Vercel, Supabase | High information density, dark-first mode, monochromatic canvas with subtle borders (`1px solid rgba(255,255,255,0.08)`), keyboard-first command bars (`Cmd+K`), tight typography (`letter-spacing: -0.02em`). |
| **Fintech & Enterprise Payments** | Stripe, Ramp, Mercury | Crisp typographic contrast, generous white space, subtle multi-stop mesh gradients, refined card elevations, high-trust neutral slate palettes. |
| **Productivity & Workspace** | Notion, Cron/Notion Calendar, Craft | Warm paper neutrals (`#FBFBFA`), fluid inline editing, minimal chrome, subtle divider rules, drag-and-drop affordances. |
| **Data & AI Analytics** | Perplexity, Scale AI, HuggingFace | Split-pane viewports, streaming skeleton feedback, prominent prompt inputs, token counter chips, high contrast data tables. |

---

## 2. Research Queries Formulation

When researching a niche, generate targeted search queries:
1. `"<target-niche> UI patterns teardown modern web"`
2. `"<benchmark-brand> design system typography color tokens"`
3. `"<target-niche> best-in-class UX dashboard components"`

---

## 3. Design DNA Manifest Template

Save learned findings into this structured schema before writing UI code:

```markdown
### Design Manifest: [Target Application]
* **Benchmark Source**: [e.g. Linear + Raycast hybrid]
* **Color Palette**:
  - Canvas: `#08090A`
  - Surface: `#121417`
  - Border: `rgba(255, 255, 255, 0.08)`
  - Accent: `#5E6AD2` (Electric Indigo)
  - Text Primary: `#EDEDED`
  - Text Muted: `#8A8F98`
* **Geometry**:
  - Corner Radius: `6px` (surgical/compact)
  - Layout Density: Compact (`36px` table row height, `32px` button height)
* **Signature Elements**:
  - Keybinding indicators (`KBD` chips)
  - Status indicator pips (pulsing glowing dots)
  - Radial gradient backdrop glow
```
