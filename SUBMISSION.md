# Submission Checklist

本文件记录交付前需要完成的动作，以及当前哪些内容已经可以作为补充材料提交。

## 当前可提交内容

- `report/main.tex`：ICML2022 模板下的英文最终报告，已包含算法简介、HARL 代码对应、环境配置、实验设置、smoke/pilot 结果和单 seed full 矩阵最终结果。
- `report/references.bib`：MAPPO、HAPPO/HARL、SMAC 的参考文献。
- `scripts/`：环境安装、HARL NumPy 2 兼容补丁、实验运行、`progress.txt` 汇总和 win rate 绘图脚本。
- `configs/smac/`：MAPPO/HAPPO × `3s5z`/`8m_vs_9m` 的配置快照。
- `results/raw/smoke/`：4 组 smoke test 的原始 `progress.txt`。
- `results/raw/pilot/`：4 组 10000-step pilot 的原始 `progress.txt`。
- `results/raw/full/`：正式训练同步进来的 `progress.txt`；当前包含 MAPPO/HAPPO × `3s5z`/`8m_vs_9m` 的单 seed 20000000-step 结果，并保留 `HAPPO` + `8m_vs_9m` 原始 stale run 的 5120000-step checkpoint 作为审计记录。
- `results/processed/progress_summary.csv`、`results/processed/progress_summary.md`：smoke test、pilot 与 full checkpoint 的汇总结果。
- `figures/win_rate_3s5z.png`、`figures/win_rate_8m_vs_9m.png`：smoke/pilot 与 full 曲线。
- `figures/teaser_smac_8m_vs_9m.png`：真实 SMAC renderer 截图，用作英文报告 teaser figure。
- `logs/`：作业摘要、安装记录、代码阅读笔记、实验笔记和 full training 快照。
- `logs/artifact_manifest.md`：提交产物的文件大小与 SHA256 清单。
- `logs/submission_validation.md`：提交前产物完整性检查；full training matrix 已通过，当前 warning 只剩学生身份占位符。
- `dist/marl_hw3_overleaf.zip`：通过 `scripts/package_overleaf_report.sh` 生成的 Overleaf 可上传 LaTeX 项目包；`dist/` 默认不纳入 Git。
- `TRAINING.md`：正式训练资源需求、推荐命令和结果整理说明。

## 仍需人工确认

- 学号、姓名、邮箱：需要填入 `report/main.tex`。
- GitHub push：`origin` 已切换为 `git@github.com:PPYYQQ/MARL-hw3.git`；SSH 认证已通过，`main` 已同步到 `origin/main`。
- LaTeX 编译器：本次最终交付按 Overleaf 项目 zip 准备，本地无需编译 PDF。
- 正式训练：当前完成 1000-step smoke test、4 组 10000-step pilot，以及 MAPPO/HAPPO × `3s5z`/`8m_vs_9m` 单 seed full 矩阵；`HAPPO` + `8m_vs_9m` 原始 run 停在 5120000 steps，recovery run `hw3_recover_happo_8m` 已完成并同步到 20000000 steps。

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

如果快照显示某个 run 长时间没有新 `progress.txt` 行，保留原始 run，并用新的 session/prefix 单独恢复缺失组合。当前 `HAPPO` + `8m_vs_9m` 已按此流程完成 recovery run：

```bash
SESSION=hw3_recover_happo_8m SEEDS=1 MAPS=8m_vs_9m ALGOS=happo EXP_PREFIX=hw3_recover bash scripts/launch_training_tmux.sh full
```

训练结果更新后，重新生成报告与提交产物并提交：

```bash
git add report/main.tex results/processed/progress_summary.csv figures/
git commit -m "docs: add full SMAC training results"
git push
```

如需重新生成环境 teaser 截图：

```bash
SDL_VIDEODRIVER=dummy conda run -n harl_hw3 python scripts/capture_smac_teaser.py
```

## Overleaf 项目 zip

生成只包含 LaTeX 报告、ICML 样式、参考文献和图片的 Overleaf 项目：

```bash
bash scripts/package_overleaf_report.sh
```

输出：

```text
dist/marl_hw3_overleaf.zip
```

上传到 Overleaf 后，入口文件为 `main.tex`，建议使用 pdfLaTeX 编译。正式提交前先替换 `Student Name`、`Student ID: TODO` 和 `email@example.com`。

## 打包建议

如果课程仍要求完整归档包，压缩包命名格式为“学号+姓名+作业名称”。建议包含：

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

可用脚本生成完整归档包：

```bash
STUDENT_ID=<id> STUDENT_NAME=<name> bash scripts/package_submission.sh
```

完整归档打包前建议先运行：

```bash
STUDENT_ID=<id> STUDENT_NAME=<name> STUDENT_EMAIL=<email> python3 scripts/apply_student_info.py
bash scripts/build_report_pdf.sh
```

也可以直接执行完整准备流程：

```bash
STUDENT_ID=<id> STUDENT_NAME=<name> STUDENT_EMAIL=<email> bash scripts/prepare_submission.sh
```

打包脚本会先运行 `python3 scripts/validate_submission.py`，若存在失败项则停止打包；当前姓名、学号、邮箱占位符只会产生 warning。输出位于 `dist/`，该目录不会纳入 Git 提交。正式提交前提供学生身份信息后，再重新运行 Overleaf zip 或完整归档脚本。
