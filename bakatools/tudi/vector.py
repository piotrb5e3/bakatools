from decimal import Decimal
from fractions import Fraction
from math import sqrt
from typing import NamedTuple, TypeVar

T = TypeVar("T", int, float, Decimal, Fraction)


class Vector2D(NamedTuple):
    x: T
    y: T

    def add(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x + other.x, self.y + other.y)

    def mul(self, by: T) -> "Vector2D":
        return Vector2D(self.x * by, self.y * by)

    def div(self, by: T) -> "Vector2D":
        return Vector2D(self.x / by, self.y / by)

    def rotate_clockwise(self) -> "Vector2D":
        return Vector2D(self.y, self.x * -1)

    def rotate_counterclockwise(self) -> "Vector2D":
        return Vector2D(self.y * -1, self.x)

    def adjacent(self, other: "Vector2D") -> bool:
        """True if the other vector is on a neighboring (also diagonally) square. Includes being at the same square."""
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1

    @property
    def length(self) -> float:
        return sqrt(pow(self.x, 2) + pow(self.y, 2))

    @property
    def int_length(self) -> int:
        l = self.length
        if l != int(l):
            ValueError("Only call int_length on vectors with integer length!")
        return int(l)

    def to_unit(self) -> "Vector2D":
        return self.div(self.length)

    @staticmethod
    def from_str(s: str) -> "Vector2D":
        x_s, y_s = s.split(",")
        return Vector2D(int(x_s.strip()), int(y_s.strip()))


V2D = Vector2D
