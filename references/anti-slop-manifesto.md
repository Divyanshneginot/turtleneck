# Anti-Slop Design Manifesto & Quality Gate

Defines strict quality gates to ban AI-generated UI clichés and enforce authentic, high-utility product engineering.

---

## 1. Banned AI-Slop Tropes (Immediate Rejection Criteria)

Any design containing these elements fails validation:

* ❌ **Cosmic Nebula / Aurora Blobs**: Huge purple, pink, cyan radial blur blobs floating behind black cards.
* ❌ **Illegible Glassmorphism**: `backdrop-filter: blur(20px)` layered over glowing backdrops where text contrast drops below readable levels.
* ❌ **Hollow Buzzword Copy**: Meaningless marketing fillers like *"Unleash autonomous neural quantum synergy"*, *"10x your cognitive velocity"*, or *"Next-gen AI magic"*.
* ❌ **Decorative Bento Bloat**: Bento grids populated with fake 3D glass spheres, spinning rings, or useless filler cards with no user actions.
* ❌ **Scroll-Hijacking & Laggy Runtimes**: Heavy canvas particle engines, 5MB Three.js blobs, or delayed scroll transitions.

---

## 2. Real Engineering Design Standards (High Signal & Utility)

Every interface must be grounded in genuine workflow research:

* ✔ **Authentic Information Density**: High data-to-ink ratio. Prioritize real metrics, structured tables, actionable rows, and status indicators over empty space and decorative art.
* ✔ **Domain-Accurate Microcopy**: Write precise, operational text (e.g., *"Export 1,420 records to CSV (2.4MB)"* instead of *"Export with AI magic"*).
* ✔ **Sub-50ms Tactile Speed**: Instant keyboard responses, crisp transitions (under 120ms), native focus outlines, zero layout shifts.
* ✔ **Content-First Contrast**: True dark/light mode with rock-solid text contrast (minimum 7:1 for core data, 4.5:1 for secondary).
* ✔ **Keyboard Command Ergonomics**: Full keyboard navigability (`Tab`, `Esc`, `Cmd+K`, hotkeys) matching high-productivity tools like high-density trackers or terminal utilities.
