from dataclasses import dataclass
from itertools import product
from operator import mul, add
from typing import Callable


Operator = Callable[[int, int], int]


@dataclass
class Pair:
    test_value: int
    args: list[int]


def parse_input(string: str) -> list[Pair]:
    pairs = []
    for line in string.split("\n"):
        if line == "":
            continue
        test_value_string, arg_string = line.split(":")
        test_value = int(test_value_string)
        args = list(map(int, arg_string.strip().split(" ")))
        pairs.append(Pair(test_value, args))
    return pairs


def load_input() -> list[Pair]:
    with open("input.txt", "r") as f:
        pairs = parse_input(f.read())
    return pairs


def apply_ops(nums: list[int], ops: list[Operator]):
    assert len(nums) == len(ops) + 1
    total = nums[0]
    for arg, op in zip(nums[1:], ops):
        total = op(total, arg)
    return total


def is_correct(pair: Pair, ops: list[Operator]) -> bool:
    num_ops = len(pair.args) - 1
    return any(
        pair.test_value == apply_ops(pair.args, ops)
        for ops in product(ops, repeat=num_ops)
    )


def part_one(pairs: list[Pair]) -> int:
    return sum(pair.test_value for pair in pairs if is_correct(pair, [add, mul]))


def int_concat(arg1: int, arg2: int) -> int:
    return int(str(arg1) + str(arg2))


def part_two(pairs: list[Pair]) -> int:
    ops = [add, mul, int_concat]
    return sum(pair.test_value for pair in pairs if is_correct(pair, ops))


if __name__ == "__main__":
    pairs = load_input()
    print(f"part_one: {part_one(pairs)}")
    print(f"part_two: {part_two(pairs)}")

