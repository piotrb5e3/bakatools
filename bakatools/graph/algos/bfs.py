from queue import SimpleQueue
from typing import Generator, TypeVar

from bakatools.graph.dag import DirectedGraph

T = TypeVar('T')


def bfs_iterate(graph: DirectedGraph, start: T) -> Generator[(int, T), None, None]:
    seen: set[T] = set()
    q = SimpleQueue()

    q.put((0, start))

    while not q.empty():
        dist, node = q.get()
        if node in seen:
            continue

        yield dist, node

        for n_node, n_dist in graph[node].items():
            q.put(dist + n_dist, n_node)
