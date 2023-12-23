from collections import defaultdict
from typing import TypeVar

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
