from queue import SimpleQueue
from typing import Optional, TypeVar, Iterable, Counter

T = TypeVar("T")


def all_different_values_start(sequence: Iterable[T], pattern_length: int) -> Optional[int]:
    window_counter = Counter[T]()
    result = 0

    si = iter(sequence)
    q = SimpleQueue()

    for _ in range(pattern_length):
        result += 1
        next_chr = next(si)
        q.put(next_chr)
        window_counter.update([next_chr])

    for next_chr in si:
        if window_counter.most_common(n=1)[0][1] == 1:
            return result
        result += 1
        q.put(next_chr)
        window_counter.update([next_chr])
        window_counter.subtract([q.get()])

    return None
