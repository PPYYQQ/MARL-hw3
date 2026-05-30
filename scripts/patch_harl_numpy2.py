#!/usr/bin/env python3
"""Patch HARL source for NumPy 2 compatibility."""

from __future__ import annotations

import argparse
from pathlib import Path


REPLACEMENTS = {
    Path("harl/envs/smac/smac_logger.py"): {
        "dtype=np.int": "dtype=int",
    },
    Path("harl/envs/smac/StarCraft2_Env.py"): {
        "dtype=np.bool": "dtype=bool",
    },
    Path("harl/runners/off_policy_base_runner.py"): {
        "dtype=np.int": "dtype=int",
    },
}


def patch_file(path: Path, replacements: dict[str, str]) -> bool:
    text = path.read_text(encoding="utf-8")
    patched = text
    for old, new in replacements.items():
        patched = patched.replace(old, new)
    if patched == text:
        return False
    path.write_text(patched, encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "harl_dir",
        type=Path,
        nargs="?",
        default=Path("external/HARL"),
        help="Path to the HARL repository.",
    )
    args = parser.parse_args()

    changed_files: list[Path] = []
    for relative_path, replacements in REPLACEMENTS.items():
        target = args.harl_dir / relative_path
        if not target.exists():
            raise FileNotFoundError(target)
        if patch_file(target, replacements):
            changed_files.append(target)

    if changed_files:
        print("patched:")
        for path in changed_files:
            print(path)
    else:
        print("no changes needed")


if __name__ == "__main__":
    main()
