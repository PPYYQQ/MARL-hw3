# SMAC Progress Summary

Source: `results/processed/progress_summary.csv`

| Mode | Map | Algo | Rows | Final step | Final reward | Final win rate | Best reward | Best win rate |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| full | `3s5z` | happo | 250 | 20000000 | 19.3452 | 0.8750 | 20.0066 | 1.0000 |
| pilot | `3s5z` | happo | 12 | 9600 | 4.0629 | 0.0000 | 9.5795 | 0.0000 |
| smoke | `3s5z` | happo | 6 | 960 | 5.5166 | 0.0000 | 5.5166 | 0.0000 |
| full | `3s5z` | mappo | 250 | 20000000 | 19.8764 | 0.9750 | 20.0115 | 1.0000 |
| pilot | `3s5z` | mappo | 12 | 9600 | 7.6954 | 0.0000 | 10.4901 | 0.0000 |
| smoke | `3s5z` | mappo | 6 | 960 | 6.4834 | 0.0000 | 6.9669 | 0.0000 |
| full | `8m_vs_9m` | happo | 64 | 5120000 | 17.9525 | 0.7250 | 18.3971 | 0.8000 |
| pilot | `8m_vs_9m` | happo | 12 | 9600 | 5.0072 | 0.0000 | 7.5108 | 0.0000 |
| full | `8m_vs_9m` | happo | 41 | 3280000 | 17.7460 | 0.7250 | 18.2432 | 0.7750 |
| smoke | `8m_vs_9m` | happo | 6 | 960 | 2.2446 | 0.0000 | 2.2446 | 0.0000 |
| full | `8m_vs_9m` | mappo | 250 | 20000000 | 18.9216 | 0.8750 | 19.2201 | 0.9000 |
| pilot | `8m_vs_9m` | mappo | 12 | 9600 | 7.5108 | 0.0000 | 9.9856 | 0.0000 |
| smoke | `8m_vs_9m` | mappo | 6 | 960 | 3.7986 | 0.0000 | 6.3022 | 0.0000 |

Notes:

- `smoke` rows verify the end-to-end training, logging, collection and plotting pipeline.
- `pilot` rows cover the complete MAPPO/HAPPO x `3s5z`/`8m_vs_9m` matrix at 10000 environment steps.
- `full` rows are checkpoints from HARL tuned configs; they are final performance evidence only after the full run completes.
- Smoke, pilot and early full checkpoints are not final performance evidence; full HARL tuned configs use 20000000 environment steps.
