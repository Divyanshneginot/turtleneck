# Verification Scope & Fast Path

What Turtleneck's automated checks actually prove — and what they deliberately do not — plus the
rules for when the full requirements interview is required and when an explicit brief may be
fast-pathed.

---

## What the gates verify (and what they do not)

Three zero-dependency scripts run in CI and locally. Each one is a *scoped, heuristic check on
declared inputs*, not a certification of an arbitrary product UI.

### `scripts/check_contrast.py`

* **Verifies:** every colour pair **declared in this repository's token table** against WCAG 2.2 AA
  thresholds (4.5:1 for text, 3:1 for UI component boundaries and graphical objects). It also fails
  the build if a declared pair drifts from the value the documentation actually contains, so a token
  cannot be silently weakened.
* **Does not verify:** colour usage that is never declared. A generated UI that introduces a new,
  unlisted hex colour — or computes colours at runtime, re-tints an image, or relies on opacity
  stacking — is outside this gate's scope. It also does not compute DOM-level rendered contrast.

### `scripts/check_examples.py`

* **Verifies:** that the three reference `examples/*.html` files honour the protocol's *textual*
  markers: `:focus-visible` rules, a `prefers-reduced-motion` fallback, no `transition: all`,
  accessible names on icon-only controls, labelled inputs, and declared token contrast.
* **Does not verify:** semantic document structure, runtime keyboard behaviour, focus trapping and
  restoration, ARIA correctness, responsive layouts at real viewport widths, browser-computed
  contrast, or visual regressions. It is a regex/source-level gate on code that is *written* a11y
  correctly — it cannot prove the running page is accessible.

### `scripts/check_consistency.py`

* **Verifies:** that the 4-phase pipeline line is byte-identical across `README.md`, `SKILL.md` and
  every `rules/` file; that the Requirements Interview step survives into every rules file; that
  every cited `.turtleneck/references/*.md` path resolves; that no reference doc or example is
  orphaned; and that prompt-facing markdown stays TeX-free.
* **Does not verify:** nothing about the UI an agent actually produces. It is a documentation-graph
  gate, not a design gate.

### What passing the gates therefore means

Passing every gate certifies that **Turtleneck's own declared tokens, examples, and docs are
internally consistent and meet the stated thresholds**. It does **not** certify that any specific
product UI an agent later generates is WCAG 2.2 AA compliant. Do not claim "WCAG compliant"
off the token/example gates alone; claim only what a specific check actually ran. For real
accessibility assurance of a generated product, add browser-based testing (keyboard navigation,
computed styles, a screen-reader pass) on top of these lightweight gates.

---

## Execution modes (tempo) vs the full interview

The interview is the protocol's *ceiling*, not its default. Four modes, chosen by what the brief
earns:

* **Direct Phase 4** — one component, one style tweak, a fix, or the user said "just do it".
  Skip Phases 1–3; apply the Phase 4 craft rules (5-state, motion budgets, contrast) directly.
* **Time-boxed fast path** — a hard deadline, or a brief that already names scope and stack.
  Skip the interview; infer archetype/density from the codebase and the request; state the
  inferred choice and ONE alternative in a single line; proceed without waiting unless the brief
  is genuinely ambiguous on *scope* (not *taste*).
* **Fast path** — an explicit brief that supplies all four of archetype, target surface, density,
  and layout/content direction. Restate inferred constraints in one short preflight, surface at
  most one genuine ambiguity, then build.
* **Full interview** — vague, greenfield, or consequential surfaces (a flagship marketing page, a
  design system). Ask the four questions and pitch 2–3 layouts.

Whichever mode is used, the Output Contract must record it (`Execution mode:` line) plus, when the
interview was skipped, `Interview: skipped, reason: <one line>` — so the shortcut is auditable,
not silent. A full interview on a two-minute fix is a protocol violation, not thoroughness.

### Fast-path trigger

Skip the multi-question interview when the user's brief already supplies **all four** of:

1. **Archetype** — one of the five, or an explicit "no preference".
2. **Target surface** — page, dashboard, form, component, etc.
3. **Density** — high-density operational / balanced SaaS / consumer guided flow.
4. **Layout / content direction** — enough to lock an architecture without pitching 2-3 options.

Then:

1. **Restate** the inferred constraints in one short preflight (archetype, surface, density, layout)
   so the user can veto cheaply.
2. **Surface at most one genuine ambiguity**, if any exists.
3. **Build** immediately after the preflight; do not wait for approval to restate uncontroversial
   defaults.

This keeps one-shot and time-constrained tasks moving while preserving the interview for the cases
where guessing is actually risky.
