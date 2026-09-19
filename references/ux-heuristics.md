# UX Heuristics & Interface Usability

Core principles adapted from Jakob Nielsen's 10 Usability Heuristics for modern application design.

---

## 1. Visibility of System Status
* **Response Times**:
  * `< 100ms`: Instantaneous perception (no loader needed).
  * `100ms - 1000ms`: Show inline spinners or micro-progress indicator.
  * `> 1000ms`: Show skeleton loader or determinate progress bar.
* Provide clear feedback on background jobs and async state saves ("Saved", "Syncing...").

---

## 2. Match Between System and Real World
* Use domain-appropriate terminology rather than technical system identifiers (e.g. "Your changes are saved" vs "200 OK update successful").
* Natural mapping: buttons placed where their physical counterparts live (e.g. "Previous" on the left, "Next" on the right).

---

## 3. User Control and Freedom
* Always offer undo/cancel for destructive operations (delete, bulk edit, archive).
* Support `Escape` key dismissal for all modals, drawers, and overlay popups.
* Never trap focus inside an element without an explicit keyboard escape route.

---

## 4. Consistency and Standards
* Follow platform conventions (iOS bottom sheet, desktop command palette, standard placement of search bar).
* Visual consistency: Identical components must look and behave identically across all views.

---

## 5. Error Prevention
* Prevent errors before they occur:
  * Disable actions when prerequisites are missing (or provide tooltips explaining why it is blocked).
  * Require explicit two-step confirmation (modal or type-to-confirm) for irreversible actions (e.g. deleting a database).
  * Sensible input masks for phone numbers, dates, and currency.

---

## 6. Recognition Rather Than Recall
* Minimize cognitive load:
  * Show recently viewed items or recent searches.
  * Keep field labels visible during input (avoid disappearing placeholder-only labels).
  * Use clear iconography paired with text labels for primary navigation.

---

## 7. Flexibility and Efficiency of Use
* Cater to both novice and power users:
  * Accelerators: Keyboard shortcuts (`Ctrl/Cmd + K`, `Enter` to submit).
  * Bulk actions for tables and lists.
  * Direct deep links to detail views.

---

## 8. Aesthetic and Minimalist Design
* Reduce visual noise:
  * Prioritize 1 primary action per screen/card.
  * Remove redundant dividers, excessive borders, and unnecessary decorative icons.
  * Embrace negative space (whitespace is an active design element, not empty space).

---

## 9. Help Users Recognize, Diagnose, and Recover from Errors
* Error messages must:
  1. Clearly state what happened in plain language.
  2. Explain why it happened.
  3. Propose an immediate solution or remedy.
* Highlight the specific form field containing the error in red with an associated inline message directly below the input.

---

## 10. Help and Documentation
* Contextual tooltips on complex metrics or uncommon terms.
* Inline onboarding hints for empty states (empty list views should guide user on how to create their first entry).
