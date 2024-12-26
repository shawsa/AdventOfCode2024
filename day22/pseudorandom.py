from more_itertools import nth
from typing import Generator


# forward declaration
class SecretNumber:
    ...


class SecretNumber:
    def __init__(self, value: int):
        self.value = value

    def __repr__(self) -> str:
        return f"SecretNumber({self.value})"

    def __str__(self) -> str:
        return str(self.value)

    def mix(self, value) -> SecretNumber:
        return SecretNumber(self.value ^ value)

    def prune(self) -> SecretNumber:
        return SecretNumber(self.value % 2**24)

    def mix_and_prune(self, value: int):
        return self.mix(value).prune()

    def next_number(self) -> SecretNumber:
        new_num = self.mix_and_prune(self.value * 64)
        new_num = new_num.mix_and_prune(new_num.value // 32)
        new_num = new_num.mix_and_prune(new_num.value * 2048)
        return new_num

    def sequence(self) -> Generator[SecretNumber, None, None]:
        num = self
        while True:
            yield num
            num = num.next_number()


def get_2000th(value: int) -> SecretNumber:
    return nth(SecretNumber(value).sequence(), 2000)
