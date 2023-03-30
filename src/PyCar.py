
import pygame
import math

from src.PySensors import PySensors
from src.PyHitbox import PyHitbox
from src.PyBrain import PyNetwork


class PyCar(pygame.sprite.Sprite):

    def __init__(self, x, y, color, is_traffic=False, have_brain=False, visible_sensors=False, visible_hitbox=False):

        pygame.sprite.Sprite.__init__(self)

        self.base_color = color
        self.is_traffic = is_traffic
        self.have_brain = have_brain

        self.car_image = pygame.Surface((30, 50), pygame.SRCALPHA)
        self.car_image.fill(self.base_color)
        self.image = self.car_image

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.sensors = PySensors(car=self, draw_sensors=visible_sensors)

        if is_traffic:
            return

        self.is_damaged = False
        self.hit_box = PyHitbox(self, is_visible=visible_hitbox)

        self.speed = 0
        self.max_speed = 6
        self.acceleration = 0.5

        self.friction = 0.05
        self.brakes = 2.0

        self.heading = 0
        self.initial_angle = -90
        self.angular_velocity = 1.8

        self.velocity = pygame.math.Vector2(0, 0)
        self.position = pygame.math.Vector2(x, y)

        self.is_first_car = False
        if self.have_brain:
            self.brain_input = [0, 0, 0, 0]
            self.brain = PyNetwork(neurons=[self.sensors.ray_count, 6, 4])

    def turn(self, angle_degrees):

        if self.speed <= 0:
            angle_degrees = 0

        self.heading += math.radians(angle_degrees)

    def accelerate(self):

        self.speed += self.acceleration
        if self.speed > self.max_speed:
            self.speed = self.max_speed

    def brake(self):

        self.speed -= self.brakes / 10
        if self.speed < self.friction:
            self.speed = 0

    def update(self):

        if self.is_traffic:
            return

        if self.speed > 0:
            self.speed -= self.friction

        if self.speed < 0:
            self.speed += self.friction

        if abs(self.speed) < self.friction:
            self.speed = 0

        if self.have_brain:

            if self.brain_input[0] == 1:
                self.accelerate()
            if self.brain_input[1] == 1:
                self.brake()
            if self.brain_input[2] == 1:
                self.turn(-self.angular_velocity)
            if self.brain_input[3] == 1:
                self.turn(self.angular_velocity)

        self.image = pygame.transform.rotate(self.car_image, math.degrees(-self.heading))
        self.rect = self.image.get_rect(center=self.rect.center)

        self.velocity.from_polar((self.speed, math.degrees(math.radians(self.initial_angle) + self.heading)))
        self.position += self.velocity

        # self.rect.center = (round(self.position[0]), round(self.position[1]))
        # self.rect.x = round(self.position[0])
        self.rect.center = (round(self.position[0]), round(self.position[1]))

        if self.have_brain and self.brain:

            readings = self.sensors.readings

            def calc_offset(r):

                if r is None:
                    return 0

                return r[0]

            offsets = list(map(calc_offset, readings))
            outputs = PyNetwork.feed_forward(offsets, self.brain)
            self.brain_input = outputs

        if self.is_damaged:
            self.car_image.fill("black")
        else:
            self.car_image.fill(self.base_color)

        if self.sensors.are_active:
            self.car_image.fill("pink")
        else:
            self.car_image.fill(self.base_color)

        if self.is_first_car:
            self.car_image.fill("red")
            self.sensors.draw_sensors = True
        else:
            self.car_image.fill(self.base_color)
            self.sensors.draw_sensors = False
