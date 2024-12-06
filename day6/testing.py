from day6_functional import (
    read_state_from_string,
    state_sequence,
    animate,
    guard_path,
    part_one,
)

test = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

initial_state = read_state_from_string(test)
states = list(state_sequence(initial_state))
animate(initial_state)
guard_path(initial_state)
part_one(test)
