from typing import TypeVar, Optional, Generator, Generic

T = TypeVar("T")


class LinkedList(Generic[T]):
    next: Optional["LinkedList[T]"] = None
    prev: Optional["LinkedList[T]"] = None
    value: T

    def __init__(self, value: T):
        self.value = value

    def _to_str(self, seen: "set[LinkedList[T]]") -> str:
        if self.next is None:
            return str(self.value)
        if self in seen:
            return f"{self.value} -> ..."
        seen.add(self)
        return f"{self.value} -> {self.next._to_str(seen)}"

    def __str__(self):
        return self._to_str(set())

    def remove_from_list(self):
        if self.prev:
            self.prev.next = self.next
        if self.next:
            self.next.prev = self.prev
        self.prev = None
        self.next = None

    def insert_after(self, target: "LinkedList[T]"):
        assert self.prev is None
        assert self.next is None

        self.next = target.next
        if self.next:
            self.next.prev = self
        self.prev = target
        target.next = self

    def insert_before(self, target: "LinkedList[T]"):
        assert self.prev is None
        assert self.next is None

        self.prev = target.prev
        if self.prev:
            self.prev.next = self
        self.next = target
        target.prev = self

    def get_nodes(self) -> Generator["LinkedList[T]", None, None]:
        seen = set()
        element = self
        while element is not None and element not in seen:
            yield element
            seen.add(element)
            element = element.next

    @staticmethod
    def from_list(l: list[T], cyclic: bool = False) -> "LinkedList[T]":
        assert len(l) > 0

        start = LinkedList(l[0])
        prev = start
        for e in l[1:]:
            tmp = LinkedList(e)
            tmp.prev = prev
            prev.next = tmp
            prev = tmp

        if cyclic:
            prev.next = start
            start.prev = prev

        return start
