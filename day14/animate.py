from day14 import (
    Grid,
    load_input,
    parse_bots,
)

from time import sleep

import matplotlib.pyplot as plt


plt.ion()

robots = parse_bots(load_input())
grid = Grid(101, 103, robots)


def to_xs_ys(grid):
    return list(zip(*[robot.location for robot in grid.swarm]))


fig = plt.figure("Tree?")
scatter, = plt.plot(*to_xs_ys(grid.after(7492)), "g.")
plt.axis("equal")

for time, g in enumerate(grid.sequence(10_000)):
    if time % 101 != 18:
        continue
    print(f"{time=}")
    scatter.set_data(*to_xs_ys(g))
    plt.pause(0.05)
    input()
