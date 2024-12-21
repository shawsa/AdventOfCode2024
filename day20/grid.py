from dataclasses import dataclass
from enum import StrEnum
from itertools import combinations
from typing import Generator


# forward declaration
class Vector:
    ...


class Vector:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __iter__(self):
        yield from (self.row, self.col)

    def __repr__(self) -> str:
        return f"Vector({self.row}, {self.col})"

    def __add__(self, vec: Vector) -> Vector:
        if isinstance(vec, Vector):
            vr, vc = vec
        else:
            assert hasattr(vec, "__len__")
            assert len(vec) == 2
            vr, vc = vec
        return Vector(self.row + vr, self.col + vc)

    def __sub__(self, vec: Vector) -> Vector:
        if isinstance(vec, Vector):
            vr, vc = vec
        else:
            assert hasattr(vec, "__len__")
            assert len(vec) == 2
            vr, vc = vec
        return Vector(self.row - vr, self.col - vc)

    @property
    def l1(self) -> int:
        return abs(self.row) + abs(self.col)

    def __eq__(self, vec: Vector) -> bool:
        return self.row == vec.row and self.col == vec.col

    def __radd__(self, vec: Vector) -> Vector:
        return self + vec

    def __hash__(self) -> int:
        return hash((self.row, self.col))


class Tile(StrEnum):
    EMPTY = "."
    WALL = "#"
    START = "S"
    END = "E"


EMPTY_TILES = (Tile.EMPTY, Tile.START, Tile.END)


class Grid:
    def __init__(self, tiles: list[list[Tile]] | str):
        if isinstance(tiles, str):
            tiles = [[Tile(c) for c in line] for line in tiles.strip().split("\n")]
        self.num_rows = len(tiles)
        self.num_cols = len(tiles[0])
        for row in tiles:
            assert len(row) == self.num_cols
        self.tiles = tiles
        self.initialize_start_end()

    def initialize_start_end(self) -> None:
        self.start = None
        self.end = None
        for loc, tile in self.enumerate():
            if tile == Tile.START:
                self.start = loc
            if tile == Tile.END:
                self.end = loc
        assert self.start is not None
        assert self.end is not None

    def __getitem__(self, index: Vector | tuple[int, int]) -> Tile:
        row, col = index
        return self.tiles[row][col]

    def enumerate(self) -> Generator[tuple[Vector, Tile], None, None]:
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                yield Vector(row, col), self[row, col]

    def adjacent_to(self, loc: Vector) -> Generator[Vector, None, None]:
        """Prefer up an to the right first"""
        row, col = loc
        if 0 < row:
            yield Vector(row - 1, col)
        if col < self.num_cols - 1:
            yield Vector(row, col + 1)
        if row < self.num_rows - 1:
            yield Vector(row + 1, col)
        if 0 < col:
            yield Vector(row, col - 1)

    def is_empty(self, loc: Vector) -> bool:
        return self[loc] in EMPTY_TILES

    def in_bounds(self, loc: Vector) -> bool:
        return (0 <= loc.row < self.num_rows) and (0 <= loc.col < self.num_cols)

    def __str__(self) -> str:
        return "\n".join("".join(tile.value for tile in row) for row in self.tiles)


# forward declaration
class Agent:
    pass


@dataclass
class Agent:
    loc: Vector
    cheat_time: int

    def can_move(self, loc: Vector, grid: Grid, max_cheat_time: int = 2) -> bool:
        if not grid.in_bounds(loc):
            return False
        if grid[loc] in EMPTY_TILES:
            return True
        if self.cheat_time < max_cheat_time - 1:
            return True
        return False

    def move(self, loc: Vector, grid: Grid, max_cheat_time: int = 2) -> Agent:
        if grid[loc] == Tile.WALL or (0 < self.cheat_time < max_cheat_time):
            return Agent(loc, self.cheat_time + 1)
        return Agent(loc, self.cheat_time)


@dataclass
class Cheat:
    start: Vector
    end: Vector
    time: int


# forward declaration
class Path:
    pass


class Path:
    def __init__(self, grid: Grid, agents: tuple[Agent]):
        self.grid = grid
        self.agents = agents

    @property
    def is_complete(self) -> bool:
        return self.agents[-1].loc == self.grid.end

    @property
    def locations(self) -> list[Vector]:
        return [agent.loc for agent in self.agents]

    def add_agent(self, agent: Agent) -> Path:
        return Path(self.grid, self.agents + (agent,))

    @property
    def last(self) -> Agent:
        return self.agents[-1]

    def next_paths(self) -> Generator[Path, None, None]:
        for loc in self.grid.adjacent_to(self.last.loc):
            if loc in self.locations:
                continue
            if not self.last.can_move(loc, self.grid):
                continue
            yield self.add_agent(self.last.move(loc, self.grid))

    @classmethod
    def all_paths(
        cls,
        grid: Grid,
        can_cheat: bool = True,
        max_time: (int | None) = None,
    ) -> Generator[Path, None, None]:
        if max_time is None:
            max_time = float("inf")
        start_agent = Agent(grid.start, 0 if can_cheat else 2)
        leaves = [Path(grid, (start_agent,))]
        while len(leaves) > 0:
            if leaves[0].time >= max_time:
                break
            new_leaves = [my_path for leaf in leaves for my_path in leaf.next_paths()]
            for leaf in new_leaves:
                if leaf.is_complete:
                    yield leaf
                    new_leaves.remove(leaf)
            leaves = new_leaves

    @classmethod
    def fastest_path(cls, grid: Grid, can_cheat: bool = True) -> Path:
        return next(cls.all_paths(grid, can_cheat))

    def __iter__(self):
        return iter(self.agents)

    def __len__(self) -> int:
        return len(self.agents)

    @property
    def time(self) -> int:
        return len(self) - 1

    def agent_at(self, loc: Vector) -> Agent | None:
        for agent in self:
            if agent.loc == loc:
                return agent
        return None

    def __str__(self) -> str:
        lines = []
        for row in range(self.grid.num_rows):
            chars = []
            for col in range(self.grid.num_cols):
                loc = Vector(row, col)
                my_agent = self.agent_at(loc)
                tile = self.grid[loc]
                if tile in [Tile.START, Tile.END]:
                    chars.append(tile.value)
                elif my_agent is None:
                    chars.append(tile.value)
                else:
                    if my_agent.cheat_time == 1:
                        chars.append("X")
                    else:
                        chars.append("O")
            lines.append("".join(chars))
        return "\n".join(lines)

    def find_cheats(self) -> Generator[Cheat, None, None]:
        for (index1, loc1), (index2, loc2) in combinations(
            enumerate(self.locations), 2
        ):
            if (loc1 - loc2).l1 != 2:
                continue
            if index1 > index2:
                index1, loc1, index2, loc2 = index2, loc2, index1, loc1
            midpoint = Vector(
                (loc1.row + loc2.row) // 2,
                (loc1.col + loc2.col) // 2,
            )
            if self.grid[midpoint] != Tile.WALL:
                continue
            time = index2 - index1 - 2
            yield Cheat(loc1, loc2, time)
