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
        result = 0
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

