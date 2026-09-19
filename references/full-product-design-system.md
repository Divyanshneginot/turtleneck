# Full Product Design System Taxonomy

Comprehensive specifications for every core application surface beyond landing pages.

---

## 1. The 6 Core Product Surfaces

```
1. App Shell & Nav  ──► 2. Dashboards  ──► 3. Data Tables  ──► 4. Forms/Settings  ──► 5. Overlays/Drawers  ──► 6. Empty States
```

---

### Surface 1: Application Shell & Global Navigation
* **Sidebar**: `220px – 240px` fixed width (or `56px` collapsed icon-rail).
  - Grouped navigation headers (`11px` uppercase tracking `+0.06em`).
  - Active item indicator: Subtle surface fill (`#15181e`) with high-contrast label (`#ededed`).
  - Keyboard accelerator badges (`1`, `2`, `G then S`).
* **Header / Titlebar**:
  - Breadcrumbs path with hoverable ancestral segments.
  - Global Search / Command Bar trigger (`Ctrl+K`).
  - Workspace selector & user profile dropdown.

---

### Surface 2: Dashboards & Telemetry Views
* **KPI Metrics Cards**:
  - Label (`12px` muted uppercase), large value (`28px` bold `tabular-nums`), trend indicator (`+12.4% vs last cycle` in emerald/rose).
  - Micro sparkline SVG curve beside or beneath value.
* **Time Range Controls**: Segmented button group (`24h`, `7d`, `30d`, `Custom`) with sliding pill indicator.
* **Chart Containers**: 1px hairline border, subtle gridlines (`rgba(255,255,255,0.04)`), tooltips anchored to cursor position.

---

### Surface 3: Dense Data Tables & CRUD Views
* **Table Header**:
  - Sticky header with sorting indicators (`▲`/`▼`) on clickable column headers.
  - Master checkbox for bulk select (`indeterminate` state support).
* **Table Rows**:
  - Height: `32px` (compact) to `40px` (comfortable).
  - Hover highlight (`rgba(255,255,255,0.025)`).
  - Fixed-width numerical columns with `tabular-nums` right-aligned.
  - Status column with colored pips (`emerald` for active, `amber` for pending, `rose` for failed).
* **Batch Action Toolbar**: Floating bar appearing when $\ge 1$ item selected (`Delete Selected`, `Change Status`, `Export`).

---

### Surface 4: Forms & Input Systems
* **Input Fields**:
  - Height: `36px`, font size `13px`.
  - Border: `1px solid rgba(255,255,255,0.08)`, focus outline: `2px solid var(--accent-indigo)`.
  - Floating or persistent labels (never disappearing placeholder-only labels).
  - Validation states:
    - *Valid*: Subtle green border glow.
    - *Error*: `1px solid #f43f5e`, inline error text below input with `aria-live="polite"`.
* **Controls**:
  - Toggle Switch: `36px × 20px` track with `16px` sliding thumb.
  - Segmented Control: `padding: 2px` track with active sliding pill.

---

### Surface 5: Overlays, Drawers & Dialogs
* **Slide-Over Detail Drawer**:
  - Width: `420px – 480px`, sliding from right viewport edge (`translateX(100% -> 0)` in `240ms`).
  - Allows deep inspection and editing of a record without losing context of the background table.
  - Header with title, close button (`Esc`), and action tabs.
* **Confirmation Modal**:
  - Critical/Destructive: Red action button (`Delete Workspace`), required text-confirmation input (`type "DELETE" to confirm`).
* **Toast System**:
  - Fixed bottom-right `24px`, stacked with `8px` gap, auto-dismiss in `4000ms`, includes `Undo` action.

---

### Surface 6: Empty States & Error Boundaries
* **Empty State Blueprint**:
  - 1. Muted geometric icon or illustration.
  - 2. Clear status heading (e.g. *"No API keys created yet"*).
  - 3. Explanatory sentence (e.g. *"Create a secret key to authenticate your server-side requests"*).
  - 4. Primary CTA button (`+ Create Secret Key`).
* **Error Boundary**:
  - Clear diagnosis without technical stack dumps.
  - Immediate recovery action (`Retry Operation` or `Back to Safety`).
