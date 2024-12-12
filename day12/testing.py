from day12 import Garden, part_one, FencePiece, Location, FenceSide, count_sides


string = """AAAA
BBCD
BBCC
EEEC"""

garden = Garden(string)
for region in garden.regions():
    print(f"{region.area()=}")
    print(f"{region.perimiter()=}")
    print(garden.show_region(region))

print(part_one(garden))

larger_string = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

print(part_one(Garden(larger_string)))

for region in garden.regions:
    print(f"sides: {count_sides(region)}")
    print(garden.show_region(region))

pieces = [
    FencePiece(Location(0, 0), Location(1, 0)),
    FencePiece(Location(0, 2), Location(1, 2)),
    FencePiece(Location(0, 4), Location(1, 4)),
]
fs = FenceSide(FencePiece(Location(0, 3), Location(1, 3)))
fs.aquire_pieces(pieces)
print(fs)
print(pieces)

string_E = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""

garden = Garden(string_E)
for region in garden.regions:
    print(f"sides: {count_sides(region)}")
    print(garden.show_region(region))
