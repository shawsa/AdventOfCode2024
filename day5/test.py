from day5 import (
    load_input,
    sum_middle_correct,
    sum_middle_fixed,
)

after_dict, updates = load_input("part_one_test.txt")
print(sum_middle_correct(updates, after_dict))
print(sum_middle_fixed(updates, after_dict))
