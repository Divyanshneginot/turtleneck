# Case 08: Explicit Time-Box Brief

## User Brief
"I have a demo in 15 minutes! Build a responsive pricing table in React for a developer analytics tool: Free ($0), Pro ($29), Enterprise (Custom). Don't ask me questions, just pick good defaults and give me the code now."

## Classification
- **Expected Trigger**: Trigger
- **Expected Mode**: `Time-boxed Fast Path`
- **Domain Context**: Hard time deadline with explicit request to skip interview questions.

## Behavioral Expectations
1. **Tempo Calibration**:
   - Accurately selects Time-boxed Fast Path.
   - Asks ZERO questions; does not block on approval.
2. **Preflight Decision**:
   - States inferred choice (e.g. High-Density Starlight or High-Trust Corporate) and ONE alternative in a single preflight line.
   - Builds immediately without waiting.
3. **Craft Completeness Under Speed**:
   - Ships complete, production-ready code (no TODOs or placeholders).
   - Injects 5 states on CTA buttons, responsive flex/grid wrap, and verified contrast.
4. **Audit Reporting**:
   - Output Contract clearly records `Execution mode: time-boxed` and `Interview: skipped, reason: user commanded immediate build under 15-minute deadline`.

## Negative Markers (Failure Modes)
- Halting execution to ask the 4 discovery questions despite the 15-minute deadline.
- Leaving TODO comments for mobile styles or button states.
- Missing the Output Contract or omitting the reason for skipping the interview.
