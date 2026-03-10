#!/usr/bin/env python3
"""
Parse CHANGELOG.md autonomy scores into plotting-friendly rows.

Examples:
    python3 tools/changelog_scores.py --group-by day --format csv
    python3 tools/changelog_scores.py --group-by overall --format csv --include-latest
    python3 tools/changelog_scores.py --group-by subsystem --format csv
    python3 tools/changelog_scores.py --group-by day-subsystem --format csv
    python3 tools/changelog_scores.py --group-by entry --format json --include-latest --verify
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

SCORE_PRECISION = 2
ROOT = Path(__file__).resolve().parents[1]
LATEST_SECTION_NAME = "Latest"

CATEGORY_ORDER = (
    "Fully human",
    "Human-driven",
    "Human-directed, AI-shaped",
    "AI-identified within brief, human-shaped",
    "AI-identified within brief, human-approved",
    "Self-initiated, human-approved",
    "Fully autonomous",
)

CATEGORY_WEIGHTS = {
    "Fully human": 6,
    "Human-driven": 5,
    "Human-directed, AI-shaped": 4,
    "AI-identified within brief, human-shaped": 3,
    "AI-identified within brief, human-approved": 2,
    "Self-initiated, human-approved": 1,
    "Fully autonomous": 0,
}

CATEGORY_HEADING_RE = re.compile(r"^(?P<label>.+?)(?: \((?P<score>\d+)\))?$")
SUBSYSTEM_TITLE_RE = re.compile(r"^(?P<subsystem>[a-z0-9][a-z0-9_./-]*): (?P<summary>.+)$")
NARRATIVE_PREFIXES = ("Meaning:", "Motivation:", "Purpose:")

EM_DASH = "\u2014"
HEADER_RE = re.compile(
    rf"^### (?P<prefix>.+?) {EM_DASH} score `(?P<score>\d+(?:\.\d+)?)`"
    rf"(?: {EM_DASH} complexity `(?P<complexity>\d+)`)?$"
)
COMMITTED_PREFIX_RE = re.compile(
    rf"^(?P<date>[A-Za-z]+ \d{{1,2}}, \d{{4}}) {EM_DASH} `(?P<commit>[0-9a-f]+)` {EM_DASH} (?P<title>.+)$"
)


@dataclass
class Entry:
    section: str
    raw_header: str
    title: str
    subsystem: str | None
    summary: str
    header_score: float
    header_complexity: int | None
    commit: str | None
    date_label: str | None
    current_section: str | None = None
    category_counts: dict[str, int] | None = None
    nested_bonus_count: int = 0

    def __post_init__(self) -> None:
        if self.category_counts is None:
            self.category_counts = {category: 0 for category in CATEGORY_ORDER}

    @property
    def top_level_bullet_count(self) -> int:
        return sum(self.category_counts[category] for category in CATEGORY_ORDER)

    @property
    def total_points(self) -> int:
        return sum(self.category_counts[category] * CATEGORY_WEIGHTS[category] for category in CATEGORY_ORDER)

    @property
    def computed_complexity(self) -> int:
        return self.total_points + self.nested_bonus_count

    @property
    def computed_score(self) -> float:
        if self.top_level_bullet_count == 0:
            return 0.0
        return round_score(self.total_points / self.top_level_bullet_count)

    @property
    def score_delta(self) -> float:
        return round_score(self.header_score - self.computed_score)

    @property
    def complexity_delta(self) -> int:
        return self.effective_header_complexity - self.computed_complexity

    @property
    def has_explicit_complexity(self) -> bool:
        return self.header_complexity is not None

    @property
    def effective_header_complexity(self) -> int:
        if self.header_complexity is not None:
            return self.header_complexity
        if self.header_score.is_integer():
            return int(self.header_score)
        raise ValueError(
            f"Header for {self.title!r} omits complexity but score {self.header_score} cannot imply an integer complexity"
        )

    @property
    def is_latest(self) -> bool:
        return self.section == LATEST_SECTION_NAME

    @property
    def missing_subsystem_prefix(self) -> bool:
        return self.subsystem is None

    @property
    def iso_date(self) -> str | None:
        if self.date_label is None:
            return None
        return datetime.strptime(self.date_label, "%B %d, %Y").date().isoformat()

    def as_row(self) -> dict[str, object]:
        row = {
            "section": self.section,
            "date": self.iso_date,
            "date_label": self.date_label,
            "commit": self.commit,
            "subsystem": self.subsystem,
            "title": self.title,
            "summary": self.summary,
            "header_score": self.header_score,
            "computed_score": self.computed_score,
            "score_delta": self.score_delta,
            "header_complexity": self.effective_header_complexity,
            "computed_complexity": self.computed_complexity,
            "complexity_delta": self.complexity_delta,
            "has_explicit_complexity": self.has_explicit_complexity,
            "is_latest": self.is_latest,
            "top_level_bullet_count": self.top_level_bullet_count,
            "total_points": self.total_points,
            "nested_bonus_count": self.nested_bonus_count,
        }
        for category in CATEGORY_ORDER:
            slug = slugify(category)
            count = self.category_counts[category]
            row[f"{slug}_count"] = count
            row[f"{slug}_points"] = count * CATEGORY_WEIGHTS[category]
        return row


def slugify(label: str) -> str:
    return label.lower().replace(",", "").replace("-", "").replace(" ", "_")


def round_score(value: float) -> float:
    return round(value, SCORE_PRECISION)


def normalize_section_label(label: str) -> str:
    match = CATEGORY_HEADING_RE.match(label)
    if not match:
        return label
    base_label = match.group("label")
    score_text = match.group("score")
    if score_text is not None and base_label in CATEGORY_WEIGHTS:
        expected = CATEGORY_WEIGHTS[base_label]
        seen = int(score_text)
        if seen != expected:
            raise ValueError(
                f"Section heading score mismatch for {base_label!r}: saw {seen}, expected {expected}"
            )
    return base_label


def parse_entry_header(line: str, current_section: str) -> Entry:
    match = HEADER_RE.match(line)
    if not match:
        raise ValueError(f"Unrecognized changelog header: {line}")

    prefix = match.group("prefix")
    header_score = float(match.group("score"))
    header_complexity = int(match.group("complexity")) if match.group("complexity") is not None else None
    committed = COMMITTED_PREFIX_RE.match(prefix)
    if committed:
        title = committed.group("title")
        commit = committed.group("commit")
        date_label = committed.group("date")
    else:
        title = prefix.split(f" {EM_DASH} ", 1)[1] if f" {EM_DASH} " in prefix else prefix
        commit = None
        date_label = None

    subsystem_match = SUBSYSTEM_TITLE_RE.match(title)
    subsystem = subsystem_match.group("subsystem") if subsystem_match else None
    summary = subsystem_match.group("summary") if subsystem_match else title
    return Entry(
        section=current_section,
        raw_header=line,
        title=title,
        subsystem=subsystem,
        summary=summary,
        header_score=header_score,
        header_complexity=header_complexity,
        commit=commit,
        date_label=date_label,
    )


def is_narrative_nested_bullet(line: str) -> bool:
    stripped = line[4:].strip()
    return any(stripped.startswith(prefix) for prefix in NARRATIVE_PREFIXES)


def parse_changelog(path: Path) -> list[Entry]:
    entries: list[Entry] = []
    current_top_level: str | None = None
    current_entry: Entry | None = None

    for raw_line in path.read_text().splitlines():
        line = raw_line.rstrip()
        if line.startswith("## "):
            current_top_level = line[3:].strip()
            continue
        if line.startswith("### "):
            if current_entry is not None:
                entries.append(current_entry)
            if current_top_level is None:
                raise ValueError(f"Entry header found outside a top-level section: {line}")
            current_entry = parse_entry_header(line, current_top_level)
            continue
        if current_entry is None:
            continue
        if line.startswith("**") and line.endswith("**"):
            label = normalize_section_label(line.strip("*"))
            current_entry.current_section = label
            continue
        if line.startswith("- ") and current_entry.current_section in CATEGORY_WEIGHTS:
            current_entry.category_counts[current_entry.current_section] += 1
            continue
        if (
            line.startswith("  - ")
            and current_entry.current_section in CATEGORY_WEIGHTS
            and CATEGORY_WEIGHTS[current_entry.current_section] >= 3
            and not is_narrative_nested_bullet(line)
        ):
            current_entry.nested_bonus_count += 1

    if current_entry is not None:
        entries.append(current_entry)
    return entries


def build_daily_rows(entries: list[Entry], include_latest: bool) -> list[dict[str, object]]:
    grouped: dict[str, dict[str, object]] = {}
    for entry in entries:
        key = entry.iso_date
        if key is None:
            if not include_latest:
                continue
            key = "latest"
        if key not in grouped:
            grouped[key] = {
                "date": key,
                "commit_count": 0,
                "top_level_bullet_count": 0,
                "total_points": 0,
                "total_nested_bonus": 0,
                "total_complexity": 0,
                "total_header_score": 0,
                "total_computed_score": 0,
                "total_score_delta": 0,
                "total_header_complexity": 0,
                "total_complexity_delta": 0,
            }
            for category in CATEGORY_ORDER:
                slug = slugify(category)
                grouped[key][f"{slug}_count"] = 0
                grouped[key][f"{slug}_points"] = 0
        row = grouped[key]
        row["commit_count"] += 1
        row["top_level_bullet_count"] += entry.top_level_bullet_count
        row["total_points"] += entry.total_points
        row["total_nested_bonus"] += entry.nested_bonus_count
        row["total_complexity"] += entry.computed_complexity
        row["total_header_score"] += entry.header_score
        row["total_computed_score"] += entry.computed_score
        row["total_score_delta"] += entry.score_delta
        row["total_header_complexity"] += entry.effective_header_complexity
        row["total_complexity_delta"] += entry.complexity_delta
        for category in CATEGORY_ORDER:
            slug = slugify(category)
            count = entry.category_counts[category]
            row[f"{slug}_count"] += count
            row[f"{slug}_points"] += count * CATEGORY_WEIGHTS[category]
    rows = []
    for key in sorted(grouped):
        row = grouped[key]
        commit_count = row["commit_count"]
        row["mean_header_score"] = round_score(row["total_header_score"] / commit_count)
        row["mean_computed_score"] = round_score(row["total_computed_score"] / commit_count)
        row["mean_score_per_bullet"] = round_score(row["total_points"] / row["top_level_bullet_count"])
        row["mean_header_complexity"] = round_score(row["total_header_complexity"] / commit_count)
        row["mean_computed_complexity"] = round_score(row["total_complexity"] / commit_count)
        rows.append(row)
    return rows


def init_grouped_score_row(**fields: object) -> dict[str, object]:
    row = {
        "commit_count": 0,
        "top_level_bullet_count": 0,
        "total_points": 0,
        "total_nested_bonus": 0,
        "total_complexity": 0,
        "total_header_score": 0,
        "total_computed_score": 0,
        "total_score_delta": 0,
        "total_header_complexity": 0,
        "total_complexity_delta": 0,
        **fields,
    }
    for category in CATEGORY_ORDER:
        slug = slugify(category)
        row[f"{slug}_count"] = 0
        row[f"{slug}_points"] = 0
    return row


def accumulate_grouped_score_row(row: dict[str, object], entry: Entry) -> None:
    row["commit_count"] += 1
    row["top_level_bullet_count"] += entry.top_level_bullet_count
    row["total_points"] += entry.total_points
    row["total_nested_bonus"] += entry.nested_bonus_count
    row["total_complexity"] += entry.computed_complexity
    row["total_header_score"] += entry.header_score
    row["total_computed_score"] += entry.computed_score
    row["total_score_delta"] += entry.score_delta
    row["total_header_complexity"] += entry.effective_header_complexity
    row["total_complexity_delta"] += entry.complexity_delta
    for category in CATEGORY_ORDER:
        slug = slugify(category)
        count = entry.category_counts[category]
        row[f"{slug}_count"] += count
        row[f"{slug}_points"] += count * CATEGORY_WEIGHTS[category]


def finalize_grouped_rows(grouped: dict[object, dict[str, object]], sort_keys: list[object]) -> list[dict[str, object]]:
    rows = []
    for key in sort_keys:
        row = grouped[key]
        commit_count = row["commit_count"]
        row["mean_header_score"] = round_score(row["total_header_score"] / commit_count)
        row["mean_computed_score"] = round_score(row["total_computed_score"] / commit_count)
        row["mean_score_per_bullet"] = round_score(row["total_points"] / row["top_level_bullet_count"])
        row["mean_header_complexity"] = round_score(row["total_header_complexity"] / commit_count)
        row["mean_computed_complexity"] = round_score(row["total_complexity"] / commit_count)
        rows.append(row)
    return rows


def build_subsystem_rows(entries: list[Entry], include_latest: bool) -> list[dict[str, object]]:
    grouped: dict[str, dict[str, object]] = {}
    for entry in entries:
        if entry.is_latest and not include_latest:
            continue
        key = entry.subsystem or "unscoped"
        if key not in grouped:
            grouped[key] = init_grouped_score_row(subsystem=key)
        accumulate_grouped_score_row(grouped[key], entry)
    return finalize_grouped_rows(grouped, sorted(grouped))


def build_day_subsystem_rows(entries: list[Entry], include_latest: bool) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], dict[str, object]] = {}
    for entry in entries:
        date_key = entry.iso_date
        if date_key is None:
            if not include_latest:
                continue
            date_key = "latest"
        subsystem_key = entry.subsystem or "unscoped"
        key = (date_key, subsystem_key)
        if key not in grouped:
            grouped[key] = init_grouped_score_row(date=date_key, subsystem=subsystem_key)
        accumulate_grouped_score_row(grouped[key], entry)
    return finalize_grouped_rows(grouped, sorted(grouped))


def build_overall_rows(entries: list[Entry], include_latest: bool) -> list[dict[str, object]]:
    scoped_entries = entries if include_latest else [entry for entry in entries if not entry.is_latest]
    if not scoped_entries:
        return []
    row = init_grouped_score_row(
        scope="including_latest" if include_latest else "committed_only",
        subsystem_count=len({entry.subsystem or "unscoped" for entry in scoped_entries}),
    )
    for entry in scoped_entries:
        accumulate_grouped_score_row(row, entry)
    return finalize_grouped_rows({"overall": row}, ["overall"])


def emit_rows(rows: list[dict[str, object]], fmt: str) -> None:
    if fmt == "json":
        json.dump(rows, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return

    if not rows:
        return

    fieldnames = list(rows[0].keys())
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    if fmt == "csv":
        writer.writeheader()
        writer.writerows(rows)
        return

    if fmt == "tsv":
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
        return

    raise ValueError(f"Unsupported format: {fmt}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize autonomy scores from CHANGELOG.md.")
    parser.add_argument(
        "--path",
        type=Path,
        default=ROOT / "CHANGELOG.md",
        help="Path to the changelog file.",
    )
    parser.add_argument(
        "--group-by",
        choices=("entry", "day", "overall", "subsystem", "day-subsystem"),
        default="day",
        help="Emit one row per commit entry, day, overall scope, subsystem, or day+subsystem.",
    )
    parser.add_argument(
        "--format",
        choices=("json", "csv", "tsv"),
        default="csv",
        help="Output format.",
    )
    parser.add_argument(
        "--include-latest",
        action="store_true",
        help="Include entries from the Latest section. Day output groups them under 'latest'.",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Exit nonzero if any header score does not match the computed score.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    entries = parse_changelog(args.path)

    if args.verify:
        mismatches = [entry for entry in entries if entry.score_delta != 0]
        unscoped = [entry for entry in entries if entry.missing_subsystem_prefix]
        if mismatches:
            for entry in mismatches:
                commit = entry.commit or "latest"
                print(
                    f"score mismatch: {commit} {entry.title!r} header={entry.header_score} computed={entry.computed_score}",
                    file=sys.stderr,
                )
        complexity_mismatches = [entry for entry in entries if entry.complexity_delta != 0]
        if complexity_mismatches:
            for entry in complexity_mismatches:
                commit = entry.commit or "latest"
                print(
                    f"complexity mismatch: {commit} {entry.title!r} "
                    f"header={entry.effective_header_complexity} computed={entry.computed_complexity}",
                    file=sys.stderr,
                )
        if unscoped:
            for entry in unscoped:
                commit = entry.commit or "latest"
                print(f"missing subsystem prefix: {commit} {entry.title!r}", file=sys.stderr)
        if mismatches or complexity_mismatches or unscoped:
            return 1

    if not args.include_latest:
        entries = [entry for entry in entries if not entry.is_latest]

    if args.group_by == "entry":
        rows = [entry.as_row() for entry in entries]
    elif args.group_by == "day":
        rows = build_daily_rows(entries, args.include_latest)
    elif args.group_by == "overall":
        rows = build_overall_rows(entries, args.include_latest)
    elif args.group_by == "subsystem":
        rows = build_subsystem_rows(entries, args.include_latest)
    else:
        rows = build_day_subsystem_rows(entries, args.include_latest)
    emit_rows(rows, args.format)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
