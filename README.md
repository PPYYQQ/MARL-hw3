# MARL HW3: MAPPO/HAPPO on SMAC

本仓库用于完成“多智能体系统作业：星际争霸对战”。作业目标是阅读 MAPPO/HAPPO 相关实现，配置 HARL + SMAC 环境，在 `3s5z` 和 `8m_vs_9m` 上复现实验，绘制 win rate 曲线，并形成研究性报告。

## 当前完成度

- 环境：已完成 HARL、SMAC、StarCraft II Linux 4.10、SMAC maps、PyTorch/CUDA 环境配置与验证。
- 代码阅读：已定位 MAPPO/HAPPO actor update、HAPPO sequential factor、GAE return、SMAC win rate logging 等关键实现。
- 实验：已完成 4 组 smoke test、4 组 10000-step pilot，以及 MAPPO/HAPPO × `3s5z`/`8m_vs_9m` 单 seed 20000000-step full 矩阵。
- 报告：`report/main.tex` 已改为英文最终报告，可通过 Overleaf 项目 zip 上传编译；旧的 HTML/PDF 产物仅作历史辅助记录。
- 校验：`python3 scripts/validate_submission.py` 当前为 `31` 项检查、`0` failures、`2` warnings。
- 剩余：需要用户提供 `STUDENT_ID`、`STUDENT_NAME`、`STUDENT_EMAIL`，替换英文 LaTeX 报告中的身份占位符。

## 主要结果

| Map | Algorithm | Step | Final reward | Final win rate | Best win rate |
| --- | --- | ---: | ---: | ---: | ---: |
| `3s5z` | MAPPO | 20000000 | 19.8764 | 0.9750 | 1.0000 |
| `3s5z` | HAPPO | 20000000 | 19.3452 | 0.8750 | 1.0000 |
| `8m_vs_9m` | MAPPO | 20000000 | 18.9216 | 0.8750 | 0.9000 |
| `8m_vs_9m` | HAPPO recovery | 20000000 | 17.5288 | 0.7500 | 0.9750 |

说明：`HAPPO + 8m_vs_9m` 的原始 full run 停在 `5120000` steps；仓库保留该 stale run 的原始记录，并使用非破坏性 recovery run 完成同组合 full 结果。

## 仓库结构

- `AGENTS.md`：coding agent 工作规范、作业理解、项目架构预估、实施计划和测试计划。
- `PROGRESS.md`：逐步进度、关键 commit、验证命令和剩余事项追踪。
- `SUBMISSION.md`：交付前检查清单、GitHub 同步、Overleaf 项目 zip 和打包说明。
- `TRAINING.md`：正式训练资源需求、tmux 训练命令、监控和结果整理说明。
- `configs/smac/`：本次实验使用的 MAPPO/HAPPO × SMAC 配置快照。
- `figures/`：`3s5z` 与 `8m_vs_9m` 的 win rate 曲线，以及真实 SMAC renderer teaser 截图。
- `logs/`：代码阅读、安装、实验记录、训练快照、校验报告和产物 manifest。
- `report/`：英文 LaTeX 报告、参考文献、ICML 样式文件和历史 HTML/PDF 辅助产物。
- `results/raw/`：smoke、pilot、full 的原始 `progress.txt`。
- `results/processed/`：统一 CSV 与 Markdown 汇总结果。
- `scripts/`：环境安装、训练、同步、汇总、绘图、校验、PDF 导出和打包脚本。

`external/HARL/` 是本地运行依赖和代码阅读对象，不纳入本作业 Git 提交。

## 快速验证

```bash
python3 scripts/validate_submission.py
```

当前预期输出：

```text
checks=31
failures=0
warnings=2
output=logs/submission_validation.md
```

查看最终结果摘要：

```bash
sed -n '1,40p' results/processed/progress_summary.md
```

查看 full training 同步状态：

```bash
python3 scripts/check_full_training_status.py
sed -n '1,25p' logs/full_training_snapshot.md
```

## 复现实验流程

环境准备：

```bash
bash scripts/setup_env.sh
```

训练命令预览：

```bash
bash scripts/run_smac_experiments.sh dry-run
```

smoke test：

```bash
conda run -n harl_hw3 bash scripts/run_smac_experiments.sh smoke
```

pilot run：

```bash
conda run -n harl_hw3 bash scripts/run_smac_experiments.sh pilot
```

full run 建议放在 tmux 中运行：

```bash
SESSION=hw3_full_20260531_seed1 SEEDS=1 EXP_PREFIX=hw3_full bash scripts/launch_training_tmux.sh full
```

如果某个 full run 长时间不再写入 `progress.txt`，保留原始输出目录，并用新的 session 和 `EXP_PREFIX` 单独恢复缺失组合。当前 `HAPPO + 8m_vs_9m` 已通过以下命令完成 recovery：

```bash
SESSION=hw3_recover_happo_8m SEEDS=1 MAPS=8m_vs_9m ALGOS=happo EXP_PREFIX=hw3_recover bash scripts/launch_training_tmux.sh full
```

同步和整理结果：

```bash
python3 scripts/sync_harl_results.py --mode full
python3 scripts/collect_progress.py
python3 scripts/summarize_progress.py
python3 scripts/check_full_training_status.py
conda run -n harl_hw3 python scripts/plot_win_rate.py
```

重新生成真实环境 teaser 截图：

```bash
SDL_VIDEODRIVER=dummy conda run -n harl_hw3 python scripts/capture_smac_teaser.py
```

## 报告与打包

生成 Overleaf 可上传的 LaTeX 项目 zip：

```bash
bash scripts/package_overleaf_report.sh
```

输出为 `dist/marl_hw3_overleaf.zip`，zip 根目录内的入口文件是 `main.tex`。

补全学生身份信息：

```bash
STUDENT_ID=<id> STUDENT_NAME=<name> STUDENT_EMAIL=<email> python3 scripts/apply_student_info.py
```

如果仍需要传统包含 PDF、脚本、结果和日志的完整归档，可以再运行：

```bash
STUDENT_ID=<id> STUDENT_NAME=<name> STUDENT_EMAIL=<email> ASSIGNMENT_NAME=星际争霸对战 bash scripts/prepare_submission.sh
```

打包产物位于 `dist/`，该目录不纳入 Git。

## GitHub 同步

当前 remote 使用 SSH：

```bash
git remote -v
git status --short --branch
git push
```

remote 地址为：

```text
git@github.com:PPYYQQ/MARL-hw3.git
```

之前 HTTPS 推送失败的原因是非交互式环境没有 GitHub 用户名/token 凭据；SSH remote 已验证可用。每个关键修改都应独立 commit，并同步更新 `PROGRESS.md`。

## 注意事项

- 当前结果是单 seed 复现，不是多 seed 统计结论。
- 当前 HARL commit 缺少 `3s5z` 和 `8m_vs_9m` 的 MAPPO tuned config；MAPPO 配置由同地图 HAPPO tuned config 转换得到。
- `report/main.tex` 中仍有学生身份占位符，正式提交前必须替换。
