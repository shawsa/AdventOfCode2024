from collections import namedtuple
from itertools import product
from termcolor import colored
from typing import Generator


Location = namedtuple("Location", ["row", "col"])


def adjacent_to(loc: Location) -> Generator[Location, None, None]:
    row, col = loc
    yield Location(row - 1, col)
    yield Location(row, col - 1)
    yield Location(row + 1, col)
    yield Location(row, col + 1)


class Region:
    def __init__(self, plant: str, locs: set[Location]):
        self.plant = plant
        self.locs = locs

    def __contains__(self, target: Location):
        return target in self.locs

    def add(self, target: Location):
        self.locs.add(target)

    def __str__(self) -> str:
        return (
            f"Region({self.plant})["
            + ",".join(f"({loc.row},{loc.col})" for loc in self.locs)
            + "]"
        )

    @property
    def area(self) -> int:
        return len(self.locs)

    @property
    def perimiter(self) -> int:
        ret = 0
        for loc in self.locs:
            for nbr in adjacent_to(loc):
                if nbr not in self:
                    ret += 1
        return ret


class Garden:
    def __init__(self, string: str):
        self.plots = [[c for c in line] for line in string.strip().split("\n")]
        self.rows = len(self.plots)
        self.cols = len(self.plots[0])
        for row in self.plots:
            assert len(row) == self.cols

    def __str__(self) -> str:
        return "\n".join("".join(plot for plot in row) for row in self.plots)

    def __getitem__(self, loc: Location):
        row, col = loc
        return self.plots[row][col]

    def enumerate(self) -> Generator[tuple[Location, str], None, None]:
        for row, col in product(range(self.rows), range(self.cols)):
            yield (Location(row, col), self[row, col])

    def in_bounds(self, loc: Location) -> bool:
        row, col = loc
        if row < 0:
            return False
        if row >= self.rows:
            return False
        if col < 0:
            return False
        if col >= self.cols:
            return False
        return True

    def adjacent(self, loc: Location) -> Generator[Location, None, None]:
        assert self.in_bounds(loc)
        for nbr in adjacent_to(loc):
            if self.in_bounds(nbr):
                yield nbr

    def region_with(self, loc: Location) -> list[Region]:
        def add_neighbors(
            leaves: set[Location], region: Region
        ) -> tuple[set[Location], Region]:
            neighbors = set(
                nbr
                for loc in leaves
                for nbr in self.adjacent(loc)
                if nbr not in region and self[nbr] == region.plant
            )
            for nbr in neighbors:
                region.add(nbr)
            return neighbors, region

        region = Region(self[loc], set((loc,)))
        leaves = [loc]
        while len(leaves) > 0:
            leaves, region = add_neighbors(leaves, region)

        return region

    def show_region(self, region: Region) -> str:
        chars = []
        for row in range(self.rows):
            for col in range(self.cols):
                c = self[(row, col)]
                if c == region.plant:
                    chars.append(colored(c, attrs=["bold"]))
                else:
                    chars.append(colored(c, "dark_grey"))
            chars.append("\n")
        return "".join(chars)

    def show_region_at(self, loc: Location) -> str:
        region = self.region_with(loc)
        return self.show_region(region)

    @property
    def regions(self) -> list[Region]:
        regions = []
        for loc, plant in self.enumerate():
            if any(loc in region for region in regions):
                continue
            regions.append(self.region_with(loc))
        return regions


def load_input() -> str:
    with open("input.txt", "r") as f:
        ret = f.read().strip()
    return ret


def part_one(garden: Garden) -> int:
    return sum(region.area * region.perimiter for region in garden.regions)


# forward declaration
class FencPiece:
    pass


class FencePiece:
    def __init__(self, inside: Location, outside: Location):
        assert inside in list(adjacent_to(outside))
        self.inside = inside
        self.outside = outside

    def __eq__(self, fp: FencPiece) -> bool:
        return self.inside == fp.inside and self.outside == fp.outside

    def __repr__(self) -> str:
        return f"[({self.inside.row},{self.inside.col}), ({self.outside.row},{self.outside.col})]"

    @property
    def horizontal(self) -> bool:
        return self.inside.col == self.outside.col

    def next_to(self, fp: FencPiece) -> bool:
        if self.horizontal:
            if abs(self.inside.col - fp.inside.col) != 1:
                return False
            if abs(self.outside.col - fp.outside.col) != 1:
                return False
            if self.inside.row != fp.inside.row:
                return False
            if self.outside.row != fp.outside.row:
                return False
            return True
        else:
            if abs(self.inside.row - fp.inside.row) != 1:
                return False
            if abs(self.outside.row - fp.outside.row) != 1:
                return False
            if self.inside.col != fp.inside.col:
                return False
            if self.outside.col != fp.outside.col:
                return False
            return True


class FenceSide:
    def __init__(self, *pieces: list[FencePiece]):
        assert len(pieces) > 0
        self.pieces = list(pieces)

    def __repr__(self) -> str:
        if self.pieces[0].horizontal:
            self.pieces.sort(key=lambda piece: piece.inside.col)
        else:
            self.pieces.sort(key=lambda piece: piece.inside.row)
        return "\n".join(str(piece) for piece in self.pieces)

    def should_add(self, fp: FencePiece) -> bool:
        if fp in self.pieces:
            return False
        return any(piece.next_to(fp) for piece in self.pieces)

    def add(self, piece: FencePiece):
        self.pieces.append(piece)

    def aquire_pieces(self, pieces: list[FencePiece]):
        def aquire_one(pieces: list[FencePiece]) -> bool:
            for piece in pieces:
                if self.should_add(piece):
                    self.add(piece)
                    pieces.remove(piece)
                    return True
            return False

        while aquire_one(pieces):
            pass


def count_sides(region: Region) -> int:
    pieces = []
    for inside in region.locs:
        for outside in adjacent_to(inside):
            if outside in region:
                continue
            pieces.append(FencePiece(inside, outside))
    sides = []
    while len(pieces) > 0:
        side = FenceSide(pieces.pop())
        side.aquire_pieces(pieces)
        sides.append(side)
    return len(sides)


def part_two(garden: Garden) -> int:
    return sum(region.area * count_sides(region) for region in garden.regions)


if __name__ == "__main__":
    string = load_input()
    garden = Garden(string)
    print(f"part one: {part_one(garden)}")
    print(f"part two: {part_two(garden)}")
