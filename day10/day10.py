from collections import namedtuple, defaultdict
import numpy as np
from itertools import product
from typing import Generator


def load_input() -> str:
    with open("input.txt", "r") as f:
        ret = f.read().strip()
    return ret


Coordinates = namedtuple("Coordinates", ["row", "col"])
Place = namedtuple("Place", ["loc", "val"])


class Topography:
    def __init__(self, string: str):
        self.arr = np.array([[int(c) for c in line] for line in string.split("\n")])
        self.rows, self.cols = self.arr.shape

    def __repr__(self) -> str:
        return "\n".join("".join(str(val) for val in row) for row in self.arr)

    def enumerate(self) -> Generator[Place, None, None]:
        for row, col in product(range(self.rows), range(self.cols)):
            loc = Coordinates(row, col)
            yield Place(loc, self.arr[loc])

    def __getitem__(self, index):
        if isinstance(index, Place):
            return self.arr[Place.loc]
        return self.arr[index]

    @property
    def trail_heads(self) -> Generator[Place, None, None]:
        for loc, val in self.enumerate():
            if val == 0:
                yield Place(loc, 0)

    def adjacent_locs(self, loc: Coordinates) -> Generator[Place, None, None]:
        row, col = loc
        if row != 0:
            yield Place(Coordinates(row - 1, col), self.arr[row - 1, col])
        if row != self.rows - 1:
            yield Place(Coordinates(row + 1, col), self.arr[row + 1, col])
        if col != 0:
            yield Place(Coordinates(row, col - 1), self.arr[row, col - 1])
        if col != self.cols - 1:
            yield Place(Coordinates(row, col + 1), self.arr[row, col + 1])

    def next_places(self, place: Place) -> Generator[Place, None, None]:
        def val_match(next_place: Place):
            return place.val + 1 == next_place.val
        return filter(val_match, self.adjacent_locs(place.loc))


# forward declaration
class Trail:
    pass


class Trail:
    def __init__(self, *places: tuple[Place]):
        self.places = tuple(places)

    def __getitem__(self, index) -> Place:
        return self.places[index]

    def __iter__(self):
        yield from self.places

    def at_end(self) -> bool:
        return len(self.places) == 10

    def append(self, place: Place) -> Trail:
        return Trail(*self.places, place)

    def __repr__(self) -> str:
        return ", ".join(
            f"[{place.val} ({place.loc.row}, {place.loc.col})]" for place in self.places
        )


def trails_in(top: Topography) -> Generator[Trail, None, None]:
    def recur(trail: Trail) -> Generator[Trail, None, None]:
        if trail.at_end():
            yield trail
        else:
            place = trail[-1]
            for next_place in top.next_places(place):
                yield from recur(trail.append(next_place))

    for head in top.trail_heads:
        yield from recur(Trail(head))


def heads_and_tails(top: Topography) -> dict[Place, set[Place]]:
    ret = defaultdict(set)
    for trail in trails_in(top):
        head = trail[0]
        tail = trail[-1]
        ret[head].add(tail)
    return ret


def part_one(top: Topography) -> int:
    return sum(len(val) for val in heads_and_tails(top).values())


if __name__ == "__main__":
    top = Topography(load_input())
    print(f"part one: {part_one(top)}")
