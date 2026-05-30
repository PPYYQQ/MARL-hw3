# Setup Notes

## 本机检查

- 日期：2026-05-30
- GPU：NVIDIA GeForce RTX 5090, 32607 MiB, driver 580.159.04
- 当前 Python：3.13.12
- 当前 `torch`：未安装
- Conda：可用，当前激活 `base`
- `SC2PATH`：未设置
- GitHub remote：未配置

## HARL

- 本地路径：`external/HARL`
- 克隆来源：https://github.com/PKU-MARL/HARL
- 当前 commit：`b1af98b0dbab72a2eee9d160751cd09aedbb8ce2`

## 需要补齐

- 创建专用 conda 环境，建议不要使用当前 Python 3.13 base 环境。
- 安装 PyTorch、HARL、SMAC、StarCraft II Linux 4.10、SMAC maps。
- 设置 `SC2PATH` 指向 StarCraft II 安装目录。
- 运行 smoke test 验证 SMAC 能启动。

## 验证命令

```bash
conda info --envs
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
python -c "import smac; print(smac.__file__)"
python -m smac.bin.map_list
python -m smac.examples.random_agents
```
