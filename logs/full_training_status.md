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
- Latest synced checkpoint: `MAPPO` + `8m_vs_9m` completed 20000000 environment steps with final eval reward 18.9216 and final eval win rate 0.875; best synced reward is 19.2201 and best synced win rate is 0.9.
- Latest early checkpoint: `HAPPO` + `8m_vs_9m` reached 5120000 environment steps with final eval reward 17.9525 and final eval win rate 0.725; best synced reward is 18.3971 and best synced win rate is 0.8.
- Latest recovery checkpoint: `HAPPO` + `8m_vs_9m` recovery run reached 1920000 environment steps with final eval reward 14.9957 and final eval win rate 0.400; this run is still in progress and is tracked separately from the original stale run.
- Diagnostic snapshot at 2026-05-31 20:23 CST: tmux session still active; `HAPPO` + `8m_vs_9m` external and synced progress files both have 64 rows and latest step 5120000. The generated `logs/full_training_snapshot.md` marks this run as `no recent progress` because the external `progress.txt` was last modified at 2026-05-31 17:28:43 CST, about 175 minutes before the snapshot. No new checkpoint was available to sync in this observation.

## Monitoring

Use these commands while the run is active:

```bash
tmux attach -t hw3_full_20260531_seed1
tail -f logs/training_sessions/hw3_full_20260531_seed1.log
python3 scripts/check_full_training_status.py
find external/HARL/examples/results -path '*hw3_full*' -type f -name progress.txt -printf '%p %s bytes\n'
nvidia-smi
```

## Stale Run Handling

If `logs/full_training_snapshot.md` marks an incomplete run as `no recent progress`, keep the existing output directory intact and launch a recovery run with a different tmux session and `EXP_PREFIX`. For the current missing matrix entry, the non-destructive recovery command is:

```bash
SESSION=hw3_recover_happo_8m SEEDS=1 MAPS=8m_vs_9m ALGOS=happo EXP_PREFIX=hw3_recover bash scripts/launch_training_tmux.sh full
```

After the recovery run writes `progress.txt`, rerun the normal result collection commands below. The old `hw3_full` run remains available for audit, while the recovery run is collected as a separate full run path.

## Recovery Launch

- Date: 2026-05-31 20:32 Asia/Shanghai
- tmux session: `hw3_recover_happo_8m`
- Log file: `logs/training_sessions/hw3_recover_happo_8m.log`
- Purpose: rerun only `HAPPO` + `8m_vs_9m` with `EXP_PREFIX=hw3_recover` because the original `hw3_full` run had no new `progress.txt` row for more than 3 hours.
- Latest synced recovery checkpoint: 1920000 environment steps, eval reward 14.9957, eval win rate 0.400.
- Command:

```bash
SESSION=hw3_recover_happo_8m SEEDS=1 MAPS=8m_vs_9m ALGOS=happo EXP_PREFIX=hw3_recover bash scripts/launch_training_tmux.sh full
```

## Result Collection

After one or more full runs produce non-empty `progress.txt` files:

```bash
python3 scripts/sync_harl_results.py --mode full
python3 scripts/collect_progress.py
python3 scripts/summarize_progress.py
python3 scripts/check_full_training_status.py
conda run -n harl_hw3 python scripts/plot_win_rate.py
bash scripts/build_report_pdf.sh
python3 scripts/generate_artifact_manifest.py
python3 scripts/validate_submission.py
```

Then update `report/main.tex`, `report/report.html`, `PROGRESS.md`, and commit the new formal training artifacts.
