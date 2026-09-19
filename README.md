# UI/UX Design Skill (`ui-ux-design`)

A production-grade, progressive-disclosure agent skill for automated UI/UX design, design token systems, component state modeling, and WCAG 2.2 accessibility compliance.

Built for **Google Antigravity**, Claude Code, and compatible AI agent frameworks.

---

## Features

* **Progressive Disclosure**: Lean `SKILL.md` footprint with specialized on-demand reference guides to minimize LLM token overhead.
* **Systematic Design Tokens**: 8pt/4pt spatial grids, modular typographic scales (Major Third / 1.25), and semantic color mapping.
* **Component State Completeness**: Standardized 5-state model (Default, Hover, Active, Focus-Visible, Disabled) with 44px touch targets.
* **Usability Heuristics**: Direct mapping of Nielsen's 10 Heuristics to interface generation.
* **WCAG 2.2 AA Compliance**: Automated checklist for color contrast, keyboard navigation, focus indicators, and screen reader semantics.

---

## Repository Layout

```text
ui-ux-design/
├── SKILL.md                          # Main agent instructions & execution protocol
├── README.md                         # Documentation & installation guide
└── references/
    ├── design-tokens.md              # Spatial grids, typographic scales, semantic color roles
    ├── ux-heuristics.md              # Usability guidelines, response latencies, error prevention
    └── accessibility-checklist.md    # WCAG 2.2 AA audit criteria, keyboard traps, ARIA rules
```

---

## Installation

### Option 1: Global Installation (All Workspaces)
Clone or copy this folder into your global Antigravity config directory:

**Windows (PowerShell)**:
```powershell
Copy-Item -Recurse -Path .\ui-ux-design -Destination "$HOME\.gemini\config\skills\ui-ux-design"
```

**macOS / Linux**:
```bash
cp -r ./ui-ux-design ~/.gemini/config/skills/ui-ux-design
```

### Option 2: Project-Specific Installation (Current Repository)
Add the skill to your project's `.agents/skills` directory and check it into git:

```bash
mkdir -p .agents/skills
cp -r ./ui-ux-design .agents/skills/ui-ux-design
git add .agents/skills/ui-ux-design
git commit -m "feat: add ui-ux-design agent skill"
```

---

## How It Activates

The agent automatically triggers this skill whenever prompts match UI/UX design intents, such as:
* *"Design a responsive dashboard layout for..."*
* *"Create an accessible color palette and design tokens for..."*
* *"Build a button component with full state coverage..."*
* *"Audit this interface for WCAG accessibility and usability issues..."*

---

## License

MIT
