import pygame
import math

from src import PyDriverUtils as utils


class PyRoad(pygame.sprite.Sprite):

    def __init__(self, screen_size, lane_count=4):

        pygame.sprite.Sprite.__init__(self)

        self.screen_size = screen_size
        self.lane_count = lane_count
        self.road_height = screen_size.h * 2

        self.image = pygame.Surface((screen_size.w, self.road_height), pygame.SRCALPHA)
        self.image.fill("gray")

        self.rect = self.image.get_rect()
        self.rect.y = (screen_size.h - self.road_height) / 2

        self.padding = 20
        self.borders_line_width = 7

        self.borders = []

        self.middle_line_width = 4
        self.middle_line_dash = 20

        self.draw_borders()
        self.draw_lanes()

    def get_lane_center(self, lane_index):

        w = self.rect.width - (self.padding * 2) - (self.borders_line_width * 2)
        lane_size = w / self.lane_count
        half_line = (lane_size/2)
        x = half_line + self.padding + self.borders_line_width
        xi = (lane_size * lane_index) + x
        return xi

    def draw_borders(self):

        x = self.padding
        lane_rect = pygame.Rect(x, 0, self.borders_line_width, self.rect.height)
        pygame.draw.rect(self.image, "white", lane_rect)
        self.borders.append(lane_rect)

        x = self.rect.width - self.padding - self.borders_line_width
        lane_rect = pygame.Rect(x, 0, self.borders_line_width, self.rect.height)
        pygame.draw.rect(self.image, "white", lane_rect)
        self.borders.append(lane_rect)

    def draw_lanes(self):

        for i in range(1, self.lane_count):

            w = self.rect.width - (self.padding * 2) - (self.borders_line_width * 2)
            x = utils.lerp(0, w, i / self.lane_count)
            x = x + self.padding + (self.middle_line_width * i)
            self.draw_dashed_line(self.image, "white", (x, 0), (x, self.rect.height), self.middle_line_width, self.middle_line_dash)

    @staticmethod
    def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=4):

        origin = utils.Point(start_pos)
        origin.y -= 120
        target = utils.Point(end_pos)
        target.y += 120
        displacement = target - origin
        length = len(displacement)

        slope = displacement.__div__(length)
        for index in range(0, int(length / dash_length), 2):
            start = origin + (slope * index * dash_length)
            end = origin + (slope * (index + 1) * dash_length)
            pygame.draw.line(surf, color, start.get(), end.get(), width)

    def update(self, car):

        self.rect.y += -car.velocity[1]
        if self.rect.y >= 0:
            self.rect.y = ((self.screen_size.h - self.road_height) / 2) - (self.middle_line_dash / 2)
        if self.rect.y <= (self.screen_size.h - self.road_height):
            self.rect.y = ((self.screen_size.h - self.road_height) / 2) + (self.middle_line_dash / 2)
