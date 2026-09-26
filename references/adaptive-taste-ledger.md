# Adaptive Taste Ledger & Persistent Aesthetic Profiles

How Turtleneck agents record user feedback, accumulate aesthetic rejections, and evolve design taste over time across sessions.

---

## 1. The Core Insight: Taste as Accumulated Rejection

LLMs are stateless by default; they reset every conversation and fall back on web-median templates unless constrained. Human designers do not develop taste by memorizing universal checklists—they develop taste by accumulating **rejections**:
* *"I never use saturated purple gradients."*
* *"I hate centered three-card feature grids."*
* *"I dislike dusty serif manifestos on cream paper."*
* *"I prefer high-contrast ink on crisp off-white with asymmetric tension."*

The Adaptive Taste Ledger makes these personal rejections persistent across agent conversations.

---

## 2. Storage Locations & Resolution Hierarchy

1. **Project Profile (Highest Precedence)**:
   `.turtleneck/taste-profile.json` in the project root. Defines the project's bespoke visual identity, rejected tropes, and token overrides.
2. **Global User Profile (Fallback)**:
   `~/.turtleneck/taste-profile.json` in user home directory. Defines the developer's personal defaults across all projects.

When resolving, project-level rules override and merge with global user defaults.

---

## 3. Taste Profile Schema

```json
{
  "version": "1.0.0",
  "updated_at": "2026-09-26T12:00:00Z",
  "preferred_vernacular": [
    "modern_high_precision_editorial",
    "asymmetric_layout",
    "generous_whitespace"
  ],
  "rejected_tropes": [
    "purple_neon_blur",
    "centered_3_cards",
    "dusty_retro_serif",
    "fake_diagnostics_telemetry"
  ],
  "typography": {
    "headline_family": "Plus Jakarta Sans",
    "mono_family": "JetBrains Mono",
    "tracking": "-0.03em"
  },
  "contrast_floor": 7.0,
  "notes": [
    "2026-09-26: User disliked centered template symmetry; prefers high-contrast crisp off-white canvas."
  ]
}
```

---

## 4. How Agents Interact With the Ledger

### On Phase 1 (Workspace Analysis)
1. Read `.turtleneck/taste-profile.json` or run `python scripts/taste.py json`.
2. Treat `rejected_tropes` as absolute negative constraints—never generate an element listed in rejections.
3. Align typography, canvas tone, and density with `preferred_vernacular` and `typography` settings.

### On User Critique (Post-Review Learning)
When the user provides aesthetic feedback (e.g. *"this looks like a generic template"* or *"hate this font"*):
1. Translate feedback into a concrete trope or preference.
2. Run `python scripts/taste.py reject "<trope>"` or `python scripts/taste.py note "<critique>"`.
3. Re-generate the surface adhering to the newly updated profile.
