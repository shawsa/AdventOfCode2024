from day6_functional import (
    read_state_from_string,
    State,
    state_sequence,
    animate,
    guard_path,
    part_one,
    will_loop,
    part_two,
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
part_one(initial_state)

will_loop(initial_state)
test_state = State(initial_state.grid.replace_at((6, 3), "#"), initial_state.guard)
will_loop(test_state)

part_two(initial_state)
