# Case 04: Tiny CSS Fix

## User Brief
"Our primary checkout button has an awkward 1px border that clips on Safari. Just remove the border and add a subtle 1px inner box-shadow instead in Button.tsx."

## Classification
- **Expected Trigger**: Trigger (user-facing UI styling)
- **Expected Mode**: `Direct Phase 4` (tempo calibration test)
- **Domain Context**: Single-component surgical fix.

## Behavioral Expectations
1. **Zero Unnecessary Ceremony**:
   - Skips Phases 1–3 entirely; asks ZERO discovery or interview questions.
   - Does not inquire about JTBD, archetypes, or color preferences.
2. **Surgical Implementation**:
   - Modifies only the requested button border/shadow styling in `Button.tsx`.
   - Preserves 5-state completeness (`hover`, `active:scale(0.98)`, `focus-visible`, `disabled`).
3. **Compact Completion Report**:
   - Emits the 4-line Compact Completion Report (Mode, Files changed, Checks run, Deliberate breaks).
   - Does NOT output the verbose 11-line full Output Contract.

## Negative Markers (Failure Modes)
- Running an interactive requirements interview on a two-minute fix (protocol violation).
- Asking "Which archetype would you like for this button?".
- Emitting the full 11-line Output Contract.
