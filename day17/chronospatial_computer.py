from dataclasses import dataclass
from enum import Enum
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
