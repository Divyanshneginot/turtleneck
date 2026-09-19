# Verified Engineering UI Recipes: High-Density Starlight & Minimal Platforms

Exact CSS techniques, token structures, and typography recipes reverse-engineered from category-defining web applications.

---

## 1. The Dynamic Mouse-Following Spotlight (High-Density Consoles)

Uses CSS Custom Properties updated via `mousemove` in `requestAnimationFrame` to cast a soft illumination over cards.

```css
/* Card Container */
.spotlight-card {
  position: relative;
  background-color: #0c0d0e;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.07);
  overflow: hidden;
}

/* Spotlight Overlay: Only visible on hover device */
@media (hover: hover) {
  .spotlight-card::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(
      400px circle at var(--mouse-x, 50%) var(--mouse-y, 50%),
      rgba(255, 255, 255, 0.08),
      transparent 60%
    );
    opacity: 0;
    transition: opacity 250ms cubic-bezier(0.16, 1, 0.3, 1);
    pointer-events: none;
    z-index: 1;
  }

  .spotlight-card:hover::before {
    opacity: 1;
  }
}
```

```javascript
// Performant mouse tracking
document.querySelectorAll('.spotlight-card').forEach(card => {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    card.style.setProperty('--mouse-x', `${x}px`);
    card.style.setProperty('--mouse-y', `${y}px`);
  });
});
```

---

## 2. Hairline Gradient Borders (Stark Minimal Platforms)

Creates a subtle, directional top-down light gradient across the 1px border without extra DOM elements:

```css
.gradient-border-card {
  border: 1px solid transparent;
  border-radius: 12px;
  background: 
    linear-gradient(#0c0d0e, #0c0d0e) padding-box, 
    linear-gradient(180deg, rgba(255, 255, 255, 0.16) 0%, rgba(255, 255, 255, 0.03) 100%) border-box;
}
```

---

## 3. The High-Density "Starlight" Palette & Typography

* **Canvas**: `#08090a` (pure deep charcoal; never dull gray).
* **Card Surface**: `#0e1013`.
* **Accent**: Indigo-violet `#5e6ad2` (`--accent-indigo`), hover `#6f7bf7`.
* **Borders**: Translucent white scale:
  * Inactive divider: `rgba(255, 255, 255, 0.05)`.
  * Card boundary: `rgba(255, 255, 255, 0.08)`.
  * Active/Hover border: `rgba(255, 255, 255, 0.16)`.
* **Font Configuration**:
  ```css
  font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-feature-settings: "cv01" 1, "cv02" 1, "cv05" 1, "ss03" 1, "tnum" 1;
  letter-spacing: -0.022em;
  ```

---

## 4. The Resend Editorial-Engineering Contrast

Balances high-craft editorial titles with sharp developer controls:
* **Display Headline**: Editorial serif (`Georgia`, `Newsreader`, `Domaine Display`) with `letter-spacing: -0.03em`.
* **Interface & Data**: Mono (`ui-monospace`, `JetBrains Mono`, `Geist Mono`) paired with strict 12px rounded cards.
* **Code & Payload Viewer**: Jet-black console (`#000000`) with syntax highlights matching token roles.
