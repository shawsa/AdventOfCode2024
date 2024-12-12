from day12 import Garden, part_one


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
