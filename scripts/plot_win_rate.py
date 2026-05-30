#!/usr/bin/env python3
"""Plot SMAC eval win rate curves from HARL progress.txt files."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from collect_progress import discover_progress_files, read_progress_rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "roots",
        nargs="*",
        type=Path,
        default=[
            Path("external/HARL/examples/results"),
            Path("external/HARL/results"),
            Path("results/raw"),
        ],
        help="Progress files or directories to scan.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("figures"),
        help="Directory for generated figures.",
    )
    parser.add_argument(
        "--maps",
        nargs="*",
        default=["3s5z", "8m_vs_9m"],
        help="SMAC maps to plot.",
    )
    args = parser.parse_args()

    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit("matplotlib is required: python -m pip install matplotlib") from exc

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for path in discover_progress_files(args.roots):
        for row in read_progress_rows(path):
            if row["map"] in args.maps:
                grouped[row["map"]].append(row)

    if not grouped:
        raise SystemExit("No matching progress rows found.")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for map_name in args.maps:
        rows = grouped.get(map_name, [])
        if not rows:
            print(f"skip {map_name}: no rows")
            continue

        by_run: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
        for row in rows:
            by_run[(row["algo"], row["run"])].append(row)

        plt.figure(figsize=(7.0, 4.2))
        for (algo, run), run_rows in sorted(by_run.items()):
            run_rows.sort(key=lambda item: float(item["step"]))
            steps = [float(item["step"]) for item in run_rows]
            win_rates = [float(item["eval_win_rate"]) for item in run_rows]
            label = f"{algo} {run}"
            plt.plot(steps, win_rates, label=label, linewidth=1.8)

        plt.title(f"SMAC {map_name} eval win rate")
        plt.xlabel("environment steps")
        plt.ylabel("eval win rate")
        plt.ylim(-0.02, 1.02)
        plt.grid(True, alpha=0.25)
        plt.legend(fontsize=8)
        plt.tight_layout()
        output = args.output_dir / f"win_rate_{map_name}.png"
        plt.savefig(output, dpi=200)
        plt.close()
        print(f"wrote {output}")


if __name__ == "__main__":
    main()
