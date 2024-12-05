from day3 import load_input
from parsy import (
    any_char,
    eof,
    digit,
    generate,
    string,
    success,
)

number = digit.at_least(1).concat().map(int)
do = string("do()")
dont = string("don't()")


@generate
def mul_op():
    yield string("mul(")
    arg1 = yield number
    yield string(",")
    arg2 = yield number
    yield string(")")
    return arg1 * arg2


@generate
def dont_block():
    while True:
        at_end = yield (do | eof).result(True) | success(False)
        if at_end:
            break
        yield any_char
    return 0


@generate
def do_block():
    total = 0
    while True:
        at_end = yield (dont | eof).result(True) | success(False)
        if at_end:
            break
        val = yield mul_op | any_char
        if isinstance(val, int):
            total += val
    return total


def part_one(memory: str) -> int:
    instructions = do_block.until(eof)
    return sum(instructions.parse(memory))


def part_two(memory: str) -> int:
    instructions = (do_block << dont_block).until(eof)
    return sum(instructions.parse(memory))


if __name__ == "__main__":
    memory = load_input()
    print(f"part one: {part_one(memory)}")
    print(f"part two: {part_two(memory)}")
