# Turtleneck Behavioral Evaluation Suite

Automated and blinded evaluation protocol to measure whether loading the Turtleneck skill causes an AI agent to produce measurably better, more accessible, less templated, and appropriately calibrated user interfaces compared to a baseline model without the skill.

---

## 1. Overview & Evaluation Goals

Most agent skills only verify that their own repository files are internally consistent. Turtleneck's evaluation suite tests the **actual behavioral effect on the agent**:
- Does the skill trigger when it should, and stay silent on non-UI tasks?
- Does it calibrate ceremony (e.g. skipping interviews on one-line fixes or tight deadlines)?
- Does it derive visual direction from domain materials before picking an archetype, avoiding generic template slop?
- Does it produce 5-state complete, accessible, touch-ergonomic components?
- Does it verify contrast and state claims with deterministic proof rather than hallucinated assertions?

---

## 2. Benchmark Protocol (Baseline vs. Skill)

Each evaluation run consists of a controlled, paired comparison across the 10 test cases in [`cases/`](./cases/):

```
                   ┌───────────────────────────────┐
                   │   Case Brief in evals/cases/  │
                   └──────────────┬────────────────┘
                                  │
                 ┌────────────────┴────────────────┐
                 ▼                                 ▼
      ┌─────────────────────┐           ┌─────────────────────┐
      │  A: Baseline Run    │           │  B: Turtleneck Run  │
      │  (Model WITHOUT     │           │  (Model WITH        │
      │   Turtleneck skill) │           │   Turtleneck skill) │
      └──────────┬──────────┘           └──────────┬──────────┘
                 │                                 │
                 └────────────────┬────────────────┘
                                  ▼
                   ┌───────────────────────────────┐
                   │    Blinded Rubric Scoring     │
                   │    (using evals/rubric.md)    │
                   └──────────────┬────────────────┘
                                  ▼
                   ┌───────────────────────────────┐
                   │  Deterministic Gate Checks    │
                   │  (check_contrast.py --tokens) │
                   └───────────────────────────────┘
```

### Protocol Steps

1. **Model & Environment Control**:
   - Both runs use the exact same foundation model version, temperature (recommended: 0.2), and system environment.
   - Run A receives standard general coding instructions.
   - Run B receives the same instructions plus the Turtleneck skill entrypoint (`SKILL.md` or installed rule).

2. **Case Execution**:
   - Present the prompt from each case in [`evals/cases/`](./cases/) verbatim.
   - Record the full transcript: model thoughts, interview questions (if any), emitted code, and completion contracts.

3. **Deterministic Verification**:
   - Extract declared tokens from emitted code or Output Contract.
   - Run `python scripts/check_contrast.py --tokens <emitted_tokens.json>` to verify mathematical WCAG 2.2 AA contrast.
   - Verify presence of `:focus-visible`, `@media (prefers-reduced-motion)`, tap target constraints, and compositor-only transitions.

4. **Blinded Scoring**:
   - An independent evaluator or structured LLM-as-judge scores anonymized outputs against [`evals/rubric.md`](./rubric.md) across all 9 dimensions (0–18 raw score, converted to percentage).

5. **Success Criteria**:
   - **Adherence**: Turtleneck must trigger on cases 1–8 and 10, and must NOT trigger on case 9 (pure backend/CLI).
   - **Ceremony**: Case 4 (tiny CSS fix) and Case 8 (time-box) must skip the multi-question interview.
   - **Delta**: Treatment score must exceed baseline score by at least +20 percentage points on average.

---

## 3. Results Scorecard

> **Status:** Unmeasured (Scaffold and cases published; baseline comparison runs pending initial execution).

| Case ID | Brief Description | Target Mode | Baseline Score | With Turtleneck | Delta | Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **01** | Vague Greenfield UI (KiteCache) | Full Pipeline | — | — | — | Unmeasured |
| **02** | Dense Operations Dashboard (K8s) | Full / Fast Path | — | — | — | Unmeasured |
| **03** | Mobile Form (Boutique Coffee) | Full / Fast Path | — | — | — | Unmeasured |
| **04** | Tiny CSS Fix (Button border) | Direct Phase 4 | — | — | — | Unmeasured |
| **05** | Supplied-Design Replication (Figma) | Fast / Direct | — | — | — | Unmeasured |
| **06** | Modal Keyboard Behavior (API key) | Direct Phase 4 | — | — | — | Unmeasured |
| **07** | Low-Contrast Regression (#94a3b8) | Direct / Review | — | — | — | Unmeasured |
| **08** | Explicit Time-Box (15-min demo) | Time-boxed Fast | — | — | — | Unmeasured |
| **09** | Non-UI Task (Apache log parser) | Skip (No trigger)| — | — | — | Unmeasured |
| **10** | Accessibility Review (Nav snippet) | Direct Review | — | — | — | Unmeasured |
| **Mean** | | | **—** | **—** | **—** | **Pending** |

*Note: In accordance with Turtleneck's honesty and verification principles, no scores or performance claims are published until actual baseline vs. treatment benchmark runs have been executed and logged.*
