# -*- coding:utf-8 -*-

import random
from core import const, utility
from core.math import Vector2


MERGE_PRECISION = 0.01


class Grid:
	# 格子大小使用整型，提高格子计算效率
	grid_size_w = const.GRID_SIZE
	grid_size_h = const.GRID_SIZE
	neighbour_offset_groups = None

	def __init__(self):
		self.index_x = None
		self.index_y = None
		self.left_top = Vector2()
		self.right_bottom = Vector2()
		self.grid_pos = Vector2()
		self.actors_in_grid = []
		self.grid_neighbours = []  		# [(dis 1, grid list 1), (dis 2, grid list 2), ...] neighbour按距离分组
		self.leader_actor = None    	# actor
		self.assistant_actor = None		# actor
		self.grid_dirty = True			# actors 改变时 grid dirty
		self.picked = False
		self.left = 0
		self.right = 0
		self.top = 0
		self.bottom = 0

		self.init_neighbours = self.init_neighbours_round

	def init_pos(self, x, y):
		self.index_x, self.index_y = x, y
		self.left = x * Grid.grid_size_w
		self.top = y * Grid.grid_size_h
		self.right = (x + 1) * Grid.grid_size_w
		self.bottom = (y + 1) * Grid.grid_size_h
		self.left_top.x, self.left_top.y = self.left, self.top
		self.right_bottom.x, self.right_bottom.y = self.right, self.bottom
		self.grid_pos.x, self.grid_pos.y = (x + 0.5) * Grid.grid_size_w, (y + 0.5) * Grid.grid_size_h

	def init_neighbours_square(self, grids, grid_num_w, grid_num_h):
		x, y = self.index_x, self.index_y
		gird_in_vision = int(const.VISION_SIZE / const.GRID_SIZE) + 1
		for i in range(1, gird_in_vision):
			neighbours = []
			for xx in range(-i, i + 1):
				xxx = x + xx
				if xxx < 0 or xxx >= grid_num_w:
					continue

				yyy = y - i
				if yyy >= 0:
					grid = grids[xxx][yyy]
					neighbours.append(grid)
				yyy = y + i
				if yyy < grid_num_h:
					grid = grids[xxx][yyy]
					neighbours.append(grid)
			for yy in range(-i + 1, i):
				yyy = y + yy
				if yyy < 0 or yyy >= grid_num_h:
					continue

				xxx = x - i
				if xxx >= 0:
					grid = grids[xxx][yyy]
					neighbours.append(grid)
				xxx = x + i
				if xxx < grid_num_w:
					grid = grids[xxx][yyy]
					neighbours.append(grid)

			self.grid_neighbours.append((i, neighbours))

	def init_neighbours_round(self, grids, grid_num_w, grid_num_h):
		vision_size = const.VISION_SIZE
		merge_precision = 1.0 / MERGE_PRECISION

		if Grid.neighbour_offset_groups is None:
			grid_in_vision_w = int(vision_size / Grid.grid_size_w) + 1
			grid_in_vision_h = int(vision_size / Grid.grid_size_h) + 1
			groups = {}
			for di in range(-grid_in_vision_w + 1, grid_in_vision_w):
				for dj in range(-grid_in_vision_h + 1, grid_in_vision_h):
					if di == 0 and dj == 0:
						continue
					dx = di * Grid.grid_size_w
					dy = dj * Grid.grid_size_h
					dis2 = dx * dx + dy * dy
					if dis2 <= vision_size * vision_size:
						key = int(dis2 * merge_precision)
						groups.setdefault(key, []).append((di, dj))
			Grid.neighbour_offset_groups = sorted(groups.items(), key=lambda x: x[0])

		neighbours = []
		for key, offset_list in Grid.neighbour_offset_groups:
			group = []
			for di, dj in offset_list:
				x = self.index_x + di
				y = self.index_y + dj
				if x < 0 or y < 0 or x >= grid_num_w or y >= grid_num_h:
					continue
				group.append(grids[x][y])
			if group:
				neighbours.append((key, group))
		self.grid_neighbours = neighbours

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
			actor.draw_color = const.WHITE

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
