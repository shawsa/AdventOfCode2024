from dataclasses import dataclass
from functools import reduce
from operator import mul
from typing import Generator

from parser import robot as robot_parser


def load_input() -> str:
    with open("input.txt", "r") as f:
        ret = f.read().strip()
    return ret


@dataclass
class Robot:
    px: int
    py: int
    vx: int
    vy: int

    @property
    def location(self) -> tuple[int, int]:
        return self.px, self.py

    @property
    def velocity(self) -> tuple[int, int]:
        return self.vx, self.vy


def parse_bots(string: str) -> list[Robot]:
    swarm = []
    for (px, py), (vx, vy) in map(robot_parser.parse, string.split("\n")):
        swarm.append(Robot(px, py, vx, vy))
    return swarm


# forward declaration
class Grid:
    ...


class Grid:
    def __init__(self, width: int, height: int, swarm: tuple[Robot] = tuple):
        self.width = width
        self.height = height
        self.swarm = tuple(swarm)

    def __str__(self) -> str:
        rows = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                count = sum(1 for bot in self.swarm if bot.location == (x, y))
                if count == 0:
                    row.append(".")
                else:
                    row.append(str(min(9, count)))
            rows.append(row)
        return "\n".join("".join(row) for row in rows)

    def next(self) -> Grid:
        new_swarm = tuple(
            Robot(
                (bot.px + bot.vx) % self.width,
                (bot.py + bot.vy) % self.height,
                bot.vx,
                bot.vy,
            )
            for bot in self.swarm
        )
        return Grid(self.width, self.height, new_swarm)

    def after(self, seconds: int) -> Grid:
        """Return a new grid representing the state after `seconds` seconds."""
        grid = self
        for _ in range(seconds):
            grid = grid.next()
        return grid

    def sequence(self, seconds: int = 100) -> Generator[Grid, None, None]:
        grid = self
        for _ in range(seconds + 1):
            yield grid
            grid = grid.next()

    def count_region(self, xmin: int, xmax: int, ymin: int, ymax: int) -> int:
        """Count the number of robots whose position (px, py) satisfy both
        xmin <= px < xmax
        ymin <= py < ymax
        """

        def in_quadrant(bot: Robot) -> bool:
            return (xmin <= bot.px < xmax) and (ymin <= bot.py < ymax)

        return sum(1 for bot in self.swarm if in_quadrant(bot))

    def quadrant_counts(self) -> tuple[int, int, int, int]:
        xmid = self.width // 2
        ymid = self.height // 2
        return (
            self.count_region(0, xmid, 0, ymid),  # Q00
            self.count_region(xmid + 1, self.width, 0, ymid),  # Q01
            self.count_region(0, xmid, ymid + 1, self.height),  # Q10
            self.count_region(xmid + 1, self.width, ymid + 1, self.height),  # Q11
        )


def part_one(grid: Grid):
    final = grid.after(100)
    return reduce(mul, final.quadrant_counts(), 1)


if __name__ == "__main__":
    robots = parse_bots(load_input())
    grid = Grid(101, 103, robots)
    print(f"part_one: {part_one(grid)}")
