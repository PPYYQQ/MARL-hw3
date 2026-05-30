# Setup Notes

## 本机检查

- 日期：2026-05-30
- GPU：NVIDIA GeForce RTX 5090, 32607 MiB, driver 580.159.04
- 当前 Python：3.13.12
- 当前 `torch`：`2.12.0+cu130`，CUDA 可用
- Conda：可用，当前激活 `base`
- `SC2PATH`：未设置
- GitHub remote：未配置

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
2.12.0+cu130 True 1.23.5 StarCraft2Env
```

```bash
conda run -n harl_hw3 python -m smac.bin.map_list
```

结果：SMAC map registry 可列出 `3s5z`、`8m_vs_9m` 等地图。

## 仍需补齐

- StarCraft II Linux 4.10 未找到；`find /home/yongqian -maxdepth 5 -iname 'StarCraftII'` 无结果。
- `conda run -n harl_hw3 python -m smac.examples.random_agents` 失败，因为缺少 `/home/yongqian/StarCraftII/Versions`。
- 设置 `SC2PATH` 指向 StarCraft II 安装目录。
- 安装 SMAC maps 并运行 random agent/smoke test。

## 验证命令

```bash
conda info --envs
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
python -c "import smac; print(smac.__file__)"
python -m smac.bin.map_list
python -m smac.examples.random_agents
```

## random agent 失败记录

当前失败原因：

```text
FileNotFoundError: [Errno 2] No such file or directory: '/home/yongqian/StarCraftII/Versions'
```

这说明 Python 依赖已到位，下一步需要安装 StarCraft II 本体或设置正确的 `SC2PATH`。
