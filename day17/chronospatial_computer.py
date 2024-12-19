from dataclasses import dataclass
from enum import Enum
from more_itertools import chunked
from typing import Callable, Generator


@dataclass
class State:
    counter: int
    A: int
    B: int
    C: int
    output: list[int]


Program = list[int]


class Opcode(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


class Operand:
    def __init__(self, literal: int):
        self.literal = literal

    def value(self, state: State) -> int:
        """The value of the combo operand"""
        if self.literal <= 3:
            return self.literal
        if self.literal == 4:
            return state.A
        if self.literal == 5:
            return state.B
        if self.literal == 6:
            return state.C
        raise ValueError(f"{self.literal} is not a valid operand")


OPS_DICT = {}


def register_opcode(opcode: Opcode):
    def decorator(func: Callable[[State, Operand], State]) -> Callable[[State], State]:
        OPS_DICT[opcode] = func
        return func

    return decorator


@register_opcode(Opcode.ADV)
def adv(state: State, operand: Operand) -> State:
    numerator = state.A
    exponent = operand.value(state)
    new_A = numerator // (2**exponent)
    return State(
        counter=state.counter + 2,
        A=new_A,
        B=state.B,
        C=state.C,
        output=state.output,
    )


@register_opcode(Opcode.BXL)
def bxl(state: State, operand: Operand) -> State:
    new_B = state.B ^ operand.literal
    return State(
        counter=state.counter + 2,
        A=state.A,
        B=new_B,
        C=state.C,
        output=state.output,
    )


@register_opcode(Opcode.BST)
def bst(state: State, operand: Operand) -> State:
    new_B = operand.value(state) % 8
    return State(
        counter=state.counter + 2,
        A=state.A,
        B=new_B,
        C=state.C,
        output=state.output,
    )


@register_opcode(Opcode.JNZ)
def jnz(state: State, operand: Operand) -> State:
    if state.A == 0:
        return State(
            counter=state.counter + 2,
            A=state.A,
            B=state.B,
            C=state.C,
            output=state.output,
        )
    else:
        return State(
            counter=operand.literal,
            A=state.A,
            B=state.B,
            C=state.C,
            output=state.output,
        )


@register_opcode(Opcode.BXC)
def bxc(state: State, operand: Operand) -> State:
    new_B = state.B ^ state.C
    return State(
        counter=state.counter + 2,
        A=state.A,
        B=new_B,
        C=state.C,
        output=state.output,
    )


@register_opcode(Opcode.OUT)
def out(state: State, operand: Operand) -> State:
    return State(
        counter=state.counter + 2,
        A=state.A,
        B=state.B,
        C=state.C,
        output=state.output + [operand.value(state) % 8],
    )


@register_opcode(Opcode.BDV)
def bdv(state: State, operand: Operand) -> State:
    numerator = state.A
    exponent = operand.value(state)
    new_B = numerator // (2**exponent)
    return State(
        counter=state.counter + 2,
        A=state.A,
        B=new_B,
        C=state.C,
        output=state.output,
    )


@register_opcode(Opcode.CDV)
def cdv(state: State, operand: Operand) -> State:
    numerator = state.A
    exponent = operand.value(state)
    new_C = numerator // (2**exponent)
    return State(
        counter=state.counter + 2,
        A=state.A,
        B=state.B,
        C=new_C,
        output=state.output,
    )


def generate_state_sequence(
    initial_state: State, program: Program
) -> Generator[State, None, None]:
    state = initial_state
    yield state
    while state.counter < len(program):
        opcode = Opcode(program[state.counter])
        operand = Operand(program[state.counter + 1])
        state = OPS_DICT[opcode](state, operand)
        yield state


def run_program(initial_state: State, program: Program) -> str:
    for state in generate_state_sequence(initial_state, program):
        pass
    return ",".join(map(str, state.output))


def human_readable_instruction(line: int, program: Program) -> str:
    opcode = Opcode(program[line])
    operand = Operand(program[line + 1])
    literal = str(operand.literal)
    if operand.literal <= 3:
        combo = str(operand.literal)
    elif operand.literal == 4:
        combo = "A"
    elif operand.literal == 5:
        combo = "B"
    elif operand.literal == 6:
        combo = "C"

    if opcode == Opcode.ADV:
        return (
            f"{line:>3}| {opcode}, on {literal}".ljust(30) + f"A <- A // (2**{combo})"
        )
    elif opcode == Opcode.BXL:
        return f"{line:>3}| {opcode}, on {literal}".ljust(30) + f"B <- B XOR {literal}"
    elif opcode == Opcode.BST:
        return f"{line:>3}| {opcode}, on {literal}".ljust(30) + f"B <- {combo}%8"
    elif opcode == Opcode.JNZ:
        return (
            f"{line:>3}| {opcode}, on {literal}".ljust(30) + f"if A != 0 JUMP {literal}"
        )
    elif opcode == Opcode.BXC:
        return f"{line:>3}| {opcode}, on {literal}".ljust(30) + "B <- B XOR C"
    elif opcode == Opcode.OUT:
        return f"{line:>3}| {opcode}, on {literal}".ljust(30) + f"OUTPUT {combo}%8"
    elif opcode == Opcode.BDV:
        return (
            f"{line:>3}| {opcode}, on {literal}".ljust(30) + f"B <- A // (2**{combo})"
        )
    elif opcode == Opcode.CDV:
        return (
            f"{line:>3}| {opcode}, on {literal}".ljust(30) + f"C <- A // (2**{combo})"
        )
    else:
        raise ValueError(f"{opcode} is not an Opcode")


def human_readable_sequence(program: Program) -> Generator[str, None, None]:
    assert len(program) % 2 == 0
    for half_line, (op_int, arg_int) in enumerate(chunked(program, 2)):
        line = str(half_line * 2)
        yield human_readable_instruction(line, program)


def assemble(program: Program) -> str:
    instructions = []
    for line in range(0, len(program), 2):
        instructions.append(human_readable_instruction(line, program))
    return "\n".join(instructions)
