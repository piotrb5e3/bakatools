from typing import Callable, TypeVar

from .polygon import PolygonalChain
from ..graph.dag import DirectedGraph
from .directions import direction_vectors
from .vector import Vector2D

T = TypeVar("T")


class Grid2D(dict[Vector2D, T]):
    x_span: int
    y_span: int

    def draw_poly(self, poly: PolygonalChain, fill: T):
        segments = list(poly.segments)
        if any(not s.is_along_the_grid() for s in segments):
            raise ValueError("We can only draw lines that go along the grid!")

        for s in segments:
            segment_direction = s.direction.to_unit()
            s_pos = s.p1
            for _ in range(s.int_length):
                self[s_pos] = fill
                s_pos = s_pos.add(segment_direction)
            self[s_pos] = fill

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

    @staticmethod
    def from_bounds(min_x: int, max_x: int, min_y: int, max_y: int, fill: T) -> "Grid2D[T]":
        assert max_x >= min_x
        assert max_y >= min_y
        result = Grid2D[T]()
        result.x_span = max_x - min_x + 1
        result.y_span = max_y - min_y + 1
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                result[Vector2D(x, y)] = fill
        return result

    def to_graph(
            self, can_go_from_to: Callable[[T, Vector2D, T], bool]
    ) -> DirectedGraph[Vector2D]:
        result: dict[Vector2D, dict[Vector2D, int]] = {k: dict() for k in self.keys()}

        for start_pos, start_v in self.items():
            for direction in direction_vectors:
                new_pos = start_pos.add(direction)
                if new_pos in self and can_go_from_to(
                        self[start_pos], direction, self[new_pos]
                ):
                    result[start_pos][new_pos] = 1

        return DirectedGraph[Vector2D](result)

    def __str__(self) -> str:
        min_x = min(p.x for p in self.keys())
        max_x = max(p.x for p in self.keys())
        min_y = min(p.y for p in self.keys())
        max_y = max(p.y for p in self.keys())
        return (
            f"Grid2D(x: [{min_x},{max_x}]; y: [{min_y},{max_y}]]\n" +
            "\n".join(
                "".join(str(self[Vector2D(x, y)])
                        for x in range(min_x, max_x + 1)
                        ) for y in range(min_y, max_y + 1))
        )


T2 = TypeVar("T2")


def transform_values(grid: Grid2D[T], f: Callable[[T], T2]) -> Grid2D[T2]:
    result = Grid2D[T2]({k: f(v) for k, v in grid.items()})
    result.x_span = grid.x_span
    result.y_span = grid.y_span
    return result


def visible_points(grid: Grid2D[int]) -> set[Vector2D]:
    visible = set[Vector2D]()

    for x in range(grid.x_span):
        top = -1
        for y in range(grid.y_span):
            tree = Vector2D(x, y)
            h = int(grid[tree])
            if grid[tree] > top:
                visible.add(tree)
                top = grid[tree]

    for x in range(grid.x_span):
        top = -1
        for y in reversed(range(grid.y_span)):
            tree = Vector2D(x, y)
            h = int(grid[tree])
            if grid[tree] > top:
                visible.add(tree)
                top = grid[tree]

    for y in range(grid.y_span):
        top = -1
        for x in range(grid.x_span):
            tree = Vector2D(x, y)
            if grid[tree] > top:
                visible.add(tree)
                top = grid[tree]

    for y in range(grid.y_span):
        top = -1
        for x in reversed(range(grid.x_span)):
            tree = Vector2D(x, y)
            if grid[tree] > top:
                visible.add(tree)
                top = grid[tree]
    return visible
