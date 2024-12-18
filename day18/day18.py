from maze import Path
from grid import Grid, Vector, Tile
from tqdm import tqdm

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        corrupted = []
        for line in f:
            x, y = line.split(",")
            corrupted.append(Vector(int(x), int(y)))
    grid = Grid(
        {vec: Tile.CORUPTED for vec in corrupted[:1024]},
        width=71,
        height=71,
    )
    # print(grid.mark(corrupted[:1024]))
    path = Path.shortest_solution(grid, verbose=True)
    print(f"part one: {path.steps}")

    for index in tqdm(range(1024, len(corrupted))):
        grid = Grid(
            {vec: Tile.CORUPTED for vec in corrupted[:index]},
            width=71,
            height=71,
        )
        path = Path.shortest_solution(grid)
        if path is None:
            break
    last_byte = corrupted[index - 1]
    print(f"{last_byte.x},{last_byte.y}")
