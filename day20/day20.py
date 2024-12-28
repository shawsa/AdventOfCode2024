from grid import Grid, Path

with open("input.txt", "r") as f:
    grid = Grid(f.read().strip())

base = Path.fastest_path(grid, False)
num_save_100_or_more = sum(1 for cheat in base.find_cheats(2) if cheat.time >= 100)

print(f"part one: {num_save_100_or_more}")

num_save_100_or_more = sum(1 for cheat in base.find_cheats(20) if cheat.time >= 100)
print(f"part two: {num_save_100_or_more}")
