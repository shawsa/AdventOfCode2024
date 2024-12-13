from collections import namedtuple
from dataclasses import dataclass
import numpy as np
import numpy.linalg as la
import re

from parser import machine as parse_machine


@dataclass
class Button:
    label: str
    x: int
    y: int


Prize = namedtuple("Prize", ["x", "y"])


class ClawMachine:
    def __init__(self, a: Button, b: Button, prize: Prize):
        self.a = a
        self.b = b
        self.prize = prize

    @property
    def mat(self):
        return np.array(
            [
                [self.a.x, self.b.x],
                [self.a.y, self.b.y],
            ],
            dtype=float,
        )

    @property
    def full_rank(self) -> bool:
        return la.matrix_rank(self.mat) == 2

    def solve_full_rank(self) -> tuple[int, int] | None:
        assert self.full_rank
        presses = la.solve(self.mat, np.array(self.prize))
        a_pushes, b_pushes = map(lambda n: int(np.round(n, 0)), presses)
        if (a_pushes * self.a.x + b_pushes * self.b.x == self.prize.x) and (
            a_pushes * self.a.y + b_pushes * self.b.y == self.prize.y
        ):
            return a_pushes, b_pushes
        return None

    def cost(self) -> int:
        sol = self.solve_full_rank()
        if sol is None:
            return 0
        a_pushes, b_pushes = sol
        return 3 * a_pushes + b_pushes


def load_input() -> str:
    with open("input.txt", "r") as f:
        ret = f.read().strip()
    return ret


def parse_machines(string: str) -> list[ClawMachine]:
    machine_strings = string.split("\n\n")
    return [
        ClawMachine(Button(a, ax, ay), Button(b, bx, by), Prize(px, py))
        for (a, ax, ay), (b, bx, by), (px, py) in map(
            parse_machine.parse, machine_strings
        )
    ]


def part_one(machines: list[ClawMachine]) -> int:
    return sum(machine.cost() for machine in machines)


if __name__ == "__main__":
    machines = parse_machines(load_input())
    print(f"part one: {part_one(machines)}")
