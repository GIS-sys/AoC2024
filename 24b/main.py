import random


DEBUG = True
BAD_ATLEAST = 10000
GOOD_ATLEAST = 1


def dec_to_bin(x: int, length: int = None) -> list[int]:
    result = []
    while x:
        r, x = x % 2, x // 2
        result.append(r)
    if length:
        result = result + [0] * (length - len(result))
    return result


class ComputeVertice:
    def __init__(self, name: str):
        self.name = name
        self.value = None

    def __repr__(self) -> str:
        return f"({self.name})"


class ComputeEdge:
    def __init__(self, in0: ComputeVertice, in1: ComputeVertice, out: ComputeVertice, operation: str):
        self.in0 = in0
        self.in1 = in1
        self.out = out
        self.operation = operation

    def calculate(self) -> int:
        if self.operation == "OR":
            return self.in0.value | self.in1.value
        if self.operation == "AND":
            return self.in0.value & self.in1.value
        if self.operation == "XOR":
            return self.in0.value ^ self.in1.value

    def __repr__(self) -> str:
        return f"CE({self.in0} {self.operation} {self.in1} = {self.out})"


class ComputeGraph:
    def __init__(self, edges: list[tuple[str, str, str, str]]):
        self.all_values: list[tuple[str, int]] = []
        self.vertices: dict[str, ComputeVertice] = {}
        self.output: dict[str, list[ComputeEdge]] = {}
        self.input: dict[str, ComputeEdge] = {}
        # add all vertices
        for input1, input2, output, operation in edges:
            self.vertices[input1] = ComputeVertice(input1)
            self.vertices[input2] = ComputeVertice(input2)
            self.vertices[output] = ComputeVertice(output)
        # add edges
        for input1, input2, output, operation in edges:
            edge = ComputeEdge(self.vertices[input1], self.vertices[input2], self.vertices[output], operation)
            self.output[input1] = self.output.get(input1, []) + [edge]
            self.output[input2] = self.output.get(input2, []) + [edge]
            self.input[output] = edge

    def push(self, name: str, value: int):
        self.vertices[name].value = value
        for edge in self.output.get(name, []):
            if edge.in0.value is not None and edge.in1.value is not None:
                self.push(edge.out.name, edge.calculate())

    def run(self, initial_values: list[tuple[str, int]]) -> list[tuple[str, int]]:
        for v in self.vertices.values():
            v.value = None
        for name, value in initial_values:
            self.push(name, value)
        self.all_values = [(v.name, v.value) for v in self.vertices.values()]
        self.all_values.sort()
        return self.all_values

    def run_get_number(self, initial_values: list[tuple[str, int]]) -> int:
        self.run(initial_values)
        z_values = self.get_sorted_starting_with("z")
        result = 0
        for i, v in enumerate(z_values):
            result += v * 2**i
        return result

    def iterate_over_tree(self, return_callback, raw_callback, allow_bfs_from_start_callback):
        wire_results = dict()
        for starting_v in self.vertices.values():
            if not allow_bfs_from_start_callback(starting_v):
                continue
            stack = [(starting_v, 0)]
            stack_value = None
            while stack:
                v, index = stack[-1]
                stack.pop()
                # print(v, index, stack_value, self.output.get(v.name, None))
                if index != 0:
                    wire_results[v.name] = return_callback(v, wire_results, starting_v, stack_value)
                elif wire_results.get(v.name, None) is not None:
                    stack_value = wire_results[v.name]
                    continue
                if v.name not in self.output:
                    wire_results[v.name] = raw_callback(v, wire_results, starting_v)
                    stack_value = wire_results[v.name]
                    continue
                if index >= len(self.output[v.name]):
                    stack_value = wire_results[v.name]
                    continue
                stack.append((v, index + 1))
                stack.append((self.output[v.name][index].out, 0))
        return wire_results

    def get_wires_reaching_only(self, bad_wires: list[str]) -> list[str]:
        wire_results = self.iterate_over_tree(
            lambda v, wire_results, starting_v, stack_value: wire_results.get(v.name, True) & stack_value,
            lambda v, wire_results, starting_v: v.name in bad_wires,
            lambda starting_v: starting_v.name.startswith(("x", "y"))
        )
        return [wire for wire in wire_results if wire_results[wire]]

    def get_wires_influencing_wires(self, wires: list[str]) -> list[str]:
        wire_results = self.iterate_over_tree(
            lambda v, wire_results, starting_v, stack_value: wire_results.get(v.name, False) | stack_value,
            lambda v, wire_results, starting_v: v.name in wires,
            lambda starting_v: starting_v.name.startswith(("x", "y"))
        )
        # print(wires, wire_results, "\n\n")
        return [wire for wire in wire_results if wire_results[wire]]

    def get_wires_connecting_xyz_same_index(self, wires: list[str]) -> list[str]:
        wire_results = self.iterate_over_tree(
            lambda v, wire_results, starting_v, stack_value: wire_results.get(v.name, False) | stack_value,
            lambda v, wire_results, starting_v: starting_v.name in wires and v.name.startswith("z") and int(v.name[1:]) == int(starting_v.name[1:]), # < instead of == doesnt help
            lambda starting_v: starting_v.name in wires,
        )
        # print(wires, wire_results, "\n\n")
        return [wire for wire in wire_results if wire_results[wire]]

    def get_sorted_starting_with(self, symbol: str) -> list[int]:
        if not self.all_values:
            return []
        return [v[1] for v in self.all_values if v[0].startswith(symbol)]


class Solver:
    def __init__(self):
        self.initial_values: list[tuple[str, int]] = None
        self.edges: list[tuple[str, str, str, str]] = None
        self.numbers_length: int = None

    def read(self):
        self.numbers_length = 0
        self.initial_values = []
        self.edges = []
        while i := input():
            name, value = i.split(": ")
            value = int(value)
            self.initial_values.append((name, value))
            if name.startswith("x"):
                self.numbers_length += 1
        while i := input():
            input1, operation, input2, _, output = i.split(" ")
            self.edges.append((input1, input2, output, operation))

    def generate_random_test(self) -> list[tuple[str, int]]:
        initial_values = []
        answer = 0
        for i in range(self.numbers_length):
            i_format = f"0{i}"[-2:]
            initial_values.append((f"x{i_format}", int(random.random() * 2)))
            initial_values.append((f"y{i_format}", int(random.random() * 2)))
            answer += (initial_values[-2][1] + initial_values[-1][1]) * 2**i
        return initial_values, answer

    def solve(self):
        graph = ComputeGraph(self.edges)
        # generate bad and good arithmetic examples
        bad_runs = []
        good_runs = []
        while len(bad_runs) < BAD_ATLEAST or len(good_runs) < GOOD_ATLEAST:
            random_initial_values, random_answer = self.generate_random_test()
            result = graph.run_get_number(random_initial_values)

            rx, ry, rz = graph.get_sorted_starting_with("x"), graph.get_sorted_starting_with("y"), graph.get_sorted_starting_with("z")
            run_result = (random_initial_values, rx, ry, rz, dec_to_bin(random_answer, len(rz)))
            if random_answer == result:
                good_runs.append(run_result)
            else:
                bad_runs.append(run_result)
        # find out which bits are bad
        bad_bits = set()
        for run_result in bad_runs:
            for i, (bit_predicted, bit_true) in enumerate(zip(run_result[-2], run_result[-1])):
                if bit_true != bit_predicted:
                    bad_bits.add(i)
        if DEBUG:
            print("bad bit indexes:")
            print(len(bad_bits), bad_bits)

        # use differen criteria to find potentially bad wires and edges
        # 1. find only those which may influence only bad bits
        foo_format = lambda x, s="z": s + ("00" + str(x))[-2:]
        wires_only_bad_bits = graph.get_wires_reaching_only([foo_format(b) for b in bad_bits])
        if DEBUG:
            print("wires leading only to bad bits:")
            print(len(wires_only_bad_bits))
            # print(wires_only_bad_bits)
        edges_only_bad_bits = set(graph.input.get(wire, None) for wire in wires_only_bad_bits) - set([None])
        if DEBUG:
            print("edges leading only to bad bits:")
            print(len(edges_only_bad_bits))
            # print(edges_only_bad_bits)

        # 2. for every bad bit find those which can influence it
        wires_influencing_bits = []
        for bit in bad_bits:
            wires_influencing_bits.append(graph.get_wires_influencing_wires([foo_format(bit)]))
        if DEBUG:
            print("wires leading to specific bad bit:")
            print([len(x) for x in wires_influencing_bits])
            # print("\n".join([str(w) for w in wires_influencing_bits]))
        edges_influencing_bits = [set(graph.input.get(wire, None) for wire in wire_complect) - set([None]) for wire_complect in wires_influencing_bits]
        if DEBUG:
            print("edges leading to specific bad bit:")
            print([len(x) for x in edges_influencing_bits])
            # print("\n".join([str(w) for w in edges_influencing_bits]))

        # 3. find those which carry influence from x/y with bigger index to z with smaller index
        wires_same_index = []
        for bit in bad_bits:
            wires_same_index.append(graph.get_wires_connecting_xyz_same_index([foo_format(bit, "x"), foo_format(bit, "y")]))
        if DEBUG:
            print("wires connecting bigger x/y to same z:")
            print([len(x) for x in wires_same_index])
            # print("\n".join([str(w) for w in wires_same_index]))
        edges_same_index = [set(graph.input.get(wire, None) for wire in wire_complect) - set([None]) for wire_complect in wires_same_index]
        if DEBUG:
            print("edges connecting bigger x/y to same z:")
            print([len(x) for x in edges_same_index])
            print("\n".join([str(w) for w in edges_same_index]))

        # TODO
        # intersect edge influencers with edges leading only to bad bits
        edges_to_check = [a & potentially_bad_edges for a in edges_influencing_bits]
        if DEBUG:
            print("edges with both criteria:")
            print([len(x) for x in edges_to_check])

        # TODO
        #if DEBUG:
        #    print(good_runs)
        #    print(bad_runs)
        #print(bad_runs[4])
        #graph.run_get_number(bad_runs[4][0])
        #print(graph.get_sorted_starting_with("x"))
        #print(graph.get_sorted_starting_with("y"))
        #print(graph.get_sorted_starting_with("z"))
        # TODO
        # try to fix
        # backpropogate?
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

