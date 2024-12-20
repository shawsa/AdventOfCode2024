from parsy import string, eof, generate
from towels import Towel, Design, Stripe


white = string("w")
blue = string("u")
black = string("b")
red = string("r")
green = string("g")

stripe = white | blue | black | red | green
design = stripe.many()
towel = design

towels = design.sep_by(string(", "))
designs = design.sep_by(string("\n"))


@generate
def input_parser():
    ts = yield towels
    yield string("\n").many()
    ds = yield designs
    yield eof
    return ts, ds


def parse_input(input_string: str):
    ts, ds = input_parser.parse(input_string)
    towels = [Towel(tuple(Stripe(s) for s in t)) for t in ts]
    designs = [Design(tuple(Stripe(s) for s in d)) for d in ds]
    return towels, designs
