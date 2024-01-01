from typing import TypeVar

T = TypeVar("T")


def trailing_cycle_finder(data: list[T], pattern_length_step: int) -> int | None:
    pattern_length = pattern_length_step

    while pattern_length <= len(data) // 2:
        if all(
            data[-i] == data[-pattern_length - i] for i in range(1, pattern_length + 1)
        ):
            return pattern_length
        pattern_length += pattern_length_step

    return None
