from day17 import (
    State,
    run_program,
    generate_state_sequence,
)

INITIAL_STATE = State(counter=0, A=41644071, B=0, C=0, output=[])

PROGRAM_STR = "2,4,1,2,7,5,1,7,4,4,0,3,5,5,3,0"
PROGRAM = list(map(int, PROGRAM_STR.split(",")))


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


def all_possible_previous_A(A):
    higher_bits = A // 2**10
    for A_shift10 in range(2**10):
        new_A = higher_bits * 2**10 + A_shift10
        if new_A <= A:
            continue
        yield new_A


def generate_A(program):
    def recur(A, prog_A):
        print(A)
        if prog_A == program:
            yield A
        if len(prog_A) < len(program):
            for prev_A in all_possible_previous_A(A):
                new_prog = same_program(prev_A)
                print(new_prog)
                if new_prog == program[-len(new_prog) :]:
                    yield from recur(prev_A, new_prog)

    for A, prog in recur(0, []):
        yield A


list(map(int, run_program(INITIAL_STATE, PROGRAM).split(",")))
my_program(INITIAL_STATE.A)
same_program(INITIAL_STATE.A)

next(generate_A(PROGRAM))
