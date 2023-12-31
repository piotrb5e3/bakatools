from typing import Iterable

from bakatools.tudi.line import Line2D
from bakatools.tudi.vector import Vector2D


class PolygonalChain(list[Vector2D]):
    @property
    def segments(self) -> Iterable[Line2D]:
        for p1, p2 in zip(self[:-1], self[1:]):
            yield Line2D(p1, p2)

    @staticmethod
    def from_line(line: str, separator: str) -> "PolygonalChain":
        res = []
        for node_s in line.split(separator):
            res.append(Vector2D.from_str(node_s))

        return PolygonalChain(res)

    @property
    def min_x(self) -> int:
        return min(n.x for n in self)

    @property
    def max_x(self) -> int:
        return max(n.x for n in self)

    @property
    def min_y(self) -> int:
        return min(n.y for n in self)

    @property
    def max_y(self) -> int:
        return max(n.y for n in self)
