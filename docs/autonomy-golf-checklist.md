# Autonomy Golf Checklist

Use this when the project already has autonomy golf installed and you just need to maintain it correctly.

## Before You Change Anything

1. Read [../CHANGELOG.md](../CHANGELOG.md) to see the current template and latest entry shape.
2. Read [autonomy-golf-agent.md](autonomy-golf-agent.md) if you need the fuller integration rules.
3. Confirm which subsystem the change belongs to.

## When You Make A Change

1. Write or update the change itself.
2. Decide which top-level provenance tier or tiers actually apply.
3. Keep directly derivative same-tier details nested under the main bullet.
4. Keep `Grounding` separate from provenance.

## When You Update The Changelog

1. Use a Linux-kernel-style header: `subsystem: summary`.
2. Add the bounded `score`.
3. Add `complexity` only when it differs from `score`.
4. Explain the change's meaning, motivation, and intended purpose.
5. Record:
   - files changed
   - checks run
   - measured effects, if any

## When You Validate

1. Prefer the strongest practical grounding the change deserves.
2. Record weaker grounding honestly if stronger validation is not practical.
3. Treat test coverage as one meaningful grounding dimension when automated tests are the right validation surface.

## When You Refresh Outputs

1. Run:

   ```bash
   python3 tools/changelog_scores.py --group-by entry --format csv --include-unreleased --verify
   ```

2. Then run:

   ```bash
   python3 tools/render_autonomy_badge.py
   ```

That refreshes both:

- `docs/autonomy-golf-badge.svg`
- the README snapshot block

## Definition Of Done

- changelog parses cleanly
- badge and README snapshot match the changelog
- provenance is conservative
- grounding is honest
