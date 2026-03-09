# Autonomy Golf Agent Integration

## Document Role

This is the implementation brief for a coding agent that has been asked to install autonomy golf in a project.

If you want the public rationale and scoring philosophy, read [autonomy-golf.md](autonomy-golf.md).
If autonomy golf is already installed and you just need the maintenance loop, read [autonomy-golf-checklist.md](autonomy-golf-checklist.md).
If you want the concrete starter template and parser input shape, read [../CHANGELOG.md](../CHANGELOG.md).

This document is for a coding agent that has been asked to integrate autonomy golf into an existing software project.

It is meant to be a reusable integration brief, not a project-specific operating prompt. The objective is not just to add a badge. The objective is to install a disciplined loop for recording who drove changes, how autonomous the work actually was, and whether that autonomy is improving over time.

The system works best when `CHANGELOG.md` is agent-managed. That does not mean unreadable machine sludge. It means the changelog is maintained in a regular structure that serves two jobs at once:

- readable engineering history for humans
- reliable input for parsers, rollups, badges, and later charts

When adopting autonomy golf, start from the working infrastructure already present in this repository rather than designing a fresh system from scratch. The intended path is to copy or adapt:

- [../CHANGELOG.md](../CHANGELOG.md)
- [../tools/changelog_scores.py](../tools/changelog_scores.py)
- [../tools/render_autonomy_badge.py](../tools/render_autonomy_badge.py) for both the badge and the README snapshot block
- [autonomy-golf.md](autonomy-golf.md)
- this document

## Goal

Add a lightweight autonomy-accounting system to the project so that:

- each landed change records its provenance explicitly
- the project can compute a bounded autonomy score over time
- the history can be broken down by subsystem
- the project can publish a project-level badge or snapshot
- the accounting is conservative enough that lower scores remain meaningful

## Core Mechanics

Autonomy golf uses one scored provenance tier per top-level changelog bullet:

- `Human-driven (5)`
- `Human-directed, AI-shaped (4)`
- `AI-identified within brief, human-shaped (3)`
- `AI-identified within brief, human-approved (2)`
- `Self-initiated, human-approved (1)`
- `Fully autonomous (0)`

`Grounding` is not scored.

Each commit entry should expose:

- `score`: the arithmetic mean of the top-level provenance bullet weights for that commit
- `complexity`: the summed weight of those same top-level bullets

`score` is the main autonomy signal. Lower is better.

`complexity` is a secondary scope signal. It shows how much separately scored provenance surface the commit covered. Omit it when it is numerically identical to `score`.

## Why Grounding Matters

Treat `Grounding` as a first-class validation record, not as leftover metadata.

Provenance and grounding answer different questions:

- provenance: who drove the change
- grounding: what evidence supports the change

Keep them separate on purpose.

- do not let strong validation make a change look more autonomous than it was
- do not let weak validation disappear behind a low autonomy score
- do use grounding to support data-driven decisions about what to keep, trust, or revert

The practical meaning is simple: an autonomy-golf system is only as useful as its grounding discipline. If the score is carefully tracked but the evidence is loose, the project still does not know which changes deserve confidence.

One useful ideal for grounding to track is meaningful test coverage. Not every change maps cleanly to a coverage percentage, and not every project should worship coverage as a proxy for correctness, but where automated tests are the right validation surface, pushing toward complete or near-complete coverage is a legitimate goal. Grounding is the place to record whether a change moved that ideal forward, held the line, or skipped it for a good reason.

## Required Rules

The system only works if the accounting stays strict.

- Bias toward under-claiming autonomy.
- If provenance is ambiguous, choose the more conservative tier.
- Score only top-level provenance bullets.
- Put directly derivative same-tier details under nested bullets so they stay visible without inflating the score.
- Keep `Grounding` separate from provenance, and use it to record the real strength of validation.
- Do not let `agent suggested` quietly become `fully autonomous`.

## Commit And Changelog Shape

Use Linux-kernel-style subsystem headers:

```text
train: Add train and wall time budget modes
checkpoints: Benchmark resume-ready checkpoint latency
changelog: Add subsystem-scoped commit headers
```

The dominant subsystem should be used as the prefix. Only use a combined subsystem when one label would be misleading.

Each changelog entry should include:

- a header with `subsystem: summary`
- the bounded `score`
- optional `complexity`
- one or more provenance sections
- a `Grounding` section with files, checks, and measurements

This structure is functional, not cosmetic. If the agent drifts into free-form prose, the accounting stops being trustworthy. If it drifts into parser-first sludge, the history stops being useful to humans. The target is both at once.

## Working Loop

This is the loop to follow when integrating or maintaining autonomy golf in a project:

1. Make or review a change.
2. Decide what actually drove the change.
3. Record that provenance in the changelog conservatively.
4. Record the grounding strength honestly so later decisions can be based on evidence rather than memory or enthusiasm.
5. Update or regenerate the score outputs.
6. Publish the project-level snapshot or badge.
7. Use the results to decide where autonomy is still weak.

The agent should treat changelog maintenance as part of the change itself, not as cleanup afterward.

In practice, the fastest path is usually:

1. adapt the changelog structure from this repository
2. adapt `tools/changelog_scores.py` to the target repo layout if needed
3. adapt `tools/render_autonomy_badge.py` for the target README
4. add a short project-specific operating prompt that tells future agents how to keep the system current

## Suggested Prompt

The fastest way to start is to give the agent a prompt like:

> Integrate autonomy golf into this project. Reuse the changelog template, score parser, and badge renderer from the canonical autonomy-golf repository. Add a conservative provenance-scored changelog format, subsystem-scoped commit headers, a project-level badge or summary in the README, and agent guidance for keeping the system updated. Bias toward under-claiming autonomy, keep grounding separate from provenance, and make the output suitable for later plotting by day and subsystem.

## Success Condition

The integration is successful when the project can answer, with evidence:

- how autonomous recent work actually was
- which subsystems are improving
- whether the accounting is honest enough to trust
- whether the score is moving toward `Fully autonomous` over time
