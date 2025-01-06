import pygame
import sys
import numbers
import math
from typing import Any
from collections.abc import Iterable


WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)
GREEN = (0, 127, 0)
BLACK = (0, 0, 0)
FPS = 60
CAMERA_MOVEMENT_RATE = 15.0
CAMERA_SCALE_RATE = 1.05


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
        scaled_position = (self.position + camera_offset) * scale
        pygame.draw.circle(surface, self.bg_color, scaled_position.to_tuple(), scaled_radius)
        font = pygame.font.SysFont(None, self.font_size)
        text = font.render(self.name, True, self.fg_color)
        surface.blit(text, (scaled_position - (text.get_width() // 2, text.get_height() // 2)).to_tuple())


class Segment:
    def __init__(self, circle1: Circle, circle2: Circle, color: tuple[int, int, int] = BLACK):
        self.circle1: Circle = circle1
        self.circle2: Circle = circle2
        self.color: tuple[int, int, int] = color

    def draw(self, surface: Any, camera_offset: Point, scale: float):
        pos1 = (self.circle1.position + camera_offset) * scale
        pos2 = (self.circle2.position + camera_offset) * scale
        pygame.draw.line(surface, self.color, pos1.to_tuple(), pos2.to_tuple(), 1)


class Node:
    def __init__(self, name: str, prefix: str = ""):
        self.name = name
        self.prefix = prefix
        self.height: int = None
        self.position: Point = None

    def __repr__(self) -> str:
        return f"({self.prefix + self.name}, h={self.height})"


class Graph:
    CIRCLE_SIZE = 64
    MAX_POSITION_CALCULATION_ITER = 100

    def __init__(self):
        self.raw_edges: list[tuple[str, str, str, str]] = None
        self.edges: dict[str, str] = {}
        self.nodes: dict[str, Node] = {}
        self.initialized_positions = False

    def read(self):
        self.raw_edges = []
        while i := input():
            pass
        while i := input():
            input1, operation, input2, _, output = i.split(" ")
            self.raw_edges.append((input1, input2, output, operation))
        self.build()

    def build(self):
        self.edges: dict[str, str] = {}
        self.nodes: dict[str, Node] = {}
        for in1, in2, out, op in self.raw_edges:
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

    def calculate_heights(self):
        queue: list[Node] = []
        for node in self.nodes.values():
            if node.name.startswith(("x", "y")):
                node.height = 0
                queue.append(node)
        while queue:
            cur_node = queue[0]
            queue.pop(0)
            for next_node_name in self.edges.get(cur_node.name, []):
                next_node = self.nodes[next_node_name]
                queue.append(next_node)
                if next_node.height is None:
                    next_node.height = cur_node.height + 1
                else:
                    next_node.height = max(cur_node.height + 1, next_node.height)

    def calculate_positions(self) -> set[Node]:
        changed = True
        changed_nodes: set[Node] = set()
        iter = 0
        for node in self.nodes.values():
            node.old_position = node.position.copy()
        while changed and iter < self.MAX_POSITION_CALCULATION_ITER:
            iter += 1
            changed = False
            for n1, n2 in cross_iter(self.nodes.values(), self.nodes.values()):
                #if n1.height != n2.height:
                #    continue
                if n1.position.y == n2.position.y:
                    continue
                # before swap
                weight_before_swap = 0
                for next_node in self.edges.get(n1.name, []):
                    weight_before_swap += norm(n1.position, self.nodes[next_node].position)
                for next_node in self.edges.get(n2.name, []):
                    weight_before_swap += norm(n2.position, self.nodes[next_node].position)
                # swap
                n1.position.y, n2.position.y = n2.position.y, n1.position.y
                # after swap
                weight_after_swap = 0
                for next_node in self.edges.get(n1.name, []):
                    weight_after_swap += norm(n1.position, self.nodes[next_node].position)
                for next_node in self.edges.get(n2.name, []):
                    weight_after_swap += norm(n2.position, self.nodes[next_node].position)
                # swap back
                n1.position.y, n2.position.y = n2.position.y, n1.position.y
                # if needed, swap
                if weight_before_swap > weight_after_swap:
                    n1.position.y, n2.position.y = n2.position.y, n1.position.y
                    changed = True
                    #print("changed", n1, n2, weight_before_swap, weight_after_swap)
                    #print(n1.position, n2.position)
                    changed_nodes.add(n1)
                    changed_nodes.add(n2)
                    break
        # clean changed nodes to make sure we highlight only nodes who really changed position
        changed_nodes_clean: set[Node] = set()
        for node in changed_nodes:
            if node.old_position != node.position:
                changed_nodes_clean.add(node)
            else:
                print(node, node.old_position, node.position)
        return changed_nodes_clean

    def get_for_draw(self) -> tuple[list[Circle], list[Segment]]:
        if not self.initialized_positions:
            self.initialized_positions = True
            self.calculate_heights()
            for i, node in enumerate(self.nodes.values()):
                node.position = Point(node.height * (2 * self.CIRCLE_SIZE), i * self.CIRCLE_SIZE)
        changed = self.calculate_positions()
        print(f"Changed: {len(changed)}")
        circles: dict[str, Circle] = {}
        for node_name, node in self.nodes.items():
            circles[node_name] = Circle(node.prefix + node.name, node.position, self.CIRCLE_SIZE, bg_color=(GREEN if node in changed else BLACK))
        segments: list[Segment] = []
        for node_in, nodes_out in self.edges.items():
            for node_out in nodes_out:
                segments.append(Segment(circles[node_in], circles[node_out]))
        return circles.values(), segments, len(changed) == 0


def main():
    graph = Graph()
    graph.read()

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    camera_offset = Point(0, 0)
    scale = 1.0
    stop_updating = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        
        # Move camera
        if keys[pygame.K_LEFT]:
            camera_offset.x += CAMERA_MOVEMENT_RATE / scale
        if keys[pygame.K_RIGHT]:
            camera_offset.x -= CAMERA_MOVEMENT_RATE / scale
        if keys[pygame.K_UP]:
            camera_offset.y += CAMERA_MOVEMENT_RATE / scale
        if keys[pygame.K_DOWN]:
            camera_offset.y -= CAMERA_MOVEMENT_RATE / scale
            
        if keys[pygame.K_PLUS] or keys[pygame.K_KP_PLUS]:
            scale *= CAMERA_SCALE_RATE
        if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
            scale /= CAMERA_SCALE_RATE

        screen.fill(WHITE)
        if not stop_updating:
            circles, segments, stop_updating = graph.get_for_draw()
        for segment in segments:
            segment.draw(screen, camera_offset, scale)
        for circle in circles:
            circle.draw(screen, camera_offset, scale)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

