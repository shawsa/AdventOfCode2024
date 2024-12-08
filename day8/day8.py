from collections import defaultdict
from itertools import chain, product, permutations, combinations, count
from math import gcd
from typing import Generator


DIGITS = [chr(i) for i in range(48, 58)]
UPPERCASE = [chr(i) for i in range(65, 91)]
LOWERCASE = [chr(i) for i in range(97, 123)]

FREQENCIES = DIGITS + UPPERCASE + LOWERCASE


Frequency = str
Location = tuple[int, int]
LocationDict = dict[Frequency, list[Location]]


def load_input() -> str:
    with open("input.txt", "r") as f:
        string = f.read()[:-1].strip()
    return string


class AntennaMap:
    def __init__(self, string: str):
        self.grid = [[c for c in line] for line in string.split("\n")]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.adict = self.generate_antenna_loc_dict()

    def __iter__(self) -> Generator[Frequency, None, None]:
        yield from chain(*self.grid)

    def enumerate(self) -> Generator[tuple[Location, Frequency], None, None]:
        yield from zip(product(range(self.rows), range(self.cols)), self)

    def __str__(self) -> str:
        return "\n".join("".join(row) for row in self.grid)

    def generate_antenna_loc_dict(self) -> LocationDict:
        ret = defaultdict(list)
        for loc, freq in self.enumerate():
            if freq not in FREQENCIES:
                continue
            ret[freq].append(loc)
        return ret

    def in_bounds(self, loc: Location) -> bool:
        row, col = loc
        return (0 <= row < self.rows) and (0 <= col < self.cols)

    def antinodes_by_freq(self, freq: Frequency) -> Generator[Location, None, None]:
        for loc1, loc2 in permutations(self.adict[freq], 2):
            diff = (loc1[0] - loc2[0], loc1[1] - loc2[1])
            loc = (loc1[0] + diff[0], loc1[1] + diff[1])
            if self.in_bounds(loc):
                yield loc

    def antinodes(self) -> Generator[Location, None, None]:
        anodes = set()
        for freq in self.adict.keys():
            for loc in self.antinodes_by_freq(freq):
                anodes.add(loc)
        return anodes

    def replace_at(self, char: str, locs: Location) -> str:
        grid = [[c for c in line] for line in self.grid]

        for row, col in locs:
            grid[row][col] = char
        return "\n".join("".join(c for c in row) for row in grid)


def part_one(amap: AntennaMap) -> int:
    return len(amap.antinodes())


class HarmonicAntennaMap(AntennaMap):
    def antinodes_by_freq(self, freq: Frequency) -> Generator[Location, None, None]:
        for loc1, loc2 in combinations(self.adict[freq], 2):
            diff = (loc1[0] - loc2[0], loc1[1] - loc2[1])
            factor = gcd(*diff)
            diff = tuple(map(lambda val: val//factor, diff))
            yield loc1
            for index in count():
                loc = (loc1[0] + index * diff[0], loc1[1] + index*diff[1])
                if self.in_bounds(loc):
                    yield loc
                else:
                    break
            for index in count():
                loc = (loc1[0] - index * diff[0], loc1[1] - index*diff[1])
                if self.in_bounds(loc):
                    yield loc
                else:
                    break


def part_two(amap: HarmonicAntennaMap) -> int:
    return len(amap.antinodes())


if __name__ == "__main__":
    string = load_input()
    amap = AntennaMap(string)
    print(f"part one: {part_one(amap)}")
    hamap = HarmonicAntennaMap(string)
    print(f"part two: {part_two(hamap)}")
