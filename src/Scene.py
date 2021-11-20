# -*- coding:utf-8 -*-

import random

from Engine import Const
from Actor import Actor
from Engine.Singleton import Singleton


class Grid(object):
	# 格子大小使用整型，提高格子计算效率
	grid_size_w = Const.GRID_SIZE
	grid_size_h = Const.GRID_SIZE
	gird_in_vision = int(Const.VISION_SIZE / Const.GRID_SIZE) + 1

	def __init__(self):
		self.index_x = None
		self.index_y = None

		self.actors = []
		self.neighbours = []  # [[grid list 1], [grid list 2], ...] index 是与当前Grid的距离
		self.nearest_neighbour = None

	def init_neighbours(self, x, y):
		grid_in_vision = Grid.gird_in_vision
		self.index_x, self.index_y = x, y
		grid_num_w, grid_num_h = Scene.instance.grid_num_w, Scene.instance.grid_num_h
		neighbours = []
		for i in range(1, grid_in_vision):
			for xx in range(-x, x + 1):
				xxx = x + xx
				if xxx < 0 or xxx >= grid_num_w:
					continue

				yyy = y - i
				if yyy >= 0:
					neighbours.append(Scene.instance.get_grid(xxx, yyy))
				yyy = y + i
				if yyy < grid_num_h:
					neighbours.append(Scene.instance.get_grid(xxx, yyy))
			for yy in range(-i + 1, i):
				yyy = y + yy
				if yyy < 0 or yyy >= grid_num_h:
					continue

				xxx = x - i
				if xxx >= 0:
					neighbours.append(Scene.instance.get_grid(xxx, yyy))
				xxx = x + i
				if xxx < grid_num_w:
					neighbours.append(Scene.instance.get_grid(xxx, yyy))

			self.neighbours.append(neighbours)

	@staticmethod
	def pos_to_grid(x, y):
		"""
			坐标转换到格子，x，y 需要是整型
		"""
		return int(x / Grid.grid_size_w), int(y / Grid.grid_size_h)


class Scene(Singleton):
	def __init__(self):
		super(Scene, self).__init__()

		self.map_w = Const.WIDTH
		self.map_h = Const.HEIGHT

		# 为了让格子大小是整型， 多加了一行一列
		self.grid_num_w = int(Const.WIDTH / Const.GRID_SIZE) + 1
		self.grid_num_h = int(Const.HEIGHT / Const.GRID_SIZE) + 1

		self.update_neighbours = self.update_neighbours1

		self.size2 = Const.VISION_SIZE * Const.VISION_SIZE

		# Grid二维数组
		self.grids = []
		for x in range(self.grid_num_w):
			self.grids.append([])
			for y in range(self.grid_num_h):
				self.grids[x].append(Grid())

		for x in range(self.grid_num_w):
			for y in range(self.grid_num_h):
				grid = self.grids[x][y]
				grid.init_neighbours(x, y)

		self.actor_num = Const.ACTOR_NUM
		self.actors = []
		for i in range(self.actor_num):
			self.actors.append(Actor())

		for actor in self.actors:
			actor.grid_x, actor.grid_y = Grid.pos_to_grid(actor.pos_x, actor.pos_y)
			self.grids[actor.grid_x][actor.grid_y].actors.append(actor)

	def get_grid(self, index_x, index_y):
		return self.grids[index_x][index_y]

	def update_actors(self, dt):
		# for x in range(self.grid_num_w):
		#     for y in range(self.grid_num_h):
		#         self.grids[x][y].actors = []

		# 更新actor，以及grid
		for actor in self.actors:
			actor.action(dt)
			x, y = int(actor.pos_x / Grid.grid_size_w), int(actor.pos_y / Grid.grid_size_h)
			if actor.grid_x != x or actor.grid_y != y:
				self.grids[actor.grid_x][actor.grid_y].actors.remove(actor)
				self.grids[x][y].actors.append(actor)
				actor.is_nearest_neighbour = False
				actor.grid_x, actor.grid_y = x, y

	def update_neighbours1(self):
		for x in range(self.grid_num_w):
			for y in range(self.grid_num_h):
				grid = self.grids[x][y]
				if grid.nearest_neighbour and grid.nearest_neighbour.is_nearest_neighbour:
					continue

				for neighbours in grid.neighbours:
					neighbour_actors = []
					for neighbour in neighbours:
						if len(neighbour.actors) > 0:
							neighbour_actors.append(neighbour)
					num_neighbours = len(neighbour_actors)
					if num_neighbours == 0:
						continue
					elif num_neighbours == 1:
						neighbour = neighbour_actors[0]
					else:
						neighbour = random.choice(neighbour_actors)
					grid.nearest_neighbour = random.choice(neighbour.actors)
					grid.nearest_neighbour.is_nearest_neighbour = True
					break

	def update_neighbours2(self):
		for actor1 in self.actors:
			neighbours = []
			nearest = 999999
			for actor2 in self.actors:
				if actor1 is actor2:
					continue

				dis = (actor1.pos - actor2.pos).length_squared()
				if dis <= self.size2:
					neighbours.append(actor2)

					if dis < nearest:
						nearest = dis
						actor1.nearest_neighbour = actor2

			actor1.neighbours = neighbours
