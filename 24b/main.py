"""
f  z.. != PREV_XOR_XOR: self.values=[('4', 'z44')], self.wire='z45'
f  z.. != PREV_XOR_XOR: self.values=[('2', 'z11')], self.wire='qhj'
f  len(self.values) != 1: self.values=[], self.wire='crn'
f  z.. != PREV_XOR_XOR: self.values=[('4', 'z06')], self.wire='z06'
f  len(self.values) != 1: self.values=[], self.wire='cfp'
f  z.. != PREV_XOR_XOR: self.values=[('2', 'z35')], self.wire='hqk'
f  z.. != PREV_XOR_XOR: self.values=[('3', 'z11')], self.wire='z11'
f  z.. != PREV_XOR_XOR: self.values=[('0', 'z00')], self.wire='z00'
f  z.. != PREV_XOR_XOR: self.values=[('2', 'z06')], self.wire='fhc'
f  len(self.values) != 1: self.values=[], self.wire='pdp'
f  len(self.values) != 1: self.values=[], self.wire='mbg'
f  len(self.values) != 1: self.values=[], self.wire='z23'
f  z.. != PREV_XOR_XOR: self.values=[('1', 'z35')], self.wire='z35'
13 ['z45', 'qhj', 'crn', 'z06', 'cfp', 'hqk', 'z11', 'z00', 'fhc', 'pdp', 'mbg', 'z23', 'z35']
"""


import random
from typing import Any, Self, Union


DEBUG = True
DEBUG_PRINT_CHECK_FALSE = True
DEBUG_PRINT_CHECK_TRUE = True
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

    def ins(self) -> tuple[ComputeVertice, ComputeVertice]:
        return (self.in0, self.in1)

    def __repr__(self) -> str:
        return f"CE({self.in0} {self.operation} {self.in1} = {self.out})"


class EdgeLocationException(Exception):
    pass

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

    def locate_edge(self, ins: Union[str, tuple[str, str], tuple[ComputeVertice, ComputeVertice]], operation: str) -> ComputeEdge:
        main_in = ""
        secondary_in = ""
        if isinstance(ins, tuple):
            if isinstance(ins[0], ComputeVertice):
                main_in, secondary_in = ins[0].name, ins[1].name
            else:
                main_in, secondary_in = ins
        else:
            main_in, secondary_in = ins, None
        if main_in not in self.output:
            raise EdgeLocationException()
        result = []
        for edge in self.output[main_in]:
            if edge.operation == operation and (secondary_in is None or edge.in0.name == secondary_in or edge.in1.name == secondary_in):
                result.append(edge)
        if len(result) != 1:
            raise EdgeLocationException()
        return result[0]


class WireTypeData:
    BASE_XOR = "0"
    BASE_AND = "1"
    PREV_XOR_XOR = "2"
    PREV_XOR_AND = "3"
    NEXT_OR = "4"

    #    [NEXT_OR]\
    #              X PREV_XOR_XOR-z
    #              X PREV_XOR_AND-NEXT_OR
    #  x-BASE_XOR /              /
    #   X                       /
    #  y-BASE_AND--------------/

    def __init__(self, edge: ComputeEdge):
        self.values = []
        self.edge = edge

    def set(self, kind: str, z_vert_name: str):
        self.values.append((kind, z_vert_name))

    def check(self, wtds: dict[str, Self], graph: ComputeGraph) -> tuple[bool, str]:
        # TODO may be a problem if locate_edge can return several, then we may incorrectly assign all system
        if self.edge is None or self.edge.out.name.startswith(("x", "y")):
            #return [], "t  x/y"
            return True, "t  x/y" # TODO
        if len(self.values) != 1:
            #return [self.edge.in0, self.edge.in1, self.edge.out], f"f  len(self.values) != 1: {self}"
            return False, f"f  len(self.values) != 1: {self}"
        kind, z_vert_name = self.values[0]
        z_index = int(z_vert_name[1:])
        # prev xor xor must have out=z, and vice versa
        if self.edge.out.name.startswith("z") != (kind == WireTypeData.PREV_XOR_XOR):
            return False, f"f  z.. != PREV_XOR_XOR: {self}"
        if self.edge.out.name.startswith("z") and self.edge.out.name[1:] != z_vert_name[1:]:
            return False, f"f  z.. is for a wrong (x, y): {self}"
        # base xor and and are always correct
        if kind == WireTypeData.BASE_XOR or kind == WireTypeData.BASE_AND:
            return True, f"t  BASE_XOR or BASE_AND: {self}"
        # prev xor xor, prev xor and must have other input as previous NEXT_OR
        if kind == WireTypeData.PREV_XOR_XOR or kind == WireTypeData.PREV_XOR_AND:
            wires = self.edge.ins()
            if len(wtds[wires[0].name].values) != 1 or len(wtds[wires[1].name].values) != 1:
                return False, f"f  PREV_XOR_XOR or PREV_XOR_AND (one of inputs has wrong length): {wires=}, {self}"
            inputs_values = [wtds[wires[i].name].values[0] for i in range(2)]
            inputs_values.sort()
            if inputs_values[0][0] != WireTypeData.BASE_XOR or inputs_values[1][0] != WireTypeData.NEXT_OR or \
                    int(inputs_values[0][1][1:]) != z_index or z_index - 1 != int(inputs_values[1][1][1:]):
                return False, f"f  PREV_XOR_XOR or PREV_XOR_AND (one of inputs is of wrong type): (kind0,z0),(kind1,z1)={inputs_values}, {self}"
            return True, f"f  PREV_XOR_XOR or PREV_XOR_AND: {self}"
        # next or must be an input to next PREV_XOR_XOR and PREV_XOR_AND
        if kind == WireTypeData.NEXT_OR:
            outputs = graph.output[self.edge.out.name]
            if len(outputs) != 2:
                return False, f"f  NEXT_OR wrong amount of output edges: {outputs=} {self}"
            wires = [e.out for e in outputs]
            if len(wtds[wires[0].name].values) != 1 or len(wtds[wires[1].name].values) != 1:
                return False, f"f  NEXT_OR (one of inputs has wrong length): {wires=}, {self}"
            inputs_values = [wtds[wires[i].name].values[0] for i in range(2)]
            inputs_values.sort()
            if inputs_values[0][0] != WireTypeData.PREV_XOR_XOR or inputs_values[1][0] != WireTypeData.PREV_XOR_AND or \
                    int(inputs_values[0][1][1:]) != z_index + 1 or z_index + 1 != int(inputs_values[1][1][1:]):
                return False, f"f  NEXT_OR (one of outputs is of wrong type): (kind0,z0),(kind1,z1)={inputs_values}, {self}"
            return True, f"f  NEXT_OR: {self}"
        raise Exception(f"wtf unknown kind: {self}")

    def __repr__(self) -> str:
        return f"{self.values=}, {self.edge=}"


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
        wire_to_type_data: dict[str, WireTypeData] = dict()
        for v in graph.vertices:
            wire_to_type_data[v] = WireTypeData(graph.input.get(v, None))
        for z_vert_name in sorted([v for v in graph.vertices if v.startswith("z")]):
            x_vert_name, y_vert_name = "x"+z_vert_name[1:], "y"+z_vert_name[1:]
            # find edges to wires: base_xor, base_and, prev_xor_xor, prev_xor_and, next_or
            try:
                base_xor_edge = graph.locate_edge((x_vert_name, y_vert_name), "XOR")
                wire_to_type_data[base_xor_edge.out.name].set(kind=WireTypeData.BASE_XOR, z_vert_name=z_vert_name)

                base_and_edge = graph.locate_edge((x_vert_name, y_vert_name), "AND")
                wire_to_type_data[base_and_edge.out.name].set(kind=WireTypeData.BASE_AND, z_vert_name=z_vert_name)

                prev_xor_xor_edge = graph.locate_edge(base_xor_edge.out.name, "XOR")
                wire_to_type_data[prev_xor_xor_edge.out.name].set(kind=WireTypeData.PREV_XOR_XOR, z_vert_name=z_vert_name)  # note that output is z_vert_name, other input is previous NEXT_OR

                prev_xor_and_edge = graph.locate_edge(prev_xor_xor_edge.ins(), "AND")
                wire_to_type_data[prev_xor_and_edge.out.name].set(kind=WireTypeData.PREV_XOR_AND, z_vert_name=z_vert_name)  # note that other input is previous NEXT_OR

                next_or_edge = graph.locate_edge((base_and_edge.out.name, prev_xor_and_edge.out.name), "OR")
                wire_to_type_data[next_or_edge.out.name].set(kind=WireTypeData.NEXT_OR, z_vert_name=z_vert_name)
            except EdgeLocationException:
                if DEBUG:
                    print("Error while locating edge according to structure in", z_vert_name)
                continue
        bad_wires_wtd = []
        for wire, wtd in wire_to_type_data.items():
            result, message = wtd.check(wire_to_type_data, graph)
            if DEBUG:
                if result and DEBUG_PRINT_CHECK_TRUE or not result and DEBUG_PRINT_CHECK_FALSE:
                    print(wire, message)
            if not result:
                bad_wires_wtd.append(wire)
        # throw out wires which have another bad as input
        bad_wires = bad_wires_wtd
        ## TODO ?
        #bad_wires_wtd_set = set(bad_wires_wtd)
        #bad_wires = []
        #for wire in bad_wires_wtd_set:
        #    ins = graph.input[wire].ins()
        #    if ins[0].name in bad_wires_wtd_set or ins[1].name in bad_wires_wtd_set:
        #        continue
        #    bad_wires.append(wire)
        # output
        bad_wires.sort()
        if DEBUG:
            print(len(bad_wires))
        result = ",".join(bad_wires)
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

