# Case 02: Dense Operations Dashboard

## User Brief
"Build a real-time cluster telemetry dashboard for our 200 Kubernetes pods in React + Tailwind. Needs pod status, CPU/memory gauges, log streams, and fast node filtering."

## Classification
- **Expected Trigger**: Trigger
- **Expected Mode**: `Full Pipeline` or `Fast Path` (scope named, but density and telemetry layout require alignment)
- **Domain Context**: SRE, high-density operations, systems observability.

## Behavioral Expectations
1. **Subject Matter & Density**:
   - Leverages High-Density Starlight or similar operational constraint lens.
   - Enforces space-efficient tabular layout with `font-variant-numeric: tabular-nums` for metrics.
   - Uses real functional telemetry widgets; strictly forbids decorative 3D spheres or hollow bento cards.
2. **Accessibility & Semaphores**:
   - Status indicators (healthy/degraded/failed) never convey state by color alone; includes icon or text badges.
   - Contrast >= 4.5:1 on text, >= 3.0:1 on status semaphores and active borders.
3. **Ergonomics**:
   - Keyboard hotkey cues (e.g. `/` for filter, `Esc` to clear).
   - Fast state feedback (`80-120ms`), sub-250ms transitions, compositor-only motion.
4. **Verification**:
   - Output Contract records verified contrast ratios on telemetry badges.

## Negative Markers (Failure Modes)
- Spacious low-density cards with excessive padding that force endless vertical scrolling.
- Unlabelled green/yellow/red dots.
- Slow (>500ms) spring animations on streaming data updates.
