# Setup Notes

## 本机检查

- 日期：2026-05-30
- GPU：NVIDIA GeForce RTX 5090, 32607 MiB, driver 580.159.04
- 当前 Python：3.13.12
- 当前 `torch`：`2.12.0+cu130`，CUDA 可用
- 当前 `numpy`：`2.2.6`
- Conda：可用，当前激活 `base`
- `SC2PATH`：未设置，但 PySC2 默认路径 `/home/yongqian/StarCraftII` 已可用
- GitHub remote：`origin` 已配置为 `https://github.com/PPYYQQ/MARL-hw3.git`；push 仍需 GitHub 凭据

## HARL

- 本地路径：`external/HARL`
- 克隆来源：https://github.com/PKU-MARL/HARL
- 当前 commit：`b1af98b0dbab72a2eee9d160751cd09aedbb8ce2`

## 已完成验证

```bash
conda run -n harl_hw3 python -c "import torch, numpy; from smac.env import StarCraft2Env; print(torch.__version__, torch.cuda.is_available(), numpy.__version__, StarCraft2Env.__name__)"
```

结果：

```text
2.12.0+cu130 True 2.2.6 StarCraft2Env
```

```bash
conda run -n harl_hw3 python -m smac.bin.map_list
```

结果：SMAC map registry 可列出 `3s5z`、`8m_vs_9m` 等地图。

## StarCraft II 与 SMAC maps

- SC2 下载包：`/home/yongqian/SC2.4.10.zip`
- SC2 安装路径：`/home/yongqian/StarCraftII`
- SC2 版本：B75689 / SC2 4.10
- SMAC maps：已复制到 `/home/yongqian/StarCraftII/Maps/SMAC_Maps`，共 23 张。
- random agent：已通过 `conda run -n harl_hw3 python -m smac.examples.random_agents`。

## 仍需补齐

- 正式训练尚未运行，当前已有 1000-step smoke test 和 4 组 10000-step pilot。
- 本机没有 LaTeX 编译器，但已通过 Chrome HTML 流程导出 PDF。
- GitHub push 需要配置 token/credential helper；非交互式 push 当前报错 `fatal: could not read Username for 'https://github.com': terminal prompts disabled`。

## 验证命令

```bash
conda info --envs
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
python -c "import smac; print(smac.__file__)"
python -m smac.bin.map_list
python -m smac.examples.random_agents
```

## random agent 记录

第一次失败原因：

```text
FileNotFoundError: [Errno 2] No such file or directory: '/home/yongqian/StarCraftII/Versions'
```

安装 SC2 和 maps 后，random agent 成功完成 10 个 episode。
