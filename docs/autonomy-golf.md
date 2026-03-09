# Autonomy Golf

## Document Role

This is the public explainer: why autonomy golf exists, what the numbers mean, and what makes the system trustworthy.

If you want implementation mechanics, read [autonomy-golf-agent.md](autonomy-golf-agent.md).
If you want the concrete template and parser substrate, read [../CHANGELOG.md](../CHANGELOG.md).

## Purpose

Autonomy golf is a simple game any software project can play to reduce how much human steering a successful change requires.

The word `golf` is deliberate. Lower is better:

- `5` means the human tightly specified the change.
- `0` means the change was fully autonomous.

The point is not to make the number look good. The point is to create pressure toward a more genuinely autonomous development loop while keeping the accounting honest enough that the number still means something.

Any project that talks about agents, autonomy, or self-improving tooling has the same risk: ordinary human-guided maintenance can accumulate while the project keeps implying stronger autonomy than it has actually achieved. Autonomy golf is a way to make that gap visible.

## Why Track It

Autonomy golf exists to answer a few concrete questions:

- Are we actually making the loop more self-directed, or just adding more code around a human-driven process?
- Which subsystems still need the most human intervention?
- Are improvements in autonomy coming from real changes in agent behavior, or just from looser bookkeeping?
- When a project says it is moving toward full autonomy, is there evidence for that claim?

The score is therefore not just a vanity metric. It is a governance tool.

It also depends on a specific kind of artifact: an agent-managed `CHANGELOG.md` that stays readable to humans while remaining structured enough for tooling to parse. Without that combination, the badge becomes either hand-wavy prose or brittle machine output, and neither is useful.

## Scoring Model

Each top-level provenance bullet in a changelog entry gets one autonomy weight:

- `Human-driven (5)`
- `Human-directed, AI-shaped (4)`
- `AI-identified within brief, human-shaped (3)`
- `AI-identified within brief, human-approved (2)`
- `Self-initiated, human-approved (1)`
- `Fully autonomous (0)`

`Grounding` is not scored.

Each commit header carries two related numbers:

- `score`: the arithmetic mean of the top-level provenance bullet weights for that commit, rounded to two decimals
- `complexity`: the summed weight of those same top-level bullets

## Why Grounding Is Separate

`Grounding` is not scored because it is measuring a different thing.

Provenance answers:

- who drove the change
- how autonomous the work really was

Grounding answers:

- what evidence supports the change
- how strong the validation was
- whether later readers should trust the claim

Those should not be collapsed into one number.

Strong grounding should not make a human-driven change look more autonomous. Weak grounding should not make an agent-driven change look less autonomous. Instead, the system should show both dimensions clearly:

- autonomy level through `score`
- validation quality through `Grounding`

That separation is what keeps autonomy golf useful for data-driven decisions. A project should be able to say both:

- how autonomous a change was
- how well the change was actually validated

Without explicit grounding, autonomy accounting becomes easy to game. The score may go down while trust in the history goes down with it.

## How To Read The Numbers

`score` is the main autonomy signal.

- lower is better
- `0` means fully autonomous
- `5` means tightly human-driven
- because it is bounded, commits stay on the same `0..5` spectrum even when they differ in breadth

`complexity` is the secondary scope signal.

- higher means the commit needed more separately scored provenance structure
- two commits can have similar autonomy levels but different breadth
- when `complexity` is numerically identical to `score`, it is omitted from the header as redundant

In practice:

- use `score` to judge autonomy level
- use `complexity` to judge how much scored change surface the commit covered

## Why The Accounting Is Strict

A useful autonomy-golf system should deliberately bias toward under-claiming autonomy.

That means:

- if provenance is ambiguous, choose the more conservative tier
- if a change was surfaced by the AI only inside a broad human brief, do not describe it as self-initiated
- if a change was fully human-authored, say so plainly or keep it out of autonomy-scored history if that is project policy

The goal is still to push as much work as possible toward `Fully autonomous`.

But inflated autonomy claims are failure, not progress.

If the bookkeeping gets soft, the game stops being useful. The number improves, but the project learns nothing.

That is why autonomy golf works best when the changelog is actively maintained by the agent as part of the normal loop, not treated as an afterthought. The human-readable narrative and the parser-facing structure have to stay aligned.

## Why Subsystems Matter

Commit headers should use Linux-kernel-style subsystem prefixes:

```text
train: Add train and wall time budget modes
checkpoints: Benchmark resume-ready checkpoint latency
changelog: Add subsystem-scoped commit headers
```

This makes autonomy golf analyzable by subsystem rather than only by day or by whole-project history.

That matters because autonomy does not improve uniformly.

## What “Winning” Looks Like

A good autonomy-golf trajectory is not:

- hiding human direction
- merging many ideas into one header to dilute provenance
- using vague changelog language so the parser cannot tell what happened

A good trajectory is:

- more commits whose ideas were initiated by the agent
- more commits whose implementation and validation were designed by the agent
- more subsystems where the mean autonomy score trends downward over time
- unchanged or improved rigor in grounding and provenance honesty

## Join The Game

The easiest way to start is to point your coding agent at [autonomy-golf-agent.md](autonomy-golf-agent.md) and ask it to integrate autonomy golf into your project.

That companion document is a reusable agent-facing integration brief. It explains how to install the autonomy-golf system itself in another codebase by leveraging the working changelog, parser, and badge infrastructure already present here.

The important implementation detail is that this works best with an agent-managed changelog. The agent should keep `CHANGELOG.md` updated as part of the working loop, using a disciplined structure that is pleasant to read in Git but regular enough that a parser can verify scores, subsystem headers, and rollups without guesswork.

## This Repository

This repository packages one concrete implementation:

- `CHANGELOG.md`: starter changelog template and example entry
- `tools/changelog_scores.py`: parser and rollup tool
- `tools/render_autonomy_badge.py`: badge renderer and README snapshot updater
- `docs/autonomy-golf-agent.md`: reusable agent integration brief

The README shows the current project snapshot as a generated badge plus a generated snapshot block. Later, the same accounting can drive richer charts without changing the underlying model.
