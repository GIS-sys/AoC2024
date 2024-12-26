from tqdm import tqdm


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
        triples: set[tuple[str, str, str]] = set()
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
        # start merging cliques until we have nothing
        cliques: set[tuple] = triples.copy()
        while True:
            print(len(cliques), len(element_from_set(cliques)))
            new_cliques: set[tuple] = set()
            for c1 in tqdm(cliques):
                for new_element in edges.keys():
                    if new_element in c1:
                        continue
                    if DEBUG:
                        print(c1, new_element)
                    found_unconnected = False
                    for element_from_c1 in c1:
                        if new_element not in edges[element_from_c1]:
                            found_unconnected = True
                            break
                    if found_unconnected:
                        continue
                    new_cliques.add(tuple(sorted(list(c1) + [new_element])))
            if len(new_cliques) == 0:
                break
            cliques = new_cliques
        # format result
        max_clique = element_from_set(cliques)
        result = ",".join(sorted(list(max_clique)))
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

