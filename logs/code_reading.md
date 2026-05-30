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

## 核心理解

MAPPO 的实现基本沿用 PPO 的 actor update：根据新旧策略 action log probability 得到 importance weight，再用 `clip_param` 限制策略比值，最终取 unclipped/clipped surrogate 的较小项作为 actor objective。多智能体部分主要由 runner 和 buffer 处理：集中式 critic 使用全局 state 或拼接信息估计 value，actor 则按智能体观测输出动作。

HAPPO 的关键区别在顺序更新和 `factor`。`on_policy_ha_runner.py` 在一次 update 开始时把 factor 初始化为 1，然后按 agent order 逐个更新 actor。每个智能体更新前，runner 把当前 factor 写入该智能体的 actor buffer；更新后，runner 重新计算该智能体在旧动作上的新策略 log probability，并把新旧策略概率比累乘进 factor。这样后续智能体的 surrogate objective 会感知前面智能体已经发生的策略变化。

GAE 的核心实现在 critic buffer 的 `compute_returns` 中：从最后一步往前递推 TD residual，使用 `gamma` 和 `gae_lambda` 平衡 bias 与 variance。HARL 中 EP 和 FP state type 分别使用不同 buffer 文件，但递推结构一致。

SMAC 的 `progress.txt` 不是普通训练 reward 日志，而是在 evaluation log 中写入 `total_num_steps, eval_avg_rew, eval_win_rate`。因此绘制作业要求的 win rate 曲线时应读取第三列。

## 当前实验观察

- 1000-step smoke test 中，MAPPO/HAPPO 在 `3s5z` 和 `8m_vs_9m` 的 eval win rate 都为 0。
- 该结果符合预期：smoke test 只验证流程，步数远低于 tuned config 的 2000 万步。
- 正式比较应使用 `full` 模式输出的 `progress.txt`，并最好用多个 seed 报告均值和波动。
