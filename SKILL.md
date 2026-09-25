---
name: turtleneck
version: 2.0.0
description: >-
  Use when designing, building, restyling, or reviewing product surfaces, visual redesigns, onboarding, quizzes, template builders, dashboards, or design-system tokens where interaction model, responsive behavior, or accessibility matters. Skip for non-visual backend/CLI work and exact reproduction of an already supplied design.
---

# Turtleneck — Product Design Intelligence

Turtleneck is not merely a styling checklist. It is a product-design decision system: it turns an outcome into an information architecture, interaction model, visual direction, state model, and implementation plan before writing the UI.

### Operating principle
Decide, then make. Do not decorate an undefined product. First determine what the user is trying to accomplish, what they must decide, what can go wrong, and what feedback makes the next action obvious. Then create an original solution that fits the existing codebase.

Use the smallest process that produces a sound decision. Under a hard deadline, do not ask a long interview: state assumptions, select a viable pattern, build, and leave clear extension points.

### Core pipeline
```
1. Workspace Analysis ──► 2. Requirements Interview ──► 3. Blueprint Alignment ──► 4. Production Build
```

---

## When to invoke

Use for:
* New pages, applications, flows, components, dashboards, settings, onboarding, and redesigns.
* A quiz, guided recommendation tool, configurator, form builder, template picker, or other interactive decision flow.
* Requests such as "make it feel designed," "make it dynamic," "create a modern UI," or "give users options."
* UI/UX audits where recommendations must become implementable changes.

Do not invoke for a trivial isolated CSS fix, a supplied pixel-perfect design, or a non-UI task. Apply the relevant accessibility and interaction rules directly in those cases.

### Select a tempo

| Mode | Use when | Required work |
| :--- | :--- | :--- |
| **Direct** | Tiny, unambiguous change | Inspect local conventions; implement complete states. Skip interview; apply craft rules directly; emit compact completion report. |
| **Fast path** | Scope/stack/outcome are known or time is short | State assumptions in one sentence; select one pattern and one fallback; build. |
| **Discovery** | Vague, high-stakes, or greenfield work | Run the design brief and present 2–3 concrete directions before build. |

Never make a user wait for ceremony when a useful, reversible default exists.

---

## Reference implementations (show, don't tell)

Before building, open the reference implementation closest to your target and mirror its craft.
The gates in `scripts/` assert that they obey the accessibility and craft baselines.

| File | What it demonstrates |
| :--- | :--- |
| `./examples/index.html` | The 5-archetype workbench: Compare token systems, density, and chrome across archetypes. |
| `./examples/high-density-tracker.html` | High-density keyboard-first operational UI: dense telemetry tables, command palette, hotkeys. |
| `./examples/creative-craft.html` | Editorial & instrument craft: serif display tension, tactile button physics, warm surfaces. |
| `./examples/accessible-dialog-palette.html` | Accessible dialogs & command palette: focus trapping, Escape dismissal, trigger restoration, 5-state buttons. |
| `./examples/form-validation-states.html` | Accessible form validation: error summary, inline field states, aria-describedby links, and tap targets. |

---

## 1. Inspect the reality (Workspace Analysis)

Before changing code, inspect the workspace (see [Workspace Scanner Guide](./references/workspace-scanner-guide.md) and [Framework Integrations](./references/framework-integrations.md)):

* Identify framework, routing, styling system, component library, token source, icon/font approach, test/build commands, and relevant existing screens. When targeting mobile or native apps, consult [Mobile, Touch & Native Ergonomics](./references/mobile-touch-and-native.md).
* Reuse local primitives and conventions where they are good; repair inconsistencies rather than layering a second system over them.
* Identify target viewport(s), real data shape, loading/error/empty permissions states, and likely content lengths.
* If references or competitor examples are available, study them as pattern evidence, not as a layout to copy (see [Design Research Playbook](./references/design-research-playbook.md), [Creative Direction Guide](./references/creative-direction-guide.md), and [Creative Synthesis Protocol](./references/creative-synthesis-protocol.md)). Extract task model, navigation, progressive disclosure, trust cues, density, and interaction feedback. Do not reproduce distinctive branding, wording, illustrations, or recognizable page composition.

Output a compact internal design brief:
* **Outcome**: `<user result>`
* **Audience/context**: `<who, where, urgency, device>`
* **Primary action**: `<one verb>`
* **Critical decisions**: `<what users must choose or understand>`
* **Constraints**: `<stack, content, accessibility, deadline>`
* **Success signal**: `<observable completion/metric>`

If key facts are missing, either ask at most three high-leverage questions or proceed with labeled assumptions. Questions should change the design, not merely collect preferences. Refer to [Requirements Interview Framework](./references/requirements-interview-framework.md) and [Verification Scope & Fast Path](./references/verification-scope.md).

---

## 2. Think like a product designer

### 2.1 Choose the interaction archetype
Choose the archetype from the job, not a fashion preference (see [Design Archetypes Catalog](./references/design-archetypes.md)):

| User job | Default pattern | Design test |
| :--- | :--- | :--- |
| Compare / monitor many items | Dense dashboard, table + detail pane | Can a user scan, filter, and act without losing place? |
| Make one consequential choice | Guided chooser / quiz / recommendation flow | Does each answer reduce uncertainty? |
| Create from a starting point | Template gallery + preview + customization | Can a newcomer start in one click and an expert customize? |
| Learn or convert | Narrative landing page | Does each section earn the next scroll/action? |
| Produce/edit content | Focused workspace with progressive tools | Is the canvas primary and controls contextual? |
| Configure a system | Settings with clear grouping and safe defaults | Can a user predict the effect before saving? |

A dark dashboard is not a default. Pick light/dark, density, type, and material based on audience, environment, task duration, and brand constraints. Ground visual choices in the product's real-world subject matter. Avoid interchangeable templates (see [Award-Winning Craft Playbook](./references/award-winning-craft-playbook.md)).

### 2.2 Generate options before committing
For discovery work, produce 2–3 meaningfully different directions, each with:
* a name and one-sentence thesis;
* page/flow structure;
* density and visual archetype;
* why it fits the job;
* one trade-off.

Good differences are structural (guided flow vs gallery, split pane vs workspace), not superficial color swaps. Recommend one. If the user does not choose and timing matters, choose the option that minimizes cognitive load and supports the primary outcome.

### 2.3 Design the whole state machine
For every interactive surface, specify:
* default, hover, active/pressed, keyboard focus-visible, disabled;
* loading/skeleton, success/confirmation, empty, error/retry, and offline/permission state where relevant;
* entry, exit, cancellation, undo, and persistence behavior;
* desktop keyboard path and touch path.

A UI is incomplete if its happy path alone is designed. Validate against [Taste vs. Slop Matrix](./references/taste-vs-slop-matrix.md).

---

## 3. Special capability: quizzes, recommenders, and template builders

When users do not know what they need, make the interface help them decide instead of presenting an overwhelming blank canvas.

### 3.1 Guided quiz / recommender
Use a quiz only when answers genuinely alter the recommendation. Do not disguise a marketing form as a quiz.

**Flow contract:**
* Establish the desired outcome in the first question.
* Ask 3–7 independent, plain-language questions; every question must affect scoring, filters, or the resulting setup.
* Use one decision per step. Offer "Not sure" when uncertainty is valid.
* Show progress as Step n of m, allow Back, preserve answers, and make Exit/cancel obvious.
* Explain the result using the user's own answers: "Recommended because you chose…"
* Offer a primary next step plus alternatives and an editable answer summary.

**Recommendation model:**
* Define options as data, not scattered conditional JSX.
* Give each option explicit fit rules/weights and a deterministic tie-breaker.
* Never claim false precision. If inputs are insufficient, return a shortlist and explain what would differentiate it.
* Keep scoring client-side when possible; do not collect sensitive data unless the product needs it and consent is clear.

Example schema:
```typescript
type Answer = string | number | boolean;
type Template = {
  id: string;
  name: string;
  description: string;
  tags: string[];
  preview: string;
  score: (answers: Record<string, Answer>) => number;
  rationale: (answers: Record<string, Answer>) => string[];
};
```

### 3.2 Template chooser
A template selection surface must enable action, not act as a static card grid.

**Required behavior:**
* 6–12 realistic starter templates grouped by user intent; include Blank only as a deliberate expert option.
* Search, category filters, and clear selected state when the collection warrants them.
* A fast preview (side panel, modal, or live canvas) containing actual structure/content, not a generic image rectangle.
* "Use template" creates an editable copy; template remains immutable.
* The chosen template may be tailored by quiz answers or a few lightweight controls (tone, color, sections, audience).
* Preserve selection and customization across navigation/reload when the host product supports persistence.

Choose between gallery-first and quiz-first:
* **Gallery-first**: users recognize what they want; show templates immediately, filters refine.
* **Quiz-first**: users describe needs better than they recognize layouts; recommend 1–3 templates, then let them browse all.
* **Hybrid**: show a gallery plus "Help me choose" when both populations matter.

### 3.3 Dynamic UI should have purpose
Use dynamic behavior to reveal cause and effect:
* selection updates a real preview;
* a step answer updates recommendation confidence or downstream options;
* form validation appears at the field at an appropriate time;
* filters update count and preserve scroll/context;
* changes are undoable when consequential.

Do not add animation that delays choice, hides navigation, or exists only as decoration. See [Full Product Design System](./references/full-product-design-system.md).

---

## 4. Visual and motion craft

### Visual direction
Create a compact token layer compatible with the project (see [Design Tokens](./references/design-tokens.md)):
* semantic colors: canvas, surface, raised surface, text, muted text, border, accent, success, warning, danger;
* spacing scale; type roles; radius/elevation; z-index; motion durations/easings.
* Use a limited, intentional palette. Reserve high-saturation color for meaningful actions/status.
* Select typography for the product's voice and reading task; use a deliberate display/body contrast only when it helps hierarchy.
* Establish hierarchy through layout, type, contrast, and whitespace before adding borders, shadows, or gradients.
* Avoid generic "AI UI" signals: arbitrary purple gradients, floating glass cards, excessive pills, meaningless charts, and uniform card grids.

### Motion system
Motion must communicate state, hierarchy, continuity, or causality (see [Engineering Craft Recipes](./references/engineering-craft-recipes.md)):
* Micro feedback: 80–140ms.
* Enter: 180–260ms; exit: 100–180ms, normally shorter than entry.
* Use `transform` and `opacity`; never `transition: all`.
* Use one easing family, e.g. `cubic-bezier(.16, 1, .3, 1)`; avoid bouncy motion in serious workflows.
* Selection may crossfade/slide a preview; step changes may transition in the direction of travel; validation may use a subtle non-looping cue.
* Respect `prefers-reduced-motion: reduce`: remove nonessential movement while preserving state clarity.
* Never use autoplay motion that competes with reading, creates motion sickness, or blocks input.

### Responsive behavior
Design narrow screens deliberately rather than shrinking desktop (see [Mobile, Touch & Native Ergonomics](./references/mobile-touch-and-native.md)):
* define what stacks, scrolls, collapses, becomes a sheet, or becomes a separate step;
* retain primary action and progress/context;
* avoid horizontal scrolling except intentionally scrollable data regions;
* validate at narrow mobile, common laptop, and wide desktop widths.

---

## 5. Implementation standard

* Build the semantic structure and real interaction model first; then style.
* Keep components small around user concepts, not arbitrary visual fragments. Keep quiz/template data separate from rendering.
* Use framework-native state patterns. Do not add a state library for a local chooser.
* Use semantic controls (`button`, `label`, `input`, `dialog`, `nav`, headings) rather than clickable divs (see [Master Craft Benchmark](./references/master-ui-craft-benchmark.md)).
* Give every async action visible pending/success/error handling. Prevent duplicate submission.
* Use stable keys, preserve focus after DOM changes, and return focus when dialogs close.
* Do not fabricate analytics, testimonials, performance claims, user data, or "AI recommendations." Use realistic mock content only when mock data is requested or unavoidable, and label it in development/demo contexts.
* Do not introduce external assets, trackers, or dependencies unless justified by the existing project and task.

### Accessibility baseline
Meet WCAG 2.2 AA contrast targets (see [Accessibility Checklist](./references/accessibility-checklist.md) and [UX Heuristics](./references/ux-heuristics.md)):
* 4.5:1 normal text, 3:1 large text and UI boundaries.
* Every function is keyboard operable; focus order follows visual/task order.
* Use visible `:focus-visible` indicators with sufficient contrast.
* Targets are at least 44 × 44 CSS pixels when touch is relevant.
* Label controls, inputs, progress, icons, errors, and dynamic status appropriately; never rely on color alone.
* Dialogs trap focus, close on Escape where appropriate, restore trigger focus, and expose a real accessible name.
* Reduced-motion support is mandatory.

### Verification
Before claiming completion:
* run the repository's relevant build, typecheck, lint, and tests;
* inspect desktop and mobile layouts; exercise keyboard-only navigation;
* test default, hover, focus, disabled, loading, empty, error, and success states that apply;
* verify quiz scoring/recommendation paths and template preview/apply/reset flows with representative answers;
* check the console for errors and avoid layout shift introduced by the work.
* Report only checks actually run. If environment/tooling prevented a check, say so plainly.

---

## Response contract

For a build, end with:

```text
Mode             : direct / fast path / discovery — reason
Outcome          : <what the surface enables>
Pattern          : <chosen archetype and why>
Design direction : <visual/density choice>
Interaction model: <key flow; quiz/template logic if used>
Responsive plan  : <mobile behavior>
Accessibility    : <implemented provisions; verified items only>
Motion           : <purpose and reduced-motion behavior>
Files changed    : <paths>
Verification     : <commands/checks actually run and results>
Assumptions      : <only unresolved assumptions>
```

#### Compact Completion Report (Direct Mode)
For tiny, unambiguous changes, emit the compact report:
```text
Mode             : Direct (<one-line reason>)
Files changed    : <list>
Checks run       : contrast (<ratio>:1, verified) · focus-visible [yes] · reduced-motion [yes]
Deliberate breaks: <any rule intentionally violated, or "none">
```

For a design-only request, provide: the brief, 2–3 directions when discovery is warranted, recommended direction, information architecture, interaction/state model, and an implementation-ready prompt. Do not pretend code or verification occurred.

---

## Implementation-ready prompt template

Use this prompt when handing Turtleneck a concrete build task:

```text
Use the turtleneck skill in [fast path/discovery] mode. Inspect the existing project before editing.

Build: [surface and primary user outcome].
Users: [audience/context].
Required content/data: [real schema or fixtures].
Platform/constraints: [framework, routes, dependencies, deadline].

The experience must [choose one: let users browse templates / guide unsure users through a 3–7 question recommender / support both].
Templates/options: [list, categories, or domain].
For a recommender, make every question change a deterministic, explainable result. Preserve Back,
progress, answers, accessible keyboard navigation, and an editable result. For templates, provide
search/filter when useful, a real preview, selected state, and an editable copy after "Use template."

Create an original direction informed by patterns, not a clone of any named site. Use purposeful
responsive motion, all meaningful UI states, semantic HTML, focus-visible styles, and
prefers-reduced-motion support. Do not ask more than three questions; if blocked by ambiguity,
state assumptions and ship the strongest reversible default.

Run the relevant checks. End with Turtleneck's response contract, listing only verification you ran.
```
