import math


def lerp(a, b, t):

    return a + (b - a) * t


class ScreeSize:

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cx = w / 2
        self.cy = h / 2
        self.c = (self.cx, self.cy)

class Point:

    def __init__(self, point_t=(0, 0)):
        self.x = float(point_t[0])
        self.y = float(point_t[1])

    def __add__(self, other):
        return Point((self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        return Point((self.x - other.x, self.y - other.y))

    def __mul__(self, scalar):
        return Point((self.x * scalar, self.y * scalar))

    def __div__(self, scalar):
        return Point((self.x / scalar, self.y / scalar))

    def __len__(self):
        return int(math.sqrt(self.x ** 2 + self.y ** 2))

    # get back values in original tuple format
    def get(self):
        return self.x, self.y