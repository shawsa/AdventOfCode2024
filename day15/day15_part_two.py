from collections import namedtuple
from enum import StrEnum
from itertools import product
from typing import Generator


def load_input() -> str:
    with open("input.txt", "r") as f:
        ret = f.read().strip()
    return ret


class Move(StrEnum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


class Tile(StrEnum):
    WALL = "#"
    LBOX = "["
    RBOX = "]"
    EMPTY = "."
    BOT = "@"


BOXES = (Tile.LBOX, Tile.RBOX)


TileMatrix = tuple[tuple[Tile]]
MutableTileMatrix = list[list[Tile]]

Coord = namedtuple("Coord", ["row", "col"])


# forward declaration
class Grid:
    ...


class Grid:
    def __init__(self, tiles: TileMatrix, bot: Coord | None = None):
        self.tiles = tiles
        self.rows = len(tiles)
        self.cols = len(tiles[0])
        if bot is None:
            for row, col in product(range(self.rows), range(self.cols)):
                if self[(row, col)] == Tile.BOT:
                    bot = Coord(row, col)
                    break
        assert bot is not None
        self.bot = bot
        assert self[bot] == Tile.BOT

    @classmethod
    def parse_string(cls, string: str) -> Grid:
        tiles = []
        for line in string.split("\n"):
            row = []
            for c in line:
                if c == "#":
                    row.append(Tile.WALL)
                    row.append(Tile.WALL)
                elif c == "O":
                    row.append(Tile.LBOX)
                    row.append(Tile.RBOX)
                elif c == ".":
                    row.append(Tile.EMPTY)
                    row.append(Tile.EMPTY)
                elif c == "@":
                    row.append(Tile.BOT)
                    row.append(Tile.EMPTY)
                else:
                    raise ValueError(f'"{c}" not in {list(Tile)}')
            tiles.append(row)
        return Grid(tuple(tuple(t for t in row) for row in tiles))

    def __getitem__(self, coord: Coord) -> Tile:
        row, col = coord
        return self.tiles[row][col]

    def __str__(self) -> str:
        return "\n".join("".join(tile for tile in row) for row in self.tiles)

    def get_target(self, coord: Coord, move: Move) -> Coord:
        row, col = coord
        if move == Move.UP:
            return Coord(row - 1, col)
        elif move == Move.DOWN:
            return Coord(row + 1, col)
        elif move == Move.LEFT:
            return Coord(row, col - 1)
        elif move == Move.RIGHT:
            return Coord(row, col + 1)
        else:
            raise ValueError(f"{move} not in {list(Move)}")

    def can_move(self, coord: Coord, move: Move) -> bool:
        target = self.get_target(coord, move)
        if self[target] == Tile.WALL:
            return False
        if self[target] == Tile.EMPTY:
            return True
        if move in [Move.LEFT, Move.RIGHT]:
            # left and right are the same
            if self[target] in BOXES:
                return self.can_move(target, move)
        else:
            # up and down are recursive
            if self[target] == Tile.LBOX:
                target2 = Coord(target.row, target.col + 1)
            else:
                target2 = Coord(target.row, target.col - 1)
            return self.can_move(target, move) and self.can_move(target2, move)
        raise ValueError(f"target @ {target} cannot be a {self[target]}")

    def _make_move(
        self, coord: Coord, move: Move, tiles: MutableTileMatrix | None = None
    ) -> MutableTileMatrix:
        if tiles is None:
            tiles = [[t for t in row] for row in self.tiles]
        target = self.get_target(coord, move)
        target_tile = tiles[target.row][target.col]
        my_tile = tiles[coord.row][coord.col]
        if target_tile in BOXES:
            if move in [Move.LEFT, Move.RIGHT]:
                # left and right are the same
                if target_tile in BOXES:
                    tiles = self._make_move(target, move, tiles)
            else:
                # up and down are recursive
                if target_tile in BOXES:
                    if target_tile == Tile.LBOX:
                        target2 = Coord(target.row, target.col + 1)
                    elif target_tile == Tile.RBOX:
                        target2 = Coord(target.row, target.col - 1)
                    tiles = self._make_move(target, move, tiles)
                    tiles = self._make_move(target2, move, tiles)
        if tiles[target.row][target.col] == Tile.EMPTY:
            tiles[target.row][target.col] = my_tile
            tiles[coord.row][coord.col] = Tile.EMPTY
            return tiles
        raise ValueError(
            f"Trying to move into {tiles[target.row][target.col]} at {target}"
        )

    def make_move(self, move: Move) -> Grid:
        if self.can_move(self.bot, move):
            new_bot = self.get_target(self.bot, move)
            new_tiles = tuple(
                tuple(Tile(c) for c in line) for line in self._make_move(self.bot, move)
            )

            return Grid(new_tiles, new_bot)
        else:
            return self

    def make_moves(self, moves: list[Move]) -> Grid:
        grid = self
        for move in moves:
            grid = grid.make_move(move)
        return grid

    def sequence(self, moves: list[Move]) -> Generator[Grid, None, None]:
        grid = self
        yield grid
        for move in moves:
            grid = grid.make_move(move)
            yield grid

    def GPS(self, target: Coord) -> int:
        return 100 * target.row + target.col

    def sum_GPS(self) -> int:
        total = 0
        for row, col in product(range(self.rows), range(self.cols)):
            if self[row, col] == Tile.LBOX:
                total += self.GPS(Coord(row, col))
        return total


def parse_input(string: str) -> tuple[Grid, list[Move]]:
    grid_str, move_string = string.split("\n\n")
    grid = Grid.parse_string(grid_str)
    moves = [Move(c) for c in move_string.replace("\n", "")]
    return grid, moves


if __name__ == "__main__":
    grid, moves = parse_input(load_input())
    final_grid = grid.make_moves(moves)
    print(f"part_two: {final_grid.sum_GPS()}")
