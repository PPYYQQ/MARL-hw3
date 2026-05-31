#!/usr/bin/env python3
"""Write a compact status snapshot for full HARL training runs."""

from __future__ import annotations

import argparse
import csv
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class ProgressSummary:
    rows: int
    final_step_value: float
    final_step: str
    final_reward: str
    final_win_rate: str
    modified: str
    age_minutes: float


def run_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, check=False)


def tmux_status(session: str) -> str:
    result = run_command(["tmux", "has-session", "-t", session])
    return "active" if result.returncode == 0 else "inactive"


def parse_progress(path: Path, now: datetime) -> ProgressSummary | None:
    if not path.is_file() or path.stat().st_size == 0:
        return None
    rows: list[list[str]] = []
    with path.open(encoding="utf-8") as file:
        for row in csv.reader(file):
            if len(row) < 3:
                continue
            try:
                float(row[0])
                float(row[1])
                float(row[2])
            except ValueError:
                continue
            rows.append(row)
    if not rows:
        return None
    final = rows[-1]
    modified_at = datetime.fromtimestamp(path.stat().st_mtime).astimezone()
    modified = modified_at.strftime("%Y-%m-%d %H:%M:%S %Z")
    final_step_value = float(final[0])
    return ProgressSummary(
        rows=len(rows),
        final_step_value=final_step_value,
        final_step=f"{final_step_value:.0f}",
        final_reward=f"{float(final[1]):.4f}",
        final_win_rate=f"{float(final[2]):.4f}",
        modified=modified,
        age_minutes=max(0.0, (now - modified_at).total_seconds() / 60.0),
    )


def discover_full_progress(source: Path, exp_prefix: str) -> list[Path]:
    if not source.exists():
        return []
    return sorted(path for path in source.rglob("progress.txt") if exp_prefix in path.as_posix() and "_full_" in path.as_posix())


def raw_path_for(source_path: Path, source_root: Path, raw_root: Path) -> Path:
    return raw_root / source_path.relative_to(source_root)


def run_state(summary: ProgressSummary, target_steps: int, stale_minutes: int) -> str:
    if summary.final_step_value >= target_steps:
        return "complete"
    if summary.age_minutes >= stale_minutes:
        return "no recent progress"
    return "in progress"


def render_snapshot(source_root: Path, raw_root: Path, session: str, exp_prefix: str, target_steps: int, stale_minutes: int) -> str:
    now = datetime.now().astimezone()
    generated = now.strftime("%Y-%m-%d %H:%M:%S %Z")
    lines = [
        "# Full Training Snapshot",
        "",
        f"- Generated: {generated}",
        f"- tmux session `{session}`: {tmux_status(session)}",
        f"- Source: `{source_root}`",
        f"- Synced raw root: `{raw_root}`",
        f"- Target full steps: {target_steps}",
        f"- Stale threshold: {stale_minutes} minutes without a new external `progress.txt` row",
        "",
        "| Map | Algo | External rows | External final step | External final win | Synced rows | Synced final step | Sync status | Run state | External age min | External modified |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: | --- |",
    ]

    attention: list[str] = []
    for source_path in discover_full_progress(source_root, exp_prefix):
        relative = source_path.relative_to(source_root)
        parts = relative.parts
        if len(parts) < 6:
            continue
        map_name = parts[1]
        algo = parts[2]
        external = parse_progress(source_path, now)
        synced = parse_progress(raw_path_for(source_path, source_root, raw_root), now)
        if external is None:
            continue
        if synced is None:
            sync_status = "not synced"
            synced_rows = "0"
            synced_step = "0"
        else:
            sync_status = "synced" if external.rows == synced.rows and external.final_step == synced.final_step else "external ahead"
            synced_rows = str(synced.rows)
            synced_step = synced.final_step
        state = run_state(external, target_steps, stale_minutes)
        if state == "no recent progress":
            attention.append(
                f"- `{algo}` + `{map_name}` is incomplete at {external.final_step} steps and has no new external progress for {external.age_minutes:.1f} minutes."
            )
        lines.append(
            f"| `{map_name}` | {algo} | {external.rows} | {external.final_step} | {external.final_win_rate} | {synced_rows} | {synced_step} | {sync_status} | {state} | {external.age_minutes:.1f} | {external.modified} |"
        )

    if attention:
        lines.extend(["", "## Attention", "", *attention])
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("external/HARL/examples/results"))
    parser.add_argument("--raw-root", type=Path, default=Path("results/raw/full"))
    parser.add_argument("--session", default="hw3_full_20260531_seed1")
    parser.add_argument("--exp-prefix", default="hw3_full")
    parser.add_argument("--target-steps", type=int, default=20_000_000)
    parser.add_argument("--stale-minutes", type=int, default=120)
    parser.add_argument("--output", type=Path, default=Path("logs/full_training_snapshot.md"))
    args = parser.parse_args()

    snapshot = render_snapshot(args.source, args.raw_root, args.session, args.exp_prefix, args.target_steps, args.stale_minutes)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(snapshot, encoding="utf-8")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()
