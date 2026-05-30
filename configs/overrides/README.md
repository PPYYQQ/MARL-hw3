# Config Overrides

本目录预留给本作业自己的配置覆盖文件。原则上优先使用 `external/HARL/tuned_configs`；只有上游缺少指定算法/地图配置时，才在脚本中生成或在这里保存覆盖配置。

`configs/smac/` 保存本次作业实际使用的 4 个配置快照，便于提交包在不包含 `external/HARL/` 的情况下仍能复查实验设置。快照由 `scripts/snapshot_configs.sh` 生成。

当前状态：

- HAPPO + `3s5z`：使用 `external/HARL/tuned_configs/smac/3s5z/happo/config.json`，快照为 `configs/smac/3s5z/happo/config.json`。
- HAPPO + `8m_vs_9m`：使用 `external/HARL/tuned_configs/smac/8m_vs_9m/happo/config.json`，快照为 `configs/smac/8m_vs_9m/happo/config.json`。
- MAPPO + `3s5z`：上游缺少 tuned config，运行脚本生成配置，快照为 `configs/smac/3s5z/mappo/config.json`。
- MAPPO + `8m_vs_9m`：上游缺少 tuned config，运行脚本生成配置，快照为 `configs/smac/8m_vs_9m/mappo/config.json`。
