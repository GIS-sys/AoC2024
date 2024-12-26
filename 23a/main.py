DEBUG = False


class Solver:
    def __init__(self):
        self.connections: list[tuple[str, str]] = None

    def read(self):
        self.connections = []
        while i := input():
            self.connections.append(i.split("-"))

    def solve(self):
        # construct graph
        edges: dict[str, set[str]] = dict()
        for a, b in self.connections:
            if not a in edges:
                edges[a] = set()
            if not b in edges:
                edges[b] = set()
            edges[a].add(b)
            edges[b].add(a)
        # find triples
        triples: set[str] = set()
        for pc1 in edges.keys():
            for pc2 in edges[pc1]:
                pc3s = edges[pc1] & edges[pc2]
                for pc3 in pc3s:
                    pcs = [pc1, pc2, pc3]
                    pcs.sort()
                    triples.add(tuple(pcs))
                if DEBUG:
                    for pc3 in pc3s:
                        print(pc1, pc2, pc3)
        # count only triples with at least one computer with a T in it
        result = 0
        for t in triples:
            if t[0].startswith("t") or t[1].startswith("t") or t[2].startswith("t"):
                result += 1
                if DEBUG:
                    print(t)
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

