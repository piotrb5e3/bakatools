from .vector import Vector3D

chr_to_directions = {
    "N": Vector3D(0, -1, 0),
    "S": Vector3D(0, 1, 0),
    "E": Vector3D(1, 0, 0),
    "W": Vector3D(-1, 0, 0),
    "U": Vector3D(0, 0, 1),
    "D": Vector3D(0, 0, -1),
}

directions = list(chr_to_directions.values())