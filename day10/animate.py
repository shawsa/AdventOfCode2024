from day10 import Topography, Trail, Place, Coordinates, trails_in, load_input
from termcolor import colored
from itertools import product
from time import sleep


def hilight(string: str) -> str:
    return colored(string, "green", attrs=["bold"])


def start_hilight(string: str) -> str:
    return colored(string, "red", attrs=["bold"])


def end_hilight(string: str) -> str:
    return colored(string, "red", attrs=["bold"])


def dim(string: str) -> str:
    return colored(string, "dark_grey")


def in_trail(place: Place, trail: Trail) -> bool:
    return any(place == p for p in trail.places)


def hilight_trail_in_top(trail: Trail, top: Topography) -> str:

    def format(place: Place) -> str:
        if in_trail(place, trail):
            if place == trail[0]:
                return start_hilight(place.val)
            if place == trail[-1]:
                return end_hilight(place.val)
            return hilight(place.val)
        else:
            return dim(place.val)

    chars = []
    for row in range(top.rows):
        for col in range(top.cols):
            place = Place((row, col), top[row, col])
            chars.append(format(place))
        chars.append("\n")

    return "".join(chars)


if __name__ == "__main__":
    string = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

    string = load_input()

    top = Topography(string)

    rows = top.rows + 1
    LINE_UP = "\033[1A"
    LINE_CLEAR = "\x1b[2K"
    if True:
        for index, trail in enumerate(trails_in(top)):
            print(hilight_trail_in_top(trail, top))
            if index < 20:
                sleep(0.5)
            else:
                sleep(0.01)
            for _ in range(rows):
                print(LINE_UP, end=LINE_CLEAR)
        print(hilight_trail_in_top(trail, top))
