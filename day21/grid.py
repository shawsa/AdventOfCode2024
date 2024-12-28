from dataclasses import dataclass
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


@dataclass
class Tile:
    value: str

    def __str__(self):
        return self.value


class Grid:
    def __init__(self, tiles: list[list[Tile]] | str):
        if isinstance(tiles, str):
            tiles = [[Tile(c) for c in line] for line in tiles.split("\n")]
        self.num_rows = len(tiles)
        self.num_cols = len(tiles[0])
        for row in tiles:
            assert len(row) == self.num_cols
        self.tiles = tiles

    def __getitem__(self, index: Vector | tuple[int, int]) -> Tile:
        row, col = index
        return self.tiles[row][col]

    def enumerate(self) -> Generator[tuple[Vector, Tile], None, None]:
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                yield Vector(row, col), self[row, col]

    def adjacent_to(self, loc: Vector) -> Generator[Vector, None, None]:
        row, col = loc
        if 0 < row:
            yield Vector(row - 1, col)
        if col < self.num_cols - 1:
            yield Vector(row, col + 1)
        if row < self.num_rows - 1:
            yield Vector(row + 1, col)
        if 0 < col:
            yield Vector(row, col - 1)

    def in_bounds(self, loc: Vector) -> bool:
        return (0 <= loc.row < self.num_rows) and (0 <= loc.col < self.num_cols)

    def __str__(self) -> str:
        return "\n".join("".join(tile.value for tile in row) for row in self.tiles)
