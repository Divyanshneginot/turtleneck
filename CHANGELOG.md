# Changelog

All notable changes to Turtleneck are documented here.

## Unreleased

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
