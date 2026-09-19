# Workspace Scanner Guide

Protocol for discovering repository frontend stack, styling conventions, and existing UI tokens.

---

## 1. Automated Detection Matrix

| Target | Files to Inspect | Indicators & Insights |
| :--- | :--- | :--- |
| **Package & Engine** | `package.json`, `pnpm-lock.yaml`, `bun.lockb` | Detect dependencies: `next`, `react`, `vue`, `svelte`, `astro`, `vite`. |
| **Styling Solution** | `tailwind.config.*`, `globals.css`, `app.css` | Detect Tailwind v3/v4, CSS variables, theme extension (colors, radiuses). |
| **Component Libraries**| `package.json`, `components.json` | Detect `@radix-ui/*`, `shadcn/ui`, `lucide-react`, `chakra-ui`, `mui`. |
| **Routing / Views** | `src/app/`, `src/pages/`, `src/views/` | Detect App Router vs Pages Router vs SPA views. |
| **State & Data** | `src/store/`, `src/hooks/`, `src/api/` | Detect TanStack Query, Zustand, Redux, SWR, or direct fetch. |

---

## 2. Extraction Commands

Run these targeted commands when scanning a new workspace:

```bash
# 1. Inspect package dependencies
cat package.json | grep -E "react|next|vue|tailwind|radix|lucide|shadcn"

# 2. Check for existing components directory
find src -maxdepth 3 -type d -name "components" -o -name "ui"

# 3. Locate existing theme or token definitions
find . -maxdepth 2 -name "tailwind.config*" -o -name "*globals.css*" -o -name "*theme*"
```

---

## 3. Outputting the Workspace Profile

Summarize findings in 3 bullet points before initiating the requirements interview:
* **Detected Stack**: e.g., Next.js 14 App Router, Tailwind CSS v3.4, Lucide icons.
* **Component Patterns**: e.g., Shadcn-style primitives located in `@/components/ui/`.
* **Theme Tokens**: e.g., CSS variables defined in `globals.css` with dark mode class support.
