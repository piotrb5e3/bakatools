from typing import TypeVar

from networkx.algorithms.connectivity.stoerwagner import stoer_wagner

from ..dag import DirectedGraph

T = TypeVar("T")


def min_cut(graph: DirectedGraph[T]) -> tuple[int, tuple[list[T], list[T]]]:
    return stoer_wagner(graph.to_nx_graph().to_undirected())
