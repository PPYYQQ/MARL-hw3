#!/usr/bin/env python3
"""Generate a deterministic manifest for submitted HW3 artifacts."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


INCLUDE_PATHS = [
    Path("AGENTS.md"),
    Path("README.md"),
    Path("SUBMISSION.md"),
    Path("TRAINING.md"),
    Path("report"),
    Path("figures"),
    Path("configs"),
    Path("scripts"),
    Path("results/processed"),
    Path("results/raw/smoke"),
    Path("results/raw/pilot"),
    Path("results/raw/full"),
    Path("logs"),
]

EXCLUDED_NAMES = {
    "artifact_manifest.md",
    "submission_validation.md",
}

EXCLUDED_DIR_NAMES = {
    "__pycache__",
}

EXCLUDED_SUFFIXES = {
    ".aux",
    ".bbl",
    ".blg",
    ".fdb_latexmk",
    ".fls",
    ".log",
    ".out",
    ".pyc",
    ".pyo",
    ".synctex.gz",
    ".toc",
}


def is_excluded(path: Path) -> bool:
    if path.name in EXCLUDED_NAMES:
        return True
    if any(part in EXCLUDED_DIR_NAMES for part in path.parts):
        return True
    return any(str(path).endswith(suffix) for suffix in EXCLUDED_SUFFIXES)


def discover_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        if path.is_file() and not is_excluded(path):
            candidates = [path]
        elif path.is_dir():
            candidates = [candidate for candidate in path.rglob("*") if candidate.is_file() and not is_excluded(candidate)]
        else:
            continue
        for candidate in candidates:
            normalized = Path(candidate)
            if normalized in seen:
                continue
            seen.add(normalized)
            files.append(normalized)
    return sorted(files, key=lambda item: item.as_posix())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def render_manifest(files: list[Path]) -> str:
    lines = [
        "# Artifact Manifest",
        "",
        "This manifest records deterministic SHA256 hashes for submitted source, report, config and result artifacts.",
        "",
        "| Path | Size | SHA256 |",
        "| --- | ---: | --- |",
    ]
    total_size = 0
    for path in files:
        size = path.stat().st_size
        total_size += size
        lines.append(f"| `{path.as_posix()}` | {size} | `{sha256(path)}` |")
    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Files: {len(files)}",
            f"- Total bytes: {total_size}",
            "- Excludes generated validation and manifest files to avoid self-referential churn.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("logs/artifact_manifest.md"),
        help="Manifest output path.",
    )
    args = parser.parse_args()

    files = discover_files(INCLUDE_PATHS)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_manifest(files), encoding="utf-8")
    print(f"files={len(files)}")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()
