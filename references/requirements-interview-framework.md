# Requirements Interview Framework

Actionable protocol for conducting a focused, rapid UI/UX alignment interview with the user.

---

## 1. The 3 Essential Discovery Questions

Never jump straight to writing code based on ambiguous prompts. Ask the user 3 structured questions:

### Q1: Job-To-Be-Done (JTBD) & Primary Outcome
* *"What is the single most critical action or decision a user needs to make on this screen?"*
* Examples: Monitor active background workers; Filter and export audit logs; Complete a multi-step checkout.

### Q2: Information Density & User Archetype
* *"What density level fits the workflow best?"*
  * **Option A: High Density / Operational** (Compact tables, tight row padding, power-user hotkeys, minimal whitespace).
  * **Option B: Balanced / SaaS Dashboard** (Clear metrics cards, separated list items, moderate whitespace).
  * **Option C: Guided / Consumer Flow** (Single-task focus, large touch surfaces, progressive disclosure).

### Q3: Layout Architecture Options
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
