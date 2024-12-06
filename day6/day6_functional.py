from dataclasses import dataclass
from enum import StrEnum
from functools import reduce
from itertools import product, chain
from time import sleep
from typing import Generator

OBSTACLE = "#"
PATH = "X"

Coord = tuple[int]


class Grid:
    pass  # Forward declaration to avoid linting error


class Grid:
    def __init__(self, arr: tuple[tuple[str]]):
        self.arr = arr
        self.rows = len(arr)
        self.cols = len(arr[0])

        for row in arr:
            assert len(row) == self.cols

    def in_bounds(self, coord: Coord):
        i, j = coord
        return (0 <= i < self.rows) and (0 <= j < self.cols)

    def __getitem__(self, coord: Coord):
        return self.arr[coord[0]][coord[1]]

    def __repr__(self) -> str():
        return "\n".join("".join(row) for row in self.arr)

    def __iter__(self):
        return chain(*self.arr)

    def enumerate(self):
        for coord in product(range(self.rows), range(self.cols)):
            yield coord, self[coord]

    def replace_at(self, coord: Coord, new_val: str) -> Grid:
        return Grid(
            tuple(
                tuple(
                    new_val if (row_index, col_index) == coord else val
                    for col_index, val in enumerate(row)
                )
                for row_index, row in enumerate(self.arr)
            )
        )


class GuardChar(StrEnum):
    LEFT = "<"
    RIGHT = ">"
    UP = "^"
    DOWN = "v"


class Guard:
    pass  # forward declaration to avoid linting error


@dataclass
class Guard:
    row: int
    col: int
    direction: GuardChar

    @property
    def location(self) -> Coord:
        return self.row, self.col

    @property
    def target(self) -> Coord:
        assert self.direction in GuardChar
        if self.direction is GuardChar.LEFT:
            return self.row, self.col - 1
        if self.direction is GuardChar.RIGHT:
            return self.row, self.col + 1
        if self.direction is GuardChar.UP:
            return self.row - 1, self.col
        if self.direction is GuardChar.DOWN:
            return self.row + 1, self.col

    def turn_right(self) -> Guard:
        assert self.direction in GuardChar
        if self.direction is GuardChar.LEFT:
            return Guard(self.row, self.col, GuardChar.UP)
        if self.direction is GuardChar.RIGHT:
            return Guard(self.row, self.col, GuardChar.DOWN)
        if self.direction is GuardChar.UP:
            return Guard(self.row, self.col, GuardChar.RIGHT)
        if self.direction is GuardChar.DOWN:
            return Guard(self.row, self.col, GuardChar.LEFT)


@dataclass
class State:
    grid: Grid
    guard: Guard

    def at_end(self):
        return not self.grid.in_bounds(self.guard.target)

    def can_step(self):
        return self.grid[self.guard.target] != OBSTACLE

    def __repr__(self) -> str:
        return str(self.grid.replace_at(self.guard.location, self.guard.direction))

    def update(self, guard: Guard):
        return State(self.grid, guard)


def read_state_from_string(string: str) -> State:
    grid = Grid(tuple(tuple(c for c in line) for line in string.split()))
    for coord, char in grid.enumerate():
        if char in list(GuardChar):
            guard = Guard(*coord, GuardChar(char))
            break
    return State(grid.replace_at(coord, "."), guard)


def state_sequence(initial_state: State) -> Generator[State, None, None]:
    state = initial_state
    yield state
    while not state.at_end():
        if state.can_step():
            row, col = state.guard.target
            direction = state.guard.direction
            state = state.update(Guard(row, col, direction))
            yield state
        else:
            state = state.update(state.guard.turn_right())
            yield state


def animate(initial_state: State, frame_durration=0.25):
    rows = initial_state.grid.rows
    LINE_UP = "\033[1A"
    LINE_CLEAR = "\x1b[2K"
    for state in state_sequence(initial_state):
        print(state)
        sleep(frame_durration)
        for _ in range(rows):
            print(LINE_UP, end=LINE_CLEAR)
    print(state.grid)


def guard_path(initial_state: State) -> Grid:
    grid = initial_state.grid
    for state in state_sequence(initial_state):
        grid = grid.replace_at(state.guard.location, PATH)
    return grid


def load_input() -> State:
    with open("input.txt", "r") as f:
        return read_state_from_string(f.read())


def part_one(initial_state):
    path = guard_path(initial_state)
    return sum(1 for char in path if char == PATH)


if __name__ == "__main__":
    initial_state = load_input()
    print(f"part_one: {part_one(initial_state)}")
