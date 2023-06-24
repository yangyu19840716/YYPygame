# -*- coding:utf-8 -*-

import random
from Core import Const, Utility
from Core.Math import Vector2


MERGE_PRECISION = 0.01


class Grid:
	# 格子大小使用整型，提高格子计算效率
	grid_size_w = Const.GRID_SIZE
	grid_size_h = Const.GRID_SIZE

	def __init__(self):
		self.index_x = None
		self.index_y = None
		self.left_top = Vector2()
		self.right_bottom = Vector2()
		self.grid_pos = Vector2()
		self.actors_in_grid = []
		self.grid_neighbours = []  	# [(dis 1, grid list 1), (dis 2, grid list 2), ...] neighbour按距离分组
		self.leader_actor = None    # actor
		self.grid_dirty = True		# actors 改变时 grid dirty
		self.picked = False

		self.init_neighbours = self.init_neighbours_round

	def init_pos(self, x, y):
		self.index_x, self.index_y = x, y
		self.left_top.x, self.left_top.y = x * Grid.grid_size_w, y * Grid.grid_size_h
		self.right_bottom.x, self.right_bottom.y = (x + 1) * Grid.grid_size_w, (y + 1) * Grid.grid_size_h
		self.grid_pos.x, self.grid_pos.y = (x + 0.5) * Grid.grid_size_w, (y + 0.5) * Grid.grid_size_w,

	def init_neighbours_square(self):
		x, y = self.index_x, self.index_y
		grid_num_w, grid_num_h = Const.SCENE.grid_num_w, Const.SCENE.grid_num_h
		gird_in_vision = int(Const.VISION_SIZE / Const.GRID_SIZE) + 1
		for i in range(1, gird_in_vision):
			neighbours = []
			for xx in range(-i, i + 1):
				xxx = x + xx
				if xxx < 0 or xxx >= grid_num_w:
					continue

				yyy = y - i
				if yyy >= 0:
					grid = Const.SCENE.grids[xxx][yyy]
					neighbours.append(grid)
				yyy = y + i
				if yyy < grid_num_h:
					grid = Const.SCENE.grids[xxx][yyy]
					neighbours.append(grid)
			for yy in range(-i + 1, i):
				yyy = y + yy
				if yyy < 0 or yyy >= grid_num_h:
					continue

				xxx = x - i
				if xxx >= 0:
					grid = Const.SCENE.grids[xxx][yyy]
					neighbours.append(grid)
				xxx = x + i
				if xxx < grid_num_w:
					grid = Const.SCENE.grids[xxx][yyy]
					neighbours.append(grid)

			self.grid_neighbours.append((i, neighbours))

	def init_neighbours_round(self):
		scene = Const.SCENE
		vision_size = Const.VISION_SIZE
		grid_in_vision = int(vision_size / Const.GRID_SIZE) + 1
		grid_num_w, grid_num_h = Const.SCENE.grid_num_w, Const.SCENE.grid_num_h
		vision2 = vision_size * vision_size
		visions = range(-grid_in_vision + 1, grid_in_vision)
		merge_precision = 1.0 / MERGE_PRECISION
		neighbours = {}
		for i in visions:
			for j in visions:
				if i == 0 and j == 0:
					continue

				x = self.index_x + i
				y = self.index_y + j
				if x < 0 or y < 0 or x >= grid_num_w or y >= grid_num_h:
					continue

				grid = scene.grids[x][y]
				dis2 = (grid.grid_pos - self.grid_pos).length_squared()
				if dis2 <= vision2:
					key_dis = int(dis2 * merge_precision)
					neighbour_list = neighbours.get(key_dis, None)
					if neighbour_list:
						neighbour_list.append(grid)
					else:
						neighbours[key_dis] = [grid]

		self.grid_neighbours = Utility.sorted_dict_by_key(neighbours)

	@staticmethod
	def pos_to_grid(x, y):
		"""
			坐标转换到格子，x，y 需要是整型
		"""
		return int(x / Grid.grid_size_w), int(y / Grid.grid_size_h)

	def in_grid(self, x, y):
		return self.left_top.x < x < self.right_bottom.x and self.left_top.y < y < self.right_bottom.y

	def pick(self):
		self.picked = True

		for actor in self.actors_in_grid:
			actor.draw_color = Const.WHITE

	def unpick(self):
		self.picked = False

		for actor in self.actors_in_grid:
			actor.draw_color = actor.actor_color

	def get_nearest_actor_in_neighbour_grid(self):
		for neighbours in self.grid_neighbours:
			neighbour_actors = []
			for neighbour in neighbours[1]:
				if neighbour.leader_actor:
					neighbour_actors.append(neighbour.leader_actor)
			if neighbour_actors:
				return random.choice(neighbour_actors)
		return None
