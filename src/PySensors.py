import pygame
import math

import PyDriverUtils as utils


class PySensorRay:

    def __init__(self, start_x, start_y, end_x, end_y):
        self.sx = start_x
        self.sy = start_y
        self.ex = end_x
        self.ey = end_y


class PySensors(pygame.sprite.Sprite):

    def __init__(self, car, ray_count=5, ray_length=200, draw_sensors=False):

        pygame.sprite.Sprite.__init__(self)

        self.draw_sensors = draw_sensors

        self.car = car
        self.ray_count = ray_count
        self.ray_length = ray_length
        self.ray_spread = math.pi / 4

        self.are_active = False
        self.have_avoided = False
        self.avoidance = 0

        self.rays = []
        self.readings = [None] * self.ray_count

    def get_readings(self, road, traffic):

        self.readings = [None] * self.ray_count

        index = 0
        for s in self.car.sensors.rays:

            for border in road.borders:

                collide = border.clipline(s.sx, s.sy, s.ex, s.ey)
                if collide:
                    (sx, sy), (_, _) = collide
                    distance = pygame.math.Vector2(sx, sy).distance_to((s.sx, s.sy)) / self.ray_length
                    output = (sx, sy), (s.ex, s.ey)
                    self.readings[index] = [distance, output]
                    if distance < 0.7:
                        self.are_active = True
                    else:
                        if self.are_active:
                            self.have_avoided = True
                            self.avoidance += 1
                        self.are_active = False

            for car in traffic:

                collide = car.rect.clipline(s.sx, s.sy, s.ex, s.ey)
                if collide:
                    (sx, sy), (_, _) = collide
                    distance = pygame.math.Vector2(sx, sy).distance_to((s.sx, s.sy)) / self.ray_length
                    output = (sx, sy), (s.ex, s.ey)
                    self.readings[index] = [distance, output]
                    if distance < 2:
                        self.are_active = True
                    else:
                        if self.are_active:
                            self.have_avoided = True
                            self.avoidance += 1
                        self.are_active = False

            index += 1

    def draw_readings(self, screen, only_closest=True):

        if not self.draw_sensors:
            return

        if only_closest:

            if len(self.readings) > 0:
                (sx, sy), (ex, ey) = self.readings[0][1]
                pygame.draw.line(screen, "red", (sx, sy), (ex, ey), 4)

        else:

            for reading in self.readings:
                if reading is not None:
                    (sx, sy), (ex, ey) = reading[1]
                    pygame.draw.line(screen, "red", (sx, sy), (ex, ey), 4)

    def draw_on_screen(self, screen):

        (csx, csy) = self.car.rect.center
        self.rays = []

        s_min = -self.ray_spread/2
        s_max = self.ray_spread/2

        for i in range(0, self.ray_count):

            angle = utils.lerp(s_min, s_max, i / (self.ray_count-1))

            cex = csx + math.sin(angle + self.car.heading) * self.ray_length
            cey = csy - math.cos(angle + self.car.heading) * self.ray_length

            ray = PySensorRay(csx, csy, cex, cey)
            self.rays.append(ray)

        if self.draw_sensors:

            for ray in self.rays:
                pygame.draw.line(screen, "yellow", (ray.sx, ray.sy), (ray.ex, ray.ey), 2)

            self.draw_readings(screen=screen, only_closest=False)
