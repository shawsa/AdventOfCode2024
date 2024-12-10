from day10 import (
    Topography,
    Trail,
    trails_in,
    part_one,
)


string = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""


top = Topography(string)
print(top)
trails = list(trails_in(top))
for trail in trails:
    print(trail)
part_one(top)
