from collections import defaultdict
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


def floyd_warshall(graph: DirectedGraph[T]) -> dict[T, dict[T, int | None]]:
    """Implements the floyd-warshall algorithm for finding the shortest paths in a graph between any pair of nodes"""
    result: dict[T, dict[T, int | None]] = defaultdict(
        lambda: defaultdict(lambda: None)
    )
    for node, node_values in graph.items():
        result[node][node] = 0
        for dest_node, weight in node_values.items():
            result[node][dest_node] = weight

    for intermediate_node in graph.keys():
        for start_node in graph.keys():
            for end_node in graph.keys():
                old = result[start_node][end_node]
                p1 = result[start_node][intermediate_node]
                p2 = result[intermediate_node][end_node]
                if p1 is not None and p2 is not None:
                    if old is None:
                        result[start_node][end_node] = p1 + p2
                    else:
                        result[start_node][end_node] = min(
                            result[start_node][end_node], p1 + p2
                        )
    return result
