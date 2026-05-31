# Full Training Status

本文件记录 HARL tuned config 正式训练的启动状态和后续整理入口。

## Launch

- Date: 2026-05-31 00:04 Asia/Shanghai
- tmux session: `hw3_full_20260531_seed1`
- Log file: `logs/training_sessions/hw3_full_20260531_seed1.log`
- Command:

```bash
SESSION=hw3_full_20260531_seed1 SEEDS=1 EXP_PREFIX=hw3_full bash scripts/launch_training_tmux.sh full
```

Expanded training command:

```bash
env MAPS="3s5z 8m_vs_9m" ALGOS="mappo happo" SEEDS=1 EXP_PREFIX=hw3_full CUDA=true conda run -n harl_hw3 bash scripts/run_smac_experiments.sh full
```

## Current Observation

- GPU check: NVIDIA GeForce RTX 5090, 32607 MiB total memory; training observed at 1461 MiB used and 8% GPU utilization shortly after launch.
- Process check: first run started under `external/HARL/examples/results/smac/3s5z/mappo/hw3_full_full_mappo_3s5z/seed-00001-2026-05-31-00-04-56/`.
- SC2 check: 20 `SC2_x64` rollout processes were active shortly after launch, matching the tuned config `n_rollout_threads=20`.
- Progress check: `progress.txt` existed but was still 0 bytes at the first short observation window; full configs evaluate less frequently than smoke/pilot runs.
- First evaluation: `MAPPO` + `3s5z` reached 80000 environment steps with eval reward 10.1708 and eval win rate 0.0; this row was synced into `results/raw/full/`.
- Latest synced checkpoint: `MAPPO` + `3s5z` completed 20000000 environment steps with final eval reward 19.8764 and final eval win rate 0.975; best synced win rate is 1.0.
- Latest synced checkpoint: `HAPPO` + `3s5z` completed 20000000 environment steps with final eval reward 19.3452 and final eval win rate 0.875; best synced win rate is 1.0.
- Latest early checkpoint: `MAPPO` + `8m_vs_9m` reached 4480000 environment steps with final eval reward 15.3734 and final eval win rate 0.475; best synced reward is 16.5362 and best synced win rate is 0.6098.

## Monitoring

Use these commands while the run is active:

```bash
tmux attach -t hw3_full_20260531_seed1
tail -f logs/training_sessions/hw3_full_20260531_seed1.log
find external/HARL/examples/results -path '*hw3_full*' -type f -name progress.txt -printf '%p %s bytes\n'
nvidia-smi
```

## Result Collection

After one or more full runs produce non-empty `progress.txt` files:

```bash
python3 scripts/sync_harl_results.py --mode full
python3 scripts/collect_progress.py
python3 scripts/summarize_progress.py
conda run -n harl_hw3 python scripts/plot_win_rate.py
bash scripts/build_report_pdf.sh
python3 scripts/generate_artifact_manifest.py
python3 scripts/validate_submission.py
```

Then update `report/main.tex`, `report/report.html`, `PROGRESS.md`, and commit the new formal training artifacts.
