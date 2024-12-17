from chronospatial_computer import State
from parsy import (
    digit,
    eof,
    generate,
    string,
)


number = digit.at_least(1).concat().map(int)


@generate
def register():
    yield string("Register ")
    yield string("A") | string("B") | string("C")
    yield string(": ")
    value = yield number
    return value


@generate
def program():
    yield string("Program: ")
    nums = number.sep_by(string(","))
    return nums


@generate
def program_info():
    A = yield register
    yield string("\n")
    B = yield register
    yield string("\n")
    C = yield register
    yield string("\n")
    yield string("\n")
    prog = yield program
    state = State(
        counter=0,
        A=A,
        B=B,
        C=C,
        output=[],
    )
    return state, prog
