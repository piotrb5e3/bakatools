from .cycles import trailing_cycle_finder


def extrapolate_linear_sequence_using_cyclic_deltas(
    data: list[int], target: int, pattern_length_step: int
) -> int | None:
    if target <= len(data) - 1:
        raise ValueError("Target should be outside of the initial data range")

    delta = [d2 - d1 for d1, d2 in zip(data[:-1], data[1:])]

    pattern_length = trailing_cycle_finder(delta, pattern_length_step)
    if pattern_length is None:
        return None

    runup = len(data) - pattern_length
    multiples = (target - runup) // pattern_length
    rest = (target - runup) % pattern_length

    result = (
        data[runup]
        + multiples * (data[-1] - data[-pattern_length - 1])
        + (data[-pattern_length + rest] - data[-pattern_length])
    )
    return result
