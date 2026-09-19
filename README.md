# Turtleneck (`turtleneck`)

**The Senior UI/UX Architect Agent Skill.** Like `ponytail` is for senior dev efficiency, `turtleneck` is for senior design craft. A production-grade, anti-slop agent skill that autonomously profiles your codebase, interviews you to clarify UI/UX requirements, aligns on wireframes, and implements accessible, high-performance interfaces.

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
turtleneck/
├── SKILL.md                                 # Primary agent skill entrypoint (Antigravity & Agent Skills spec)
├── README.md                                # Documentation & universal installation guide
├── rules/                                   # Drop-in rules for all major AI coding agents
│   ├── AGENTS.md                            # Universal standard (Antigravity, Codex, Aider, OpenHands)
│   ├── CLAUDE.md                            # Claude Code command-line agent rules
│   ├── .cursorrules                         # Cursor AI editor rules
│   ├── .windsurfrules                       # Windsurf / Cascade rules
│   └── copilot-instructions.md              # GitHub Copilot workspace instructions
├── scripts/
│   ├── install.py                           # Zero-dependency universal installer CLI
│   ├── extract_design.py                    # Playwright headless browser design DNA extractor
│   ├── research_award_sites.py              # Headless inspector for award-winning benchmarks
│   └── research_links.py                    # Headless inspector for category references
├── references/
│   ├── award-winning-craft-playbook.md      # Scale tension, button ergonomics & surface chemistry
│   ├── creative-direction-guide.md          # Principles of authentic soul, personality & materiality
│   ├── creative-synthesis-protocol.md       # Multi-Source (4+) Synthesis rules preventing 1:1 cloning
│   ├── master-ui-craft-benchmark.md         # Motion timing, typography math, OKLCH, WCAG 2.2
│   ├── taste-vs-slop-matrix.md              # Quality rubric & anti-slop quality gate
│   ├── design-archetypes.md                 # 5 archetype palettes (Corporate, Editorial, Fluid, Starlight, Minimal)
│   ├── full-product-design-system.md        # 6 product surfaces & copy-paste accessible primitives
│   ├── framework-integrations.md            # React, Next.js, Vue 3, Svelte 5, Tailwind & Native recipes
│   ├── engineering-craft-recipes.md         # Spotlight cards, hairline borders, editorial & native platform recipes
│   ├── design-research-playbook.md          # Category benchmarks & synthesis manifest template
│   ├── workspace-scanner-guide.md           # Tooling & stack detection runbook
│   ├── requirements-interview-framework.md  # JTBD discovery & wireframe option templates
│   ├── design-tokens.md                     # 8pt grid, type scales, semantic color roles
│   ├── ux-heuristics.md                     # Usability rules & response latencies
│   ├── accessibility-checklist.md           # WCAG 2.2 AA audit criteria
│   ├── deep_research/                       # Curated benchmark extractions (JSON & captures)
│   └── award_research/                      # Award-winning benchmark synthesis (JSON & captures)
└── examples/
    ├── index.html                           # Multi-Archetype Workbench with 5 live visual modes
    ├── creative-craft.html                  # Instrument Console (Original Benchmark Synthesis)
    └── high-density-tracker.html            # High-density keyboard-first issue tracker
```

---

## Universal Installation

Turtleneck works across **all** major AI coding environments.

### 1. One-Line Universal CLI (Any Repository)
Run the installer directly in your project root:

```bash
# Auto-detects your setup and installs AGENTS.md / .cursorrules / Copilot
python path/to/turtleneck/scripts/install.py

# Or install for all platforms simultaneously:
python path/to/turtleneck/scripts/install.py --all
```

---

### 2. Framework-by-Framework Setup

#### A. Cursor
Copy `rules/.cursorrules` to your project root or run:
```bash
python path/to/turtleneck/scripts/install.py --cursor
```

#### B. Claude Code
Copy `rules/CLAUDE.md` to your project root or run:
```bash
python path/to/turtleneck/scripts/install.py --claude
```

#### C. Windsurf / Cascade
Copy `rules/.windsurfrules` to your project root or run:
```bash
python path/to/turtleneck/scripts/install.py --windsurf
```

#### D. GitHub Copilot
Copy `rules/copilot-instructions.md` to `.github/copilot-instructions.md` or run:
```bash
python path/to/turtleneck/scripts/install.py --copilot
```

#### E. Google Antigravity
Install globally into your Antigravity skills catalog:
```bash
python path/to/turtleneck/scripts/install.py --antigravity
```
Or manually:
```powershell
Copy-Item -Recurse -Path .\turtleneck -Destination "$HOME\.gemini\config\skills\turtleneck"
```

#### F. Aider / Codex / OpenHands / Generic Agents
Drop `rules/AGENTS.md` into your repo root. Universal markdown instructions are recognized by all standard LLM tooling.

---

## License

MIT

