# Contributing

Thanks for improving Turtleneck. The whole point of the repo is that its rules are mechanically
enforced, so contributions are cheap to check — run the gates, and if any of them fail, the drift
is *your* starting point, not your reviewer's.

## Environment

```bash
python -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
```

Everything a user *runs* (the installer, all three gates) is Python standard library only.
`pytest` is a dev-only dependency; the Playwright scrapers are a maintainer-only capture
regeneration path.

## The gates you must keep green

```bash
.venv/bin/pytest tests/ -q
python scripts/check_consistency.py
python scripts/check_contrast.py
python scripts/check_examples.py
```

CI runs the same four commands on Python 3.11 and 3.12.

## Drift-proofs to respect

* **Change a colour token?** Update the matching pair in `scripts/check_contrast.py` — it fails if
  the docs and the gate disagree.
* **Add a reference doc?** Link it from `SKILL.md`, or `check_consistency.py` flags it as orphaned.
  Docs that must be reachable by installed rules are also listed in the load-on-demand tables in
  `rules/AGENTS.md` and `rules/CLAUDE.md`.
* **Add an example?** Wire it into `SKILL.md`'s reference table, or the gate calls it out.
* **Touch the pipeline?** The exact line
  `1. Workspace Analysis ──► … ──► 4. Production Build` must stay identical in `README.md`,
  `SKILL.md` and every file under `rules/`.

## The installer's safety contract

Any change to `scripts/install.py` must keep this true:

1. **No foreign user file may be modified or deleted by default.** A destination holding content
   Turtleneck does not own is refused, with the protected path reported.
2. **Every destructive path requires an explicit opt-in and creates a recoverable backup.**
   `--force` writes a numbered `.turtleneck.bak` (rule files) or snapshots the whole skill tree;
   a backup suffix is never overwritten.
3. **Skill and rule installs obey the same ownership model.** Skill ownership is proven by a
   schema-versioned manifest (`turtleneck-skill-manifest.json`) with per-file SHA-256 hashes; a
   tampered or missing manifest never grants ownership.
4. **Uninstall removes only manifest-owned files** whose content still matches the recorded hash,
   restores the appropriate backup without overwriting foreign survivors, and never deletes
   foreign additions.

Before opening a PR, make the gates pass; the reviewer will run them anyway, and so will CI.

## Release process

* Update `CHANGELOG.md` under `## Unreleased` as you work.
* Bump the documentation where test counts, token counts, or supported surfaces change
  (`README.md` states the declared pair count and the test count).
* Maintainers tag releases locally with `git tag`; do not push tags/tools to GitHub from an
  external agent workflow.
