DEBUG = False
LOG_TABLE = {
    2**k : k for k in range(0, 1000)
}


def dec_to_bin(x: int) -> list[int]:
    result = []
    while x:
        r, x = x % 2, x // 2
        result.append(r)
    return result[::-1]


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
        # find all nodes
        nodes: set[str] = set()
        for a, b in self.connections:
            nodes.add(a)
            nodes.add(b)
        # rename nodes
        node_to_id: dict[str, int] = dict()
        id_to_node: dict[int, str] = dict()
        for index, node in enumerate(nodes):
            node_to_id[node] = index
            id_to_node[index] = node
        if DEBUG:
            print(f"{node_to_id=}")
        # construct graph
        edges: dict[int, set[int]] = dict()
        for a, b in self.connections:
            a, b = node_to_id[a], node_to_id[b]
            if not a in edges:
                edges[a] = set()
            if not b in edges:
                edges[b] = set()
            edges[a].add(b)
            edges[b].add(a)
        if DEBUG:
            print(f"{edges=}")
        # find cliques
        dp: dict[int, bool] = dict()
        largest_clique: int = 0
        largest_clique_size: int = 0
        for mask in range(1, 2**(len(set(edges.keys())) + 1)):
            if mask in LOG_TABLE.keys():
                print(LOG_TABLE[mask], len(set(edges.keys())) + 1)
            # find one bit in number and calculate mask without one of the bits
            one_bit = mask & (mask ^ (mask - 1))
            smaller_mask = mask ^ one_bit
            # base for dp
            if smaller_mask == 0:
                dp[mask] = True
                continue
            # if smaller mask is not a clique - immediately false
            if not dp[smaller_mask]:
                dp[mask] = False
                continue
            # check if all other bits are connected to selected one
            if DEBUG:
                print(f"{mask=} ({dec_to_bin(mask)})   {one_bit=} (2**{LOG_TABLE[one_bit]})   {smaller_mask=}")
                # print(dp)
            bin_mask = mask
            bit_index = 0
            amount = 0
            found_unconnected = False
            while bin_mask > 0:
                bit, bin_mask = bin_mask % 2, bin_mask // 2
                if bit:
                    amount += 1
                if bit and bit_index != LOG_TABLE[one_bit]:
                    if DEBUG:
                        print(f"checking {bit_index=} in edges[one_bit]={edges[LOG_TABLE[one_bit]]}  -  {bit_index in edges[LOG_TABLE[one_bit]]}")
                    if bit_index not in edges[LOG_TABLE[one_bit]]:
                        dp[mask] = False
                        found_unconnected = True
                        break
                bit_index += 1
            if found_unconnected:
                continue
            dp[mask] = True
            if largest_clique_size < amount:
                largest_clique = mask
                largest_clique_size = amount
        # format result
        if DEBUG:
            print(f"{largest_clique=} ({dec_to_bin(largest_clique)}) {largest_clique_size=}")
        result = []
        for bit_index, bit in enumerate(dec_to_bin(largest_clique)[::-1]):
            if bit:
                result.append(id_to_node[bit_index])
        result.sort()
        return ",".join(result)


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

