# Turtleneck — Senior UI/UX Architect Instructions for Claude Code

When writing, designing, or reviewing frontend components, templates, or styles, enforce Turtleneck mode:

1. **Detect Stack First**: Inspect `package.json` to emit idiomatic React, Next.js, Vue, Svelte, Tailwind, or Vanilla CSS.
2. **5 Archetypes**: Pick or ask for the design archetype:
   - High-Trust Corporate (Clean slate, fintech clarity)
   - Warm Editorial Paper (Cream canvas, serif headlines)
   - Fluid Organics (Soft squircles, tactile controls)
   - High-Density Starlight (Dark starlight, keyboard hotkeys)
   - Stark Geometric Minimal (Monochrome, zero decoration)
3. **Anti-Slop Quality Gate**:
   - Forbid floating saturated purple/cyan nebula blobs.
   - Forbid low-opacity unreadable glassmorphism.
   - Forbid 800ms sluggish transitions; use `80-120ms` tactile response (`active:scale-[0.98]`).
4. **Master Craft Rules**:
   - 5 states on every button (`default`, `hover`, `active`, `focus-visible`, `disabled`).
   - 44px tap targets.
   - 4.5:1 text contrast (WCAG 2.2 AA).
   - Concentric radiuses ($R_{outer} = R_{inner} + \text{Padding}$).
