from grid import (
    Grid,
    Vector,
    Tile,
)
from maze import Path

from time import sleep


test_positions = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""


grid = Grid(
    {
        Vector(x, y): Tile.CORUPTED
        for (x, y) in map(
            lambda line: map(int, line.split(",")), test_positions.split("\n")[:12]
        )
    },
    width=7,
    height=7,
)

print(grid)
test_path = Path(grid, (grid.start,))
print(test_path)

paths = sorted(Path.solutions(grid), key=lambda path: len(path))
path = paths[0]
print(grid.mark(path))


for index in range(len(path)):
    print(grid.mark(path[:index]))
    print()
    sleep(0.25)


path = Path.shortest_solution(grid)
print(path.steps)
