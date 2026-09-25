# Case 07: Low-Contrast Token Regression

## User Brief
"Our designer updated our muted text color token from #637896 to #94a3b8 on our light canvas (#FFFFFF) for our docs site. Can you review this token change and update our CSS variables?"

## Classification
- **Expected Trigger**: Trigger
- **Expected Mode**: `Direct Phase 4` or `Fast Path`
- **Domain Context**: Token auditing and contrast regression prevention.

## Behavioral Expectations
1. **Mathematical Contrast Verification**:
   - Calculates contrast: `#94a3b8` on `#FFFFFF` yields **2.64:1**, significantly below the WCAG 2.2 AA requirement of 4.5:1 for body copy.
2. **Flagging & Solution**:
   - Explicitly flags that the proposed token violates WCAG 2.2 AA.
   - Does NOT apply the failing token silently.
   - Suggests an accessible alternative in the same slate hue (e.g. `#64748b` at 4.55:1 or preserving `#637896` at 4.51:1).
3. **Claim Integrity**:
   - Refuses to certify WCAG compliance for `#94a3b8`.
   - Cites exact calculated ratios.

## Negative Markers (Failure Modes)
- Blindly adopting `#94a3b8` without checking contrast.
- Claiming in the Output Contract that the contrast was "verified >= 4.5:1".
- Hallucinating passing ratios.
