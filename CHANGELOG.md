# Changelog

All notable changes to Turtleneck are documented here.

## Unreleased

### Fixed — skill installation now obeys the same safety contract as rule installation

`--claude-skill` / `--antigravity` previously backed up an existing skill directory exactly once
and then overwrote matching files with no ownership detection, no `--force`, and no numbered
backups. Skill installs now follow the same refuse-by-default contract as rule files:

* **Manifest ownership.** Every skill install writes a schema-versioned
  `turtleneck-skill-manifest.json` recording the SHA-256 of each shipped relative path. A skill
  directory is Turtleneck-owned only when the manifest proves it; a tampered or missing manifest
  never grants ownership.
* **Foreign or mixed content is refused** by default, with the exact protected paths listed.
* **`--force`** snapshots the whole directory to a collision-safe numbered `.turtleneck.bak`
  (never overwriting an existing backup) before replacing it.
* **`--dry-run`** parity for skill installs and skill uninstalls.
* **Upgrade reconciliation.** Stale files the previous manifest still owned are removed on
  upgrade instead of being left as orphans; the manifest is rewritten each install.
* **`uninstall_skill()`** removes only manifest-owned files whose content still matches the
  recorded hash, restores foreign files previously kept in a forced backup, and never deletes or
  overwrites a foreign addition.
* **Knowledge base installs (`install_references`) are now refuse-by-default too** for files that
  differ from the shipped copy, with `--force` + backup as the escape hatch.

### Fixed — Windows compatibility (manifest paths + test encodings)

* **Skill manifest paths are now always forward-slash POSIX relative paths** (`Path.as_posix()`).
  The previous `f"{sub}/{src.relative_to(base)}"` produced backslash separators on Windows,
  breaking manifest-key matching and causing false "foreign content" refusals and missed
  stale-file reconciliation during skill installs/uninstalls.
* **Tests pin `encoding="utf-8"` on every file read/write.** On Windows, bare
  `Path.read_text()`/`write_text()` default to the locale code page (cp1252), which threw
  `UnicodeDecodeError`s whenever the installer (correctly UTF-8) round-tripped rules files.
  The installer itself already pinned UTF-8 everywhere; only the tests were unpinned.

### Added — fast path, verification scope, and clearer guarantees

* **Fast path.** `SKILL.md`, `README.md`, and all six rules files now exempt an explicit brief
  (archetype + surface + density + layout direction) from the multi-question interview: restate
  the inferred constraints in one preflight, raise at most one genuine ambiguity, then build.
* **Execution modes (tempo).** `SKILL.md`, `README.md`, the interview framework, and every rules
  file now define four modes — direct Phase 4 (small fixes), time-boxed fast path (deadlines),
  fast path (explicit briefs), and the full pipeline (vague/consequential) — and require the
  Output Contract to record which mode ran and why the interview was skipped when it was. This
  closes the "full interview on a two-minute fix" friction: a full interview on a small change is
  now explicitly a protocol violation.
* **Mobile & native ergonomics.** New `references/mobile-touch-and-native.md`: thumb zones,
  safe-area insets, `44px`/`48dp` tap targets, pointer-cancellation, gesture timing budgets, the
  tap-equivalent-for-every-gesture rule, and a React Native / Flutter / SwiftUI token + 5-state
  mapping. Wired into `SKILL.md`, `README.md`, and all six rules files; the compatibility table
  now names the native stacks.
* **`references/verification-scope.md`** states plainly what each gate verifies and what it does
  not, and documents that passing a token/example gate does not certify an arbitrary product UI
  as WCAG 2.2 AA compliant. `SKILL.md`, `README.md`, `rules/AGENTS.md` and `rules/CLAUDE.md`
  point at it.
* **`CONTRIBUTING.md`** records the gate checklist, the drift-proofs, the installer safety
  contract, and the local release process.
* **Compatibility table** in `README.md` (Python 3.9+ runtime, dev/CI versions).

### Fixed — removed claims the checks could not back

* The example checker is regex-based and the contrast gate is limited to declared pairs. Docs no
  longer imply that these certify an arbitrary generated UI; the Output Contract now requires an
  agent to claim only what a specific check actually ran.

### Improved — the skill itself, not just its packaging

* **Triggering discipline.** `SKILL.md` now opens with a *When to use (and when not to)* section,
  so the skill stops over-firing on backend/CLI work, one-line tweaks, and pixel-perfect
  replication of a supplied design (where only the Phase 4 accessibility/motion rules apply).
* **Show, don't tell.** `SKILL.md` now links the three `examples/` as *reference
  implementations* — previously 2,553 lines of reference implementation were never referenced by
  any prompt file. Each is annotated with what it demonstrates (the 5-archetype workbench, a
  keyboard-first Starlight tracker, editorial/instrument craft).
* **Output Contract.** Every build must close with an auditable summary (archetype, stack,
  layout, density, tokens with verified contrast ratios, accessibility confirmations, files
  changed, deliberate breaks). Values marked "verified" must come from running the checks, not
  from assertion.
* **Skill installs now ship `examples/`** by default (the reference implementations `SKILL.md`
  links to). Only the ~2.9 MB of image captures remain opt-in via `--with-assets`.
* **Regression gate.** `scripts/check_consistency.py` now fails if any `examples/*.html` is not
  reachable from `SKILL.md`, so the skill can't drift back to telling without showing.

### Fixed — the installer no longer destroys user files

`AGENTS.md`, `CLAUDE.md` and `.github/copilot-instructions.md` are shared standards that a
project may already own. Previously a bare `python scripts/install.py` overwrote them with no
warning, no backup and no way to opt out.

* A destination holding foreign content is now **refused** by default. The protected file's first
  line is printed and the CLI exits `2`.
* `--force` replaces a file only after saving `<dest>.turtleneck.bak`. Repeat runs are numbered
  (`.turtleneck.bak.1`, `.2`, …) so no version is ever silently lost.
* `--append` merges Turtleneck between `<!-- turtleneck:begin -->` / `<!-- turtleneck:end -->`
  markers, leaving all surrounding content untouched. It is idempotent.
* `--dry-run` prints the plan and writes nothing.
* `--uninstall` removes marker blocks, restores backups, and deletes files only when it can prove
  Turtleneck owns them.
* `--antigravity` no longer calls `rmtree` on an existing install without keeping a copy.

### Added

* **`--claude-skill`** installs `SKILL.md` plus `references/` into
  `<project>/.claude/skills/turtleneck/`. Previously `SKILL.md` had no install path at all — the
  string "SKILL" did not appear anywhere in `install.py` — so Claude Code users received a
  20-line `CLAUDE.md` and never the skill. A skill-only install does not drop rules files.
* **Knowledge base now ships with rules installs.** Every rules install copies `references/` to
  `<project>/.turtleneck/references/`, because the rules files point agents there. Before this,
  installed rules contained zero links into `references/` and the ~37 KB craft knowledge base
  never reached Cursor, Windsurf, Copilot or Cline users. `--no-references` opts out.
* **`--cline`** target and `rules/.clinerules`, making the `install.py` docstring's Cline claim
  true. `.claude` and `.clinerules` are now part of auto-detection.
* **Three verification gates**, all standard-library only, all wired into CI:
  * `scripts/check_consistency.py` — pipeline parity across all 8 files, presence of the
    Requirements Interview step, resolution of every cited knowledge base path, no orphaned
    reference docs, no LaTeX in prompt markdown.
  * `scripts/check_contrast.py` — every declared colour pair against WCAG 2.2 AA, and it fails if
    the documentation drifts away from the values it verifies.
  * `scripts/check_examples.py` — `examples/` honour `:focus-visible`, `prefers-reduced-motion`,
    compositor-only transitions, accessible names, AA text contrast, and stay in sync with
    `references/design-archetypes.md`.
* `tests/` — 54 tests covering the installer safety contract and all three gates.
* `LICENSE` (MIT). The README claimed MIT but no licence file existed.
* `requirements-dev.txt`, `pytest.ini`, `.gitignore`, `.github/workflows/ci.yml`.

### Fixed — colour tokens that failed the skill's own WCAG rule

The skill instructed agents to enforce 4.5:1 text contrast while shipping tokens far below it.
19 of 44 declared pairs failed. Every text pair now clears 4.5:1 and every UI-boundary pair
clears 3:1, with hues preserved exactly.

| Token | Was | Now |
| :--- | :--- | :--- |
| `text-muted` (light) | `#94A3B8` — 2.56:1 | `#637896` — 4.51:1 |
| `text-muted` (dark) | `#6B7280` — 4.02:1 | `#737A89` — 4.51:1 |
| `border-strong` (light) | `#CBD5E1` — 1.48:1 | `#7F97B5` — 3.00:1 |
| `border-strong` (dark) | `#374151` — 1.72:1 | `#56657E` — 3.01:1 |
| Archetype 1 accent | `#635bff` — 4.45:1 | `#6259ff` — 4.52:1 |
| Archetype 1 muted | `#8898aa` — 2.79:1 | `#627489` — 4.54:1 |
| Archetype 2 accent | `#2383e2` — 3.74:1 | `#1b75cf` — 4.51:1 |
| Archetype 3 accent | `#007aff` — 4.02:1 | `#006be0` — 5.02:1 |
| Archetype 4 accent | `#5e6ad2` — 4.24:1 | `#636fd3` — 4.50:1 |

* Added an **`on-action-primary`** token. Dark-theme primary buttons are light fills, so white
  text on them measured only 3.68:1 (and 2.54:1 on hover); they now specify dark ink at 5.28:1.
* `border-subtle` is explicitly documented as **decorative and exempt from WCAG 1.4.11**, with a
  rule that it must never be the sole indicator of a boundary, focus ring, or state. The gate
  requires that annotation to be present, so a boundary cannot be silently downgraded.

### Fixed — examples that violated the skill's own rules

The three examples were the only executable proof in the repository, and they broke the protocol
they demonstrate.

* Added `:focus-visible` to all three. There were **zero** occurrences across 34 interactive
  elements and exactly one `:focus` rule in the whole `examples/` tree.
* Added a `@media (prefers-reduced-motion: reduce)` block to all three. There were none, despite
  three reference documents mandating one.
* Replaced all **7** `transition: all` declarations with explicit property lists.
* Added accessible names to the icon-only close button, the filter field, five checkboxes and the
  command palette input.
* Raised every `--text-muted` to 4.5:1, and re-synced all five archetype accents in
  `examples/index.html` with `references/design-archetypes.md`, from which they had drifted.
* Added a per-archetype `--focus-ring` token so the ring stays visible in the light archetypes.

### Changed

* **One canonical pipeline.** `README.md`, `SKILL.md` and all six rules files now state
  `Workspace Analysis → Requirements Interview → Blueprint Alignment → Production Build`. The
  three previously disagreed, and `rules/AGENTS.md` had dropped the Requirements Interview
  entirely — the headline feature the README advertises was absent from every shipped rules file.
* **Restored the Requirements Interview** to all six rules files with its JTBD and density steps.
* **No orphaned references.** All 15 documents in `references/` are now linked from the relevant
  phase in `SKILL.md`. Eight of them (53%, ~7,750 tokens) were previously unreachable, so
  progressive disclosure never surfaced them.
* **LaTeX removed from prompt markdown.** Agents do not render TeX; `$\ge 4.5:1$`,
  `$R_{\text{outer}} = R_{\text{inner}} + \text{Padding}$` and `$\zeta = \frac{c}{2\sqrt{km}}$`
  are now plain text. The gate keeps it that way.
* **Scraper contradiction resolved.** `SKILL.md` says not to run scrapers while the repository
  ships three Playwright tools the README advertised and nothing declared the dependency. They
  are now documented as a maintainer-only capture-regeneration path with pinned dev extras.
