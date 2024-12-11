from day11 import (
    Stone,
    StoneLine,
)


print(StoneLine.from_nums(0, 1, 10, 99, 999).next_line())

for sl in StoneLine.from_nums(125, 17).sequence(max_iter=7):
    print(sl)

print(len(StoneLine.from_nums(125, 17).blink(25)))


for sl in StoneLine.from_nums(0).sequence(max_iter=7):
    print(sl)
