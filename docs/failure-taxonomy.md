# Turtleneck Failure Taxonomy

Catalogued from earlier development sessions.
Preserved as evidence for Phase C evaluation design.

---

## 1. Literal Reference Copying

**Pattern**: When told to draw inspiration from a reference site, the model copied its literal visual treatment instead of extracting transferable principles.

**Example**: Directed to emulate an engineering utility site's character → model produced dark terminal chrome, monospace fonts, and shell prompts on a design skill's landing page. The useful lesson (presentation expresses product character) was lost; the surface decoration was duplicated.

**Root cause**: Model treats "be inspired by X" as "reproduce X's CSS."

---

## 2. Irrelevant Centerpiece

**Pattern**: The landing page's hero section showcased a feature (seat-price billing calculator) unrelated to the skill's value proposition (design judgment).

**Example**: A billing/seat calculator as the primary interactive demo on a design intelligence skill page. Does not demonstrate that the skill makes better design decisions.

**Root cause**: Model filled the "interactive demo" slot with the most complex widget it could generate, regardless of product fit.

---

## 3. Incompatible Visual Rules

**Pattern**: The skill's own instructions contained competing mandates that the model couldn't satisfy simultaneously.

**Examples**:
- `creative-synthesis-protocol.md` requires 4+ orthogonal sources → other guidance warns against aesthetic collage
- 8 numbered mandates prescribe specific dark-mode tokens AND say "derive direction from task"
- "One archetype only" + "dramatic type ratios" + "Web Audio feedback" = a recipe, not a decision process

**Root cause**: Each mandate was locally reasonable but collectively they formed a contradictory checklist.

---

## 4. Cosmetic Compliance Over Product Proof

**Pattern**: Model treated design quality as a math exam — producing audit badges, score displays, and compliance chips instead of demonstrating actual design judgment.

**Examples**:
- `PASS/FAIL` visual audit chips rendered on the landing page
- `SFX: ON` and `8PT GRID` toggle gimmicks as decoration
- Server telemetry (`p99: 9.4ms`, `req/s`) on a design portfolio page

**Root cause**: Skill's verification emphasis was interpreted as "show the verification" rather than "do the verification."

---

## 5. Unsupported Verification Claims

**Pattern**: Broad claims not supported by actual gate scope.

**Examples**:
- "WCAG 2.2 AA Verified" badge — gates only check declared token pairs, not rendered DOM
- "SCALE TENSION: 4.8:1 (32px / 11px)" — arithmetic is wrong (32÷11 ≈ 2.91)
- GitHub links pointing to wrong repository

**Root cause**: Model generates plausible-sounding verification text without checking the math.

---

## 6. Repeated User Steering (Context Exhaustion)

**Pattern**: 600+ turns of user corrections, each converting a criticism into another universal prescription that created new failure modes.

**Cycle**: User says "this sucks" → model adds new mandate → mandate produces new failure → user says "this sucks" → ...

**Examples**:
- "Don't copy terminal" → model adds "use atelier workbench" → atelier becomes new template
- "Don't use server metrics" → model bans all technical data → even on server products
- "Commit to one world" → model adds "one archetype only" → settings screens get promotional aesthetics

**Root cause**: Long-context drift + each fix was additive (new rule) rather than structural (better decision process). Session should have been reset much earlier.
