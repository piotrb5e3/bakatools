from typing import TypeVar, Optional

from bakatools.graph.dag import DirectedGraph

T = TypeVar('T')


def longest_path(start: T, end: T, graph: DirectedGraph[T]) -> int:
    def lp(current: T, seen: set[T]) -> Optional[int]:
        if current == end:
            return 0

        res = None
        new_seen = set(seen)
        new_seen.add(current)
        for nxt in graph[current].keys():
            if nxt not in seen:
                r = lp(nxt, new_seen)
                if r is None:
                    continue
                r += graph[current][nxt]
                if res is None:
                    res = r
                else:
                    res = max(res, r)
        return res

    return lp(start, set())
