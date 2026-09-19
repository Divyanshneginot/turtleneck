# Requirements Interview Framework

Actionable protocol for conducting a focused, rapid UI/UX alignment interview with the user.

---

## 0. Earn the interview before running it

The interview is a ceiling, not a default. Pick the route the brief earns before asking anything:

| Situation | Route |
| :--- | :--- |
| One component, one style tweak, a fix, or the user said "just do it" | **Direct Phase 4** — no interview; apply craft rules, build. |
| Hard deadline, or a brief already naming scope + stack across all four dimensions (archetype, surface, density, layout direction) | **Fast path** — restate inferred constraints in one preflight line, raise at most one real ambiguity, build. |
| Vague or consequential (greenfield, flagship marketing, design system) | **Full interview** below. |

Under a hard time budget, compress the pipeline deliberately:

1. Skip the full interactive interview; infer archetype, stack, and density from the codebase and
   the request itself.
2. State the inferred choice and ONE alternative in a single line, then proceed — wait for
   confirmation only when the brief is genuinely ambiguous on *scope*, not on *taste*.
3. Go straight to Phase 3/4: lock tokens from `design-tokens.md`, mirror the closest `examples/`
   file, build.
4. Still run the non-negotiables before declaring done (focus-visible, `>=44px` tap targets,
   reduced-motion, contrast verification).
5. Close with the Output Contract and an auditable line: `Interview: skipped, reason: <one line>`.

Never burn a full interview cycle on a two-minute fix. If the task is small or well-scoped, say
so in one line and take the short route — an agent that interviews for every tweak is failing the
protocol, not following it.

---

## 1. The 4 Essential Discovery Questions

Never jump straight to writing code based on ambiguous prompts. Ask the user 4 structured questions:

### Q1: Visual Archetype & DNA
* "Based on your project domain, should this feel like A) High-Trust Corporate, B) Warm Editorial Paper, C) Fluid Organics, D) High-Density Starlight, or E) Stark Geometric?"
* (Or agent researches domain to recommend one.)

### Q2: Job-To-Be-Done (JTBD) & Primary Outcome
* *"What is the single most critical action or decision a user needs to make on this screen?"*
* Examples: Monitor active background workers; Filter and export audit logs; Complete a multi-step checkout.

### Q3: Information Density & User Archetype
* *"What density level fits the workflow best?"*
  * **Option A: High Density / Operational** (Compact tables, tight row padding, power-user hotkeys, minimal whitespace).
  * **Option B: Balanced / SaaS Dashboard** (Clear metrics cards, separated list items, moderate whitespace).
  * **Option C: Guided / Consumer Flow** (Single-task focus, large touch surfaces, progressive disclosure).

### Q4: Layout Architecture Options
Present 2 concrete wireframe architectures suited for the task:
* **Architecture 1: Master-Detail Split** (Left list, right active detail pane. Ideal for fast triage).
* **Architecture 2: Full-Width Data Grid + Drawer** (Spacious tabular overview with slide-over panel for inspect/edit).
* **Architecture 3: Modular Bento Dashboard** (High-level telemetry widgets with drill-down routes).

---

## 2. Option Selection Template

Present choices cleanly to user:

```text
Based on workspace analysis ([Stack]), here are two layout options for [Feature]:

• Option 1 (Recommended): [Name]
  - Layout: [e.g., Split-pane with sticky filter rail]
  - Best for: [e.g., Rapid triage and frequent keyboard navigation]

• Option 2: [Name]
  - Layout: [e.g., Full-width paginated table with slide-over drawer]
  - Best for: [e.g., Deep data inspection with 10+ columns]

Which approach matches your goal best?
```
