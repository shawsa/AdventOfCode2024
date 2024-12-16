from dataclasses import dataclass
from enum import Enum, StrEnum
from itertools import pairwise
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

    def __eq__(self, vec: Vector) -> bool:
        return self.row == vec.row and self.col == vec.col

    def __radd__(self, vec: Vector) -> Vector:
        return self + vec


class Heading(Enum):
    NORTH = Vector(-1, 0)
    SOUTH = Vector(1, 0)
    WEST = Vector(0, -1)
    EAST = Vector(0, 1)


@dataclass
class Reindeer:
    position: Vector
    heading: Vector


class Tile(StrEnum):
    WALL = "#"
    EMPTY = "."
    START = "S"
    END = "E"


class Maze:
    def __init__(self, string: str):
        """Parse the maze input."""
        self.tiles = [[Tile(c) for c in line] for line in string.split("\n")]
        self.height = len(self.tiles)
        self.width = len(self.tiles[0])

        self.start = None
        self.end = None
        for vec, tile in self.enumerate():
            if tile == Tile.START:
                self.start = vec
            elif tile == Tile.END:
                self.end = vec

    def __str__(self) -> str:
        return "\n".join("".join(row) for row in self.tiles)

    def __getitem__(self, loc: Vector) -> Tile:
        row, col = loc
        return self.tiles[row][col]

    def enumerate(self) -> Generator[tuple[Vector, Tile], None, None]:
        for row in range(self.height):
            for col in range(self.width):
                yield Vector(row, col), self[row, col]

    def adjacent_to(self, loc: Vector) -> Generator[Vector, None, None]:
        for direction in Heading:
            target = loc + direction
            if target == Tile.WALL:
                continue
            yield target


# forward declaration
class Path:
    ...


class Path:
    def __init__(self, maze: Maze, reindeers: tuple[Reindeer] | None = None):
        self.maze = maze
        if reindeers is None:
            self.reindeers = (Reindeer(maze.start, Heading.EAST),)
        else:
            self.reindeers = reindeers

        if self.maze.end == self.reindeers[-1].position:
            self.score = self.calculate_score()
        else:
            self.score = float("inf")

    @property
    def locations(self) -> list[Vector]:
        return [deer.position for deer in self.reindeers]

    def get_deer_at(self, loc: Vector) -> Reindeer:
        for deer in self.reindeers:
            if deer.position == loc:
                return deer

    @property
    def last(self) -> Reindeer:
        return self.reindeers[-1]

    def __len__(self) -> int:
        return len(self.reindeers)

    def __str__(self) -> str:
        chars = []
        for row in range(self.maze.height):
            for col in range(self.maze.width):
                loc = Vector(row, col)
                tile = self.maze[loc]
                if tile != Tile.EMPTY:
                    chars.append(str(tile))
                else:
                    if loc in self.locations:
                        heading = self.get_deer_at(loc).heading
                        if heading == Heading.NORTH:
                            chars.append("^")
                        elif heading == Heading.SOUTH:
                            chars.append("V")
                        elif heading == Heading.EAST:
                            chars.append(">")
                        elif heading == Heading.WEST:
                            chars.append("<")
                        else:
                            raise ValueError(f"{heading} is not in {list(Heading)}")
                    else:
                        assert tile == Tile.EMPTY
                        chars.append(str(tile))
            chars.append("\n")
        return "".join(chars)

    def calculate_score(self) -> int:
        steps = sum(1 for _ in self.reindeers[1:])
        turns = 0
        for deer1, deer2 in pairwise(self.reindeers):
            if deer1.heading != deer2.heading:
                turns += 1
        return steps + 1000 * turns

    @classmethod
    def all_paths(cls, maze: Maze) -> Generator[Path, None, None]:
        def _recursive_paths(path: Path) -> Generator[Path, None, None]:
            if path.last.position == maze.end:
                yield path
            else:
                for heading in Heading:
                    target = path.last.position + heading.value
                    if maze[target] == Tile.WALL or target in path.locations:
                        continue
                    new_path = Path(maze, path.reindeers + (Reindeer(target, heading),))
                    yield from _recursive_paths(new_path)

        yield from _recursive_paths(Path(maze))


def load_input() -> str:
    with open("input.txt", "r") as f:
        return f.read().strip()


def part_one(maze: Maze) -> int:
    best = min(Path.all_paths(maze), key=lambda path: path.score)
    return best.score


if __name__ == "__main__":
    maze = Maze(load_input())
    print(f"part one: {part_one(maze)}")
