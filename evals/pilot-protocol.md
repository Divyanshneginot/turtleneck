# Phase C Evaluation Protocol & Success Definition

## 1. Testable Definition of Success

The Turtleneck skill succeeds if and only if it helps the agent independently reach a fitting design concept, translate inspiration rather than copy it, and execute coherently across unrelated product domains without user micromanagement.

### Pass Criteria (Must satisfy all):
1. **Transferable Judgment**: Candidate outperforms baseline across all four distinct domain briefs, not merely its own landing page.
2. **Zero Inappropriate Reference Copying**: Zero instances of pasting literal external metaphors (e.g. terminal prompts on non-CLI tools, drafting tools on non-studio products).
3. **No Decorative Compliance Slop**: Zero fake audit chips (`PASS/FAIL`), zero decorative server telemetry on consumer/event surfaces, and zero gimmick toggles (`SFX: ON`, `8PT GRID`).
4. **Complete Functional Ergonomics**: 100% of interactive controls implement keyboard focus-visible (>=3:1), semantic labels, valid touch targets (>=44px where applicable), and compositor-only transitions with `prefers-reduced-motion` support.
5. **Calibrated Tempo**: Zero discovery interviews on small CSS tweaks or tight timeboxes; structured options presented only when architectural direction is genuinely ambiguous.
6. **Integrity of Claims**: No claims of WCAG certification or mathematical ratios that are not verified by deterministic checks or rendered testing.

---

## 2. 3-Arm Comparison Matrix

| Arm | Description | Purpose |
| :--- | :--- | :--- |
| **Arm 1: Baseline** | Model with NO Turtleneck skill | Measure unassisted default model capabilities. |
| **Arm 2: Current** | Model with current Turtleneck (`b813a7f`) | Measure whether current additive mandates help or hinder. |
| **Arm 3: Candidate** | Model with candidate decision-loop skill | Measure whether restructured decision engine improves outcome. |

---

## 3. Four Standardized Pilot Briefs

Total runs: 4 briefs × 3 arms × 2 fresh runs = **24 controlled runs**.

### Brief 1: Product Proof (Turtleneck Landing Page)
- **Task**: "Create a landing page for Turtleneck, a product design intelligence skill for AI coding agents. Demonstrate how it improves agent decision-making."
- **Focus**: Product proof, honest claims, relevant centerpiece, reference translation rather than cloning.

### Brief 2: Expressive Cultural/Event Surface
- **Task**: "Build a promotional and ticketing landing page for 'Archipelago 2027', an international experimental architecture and sound biennial held across five volcanic islands."
- **Focus**: Can the design be intentionally elaborate, atmospheric, and expressive WITHOUT defaulting to dark developer starlight or atelier workbench cliches?

### Brief 3: High-Density Operational Dashboard
- **Task**: "Build an operations telemetry dashboard for a municipal water treatment plant monitoring pump pressures, chemical filtration stages, and flow rates across 12 zones."
- **Focus**: True operational density, legitimate telemetry, scannability, urgent threshold semaphores, zero ornamental bento fluff.

### Brief 4: Mobile Booking & Input Flow
- **Task**: "Build a mobile-first appointment booking flow for a neighborhood dental studio, including treatment selection, date/time picker, patient info, and confirmation."
- **Focus**: Thumb zones, form clarity, error recovery, step state preservation, zero horizontal scroll, tactile completion.

---

## 4. Evaluation Protocol

1. **Isolation**: Every run executed in a fresh context window. No conversational cross-contamination.
2. **Controls**: Identical model, identical prompts, identical starting files, fixed viewport targets.
3. **Double-Blind Review**:
   - Screenshots and working HTML anonymized (labeled Run A-X).
   - Evaluator scores visual hierarchy, domain fit, identity coherence, and usability BEFORE reading the agent transcript or rationale.
4. **Scoring Breakdown**:
   - **Task Fit & Domain Empathy (25%)**: Does the design speak the native language of the domain?
   - **Visual Hierarchy & Restraint (25%)**: Clear focal point, proper density, zero decorative clutter.
   - **Interaction & State Rigor (25%)**: Complete states, keyboard navigation, touch ergonomics.
   - **Claim & Execution Integrity (25%)**: Accurate math, working code, honest verification statements.
