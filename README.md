# MARL HW3 Workspace

本目录用于完成“多智能体系统作业：星际争霸对战”。当前目标是基于 HARL 和 SMAC 完成 MAPPO/HAPPO 的代码阅读、环境配置、训练复现、win rate 绘图和研究性报告。

## 当前进度

- `AGENTS.md`：coding agent 工作规范和完整实施计划。
- `PROGRESS.md`：逐步进度、commit 与剩余任务追踪。
- `external/HARL/`：本地克隆的 HARL 仓库，仅作运行和阅读参考，不纳入本作业 Git 提交。
- `scripts/`：环境安装、训练、日志收集和绘图脚本。
- `logs/`：作业摘要、环境检查、代码阅读和实验笔记。
- `report/`：研究性报告骨架。

## 推荐流程

1. 配置 GitHub remote 后 push 当前本地提交。
2. 运行 `bash scripts/setup_env.sh` 创建 HARL/SMAC 环境。
3. 运行 `bash scripts/run_smac_experiments.sh smoke` 做最小验证。
4. 运行 `bash scripts/run_smac_experiments.sh full` 做正式训练。
5. 运行 `python scripts/collect_progress.py` 汇总 `progress.txt`。
6. 运行 `python scripts/plot_win_rate.py` 生成 `figures/win_rate_*.png`。
7. 补全 `report/main.tex` 并导出 PDF。

## 关键说明

当前 HARL commit `b1af98b0dbab72a2eee9d160751cd09aedbb8ce2` 的 `tuned_configs/smac` 中，`3s5z` 和 `8m_vs_9m` 只提供 `happo`、`hatrpo`、`hasac` 配置，没有 MAPPO tuned config。脚本对 HAPPO 使用官方 tuned config；对 MAPPO 会基于同地图 HAPPO tuned config 生成临时 MAPPO 配置，并把算法关键项切换为 `share_param: true`、`fixed_order: true`。

## GitHub

本地 Git 仓库已初始化，但当前未配置 remote。配置后可执行：

```bash
git remote add origin <your-github-repo-url>
git push -u origin main
```

之后每个关键修改继续使用独立 commit，并同步更新 `PROGRESS.md`。
