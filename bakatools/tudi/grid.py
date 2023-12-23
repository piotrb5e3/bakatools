from collections import defaultdict
from typing import Callable, TypeVar

from ..graph.dag import DirectedGraph
from .directions import direction_vectors
from .vector import Vector2D

T = TypeVar("T")


class Grid2D(dict[Vector2D, T]):
    x_span: int
    y_span: int

    @staticmethod
    def from_lines(lines: list[str]) -> "Grid2D[str]":
        assert len(lines) > 0
        assert all(len(line) == len(lines[0]) for line in lines)

        result = Grid2D[str]()
        result.x_span = len(lines[0])
        result.y_span = len(lines)

        for y, row in enumerate(lines):
            for x, c in enumerate(row):
                result[Vector2D(x, y)] = c

        return result

    def to_graph(
        self, can_go_from_to: Callable[[str, Vector2D, str], bool]
    ) -> DirectedGraph[Vector2D]:
        result: dict[Vector2D, dict[Vector2D, int]] = defaultdict(lambda: dict())

        for start_pos, start_v in self.items():
            for direction in direction_vectors:
                new_pos = start_pos.add(direction)
                if new_pos in self and can_go_from_to(
                    self[start_pos], direction, self[new_pos]
                ):
                    result[start_pos][new_pos] = 1

        return DirectedGraph[Vector2D](result)
