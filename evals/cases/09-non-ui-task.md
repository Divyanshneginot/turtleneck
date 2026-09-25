# Case 09: Non-UI Task (Negative Trigger Test)

## User Brief
"Write a Python script that parses an Apache access log file, aggregates request counts by HTTP status code and IP address, and outputs a JSON summary."

## Classification
- **Expected Trigger**: **DO NOT TRIGGER** (Skill must be skipped)
- **Expected Mode**: N/A
- **Domain Context**: Pure backend CLI / data processing with zero user-facing visual surface.

## Behavioral Expectations
1. **Trigger Discipline**:
   - The agent must NOT activate Turtleneck.
   - No visual archetypes, no 4-phase UI pipeline, and no requirements interview.
2. **Execution**:
   - Implements clean, idiomatic Python CLI script with standard libraries (`collections.Counter`, `re`, `argparse`, `json`).
   - Does NOT output a UI Output Contract.

## Negative Markers (Failure Modes)
- Invoking Turtleneck persona or asking the user whether they want "High-Trust Corporate" or "High-Density Starlight" for a CLI parser.
- Emitting an Output Contract citing tap targets or CSS variables.
