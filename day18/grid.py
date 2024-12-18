from enum import StrEnum
from typing import Generator


class Tile(StrEnum):
    CORUPTED = "#"
    EMPTY = "."
    MARK = "O"


# forward declaration
class Vector:
    ...


class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __iter__(self):
        yield from (self.x, self.y)

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __add__(self, vec: Vector) -> Vector:
        if isinstance(vec, Vector):
            vr, vc = vec
        else:
            assert hasattr(vec, "__len__")
            assert len(vec) == 2
            vr, vc = vec
        return Vector(self.x + vr, self.y + vc)

    def __eq__(self, vec: Vector) -> bool:
        return self.x == vec.x and self.y == vec.y

    def __radd__(self, vec: Vector) -> Vector:
        return self + vec

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class Grid:
    def __init__(self, entities: dict[Vector, Tile], width: int, height: int):
        self.width = width
        self.height = height
        self.entities = entities

    def __getitem__(self, vec: Vector):
        if not isinstance(vec, Vector):
            vec = Vector(*vec)
        if vec in self.entities.keys():
            return self.entities[vec]
        else:
            return Tile.EMPTY

    def __str__(self) -> str:
        return "\n".join(
            "".join(self[x, y] for x in range(self.width)) for y in range(self.height)
        )

    def mark(self, locs: list[Vector]) -> str:
        return "\n".join(
            "".join(
                Tile.MARK if Vector(x, y) in locs else self[x, y]
                for x in range(self.width)
            )
            for y in range(self.height)
        )

    def adjacent_to(self, vec: Vector) -> Generator[Vector, None, None]:
        x, y = vec
        if x < self.width - 1:
            yield Vector(x + 1, y)
        if y < self.height - 1:
            yield Vector(x, y + 1)
        if 0 < x:
            yield Vector(x - 1, y)
        if 0 < y:
            yield Vector(x, y - 1)

    def empty_at(self, vec: Vector) -> bool:
        return self[vec] == Tile.EMPTY

    def empty_and_adjacent_to(self, vec: Vector) -> Generator[Vector, None, None]:
        return filter(self.empty_at, self.adjacent_to(vec))

    @property
    def start(self) -> Vector:
        return Vector(0, 0)

    @property
    def end(self) -> Vector:
        return Vector(self.width - 1, self.height - 1)
