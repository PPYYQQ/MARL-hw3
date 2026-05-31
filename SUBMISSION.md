# Submission Checklist

本文件记录交付前需要完成的动作，以及当前哪些内容已经可以作为补充材料提交。

## 当前可提交内容

- `report/main.tex`：ICML2022 模板下的报告草稿，已包含算法简介、HARL 代码对应、环境配置、实验设置、smoke/pilot 结果、`3s5z` full 结果、`MAPPO` + `8m_vs_9m` full 结果和 `HAPPO` + `8m_vs_9m` 阶段性结果。
- `report/references.bib`：MAPPO、HAPPO/HARL、SMAC 的参考文献。
- `scripts/`：环境安装、HARL NumPy 2 兼容补丁、实验运行、`progress.txt` 汇总和 win rate 绘图脚本。
- `configs/smac/`：MAPPO/HAPPO × `3s5z`/`8m_vs_9m` 的配置快照。
- `results/raw/smoke/`：4 组 smoke test 的原始 `progress.txt`。
- `results/raw/pilot/`：4 组 10000-step pilot 的原始 `progress.txt`。
- `results/raw/full/`：正式训练同步进来的 `progress.txt`；当前包含 `MAPPO` + `3s5z`、`HAPPO` + `3s5z`、`MAPPO` + `8m_vs_9m` 的完整 20000000-step 结果，`HAPPO` + `8m_vs_9m` 原始 run 的 latest synced 5120000-step 早期 checkpoint，以及 recovery run 的 2160000-step checkpoint。
- `results/processed/progress_summary.csv`、`results/processed/progress_summary.md`：smoke test、pilot 与 full checkpoint 的汇总结果。
- `figures/win_rate_3s5z.png`、`figures/win_rate_8m_vs_9m.png`：smoke/pilot 与 full 曲线。
- `logs/`：作业摘要、安装记录、代码阅读笔记、实验笔记和 full training 快照。
- `logs/artifact_manifest.md`：提交产物的文件大小与 SHA256 清单。
- `logs/submission_validation.md`：提交前产物完整性检查；当前会把未完成的 full training matrix 标为 warning。
- `TRAINING.md`：正式训练资源需求、推荐命令和结果整理说明。

## 仍需人工确认

- 学号、姓名、邮箱：需要填入 `report/main.tex`。
- GitHub push：`origin` 已切换为 `git@github.com:PPYYQQ/MARL-hw3.git`；SSH 认证已通过，`main` 已同步到 `origin/main`。
- LaTeX 编译器：当前系统没有 `xelatex` 或 `pdflatex`；PDF 已通过 Chrome HTML 导出流程生成。
- 正式训练：当前完成 1000-step smoke test 和 4 组 10000-step pilot；单 seed full 训练已在 `hw3_full_20260531_seed1` 中运行，`MAPPO` + `3s5z`、`HAPPO` + `3s5z`、`MAPPO` + `8m_vs_9m` 均已同步完整 20000000-step 结果，`HAPPO` + `8m_vs_9m` 原始 run latest synced checkpoint 为 5120000 steps；recovery run `hw3_recover_happo_8m` 已同步到 2160000 steps。

## GitHub 同步

当前使用 SSH remote，正常同步命令为：

```bash
git push
```

若改回 HTTPS remote，也可以使用不会修改 remote URL 的 token 辅助脚本：

```bash
GITHUB_TOKEN=<token> bash scripts/push_to_github.sh
```

验证：

```bash
git remote -v
git status --short
git log --oneline --decorate -15
```

## 正式训练

正式训练会使用 tuned config 中的训练步数，当前 HAPPO tuned config 为 2000 万 environment steps。建议在 tmux 或服务器长期会话中运行：

```bash
conda run -n harl_hw3 bash scripts/run_smac_experiments.sh pilot
```

```bash
bash scripts/launch_training_tmux.sh full
```

训练完成后生成曲线：

```bash
python3 scripts/sync_harl_results.py --mode full
python3 scripts/collect_progress.py
python3 scripts/check_full_training_status.py
conda run -n harl_hw3 python scripts/plot_win_rate.py
```

如果快照显示 `HAPPO` + `8m_vs_9m` 长时间没有新 `progress.txt` 行，保留原始 run，并用新的 session/prefix 单独恢复缺失组合：

```bash
SESSION=hw3_recover_happo_8m SEEDS=1 MAPS=8m_vs_9m ALGOS=happo EXP_PREFIX=hw3_recover bash scripts/launch_training_tmux.sh full
```

然后更新 `report/main.tex` 的结果讨论，并提交：

```bash
git add report/main.tex results/processed/progress_summary.csv figures/
git commit -m "docs: add full SMAC training results"
git push
```

## PDF 导出

当前本机没有 LaTeX，但有 Chrome，已经可以用 HTML 版报告导出 PDF：

```bash
bash scripts/build_report_pdf.sh
```

安装 LaTeX 后，也可以在仓库根目录执行：

```bash
cd report
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

若使用 Word 版，则根据 `report/main.tex` 和 `logs/` 中的内容整理为双栏、单倍行距，并导出 PDF。

## 打包建议

压缩包命名格式为“学号+姓名+作业名称”。建议包含：

- `report/main.pdf`
- `report/main.tex`
- `report/references.bib`
- `figures/`
- `scripts/`
- `configs/`
- `logs/`
- `results/processed/progress_summary.csv`
- `results/processed/progress_summary.md`
- `results/raw/smoke/`
- `results/raw/pilot/`
- `results/raw/full/`，如果正式训练已经完成

不要包含：

- `external/`
- `/home/yongqian/StarCraftII`
- `/home/yongqian/SC2.4.10.zip`
- 大型模型 checkpoint

可用脚本生成当前 smoke 版交付包：

```bash
STUDENT_ID=<id> STUDENT_NAME=<name> bash scripts/package_submission.sh
```

打包前建议先运行：

```bash
STUDENT_ID=<id> STUDENT_NAME=<name> STUDENT_EMAIL=<email> python3 scripts/apply_student_info.py
bash scripts/build_report_pdf.sh
```

也可以直接执行完整准备流程：

```bash
STUDENT_ID=<id> STUDENT_NAME=<name> STUDENT_EMAIL=<email> bash scripts/prepare_submission.sh
```

打包脚本会先运行 `python3 scripts/validate_submission.py`，若存在失败项则停止打包；当前姓名、学号、邮箱占位符和未完成的 full training matrix 只会产生 warning。输出位于 `dist/`，该目录不会纳入 Git 提交。正式训练完成后，先更新报告、图和汇总 CSV，再重新运行打包脚本。
