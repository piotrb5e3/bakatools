from typing import TypeVar, Callable, Iterable

T = TypeVar("T")


def find_first_index(l: Iterable[T], classifier: Callable[[T], bool]) -> int:
    try:
        return next(idx for idx, v in enumerate(l) if classifier(v))
    except StopIteration:
        return -1
