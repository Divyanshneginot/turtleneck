# Case 06: Modal Keyboard Behavior

## User Brief
"Implement a confirmation modal dialog for deleting an API key in vanilla JavaScript and CSS. It needs to be accessible."

## Classification
- **Expected Trigger**: Trigger
- **Expected Mode**: `Direct Phase 4` or `Fast Path`
- **Domain Context**: Interactive component requiring keyboard semantics and focus management.

## Behavioral Expectations
1. **Dialog Semantics**:
   - Uses native HTML `<dialog>` with `.showModal()` or provides `role="dialog"`, `aria-modal="true"`, and `aria-labelledby`.
2. **Keyboard Management**:
   - Focus trapped within the dialog while active (Tab / Shift+Tab cycling).
   - Dismissal on `Escape` key press.
   - Initial focus directed to a non-destructive element (e.g. Cancel button or dialog close).
   - Focus restored to the triggering element upon closure.
3. **Craft & Motion Timing**:
   - Enter transition: 200–240ms; Exit transition: 100–140ms (asymmetric exit rule).
   - Compositor-only animation (`opacity`, `transform: scale`), never `transition: all`.
   - `@media (prefers-reduced-motion: reduce)` override.
   - Contrast on focus rings >= 3:1 against dialog surface and backdrop.

## Negative Markers (Failure Modes)
- Missing Escape handler or focus trap (keyboard focus escapes behind the overlay).
- Focus lost to `<body>` after closing the modal.
- Transitioning layout properties like `top`, `width`, or `height`.
