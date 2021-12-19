# -*- coding:utf-8 -*-

from Core import Const, Utility
import random


MERGE_PRECISION = 0.01


class Grid(object):
	# 格子大小使用整型，提高格子计算效率
	grid_size_w = Const.GRID_SIZE
	grid_size_h = Const.GRID_SIZE
	gird_in_vision = int(Const.VISION_SIZE / Const.GRID_SIZE) + 1

	def __init__(self):
		self.index_x = None
		self.index_y = None
		self.left_top_pos_x = self.left_top_pos_y = 0
		self.right_bottom_pos_x = self.right_bottom_pos_y = 0
		self.pos_x = self.pos_y = 0
		self.actors = []
		self.neighbours = []  		# [(dis 1, grid list 1), (dis 2, grid list 2), ...] neighbour按距离分组
		self.leader_actor = None    # actor, nearest_neighbour 首选
		self.dirty = True			# actors 改变
		self.picked = False

		self.init_neighbours = self.init_neighbours_round

	def init_pos(self, x, y):
		self.index_x, self.index_y = x, y
		self.left_top_pos_x, self.left_top_pos_y = x * Grid.grid_size_w, y * Grid.grid_size_h
		self.right_bottom_pos_x, self.right_bottom_pos_y = (x + 1) * Grid.grid_size_w, (y + 1) * Grid.grid_size_h
		self.pos_x, self.pos_y = (x + 0.5) * Grid.grid_size_w, (y + 0.5) * Grid.grid_size_w,

	def init_neighbours_square(self):
		x, y = self.index_x, self.index_y
		grid_num_w, grid_num_h = Const.SCENE.grid_num_w, Const.SCENE.grid_num_h
		for i in range(1, Grid.gird_in_vision):
			neighbours = []
			for xx in range(-i, i + 1):
				xxx = x + xx
				if xxx < 0 or xxx >= grid_num_w:
					continue

				yyy = y - i
				if yyy >= 0:
					grid = Const.SCENE.get_grid(xxx, yyy)
					neighbours.append(grid)
				yyy = y + i
				if yyy < grid_num_h:
					grid = Const.SCENE.get_grid(xxx, yyy)
					neighbours.append(grid)
			for yy in range(-i + 1, i):
				yyy = y + yy
				if yyy < 0 or yyy >= grid_num_h:
					continue

				xxx = x - i
				if xxx >= 0:
					grid = Const.SCENE.get_grid(xxx, yyy)
					neighbours.append(grid)
				xxx = x + i
				if xxx < grid_num_w:
					grid = Const.SCENE.get_grid(xxx, yyy)
					neighbours.append(grid)

			self.neighbours.append((i, neighbours))

	def init_neighbours_round(self):
		scene = Const.SCENE
		vision_size = Const.VISION_SIZE
		grid_in_vision = Grid.gird_in_vision
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

				grid = scene.get_grid(x, y)
				dx = grid.pos_x - self.pos_x
				dy = grid.pos_y - self.pos_y
				dis2 = dx * dx + dy * dy
				if dis2 <= vision2:
					key_dis = int(dis2 * merge_precision)
					neighbour_list = neighbours.get(key_dis, None)
					if neighbour_list:
						neighbour_list.append(grid)
					else:
						neighbours[key_dis] = [grid]

		self.neighbours = Utility.sorted_dict_by_key(neighbours)

	@staticmethod
	def pos_to_grid(x, y):
		"""
			坐标转换到格子，x，y 需要是整型
		"""
		return int(x / Grid.grid_size_w), int(y / Grid.grid_size_h)

	def in_grid(self, x, y):
		return self.left_top_pos_x < x < self.right_bottom_pos_x and self.left_top_pos_y < y < self.right_bottom_pos_y

	def pick(self):
		self.picked = True

		for actor in self.actors:
			actor.draw_color = Const.WHITE

	def unpick(self):
		self.picked = False

		for actor in self.actors:
			actor.draw_color = actor.color

	def get_nearest_grid_actor(self):
		for neighbours in self.neighbours:
			neighbour_actors = []
			for neighbour in neighbours[1]:
				if neighbour.leader_actor:
					neighbour_actors.append(neighbour.leader_actor)
			if neighbour_actors:
				return random.choice(neighbour_actors)
		return None
