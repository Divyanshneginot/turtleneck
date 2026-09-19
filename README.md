# Autonomous UI/UX Architect Skill (`ui-ux-design`)

A production-grade, anti-slop agent skill that autonomously profiles your codebase, interviews you to clarify UI/UX requirements, aligns on wireframes, and implements accessible, high-performance interfaces.

Built for **Google Antigravity**, Claude Code, and compatible AI agent frameworks.

---

## 4-Phase Architecture

```
1. Workspace Scanner ──► 2. Requirements Interview ──► 3. Blueprint Alignment ──► 4. Anti-Slop Implementation
```

1. **Workspace Stack Profiling**: Detects your framework (React, Next.js, Vue, Svelte), styling system (Tailwind, CSS Modules, Radix, Shadcn), existing theme tokens, and component directories.
2. **Interactive Requirements Interview**: Asks focused questions to nail down Jobs-To-Be-Done (JTBD), user density needs, and offers 2-3 concrete layout options.
3. **Design Blueprint & Tokens**: Establishes anti-slop visual hierarchy and components grounded in your existing code patterns.
4. **Production Implementation**: Generates clean, accessible (WCAG 2.2 AA), responsive, and 5-state complete UI.

---

## Repository Layout

```text
ui-ux-design/
├── SKILL.md                                 # Primary agent entrypoint & workflow
├── README.md                                # Documentation & installation guide
├── references/
│   ├── workspace-scanner-guide.md           # Tooling & stack detection runbook
│   ├── requirements-interview-framework.md  # JTBD discovery & wireframe option templates
│   ├── anti-slop-manifesto.md               # Banned AI tropes & quality standards
│   ├── design-tokens.md                     # 8pt grid, type scales, semantic color roles
│   ├── ux-heuristics.md                     # Usability rules & response latencies
│   └── accessibility-checklist.md           # WCAG 2.2 AA audit criteria
└── examples/
    ├── linear-issue-tracker.html            # Working Linear-style high-density UI demo
    └── index.html                           # Accessible telemetry dashboard demo
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

## License

MIT
