from .vector import Vector2D

direction_to_chrs: dict[Vector2D, str] = {
    Vector2D(0, -1): "UN^",
    Vector2D(1, 0): "RE>",
    Vector2D(0, 1): "DSVv",
    Vector2D(-1, 0): "LW<",
}

chr_to_direction: dict[str, Vector2D] = {
    c: direction for direction, cs in direction_to_chrs.items() for c in cs
}

direction_vectors: list[Vector2D] = list(direction_to_chrs.keys())
