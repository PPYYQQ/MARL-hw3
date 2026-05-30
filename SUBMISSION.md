# Submission Checklist

本文件记录交付前需要完成的动作，以及当前哪些内容已经可以作为补充材料提交。

## 当前可提交内容

- `report/main.tex`：ICML2022 模板下的报告草稿，已包含算法简介、HARL 代码对应、环境配置、实验设置、smoke test 结果和后续正式训练说明。
- `report/references.bib`：MAPPO、HAPPO/HARL、SMAC 的参考文献。
- `scripts/`：环境安装、HARL NumPy 2 兼容补丁、实验运行、`progress.txt` 汇总和 win rate 绘图脚本。
- `results/raw/smoke/`：4 组 smoke test 的原始 `progress.txt`。
- `results/processed/progress_summary.csv`：smoke test 的汇总结果。
- `figures/win_rate_3s5z.png`、`figures/win_rate_8m_vs_9m.png`：smoke test 曲线。
- `logs/`：作业摘要、安装记录、代码阅读笔记、实验笔记。

## 仍需人工确认

- 学号、姓名、邮箱：需要填入 `report/main.tex`。
- GitHub remote：当前本地仓库没有 remote，且未安装 `gh`，无法自动 push 到 GitHub。
- LaTeX 编译器：当前系统没有 `xelatex` 或 `pdflatex`，无法在本机直接导出 PDF。
- 正式训练：当前只完成 1000-step smoke test，未完成 HARL tuned config 的完整训练。

## GitHub 同步

配置 remote 后执行：

```bash
git remote add origin <your-github-repo-url>
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

安装 LaTeX 后，在仓库根目录执行：

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
- `results/raw/smoke/`

不要包含：

- `external/`
- `/home/yongqian/StarCraftII`
- `/home/yongqian/SC2.4.10.zip`
- 大型模型 checkpoint
