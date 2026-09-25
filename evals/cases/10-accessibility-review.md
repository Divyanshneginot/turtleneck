# Case 10: Accessibility-Only Review

## User Brief
"Review this existing navigation bar snippet for accessibility issues. Do not rewrite or redesign the visual styles, just audit the markup and tell me what violates WCAG 2.2 AA:
<nav><div class='logo'>Acme</div><a href='/'>Home</a><a href='/pricing'>Pricing</a><button onclick='toggle()'><svg viewBox='0 0 24 24'><path d='M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z'/></svg></button></nav>"

## Classification
- **Expected Trigger**: Trigger (Review scope)
- **Expected Mode**: `Direct Phase 4` / `Review Mode`
- **Domain Context**: Accessibility and semantic audit of existing code.

## Behavioral Expectations
1. **Audit Precision**:
   - Identifies the unlabelled icon-only hamburger button (missing `aria-label="Toggle navigation menu"` or screen-reader text).
   - Identifies missing disclosure semantics on the toggle (`aria-expanded="false"`, `aria-controls="nav-menu"`).
   - Notes missing active page indicator on navigation links (`aria-current="page"`).
   - Notes touch target size requirements (minimum 44x44px for the toggle button).
2. **Review Discipline**:
   - Strictly addresses the accessibility audit request.
   - Does NOT launch into a 4-question visual requirements interview.
   - Does NOT redesign the logo or rewrite layout with new visual archetypes.

## Negative Markers (Failure Modes)
- Running an interactive interview asking about design archetypes for an audit request.
- Hallucinating aesthetic defects instead of identifying the concrete markup accessibility failures.
- Omitting the missing accessible name on the icon button.
