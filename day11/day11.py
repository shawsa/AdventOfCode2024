from collections import defaultdict
from itertools import chain, count
from typing import Generator


# forward declarations
class Stone:
    pass


class StoneLine:
    pass


class Stone:
    def __init__(self, val: int):
        self.val = val

    def next_stones(self) -> Generator[Stone, None, None]:
        if self.val == 0:
            yield Stone(1)
        elif len(str(self.val)) % 2 == 0:
            my_str = str(self.val)
            my_len = len(my_str) // 2
            yield Stone(int(my_str[:my_len]))
            yield Stone(int(my_str[my_len:]))
        else:
            yield Stone(self.val * 2024)

    def __repr__(self) -> str:
        return f"Stone({self.val})"

    def __hash__(self) -> int:
        return hash(self.val)

    def __eq__(self, stone: Stone):
        if not isinstance(stone, Stone):
            return False
        return self.val == stone.val


class StoneLine:
    def __init__(self, stones: tuple[Stone]):
        self.stones = tuple(stones)

    @classmethod
    def from_nums(cls, *nums):
        return StoneLine(map(Stone, nums))

    def __iter__(self) -> Generator[Stone, None, None]:
        yield from self.stones

    def __len__(self) -> int:
        return len(self.stones)

    def __getitem__(self, index) -> Stone:
        return self.stones[index]

    def __repr__(self) -> str:
        return f"StoneLine({', '.join(str(stone.val) for stone in self)})"

    def next_line(self) -> StoneLine:
        return StoneLine(chain(*(stone.next_stones() for stone in self.stones)))

    def sequence(self, max_iter: None | int = None) -> Generator[StoneLine, None, None]:
        if max_iter is None:
            max_iter = float("inf")
        sl = self
        for index in count():
            if index > max_iter:
                break
            yield sl
            sl = sl.next_line()

    def blink(self, num_blinks: int) -> StoneLine:
        sl = self
        for _ in range(num_blinks):
            sl = sl.next_line()
        return sl


def load_input() -> str:
    with open("input.txt", "r") as f:
        ret = f.read().strip()
    return list(map(int, ret.split(" ")))


def part_one(stone_line: StoneLine) -> int:
    return len(stone_line.blink(25))


StoneDict = dict[Stone, int]


def stone_dict_from_nums(*nums: list[int]) -> StoneDict:
    stone_dict = defaultdict(int)
    for num in nums:
        stone_dict[Stone(num)] += 1
    return stone_dict


def stone_dict_from_stones(*stones: list[Stone]) -> StoneDict:
    stone_dict = defaultdict(int)
    for stone in stones:
        stone_dict[stone] += 1
    return stone_dict


def blink_dict_once(stone_dict: StoneDict) -> StoneDict:
    new_dict = defaultdict(int)
    for parent_stone, num in stone_dict.items():
        for stone in parent_stone.next_stones():
            new_dict[stone] += num
    return new_dict


def blink_dict(blinks: int, stone_dict: StoneDict) -> StoneDict:
    for _ in range(blinks):
        stone_dict = blink_dict_once(stone_dict)
    return stone_dict


def part_two(nums: list[int]) -> int:
    stone_dict = stone_dict_from_nums(*nums)
    stone_dict = blink_dict(75, stone_dict)
    return sum(stone_dict.values())


if __name__ == "__main__":
    nums = load_input()
    sl = StoneLine.from_nums(*nums)
    print(f"part one: {part_one(sl)}")
    print(f"part two: {part_two(nums)}")
