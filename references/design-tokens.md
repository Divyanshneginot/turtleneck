# Design Tokens Reference

Token specifications for building systematic, scalable user interfaces.

---

## 1. Spacing System (8pt Grid with 4pt Half-Steps)

Use powers of 8 for layout, containers, and margins. Use 4pt half-steps only for tight component internals (badges, compact inputs, icon offsets).

| Token | Size | Common Application |
| :--- | :--- | :--- |
| `space-0.5` | `2px` | Borders, subtle divider offsets |
| `space-1` | `4px` | Badge padding, icon micro-spacing |
| `space-2` | `8px` | Button inline padding (compact), input internal gap |
| `space-3` | `12px` | Standard button padding-y, card internal spacing (compact) |
| `space-4` | `16px` | Standard container padding, form field vertical gap |
| `space-5` | `20px` | Medium card padding, stack gaps |
| `space-6` | `24px` | Section sub-headings, modal margins |
| `space-8` | `32px` | Page section margins, card groupings |
| `space-10` | `40px` | Feature blocks, hero section offsets |
| `space-12` | `48px` | Large hero spacing, viewport boundaries |
| `space-16` | `64px` | Full page section breaks |

---

## 2. Typography Scale (Major Third - 1.25 Ratio)

Default body size: `16px` (`1rem`). Default base line-height: `1.5` for body, `1.2` - `1.25` for display headings.

| Token | Font Size | Line Height | Tracking | Recommended Use |
| :--- | :--- | :--- | :--- | :--- |
| `text-xs` | `11px` (`0.6875rem`) | `16px` | `+0.02em` | Legal text, tiny badges |
| `text-sm` | `13px` (`0.8125rem`) | `20px` | `+0.01em` | Captions, secondary labels, table cells |
| `text-base`| `16px` (`1.000rem`) | `24px` | `0` | Default body copy, form inputs |
| `text-lg` | `20px` (`1.250rem`) | `28px` | `-0.01em` | Subsection titles, modal headers |
| `text-xl` | `25px` (`1.563rem`) | `32px` | `-0.015em`| Section headers, H3 |
| `text-2xl`| `31px` (`1.953rem`) | `38px` | `-0.02em` | Page headers, H2 |
| `text-3xl`| `39px` (`2.441rem`) | `46px` | `-0.025em`| Primary view titles, H1 |
| `text-4xl`| `49px` (`3.052rem`) | `56px` | `-0.03em` | Hero displays |

---

## 3. Semantic Color Role Mapping

Never hardcode arbitrary hex values into component files. Always map tokens to functional roles.

| Role Token | Purpose | Light Theme Reference | Dark Theme Reference |
| :--- | :--- | :--- | :--- |
| `bg-canvas` | Main application background | `#FFFFFF` or `#F8FAFC` | `#090D16` |
| `bg-surface` | Card, container, and modal fill | `#FFFFFF` | `#111827` |
| `bg-surface-elevated` | Popovers, tooltips, dropdowns | `#FFFFFF` (with shadow) | `#1F2937` |
| `text-primary` | Main titles and high-priority copy | `#0F172A` | `#F9FAFB` |
| `text-secondary` | Descriptive paragraphs, subtitles | `#475569` | `#9CA3AF` |
| `text-muted` | Placeholder text, inactive hints | `#637896` | `#737A89` |
| `border-subtle` | Card borders, dividers *(decorative — see note below)* | `#E2E8F0` | `#1F2937` |
| `border-strong` | Active input borders, key dividers *(UI boundary)* | `#7F97B5` | `#56657E` |
| `action-primary` | Primary buttons, active tabs | `#2563EB` | `#3B82F6` |
| `action-primary-hover`| Hover state for primary action | `#1D4ED8` | `#60A5FA` |
| `on-action-primary` | Foreground on primary buttons | `#FFFFFF` | `#090D16` |
| `status-success`| Positive indicators, confirmations | `#16A34A` | `#22C55E` |
| `status-warning`| Caution alerts, intermediate status | `#D97706` | `#F59E0B` |
| `status-danger` | Errors, destructive actions | `#DC2626` | `#EF4444` |

### 3.1 Contrast Compliance Notes (WCAG 2.2 AA)

Every pair above is verified by `scripts/check_contrast.py`. Read these before substituting values:

* **`text-*` tokens are held at >= 4.5:1** against `bg-canvas` in both themes. The previous
  `text-muted` values (`#94A3B8` light at 2.56:1, `#6B7280` dark at 4.02:1) failed AA and were
  replaced with `#637896` (4.51:1) and `#737A89` (4.51:1) at identical hue.
* **`border-strong` is a UI component boundary** (WCAG 1.4.11) and is therefore held at >= 3:1:
  `#7F97B5` light (3.00:1 on `#FFFFFF`), `#56657E` dark (3.01:1 on `#111827`, 3.29:1 on `#090D16`).
  The previous `#CBD5E1` / `#374151` measured 1.48:1 and 1.72:1.
* **`border-subtle` is decorative and exempt from WCAG 1.4.11.** It renders card edges and
  section dividers, which are not interactive components. It MUST NOT be the only indicator of
  a component boundary, a focus ring, or a selected/active state. If you need a boundary the
  user must perceive, use `border-strong`.
* **Dark-theme primary buttons use dark ink, not white.** `#3B82F6` and its hover `#60A5FA` are
  light fills: white text on them measures only 3.68:1 and 2.54:1. Always render
  `on-action-primary` (`#090D16`) on dark-theme primary buttons — 5.28:1 and 7.64:1 respectively.

---

## 4. Elevation & Shadows

Use elevation to convey z-axis hierarchy rather than heavy borders.

```css
/* Elevation 1: Subtle cards, inputs */
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);

/* Elevation 2: Interactive cards on hover, popovers */
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);

/* Elevation 3: Modals, slide-overs, dialogs */
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);

/* Elevation 4: Floating toasts, system menus */
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
```
