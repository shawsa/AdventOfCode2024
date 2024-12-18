from grid import Grid, Vector
from typing import Generator


# forward declaration
class Path:
    ...


class Path:
    def __init__(self, grid: Grid, locations: tuple[Vector]):
        self.grid = grid
        self.locations = locations

    def __getitem__(self, index: int) -> Vector:
        return self.locations[index]

    def __len__(self) -> int:
        return len(self.locations)

    def __contains__(self, target) -> bool:
        return target in self.locations

    def __iter__(self) -> list[Vector]:
        return iter(self.locations)

    def __add__(self, target: Vector) -> Path:
        return Path(self.grid, self.locations + (target,))

    def __str__(self) -> str:
        return "Path[" + ", ".join([f"({vec.x},{vec.y})" for vec in self]) + "]"

    @property
    def steps(self) -> int:
        return len(self) - 1

    @property
    def last(self) -> Vector:
        return self.locations[-1]

    @property
    def is_complete(self) -> bool:
        return self.last == self.grid.end

    def child_paths(self) -> Generator[Path, None, None]:
        for target in self.grid.empty_and_adjacent_to(self.last):
            if target in self.locations:
                continue
            yield self + target

    @classmethod
    def solutions(cls, grid) -> Generator[Path, None, None]:
        def recur(path: Path):
            if path.is_complete:
                yield path
            else:
                for child in path.child_paths():
                    yield from recur(child)

        yield from recur(Path(grid, (grid.start,)))

    @classmethod
    def shortest_solution(cls, grid: Grid, verbose: bool = False) -> Path:
        locs = set(grid.start)
        leaves = [Path(grid, (grid.start,))]
        while len(leaves) > 0:
            if verbose:
                print(
                    f"leaves: {len(leaves)}|".ljust(20) + f"locs: {len(locs)}".ljust(20),
                    end="\r",
                )
            new_leaves = []
            for leaf in leaves:
                for new_leaf in leaf.child_paths():
                    if new_leaf.is_complete:
                        if verbose:
                            print()
                        return new_leaf
                    if new_leaf.last in locs:
                        continue
                    new_leaves.append(new_leaf)
                leaves = new_leaves
                for leaf in leaves:
                    locs.add(leaf.last)
        return None
