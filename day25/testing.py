from parser import parse_to_locks_and_keys
from locks_and_keys import overlap
from itertools import product

test_input = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""


locks, keys = parse_to_locks_and_keys(test_input)

num_fit = sum(1 for lock, key in product(locks, keys) if not overlap(lock, key))
