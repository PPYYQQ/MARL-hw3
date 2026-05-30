#!/usr/bin/env python3
"""Validate the current HW3 submission artifacts."""

from __future__ import annotations

import argparse
import csv
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Check:
    name: str
    status: str
    detail: str


REQUIRED_FILES = [
    Path("AGENTS.md"),
    Path("README.md"),
    Path("PROGRESS.md"),
    Path("SUBMISSION.md"),
    Path("TRAINING.md"),
    Path("report/main.pdf"),
    Path("report/main.tex"),
    Path("report/report.html"),
    Path("report/references.bib"),
    Path("figures/win_rate_3s5z.png"),
    Path("figures/win_rate_8m_vs_9m.png"),
    Path("results/processed/progress_summary.csv"),
    Path("results/processed/progress_summary.md"),
    Path("logs/artifact_manifest.md"),
]

REQUIRED_DIRS = [
    Path("scripts"),
    Path("configs/smac"),
    Path("logs"),
    Path("results/raw/smoke"),
    Path("results/raw/pilot"),
]


def ok(name: str, detail: str) -> Check:
    return Check(name, "OK", detail)


def warn(name: str, detail: str) -> Check:
    return Check(name, "WARN", detail)


def fail(name: str, detail: str) -> Check:
    return Check(name, "FAIL", detail)


def file_check(path: Path) -> Check:
    if not path.is_file():
        return fail(str(path), "missing file")
    if path.stat().st_size == 0:
        return fail(str(path), "empty file")
    return ok(str(path), "file present")


def dir_check(path: Path) -> Check:
    if not path.is_dir():
        return fail(str(path), "missing directory")
    return ok(str(path), "directory present")


def count_progress(root: Path, expected: int) -> Check:
    files = sorted(root.rglob("progress.txt")) if root.exists() else []
    status = ok if len(files) >= expected else fail
    return status(str(root), f"{len(files)} progress.txt files; expected at least {expected}")


def optional_progress_check(root: Path, expected: int) -> Check:
    files = sorted(root.rglob("progress.txt")) if root.exists() else []
    if len(files) >= expected:
        return ok(str(root), f"{len(files)} progress.txt files; expected at least {expected}")
    return warn(str(root), f"{len(files)} progress.txt files; full training not complete")


def count_configs(root: Path, expected: int) -> Check:
    files = sorted(root.rglob("config.json")) if root.exists() else []
    status = ok if len(files) >= expected else fail
    return status(str(root), f"{len(files)} config.json files; expected at least {expected}")


def progress_csv_check(path: Path) -> Check:
    if not path.is_file():
        return fail(str(path), "missing CSV")
    with path.open(encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    required = {"map", "algo", "exp", "run", "step", "eval_average_episode_reward", "eval_win_rate", "path"}
    missing = required.difference(rows[0].keys() if rows else set())
    if missing:
        return fail(str(path), f"missing columns: {', '.join(sorted(missing))}")
    if len(rows) < 72:
        return fail(str(path), f"{len(rows)} rows; expected at least 72")
    return ok(str(path), f"{len(rows)} data rows")


def pdf_check(path: Path) -> Check:
    base = file_check(path)
    if base.status != "OK":
        return base
    try:
        result = subprocess.run(
            ["pdfinfo", str(path)],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return warn(str(path), f"{path.stat().st_size} bytes; pdfinfo unavailable")

    pages = "unknown"
    for line in result.stdout.splitlines():
        if line.startswith("Pages:"):
            pages = line.split(":", 1)[1].strip()
            break
    if pages != "unknown" and int(pages) < 3:
        return fail(str(path), f"{pages} pages; expected at least 3")
    return ok(str(path), f"{path.stat().st_size} bytes; {pages} pages")


def placeholder_check(path: Path) -> Check:
    if not path.is_file():
        return fail(str(path), "missing report source")
    text = path.read_text(encoding="utf-8")
    placeholders = ["待填写", "email@example.com", "\\icmlauthor{姓名}"]
    found = [placeholder for placeholder in placeholders if placeholder in text]
    if found:
        return warn(str(path), "student identity placeholders still present")
    return ok(str(path), "student identity placeholders not found")


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        check=False,
        capture_output=True,
        text=True,
    )


def git_remote_check() -> Check:
    result = run_git(["remote", "get-url", "origin"])
    if result.returncode != 0:
        return fail("git remote origin", "origin remote is not configured")
    url = result.stdout.strip()
    if not url:
        return fail("git remote origin", "origin remote URL is empty")
    return ok("git remote origin", url)


def git_upstream_check() -> Check:
    branch = run_git(["branch", "--show-current"])
    branch_name = branch.stdout.strip() or "unknown"
    upstream = run_git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
    if upstream.returncode != 0:
        return warn("git upstream", f"branch `{branch_name}` has no upstream; push with `git push -u origin {branch_name}`")

    left_right = run_git(["rev-list", "--left-right", "--count", "HEAD...@{u}"])
    if left_right.returncode != 0:
        return warn("git upstream", "upstream exists but ahead/behind count is unavailable")
    ahead, behind = left_right.stdout.split()
    if ahead != "0" or behind != "0":
        return warn("git upstream", f"ahead {ahead}, behind {behind}")
    return ok("git upstream", "branch is synchronized with upstream")


def render_markdown(checks: list[Check]) -> str:
    lines = [
        "# Submission Validation",
        "",
        "| Check | Status | Detail |",
        "| --- | --- | --- |",
    ]
    for check in checks:
        lines.append(f"| `{check.name}` | {check.status} | {check.detail} |")

    failures = sum(check.status == "FAIL" for check in checks)
    warnings = sum(check.status == "WARN" for check in checks)
    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Failures: {failures}",
            f"- Warnings: {warnings}",
            "- GitHub push is not validated here; `PROGRESS.md` records the current credential blocker.",
            "- Student identity fields are warnings because they require user-provided name, ID and email.",
            "- `results/raw/full` remains a warning until full training progress files are synced.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("logs/submission_validation.md"),
        help="Markdown validation report.",
    )
    args = parser.parse_args()

    checks: list[Check] = []
    checks.extend(file_check(path) for path in REQUIRED_FILES)
    checks.extend(dir_check(path) for path in REQUIRED_DIRS)
    checks.append(pdf_check(Path("report/main.pdf")))
    checks.append(progress_csv_check(Path("results/processed/progress_summary.csv")))
    checks.append(count_progress(Path("results/raw/smoke"), expected=4))
    checks.append(count_progress(Path("results/raw/pilot"), expected=4))
    checks.append(optional_progress_check(Path("results/raw/full"), expected=4))
    checks.append(count_configs(Path("configs/smac"), expected=4))
    checks.append(placeholder_check(Path("report/main.tex")))
    checks.append(placeholder_check(Path("report/report.html")))
    checks.append(git_remote_check())
    checks.append(git_upstream_check())

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_markdown(checks), encoding="utf-8")
    failures = sum(check.status == "FAIL" for check in checks)
    warnings = sum(check.status == "WARN" for check in checks)
    print(f"checks={len(checks)}")
    print(f"failures={failures}")
    print(f"warnings={warnings}")
    print(f"output={args.output}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
