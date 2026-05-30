# Submission Checklist

本文件记录交付前需要完成的动作，以及当前哪些内容已经可以作为补充材料提交。

## 当前可提交内容

- `report/main.tex`：ICML2022 模板下的报告草稿，已包含算法简介、HARL 代码对应、环境配置、实验设置、smoke test 结果和后续正式训练说明。
- `report/references.bib`：MAPPO、HAPPO/HARL、SMAC 的参考文献。
- `scripts/`：环境安装、HARL NumPy 2 兼容补丁、实验运行、`progress.txt` 汇总和 win rate 绘图脚本。
- `configs/smac/`：MAPPO/HAPPO × `3s5z`/`8m_vs_9m` 的配置快照。
- `results/raw/smoke/`：4 组 smoke test 的原始 `progress.txt`。
- `results/raw/pilot/`：4 组 10000-step pilot 的原始 `progress.txt`。
- `results/processed/progress_summary.csv`、`results/processed/progress_summary.md`：smoke test 与 pilot 的汇总结果。
- `figures/win_rate_3s5z.png`、`figures/win_rate_8m_vs_9m.png`：smoke/pilot 曲线。
- `logs/`：作业摘要、安装记录、代码阅读笔记、实验笔记。
- `TRAINING.md`：正式训练资源需求、推荐命令和结果整理说明。

## 仍需人工确认

- 学号、姓名、邮箱：需要填入 `report/main.tex`。
- GitHub push：`origin` 已配置为 `https://github.com/PPYYQQ/MARL-hw3.git`，但非交互式 HTTPS push 缺少 GitHub 凭据；当前系统也未安装 `gh`。
- LaTeX 编译器：当前系统没有 `xelatex` 或 `pdflatex`；PDF 已通过 Chrome HTML 导出流程生成。
- 正式训练：当前完成 1000-step smoke test 和 4 组 10000-step pilot，未完成 HARL tuned config 的完整训练。

## GitHub 同步

配置 GitHub 凭据后执行：

```bash
git push -u origin main
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
conda run -n harl_hw3 bash scripts/run_smac_experiments.sh full
```

训练完成后生成曲线：

```bash
python3 scripts/collect_progress.py
conda run -n harl_hw3 python scripts/plot_win_rate.py
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

不要包含：

- `external/`
- `/home/yongqian/StarCraftII`
- `/home/yongqian/SC2.4.10.zip`
- 大型模型 checkpoint

可用脚本生成当前 smoke 版交付包：

```bash
STUDENT_ID=<id> STUDENT_NAME=<name> bash scripts/package_submission.sh
```

输出位于 `dist/`，该目录不会纳入 Git 提交。正式训练完成后，先更新报告、图和汇总 CSV，再重新运行打包脚本。
