from chronospatial_computer import (
    State,
    Program,
    generate_state_sequence,
    human_readable_instruction,
)

from math import ceil
from more_itertools import chunked


from termcolor import colored


class BinaryFormater:
    def __init__(self, num: int):
        self.num = num
        self.bin_string = bin(self.num)[2:]
        self.pad(len(self.bin_string))

    def pad(self, min_len: int) -> None:
        new_len = max(6, ceil(min_len / 6) * 6)
        self.bin_string = self.bin_string.rjust(new_len, "0")

    def __len__(self) -> int:
        return len(self.bin_string)

    def __str__(self) -> str:
        byte_list = list(map(lambda lst: "".join(lst), chunked(self.bin_string, 3)))

        def colored_byte(my_byte, index):
            if index % 2 == 0:
                return colored(my_byte, "light_grey", attrs=["dark"])
            else:
                return colored(my_byte, attrs=["bold"])

        return "".join(
            [colored_byte(byte, index) for index, byte in enumerate(byte_list)]
        )


def debug(initial_state: State, program: Program, binary: bool = False) -> None:
    """Print the state followed by the instruction."""
    state_seq = generate_state_sequence(initial_state, program)
    state = next(state_seq)

    def print_binary_state(state: State):
        A = BinaryFormater(state.A)
        B = BinaryFormater(state.B)
        C = BinaryFormater(state.C)
        max_len = max(map(len, [A, B, C]))
        A.pad(max_len)
        B.pad(max_len)
        C.pad(max_len)
        print(f"\tCNT={state.counter:>3}")
        print("\tA=" + str(A) + f" = {state.A}")
        print("\tB=" + str(B) + f" = {state.B}")
        print("\tC=" + str(C) + f" = {state.C}")
        print(f"\tOUT = {state.output}")

    if binary:
        print_binary_state(state)
    else:
        print(state)
    for new_state in state_seq:
        print(human_readable_instruction(state.counter, program))
        state = new_state
        if binary:
            print_binary_state(state)
        else:
            print(state)
