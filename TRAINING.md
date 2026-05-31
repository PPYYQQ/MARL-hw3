# Training Handoff

本文件记录正式训练的建议流程。当前仓库已经完成环境安装、命令生成、4 组 smoke test、结果汇总、绘图和 PDF 草稿导出；正式训练仍需要较长时间的稳定计算资源。

## 模式

- `dry-run`：只打印 4 个训练命令，不启动 StarCraft II。
- `smoke`：每组 1000 environment steps，用于验证 HARL、SMAC、SC2、日志和绘图链路。
- `pilot`：默认每组 10000 environment steps，用于正式训练前的短跑检查。
- `full`：使用 HARL tuned config 的训练步数；当前 `3s5z` 和 `8m_vs_9m` 的 HAPPO config 为 2000 万 environment steps。

## 推荐资源

- smoke test：单机 CPU 可跑，但需要本地 StarCraft II 和 SMAC maps；当前本机已验证通过。
- pilot：建议使用 GPU，但 1 个 rollout thread 下 CPU 也可运行；主要用于排查长跑前的配置问题。
- full：建议 NVIDIA GPU、稳定服务器或 tmux 会话、至少数十 GB 可用磁盘。4 组实验乘以多 seed 可能需要数小时到数天，取决于 GPU、CPU、SC2 进程速度和 seed 数。

## 命令

先检查命令：

```bash
conda run -n harl_hw3 bash scripts/run_smac_experiments.sh dry-run
```

预览 pilot 或 full 的真实参数但不启动训练：

```bash
PRINT_ONLY=true conda run -n harl_hw3 bash scripts/run_smac_experiments.sh pilot
```

跑 pilot：

```bash
conda run -n harl_hw3 bash scripts/run_smac_experiments.sh pilot
```

正式训练建议用脚本放在 tmux 中：

```bash
SEEDS="1 2 3" EXP_PREFIX=hw3_full bash scripts/launch_training_tmux.sh full
tmux attach -t <session-name>
```

启动前可以先预览命令，不创建 tmux session：

```bash
LAUNCH_DRY_RUN=true SEEDS="1 2 3" bash scripts/launch_training_tmux.sh full
```

只跑单个组合时可限制地图和算法：

```bash
MAPS=3s5z ALGOS=happo SEEDS=1 bash scripts/launch_training_tmux.sh full
```

如果 `logs/full_training_snapshot.md` 将某个未完成 run 标为 `no recent progress`，先确认当前会话、进程和 GPU 状态：

```bash
python3 scripts/check_full_training_status.py
tmux attach -t hw3_full_20260531_seed1
nvidia-smi
```

若确认需要重跑缺失组合，不要删除旧结果；使用新的 tmux session 和 `EXP_PREFIX` 保留原始 run，单独启动缺失组合：

```bash
SESSION=hw3_recover_happo_8m SEEDS=1 MAPS=8m_vs_9m ALGOS=happo EXP_PREFIX=hw3_recover bash scripts/launch_training_tmux.sh full
```

恢复 run 产出后，仍使用同一套同步、汇总、绘图和校验命令。`check_full_training_status.py` 默认扫描 `hw3*` full run 并列出 `hw3*` tmux sessions，因此会同时显示原始 `hw3_full` 和恢复用的 `hw3_recover`；`collect_progress.py` 会按 run path 保留记录，`summarize_progress.py` 会在摘要中显示新的 full run。

## 结果整理

训练完成后运行：

```bash
python3 scripts/sync_harl_results.py --mode full
python3 scripts/collect_progress.py
python3 scripts/summarize_progress.py
python3 scripts/check_full_training_status.py
conda run -n harl_hw3 python scripts/plot_win_rate.py
bash scripts/snapshot_configs.sh
bash scripts/build_report_pdf.sh
python3 scripts/generate_artifact_manifest.py
python3 scripts/validate_submission.py
```

然后检查：

- `results/processed/progress_summary.csv`
- `results/processed/progress_summary.md`
- `results/raw/full/`
- `logs/full_training_snapshot.md`，其中会标出同步状态和长时间没有新 `progress.txt` 行的未完成 run。
- `figures/win_rate_3s5z.png`
- `figures/win_rate_8m_vs_9m.png`
- `configs/smac/`
- `report/main.pdf`
- `logs/artifact_manifest.md`
- `logs/submission_validation.md`

最后更新报告中的正式训练结果讨论，并为关键修改建立 Git commit。

生成交付压缩包时，`scripts/package_submission.sh` 会默认先运行提交校验；若只是调试打包脚本，可临时设置 `SKIP_VALIDATION=true`。

提交前用 `scripts/apply_student_info.py` 写入姓名、学号和邮箱，再重新导出 PDF：

```bash
STUDENT_ID=<id> STUDENT_NAME=<name> STUDENT_EMAIL=<email> python3 scripts/apply_student_info.py
bash scripts/build_report_pdf.sh
```

最终交付可用一键流程：

```bash
STUDENT_ID=<id> STUDENT_NAME=<name> STUDENT_EMAIL=<email> bash scripts/prepare_submission.sh
```

GitHub 凭据准备好后，可用 `GITHUB_TOKEN=<token> bash scripts/push_to_github.sh` 推送本地提交。
