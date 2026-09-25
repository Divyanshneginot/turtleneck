# Turtleneck Behavioral Evaluation Rubric

This rubric scores AI agent behavior when presented with UI engineering tasks, measuring whether loading the Turtleneck skill causes measurably better architectural decisions, craft rigor, and verification integrity compared to baseline models.

Scoring Scale:
- **0 = Violation / Fail**: Misses critical requirement, introduces anti-patterns, or violates protocol.
- **1 = Partial / Marginal**: Partially adheres; some ceremony mismatch, generic defaults, or incomplete verification.
- **2 = Exemplary / Compliant**: Cleanly follows protocol; appropriate tempo, domain grounding, verified craft.

---

## 1. Trigger & Mode Selection
*Did the agent trigger only when appropriate, and did it pick the least ceremony the brief earned?*
- **0**: False trigger on pure backend/CLI tasks, OR failed to trigger on vague greenfield UI, OR chose full interview for a one-line CSS tweak.
- **1**: Triggered correctly but mismatched mode (e.g. used Fast Path when a brief was too vague, or used Full Pipeline on a well-specified brief).
- **2**: Optimal mode chosen: skipped on non-UI; Direct Phase 4 for small fixes; Fast Path for explicit briefs; Full Pipeline only for vague/consequential surfaces.

## 2. Ceremony Calibration & Tempo
*Did the agent calibrate friction and question count to the task urgency and scope?*
- **0**: Ran a multi-question interview when the user specified a hard deadline or a one-line fix; or asked zero questions on a vague greenfield project.
- **1**: Asked questions but included redundant or obvious queries already answered in the brief.
- **2**: Zero friction on fast-path / fixes; asked focused JTBD questions and pitched 2–3 concrete wireframe options when architectural ambiguity was real.

## 3. Subject-Matter Specificity
*Did the agent derive the visual language from the domain, audience, and real-world materials before selecting an archetype?*
- **0**: Reflexively jumped to generic templates or dark starlight mode without domain analysis.
- **1**: Mentioned the domain in passing but relied on off-the-shelf archetype defaults with no domain-specific visual moves.
- **2**: Grounded typography, layout density, and materials in the actual subject matter (e.g. clinical precision, financial ledger clarity, editorial reading comfort).

## 4. Creative Distinctiveness vs. Template Reflex (Genericity Check)
*Could this interface be reused unchanged for an unrelated product in this category?*
- **0**: Fails genericity test: interchangeable cookie-cutter layout, giant saturated purple/cyan nebula blobs, hollow bento cards.
- **1**: Avoids slop but feels generic; lacks a memorable, brief-specific design move.
- **2**: Passes genericity test: introduces an intentional, brief-specific design move; authentic visual voice tailored specifically to the problem.

## 5. State & Interaction Completeness
*Are interactive elements built with complete state lifecycles and physical feedback?*
- **0**: Missing hover, active, focus, or disabled states; uses `transition: all`; laggy (>500ms) animations.
- **1**: Implements basic hover/active states, but omits active scale compression (`scale(0.98)`), uses non-compositor transitions, or omits `@media (prefers-reduced-motion)`.
- **2**: Complete 5-state controls (`default`, `hover`, `active:scale(0.98)`, `focus-visible`, `disabled`), `80-120ms` feedback, compositor-only motion, and robust reduced-motion overrides.

## 6. Responsive Behavior & Touch Ergonomics
*Does the layout adapt gracefully and obey physical ergonomics?*
- **0**: Fixed pixel widths that cause horizontal scroll on mobile (320px); tap targets < 36px.
- **1**: Responsive layout wraps, but tap targets on secondary actions fall below 44x44px, or thumb-zone placement is ignored on mobile.
- **2**: Fluid responsive adaptation without horizontal overflow; all interactive controls >= 44x44px physical targets; thumb-zone ergonomics applied for mobile.

## 7. Accessibility & Keyboard Semantics
*Are semantic markup, keyboard interaction, and contrast thresholds rigorously upheld?*
- **0**: Text contrast < 4.5:1; missing accessible names on icon buttons; missing form labels; focus trapped or lost in modals.
- **1**: Text contrast meets 4.5:1, but focus rings are low contrast (< 3:1) or modal focus restoration is omitted.
- **2**: Full WCAG 2.2 AA compliance: >= 4.5:1 text, >= 3:1 UI boundaries/focus rings; native `<dialog>` or trapped focus with `Escape` dismiss and trigger restoration; all controls labelled.

## 8. Verification Evidence & Auditability
*Did the agent provide verifiable proof for its claims using deterministic checks?*
- **0**: No completion contract or report emitted; or claims "tested" without running or citing checks.
- **1**: Emitted Output Contract but left values generic, unverified, or used the full 11-line contract on a minor one-line tweak.
- **2**: Ran contrast verification via `scripts/check_contrast.py` (or computed mathematical ratios); emitted full contract for major builds or Compact Completion Report for Direct Phase 4 fixes with audited checks.

## 9. Claim Discipline & Integrity
*Did the agent avoid false, exaggerated, or unsupported claims?*
- **0**: Made wild claims (e.g. "certifies 100% WCAG 2.2 AA compliant across all browsers") off static code alone.
- **1**: Acknowledged some limits, but blurred the line between token mathematical contrast and rendered DOM accessibility.
- **2**: Strict claim discipline: acknowledges limits in `verification-scope.md`; states exactly what was verified (e.g. declared tokens, regex markers) and what requires browser testing.

---

## Score Summary Table

| Dimension | Max Points | Weight | Score (0-2) | Weighted Score |
| :--- | :---: | :---: | :---: | :---: |
| 1. Trigger & Mode Selection | 2 | 10% | | |
| 2. Ceremony Calibration & Tempo | 2 | 10% | | |
| 3. Subject-Matter Specificity | 2 | 15% | | |
| 4. Creative Distinctiveness | 2 | 15% | | |
| 5. State & Interaction Completeness | 2 | 10% | | |
| 6. Responsive & Touch Ergonomics | 2 | 10% | | |
| 7. Accessibility & Keyboard Semantics | 2 | 15% | | |
| 8. Verification Evidence | 2 | 10% | | |
| 9. Claim Discipline & Integrity | 2 | 5% | | |
| **Total** | **18** | **100%** | | **/ 100%** |

### Benchmark Pass Gates
- **Total Score >= 80%**
- **Zero critical 0s** on Trigger/Mode, Accessibility, or Claim Discipline.
- **Measurable Delta over Baseline**: Treatment (with Turtleneck) must outperform Baseline (without Turtleneck) by at least +20 percentage points overall.
