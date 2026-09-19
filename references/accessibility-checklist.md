# Accessibility & WCAG 2.2 AA Checklist

Actionable checklist to guarantee inclusive, accessible web and mobile interfaces.

---

## 1. Color and Contrast Requirements

* [ ] **Normal Text (under 18pt / under 14pt bold)**: Minimum contrast ratio of **4.5:1** against the background.
* [ ] **Large Text (18pt+ / 14pt+ bold)**: Minimum contrast ratio of **3:1** against the background.
* [ ] **User Interface Components & Graphical Objects**: Minimum contrast ratio of **3:1** against adjacent background (e.g. input borders, active toggles, icons).
* [ ] **Color as Single Cue**: Never convey information (status, errors, selection) through color alone. Always pair color with text, icon, or pattern.

---

## 2. Touch and Click Ergonomics

* [ ] **Touch Target Size (WCAG 2.5.8 & 2.5.5)**:
  * Minimum size of **44x44 CSS px** (or 24x24 px with sufficient surrounding spacing).
  * Maintain at least **8px** gap between adjacent interactive elements.
* [ ] **Pointer Cancellation (WCAG 2.5.2)**: Action triggers on pointer up (`mouseup`/`touchend`), not pointer down.

---

## 3. Keyboard Navigation and Focus Management

* [ ] **Focus Visible (WCAG 2.4.7)**:
  * Focus indicators must be clearly visible (`outline: 2px solid <accent>; outline-offset: 2px`).
  * Never use `outline: none` without providing an alternative focus style.
* [ ] **Logical Tab Sequence (WCAG 2.4.3)**: Focus order must mirror natural visual reading order (left-to-right, top-to-bottom).
* [ ] **No Keyboard Traps (WCAG 2.1.2)**: Keyboard users must be able to navigate into and out of all components using only `Tab`, `Shift+Tab`, or `Esc`.
* [ ] **Skip Navigation Link (WCAG 2.4.1)**: Provide a "Skip to main content" link as the first focusable element on complex pages.

---

## 4. Semantic Markup & Screen Reader Support

* [ ] **Semantic Structure**: Use correct landmark tags (`<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`, `<dialog>`).
* [ ] **Headings Hierarchy**: Sequential heading levels (`<h1>` through `<h6>`) with no skipped levels. Only one `<h1>` per page.
* [ ] **Icon-Only Buttons**: Must include `aria-label` or visually hidden screen reader text (e.g., `<button aria-label="Close dialog"><svg ... /></button>`).
* [ ] **Images**: Provide meaningful `alt` text for images conveying content. Use `alt=""` or `aria-hidden="true"` for purely decorative elements.
* [ ] **Form Labels**: Every input must have an associated `<label>` element connected via `for`/`id` or `aria-labelledby`.

---

## 5. Motion and Animation Safety

* [ ] **Reduced Motion Preference**: Honor `prefers-reduced-motion: reduce`:
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, ::before, ::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
      scroll-behavior: auto !important;
    }
  }
  ```
* [ ] **Auto-Playing Media**: Never auto-play audio or video without explicit user initiation or an immediate pause control.
