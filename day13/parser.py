from parsy import (
    digit,
    generate,
    string,
)

number = digit.at_least(1).concat().map(int)


@generate
def button():
    yield string("Button ")
    name = yield string("A") | string("B")
    yield string(": X+")
    x = yield number
    yield string(", Y+")
    y = yield number
    return name, x, y


@generate
def prize():
    yield string("Prize: X=")
    x = yield number
    yield string(", Y=")
    y = yield number
    return x, y


@generate
def machine():
    a = yield button
    yield string("\n")
    b = yield button
    yield string("\n")
    p = yield prize
    return a, b, p
