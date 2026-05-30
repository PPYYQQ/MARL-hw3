#!/usr/bin/env python3
"""Copy HARL progress.txt files into the tracked results/raw tree."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


MODES = {"smoke", "pilot", "full"}


def mode_for_progress(path: Path, source: Path) -> str | None:
    try:
        relative = path.relative_to(source)
    except ValueError:
        return None
    parts = relative.parts
    if len(parts) < 5:
        return None
    exp_name = parts[3]
    for mode in MODES:
        if mode in exp_name:
            return mode
    return None


def discover_progress_files(source: Path, mode: str) -> list[tuple[Path, str]]:
    files: list[tuple[Path, str]] = []
    if not source.exists():
        return files
    for path in sorted(source.rglob("progress.txt")):
        detected_mode = mode_for_progress(path, source)
        if detected_mode is None:
            continue
        if mode != "all" and detected_mode != mode:
            continue
        files.append((path, detected_mode))
    return files


def copy_progress_files(source: Path, destination: Path, mode: str, dry_run: bool) -> int:
    copied = 0
    for path, detected_mode in discover_progress_files(source, mode):
        relative = path.relative_to(source)
        target = destination / detected_mode / relative
        print(f"{path} -> {target}")
        if dry_run:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        copied += 1
    return copied


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("external/HARL/examples/results"),
        help="HARL results root to scan.",
    )
    parser.add_argument(
        "--destination",
        type=Path,
        default=Path("results/raw"),
        help="Tracked raw results root.",
    )
    parser.add_argument(
        "--mode",
        choices=["all", *sorted(MODES)],
        default="full",
        help="Which result mode to sync. Defaults to full to avoid changing smoke/pilot archives.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print copy operations without writing files.",
    )
    args = parser.parse_args()

    copied = copy_progress_files(args.source, args.destination, args.mode, args.dry_run)
    print(f"copied={copied}")
    print(f"mode={args.mode}")
    print(f"source={args.source}")
    print(f"destination={args.destination}")


if __name__ == "__main__":
    main()
