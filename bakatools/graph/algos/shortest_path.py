from queue import PriorityQueue
from typing import TypeVar

from bakatools.graph.dag import DirectedGraph

T = TypeVar("T")


def shortest_paths(graph: DirectedGraph[T], start: T) -> dict[T, int]:
    """Uses the Dijkstra algorithm to find the shortest path from node to all other nodes"""
    shortest_paths_dict: dict[T, int] = {}
    pq = PriorityQueue()
    pq.put((0, start))

    while not pq.empty():
        distance, node = pq.get()

        if node not in shortest_paths_dict or distance < shortest_paths_dict[node]:
            shortest_paths_dict[node] = distance
            for next_node, next_dist in graph[node].items():
                pq.put((distance + next_dist, next_node))

    return shortest_paths_dict
