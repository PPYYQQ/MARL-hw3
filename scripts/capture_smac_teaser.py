#!/usr/bin/env python3
"""Capture a real SMAC renderer frame for the report teaser figure."""

from __future__ import annotations

import argparse
import os
import random
from pathlib import Path

import matplotlib.pyplot as plt
from smac.env import StarCraft2Env


def available_actions(env: StarCraft2Env, agent_id: int) -> list[int]:
    mask = env.get_avail_agent_actions(agent_id)
    return [action_id for action_id, is_available in enumerate(mask) if is_available]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map-name", default="8m_vs_9m")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--output", type=Path, default=Path("figures/teaser_smac_8m_vs_9m.png"))
    args = parser.parse_args()

    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    random.seed(args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    env = StarCraft2Env(
        map_name=args.map_name,
        seed=args.seed,
        window_size_x=960,
        window_size_y=720,
    )
    try:
        env.reset()
        for _ in range(args.steps):
            actions = [
                int(random.choice(available_actions(env, agent_id)))
                for agent_id in range(env.n_agents)
            ]
            env.step(actions)
        frame = env.render(mode="rgb_array")
        plt.imsave(args.output, frame)
        print(f"wrote {args.output}")
    finally:
        env.close()


if __name__ == "__main__":
    main()
