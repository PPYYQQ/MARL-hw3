# Experiment Notes

## 实验矩阵

| 算法 | 地图 | 配置来源 | 状态 |
| --- | --- | --- | --- |
| HAPPO | `3s5z` | HARL tuned config | smoke test 通过 |
| HAPPO | `8m_vs_9m` | HARL tuned config | smoke test 通过 |
| MAPPO | `3s5z` | 基于同地图 HAPPO tuned config 生成 MAPPO 配置 | smoke test 通过 |
| MAPPO | `8m_vs_9m` | 基于同地图 HAPPO tuned config 生成 MAPPO 配置 | smoke test 通过 |

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
- 汇总结果已保存到 `results/processed/progress_summary.csv`，共 24 行。
- 曲线已保存到 `figures/win_rate_3s5z.png` 和 `figures/win_rate_8m_vs_9m.png`。
- 由于 smoke test 只有 1000 environment steps，4 组实验的 eval win rate 都是 0，曲线只能证明流程可用，不能代表算法性能。

## 运行记录模板

| 时间 | 命令 | seed | 输出目录 | 结果 |
| --- | --- | --- | --- | --- |
| 2026-05-30 | `conda run -n harl_hw3 bash scripts/run_smac_experiments.sh smoke` | 1 | `external/HARL/examples/results/smac/...` | 4 组 smoke test 通过 |

## 观察模板

- `3s5z`：smoke 曲线已生成，正式训练后记录收敛速度、最终 win rate、波动情况。
- `8m_vs_9m`：smoke 曲线已生成，正式训练后记录收敛速度、最终 win rate、波动情况。
- MAPPO vs HAPPO：正式训练后比较 sample efficiency、稳定性和最终性能。
