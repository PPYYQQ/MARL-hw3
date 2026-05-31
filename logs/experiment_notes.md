# Experiment Notes

## 实验矩阵

| 算法 | 地图 | 配置来源 | 状态 |
| --- | --- | --- | --- |
| HAPPO | `3s5z` | HARL tuned config | smoke test 与 10000-step pilot 通过，full 已完成 20000000 steps |
| HAPPO | `8m_vs_9m` | HARL tuned config | smoke test 与 10000-step pilot 通过，原始 full latest synced checkpoint 为 5120000 steps；recovery run 已同步到 3840000 steps |
| MAPPO | `3s5z` | 基于同地图 HAPPO tuned config 生成 MAPPO 配置 | smoke test 与 10000-step pilot 通过，full 已完成 20000000 steps |
| MAPPO | `8m_vs_9m` | 基于同地图 HAPPO tuned config 生成 MAPPO 配置 | smoke test 与 10000-step pilot 通过，full 已完成 20000000 steps |

## dry-run 结果

已执行：

```bash
bash scripts/run_smac_experiments.sh dry-run
```

结果：

- MAPPO + `3s5z`：使用 `results/processed/generated_mappo_3s5z.json`。
- HAPPO + `3s5z`：使用 `external/HARL/tuned_configs/smac/3s5z/happo/config.json`。
- MAPPO + `8m_vs_9m`：使用 `results/processed/generated_mappo_8m_vs_9m.json`。
- HAPPO + `8m_vs_9m`：使用 `external/HARL/tuned_configs/smac/8m_vs_9m/happo/config.json`。

## smoke test 结果

已执行：

```bash
conda run -n harl_hw3 bash scripts/run_smac_experiments.sh smoke
python3 scripts/collect_progress.py
conda run -n harl_hw3 python scripts/plot_win_rate.py
```

结果：

- 原始 `progress.txt` 已保存到 `results/raw/smoke/`。
- 汇总结果已保存到 `results/processed/progress_summary.csv`。
- 曲线已保存到 `figures/win_rate_3s5z.png` 和 `figures/win_rate_8m_vs_9m.png`。
- 由于 smoke test 只有 1000 environment steps，4 组实验的 eval win rate 都是 0，曲线只能证明流程可用，不能代表算法性能。

## pilot 结果

已执行：

```bash
MAPS=3s5z ALGOS=happo EXP_PREFIX=hw3_pilot SEEDS=1 conda run -n harl_hw3 bash scripts/run_smac_experiments.sh pilot
MAPS=3s5z ALGOS=mappo EXP_PREFIX=hw3 SEEDS=1 conda run -n harl_hw3 bash scripts/run_smac_experiments.sh pilot
MAPS=8m_vs_9m ALGOS="mappo happo" EXP_PREFIX=hw3 SEEDS=1 conda run -n harl_hw3 bash scripts/run_smac_experiments.sh pilot
python3 scripts/collect_progress.py
python3 scripts/summarize_progress.py
conda run -n harl_hw3 python scripts/plot_win_rate.py
```

结果：

- 原始 `progress.txt` 已保存到 `results/raw/pilot/`，共 4 个 run、48 条 evaluation 记录。
- 汇总结果更新到 `results/processed/progress_summary.csv` 和 `results/processed/progress_summary.md`；CSV 共 72 行，其中 pilot 贡献 48 行 evaluation 记录。
- 四组 pilot 的最后一次 evaluation 都位于 9600 environment steps，eval win rate 都为 0。

| 地图 | 算法 | 最后 step | Eval reward | Eval win rate |
| --- | --- | --- | --- | --- |
| `3s5z` | HAPPO | 9600 | 4.0629 | 0.0 |
| `3s5z` | MAPPO | 9600 | 7.6954 | 0.0 |
| `8m_vs_9m` | HAPPO | 9600 | 5.0072 | 0.0 |
| `8m_vs_9m` | MAPPO | 9600 | 7.5108 | 0.0 |

该短跑进一步验证了四组目标实验都能稳定运行到 10000-step 量级，但仍不能代表正式复现性能。

## full 阶段性结果

已启动：

```bash
SESSION=hw3_full_20260531_seed1 SEEDS=1 EXP_PREFIX=hw3_full bash scripts/launch_training_tmux.sh full
```

阶段性结果：

- tmux 会话 `hw3_full_20260531_seed1` 仍在运行。
- 当前已同步 `MAPPO` + `3s5z` 的 250 个 full evaluation、`HAPPO` + `3s5z` 的 250 个 full evaluation、`MAPPO` + `8m_vs_9m` 的 250 个 full evaluation、`HAPPO` + `8m_vs_9m` 原始 run 的 64 个 early full evaluation，以及 `HAPPO` + `8m_vs_9m` recovery run 的 48 个 early full evaluation 到 `results/raw/full/`。
- `MAPPO` + `8m_vs_9m` 已到达 20000000 environment steps，final eval reward 为 18.9216，final eval win rate 为 0.875；当前最佳 reward 为 19.2201，当前最佳 win rate 为 0.9。
- `HAPPO` + `8m_vs_9m` latest synced checkpoint 为 5120000 environment steps，final eval reward 为 17.9525，final eval win rate 为 0.725；当前最佳 reward 为 18.3971，当前最佳 win rate 为 0.8。
- `HAPPO` + `8m_vs_9m` recovery run 已同步到 3840000 environment steps，final eval reward 为 16.3014，final eval win rate 为 0.55；该 run 仍在继续。
- `results/processed/progress_summary.csv` 当前共有 934 行，其中 full 贡献 862 行。
- `MAPPO` + `3s5z` 已到达 20000000 environment steps，final eval reward 为 19.8764，final eval win rate 为 0.975；当前最佳 win rate 为 1.0。
- `HAPPO` + `3s5z` 已到达 20000000 environment steps，final eval reward 为 19.3452，final eval win rate 为 0.875；当前最佳 win rate 为 1.0。

## 运行记录模板

| 时间 | 命令 | seed | 输出目录 | 结果 |
| --- | --- | --- | --- | --- |
| 2026-05-30 | `conda run -n harl_hw3 bash scripts/run_smac_experiments.sh smoke` | 1 | `external/HARL/examples/results/smac/...` | 4 组 smoke test 通过 |
| 2026-05-30 | `MAPS=3s5z ALGOS=happo EXP_PREFIX=hw3_pilot SEEDS=1 conda run -n harl_hw3 bash scripts/run_smac_experiments.sh pilot` | 1 | `external/HARL/examples/results/smac/3s5z/happo/hw3_pilot_pilot_happo_3s5z/seed-00001-2026-05-30-23-12-25` | 10000-step pilot 通过 |
| 2026-05-30 | `MAPS=3s5z ALGOS=mappo EXP_PREFIX=hw3 SEEDS=1 conda run -n harl_hw3 bash scripts/run_smac_experiments.sh pilot` | 1 | `external/HARL/examples/results/smac/3s5z/mappo/hw3_pilot_mappo_3s5z/seed-00001-2026-05-30-23-20-22` | 10000-step pilot 通过 |
| 2026-05-30 | `MAPS=8m_vs_9m ALGOS="mappo happo" EXP_PREFIX=hw3 SEEDS=1 conda run -n harl_hw3 bash scripts/run_smac_experiments.sh pilot` | 1 | `external/HARL/examples/results/smac/8m_vs_9m/...` | 2 组 10000-step pilot 通过 |
| 2026-05-31 | `SESSION=hw3_full_20260531_seed1 SEEDS=1 EXP_PREFIX=hw3_full bash scripts/launch_training_tmux.sh full` | 1 | `external/HARL/examples/results/smac/3s5z/mappo/hw3_full_full_mappo_3s5z/seed-00001-2026-05-31-00-04-56` | `MAPPO` + `3s5z` 已同步完整 20000000-step 结果 |
| 2026-05-31 | `SESSION=hw3_full_20260531_seed1 SEEDS=1 EXP_PREFIX=hw3_full bash scripts/launch_training_tmux.sh full` | 1 | `external/HARL/examples/results/smac/3s5z/happo/hw3_full_full_happo_3s5z/seed-00001-2026-05-31-05-20-04` | `HAPPO` + `3s5z` 已同步完整 20000000-step 结果 |
| 2026-05-31 | `SESSION=hw3_full_20260531_seed1 SEEDS=1 EXP_PREFIX=hw3_full bash scripts/launch_training_tmux.sh full` | 1 | `external/HARL/examples/results/smac/8m_vs_9m/mappo/hw3_full_full_mappo_8m_vs_9m/seed-00001-2026-05-31-10-59-45` | `MAPPO` + `8m_vs_9m` 已同步完整 20000000-step 结果 |
| 2026-05-31 | `SESSION=hw3_full_20260531_seed1 SEEDS=1 EXP_PREFIX=hw3_full bash scripts/launch_training_tmux.sh full` | 1 | `external/HARL/examples/results/smac/8m_vs_9m/happo/hw3_full_full_happo_8m_vs_9m/seed-00001-2026-05-31-16-04-52` | `HAPPO` + `8m_vs_9m` latest synced checkpoint 为 5120000 steps |
| 2026-05-31 | `SESSION=hw3_recover_happo_8m SEEDS=1 MAPS=8m_vs_9m ALGOS=happo EXP_PREFIX=hw3_recover bash scripts/launch_training_tmux.sh full` | 1 | `external/HARL/examples/results/smac/8m_vs_9m/happo/hw3_recover_full_happo_8m_vs_9m/seed-00001-2026-05-31-20-32-33` | `HAPPO` + `8m_vs_9m` recovery run 已同步到 3840000 steps |

## 观察模板

- `3s5z`：smoke/pilot/full 曲线已生成，`MAPPO` 与 `HAPPO` 都已完成 20000000 steps。
- `8m_vs_9m`：smoke/pilot/full 曲线已生成，`MAPPO` 已完成 20000000 steps，`HAPPO` 原始 full latest synced checkpoint 为 5120000 steps，recovery run 已同步到 3840000 steps。
- MAPPO vs HAPPO：正式训练后比较 sample efficiency、稳定性和最终性能。
