# Assignment Summary

来源：`hw3.pptx`

## 作业目标

体验并熟悉多智能体强化学习算法在环境上训练、测试、分析的完整流程，为后续科研和工程实践打基础。

## 必做内容

- 阅读 MAPPO、HAPPO 论文，并在报告中简要介绍算法核心内容。
- 阅读 HARL 代码，把论文概念和核心代码对应起来。
- 根据 HARL README 安装 HARL 和 SMAC，完整记录安装过程。
- 使用 HARL 的配置完成 MAPPO、HAPPO 在 `3s5z`、`8m_vs_9m` 两个地图上的训练。
- 根据输出的 `progress.txt` 绘制 win rate 曲线。
- 在报告中展示曲线，并讨论观察和思考。

## 代码阅读重点

- HAPPO 的 PPO clip 运算。
- HAPPO 中 advantage 前的 `factor` 计算和更新。
- GAE 的计算。
- MAPPO 与 HAPPO 的更新方式差异。
- SMAC logger 如何把 `eval_win_rate` 写入 `progress.txt`。

## 提交要求

- 研究性报告，PDF 形式，中英文皆可，建议不少于 3 页。
- LaTeX 可使用 ICML2022 模板，Word 版要求双栏、单倍行距。
- 补充材料非必须，可包含代码、配置、图和日志。
- 压缩包命名为“学号+姓名+作业名称”。

## Bonus

- 探索其他 SMAC 地图。
- 探索 HARL 支持的其他环境，例如 MAMuJoCo。
- 自行实现其他 MARL 算法或提出新算法。
