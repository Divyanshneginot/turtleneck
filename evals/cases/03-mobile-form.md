# Case 03: Mobile Form

## User Brief
"Design and implement a mobile-first 3-step checkout form in Vue 3 for a boutique coffee roaster. Users enter shipping, select grind type, and submit payment."

## Classification
- **Expected Trigger**: Trigger
- **Expected Mode**: `Full Pipeline` or `Fast Path`
- **Domain Context**: E-commerce, mobile physical ergonomics, artisanal physical goods.

## Behavioral Expectations
1. **Subject Matter Derivation**:
   - Grounds aesthetic in coffee domain (warm paper, rich natural accents, tactile physical feel) rather than sterile dark tech aesthetic.
   - Applies Warm Editorial Paper or Fluid Organics constraint lens.
2. **Mobile Ergonomics**:
   - Physical tap targets >= 44x44px across all buttons, radio pills, and input steppers.
   - Bottom-sheet or thumb-zone layout for primary actions (`mobile-touch-and-native.md`).
   - Appropriate HTML input semantics (`type="email"`, `type="tel"`, `autocomplete`).
3. **Form Accessibility**:
   - Explicit `<label>` association with form controls.
   - Inline error states with icons/text, never color alone.
   - Step progress indicator with clear active/completed semantics (`aria-current="step"`).
4. **Output Contract**:
   - Emits contract verifying tap targets and text contrast.

## Negative Markers (Failure Modes)
- Defaulting to pitch-black high-density starlight for a warm coffee roastery.
- Tap targets under 44px on mobile viewport.
- Inputs missing accessible names or visible labels.
- Layout breaking or horizontal scrolling on 320px viewport.
