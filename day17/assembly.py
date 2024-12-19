from chronospatial_computer import (
    State,
    run_program,
    generate_state_sequence,
)

from debugging import debug

from typing import Generator


def state_from_A(A: int) -> State:
    return State(counter=0, A=A, B=0, C=0, output=[])


def my_program(A: int) -> list[int]:
    """
    This is the assmbly version of my program.
      0| Opcode.BST, on 4         B <- A%8
      2| Opcode.BXL, on 2         B <- B XOR 2
      4| Opcode.CDV, on 5         C <- A // (2**B)
      6| Opcode.BXL, on 7         B <- B XOR 7
      8| Opcode.BXC, on 4         B <- B XOR C
     10| Opcode.ADV, on 3         A <- A // (2**3)
     12| Opcode.OUT, on 5         OUTPUT B%8
     14| Opcode.JNZ, on 0         if A != 0 JUMP 0

    This function converts it to python so that I can reason about it.
    """

    B = 0
    C = 0
    output = []

    while True:
        B = A % 8
        B = B ^ 2
        C = A // (2**B)
        B = B ^ 7
        B = B ^ C
        A = A // 8
        output.append(B % 8)
        if A == 0:
            break

    return output


def next_B(A):
    B = A % 8
    B = B ^ 2
    C = A // (2**B)  # in practice, C can be 3 bit
    B = B ^ 7
    B = B ^ C
    # B = B & C
    return B


def next_AB(A):
    # only the first 10 bits of A matter
    return A // 8, next_B(A % (2**10))


def same_program(A: int) -> list[int]:
    """
    A simplified version of the same program
    """
    output = []
    while True:
        A, B = next_AB(A)
        output.append(B % 8)
        if A == 0:
            break
    return output


def possible_previous_As(A: int, out: int) -> Generator[int, 0, 0]:
    for A8 in range(8):
        prev_A = A * 8 + A8
        if prev_A == A:
            continue
        new_A, new_B = next_AB(prev_A)
        if new_A == A and (new_B % 8) == out:
            yield prev_A


def generate_A(output: list[int]) -> int:
    def recur(A):
        A_out = my_program(A)
        if A_out == output:
            yield A
        if len(A_out) >= len(output):
            return None
        truncated_output = output[-len(A_out) :]
        if A_out != truncated_output:
            return None
        next_output = output[-len(A_out) - 1]
        for possible_A in possible_previous_As(A, next_output):
            yield from recur(possible_A)

    return next(recur(5))


if __name__ == "__main__":
    INITIAL_STATE = state_from_A(41644071)
    PROGRAM_STR = "2,4,1,2,7,5,1,7,4,4,0,3,5,5,3,0"
    PROGRAM = list(map(int, PROGRAM_STR.split(",")))
    debug(INITIAL_STATE, PROGRAM, binary=True)

    list(map(int, run_program(INITIAL_STATE, PROGRAM).split(",")))
    my_program(INITIAL_STATE.A)
    same_program(INITIAL_STATE.A)

    A = generate_A(PROGRAM)
    print(f"{A=}")
