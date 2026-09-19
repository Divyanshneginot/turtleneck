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

## 4. Editorial-Engineering Contrast Recipe

Balances high-craft editorial titles with sharp technical controls:
* **Display Headline**: Editorial serif (`Newsreader`, `Georgia`, `serif`) with `letter-spacing: -0.03em`.
* **Interface & Data**: Clean technical mono (`ui-monospace`, `CommitMono`, `monospace`) paired with strict 8px rounded cards.
* **Payload Viewer**: Deep slate console (`#0d0f12`) with syntax highlights matching token roles.

---

## 5. Warm Editorial Paper Surface & Cadence (Warm Light)

Synthesized from world-class editorial publishing layouts:

```css
/* Warm Paper Canvas & Ink Dividers */
.editorial-canvas {
  background-color: #fbfbfa;
  color: #201f1d;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.6;
}

.editorial-header {
  font-family: "Newsreader", "Georgia", serif;
  font-size: clamp(2.5rem, 5vw, 4.5rem);
  font-weight: 400;
  line-height: 1.05;
  letter-spacing: -0.03em;
  color: #121110;
}

.editorial-card {
  background: #ffffff;
  border: 1px solid #e9e9e8;
  border-radius: 4px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.editorial-divider {
  height: 1px;
  background: #e9e9e8;
  margin: 32px 0;
}
```

---

## 6. Expressive Identity & Asymmetric Grid Cadence

Synthesized from award-winning studio portfolios with kinetic visual tension:

```css
/* Asymmetric 12-column kinetic container */
.asymmetric-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 24px;
}

.asymmetric-col-primary {
  grid-column: span 7;
}

.asymmetric-col-secondary {
  grid-column: span 5;
  margin-top: clamp(24px, 4vw, 64px); /* Staggered spatial breathing */
}

/* Kinetic scale on hover with hardware isolation */
.kinetic-card {
  transition: transform 180ms cubic-bezier(0.16, 1, 0.3, 1), box-shadow 180ms ease;
  will-change: transform;
}

.kinetic-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px -4px rgba(0, 0, 0, 0.12);
}
```

---

## 7. Native Platform Minimalism (Zero Dependencies)

Pure browser capabilities without utility framework bloat:

```css
/* Fluid responsive typography with pure clamp() */
h1.fluid-title {
  font-size: clamp(2rem, 1.2rem + 3.2vw, 4.2rem);
  line-height: 1.05;
  letter-spacing: -0.03em;
  text-wrap: balance;
}

/* Container query responsive cards */
@container (min-width: 480px) {
  .responsive-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
}

/* Hardware-accelerated modal dialog */
dialog::backdrop {
  background: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(8px);
}
```
