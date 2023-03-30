import mpmath
import pygame
import math
from mpmath import *


class PyLine:

    def __init__(self, start_point, end_point):
        self.sx = start_point[0]
        self.sy = start_point[1]
        self.ex = end_point[0]
        self.ey = end_point[1]


class PyHitbox:

    def __init__(self, car, is_visible=False):

        self.is_visible = is_visible
        self.car = car
        self.line_width = 1

        self.polygon = [PyLine((0, 0), (0, 0)), PyLine((0, 0), (0, 0)), PyLine((0, 0), (0, 0)), PyLine((0, 0), (0, 0))]

    def draw_on_screen(self, screen):
        center = self.car.rect.center

        widht = 32 * 1
        height = 53.6 * 1
        a = widht / 2
        b = height / 2
        c = math.sqrt(((a / 2) * (a / 2)) + ((b / 2) * (b / 2))) * 2

        c = c * 0.9

        angle = math.atan(b / a)

        p1x = center[0] + math.sin(math.degrees(-angle) - self.car.heading) * c
        p1y = center[1] + math.cos(math.degrees(-angle) - self.car.heading) * c

        p2x = center[0] + math.sin(math.degrees(angle) - self.car.heading) * c
        p2y = center[1] + math.cos(math.degrees(angle) - self.car.heading) * c

        p4x = center[0] - math.sin(math.degrees(angle) - self.car.heading) * c
        p4y = center[1] - math.cos(math.degrees(angle) - self.car.heading) * c

        p3x = center[0] - math.sin(math.degrees(-angle) - self.car.heading) * c
        p3y = center[1] - math.cos(math.degrees(-angle) - self.car.heading) * c

        self.polygon[0] = PyLine((p1x, p1y), (p2x, p2y))
        self.polygon[1] = PyLine((p2x, p2y), (p3x, p3y))
        self.polygon[2] = PyLine((p3x, p3y), (p4x, p4y))
        self.polygon[3] = PyLine((p4x, p4y), (p1x, p1y))

        if self.is_visible:

            pygame.draw.line(screen, "red", (p1x, p1y), (p2x, p2y), self.line_width)
            pygame.draw.line(screen, "red", (p2x, p2y), (p3x, p3y), self.line_width)
            pygame.draw.line(screen, "red", (p3x, p3y), (p4x, p4y), self.line_width)
            pygame.draw.line(screen, "red", (p4x, p4y), (p1x, p1y), self.line_width)
