# Experiment Notes

## 实验矩阵

| 算法 | 地图 | 配置来源 | 状态 |
| --- | --- | --- | --- |
| HAPPO | `3s5z` | HARL tuned config | 待 smoke test |
| HAPPO | `8m_vs_9m` | HARL tuned config | 待 smoke test |
| MAPPO | `3s5z` | 基于同地图 HAPPO tuned config 生成 MAPPO 配置 | 待 smoke test |
| MAPPO | `8m_vs_9m` | 基于同地图 HAPPO tuned config 生成 MAPPO 配置 | 待 smoke test |

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

当前无法进入 smoke test，因为 StarCraft II Linux 4.10 尚未安装或 `SC2PATH` 未配置。

## 运行记录模板

| 时间 | 命令 | seed | 输出目录 | 结果 |
| --- | --- | --- | --- | --- |
| 待填 | 待填 | 待填 | 待填 | 待填 |

## 观察模板

- `3s5z`：待训练后记录收敛速度、最终 win rate、波动情况。
- `8m_vs_9m`：待训练后记录收敛速度、最终 win rate、波动情况。
- MAPPO vs HAPPO：待训练后比较 sample efficiency、稳定性和最终性能。
