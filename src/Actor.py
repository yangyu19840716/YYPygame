# -*- coding:utf-8 -*-

import math
import random

from pygame.math import Vector2

from Engine import Const, Utility
from Engine.Graph import Graph


class Actor(object):
	speed_acc = 10
	rad_acc = 0.1
	size = 4

	def __init__(self):
		self.pos = Vector2(Const.CENTER_X, Const.CENTER_Y)
		self.pos_x, self.pos_y = int(self.pos.x), int(self.pos.y)  # 整型的位置
		self.grid_x = self.grid_y = 0
		self.max_speed = Const.MAX_SPEED
		self.color = Utility.rand_color()
		self.dir_rad = random.uniform(0.0, Const.DOUBLE_PI)
		self.speed = random.uniform(0.0, self.max_speed)
		self.speed_vec = Vector2(self.speed * math.cos(self.dir_rad), self.speed * math.sin(self.dir_rad))

		self.vision_size = Const.VISION_SIZE
		self.neighbours = []
		self.nearest_neighbour = None
		self.is_nearest_neighbour = False  # 被人指定为nearest_neighbour， 改变grid的时候重制

	def action(self, dt):
		self.pos += self.speed_vec * dt
		if self.pos.x > Const.WIDTH:
			self.pos.x -= (int(self.pos.x / Const.WIDTH) + 1) * Const.WIDTH
		elif self.pos.x < 0:
			self.pos.x += (int(-self.pos.x / Const.WIDTH) + 1) * Const.WIDTH
		if self.pos.y > Const.HEIGHT:
			self.pos.y -= (int(self.pos.y / Const.HEIGHT) + 1) * Const.HEIGHT
		elif self.pos.y < 0:
			self.pos.y += (int(-self.pos.y / Const.HEIGHT) + 1) * Const.HEIGHT
		self.pos_x, self.pos_y = int(self.pos.x), int(self.pos.y)

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

	def picked(self, x, y):
		pass

	def draw(self):
		Graph.draw_circle(Actor.size, self.pos, Actor.size, self.color)
