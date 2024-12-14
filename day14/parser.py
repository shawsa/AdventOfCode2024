from parsy import (
    digit,
    generate,
    string,
)


number = digit.at_least(1).concat().map(int)


@generate
def integer():
    negative = yield string("-").optional()
    val = yield number
    if negative is not None:
        return -val
    return val


@generate
def robot():
    yield string("p=")
    px = yield integer
    yield string(",")
    py = yield integer
    yield string(" v=")
    vx = yield integer
    yield string(",")
    vy = yield integer
    return (px, py), (vx, vy)

