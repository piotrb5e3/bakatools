from typing import NamedTuple

from bakatools.tudi.vector import Vector2D


class Line2D(NamedTuple):
    p1: Vector2D
    p2: Vector2D

    def is_along_the_grid(self) -> bool:
        return not (self.p1.x != self.p2.x and self.p1.y != self.p2.y)

    @property
    def direction(self) -> Vector2D:
        return self.p2.add(self.p1.mul(-1))

    @property
    def length(self) -> int | float:
        return self.direction.length

    @property
    def manhattan_length(self) -> int | float:
        direction = self.direction
        return abs(direction.x) + abs(direction.y)

    @property
    def int_length(self) -> int:
        return self.direction.int_length
