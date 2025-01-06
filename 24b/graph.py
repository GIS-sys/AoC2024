import pygame
import sys
import numbers
import math
from typing import Any
from collections.abc import Iterable


WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)
BLACK = (0, 0, 0)
FPS = 60
CAMERA_MOVEMENT_RATE = 5.0
CAMERA_SCALE_RATE = 1.01


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


class Graph:
    def __init__(self):
        pass

    def get_for_draw(self) -> tuple[list[Circle], list[Segment]]:
        circles = [
            Circle("Circle A", Point(100, 100), 30),
            Circle("Circle B", Point(300, 200), 50),
            Circle("Circle C", Point(500, 300), 20)
        ]
        segments = [
            Segment(circles[0], circles[1]),
            Segment(circles[1], circles[2]),
            Segment(circles[2], circles[0])
        ]
        return circles, segments


def main():
    graph = Graph()
    circles, segments = graph.get_for_draw()

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    camera_offset = Point(0, 0)
    scale = 1.0

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
        for segment in segments:
            segment.draw(screen, camera_offset, scale)
        for circle in circles:
            circle.draw(screen, camera_offset, scale)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

