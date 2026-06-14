#!/usr/bin/env python3
"""Apply student identity fields to the report sources."""

from __future__ import annotations

import argparse
import html
import os
import re
from pathlib import Path


def require_value(name: str, value: str | None) -> str:
    if not value:
        raise SystemExit(f"Missing required value: {name}")
    return value


def latex_escape(value: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in value)


def replace_one(pattern: str, replacement: str, text: str, label: str) -> str:
    next_text, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise SystemExit(f"Could not update {label}; pattern matched {count} times")
    return next_text


def update_tex(path: Path, student_id: str, name: str, email: str) -> None:
    text = path.read_text(encoding="utf-8")
    escaped_name = latex_escape(name)
    escaped_id = latex_escape(student_id)
    escaped_email = latex_escape(email)
    text = replace_one(
        r"\\icmlauthor\{[^{}]+\}\{student\}",
        rf"\\icmlauthor{{{escaped_name}}}{{student}}",
        text,
        "LaTeX author",
    )
    text = replace_one(
        r"\\icmlaffiliation\{student\}\{[^{}]+\}",
        rf"\\icmlaffiliation{{student}}{{Student ID: {escaped_id}}}",
        text,
        "LaTeX affiliation",
    )
    text = replace_one(
        r"\\icmlcorrespondingauthor\{[^{}]+\}\{[^{}]+\}",
        rf"\\icmlcorrespondingauthor{{{escaped_name}}}{{{escaped_email}}}",
        text,
        "LaTeX corresponding author",
    )
    path.write_text(text, encoding="utf-8")


def update_html(path: Path, student_id: str, name: str, email: str) -> None:
    text = path.read_text(encoding="utf-8")
    meta = (
        f'<div class="meta">Student ID: {html.escape(student_id)} &nbsp; '
        f"Name: {html.escape(name)} &nbsp; Email: {html.escape(email)}</div>"
    )
    text = replace_one(r'<div class="meta">.*?</div>', meta, text, "HTML metadata")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--student-id", default=os.environ.get("STUDENT_ID"))
    parser.add_argument("--name", default=os.environ.get("STUDENT_NAME"))
    parser.add_argument("--email", default=os.environ.get("STUDENT_EMAIL"))
    parser.add_argument("--tex", type=Path, default=Path("report/main.tex"))
    parser.add_argument("--html", type=Path, default=Path("report/report.html"))
    args = parser.parse_args()

    student_id = require_value("STUDENT_ID or --student-id", args.student_id)
    name = require_value("STUDENT_NAME or --name", args.name)
    email = require_value("STUDENT_EMAIL or --email", args.email)

    update_tex(args.tex, student_id, name, email)
    update_html(args.html, student_id, name, email)
    print(f"updated {args.tex}")
    print(f"updated {args.html}")


if __name__ == "__main__":
    main()
