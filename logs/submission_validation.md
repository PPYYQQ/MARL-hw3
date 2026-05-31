# Submission Validation

| Check | Status | Detail |
| --- | --- | --- |
| `AGENTS.md` | OK | file present |
| `README.md` | OK | file present |
| `PROGRESS.md` | OK | file present |
| `SUBMISSION.md` | OK | file present |
| `TRAINING.md` | OK | file present |
| `report/main.pdf` | OK | file present |
| `report/main.tex` | OK | file present |
| `report/report.html` | OK | file present |
| `report/references.bib` | OK | file present |
| `figures/win_rate_3s5z.png` | OK | file present |
| `figures/win_rate_8m_vs_9m.png` | OK | file present |
| `results/processed/progress_summary.csv` | OK | file present |
| `results/processed/progress_summary.md` | OK | file present |
| `logs/artifact_manifest.md` | OK | file present |
| `scripts` | OK | directory present |
| `configs/smac` | OK | directory present |
| `logs` | OK | directory present |
| `results/raw/smoke` | OK | directory present |
| `results/raw/pilot` | OK | directory present |
| `report/main.pdf` | OK | 918349 bytes; 3 pages |
| `results/processed/progress_summary.csv` | OK | 608 data rows |
| `results/raw/smoke` | OK | 4 progress.txt files; expected at least 4 |
| `results/raw/pilot` | OK | 4 progress.txt files; expected at least 4 |
| `results/raw/full` | WARN | 3 progress.txt files; full training not complete |
| `configs/smac` | OK | 4 config.json files; expected at least 4 |
| `report/main.tex` | WARN | student identity placeholders still present |
| `report/report.html` | WARN | student identity placeholders still present |
| `git remote origin` | OK | git@github.com:PPYYQQ/MARL-hw3.git |
| `git upstream` | OK | branch is synchronized with upstream |

## Summary

- Failures: 0
- Warnings: 3
- GitHub push state is checked through the git upstream status; `PROGRESS.md` records the push history.
- Student identity fields are warnings because they require user-provided name, ID and email.
- `results/raw/full` remains a warning until full training progress files are synced.
