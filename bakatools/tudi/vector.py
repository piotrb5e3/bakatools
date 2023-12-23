from typing import NamedTuple


class Vector2D(NamedTuple):
    x: int
    y: int

    def add(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x + other.x, self.y + other.y)

    def mul(self, by: int) -> "Vector2D":
        return Vector2D(self.x * by, self.y * by)

    def rotate_clockwise(self) -> "Vector2D":
        return Vector2D(self.y, self.x * -1)

    def rotate_counterclockwise(self) -> "Vector2D":
        return Vector2D(self.y * -1, self.x)
