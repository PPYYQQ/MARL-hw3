# Full Training Snapshot

- Generated: 2026-05-31 20:29:39 CST
- tmux session `hw3_full_20260531_seed1`: active
- Source: `external/HARL/examples/results`
- Synced raw root: `results/raw/full`
- Target full steps: 20000000
- Stale threshold: 120 minutes without a new external `progress.txt` row

| Map | Algo | External rows | External final step | External final win | Synced rows | Synced final step | Sync status | Run state | External age min | External modified |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: | --- |
| `3s5z` | happo | 250 | 20000000 | 0.8750 | 250 | 20000000 | synced | complete | 569.9 | 2026-05-31 10:59:43 CST |
| `3s5z` | mappo | 250 | 20000000 | 0.9750 | 250 | 20000000 | synced | complete | 909.6 | 2026-05-31 05:20:02 CST |
| `8m_vs_9m` | happo | 64 | 5120000 | 0.7250 | 64 | 5120000 | synced | no recent progress | 180.9 | 2026-05-31 17:28:43 CST |
| `8m_vs_9m` | mappo | 250 | 20000000 | 0.8750 | 250 | 20000000 | synced | complete | 264.8 | 2026-05-31 16:04:50 CST |

## Attention

- `happo` + `8m_vs_9m` is incomplete at 5120000 steps and has no new external progress for 180.9 minutes.
