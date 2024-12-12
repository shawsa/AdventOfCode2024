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


if __name__ == "__main__":
    string = load_input()
    garden = Garden(string)
    print(f"part one: {part_one(garden)}")
