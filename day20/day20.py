from grid import Grid, Path
from tq

with open("input.txt", "r") as f:
    grid = Grid(f.read().strip())

base = Path.fastest_path(grid, False)
num_save_100_or_more = sum(1 for cheat in base.find_cheats() if cheat.time >= 100)

print(f"part one: {num_save_100_or_more}")
