from day14 import (
    Grid,
    parse_bots,
    Robot,
)


test = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""


grid = Grid(11, 7, (
    Robot(2, 4, 2, -3),
))
for g in grid.sequence(5):
    print(g)
    print()


swarm = parse_bots(test)
grid = Grid(width=11, height=7, swarm=swarm)
final = grid.after(100)
print(final)
print(final.quadrant_counts())

