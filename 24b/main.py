# real answer:
# fhc,ggt,hqk,mwh,qhj,z06,z11,z35

# program output:
# ['qhj', 'z06', 'ggt', 'cfp', 'z36', 'hqk', 'z11', 'fhc', 'dbr', 'pdp', 'krr', 'mwh', 'mbg', 'z24', 'z23', 'z35', 'dgv', 'z07']
# wrongly accused:
# cfp z36 dbr pdp krr mbg z23 z24 dgv z07

# program output:
# ['qhj', 'z06', 'ggt', 'z36', 'hqk', 'z11', 'fhc', 'krr', 'mwh', 'z24', 'z35', 'dgv']
# wrongly accused:
# krr, z24, z36, dgv

# program output:
# ['qhj', 'z06', 'ggt', 'hqk', 'z11', 'fhc', 'mwh', 'z35']
# wrongly accused:


DEBUG = False
if DEBUG:
    import pygame
import sys
import numbers
import math
from typing import Any
from collections.abc import Iterable


REPLACEMENTS = [
#    ("z06", "fhc"),
#    ("ggt", "mwh"),
#    ("z35", "hqk"),
#    ("z11", "qhj"),
]

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)
GREEN = (0, 127, 0)
RED = (127, 0, 0)
BLACK = (0, 0, 0)
FPS = 60
CAMERA_MOVEMENT_RATE = 150.0
CAMERA_SCALE_RATE = 1.05
CAMERA_INIT_MARGIN = 0.05


def cross_iter(*args):
    if len(args) == 1:
        for x in args[0]:
            yield (x, )
    else:
        for x in args[0]:
            for y in cross_iter(*args[1:]):
                yield x, *y


class Point:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __add__(self, oth):
        if isinstance(oth, Point):
            return Point(self.x + oth.x, self.y + oth.y)
        elif isinstance(oth, Iterable):
            return Point(self.x + oth[0], self.y + oth[1])
        raise Exception(f"{type(self)} can't add {oth} ({type(oth)})")

    def __sub__(self, oth):
        if isinstance(oth, Point):
            return self + (-oth)
        elif isinstance(oth, Iterable):
            return self + (-oth[0], -oth[1])
        raise Exception(f"{type(self)} can't sub {oth} ({type(oth)})")

    def __mul__(self, oth):
        if isinstance(oth, Point):
            return Point(self.x * oth.x, self.y * oth.y)
        elif isinstance(oth, Iterable):
            return Point(self.x * oth[0], self.y * oth[1])
        elif isinstance(oth, numbers.Number):
            return Point(self.x * oth, self.y * oth)
        raise Exception(f"{type(self)} can't mul {oth} ({type(oth)})")

    def __truediv__(self, oth):
        if isinstance(oth, Point):
            return self * Point(1 / oth.x, 1 / oth.y)
        elif isinstance(oth, Iterable):
            return self * Point(1 / oth[0], 1 / oth[1])
        elif isinstance(oth, numbers.Number):
            return self * (1 / oth)
        raise Exception(f"{type(self)} can't div {oth} ({type(oth)})")

    def to_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def copy(self):
        return Point(self.x, self.y)

    def __eq__(self, oth):
        if isinstance(oth, Point):
            return self.x == oth.x and self.y == oth.y
        elif isinstance(oth, Iterable):
            return self.x == oth[0] and self.y == oth[1]
        raise Exception(f"{type(self)} can't eq {oth} ({type(oth)})")

    def __ne__(self, oth):
        return not (self == oth)


def norm(p1: Point, p2: Point) -> float:
    return (p1.x - p2.x)**2 + (p1.y - p2.y)**2


class Circle:
    def __init__(self, name: str, position: Point, radius: float, bg_color: tuple[int, int, int] = BLACK, fg_color: tuple[int, int, int] = GRAY, font_size: int = 24):
        self.name: str = name
        self.position: Point = position
        self.radius: float = radius
        self.bg_color: tuple[int, int, int] = bg_color
        self.fg_color: tuple[int, int, int] = fg_color
        self.font_size: int = font_size

    def draw(self, surface: Any, camera_offset: Point, scale: float):
        scaled_radius = int(self.radius * scale)
        scaled_position = (self.position - camera_offset) * scale
        pygame.draw.circle(surface, self.bg_color, scaled_position.to_tuple(), scaled_radius)
        font = pygame.font.SysFont(None, self.font_size)
        text = font.render(self.name, True, self.fg_color)
        surface.blit(text, (scaled_position - (text.get_width() // 2, text.get_height() // 2)).to_tuple())


class Segment:
    def __init__(self, circle1: Circle, circle2: Circle, color: tuple[int, int, int] = BLACK, width: int = 1):
        self.circle1: Circle = circle1
        self.circle2: Circle = circle2
        self.color: tuple[int, int, int] = color
        self.width = width

    def draw(self, surface: Any, camera_offset: Point, scale: float):
        pos1 = (self.circle1.position - camera_offset) * scale
        pos2 = (self.circle2.position - camera_offset) * scale
        pygame.draw.line(surface, self.color, pos1.to_tuple(), pos2.to_tuple(), self.width)


class Node:
    def __init__(self, name: str, prefix: str = ""):
        self.name = name
        self.prefix = prefix
        self.height: int = None
        self.position: Point = None
        self.kind = None
        self.is_bad = False

    def __repr__(self) -> str:
        return f"({self.prefix + self.name}, h={self.height})"


class Graph:
    CIRCLE_SIZE = 64
    MAX_POSITION_CALCULATION_ITER = 1

    def __init__(self):
        self.raw_edges: list[tuple[str, str, str, str]] = None
        self.edges: dict[str, list[str]] = {}
        self.redges: dict[str, list[str]] = {}
        self.nodes: dict[str, Node] = {}
        self.initialized_positions = False
        self.finished_calculating_position = False
        self.numbers_length: int = 0

    def read(self):
        self.raw_edges = []
        while i := input():
            pass
        while i := input():
            input1, operation, input2, _, output = i.split(" ")
            self.raw_edges.append((input1, input2, output, operation))
            if output.startswith("z"):
                self.numbers_length = max(self.numbers_length, int(output[1:]))
        self.build()

    def build(self):
        replacements: dict[str, str] = {}
        for a, b in REPLACEMENTS:
            replacements[a] = b
            replacements[b] = a
        self.edges: dict[str, list[str]] = {}
        self.redges: dict[str, list[str]] = {}
        self.nodes: dict[str, Node] = {}
        for in1, in2, out, op in self.raw_edges:
            if out in replacements:
                out = replacements[out]
            if in1 not in self.nodes:
                self.nodes[in1] = Node(in1)
            if in2 not in self.nodes:
                self.nodes[in2] = Node(in2)
            if out not in self.nodes:
                self.nodes[out] = Node(out, prefix=op)
            else:
                self.nodes[out].prefix = op
            self.edges[in1] = self.edges.get(in1, []) + [out]
            self.edges[in2] = self.edges.get(in2, []) + [out]
            self.redges[out] = self.redges.get(out, []) + [in1, in2]

    def calculate_heights(self):
        max_height = 0
        queue: list[Node] = []
        for node in self.nodes.values():
            if node.name.startswith(("x", "y")):
                node.height = 0
                queue.append(node)
        while queue:
            cur_node = queue[0]
            max_height = max(max_height, cur_node.height)
            queue.pop(0)
            for next_node_name in self.edges.get(cur_node.name, []):
                next_node = self.nodes[next_node_name]
                queue.append(next_node)
                if next_node.height is None:
                    next_node.height = cur_node.height + 1
                else:
                    next_node.height = max(cur_node.height + 1, next_node.height)
        for node in self.nodes.values():
            if node.name.startswith(("z")):
                node.height = max_height + 1

    def calculate_positions(self) -> set[Node]:
        def current_weight(self, n1: Node, n2: Node) -> float:
            weight = 0
            if n1.height >= n2.height:
            #if True:
                for next_node in self.edges.get(n1.name, []) + self.redges.get(n1.name, []):
                    weight += norm(n1.position, self.nodes[next_node].position)
            if n2.height >= n1.height:
            #if True:
                for next_node in self.edges.get(n2.name, []) + self.redges.get(n2.name, []):
                    weight += norm(n2.position, self.nodes[next_node].position)
            return weight

        def swap_all(n1: Node, n2: Node, _):
            n1.position, n2.position = n2.position, n1.position
        def swap_x(n1: Node, n2: Node, _):
            n1.position.x, n2.position.x = n2.position.x, n1.position.x
        def swap_y(n1: Node, n2: Node, _):
            n1.position.y, n2.position.y = n2.position.y, n1.position.y
        def move_down(n1: Node, _, reverse: bool):
            n1.position.y = n1.position.y + (-1 if reverse else 1) * self.CIRCLE_SIZE
        def move_up(n1: Node, _, reverse: bool):
            n1.position.y = n1.position.y + (-1 if reverse else 1) * -self.CIRCLE_SIZE

        def allow_swapping_name(n1: Node, n2: Node):
            if n1.name.startswith(("x", "y", "z")):
                return False
            if n2.name.startswith(("x", "y", "z")):
                return False
            #if n1.height != n2.height:
            #    return False
            #if n1.position.y == n2.position.y:
            #    return False
            return True
        def allow_swapping_preserve_hierarchy(n1: Node, n2: Node):
            if not allow_swapping_name(n1, n2):
                return False
            if n1.height != n2.height:
                if n1.height > n2.height:
                    n1, n2 = n2, n1
                # we need to preserve n2.pos < next_n1 and prev_n2 < n1.pos (for those where heights are <)
                for next_node_name in self.edges[n1.name]:
                    next_node = self.nodes[next_node_name]
                    if n2.position.x >= next_node.position.x and n1.height < next_node.height:
                        return False
                for next_node_name in self.redges[n2.name]:
                    next_node = self.nodes[next_node_name]
                    if next_node.position.x >= n1.position.x and next_node.height < n2.height:
                        return False
            return True
        def allow_swapping_no_near(n1: Node, n2: Node):
            if not allow_swapping_name(n1, n2):
                return False
            for next_node_name in self.nodes:
                if next_node_name == n1.name or next_node_name == n2.name:
                    continue
                next_node = self.nodes[next_node_name]
                if norm(next_node.position, n1.position) <= 2 * self.CIRCLE_SIZE**2:
                    return False
                if norm(next_node.position, n2.position) <= 2 * self.CIRCLE_SIZE**2:
                    return False
            return True

        swaps = [swap_all, swap_x, swap_y, move_up, move_down]
        #allow_swaps = [allow_swapping_preserve_hierarchy, lambda a, b: allow_swapping_preserve_hierarchy(a, b) and allow_swapping_no_near(a, b), allow_swapping_no_near, allow_swapping_no_near, allow_swapping_no_near]
        allow_swaps = [allow_swapping_preserve_hierarchy, allow_swapping_preserve_hierarchy, allow_swapping_name, allow_swapping_name, allow_swapping_name]

        changed_nodes_clean: set[Node] = set([None])
        iter = 0
        for node in self.nodes.values():
            node.old_position = node.position.copy()
        while changed_nodes_clean and iter < self.MAX_POSITION_CALCULATION_ITER:
            iter += 1
            changed = False
            changed_nodes: set[Node] = set()
            for n1, n2 in cross_iter(self.nodes.values(), self.nodes.values()):
                for swap, allow_swap in zip(swaps, allow_swaps):
                    if not allow_swap(n1, n2):
                        continue
                    # calculate weights before and after swap
                    weight_before_swap = current_weight(self, n1, n2)
                    swap(n1, n2, False)
                    weight_after_swap = current_weight(self, n1, n2)
                    swap(n1, n2, True)
                    # if needed, swap
                    if weight_before_swap > weight_after_swap:
                        swap(n1, n2, False)
                        changed = True
                        changed_nodes.add(n1)
                        changed_nodes.add(n2)
            # clean changed nodes to make sure we highlight only nodes who really changed position
            changed_nodes_clean: set[Node] = set()
            for node in changed_nodes:
                if node.old_position != node.position:
                    changed_nodes_clean.add(node)
        return changed_nodes_clean

    def find_bad_nodes(self):
        for node in self.nodes.values():
            node.kind = None
            node.is_bad = False
        # mark start and end
        for node in self.nodes.values():
            if node.name.startswith(("x", "y")):
                node.kind = "start"
            if node.name.startswith("z"):
                node.kind = "end"
        # mark base XOR and AND
        for node in self.nodes.values():
            if node.kind == "start":
                if len(self.edges[node.name]) != 2:
                    node.is_bad = True
                    continue
                for next_node_name in self.edges[node.name]:
                    next_node = self.nodes[next_node_name]
                    if node.name[1:] == "00":
                        if next_node.prefix == "AND":
                            if next_node.kind and next_node.kind != "next OR":
                                next_node.is_bad = True
                                continue
                            next_node.kind = "next OR"
                        elif next_node.prefix == "XOR":
                            if next_node.kind and next_node.kind != "end":
                                next_node.is_bad = True
                                continue
                            next_node.kind = "end"
                        else:
                            next_node.is_bad = True
                    else:
                        if next_node.prefix == "AND":
                            if next_node.kind and next_node.kind != "base AND":
                                next_node.is_bad = True
                                continue
                            next_node.kind = "base AND"
                        elif next_node.prefix == "XOR":
                            if next_node.kind and next_node.kind != "base XOR":
                                next_node.is_bad = True
                                continue
                            next_node.kind = "base XOR"
                        else:
                            next_node.is_bad = True
        # check base XOR
        for node in self.nodes.values():
            if node.kind == "base XOR":
                if len(self.edges[node.name]) != 2:
                    node.is_bad = True
                    continue
                for next_node_name in self.edges[node.name]:
                    next_node = self.nodes[next_node_name]
                    if next_node.prefix == "AND":
                        if next_node.kind:
                            next_node.is_bad = True
                            continue
                        next_node.kind = "help AND"
                    elif next_node.prefix == "XOR":
                        if next_node.kind and next_node.kind != "end":
                            next_node.is_bad = True
                            continue
                    else:
                        next_node.is_bad = True
        # mark next OR
        for node in self.nodes.values():
            if node.kind == "base AND":
                if len(self.edges[node.name]) != 1:
                    node.is_bad = True
                    continue
                next_node_name = self.edges[node.name][0]
                next_node = self.nodes[next_node_name]
                if next_node.prefix == "OR":
                    if next_node.kind:
                        next_node.is_bad = True
                        continue
                    next_node.kind = "next OR"
                else:
                    next_node.is_bad = True
        # mark help AND
        for node in self.nodes.values():
            if node.kind == "next OR":
                if len(self.edges[node.name]) != 2:
                    node.is_bad = True
                    continue
                nnn1, nnn2 = self.redges[node.name]
                next_node_1 = self.nodes[nnn1]
                next_node_2 = self.nodes[nnn2]
                if next_node_1.kind == "start" and next_node_2.kind == "start":
                    continue
                if next_node_1.kind == "base AND":
                    next_node = next_node_2
                else:
                    next_node = next_node_1
                if next_node.prefix != "AND":
                    next_node.is_bad = True
                    continue
                if next_node.kind and next_node.kind != "help AND":
                    next_node.is_bad = True
                    continue
                next_node.kind = "help AND"
        # check help AND
        for node in self.nodes.values():
            if node.kind == "help AND":
                if len(self.edges[node.name]) != 1:
                    node.is_bad = True
                    continue
                nnn1, nnn2 = self.redges[node.name]
                next_node_1 = self.nodes[nnn1]
                next_node_2 = self.nodes[nnn2]
                if not (next_node_1.kind == "base XOR" and next_node_2.kind == "next OR" or
                    next_node_2.kind == "base XOR" and next_node_1.kind == "next OR"):
                    node.is_bad = True
                    continue
        # check end
        for node in self.nodes.values():
            if node.kind == "end":
                if node.name == f"z{self.numbers_length}":
                    node.is_bad = False
                    nnn1, nnn2 = self.redges[node.name]
                    next_node_1 = self.nodes[nnn1]
                    next_node_2 = self.nodes[nnn2]
                    if next_node_1.kind == "base AND":
                        next_node = next_node_2
                    else:
                        next_node = next_node_1
                    next_node.kind = "help AND"
                    continue
                if node.prefix != "XOR":
                    node.is_bad = True
                    continue
                nnn1, nnn2 = self.redges[node.name]
                next_node_1 = self.nodes[nnn1]
                next_node_2 = self.nodes[nnn2]
                if node.name == "z00":
                    if not (next_node_1.kind == "start" and next_node_2.kind == "start"):
                        node.is_bad = True
                else:
                    if not (next_node_1.kind == "base XOR" and next_node_2.kind == "next OR" or
                        next_node_2.kind == "base XOR" and next_node_1.kind == "next OR"):
                        node.is_bad = True
        # mark unkinded
        for node in self.nodes.values():
            if not node.kind:
                node.is_bad = True
        # unmark those who has bad children
        for node in self.nodes.values():
            if node.is_bad:
                for child_name in self.redges[node.name]:
                    child = self.nodes[child_name]
                    if child.is_bad or child.kind is None:
                        node.is_bad = False
                        break
        if DEBUG:
            print("\n\n\nbad:")
            print([n.name for n in self.nodes.values() if n.is_bad])
            for node in sorted(self.nodes.values(), key=lambda x: x.name):
                if node.is_bad:
                    print(f"{node.name} op={node.prefix} kind={node.kind}")
                    print("prev:")
                    for next_node_name in self.redges.get(node.name, []):
                        next_node = self.nodes[next_node_name]
                        print(f"\t{next_node.name} op={next_node.prefix} kind={next_node.kind}")
                    print("next:")
                    for next_node_name in self.edges.get(node.name, []):
                        next_node = self.nodes[next_node_name]
                        print(f"\t{next_node.name} op={next_node.prefix} kind={next_node.kind}")

    def get_for_draw(self) -> tuple[list[Circle], list[Segment]]:
        # initialize heights and positions if needed
        if not self.initialized_positions:
            self.initialized_positions = True
            self.calculate_heights()
            for i, node in enumerate(self.nodes.values()):
                x = node.height * (4 * self.CIRCLE_SIZE)
                y = i * self.CIRCLE_SIZE
                if node.name.startswith(("x", "y", "z")):
                    y = len(self.nodes) * int(node.name[1:]) / self.numbers_length
                    y += int(node.name.startswith("y"))
                    y *= self.CIRCLE_SIZE
                node.position = Point(x, y)
        # move around positions if not finished already
        changed = set()
        if not self.finished_calculating_position:
            changed = self.calculate_positions()
            if DEBUG:
                print(f"Changed: {len(changed)}")
            if len(changed) == 0:
                self.finished_calculating_position = True
        # convert nodes to circles
        circles: dict[str, Circle] = {}
        for node_name, node in self.nodes.items():
            circles[node_name] = Circle(node.prefix + node.name, node.position, self.CIRCLE_SIZE, bg_color=(GREEN if node in changed else BLACK))
        # find probably bad places and mark circles
        self.find_bad_nodes()
        # convert edges to segments
        segments: list[Segment] = []
        for node_in, nodes_out in self.edges.items():
            for node_out in nodes_out:
                if self.nodes[node_in].is_bad or self.nodes[node_out].is_bad:
                    color = RED
                    width = 8
                else:
                    color = BLACK
                    width = 1
                segments.append(Segment(circles[node_in], circles[node_out], color=color, width=width))
        return circles.values(), segments


def main_graph():
    graph = Graph()
    graph.read()
    circles, segments = graph.get_for_draw()

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    min_x, max_x, min_y, max_y = 0, 0, 0, 0
    for p in [c.position for c in circles]:
        min_x, max_x, min_y, max_y = min(min_x, p.x), max(max_x, p.x), min(min_y, p.y), max(max_y, p.y)
    min_x -= (max_x - min_x) * CAMERA_INIT_MARGIN
    max_x += (max_x - min_x) * CAMERA_INIT_MARGIN
    min_y -= (max_y - min_y) * CAMERA_INIT_MARGIN
    max_y += (max_y - min_y) * CAMERA_INIT_MARGIN
    camera_offset = Point(min_x, min_y)
    scale = min(WIDTH / (max_x - min_x), HEIGHT / (max_y - min_y))

    search_text = " "

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                search_text = (search_text + event.unicode)[-3:]
                if DEBUG:
                    print("Searching for:", search_text)

        keys = pygame.key.get_pressed()
        
        # Move camera
        if keys[pygame.K_LEFT]:
            camera_offset.x -= CAMERA_MOVEMENT_RATE #/ scale
        if keys[pygame.K_RIGHT]:
            camera_offset.x += CAMERA_MOVEMENT_RATE #/ scale
        if keys[pygame.K_UP]:
            camera_offset.y -= CAMERA_MOVEMENT_RATE #/ scale
        if keys[pygame.K_DOWN]:
            camera_offset.y += CAMERA_MOVEMENT_RATE #/ scale
            
        if keys[pygame.K_PLUS] or keys[pygame.K_KP_PLUS]:
            scale *= CAMERA_SCALE_RATE
        if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
            scale /= CAMERA_SCALE_RATE

        screen.fill(WHITE)
        circles, segments = graph.get_for_draw()
        for circle in circles:
            if search_text in circle.name.lower():
                circle.bg_color = RED
                circle.radius = Graph.CIRCLE_SIZE * 8
        for segment in segments:
            segment.draw(screen, camera_offset, scale)
        for circle in circles:
            circle.draw(screen, camera_offset, scale)

        pygame.display.flip()
        clock.tick(FPS)


def main_solution():
    graph = Graph()
    graph.read()
    graph.MAX_POSITION_CALCULATION_ITER = 0
    _ = graph.get_for_draw()
    bad_nodes = [n.name for n in graph.nodes.values() if n.is_bad]
    return ",".join(sorted(bad_nodes))


if __name__ == "__main__":
    if DEBUG:
        main_graph()
    else:
        print(main_solution())

