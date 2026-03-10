# Changelog

This changelog is intended to be useful for research and engineering governance, not just release bookkeeping.
Each entry records:

- `Fully human (6)`: the change was identified and authored by a human, with the agent absent or limited to review and minor revisions.
- `Human-driven (5)`: the human identified the change and specified it tightly enough that the agent mostly executed.
- `Human-directed, AI-shaped (4)`: the human set the direction or requirement, but the agent designed the concrete mechanism, structure, or validation plan.
- `AI-identified within brief, human-shaped (3)`: inside a broad human-scoped workstream, the agent surfaced the opportunity, and the human materially shaped the exact target, scope, or framing before implementation.
- `AI-identified within brief, human-approved (2)`: inside a broad human-scoped workstream, the agent surfaced the opportunity and the human approved it with little additional shaping.
- `Self-initiated, human-approved (1)`: the agent initiated the change outside explicit human direction in the thread, but still got human approval before landing.
- `Fully autonomous (0)`: changes or experiments the agent initiated without explicit human direction or approval in the thread.
- `Grounding`: the files changed, the checks run, and any measured effects. It is intentionally unscored because it measures validation strength rather than autonomy level.

This changelog should bias toward under-claiming rather than over-claiming successful autonomy.
Each entry should describe not just what changed, but also the change's meaning, motivation, and intended purpose.
A short nested `Meaning:`, `Motivation:`, `Purpose:` trio is a good default way to make that explicit when an entry would otherwise read like a file or task inventory.
Top-level provenance bullets are the scored units. If a point is directly derivative of a main bullet and stays at the same autonomy level, record it as a nested sub-bullet so it remains visible without adding score.
Each commit header should use a Linux-kernel-style subsystem prefix: `subsystem: summary`. Use the dominant subsystem rather than a file inventory. Only use a combined prefix such as `docs/tools:` when the change is genuinely cross-cutting and one subsystem label would be misleading.
Each commit entry should also show an autonomy golf score in the header. Score each provenance bullet as `Fully human = 6`, `Human-driven = 5`, `Human-directed, AI-shaped = 4`, `AI-identified within brief, human-shaped = 3`, `AI-identified within brief, human-approved = 2`, `Self-initiated, human-approved = 1`, and `Fully autonomous = 0`. `Grounding` does not contribute to the score because validation strength should stay separate from autonomy level. The header `score` is the arithmetic mean of the top-level provenance bullet weights for that entry, rounded to two decimals, so each commit stays on a bounded `0..6` spectrum. The summed value is preserved separately in the header as `complexity`, which now means top-level provenance weights plus `+1` for each nested sub-bullet under provenance items scored `3` or higher, excluding `Meaning:`, `Motivation:`, and `Purpose:` narrative lines. When `complexity` is numerically identical to the bounded `score`, omit it from the header as redundant; the parser treats omission as an implicit equality.
Entries should omit empty provenance sections rather than spelling out `None in this entry.`
If an entry has no measurements yet, it should say so explicitly.

## Latest

## Committed History

### March 10, 2026 — `6e3d4ba` — changelog: Rename active section to Latest — score `4` — complexity `6`

**Human-directed, AI-shaped (4)**

- Requested that the canonical autonomy-golf repo rename the active changelog section to `Latest` and make the CLI/tooling use that name too.
  - Meaning: the template repo should model one canonical section name and one matching parser interface for adopters to copy.
  - Motivation: `Latest` reads more naturally than `Unreleased`, and the canonical template should model that clearer wording directly.
  - Purpose: keep the canonical repo crisp so downstream adopters copy one clean pattern instead of inheriting alias baggage.
  - Renamed the parser and renderer interface from `--include-unreleased` to `--include-latest`, and changed the emitted fields and scope labels from `is_unreleased` / `including_unreleased` to `is_latest` / `including_latest`.
  - Updated the canonical changelog, README commands, and checklist/agent instructions to use `Latest` and `--include-latest` consistently.

**Grounding**

- Files:
  - `CHANGELOG.md`
  - `README.md`
  - `docs/autonomy-golf-agent.md`
  - `docs/autonomy-golf-checklist.md`
  - `tools/changelog_scores.py`
  - `tools/render_autonomy_badge.py`
- Validation:
  - `python3 tools/changelog_scores.py --group-by entry --format csv --include-latest --verify`
  - `python3 tools/render_autonomy_badge.py`
- Measurements:
  - This is governance and scoring-tooling work, not a runtime optimization, so there are no performance measurements.

### March 10, 2026 — `fbab975` — docs: Tighten canonical README and install guidance — score `4` — complexity `8`

**Human-directed, AI-shaped (4)**

- Requested that the canonical README pick up the improved project-local framing we just used in `autoresearch`, while leaving the exact wording and placement to the agent.
  - Meaning: the canonical repo should present itself not just as a template library, but as a project that is itself playing autonomy golf on itself.
  - Motivation: the old README opening still read mostly as a general invitation, while the newer phrasing makes the Score / Grounding loop and the self-referential use of the system clearer.
  - Purpose: make the canonical repo a stronger example of the game in practice, not just a host for the rules and tools.
  - Reworded the opening README framing so the repo explicitly describes itself as playing autonomy golf on itself through its changelog, parser, and badge.
  - Tightened the README language around `Score` and `Grounding` so those terms read as the managed paired signals of the system rather than just a loose list of concepts.
  - Wrapped the top badge in a local anchor link so the headline graphic jumps readers directly into the explanatory section it summarizes.
  - Updated the agent brief so `What To Install` explicitly includes the README autonomy-golf block pattern, not just the changelog and tools.

**Grounding**

- Files:
  - `README.md`
  - `CHANGELOG.md`
  - `docs/autonomy-golf-agent.md`
- Validation:
  - `python3 tools/changelog_scores.py --group-by entry --format csv --include-latest --verify`
  - `python3 tools/changelog_scores.py --group-by overall --format csv --include-latest`
  - `python3 tools/render_autonomy_badge.py`
- Measurements:
  - This is README framing work, not a runtime optimization, so there are no performance measurements.

### March 10, 2026 — `55c401c` — badge: Add house golf term to generated badge — score `4` — complexity `7`

**Human-directed, AI-shaped (4)**

- Requested that the badge itself adopt the house golf language, while leaving the exact badge rendering choice to the agent.
  - Meaning: the headline project badge should speak the same playful autonomy-golf language as the manifesto, not just expose a raw number.
  - Motivation: the canonical repo now defines house terms like `eagle`, `birdie`, and `par`, but the badge was still numerically literal.
  - Purpose: make the top-level project badge feel more like the game the docs describe, without losing the precise numeric score.
  - Updated the badge renderer so it maps the project mean score to the nearest house term and shows that term alongside the numeric score.
  - Added a small hole flag graphic to the badge so the visual itself carries a bit of the golf theme, not just the text.
  - Exempted `Meaning:`, `Motivation:`, and `Purpose:` narrative sub-bullets from complexity so explanatory context does not inflate the scope signal.

**Grounding**

- Files:
  - `CHANGELOG.md`
  - `tools/render_autonomy_badge.py`
  - `docs/autonomy-golf-badge.svg`
- Validation:
  - `python3 tools/render_autonomy_badge.py`
- Measurements:
  - This is badge/rendering work, not a runtime optimization, so there are no performance measurements.
  - Current parser summary (`python3 tools/changelog_scores.py --group-by overall --format csv --include-latest`):

    | Scope | commits | subsystems | mean score | mean complexity / commit | mean score / bullet |
    | --- | ---: | ---: | ---: | ---: | ---: |
    | `including_latest` | `3` | `2` | `3.67` | `13.33` | `3.50` |

### March 10, 2026 — `0e70c0d` — changelog: Tighten maintenance checklist and canonical references — score `4` — complexity `20`

**Human-directed, AI-shaped (4)**

- Requested review of the in-flight docs and checklist as maintenance instructions for the current change, leaving the exact doc wording and structure to the agent.
  - Meaning: the canonical autonomy-golf bundle is being tightened into a more portable and more disciplined adoption package, not just cosmetically edited.
  - Motivation: the docs were directionally right, but they still left too much interpretive work to downstream adopters and did not model their own documentation rules strongly enough.
  - Purpose: make the canonical repository easier to copy into another project without inventing local variants or drifting away from the parser-backed structure.
  - Added explicit references to the canonical GitHub home across the public docs so downstream adopters know where the authoritative template and tooling live.
  - Reframed `docs/autonomy-golf.md` as a portable manifesto and file directory that can be dropped into another repository while still pointing back to the canonical source bundle.
  - Tightened the manifesto's adoption step so “copy the changelog and tooling” points directly at the canonical GitHub repository instead of referring to it indirectly.
  - Aggressively trimmed `docs/autonomy-golf-agent.md` down to the essential install brief: bundle, score model, hard rules, changelog contract, grounding, install loop, maintenance handoff, and starter prompt.
  - Leaned the agent brief harder onto the existing README, changelog template, and maintenance checklist so adopting agents reuse the canonical files instead of carrying redundant rule text.
  - Added practical integration guidance that autonomy golf should hook into an existing change-management path, ideally pre-commit or pre-merge, rather than becoming a parallel ritual.
  - Made the “meaning, motivation, purpose” narrative more prominent across the README, manifesto, agent brief, checklist, and changelog so the system reads as consensus-building discipline rather than scorekeeping alone.
  - Re-centered the public framing around the ideal of driving toward total automation in a fun and meaningful way, with score and grounding treated as the mechanisms that keep that game honest.
  - Added explicit house golf language in the manifesto so scores can be discussed as `albatross`, `eagle`, `birdie`, `par`, `bogey`, and so on, rather than only as raw numbers.
  - Shifted the whole house scale by one so `2 = eagle`, `3 = birdie`, and `4 = par`, which matches the intended golf framing better than the first draft.
  - Extended the score ladder to `0..6` by adding an explicit `Fully human (6)` tier, so projects can distinguish human-authored work from human-directed but agent-executed work.
  - Changed `complexity` so nested sub-bullets under provenance items scored `3` or higher each add `+1`, which better reflects elaborated high-agency change structure.
  - Tightened the maintenance instructions so they explicitly cover derived score recalculation, generated README snapshot ownership, and targeted validation when the parser or badge renderer changes.
  - Tightened the checklist and agent brief around the exact in-flight maintenance loop this repo exercised: update provenance, recompute derived changelog values, refresh generated outputs, and verify the parser still agrees.
  - Added the explicit lag-by-one commit-ID rule: latest in-flight work stays as `New commit` until the hash exists, then gets stamped into committed history and replaced by a fresh latest slot only if more work continues.
  - Tightened the changelog entry itself so it demonstrates explicit meaning, motivation, and purpose instead of only requiring them.

**Grounding**

- Files:
  - `README.md`
  - `CHANGELOG.md`
  - `docs/autonomy-golf.md`
  - `docs/autonomy-golf-agent.md`
  - `docs/autonomy-golf-checklist.md`
  - `tools/changelog_scores.py`
  - `tools/render_autonomy_badge.py`
- Validation:
  - `python3 -m py_compile tools/changelog_scores.py tools/render_autonomy_badge.py`
  - `python3 tools/changelog_scores.py --group-by entry --format csv --include-latest --verify`
  - `python3 tools/changelog_scores.py --group-by overall --format csv --include-latest`
  - `python3 tools/render_autonomy_badge.py`
- Measurements:
  - This is follow-up documentation and maintenance work, not a runtime optimization, so there are no performance measurements.
  - Current parser summary (`python3 tools/changelog_scores.py --group-by overall --format csv --include-latest`):

    | Scope | commits | subsystems | mean score | mean complexity / commit | mean score / bullet |
    | --- | ---: | ---: | ---: | ---: | ---: |
    | `including_latest` | `2` | `1` | `3.50` | `16.50` | `3.33` |

### March 10, 2026 — `393a4be` — changelog: Seed canonical autonomy-golf repository — score `3` — complexity `13`

**Human-directed, AI-shaped (4)**

- Requested a standalone canonical autonomy-golf repository beside `autoresearch`, while leaving the exact repository shape and seeded content to the agent.
  - Meaning: autonomy golf now exists as a reusable standalone system rather than an incidental pattern buried inside another repository.
  - Motivation: downstream projects need a single canonical source for the template, parser, badge, and explainer instead of having to extract them from unrelated work.
  - Purpose: make adoption cheap and repeatable enough that other projects can install the full loop, not just copy the headline idea.
  - Initialized a sibling Git repository.
  - Added a generic README, changelog template, public explainer, and reusable agent integration brief.
  - Added a concise maintenance checklist so agents can be told to "read and follow the autonomy golf checklist" once the system is already installed.
  - Copied in the score parser and badge renderer as the initial working tooling.
  - Positioned the repository as turnkey infrastructure rather than a loose concept note.
  - Clarified in the canonical docs and template that `Grounding` is unscored not because it is secondary, but because it is a separate validation dimension that should inform data-driven decisions without being conflated with autonomy.
  - Refactored the docs around explicit document roles so README, explainer, agent brief, and changelog each have a clear job and cross-reference each other cleanly.

**AI-identified within brief, human-approved (2)**

- Made the existing badge tool refresh the README snapshot block as well, so the visible project summary no longer depends on manual table edits.
  - Meaning: the visible project snapshot became generated output rather than a hand-maintained summary.
  - Motivation: manual snapshot edits would inevitably drift away from parser truth.
  - Purpose: keep the README badge and snapshot trustworthy enough to serve as a public-facing project score.

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
  - `python3 tools/changelog_scores.py --group-by entry --format csv --include-latest --verify`
  - `python3 tools/changelog_scores.py --group-by overall --format csv --include-latest`
  - `python3 tools/render_autonomy_badge.py`
- Measurements:
  - This is scaffolding and documentation work, not a runtime optimization, so there are no performance measurements.
  - Parser summary at commit time (`python3 tools/changelog_scores.py --group-by overall --format csv --include-latest`):

    | Scope | commits | subsystems | mean score | mean complexity / commit | mean score / bullet |
    | --- | ---: | ---: | ---: | ---: | ---: |
    | `including_latest` | `1` | `1` | `3.00` | `13.00` | `3.00` |
