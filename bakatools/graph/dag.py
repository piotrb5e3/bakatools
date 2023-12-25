import re
from collections import defaultdict
from typing import TypeVar

from networkx import DiGraph

T = TypeVar("T")


class DirectedGraph(dict[T, dict[T, int]]):
    def simplify_in_place(self):
        inputs: dict[T, set[T]] = defaultdict(lambda: set())
        for k, v in self.items():
            for v_to in v.keys():
                inputs[v_to].add(k)

        for k in list(self.keys()):
            if len(self[k]) == 2 and set(self[k].keys()) == inputs[k]:
                n1, n2 = self[k].keys()
                if k in self[n1] and k in self[n2]:
                    self[n1][n2] = self[n1][k] + self[k][n2]
                    inputs[n1].add(n2)
                    self[n1].pop(k)
                    inputs[n1].remove(k)
                    self[n2][n1] = self[n2][k] + self[k][n1]
                    inputs[n2].add(n1)
                    self[n2].pop(k)
                    inputs[n2].remove(k)
                    self.pop(k)

    def merge_vertices(self, s: T, t: T) -> "DirectedGraph[T]":
        result = DirectedGraph[T](self)
        result[s].update(result[t])
        result.pop(t)
        for v in result.values():
            if t in v:
                v[s] = v[t]
                v.pop(t)

        return result

    def to_nx_graph(self) -> DiGraph:
        res = DiGraph()
        res.add_edges_from([(a, b) for a, bs in self.items() for b in bs.keys()])
        return res

    @staticmethod
    def from_lines(
        lines: list[str], separators=r"[\s]+", two_way=False
    ) -> "DirectedGraph[str]":
        """
        Parse graphs described where this:
        N1 N2 N3 N4
        means that there are vertices from N1 to N2, N3 and N4
        """
        result = defaultdict(lambda: dict())

        for line in lines:
            nodes = re.split(separators, line)
            from_node = nodes[0]
            to_nodes = nodes[1:]
            for tn in to_nodes:
                result[from_node][tn] = 1
                if two_way:
                    result[tn][from_node] = 1

        return DirectedGraph[str](result)
