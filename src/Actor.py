# -*- coding:utf-8 -*-

import math
import random

from Core import Const, Utility
from Core.Graph import Graph


SPEED_ACC = 1
RAD_ACC = 0.1
SIZE = 4
PICK_SIZE_EXTEND = 2
MAX_SPEED = 30.0
MIN_MOVE = 0.01


class Actor(object):
	ACTOR_ID = 0

	def __init__(self):
		self.new_pos_x, self.new_pos_y = self.pos_x, self.pos_y =\
			random.randint(0, Const.WIDTH), random.randint(0, Const.HEIGHT)  # pos为整型的位置
		self.grid_x = self.grid_y = 0
		self.max_speed = MAX_SPEED
		self.color = Utility.rand_color()
		self.dir_rad = random.uniform(0.0, Const.DOUBLE_PI)
		self.speed = random.uniform(0.0, self.max_speed)
		self.speed_x, self.speed_y = self.speed * math.cos(self.dir_rad), self.speed * math.sin(self.dir_rad)

		self.vision_size = Const.VISION_SIZE
		self.neighbours = []
		self.nearest_neighbour = None
		self.followers = []  		# grid list, 被leader指定为nearest_neighbour, 改变grid的时候重置
		self.is_leader = False  	# 被grid指定为leader_actor, 改变grid的时候重置

		self.name = Actor.ACTOR_ID
		Actor.ACTOR_ID += 1
		self.dirty = True  # 位置改变会 dirty
		self.picked = False
		self.draw_color = self.color

	def update(self, dt):
		self.speed += random.uniform(-SPEED_ACC, SPEED_ACC)
		if self.speed > self.max_speed:
			self.speed = self.max_speed
		elif self.speed < 0:
			self.speed = 0

		self.dir_rad += random.uniform(-RAD_ACC, RAD_ACC)
		if self.dir_rad > Const.DOUBLE_PI:
			self.dir_rad -= Const.DOUBLE_PI
		elif self.dir_rad < 0:
			self.dir_rad += Const.DOUBLE_PI

		self.speed_x, self.speed_y = self.speed * math.cos(self.dir_rad), self.speed * math.sin(self.dir_rad)

		self.new_pos_x += self.speed_x * dt
		self.new_pos_y += self.speed_y * dt
		dx = self.new_pos_x - self.pos_x
		dy = self.new_pos_y - self.pos_y
		if dx * dx + dy * dy < MIN_MOVE:
			return

		self.pos_x, self.pos_y = int(self.new_pos_x), int(self.new_pos_y)
		if self.pos_x > Const.WIDTH:
			self.pos_x -= int(self.pos_x / Const.WIDTH) * Const.WIDTH
		elif self.pos_x < 0:
			self.pos_x += (int(-self.pos_x / Const.WIDTH) + 1) * Const.WIDTH
		if self.pos_y > Const.HEIGHT:
			self.pos_y -= int(self.pos_y / Const.HEIGHT) * Const.HEIGHT
		elif self.pos_y < 0:
			self.pos_y += (int(-self.pos_y / Const.HEIGHT) + 1) * Const.HEIGHT

		self.dirty = True

	def in_actor(self, x, y):
		size = SIZE + PICK_SIZE_EXTEND
		if self.pos_x - size < x < self.pos_x + size and self.pos_y - size < y < self.pos_y + size:
			return True
		else:
			return False

	def pick(self):
		self.picked = True

	def unpick(self):
		self.picked = False

	def draw(self):
		Graph.draw_circle(self.pos_x, self.pos_y, SIZE, SIZE, self.draw_color)

	def get_neighbours_from_grid(self):
		grid = Const.SCENE.get_grid(self.grid_x, self.grid_y)
		neighbours = []
		for neighbour_grids in grid.neighbours:
			for neighbour_grid in neighbour_grids:
				neighbours.extend(neighbour_grid.actors)

		if self.is_leader:
			nearest = self.nearest_neighbour
		else:
			nearest = grid.leader_actor

		return neighbours, nearest

