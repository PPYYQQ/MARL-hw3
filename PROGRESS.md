# HW3 Progress Tracker

本文件用于跟踪“多智能体系统作业：星际争霸对战”的完成进度。每个关键修改都应对应一个 Git commit，并在这里记录目的、结果和下一步。

## 当前状态

- 工作区：已初始化为 Git 仓库，默认分支为 `main`。
- 作业文档：已解析 `hw3.pptx`，确认任务包括 MAPPO/HAPPO 阅读、HARL+SMAC 环境配置、`3s5z` 和 `8m_vs_9m` 复现实验、win rate 绘图、研究性报告。
- GitHub 状态：本地 Git 可用；`origin` 已配置为 `https://github.com/PPYYQQ/MARL-hw3.git`。
- GitHub CLI：当前未安装 `gh`；非交互式 HTTPS push 缺少 GitHub 凭据，且 `main` 尚无 upstream，尚未同步到远端。
- 正式训练：已启动单 seed tmux 会话 `hw3_full_20260531_seed1`，按 `mappo/happo` × `3s5z`/`8m_vs_9m` 顺序运行 full tuned config；当前已同步 `MAPPO` + `3s5z` 到 240000-step checkpoint。
- 已知限制：完整训练依赖 StarCraft II、SMAC maps、GPU/CPU 资源和长时间运行环境。

## 提交记录

| 时间 | Commit | 内容 | 证据 |
| --- | --- | --- | --- |
| 2026-05-30 | `347c0fa` | 建立作业工作区基线，加入 `AGENTS.md`、作业 PPT、ICML 模板 zip、`.gitignore` | `git log --oneline` |
| 2026-05-30 | `0437b33` | 建立 `PROGRESS.md`，开始跟踪进度、commit 和剩余任务 | `git log --oneline` |
| 2026-05-30 | `5d35696` | 建立 README、脚本、日志、报告骨架和 ICML LaTeX 样式文件 | `bash -n`、`py_compile`、`collect_progress.py` |
| 2026-05-30 | `8f446f0` | 给 HARL 环境安装脚本加入 gym fallback | `bash -n scripts/setup_env.sh` |
| 2026-05-30 | `ec95d34` | 修正 SMAC 安装来源为 oxwhirl/SMAC | `from smac.env import StarCraft2Env` |
| 2026-05-30 | `dc0837a` | 稳定 HARL 环境安装：conda gym、NumPy 兼容、setuptools 约束 | `torch.cuda.is_available()` |
| 2026-05-30 | `69903ad` | 给 SMAC 训练脚本加入 `dry-run` 模式 | `bash scripts/run_smac_experiments.sh dry-run` |
| 2026-05-30 | `549810a` | 保存两个生成的 MAPPO SMAC 配置 | `rg share_param results/processed/generated_mappo_*.json` |
| 2026-05-30 | `8b0267a` | 修正收集/绘图脚本默认扫描 HARL `examples/results` | `py_compile` |
| 2026-05-30 | `ec9259a` | 加入 HARL NumPy 2 兼容补丁脚本 | `torch.from_numpy(np.zeros(...))` |
| 2026-05-30 | `7e106a7` | 完成 4 组 SMAC smoke test，提交 raw progress、汇总 CSV 和 win rate 图 | `bash scripts/run_smac_experiments.sh smoke`、`plot_win_rate.py` |
| 2026-05-30 | `2730a64` | 更新文档，记录 SC2/SMAC/smoke test 成功状态 | `git log --oneline` |
| 2026-05-30 | `522ab67` | 扩写报告草稿、代码阅读笔记和提交检查清单 | `py_compile`、`bash -n`、`rg` |
| 2026-05-30 | `57e1afd` | 增加 HTML 报告、Chrome PDF 构建脚本，并导出 3 页 PDF | `bash scripts/build_report_pdf.sh`、`pdfinfo` |
| 2026-05-30 | `6d201b9` | 记录已生成 PDF 的进度状态 | `git log --oneline` |
| 2026-05-30 | `55fd9a8` | 增加 pilot/PRINT_ONLY 模式、正式训练交接文档和交付压缩包脚本 | `bash -n`、`py_compile`、`package_submission.sh` |
| 2026-05-30 | `49e9ee5` | 记录打包工作流进度 | `git log --oneline` |
| 2026-05-30 | `c487a88` | 完成 HAPPO + `3s5z` 10000-step pilot，更新 raw progress、CSV、曲线、报告和打包内容 | `run_smac_experiments.sh pilot`、`collect_progress.py`、`plot_win_rate.py`、`build_report_pdf.sh` |
| 2026-05-30 | `61a155b` | 记录第一组 pilot 进度和 GitHub 凭据阻塞状态 | `git log --oneline` |
| 2026-05-30 | `2ff9c73` | 修正 README 中 GitHub push 凭据说明 | `git log --oneline` |
| 2026-05-30 | `785c08c` | 完成剩余 3 组 10000-step pilot，形成 MAPPO/HAPPO × 2 maps 的完整 pilot 矩阵 | `run_smac_experiments.sh pilot`、`collect_progress.py`、`plot_win_rate.py`、`build_report_pdf.sh` |
| 2026-05-30 | `29837b8` | 记录完整 pilot 矩阵进度 | `git log --oneline` |
| 2026-05-30 | `30a96ce` | 保存 4 个 SMAC 实验配置快照，确保提交包不依赖被忽略的 `external/HARL` | `snapshot_configs.sh`、`package_submission.sh` |
| 2026-05-30 | `28c9e0c` | 记录配置快照进度 | `git log --oneline` |
| 2026-05-30 | `c49b7eb` | 增加 Markdown 结果摘要脚本与 `progress_summary.md`，自动汇总每个 run 的最终/最佳 evaluation | `summarize_progress.py`、`package_submission.sh` |
| 2026-05-30 | `4107d48` | 记录 Markdown 结果摘要进度 | `git log --oneline` |
| 2026-05-30 | `abc051e` | 增加提交前校验脚本与 `logs/submission_validation.md`，当前 25 项检查 0 failures、2 warnings | `validate_submission.py`、`package_submission.sh` |
| 2026-05-30 | `8588496` | 记录提交前校验进度 | `git log --oneline` |
| 2026-05-30 | `bbee68b` | 稳定提交前校验报告输出，避免进度文件大小变化导致重复变脏 | `validate_submission.py`、`git status --short` |
| 2026-05-30 | `6749ac6` | 记录提交前校验稳定化进度 | `git log --oneline` |
| 2026-05-30 | `a4d350a` | 打包脚本默认先运行提交校验，失败时停止生成压缩包 | `package_submission.sh`、`validate_submission.py` |
| 2026-05-30 | `9d005c1` | 记录打包校验门禁进度 | `git log --oneline` |
| 2026-05-30 | `72db082` | 增加学生身份信息写入脚本，支持用环境变量同步更新 LaTeX 与 HTML 报告 | `apply_student_info.py`、`package_submission.sh` |
| 2026-05-30 | `ef5d92b` | 记录学生身份信息脚本进度 | `git log --oneline` |
| 2026-05-30 | `da93301` | 增加一键最终提交准备脚本，串联身份写入、配置快照、汇总、绘图、PDF、校验和打包 | `prepare_submission.sh`、`validate_submission.py` |
| 2026-05-30 | `3b20cc1` | 记录一键最终提交准备脚本进度 | `git log --oneline` |
| 2026-05-30 | `ca3f875` | 提交前校验加入 Git remote/upstream 检查，明确记录当前 GitHub push 未完成 | `validate_submission.py`、`package_submission.sh` |
| 2026-05-30 | `6deebf4` | 记录 Git 同步校验进度 | `git log --oneline` |
| 2026-05-30 | `5a3ffeb` | 增加 tmux 正式训练启动脚本，支持 dry-run 预览和日志记录 | `launch_training_tmux.sh`、`bash -n` |
| 2026-05-30 | `828af1b` | 记录 tmux 正式训练启动脚本进度 | `git log --oneline` |
| 2026-05-30 | `2d0b67b` | 增加 GitHub token 推送辅助脚本，使用临时 askpass 且不改写 remote URL | `push_to_github.sh`、`PUSH_DRY_RUN=true` |
| 2026-05-30 | `49c0407` | 记录 GitHub token 推送辅助脚本进度 | `git log --oneline` |
| 2026-05-30 | `7dcbc73` | 生成提交产物 SHA256/大小 manifest，并接入最终准备、校验和打包流程 | `generate_artifact_manifest.py`、`validate_submission.py`、`package_submission.sh` |
| 2026-05-30 | `111cd09` | 记录提交产物 manifest 进度 | `git log --oneline` |
| 2026-05-31 | `5d343c6` | 增加正式训练 `progress.txt` 同步脚本，并将 `results/raw/full` 纳入 manifest、校验和打包流程 | `sync_harl_results.py`、`validate_submission.py`、`package_submission.sh` |
| 2026-05-31 | `78f6aaa` | 记录正式训练结果同步脚本进度 | `git log --oneline` |
| 2026-05-31 | `7ce16d7` | 启动单 seed 正式训练 tmux 会话，并记录资源、命令和结果整理入口 | `logs/full_training_status.md`、`tmux has-session` |
| 2026-05-31 | `3bafb6e` | 记录正式训练 tmux 会话运行状态 | `git log --oneline` |
| 2026-05-31 | `f3a7ac8` | 同步 `MAPPO` + `3s5z` 阶段性 full checkpoint 到 240000 steps，更新汇总、曲线、报告和 PDF | `sync_harl_results.py`、`collect_progress.py`、`plot_win_rate.py`、`validate_submission.py` |

## 任务清单

### 1. 项目管理

- [x] 建立 `AGENTS.md`，明确 coding agent 工作规范。
- [x] 初始化 Git 仓库。
- [x] 建立进度追踪文档。
- [x] 建立项目 README、目录结构和报告骨架。
- [x] 建立提交检查清单。
- [x] 导出当前 3 页 PDF 报告草稿。
- [x] 建立正式训练交接文档。
- [x] 建立 smoke 版交付压缩包脚本。
- [x] 建立提交前产物校验脚本和校验报告。
- [x] 建立学生身份信息写入脚本。
- [x] 建立一键最终提交准备脚本。
- [x] 建立 tmux 正式训练启动脚本。
- [x] 建立 GitHub token 推送辅助脚本。
- [x] 建立提交产物哈希清单生成脚本。
- [x] 建立正式训练结果同步脚本。
- [x] 保存 MAPPO/HAPPO × `3s5z`/`8m_vs_9m` 配置快照。
- [x] 配置 GitHub remote。
- [ ] push 提交到 GitHub。当前缺少 GitHub HTTPS 凭据。

### 2. 环境与依赖

- [x] 克隆或接入 HARL 仓库。
- [x] 建立 Python/Conda 环境安装脚本。
- [x] 验证 PyTorch、CUDA、HARL、SMAC Python package。
- [x] 验证 SMAC map registry 包含 `3s5z` 和 `8m_vs_9m`。
- [x] 安装并验证 StarCraft II Linux 4.10。
- [x] 安装 SMAC maps，共 23 张。
- [x] 记录初始环境检查结果。

### 3. 代码阅读

- [x] 定位 MAPPO/HAPPO 的核心代码文件。
- [x] 记录论文概念与 HARL 实现的初步对应关系。
- [x] 整理 GAE、clip、factor、顺序更新等关键实现位置。

### 4. 实验复现

- [x] 准备 `mappo` + `3s5z` 训练命令。
- [x] 准备 `happo` + `3s5z` 训练命令。
- [x] 准备 `mappo` + `8m_vs_9m` 训练命令。
- [x] 准备 `happo` + `8m_vs_9m` 训练命令。
- [x] 完成 dry-run，打印 4 个实验命令。
- [x] 完成 smoke test。
- [x] 增加 `pilot` 短跑模式和 `PRINT_ONLY=true` 预览开关。
- [x] 完成 MAPPO/HAPPO × `3s5z`/`8m_vs_9m` 四组 10000-step pilot。
- [x] 启动单 seed 正式训练 tmux 会话。
- [x] 同步首个阶段性 full checkpoint。
- [ ] 完成正式训练或记录无法完成的资源原因。

### 5. 数据与报告

- [x] 编写 `progress.txt` 收集脚本。
- [x] 编写 HARL 正式训练 `progress.txt` 同步脚本。
- [x] 编写 Markdown 结果摘要脚本。
- [x] 编写 win rate 绘图脚本。
- [x] 生成 smoke win rate 曲线。
- [x] 生成包含四组 pilot 的 win rate 曲线。
- [x] 生成包含阶段性 full checkpoint 的 win rate 曲线。
- [ ] 生成正式训练曲线。
- [x] 建立报告骨架。
- [x] 写入算法简介、代码对应、环境配置、smoke/pilot 结果和讨论。
- [ ] 写入正式训练结果和讨论。
- [x] 导出 smoke/pilot 版 PDF。
- [ ] 导出正式训练版 PDF。

## 下一步

1. 配置 GitHub 凭据后执行 `git push -u origin main`，或运行 `GITHUB_TOKEN=<token> bash scripts/push_to_github.sh`。
2. 设置 `STUDENT_ID`、`STUDENT_NAME`、`STUDENT_EMAIL` 后运行 `python3 scripts/apply_student_info.py`，再重新导出 PDF。
3. 监控正式训练：`tmux attach -t hw3_full_20260531_seed1`，或查看 `logs/full_training_status.md`。
4. 正式训练完成后运行 `python scripts/sync_harl_results.py --mode full`、`python scripts/collect_progress.py` 和 `conda run -n harl_hw3 python scripts/plot_win_rate.py`。
5. 用正式训练曲线替换或补充报告中的 smoke 曲线。
6. 设置 `STUDENT_ID`、`STUDENT_NAME`、`STUDENT_EMAIL` 后运行 `bash scripts/prepare_submission.sh` 生成最终交付包。
