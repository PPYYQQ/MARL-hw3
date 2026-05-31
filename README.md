# MARL HW3 Workspace

本目录用于完成“多智能体系统作业：星际争霸对战”。当前目标是基于 HARL 和 SMAC 完成 MAPPO/HAPPO 的代码阅读、环境配置、训练复现、win rate 绘图和研究性报告。

## 当前进度

- `AGENTS.md`：coding agent 工作规范和完整实施计划。
- `PROGRESS.md`：逐步进度、commit 与剩余任务追踪。
- `external/HARL/`：本地克隆的 HARL 仓库，仅作运行和阅读参考，不纳入本作业 Git 提交。
- `scripts/`：环境安装、训练、日志收集和绘图脚本。
- `configs/smac/`：本作业实际使用的 MAPPO/HAPPO 配置快照。
- `logs/`：作业摘要、环境检查、代码阅读和实验笔记。
- `report/`：研究性报告骨架。
- `SUBMISSION.md`：提交、GitHub 同步、正式训练和 PDF 导出的检查清单。
- `TRAINING.md`：正式训练资源、命令和结果整理说明。

## 推荐流程

1. 运行 `bash scripts/setup_env.sh` 创建 HARL/SMAC 环境。
2. 安装 StarCraft II Linux 4.10，设置 `SC2PATH`，并安装 SMAC maps。当前本机已安装到 `/home/yongqian/StarCraftII`。
3. 运行 `bash scripts/run_smac_experiments.sh dry-run` 检查 4 个实验命令。
4. 运行 `conda run -n harl_hw3 bash scripts/run_smac_experiments.sh smoke` 做最小验证。
5. 运行 `PRINT_ONLY=true conda run -n harl_hw3 bash scripts/run_smac_experiments.sh pilot` 预览短跑参数。
6. 运行 `conda run -n harl_hw3 bash scripts/run_smac_experiments.sh pilot` 做短跑检查。
7. 运行 `bash scripts/launch_training_tmux.sh full` 在 tmux 中启动正式训练。
8. 运行 `bash scripts/snapshot_configs.sh` 保存本次使用的配置快照。
9. 运行 `python scripts/sync_harl_results.py --mode full` 将正式训练 `progress.txt` 复制到 `results/raw/full/`。
10. 运行 `python scripts/collect_progress.py` 汇总 `progress.txt`。
11. 运行 `python scripts/summarize_progress.py` 生成 Markdown 结果摘要。
12. 运行 `python scripts/check_full_training_status.py` 生成 full training 快照。
13. 运行 `python scripts/plot_win_rate.py` 生成 `figures/win_rate_*.png`。
14. 运行 `python scripts/generate_artifact_manifest.py` 生成产物哈希清单。
15. 运行 `python scripts/validate_submission.py` 生成提交前校验报告。
16. 设置 `STUDENT_ID`、`STUDENT_NAME`、`STUDENT_EMAIL` 后运行 `python scripts/apply_student_info.py` 补全报告身份信息。
17. 运行 `bash scripts/build_report_pdf.sh` 导出 PDF。
18. 设置学号姓名后运行 `STUDENT_ID=<id> STUDENT_NAME=<name> bash scripts/package_submission.sh` 生成压缩包；脚本会先运行提交校验。

也可以在学生信息确定后运行一键准备脚本：

```bash
STUDENT_ID=<id> STUDENT_NAME=<name> STUDENT_EMAIL=<email> bash scripts/prepare_submission.sh
```

## 关键说明

当前 HARL commit `b1af98b0dbab72a2eee9d160751cd09aedbb8ce2` 的 `tuned_configs/smac` 中，`3s5z` 和 `8m_vs_9m` 只提供 `happo`、`hatrpo`、`hasac` 配置，没有 MAPPO tuned config。脚本对 HAPPO 使用官方 tuned config；对 MAPPO 会基于同地图 HAPPO tuned config 生成临时 MAPPO 配置，并把算法关键项切换为 `share_param: true`、`fixed_order: true`。

## GitHub

本地 Git 仓库已初始化，`origin` 已切换为 SSH 地址 `git@github.com:PPYYQQ/MARL-hw3.git`。SSH 认证已通过，`main` 已设置为跟踪 `origin/main`：

```bash
git push
```

之前 HTTPS 地址 `https://github.com/PPYYQQ/MARL-hw3.git` 推送失败的原因不是仓库地址错误，而是非交互式环境没有 GitHub 用户名/token 凭据。之后每个关键修改继续使用独立 commit，并同步更新 `PROGRESS.md`。

如果需要改回 HTTPS token 推送，可以用辅助脚本，脚本不会把 token 写入 remote URL：

```bash
GITHUB_TOKEN=<token> bash scripts/push_to_github.sh
```

## 提交

交付前按 `SUBMISSION.md` 检查 PDF、补充材料、压缩包命名和 GitHub 同步状态。
