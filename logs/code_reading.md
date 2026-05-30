# Code Reading Notes

HARL 本地参考路径：`external/HARL`

## 初步对应关系

| 论文/报告概念 | HARL 位置 | 说明 |
| --- | --- | --- |
| HAPPO actor | `external/HARL/harl/algorithms/actors/happo.py:10` | 定义 HAPPO actor 更新逻辑。 |
| MAPPO actor | `external/HARL/harl/algorithms/actors/mappo.py:10` | 定义 MAPPO actor 更新逻辑，包含参数共享训练分支。 |
| PPO clip | `external/HARL/harl/algorithms/actors/happo.py:73` | HAPPO 在 importance ratio 上做 clip。 |
| HAPPO factor | `external/HARL/harl/algorithms/actors/happo.py:79` | HAPPO actor loss 乘以前序智能体更新带来的 `factor_batch`。 |
| factor 初始化 | `external/HARL/harl/runners/on_policy_ha_runner.py:15` | runner 在每轮 actor 更新前把 factor 初始化为 1。 |
| factor 写入 buffer | `external/HARL/harl/runners/on_policy_ha_runner.py:52` | 当前智能体更新前保存 factor。 |
| factor 更新 | `external/HARL/harl/runners/on_policy_ha_runner.py:115` | 更新完当前智能体后，用新旧动作概率比更新 factor。 |
| GAE/return | `external/HARL/harl/common/buffers/on_policy_critic_buffer_ep.py:97` | EP state critic buffer 中计算 return/GAE。 |
| GAE/return | `external/HARL/harl/common/buffers/on_policy_critic_buffer_fp.py:107` | FP state critic buffer 中计算 return/GAE。 |
| MAPPO 多智能体更新 | `external/HARL/harl/runners/on_policy_ma_runner.py:36` | MAPPO 根据 `share_param` 选择参数共享或逐智能体训练。 |
| HAPPO 顺序更新 | `external/HARL/harl/runners/on_policy_ha_runner.py:47` | 根据 `fixed_order` 决定固定顺序或随机顺序更新。 |
| progress.txt 写入 | `external/HARL/harl/envs/smac/smac_logger.py:166` | 写入 `total_num_steps, eval_avg_rew, eval_win_rate`。 |

## 待补充

- MAPPO 论文核心：集中式 critic、去中心化 actor、PPO clipping 在多智能体中的直接扩展。
- HAPPO 论文核心：多智能体优势分解、顺序策略更新、带 factor 的 surrogate objective。
- 对比 MAPPO/HAPPO 在同质 SMAC 任务上的预期差异。
- 把训练曲线现象回填到本文件和报告中。
