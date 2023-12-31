from bakatools.ranges.closed_range import ClosedRange


class DisjointRange(list[ClosedRange]):
    def add(self, r: ClosedRange):
        for er in list(self):
            if er.intersects(r):
                self.remove(er)
                self.add(ClosedRange(min(r.start, er.start), max(r.end, er.end)))
                return
        self.append(r)
        self._fix_order()

    def subtract(self, r: ClosedRange):
        for er in list(self):
            if er.intersects(r):
                self.remove(er)
                if er.start < r.start:
                    self.append(ClosedRange(er.start, r.start - 1))
                    self._fix_order()
                if er.end > r.end:
                    self.append(ClosedRange(r.end + 1, er.end))
                    self._fix_order()

    def _fix_order(self):
        self.sort(key=lambda x: x.start)

    @property
    def total_length(self) -> int:
        return sum(r.total_length for r in self)

    def invert_over_intersection(self, other: ClosedRange) -> "DisjointRange":
        result = DisjointRange([other])
        for section in self:
            result.subtract(section)

        return result
