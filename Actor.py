# -*- coding:utf-8 -*-

import math
import random
import Const
from Graph import Graph
from pygame.math import Vector2


class Actor(object):
    speed_acc = 10
    rad_acc = 0.1
    size = 4

    def __init__(self):
        self.pos = Vector2(Const.CENTER_X, Const.CENTER_Y)
        self.max_speed = 300.0
        self.color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
        self.dir_rad = random.uniform(0.0, Const.DOUBLE_PI)
        self.speed = random.uniform(0.0, self.max_speed)
        self.speed_vec = Vector2(self.speed * math.cos(self.dir_rad), self.speed * math.sin(self.dir_rad))

    def action(self, dt):
        self.pos += self.speed_vec * dt
        if self.pos.x > Const.WIDTH:
            self.pos.x -= Const.WIDTH
        elif self.pos.x < 0:
            self.pos.x += Const.WIDTH
        if self.pos.y > Const.HEIGHT:
            self.pos.y -= Const.HEIGHT
        elif self.pos.y < 0:
            self.pos.y += Const.HEIGHT

        self.speed += random.uniform(-Actor.speed_acc, Actor.speed_acc)
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        elif self.speed < 0:
            self.speed = 0

        self.dir_rad += random.uniform(-Actor.rad_acc, Actor.rad_acc)
        if self.dir_rad > Const.DOUBLE_PI:
            self.dir_rad -= Const.DOUBLE_PI
        elif self.dir_rad < 0:
            self.dir_rad += Const.DOUBLE_PI

        self.speed_vec.x, self.speed_vec.y = self.speed * math.cos(self.dir_rad), self.speed * math.sin(self.dir_rad)

    def draw(self):
        Graph.draw_circle(Actor.size, self.pos, Actor.size, self.color)
