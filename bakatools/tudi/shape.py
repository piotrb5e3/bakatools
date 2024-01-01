from typing import Iterable, TypeVar

from .grid import Grid2D
from .vector import Vector2D

T = TypeVar("T")


class Shape2D(set[Vector2D]):
    def get_bounding_box(self) -> tuple[Vector2D, Vector2D]:
        return (
            Vector2D(
                min(e.x for e in self),
                min(e.y for e in self),
            ),
            Vector2D(
                max(e.x for e in self),
                max(e.y for e in self),
            ),
        )

    def get_x_span(self):
        return max(e.x for e in self) - min(e.x for e in self) + 1

    def get_y_span(self):
        return max(e.y for e in self) - min(e.y for e in self) + 1

    def intersects_with(self, other: "Shape2D") -> bool:
        if len(other) < len(self):
            return any(o in self for o in other)
        return any(o in other for o in self)

    def add(self, vec: Vector2D) -> "Shape2D":
        return Shape2D(e.add(vec) for e in self)

    def combine(self, other: "Shape2D") -> "Shape2D":
        return Shape2D(self.union(other))

    def combine_in_place(self, other: "Shape2D") -> None:
        self.update(other)

    def __str__(self):
        bb = self.get_bounding_box()
        return "\n".join(
            "".join(
                "#" if Vector2D(x, y) in self else "."
                for x in range(bb[0].x, bb[1].x + 1)
            )
            for y in range(bb[0].y, bb[1].y + 1)
        )

    @staticmethod
    def from_grid(grid: Grid2D[T], occupied: Iterable[T]) -> "Shape2D":
        return Shape2D(k for k, v in grid.items() if v in occupied)
