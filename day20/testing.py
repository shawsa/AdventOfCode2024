from collections import defaultdict
from grid import Grid, Path


test_input = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""


grid = Grid(test_input)
base = Path.fastest_path(grid, False)

cheats = list(base.find_cheats())

times_dict = defaultdict(int)
for cheat in cheats:
    times_dict[cheat.time] += 1

for time, count in sorted(times_dict.items(), key=lambda pair: pair[0]):
    if count == 1:
        print(f"There is one cheat that saves {time} picoseconds.")
    else:
        print(f"There are {count} cheats that save {time} picoseconds.")
