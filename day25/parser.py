from locks_and_keys import Key, Lock


def parse_to_grids(string: str) -> list[str]:
    return [grid.strip().split("\n") for grid in string.strip().split("\n\n")]


def is_lock(grid: list[str]) -> bool:
    return grid[0] == "#" * len(grid[0])


def is_key(grid: list[str]) -> bool:
    return grid[-1] == "#" * len(grid[0])


def grid_to_heights(grid: list[str]) -> list[int]:
    heights = []
    for col in zip(*grid):
        heights.append(sum(c == "#" for c in col) - 1)
    return heights


def parse_to_locks_and_keys(string: str) -> tuple[list[Lock], list[Key]]:
    locks = []
    keys = []
    for grid in parse_to_grids(string):
        heights = grid_to_heights(grid)
        if is_key(grid):
            keys.append(Key(heights))
        elif is_lock(grid):
            locks.append(Lock(heights))
        else:
            raise ValueError(f"grid {grid} is not a key or a lock")
    return locks, keys
