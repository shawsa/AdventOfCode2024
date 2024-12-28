from dataclasses import dataclass
from grid import Vector, Grid, Tile
from enum import Enum
from typing import Generator


class Button(Tile):
    pass


ACTIVATE = Button("A")


class Move(Enum):
    UP = Vector(-1, 0)
    DOWN = Vector(1, 0)
    LEFT = Vector(0, -1)
    RIGHT = Vector(0, 1)


MoveSequence = tuple[Move]


class Keypad(Grid):
    def __init__(self, key_string: str):
        buttons = []
        for row in key_string.split("\n"):
            buttons.append([Button(c) for c in row])
        super().__init__(buttons)

        self.gap = None
        try:
            self.gap = self.loc(" ")
        except ValueError:
            pass

    def loc(self, target: Button) -> Vector:
        if not isinstance(target, Button):
            target = Button(str(target))

        for loc, button in self.enumerate():
            if target == button:
                return loc
        raise ValueError(f"No button '{button.value}' found")

    def valid_moves(self, start: Vector, moves: MoveSequence) -> bool:
        if self.gap is None:
            return True
        if start == self.gap:
            return False
        loc = start
        for move in moves:
            loc = loc + move.value
            if loc == self.gap:
                return False
        return True

    def shortest_paths(self, start: Button, end: Button) -> list[MoveSequence]:
        start_loc = self.loc(start)
        end_loc = self.loc(end)
        return self.shortest_paths_by_loc(start_loc, end_loc)

    def shortest_paths_by_loc(
        self, start_loc: Vector, end_loc: Vector
    ) -> list[MoveSequence]:
        difference = end_loc - start_loc
        if difference.row < 0:
            vertical_moves = [Move.UP for _ in range(-difference.row)]
        else:
            vertical_moves = [Move.DOWN for _ in range(difference.row)]
        if difference.col < 0:
            horizontal_moves = [Move.LEFT for _ in range(-difference.col)]
        else:
            horizontal_moves = [Move.RIGHT for _ in range(difference.col)]

        first = tuple(vertical_moves + horizontal_moves)
        second = tuple(horizontal_moves + vertical_moves)
        if 0 in difference:
            # one list was empty, so first and second are the same
            return [first]

        return [
            my_moves
            for my_moves in [first, second]
            if self.valid_moves(start_loc, my_moves)
        ]


class DirectionalKeypad(Keypad):
    def __init__(self):
        super().__init__(" ^A\n<v>")
        self.loc_up = self.loc("^")
        self.loc_down = self.loc("v")
        self.loc_left = self.loc("<")
        self.loc_right = self.loc(">")


class NumericKeypad(Keypad):
    def __init__(self):
        super().__init__("789\n456\n123\n 0A")


ButtonSequence = list[Button]


def button_sequence_to_str(seq: ButtonSequence) -> str:
    return "".join(str(b) for b in seq)


class RobotArm:
    def __init__(self, keypad: Keypad):
        self.keypad = keypad

    def move_to_button(self, move: Move) -> Button:
        if move == Move.UP:
            return Button("^")
        if move == Move.DOWN:
            return Button("v")
        if move == Move.LEFT:
            return Button("<")
        if move == Move.RIGHT:
            return Button(">")
        raise ValueError(f"{move} is not in {list(Move)}")

    def input_sequences(
        self,
        start: Button,
        output_sequence: ButtonSequence,
    ) -> Generator[ButtonSequence, None, None]:
        if len(output_sequence) == 0:
            yield []
        else:
            next_button = output_sequence[0]
            remainder = output_sequence[1:]
            for trailing_sequence in self.input_sequences(next_button, remainder):
                for path in self.keypad.shortest_paths(start=start, end=next_button):
                    yield [self.move_to_button(move) for move in path] + [
                        ACTIVATE
                    ] + trailing_sequence

    def input_strings(self, start: str, output: str) -> Generator[str, None, None]:
        start_button = Button(start)
        output_seq = [Button(c) for c in output]
        for button_seq in self.input_sequences(start_button, output_seq):
            yield button_sequence_to_str(button_seq)


class Chain:
    def __init__(self, num_bots: int):
        assert num_bots > 0
        self.robots = [RobotArm(DirectionalKeypad()) for _ in range(num_bots - 1)] + [
            RobotArm(NumericKeypad())
        ]

    def input_sequences(
        self, output_sequence: str
    ) -> Generator[ButtonSequence, None, None]:
        output = [Button(c) for c in output_sequence]

        def recur(
            robots: list[RobotArm], output: ButtonSequence
        ) -> Generator[ButtonSequence, None, None]:
            if len(robots) == 0:
                yield output
            else:
                robot = robots[-1]
                remainder = robots[:-1]
                for seq in robot.input_sequences(ACTIVATE, output):
                    yield from recur(remainder, seq)

        yield from recur(self.robots, output)

    def shortest_seq(self, output_sequence: str) -> str:
        sequences = list(self.input_sequences(output_sequence))
        sequences.sort(key=lambda seq: len(seq))
        return button_sequence_to_str(sequences[0])

    def complexity(self, code: str) -> int:
        value = int(code[:-1])
        return len(self.shortest_seq(code)) * value
