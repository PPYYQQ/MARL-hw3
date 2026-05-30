#!/usr/bin/env python3
"""Collect HARL progress.txt files into one CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def discover_progress_files(roots: list[Path]) -> list[Path]:
    files: list[Path] = []
    seen: set[Path] = set()
    for root in roots:
        candidates: list[Path] = []
        if root.is_file() and root.name == "progress.txt":
            candidates = [root]
        elif root.exists():
            candidates = sorted(root.rglob("progress.txt"))
        for candidate in candidates:
            if candidate in seen:
                continue
            seen.add(candidate)
            files.append(candidate)
    return files


def parse_metadata(path: Path) -> dict[str, str]:
    parts = path.parts
    for index, part in enumerate(parts):
        if part == "smac" and index + 4 < len(parts):
            return {
                "map": parts[index + 1],
                "algo": parts[index + 2],
                "exp": parts[index + 3],
                "run": parts[index + 4],
            }
    return {"map": "unknown", "algo": "unknown", "exp": "unknown", "run": path.parent.name}


def read_progress_rows(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    metadata = parse_metadata(path)
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        fields = [field.strip() for field in line.split(",")]
        if len(fields) < 3:
            fields = line.split()
        if len(fields) < 3 or any(char.isalpha() for char in fields[0]):
            continue
        rows.append(
            {
                **metadata,
                "step": fields[0],
                "eval_average_episode_reward": fields[1],
                "eval_win_rate": fields[2],
                "path": str(path),
            }
        )
    return rows


def deduplicate_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    unique_rows: list[dict[str, str]] = []
    seen: set[tuple[str, str, str, str, str, str, str]] = set()
    for row in rows:
        key = (
            row["map"],
            row["algo"],
            row["exp"],
            row["run"],
            row["step"],
            row["eval_average_episode_reward"],
            row["eval_win_rate"],
        )
        if key in seen:
            continue
        seen.add(key)
        unique_rows.append(row)
    return unique_rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "roots",
        nargs="*",
        type=Path,
        default=[
            Path("results/raw"),
            Path("external/HARL/examples/results"),
            Path("external/HARL/results"),
        ],
        help="Progress files or directories to scan.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/processed/progress_summary.csv"),
        help="CSV output path.",
    )
    args = parser.parse_args()

    progress_files = discover_progress_files(args.roots)
    rows: list[dict[str, str]] = []
    for path in progress_files:
        rows.extend(read_progress_rows(path))
    rows = deduplicate_rows(rows)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "map",
        "algo",
        "exp",
        "run",
        "step",
        "eval_average_episode_reward",
        "eval_win_rate",
        "path",
    ]
    with args.output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"found_progress_files={len(progress_files)}")
    print(f"written_rows={len(rows)}")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()
