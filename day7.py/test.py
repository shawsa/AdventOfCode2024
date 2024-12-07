from day7 import (
    apply_ops,
    parse_input,
    is_correct,
    part_one,
    part_two,
)
from operator import mul, add


test_input = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""


pairs = parse_input(test_input)
correct = [pair for pair in pairs if is_correct(pair, [add, mul])]
apply_ops([1, 2, 3], [add, mul])
part_one(pairs)
part_two(pairs)
