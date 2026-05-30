# HW3 Progress Tracker

本文件用于跟踪“多智能体系统作业：星际争霸对战”的完成进度。每个关键修改都应对应一个 Git commit，并在这里记录目的、结果和下一步。

## 当前状态

- 工作区：已初始化为 Git 仓库，默认分支为 `main`。
- 作业文档：已解析 `hw3.pptx`，确认任务包括 MAPPO/HAPPO 阅读、HARL+SMAC 环境配置、`3s5z` 和 `8m_vs_9m` 复现实验、win rate 绘图、研究性报告。
- GitHub 状态：本地 Git 可用；当前未配置 GitHub remote，不能直接 push 到 GitHub。
- 已知限制：完整训练依赖 StarCraft II、SMAC maps、GPU/CPU 资源和长时间运行环境。

## 提交记录

| 时间 | Commit | 内容 | 证据 |
| --- | --- | --- | --- |
| 2026-05-30 | `347c0fa` | 建立作业工作区基线，加入 `AGENTS.md`、作业 PPT、ICML 模板 zip、`.gitignore` | `git log --oneline` |

## 任务清单

### 1. 项目管理

- [x] 建立 `AGENTS.md`，明确 coding agent 工作规范。
- [x] 初始化 Git 仓库。
- [x] 建立进度追踪文档。
- [ ] 配置 GitHub remote 并 push 提交。

### 2. 环境与依赖

- [ ] 克隆或接入 HARL 仓库。
- [ ] 建立 Python/Conda 环境安装脚本。
- [ ] 验证 PyTorch、CUDA、SMAC、StarCraft II。
- [ ] 记录安装过程和异常处理。

### 3. 代码阅读

- [ ] 定位 MAPPO/HAPPO 的核心代码文件。
- [ ] 记录论文概念与 HARL 实现的对应关系。
- [ ] 整理 GAE、clip、factor、顺序更新等关键实现说明。

### 4. 实验复现

- [ ] 准备 `mappo` + `3s5z` 训练命令。
- [ ] 准备 `happo` + `3s5z` 训练命令。
- [ ] 准备 `mappo` + `8m_vs_9m` 训练命令。
- [ ] 准备 `happo` + `8m_vs_9m` 训练命令。
- [ ] 完成 smoke test。
- [ ] 完成正式训练或记录无法完成的资源原因。

### 5. 数据与报告

- [ ] 编写 `progress.txt` 收集脚本。
- [ ] 编写 win rate 绘图脚本。
- [ ] 生成实验曲线。
- [ ] 建立报告骨架。
- [ ] 写入算法简介、代码对应、环境配置、实验结果和讨论。
- [ ] 导出 PDF。

## 下一步

1. 建立推荐目录结构和脚本骨架。
2. 克隆 HARL 或准备克隆脚本。
3. 检查本机 CUDA/PyTorch/Conda 状态。
4. 如需真正同步到 GitHub，需要提供 remote URL 或本机 GitHub CLI/SSH 凭据。
