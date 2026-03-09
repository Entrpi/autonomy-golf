# autonomy-golf

![Autonomy Golf Badge](docs/autonomy-golf-badge.svg)

Come play autonomy golf: wire your project up with a changelog, parser, and badge that make the drive toward total automation fun, legible, and honest, then try to drive the score down over time without getting sloppy about evidence.

Canonical GitHub home: [Entrpi/autonomy-golf](https://github.com/Entrpi/autonomy-golf)

Autonomy golf works best with an agent-managed `CHANGELOG.md` that stays readable to humans while remaining structured enough for parsers, badges, and charts. This repository packages the working pieces:

- a conservative changelog template in [CHANGELOG.md](CHANGELOG.md)
- the public explainer in [docs/autonomy-golf.md](docs/autonomy-golf.md)
- the agent integration brief in [docs/autonomy-golf-agent.md](docs/autonomy-golf-agent.md)
- the score parser in [tools/changelog_scores.py](tools/changelog_scores.py)
- the badge renderer in [tools/render_autonomy_badge.py](tools/render_autonomy_badge.py)

Just as importantly, autonomy golf is a discipline for building explicit consensus around a change's meaning, motivation, and purpose. The point is to make progress toward total automation both fun and meaningful: fun enough that teams want to play, meaningful enough that the score still corresponds to real autonomy.

The key discipline is that autonomy golf tracks two separate things on purpose:

- `score`: how autonomous the change was
- `Grounding`: how well the change was validated

`Grounding` is intentionally unscored. It is the evidence layer that keeps the autonomy accounting useful for validation and data-driven decisions instead of turning into a cosmetic badge game.

Scoring tiers:

| Tier | Meaning | Score |
| --- | --- | ---: |
| `Fully human` | the change was identified and authored by a human, with the agent absent or limited to review and minor revisions | `6` |
| `Human-driven` | the human identified the change and specified it tightly enough that the agent mostly executed | `5` |
| `Human-directed, AI-shaped` | the human set the direction, but the agent designed the concrete mechanism or validation | `4` |
| `AI-identified within brief, human-shaped` | the agent surfaced the opportunity inside a broad human brief, and the human materially reshaped it | `3` |
| `AI-identified within brief, human-approved` | the agent surfaced the opportunity inside a broad human brief, and the human approved it with little reshaping | `2` |
| `Self-initiated, human-approved` | the agent initiated the change outside explicit human direction, but still got approval before landing | `1` |
| `Fully autonomous` | the agent initiated the change without explicit human direction or approval in the thread | `0` |

<!-- autonomy-golf-snapshot:start -->
Current project snapshot from [CHANGELOG.md](CHANGELOG.md):

| Metric | Value |
| --- | --- |
| Mean autonomy score | `3.67 / 6` |
| Mean complexity | `13.33 / commit` |
| Mean score per top-level bullet | `3.50 / 6` |
| History covered | `3` commits across `2` subsystems |
<!-- autonomy-golf-snapshot:end -->

## Document Map

- [README.md](README.md): front door, quick start, badge, and example entry
- [docs/autonomy-golf.md](docs/autonomy-golf.md): public explainer for the purpose and philosophy of autonomy golf
- [docs/autonomy-golf-agent.md](docs/autonomy-golf-agent.md): reusable agent-facing brief for integrating the system into another project
- [docs/autonomy-golf-checklist.md](docs/autonomy-golf-checklist.md): concise maintenance checklist for agents working in a project that already uses autonomy golf
- [CHANGELOG.md](CHANGELOG.md): canonical changelog template and parser-facing source of truth

## Start Here

The fastest way to adopt the system in another codebase is:

1. Point your agent at [docs/autonomy-golf-agent.md](docs/autonomy-golf-agent.md).
2. Copy or adapt the changelog structure from [CHANGELOG.md](CHANGELOG.md).
3. Copy or adapt the tooling under [tools/](tools/).
4. Add the badge to your README and keep it refreshed from the parser output.

If you are starting from outside this repository, the canonical source for those files is [Entrpi/autonomy-golf](https://github.com/Entrpi/autonomy-golf).

Once autonomy golf is already installed in a project, the shorter maintenance instruction is: read and follow [docs/autonomy-golf-checklist.md](docs/autonomy-golf-checklist.md).

## Core Ideas

- the central game is to push the project toward total automation in a way that stays enjoyable, legible, and worth trusting
- `score` is the bounded autonomy signal on a `0..6` scale. Lower is better.
- `complexity` is the scope signal: top-level provenance weights plus a `+1` bonus for each nested sub-bullet under provenance items scored `3` or higher, excluding `Meaning:`, `Motivation:`, and `Purpose:` narrative lines.
- top-level provenance bullets are the scored units
- good entries do more than log tasks; they build explicit consensus on a change's meaning, motivation, and purpose
- `Grounding` is the separate validation signal: files changed, checks run, and measured effects. It is intentionally unscored so validation strength stays distinct from autonomy level.
- subsystem-prefixed commit headers make the history analyzable by subsystem as well as by day

## Example Entry

```md
### March 9, 2026 — `abc1234` — parser: Add subsystem rollup output — score `3` — complexity `7`

**Human-directed, AI-shaped (4)**

- Requested subsystem-level autonomy reporting so the project can see where human direction is still concentrated.
  - Meaning: autonomy trends should be inspectable by subsystem, not only at whole-project level.
  - Motivation: aggregate project scores hide where the real human bottlenecks still are.
  - Purpose: make the score actionable enough to steer future autonomy work.
  - Added a subsystem rollup mode to the parser.

**AI-identified within brief, human-approved (2)**

- Added a matching README summary command so the new rollup is visible and easy to use.

**Grounding**

- Files:
  - `tools/changelog_scores.py`
  - `README.md`
- Validation:
  - `python3 -m py_compile tools/changelog_scores.py`
  - `python3 tools/changelog_scores.py --group-by subsystem --format csv`
- Measurements:
  - This is tooling work, so there are no runtime performance measurements.
```

## Commands

Project-level rollup:

```bash
python3 tools/changelog_scores.py --group-by overall --format csv --include-unreleased
```

Per-entry verification:

```bash
python3 tools/changelog_scores.py --group-by entry --format csv --include-unreleased --verify
```

Refresh the badge and README snapshot:

```bash
python3 tools/render_autonomy_badge.py
```

## Repository Layout

```text
CHANGELOG.md                 starter changelog template and example history
docs/autonomy-golf.md        public explainer
docs/autonomy-golf-agent.md  reusable agent integration brief
docs/autonomy-golf-checklist.md
                             concise maintenance checklist
tools/changelog_scores.py    parser and rollup tool
tools/render_autonomy_badge.py
                             badge renderer
```
