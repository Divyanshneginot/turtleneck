# Modern Frontend Framework Integration Recipes

Concrete, copy-pasteable patterns for integrating the 5 design archetypes and anti-slop principles into React, Next.js, Vue, Svelte, and Tailwind CSS.

---

## 1. Tailwind CSS (v3 / v4) Universal Theme Configuration

Maps the 5 design archetypes into semantic Tailwind utility tokens via CSS Custom Properties.

```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ['class', '[data-archetype="starlight"]'],
  content: ['./src/**/*.{js,ts,jsx,tsx,vue,svelte,html}'],
  theme: {
    extend: {
      colors: {
        canvas: 'var(--canvas)',
        surface: {
          DEFAULT: 'var(--surface)',
          elevated: 'var(--surface-elevated)',
          active: 'var(--surface-active)',
        },
        border: {
          subtle: 'var(--border-subtle)',
          window: 'var(--border-window)',
          strong: 'var(--border-strong)',
        },
        content: {
          primary: 'var(--text-primary)',
          secondary: 'var(--text-secondary)',
          muted: 'var(--text-muted)',
        },
        accent: {
          DEFAULT: 'var(--accent-indigo)',
          hover: 'var(--accent-indigo-hover)',
        },
      },
      borderRadius: {
        window: 'var(--radius-window, 8px)',
        control: 'var(--radius-control, 6px)',
        badge: 'var(--radius-badge, 4px)',
      },
      fontFamily: {
        sans: ['var(--font-sans)', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        mono: ['var(--font-mono)', 'ui-monospace', 'monospace'],
        serif: ['var(--font-serif)', 'Georgia', 'serif'],
      },
      boxShadow: {
        specular: 'var(--shadow-specular)',
      },
      transitionTimingFunction: {
        tactile: 'cubic-bezier(0.16, 1, 0.3, 1)',
      },
      transitionDuration: {
        tactile: '120ms',
      },
    },
  },
  plugins: [],
};
```

---

## 2. React / Next.js (TypeScript)

### A. 5-State Accessible Button Primitive

```tsx
import React, { forwardRef } from 'react';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'destructive';
  size?: 'sm' | 'md' | 'lg';
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'primary', size = 'md', className = '', children, disabled, ...props }, ref) => {
    const baseStyles =
      'inline-flex items-center justify-center font-medium select-none cursor-pointer ' +
      'transition-all duration-tactile ease-tactile ' +
      'active:scale-[0.98] ' +
      'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-canvas ' +
      'disabled:opacity-40 disabled:pointer-events-none disabled:cursor-not-allowed';

    const sizeStyles = {
      sm: 'h-8 min-w-[32px] px-2.5 text-xs rounded-badge gap-1.5',
      md: 'h-9 min-w-[44px] px-3.5 text-sm rounded-control gap-2', // 44px touch target boundary
      lg: 'h-11 min-w-[44px] px-5 text-base rounded-control gap-2.5',
    };

    const variantStyles = {
      primary: 'bg-accent text-white hover:bg-accent-hover shadow-specular border border-transparent',
      secondary: 'bg-surface-elevated text-content-primary border border-border-strong hover:bg-surface-active',
      ghost: 'bg-transparent text-content-secondary hover:text-content-primary hover:bg-surface-active',
      destructive: 'bg-rose-600 text-white hover:bg-rose-700 active:bg-rose-800',
    };

    return (
      <button
        ref={ref}
        disabled={disabled}
        className={`${baseStyles} ${sizeStyles[size]} ${variantStyles[variant]} ${className}`}
        {...props}
      >
        {children}
      </button>
    );
  }
);
Button.displayName = 'Button';
```

### B. Keyboard-First Command Palette (Native `<dialog>` React Hook)

```tsx
import React, { useEffect, useRef, useState } from 'react';

export interface CommandItem {
  id: string;
  label: string;
  shortcut?: string;
  onSelect: () => void;
}

export function CommandPalette({ items }: { items: CommandItem[] }) {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState('');
  const [activeIndex, setActiveIndex] = useState(0);
  const dialogRef = useRef<HTMLDialogElement>(null);

  const filtered = items.filter((i) => i.label.toLowerCase().includes(search.toLowerCase()));

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setOpen((prev) => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (open) {
      dialog.showModal();
      setActiveIndex(0);
    } else {
      dialog.close();
      setSearch('');
    }
  }, [open]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setActiveIndex((prev) => (prev + 1) % filtered.length);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setActiveIndex((prev) => (prev - 1 + filtered.length) % filtered.length);
    } else if (e.key === 'Enter' && filtered[activeIndex]) {
      e.preventDefault();
      filtered[activeIndex].onSelect();
      setOpen(false);
    } else if (e.key === 'Escape') {
      setOpen(false);
    }
  };

  return (
    <dialog
      ref={dialogRef}
      onKeyDown={handleKeyDown}
      onClick={(e) => e.target === dialogRef.current && setOpen(false)}
      className="backdrop:bg-black/60 backdrop:backdrop-blur-sm bg-surface-elevated text-content-primary border border-border-strong rounded-window shadow-2xl p-0 w-full max-w-lg overflow-hidden m-auto"
    >
      <div className="flex items-center px-4 border-b border-border-subtle h-12 gap-3">
        <span className="text-accent text-sm">❯</span>
        <input
          autoFocus
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setActiveIndex(0);
          }}
          placeholder="Type a command or search..."
          className="bg-transparent text-sm w-full outline-none text-content-primary placeholder:text-content-muted"
        />
        <kbd className="text-[10px] font-mono text-content-muted px-1.5 py-0.5 border border-border-subtle rounded">
          ESC
        </kbd>
      </div>
      <ul className="max-h-64 overflow-y-auto p-2" role="listbox">
        {filtered.map((item, idx) => (
          <li
            key={item.id}
            role="option"
            aria-selected={idx === activeIndex}
            onClick={() => {
              item.onSelect();
              setOpen(false);
            }}
            className={`flex items-center justify-between px-3 py-2 rounded-control text-xs font-mono cursor-pointer transition-colors ${
              idx === activeIndex ? 'bg-surface-active text-content-primary' : 'text-content-secondary'
            }`}
          >
            <span>{item.label}</span>
            {item.shortcut && <kbd className="text-[10px] text-content-muted">{item.shortcut}</kbd>}
          </li>
        ))}
      </ul>
    </dialog>
  );
}
```

---

## 3. Vue 3 (Composition API & `<script setup>`)

```vue
<!-- components/TactileButton.vue -->
<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(
  defineProps<{
    variant?: 'primary' | 'secondary' | 'ghost';
    size?: 'sm' | 'md' | 'lg';
    disabled?: boolean;
  }>(),
  {
    variant: 'primary',
    size: 'md',
    disabled: false,
  }
);

const classes = computed(() => {
  const base =
    'inline-flex items-center justify-center font-medium select-none cursor-pointer ' +
    'transition-all duration-tactile ease-tactile active:scale-[0.98] ' +
    'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent ' +
    'disabled:opacity-40 disabled:pointer-events-none';

  const sizes = {
    sm: 'h-8 px-2.5 text-xs rounded-badge',
    md: 'h-9 px-3.5 text-sm rounded-control',
    lg: 'h-11 px-5 text-base rounded-control',
  };

  const variants = {
    primary: 'bg-accent text-white hover:bg-accent-hover',
    secondary: 'bg-surface-elevated text-content-primary border border-border-strong hover:bg-surface-active',
    ghost: 'bg-transparent text-content-secondary hover:text-content-primary hover:bg-surface-active',
  };

  return `${base} ${sizes[props.size]} ${variants[props.variant]}`;
});
</script>

<template>
  <button :class="classes" :disabled="disabled">
    <slot />
  </button>
</template>
```

---

## 4. Svelte 5 (Runes)

```svelte
<!-- components/TactileButton.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';

  interface Props {
    variant?: 'primary' | 'secondary' | 'ghost';
    size?: 'sm' | 'md' | 'lg';
    disabled?: boolean;
    children?: Snippet;
    onclick?: (e: MouseEvent) => void;
  }

  let {
    variant = 'primary',
    size = 'md',
    disabled = false,
    children,
    onclick,
    ...rest
  }: Props = $props();

  const sizeClasses = {
    sm: 'h-8 px-2.5 text-xs rounded-badge',
    md: 'h-9 px-3.5 text-sm rounded-control',
    lg: 'h-11 px-5 text-base rounded-control',
  };

  const variantClasses = {
    primary: 'bg-accent text-white hover:bg-accent-hover',
    secondary: 'bg-surface-elevated text-content-primary border border-border-strong hover:bg-surface-active',
    ghost: 'bg-transparent text-content-secondary hover:text-content-primary hover:bg-surface-active',
  };
</script>

<button
  {disabled}
  {onclick}
  class="inline-flex items-center justify-center font-medium select-none cursor-pointer transition-all duration-tactile ease-tactile active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent disabled:opacity-40 disabled:pointer-events-none {sizeClasses[size]} {variantClasses[variant]}"
  {...rest}
>
  {@render children?.()}
</button>
```

---

## 5. Native Platform / Zero-Dependency Mode

When repository has no build step or framework (pure HTML/CSS/JS):
* Use CSS Custom Properties on `:root` or `body[data-archetype]`.
* Use native HTML `<dialog>` with `.showModal()`, native `<template>`, and standard DOM event listeners.
* Use `@container` queries and `clamp()` for responsive layout without CSS-in-JS or Tailwind.
