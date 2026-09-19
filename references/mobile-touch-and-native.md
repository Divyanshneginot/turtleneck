# Mobile, Touch & Native-App Ergonomics

Small screens and native apps are not the web shrunk down. This reference extends the base tokens
in `design-tokens.md` and the timing discipline in `master-ui-craft-benchmark.md` to thumb-first,
gesture-driven surfaces — and to the native stacks (`React Native`, `Flutter`, `SwiftUI`) that the
web-only rules do not cover.

---

## 1. Thumb zones, touch targets & safe areas

### Minimum tap targets

* **Web / cross-platform baseline**: `44×44px` (`44×44pt` on iOS).
* **Material (Android / Flutter)**: `48×48dp` — use this when the platform is Material.
* **Compact desktop controls** may drop to `24×24px` **only** with at least `8px` of surrounding
  non-interactive spacing (WCAG 2.5.8 target-size exception).
* **Expand hit areas invisibly**: a small icon-button keeps its visible glyph small while a padded
  `::after` / `padding + negative margin` / `hitSlop` region grows the touchable area — the tap
  target, not the glyph, is what must clear `44px`.

### 8px separation

Keep at least `8px` of spacing between adjacent interactive elements so overlapping/adjacent hit
areas never cause mis-taps (WCAG 2.5.5 / 2.5.8).

### Thumb-zone layout (one-handed phones)

* **Primary actions** go in the **bottom `¼` of the screen** (the thumb's natural reach). Persist
  the most frequent action as a bottom-right floating action / docked bar.
* **Destructive actions** (delete, sign-out) go **away from the thumb's rest position** — top
  corners or behind explicit confirmation — never bottom-center where a natural flick triggers them.
* **Navigation** lives on the **bottom edge** when a tab bar exists; never force users to reach the
  top-left on a phone.
* **In-screen back affordances** must duplicate the system gesture; never rely on the OS back
  gesture alone when the platform has none.

### Safe areas & system chrome

* Respect `env(safe-area-inset-*)` (web/React Native) or `SafeArea` / `.ignoresSafeArea()` /
  `WindowInsets` (Flutter / SwiftUI) for notches, home indicators, and dynamic-island overlays.
* Never pin critical controls inside a safe-area inset region. Add `scroll-margin-top` (web) or
  keyboard-avoidance (native) so fixed chrome and on-screen keyboards do not obscure focused
  fields.

---

## 2. Gesture & interaction timing

### Feedback budget (input → visible response)

| Interaction | Budget |
| :--- | :--- |
| Press / toggle / checkbox | `< 100ms` (aim `80–120ms` per the base craft rules) |
| Tap ripple / highlight down | trigger on pointer-down, settle `120ms` |
| Sheet / modal enter | `200–240ms` |
| Full screen / route transition | `300–360ms` |
| Sheet / modal exit | `100–140ms` (asymmetric exit rule: 30–50% faster than entrance) |

### Pointer cancellation & gesture ownership

* Actions commit on pointer-up / release (`mouseup`, `touchend`, or the framework's
  `onPress`/`onTap`), not on pointer-down — so a user can slide off a control to cancel (WCAG 2.5.2).
* Swipe gestures must not fight native navigation: horizontal edge swipes belong to the system;
  claim them only with good reason and an explicit escape.
* Support tap as the accessible alternative to every gesture — a swipe-only action is an
  accessibility failure unless an equivalent button exists.

### Motion on mobile

* Swipe/scroll-linked animation must remain `transform`/`opacity` only (never layout properties,
  never `transition: all`), and must be cancellable mid-gesture.
* Golden rule for gesture velocity mapping: distanced moved ≈ `1:1` with the finger during drag,
  decelerating quietly after release (damping ratio `zeta >= 0.85`). No underdamped bounce in
  utility UI.
* Always honor `prefers-reduced-motion: reduce` (web) and the OS reduce-motion setting (native:
  `UIAccessibility.isReduceMotionEnabled`, `reduce motion` in Flutter, `@Environment(\.accessibilityReduceMotion)` in SwiftUI).

---

## 3. Native stack mapping

When the target is a native or cross-platform app, map the protocol onto the platform's idioms:
do not hand-roll web patterns where the platform has a native primitive.

| Turtleneck concern | React Native | Flutter | SwiftUI |
| :--- | :--- | :--- | :--- |
| 5-state controls | `Pressable` with `pressed`/`disabled` styles + `focus` via tvOS/`useFocusState` | `MaterialStateProperty` set on `ElevatedButton` / `InkWell` (hover, pressed, focused, disabled) | `ButtonStyle`/`PrimitiveButtonStyle` with `isPressed`, `isFocused`, `disabled` environment |
| Focus-visible ring | focus ring on web builds / AppleTV `useFocusState` | `focusNode` + `FocusHighlightMode` / `Focus` widget | `@FocusState` + `.focusable()` |
| Reduced motion | `useReducedMotion()` + `AccessibilityInfo.isReduceMotionEnabled` | `MediaQuery.disableAnimationsOf(context)` | `@Environment(\.accessibilityReduceMotion)` |
| Semantic surface | `react-native-reanimated`, `RN StyleSheet`, `accessibilityLabel`/`accessibilityRole` | `ThemeData`, `ThemeExtension`, `Semantics` widget | `Color(hex)` → semantic extension on `ShapeStyle`, `accessibilityLabel` |
| Tap targets | `44×44pt`, `hitSlop` for small icons | `48×48dp`, `kMinInteractiveDimension`, `IconButton` fills | `44×44pt` (Apple HIG), `.contentShape()` expands the hit area |
| Modal focus trap | native sheets/modals + `onRequestClose` for Android back | `showModalBottomSheet` / `showDialog` | `.sheet` / `.alert` (system manages trap + restore) |
| Safe areas | `SafeAreaView` / `useSafeAreaInsets` | `SafeArea` (`MediaQuery.viewPaddingOf`) | `.ignoresSafeArea` only where intended |
| Tokens | RN StyleSheet constants or a `useTheme()` hook fed by the archetype tokens | `ThemeData` + `ThemeExtension` (type-safe token access) | custom `ShapeStyle`/`EnvironmentKey` values |

### Common native failures to avoid

* `TouchableOpacity` wrapping a full card (no dedicated 44px target, poor feedback).
* Hard-coded `#000000`/`#FFFFFF` instead of semantic tokens.
* White text on a light accent fill — reuse the `on-action-primary` rule from `design-tokens.md`.
* `alert('...')`-style native confirmation instead of a designed, focusable dialog.

---

## 4. Density on small screens

* Do not squeeze the desktop layout down: **re-flow, don't shrink**. One column, bottom-anchored
  actions, and a collapsed (hamburger→bottom-sheet) nav beat a 6-column table at 375px.
* Breakpoints in `dp/pt` when native, CSS `px` when web:
  * `360–414px` phones — single column, 44px rows.
  * `768–1024px` tablet / fold — two-pane master-detail.
  * `1024px+` desktop — the archetype's high-density layout reapplies.
* Touch-friendly row heights: list rows `48px` minimum; data tables on touch `56px` rows with
  horizontal scroll and sticky headers, never tiny tap rows on a phone.
* Readable typefloor: on phones keep body `16px`+ (`sp` on Android) to avoid iOS auto-zoom; only
  `text-sm`/`13px` where the density archetype explicitly calls for it and space permits.

---

## 5. Cross-check

Before declaring a mobile/native build done, confirm the non-negotiables from the base protocol
still hold on device:

* `:focus-visible` / focus-ring equivalent on every interactive element (web) or focusable
  (native).
* Tap targets `44px` (web/iOS) / `48dp` (Material) with `8px` separation.
* Actions commit on release, not press; every gesture has a tap equivalent.
* Reduced-motion honored in code, not just on responsive web.
* No colour-as-only-cue; pair status with text, icon, or pattern.
* Every colour pair introduced on device verified with `scripts/check_contrast.py` (or the same
  WCAG 2.2 AA math by hand when the script can't target generated markup) before claiming AA.
