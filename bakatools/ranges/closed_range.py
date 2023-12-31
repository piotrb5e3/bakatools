from typing import NamedTuple


class ClosedRange(NamedTuple):
    """Represents a range that contains its ends"""
    start: int
    end: int

    @property
    def total_length(self) -> int:
        return self.end - self.start + 1

    def intersects(self, other: "ClosedRange") -> bool:
        return (
                self.start <= other.start <= self.end or
                self.start <= other.end <= self.end or
                other.start <= self.start <= other.end or
                other.start <= self.end <= other.end
        )