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

    def get_wires_reaching_only(self, bad_wires: list[str]) -> list[str]:
        wire_results: dicts[str, bool] = dict()
        for v in self.vertices.values():
            stack = [(v, 0)]
            stack_value = None
            while stack:
                v, index = stack[-1]
                stack.pop()
                # print(v, index, wire_results, stack, stack_value)
                if index != 0:
                    wire_results[v.name] = wire_results.get(v.name, True) & stack_value
                if wire_results.get(v.name, None) is not None:
                    stack_value = wire_results[v.name]
                    continue
                if v.name not in self.output:
                    wire_results[v.name] = (v.name in bad_wires)
                    stack_value = wire_results[v.name]
                    # print("get_wires_reaching_only fin", v.name)
                    continue
                if index >= len(self.output[v.name]):
                    stack_value = wire_results[v.name]
                    # print("get_wires_reaching_only reg", v.name)
                    continue
                stack.append((v, index + 1))
                stack.append((self.output[v.name][index].out, 0))
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
        # trace them to find all gates where only those who use only these bits
        foo_format = lambda x: "z" + ("00" + str(x))[-2:]
        potentially_bad_wires = graph.get_wires_reaching_only([foo_format(b) for b in bad_bits])
        if DEBUG:
            print("potentially bad wires:")
            print(len(potentially_bad_wires), potentially_bad_wires)
        potentially_bad_edges = set(graph.input.get(wire, None) for wire in potentially_bad_wires) - set([None])
        if DEBUG:
            print("potentially bad edges:")
            print(len(potentially_bad_edges), potentially_bad_edges)
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

