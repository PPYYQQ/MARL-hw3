# AGENTS.md

本文件用于指导 coding agent 在本目录下完成“多智能体系统作业：星际争霸对战”。所有回复必须以 `Harry` 开头，以便保持当前上下文。
github目录：https://github.com/PPYYQQ/MARL-hw3.git
写作使用模版：/home/yongqian/Documents/yongqian/MARL大作业/hw3/icml2022.zip
如果遇到hugging face的网络问题考虑挂：https://hf-mirror.com
如果遇到网络问题需要代理，可以考虑看batshrc里的setp

## 总体概述

作业文档为 `hw3.pptx`。核心任务不是从零实现 MAPPO/HAPPO，而是基于 HARL 代码库和 SMAC 环境完成算法阅读、代码理解、实验复现、结果绘图和研究性报告。

需要完成的内容：

- 阅读 MAPPO 与 HAPPO 论文，报告中简要说明算法核心思想。
- 阅读 HARL 代码，将算法理论与核心实现位置对应起来，例如 HAPPO 的 `clip`、优势函数前的 `factor`、GAE 计算、顺序更新策略等。
- 按 HARL README 安装 HARL 与 SMAC，完整记录安装流程和关键问题。
- 使用 HARL 的 `tuned_configs` 完成 MAPPO、HAPPO 在 `3s5z`、`8m_vs_9m` 两个 SMAC 地图上的训练。
- 从训练输出的 `progress.txt` 绘制 `win rate` 曲线，并在报告中展示、比较和讨论。
- 可选 Bonus：探索其他 SMAC 地图、MAMuJoCo 等环境，或自行实现/改进 MARL 算法。

主要参考链接：

- HARL: https://github.com/PKU-MARL/HARL
- SMAC: https://github.com/oxwhirl/smac
- MAPPO/on-policy: https://github.com/marlbenchmark/on-policy
- MAPPO paper: https://arxiv.org/abs/2103.01955
- HAPPO/HARL paper: https://jmlr.org/papers/volume25/23-0488/23-0488.pdf
- SMAC paper: https://arxiv.org/abs/1902.04043

## 完成预估

### 自动化边界

coding agent 可以自动完成：

- 解析作业要求，建立项目目录、实验脚本、绘图脚本和报告骨架。
- 克隆/安装 HARL、SMAC 的 Python 依赖，并记录安装日志。
- 定位 HARL 中 MAPPO/HAPPO、GAE、buffer、runner、logger、配置加载等关键代码。
- 生成 4 个基础训练命令：`mappo/happo` × `3s5z/8m_vs_9m`。
- 在环境可用时运行 smoke test、短训练、正式训练，并从 `progress.txt` 自动绘制曲线。
- 起草报告中的方法介绍、代码对应关系、实验设置、曲线分析和参考文献。

coding agent 不能保证自动完成：

- 无人值守解决所有 CUDA、PyTorch、SC2 二进制、系统库、显卡驱动问题。
- 在没有足够 GPU/CPU 时间的机器上完成完整训练。
- 替代人工完成论文理解的最终判断、实验现象解释和课程提交信息确认。
- 判断最终报告是否满足教师偏好的表达风格和评分标准。

### 计算资源

最低可行资源：

- Linux 环境，建议 Ubuntu 或兼容发行版。
- Python/Conda 环境，HARL README 当前建议 Python 3.8。
- CPU 8 核、内存 16 GB、磁盘 20 GB 以上。
- 可用于 smoke test 和短训练，但正式复现实验会很慢。

推荐资源：

- NVIDIA GPU，显存 8 GB 以上，CUDA/PyTorch 版本与驱动匹配。
- CPU 16 核、内存 32 GB、磁盘 50 GB 以上。
- StarCraft II Linux 版本、SMAC maps、稳定网络和可长时间运行的 shell/tmux。

预计时间：

- 环境安装与排错：1-4 小时，依赖机器状态。
- 代码阅读与报告骨架：0.5-1 天。
- 4 个正式训练任务：单 seed 通常需要 20-60 小时总计算时间；多 seed 约按 seed 数线性增加。
- 绘图、结果分析、报告整理：0.5-1 天。
- 若只做短训练验证流程，可在数小时内完成脚本、日志和示例曲线，但报告中的复现说服力会下降。

### 需要的支持

- 学号、姓名、作业名称、提交格式偏好（LaTeX ICML2022 或 Word 双栏）。
- 可用 GPU 服务器或允许长时间运行的本机环境。
- StarCraft II 安装路径，必要时提供 `SC2PATH`。
- 是否要求多 seed，以及每个实验的训练步数/预算。
- 是否需要 Bonus，若需要需提前确认可用计算资源。

## 预估项目架构

建议保持本目录为作业工作区，不要直接修改上游库源码，除非需要明确 patch。推荐结构：

```text
hw3/
  AGENTS.md
  hw3.pptx
  README.md
  external/
    HARL/
  scripts/
    setup_env.sh
    run_smac_experiments.sh
    plot_win_rate.py
    collect_progress.py
  configs/
    overrides/
      mappo_3s5z.yaml
      happo_3s5z.yaml
      mappo_8m_vs_9m.yaml
      happo_8m_vs_9m.yaml
  logs/
    setup.md
    code_reading.md
    experiment_notes.md
  figures/
    win_rate_3s5z.png
    win_rate_8m_vs_9m.png
  report/
    main.tex
    references.bib
    figures/
  results/
    raw/
    processed/
```

目录约定：

- `external/HARL/` 存放克隆的 HARL 仓库；尽量通过配置和脚本驱动，不直接改动上游代码。
- `scripts/` 存放可复现实验命令、数据整理和绘图逻辑。
- `configs/overrides/` 存放本作业所需的配置副本或覆盖配置，避免污染 HARL 的 tuned configs。
- `logs/` 记录安装过程、关键代码位置、异常处理和实验观察。
- `results/raw/` 存放 HARL 输出日志或其软链接；不要提交大型模型 checkpoint。
- `figures/` 存放报告可直接引用的图。
- `report/` 存放最终研究性报告源码；如使用 Word，则保留导出的 PDF 和素材说明。

## 实施计划

### 阶段 1：资料与环境确认

- 从 `hw3.pptx` 提取作业要求，维护到 `logs/assignment_summary.md`。
- 阅读 HARL、SMAC、MAPPO/on-policy README，记录当前日期、commit hash、安装命令和关键版本。
- 确认本机 `conda`、CUDA、NVIDIA driver、磁盘空间、`SC2PATH` 和 StarCraft II maps。
- 先运行 `python -m smac.bin.map_list` 和 `python -m smac.examples.random_agents` 验证 SMAC。

### 阶段 2：代码阅读与对应关系

- 在 HARL 中定位 `happo`、`mappo`、actor/critic、buffer、runner、logger、GAE 相关实现。
- 用 `rg` 搜索 `clip`、`factor`、`gae`、`advantages`、`update`、`sequential` 等关键词。
- 在 `logs/code_reading.md` 记录“论文概念 -> 文件路径 -> 函数/类 -> 简要解释”。
- 只做必要摘录，避免复制大段上游代码到报告。

### 阶段 3：实验脚本与短训练

- 使用 HARL `tuned_configs` 定位 `mappo/happo` 在 `smac` 的 `3s5z`、`8m_vs_9m` 配置。
- 编写 `scripts/run_smac_experiments.sh`，参数化算法、地图、seed、实验名和配置路径。
- 先把训练步数降到很小做 smoke test，确认 `progress.txt`、TensorBoard 和模型目录正常生成。
- 记录每次运行命令、commit hash、seed、地图、配置文件和输出目录。

### 阶段 4：正式训练与结果整理

- 按作业要求运行 `mappo/happo` × `3s5z/8m_vs_9m`，优先单 seed 完整跑通。
- 若资源允许，增加 3 个以上 seeds，并在报告中展示均值与方差/置信区间。
- 编写 `scripts/plot_win_rate.py` 解析 `progress.txt`，输出每个地图的 win rate 对比曲线。
- 在 `logs/experiment_notes.md` 记录收敛速度、最终胜率、波动性、失败 case 和可能原因。

### 阶段 5：报告与提交材料

- 报告至少包含：背景、算法简介、代码对应、环境配置、实验设置、结果曲线、讨论、参考文献。
- 安装流程需记录完整，包括环境变量、版本、报错与修复。
- 最终导出 PDF，建议不少于 3 页。
- 按“学号+姓名+作业名称”命名压缩包，补充材料可包含脚本、配置、图和精选日志。

## 测试计划

### 环境测试

- `conda info`：确认当前环境。
- `python -c "import torch; print(torch.__version__, torch.cuda.is_available())"`：确认 PyTorch 和 CUDA。
- `python -c "import smac; print(smac.__file__)"`：确认 SMAC 可导入。
- `python -m smac.bin.map_list`：确认 SMAC maps 可识别。
- `python -m smac.examples.random_agents`：确认 StarCraft II 可启动。

### HARL 测试

- 在 `external/HARL/examples` 中执行最小训练命令，使用小步数覆盖配置。
- 验证输出目录包含配置快照、日志、`progress.txt` 或等价进度文件。
- 检查训练进程能正常结束，并调用环境 `close()`。

### 数据与绘图测试

- 用真实或最小样例 `progress.txt` 测试 `scripts/plot_win_rate.py`。
- 检查脚本能自动识别 win rate 列名；若列名变化，应输出清晰错误信息。
- 检查生成图片存在、非空，坐标轴、图例、算法名和地图名正确。

### 报告一致性测试

- 报告中的算法名、地图名、seed、训练步数、配置路径必须与日志一致。
- 曲线文件名和报告引用路径必须一致。
- 参考文献必须覆盖 MAPPO、HAPPO/HARL、SMAC。
- 提交前检查 PDF 能打开，压缩包命名符合提交说明。

## 工作约束

- 优先使用 `rg`/`rg --files` 搜索文件和代码。
- 不要提交大型训练结果、StarCraft II 文件、conda 环境或模型 checkpoint。
- 对上游 HARL 的任何源码改动都要先说明原因，并尽量以独立 patch 或配置覆盖方式保存。
- 若训练无法完成，至少保留 smoke test 日志、失败原因、资源瓶颈和可复现实验命令。
- 最终回答应简洁说明改动、验证结果和仍需人工确认的事项。
