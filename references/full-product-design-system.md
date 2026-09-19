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
* **Batch Action Toolbar**: Floating bar appearing when >= 1 item is selected (`Delete Selected`, `Change Status`, `Export`).

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

---

## 2. Production-Ready Accessible Component Primitives

Copy-pasteable, zero-dependency accessible implementations compliant with WCAG 2.2 AA.

### A. Accessible Modal Dialog (`<dialog>`)

```html
<button id="open-dialog-btn" class="btn-primary">Open Settings</button>

<dialog id="settings-dialog" class="app-dialog" aria-modal="true" aria-labelledby="dialog-title">
  <div class="dialog-header">
    <h2 id="dialog-title">Project Settings</h2>
    <button id="close-dialog-btn" class="btn-close" aria-label="Close dialog">✕</button>
  </div>
  <div class="dialog-body">
    <label for="project-name">Workspace Name</label>
    <input id="project-name" type="text" class="input-field" value="Production Cluster">
  </div>
  <div class="dialog-footer">
    <button id="cancel-btn" class="btn-ghost">Cancel</button>
    <button class="btn-primary">Save Changes</button>
  </div>
</dialog>

<script>
  const dialog = document.getElementById('settings-dialog');
  const openBtn = document.getElementById('open-dialog-btn');
  const closeBtn = document.getElementById('close-dialog-btn');
  const cancelBtn = document.getElementById('cancel-btn');

  openBtn.addEventListener('click', () => dialog.showModal());
  [closeBtn, cancelBtn].forEach(b => b.addEventListener('click', () => {
    dialog.close();
    openBtn.focus(); // Restore focus to trigger element
  }));

  // Backdrop click dismiss
  dialog.addEventListener('click', (e) => {
    if (e.target === dialog) {
      dialog.close();
      openBtn.focus();
    }
  });
</script>
```

### B. Keyboard-First Command Palette (`Cmd/Ctrl+K`)

```html
<dialog id="cmd-palette" class="palette-dialog" aria-modal="true" aria-label="Command Palette">
  <div class="palette-bar">
    <input id="cmd-input" type="text" role="combobox" aria-expanded="true" aria-controls="cmd-list" aria-autocomplete="list" placeholder="Type a command...">
    <kbd>ESC</kbd>
  </div>
  <ul id="cmd-list" role="listbox">
    <li id="opt-1" role="option" aria-selected="true" class="cmd-item active">Deploy to Staging</li>
    <li id="opt-2" role="option" aria-selected="false" class="cmd-item">Export Telemetry</li>
    <li id="opt-3" role="option" aria-selected="false" class="cmd-item">Rotate API Keys</li>
  </ul>
</dialog>

<script>
  const palette = document.getElementById('cmd-palette');
  const cmdInput = document.getElementById('cmd-input');
  const items = Array.from(document.querySelectorAll('.cmd-item'));
  let activeIndex = 0;

  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      palette.open ? palette.close() : palette.showModal();
    }
    if (!palette.open) return;

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      activeIndex = (activeIndex + 1) % items.length;
      updateActiveItem();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      activeIndex = (activeIndex - 1 + items.length) % items.length;
      updateActiveItem();
    }
  });

  function updateActiveItem() {
    items.forEach((item, i) => {
      const isSelected = i === activeIndex;
      item.classList.toggle('active', isSelected);
      item.setAttribute('aria-selected', isSelected);
      if (isSelected) {
        cmdInput.setAttribute('aria-activedescendant', item.id);
        item.scrollIntoView({ block: 'nearest' });
      }
    });
  }
</script>
```

### C. 5-State Button Primitive (WCAG 2.2 AA Compliant)

```css
.btn-core {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 36px;
  min-width: 44px; /* WCAG 2.2 minimum tap boundary */
  padding: 0 14px;
  font-size: 13px;
  font-weight: 500;
  border-radius: var(--radius-control, 6px);
  border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.08));
  background: var(--surface-elevated, #14161a);
  color: var(--text-primary, #f0f0f0);
  cursor: pointer;
  user-select: none;
  transition: background 120ms ease, border-color 120ms ease, transform 80ms ease;
}

/* 1. Hover */
.btn-core:hover:not(:disabled) {
  background: var(--surface-active, #1a1d22);
  border-color: var(--border-strong, rgba(255, 255, 255, 0.16));
}

/* 2. Active (Physical depression) */
.btn-core:active:not(:disabled) {
  transform: scale(0.98);
}

/* 3. Focus-Visible (WCAG 2.2 3:1 contrast focus ring) */
.btn-core:focus-visible {
  outline: 2px solid var(--accent-indigo, #5e6ad2);
  outline-offset: 2px;
}

/* 4. Disabled */
.btn-core:disabled {
  opacity: 0.45;
  cursor: not-allowed;
  pointer-events: none;
}
```

### D. Toast Notification Primitive

```html
<div id="toast-region" class="toast-stack" role="region" aria-label="Notifications"></div>

<script>
  function triggerToast(message, duration = 3000) {
    const stack = document.getElementById('toast-region');
    const toast = document.createElement('div');
    toast.className = 'toast-alert';
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    toast.textContent = message;

    stack.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(4px)';
      setTimeout(() => toast.remove(), 180);
    }, duration);
  }
</script>

<style>
  .toast-stack {
    position: fixed;
    bottom: 24px;
    right: 24px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    z-index: 9999;
  }
  .toast-alert {
    background: var(--surface-elevated, #14161a);
    border: 1px solid var(--border-strong, rgba(255, 255, 255, 0.14));
    border-radius: 6px;
    padding: 10px 16px;
    font-size: 12px;
    color: var(--text-primary, #f0f0f0);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
    transition: opacity 180ms ease, transform 180ms ease;
  }
</style>
```
