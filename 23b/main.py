DEBUG = False


def element_from_set(s: set):
    if not s:
        return None
    for x in s:
        return x


class Solver:
    def __init__(self):
        self.connections: list[tuple[str, str]] = None

    def read(self):
        self.connections = []
        while i := input():
            self.connections.append(i.split("-"))

    def find_largest_clique(self, computers: set[str]) -> set[str]:
        if DEBUG:
            print(computers)
        if len(computers) == 0:
            return set()
        largest_clique = set([element_from_set(computers)])
        for pc1 in computers:
            for pc2 in self.edges[pc1] & computers:
                pc3s = self.edges[pc1] & self.edges[pc2] & computers
                possible_largest_clique = set([pc1, pc2])
                if len(computers) == len(self.edges):
                    print(possible_largest_clique, pc3s)
                possible_largest_clique |= self.find_largest_clique(pc3s)
                if len(possible_largest_clique) > len(largest_clique):
                    largest_clique = possible_largest_clique
        return largest_clique

    def solve(self):
        # construct graph
        self.edges: dict[str, set[str]] = dict()
        for a, b in self.connections:
            if not a in self.edges:
                self.edges[a] = set()
            if not b in self.edges:
                self.edges[b] = set()
            self.edges[a].add(b)
            self.edges[b].add(a)
        # find triples
        result = self.find_largest_clique(self.edges.keys())
        result = list(result)
        result.sort()
        return ",".join(result)


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

