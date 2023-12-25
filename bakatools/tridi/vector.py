from typing import NamedTuple

from bakatools.tudi.vector import Vector2D


class Vector3D(NamedTuple):
    x: int
    y: int
    z: int

    def add(self, other: "Vector3D") -> "Vector3D":
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def mul(self, by: int) -> "Vector3D":
        return Vector3D(self.x * by, self.y * by, self.z * by)

    def drop_z(self) -> Vector2D:
        return Vector2D(self.x, self.y)

    @staticmethod
    def from_str(s: str, sep: str = ",") -> "Vector3D":
        segments = s.split(sep)
        assert (
            len(segments) == 3
        ), f"There must be exactly 3 segments. Found: {len(segments)}"
        xs, ys, zs = segments
        return Vector3D(int(xs.strip()), int(ys.strip()), int(zs.strip()))
