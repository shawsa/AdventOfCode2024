from day16 import (
    Maze,
    Path,
    part_one,
    part_two,
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

maze = Maze(test_input)
best_paths = Path.best_paths(maze)
for path in best_paths:
    print(f"score = {path.score}")
    print(path)


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


maze = Maze(test_input_2)
best_paths = Path.best_paths(maze)
for path in best_paths:
    print(f"score = {path.score}")
    print(path)


part_one(Maze(test_input))
part_one(Maze(test_input_2))

part_two(Maze(test_input))
part_two(Maze(test_input_2))
