from dataclasses import dataclass
from typing import Optional, Generator


@dataclass
class Dir:
    path: list[str]
    parent: Optional["Dir"]
    dirs: dict[str, "Dir"]
    files: dict[str, "File"]

    def __init__(self, path: list[str], parent: Optional["Dir"] = None):
        self.path = path
        self.parent = parent
        self.dirs = dict()
        self.files = dict()

    @property
    def name(self):
        return self.path[-1]

    def size(self) -> int:
        return sum(f.size for f in self.files.values()) + sum(d.size() for d in self.dirs.values())

    def iter_dirs(self) -> Generator["Dir", None, None]:
        yield self

        for d in self.dirs.values():
            yield from d.iter_dirs()


@dataclass
class File:
    path: list[str]
    size: int

    @property
    def name(self):
        return self.path[-1]
