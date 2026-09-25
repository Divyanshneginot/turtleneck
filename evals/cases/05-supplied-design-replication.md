# Case 05: Exact Supplied-Design Replication

## User Brief
"Here is our Figma spec screenshot and exact hex tokens: background #18181b, card #27272a, primary #a855f7, text #fafafa, border #3f3f46. Implement this exact pricing card in HTML/CSS matching the spec."

## Classification
- **Expected Trigger**: Trigger (bounded execution)
- **Expected Mode**: `Fast Path` / `Direct Phase 4` (no architectural interview)
- **Domain Context**: Strict visual replication of client-supplied assets.

## Behavioral Expectations
1. **Respect Supplied Direction**:
   - Uses the supplied hex tokens and layout faithfully; does NOT overwrite them with Turtleneck's default archetype palettes.
   - Skips the requirements interview (the user already made all design decisions).
2. **Inject Craft & Ergonomics**:
   - Injects protocol non-negotiables: `:focus-visible` ring with >= 3:1 contrast against `#27272a`, `prefers-reduced-motion` query, tap targets >= 44x44px.
   - Applies 5 interaction states to the CTA button.
3. **Verification**:
   - Checks contrast on supplied tokens (e.g. notes that `#a855f7` on `#18181b` yields ~4.53:1).
   - Emits completion report noting supplied-design execution.

## Negative Markers (Failure Modes)
- Trying to force Archetype 1 (`#6259ff` Indigo) or another palette over the client's explicit tokens.
- Conducting a multi-question interview asking the user to choose an archetype.
- Omitting focus-visible or accessibility states because the static mockup didn't draw them.
