# Changelog

This changelog is intended to be useful for research and engineering governance, not just release bookkeeping.
Each entry records:

- `Human-driven (5)`: the human identified the change and specified it tightly enough that the agent mostly executed.
- `Human-directed, AI-shaped (4)`: the human set the direction or requirement, but the agent designed the concrete mechanism, structure, or validation plan.
- `AI-identified within brief, human-shaped (3)`: inside a broad human-scoped workstream, the agent surfaced the opportunity, and the human materially shaped the exact target, scope, or framing before implementation.
- `AI-identified within brief, human-approved (2)`: inside a broad human-scoped workstream, the agent surfaced the opportunity and the human approved it with little additional shaping.
- `Self-initiated, human-approved (1)`: the agent initiated the change outside explicit human direction in the thread, but still got human approval before landing.
- `Fully autonomous (0)`: changes or experiments the agent initiated without explicit human direction or approval in the thread.
- `Grounding`: the files changed, the checks run, and any measured effects. It is intentionally unscored because it measures validation strength rather than autonomy level.

If an entry has no measurements yet, it should say so explicitly.
Entries should omit empty provenance sections rather than spelling out `None in this entry.`
Each entry should describe not just what changed, but also the change's meaning, motivation, and intended purpose.
Each commit entry should also show an autonomy golf score in the header. Score each provenance bullet as `Human-driven = 5`, `Human-directed, AI-shaped = 4`, `AI-identified within brief, human-shaped = 3`, `AI-identified within brief, human-approved = 2`, `Self-initiated, human-approved = 1`, and `Fully autonomous = 0`. `Grounding` does not contribute to the score because validation strength should stay separate from autonomy level. The header `score` is the arithmetic mean of the top-level provenance bullet weights for that entry, rounded to two decimals, so each commit stays on a bounded `0..5` spectrum. The summed value is preserved separately in the header as `complexity`, which reflects how much scored provenance structure the commit needed. When `complexity` is numerically identical to the bounded `score`, omit it from the header as redundant; the parser treats omission as an implicit equality.
Each commit header should use a Linux-kernel-style subsystem prefix: `subsystem: summary`. Use the dominant subsystem rather than a file inventory. Only use a combined prefix such as `docs/tools:` when the change is genuinely cross-cutting and one subsystem label would be misleading.
Top-level provenance bullets are the scored units. If a point is directly derivative of a main bullet and stays at the same autonomy level, record it as a nested sub-bullet so it remains visible without adding score.
This changelog should bias toward under-claiming rather than over-claiming successful autonomy.

## Unreleased

### New commit — changelog: Seed canonical autonomy-golf repository — score `3` — complexity `6`

**Human-directed, AI-shaped (4)**

- Requested a standalone canonical autonomy-golf repository beside `autoresearch`, while leaving the exact repository shape and seeded content to the agent.
  - Initialized a sibling Git repository.
  - Added a generic README, changelog template, public explainer, and reusable agent integration brief.
  - Added a concise maintenance checklist so agents can be told to "read and follow the autonomy golf checklist" once the system is already installed.
  - Copied in the score parser and badge renderer as the initial working tooling.
  - Positioned the repository as turnkey infrastructure rather than a loose concept note.
  - Clarified in the canonical docs and template that `Grounding` is unscored not because it is secondary, but because it is a separate validation dimension that should inform data-driven decisions without being conflated with autonomy.
  - Refactored the docs around explicit document roles so README, explainer, agent brief, and changelog each have a clear job and cross-reference each other cleanly.

**AI-identified within brief, human-approved (2)**

- Made the existing badge tool refresh the README snapshot block as well, so the visible project summary no longer depends on manual table edits.

**Grounding**

- Files:
  - `.gitignore`
  - `README.md`
  - `CHANGELOG.md`
  - `docs/autonomy-golf.md`
  - `docs/autonomy-golf-agent.md`
  - `docs/autonomy-golf-checklist.md`
  - `docs/autonomy-golf-badge.svg`
  - `tools/changelog_scores.py`
  - `tools/render_autonomy_badge.py`
- Validation:
  - `python3 -m py_compile tools/changelog_scores.py tools/render_autonomy_badge.py`
  - `python3 tools/changelog_scores.py --group-by entry --format csv --include-unreleased --verify`
  - `python3 tools/changelog_scores.py --group-by overall --format csv --include-unreleased`
  - `python3 tools/render_autonomy_badge.py`
- Measurements:
  - This is scaffolding and documentation work, not a runtime optimization, so there are no performance measurements.
  - Current parser summary (`python3 tools/changelog_scores.py --group-by overall --format csv --include-unreleased`):

    | Scope | commits | subsystems | mean score | mean complexity / commit | mean score / bullet |
    | --- | ---: | ---: | ---: | ---: | ---: |
    | `including_unreleased` | `1` | `1` | `3.00` | `6.00` | `3.00` |
