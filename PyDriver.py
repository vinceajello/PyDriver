import pygame
import random

import PyDriverUtils as utils
from PyRoad import PyRoad
from PyCar import PyCar


class PyDriver:

    def __init__(self, run_type="play"):

        pygame.init()

        self.run_type = run_type

        self.done = False

        self.clock = pygame.time.Clock()
        self.start = pygame.time.get_ticks()

        self.screen_size = utils.ScreeSize(400, 700)
        self.screen = pygame.display.set_mode((self.screen_size.w, self.screen_size.h))

        self.road_group = pygame.sprite.Group()
        self.road = PyRoad(self.screen_size, 3)
        self.road_group.add(self.road)

        self.traffic = []
        self.traffic_enabled = True
        self.traffic_speed = 4
        self.traffic_spawn_y = 200
        self.traffic_spawn_frequency = 3000
        self.traffic_cars_per_spawn = 1
        self.traffic_spawn_start_time = self.start - self.traffic_spawn_frequency
        self.traffic_group = pygame.sprite.Group()

        self.players = []
        self.players_per_generation = 200
        self.generation_count = 0
        self.generation_heritage_percent = 1
        self.generation_mutability_factor = 1
        self.players_spawn_y = self.screen_size.h * 0.8

        self.car = None
        self.cars_group = pygame.sprite.LayeredUpdates()

        match run_type:
            case "play":
                self.add_player()
            case "train":
                self.best_car = None
                self.add_players_generation(self.players_per_generation)

    def restart(self):

        self.traffic = []
        self.players = []
        self.cars_group = pygame.sprite.LayeredUpdates()
        self.traffic_group = pygame.sprite.Group()
        self.traffic_spawn_start_time = pygame.time.get_ticks() - self.traffic_spawn_frequency

        if self.run_type == "train":

            self.best_car = None
            self.add_players_generation(self.players_per_generation)

    #
    #
    # GAME MODES - PLAYER
    #
    #

    def add_player(self):

        car_x = self.road.get_lane_center(1)
        self.car = PyCar(car_x, self.players_spawn_y, "blue", visible_sensors=True)
        self.cars_group.add(self.car, layer=1)
        self.players.append(self.car)

    #
    #
    # GAME MODES - TRAIN
    #
    #

    def add_players_generation(self, n_of_players):

        print(f"Generation {self.generation_count}")

        for i in range(0, n_of_players):
            # rnd_lane = random.randrange(0, self.road.lane_count)
            car_x = self.road.get_lane_center(1)
            player_car = PyCar(car_x, self.players_spawn_y, "blue", have_brain=True, visible_sensors=False)

            self.cars_group.add(player_car, layer=2)
            self.players.append(player_car)

        if self.best_car:

            self.players[0].brain = self.best_car.brain

            heritage = int(len(self.players) * self.generation_heritage_percent)
            for i in range(1, heritage):
                self.players[i].brain = self.best_car.brain.mutate(self.players[i].brain,
                                                                   self.generation_mutability_factor)

        self.generation_count += 1

    def fitness(self):

        best_payers = sorted(self.players, key=lambda x: x.sensors.avoidance)
        self.best_car = best_payers[0]
        return best_payers[0]

    #
    #
    # TRAFFIC
    #
    #

    def handle_traffic_events(self):

        if self.traffic_enabled:
            self.add_random_car()
            self.animate_traffic()

    def add_random_car(self):

        now = pygame.time.get_ticks()
        if now - self.traffic_spawn_start_time < self.traffic_spawn_frequency:
            return

        colors = ["white", "green", "purple", "brown", "pink"]
        random_lanes = random.sample(range(0, self.road.lane_count), self.traffic_cars_per_spawn)

        for random_lane in random_lanes:
            rnd_color_index = random.randrange(0, len(colors) - 1)
            car_x = self.road.get_lane_center(random_lane)
            traffic_car = PyCar(car_x, self.traffic_spawn_y, colors[rnd_color_index], is_traffic=True)

            self.traffic.append(traffic_car)
            self.traffic_group.add(traffic_car)

        self.traffic_spawn_start_time = now

    def animate_traffic(self):

        i = 0
        for car in self.traffic:

            if len(self.players) > 0:
                ordered_players = sorted(self.players, key=lambda x: x.position[1])
                car.rect.y -= (self.traffic_speed + ordered_players[0].velocity[1])
            else:
                car.rect.y -= self.traffic_speed

            if car.rect.y < -0 or car.rect.y > self.screen.get_height() + 0:
                self.traffic.pop(i)
                self.traffic_group.remove(car)

            i += 1

    #
    #
    # COLLISIONS
    #
    #

    def check_collisions(self):

        for player in self.players:

            for line in player.hit_box.polygon:

                for border in self.road.borders:

                    collision = border.clipline(line.sx, line.sy, line.ex, line.ey)
                    if collision:
                        player.is_damaged = True
                        self.destroy_player(player)
                    else:
                        player.is_damaged = False

                for car in self.traffic:

                    collision = car.rect.clipline(line.sx, line.sy, line.ex, line.ey)
                    if collision:
                        if collision:
                            player.is_damaged = True
                            self.destroy_player(player)
                        else:
                            player.is_damaged = False

    def destroy_player(self, player):

        if player == self.car:
            return

        if player in self.players:
            self.players.remove(player)
            self.cars_group.remove(player)

    #
    #
    # PLAYER CONTROLLER
    #
    #

    def player_controller(self, keys):

        if keys[pygame.K_UP]:
            self.car.accelerate()
        if keys[pygame.K_DOWN]:
            self.car.brake()
        if keys[pygame.K_LEFT]:
            self.car.turn(-self.car.angular_velocity)
        if keys[pygame.K_RIGHT]:
            self.car.turn(self.car.angular_velocity)

    #
    #
    # KEY RELATED EVENTS
    #
    #

    def key_events(self, event):

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                self.restart()
        if event.type == pygame.QUIT:
            self.done = True

    #
    #
    # EVENTS / UPDATES / RENDER LOGIC
    #
    #

    def events(self):

        self.handle_traffic_events()

        keys = pygame.key.get_pressed()
        if keys is not None and self.car:
            self.player_controller(keys)

        for event in pygame.event.get():
            self.key_events(event)

    #
    #
    # UPDATE
    #
    #

    def remove_slow_car(self, car):

        if car.rect.y > self.screen_size.h - 50:
            self.destroy_player(car)

    @staticmethod
    def update_cars_relative(car, first_car):

        car.position[1] -= first_car.velocity[1]

    def update_sensors(self, car):

        car.sensors.get_readings(self.road, self.traffic)

    def update_road(self, first_car):

        self.road.update(first_car)

    def update(self):

        if len(self.players) <= 0:
            if self.run_type == "train":
                self.restart()

        ordered_players = sorted(self.players, key=lambda x: x.rect.center[1])

        for car in ordered_players:

            car.is_first_car = False
            if self.best_car and self.best_car in self.cars_group:
                self.cars_group.change_layer(self.best_car, 2)

            self.update_sensors(car)

            self.update_cars_relative(car, ordered_players[0])

            self.remove_slow_car(car)

        if len(ordered_players) > 0:

            self.update_road(ordered_players[0])

        if self.run_type == "train":
            best_player = self.fitness()
            if self.best_car:
                best_player.is_first_car = True
                self.cars_group.change_layer(best_player, 3)

        self.cars_group.update()
        self.check_collisions()

    def render(self):

        self.road_group.draw(self.screen)
        self.cars_group.draw(self.screen)
        self.traffic_group.draw(self.screen)

        for car in self.players:
            car.sensors.draw_on_screen(self.screen)
            car.hit_box.draw_on_screen(self.screen)

        pygame.display.flip()

    #
    #
    # MAIN LOOP
    #
    #

    def run(self):

        while not self.done:
            self.events()

            self.update()

            self.render()

            self.clock.tick(30)

        pygame.quit()


if __name__ == '__main__':
    pyd = PyDriver(run_type="train")
    pyd.run()
