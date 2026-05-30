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
| `report/main.pdf` | OK | 797747 bytes; 3 pages |
| `results/processed/progress_summary.csv` | OK | 79 data rows |
| `results/raw/smoke` | OK | 4 progress.txt files; expected at least 4 |
| `results/raw/pilot` | OK | 4 progress.txt files; expected at least 4 |
| `results/raw/full` | WARN | 1 progress.txt files; full training not complete |
| `configs/smac` | OK | 4 config.json files; expected at least 4 |
| `report/main.tex` | WARN | student identity placeholders still present |
| `report/report.html` | WARN | student identity placeholders still present |
| `git remote origin` | OK | https://github.com/PPYYQQ/MARL-hw3.git |
| `git upstream` | WARN | branch `main` has no upstream; push with `git push -u origin main` |

## Summary

- Failures: 0
- Warnings: 4
- GitHub push is not validated here; `PROGRESS.md` records the current credential blocker.
- Student identity fields are warnings because they require user-provided name, ID and email.
- `results/raw/full` remains a warning until full training progress files are synced.
