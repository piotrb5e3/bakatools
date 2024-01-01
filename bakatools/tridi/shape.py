from itertools import product
from typing import Generator

from .directions import directions
from .vector import Vector3D


class Shape3D(set[Vector3D]):
    def get_bounding_box(self) -> tuple[Vector3D, Vector3D]:
        return (
            Vector3D(
                min(e.x for e in self),
                min(e.y for e in self),
                min(e.z for e in self)
            ),
            Vector3D(
                max(e.x for e in self),
                max(e.y for e in self),
                max(e.z for e in self)
            ),
        )

    def get_x_span(self):
        return max(e.x for e in self) - min(e.x for e in self) + 1

    def get_y_span(self):
        return max(e.y for e in self) - min(e.y for e in self) + 1


    def get_z_span(self):
        return max(e.z for e in self) - min(e.z for e in self) + 1

    def intersects_with(self, other: "Shape3D") -> bool:
        if len(other) < len(self):
            return any(o in self for o in other)
        return any(o in other for o in self)

    def get_surface_area(self) -> int:
        return sum(0 if e.add(d) in self else 1 for e, d in product(self, directions))

    def subtract_in_place(self, other: "Shape3D"):
        self.difference_update(other)

    def iterate_joined_elements(self, start: Vector3D) -> Generator[Vector3D, None, None]:
        seen_elements = set()
        elements_to_explore = {start}
        while len(elements_to_explore) > 0:
            element = elements_to_explore.pop()
            if element not in self or element in seen_elements:
                continue
            seen_elements.add(element)
            yield element
            elements_to_explore.update(element.add(d) for d in directions)

    @staticmethod
    def cube_from_bounding_boxes(start: Vector3D, end: Vector3D) -> "Shape3D":
        res = set()

        for x in range(start.x, end.x + 1):
            for y in range(start.y, end.y + 1):
                res.update(Vector3D(x, y, z) for z in range(start.z, end.z + 1))

        return Shape3D(res)
