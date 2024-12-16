from day16 import (
    Maze,
    Path,
    part_one,
)


test_input = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

test_input_2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""


maze = Maze(test_input)
paths = list(Path.all_paths(maze))
best = min(paths, key=lambda path: path.score)
print(f"score = {best.score}")
print(best)
print()
print(Path.best_path(maze))

best = min(Path.all_paths(Maze(test_input_2)), key=lambda path: path.score)
print(f"score = {best.score}")
print(best)
print()
print(Path.best_path(Maze(test_input_2)))

part_one(Maze(test_input))
part_one(Maze(test_input_2))
