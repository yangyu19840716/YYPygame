# -*- coding:utf-8 -*-

import random

from Core import Const
from Actor import Actor
from Core.Singleton import Singleton
from Core.Engine import Engine, DebugModule
from Grid import Grid


class Scene(Singleton):
	def __init__(self):
		super(Scene, self).__init__()

		Const.SCENE = self

		self.map_w = Const.WIDTH
		self.map_h = Const.HEIGHT

		# 为了让格子大小是整型， 多加了一行一列
		self.grid_num_w = int(Const.WIDTH / Const.GRID_SIZE) + 1
		self.grid_num_h = int(Const.HEIGHT / Const.GRID_SIZE) + 1

		self.size2 = Const.VISION_SIZE * Const.VISION_SIZE

		self.picked_actor = None
		self.picked_grid = None

		self.grid_to_update = []

		# Grid二维数组
		self.grids = []
		for x in range(self.grid_num_w):
			self.grids.append([])
			for y in range(self.grid_num_h):
				self.grids[x].append(Grid())

		for x in range(self.grid_num_w):
			for y in range(self.grid_num_h):
				grid = self.grids[x][y]
				self.grid_to_update.append(grid)
				grid.init_neighbours(x, y)

		self.actor_num = Const.ACTOR_NUM
		self.actors = []
		for i in range(self.actor_num):
			self.actors.append(Actor())

		for actor in self.actors:
			actor.grid_x, actor.grid_y = Grid.pos_to_grid(actor.pos_x, actor.pos_y)
			grid = self.get_grid(actor.grid_x, actor.grid_y)
			grid.actors.append(actor)

	def get_grid(self, index_x, index_y):
		return self.grids[index_x][index_y]

	def update(self):
		self.update_actors()
		self.update_neighbours()

	def update_actors(self):
		dt = Engine.instance.frame_time
		# 更新actor
		for actor in self.actors:
			actor.update(dt)
			if not actor.dirty:
				continue

			x, y = int(actor.pos_x / Grid.grid_size_w), int(actor.pos_y / Grid.grid_size_h)
			if actor.grid_x != x or actor.grid_y != y:
				grid = self.grids[actor.grid_x][actor.grid_y]
				grid.actors.remove(actor)
				if not grid.dirty:
					self.grid_to_update.append(grid)
					grid.dirty = True

				for follower in actor.followers:
					if not follower.leader_actor:
						continue

					follower.leader_actor.nearest_neighbour = None
					if follower.dirty:
						continue

					follower.dirty = True
					self.grid_to_update.append(follower)
				actor.followers = []

				if actor.is_leader:
					grid.leader_actor = None
					actor.is_leader = False

				grid = self.grids[x][y]
				grid.actors.append(actor)
				if not grid.dirty:
					self.grid_to_update.append(grid)
					grid.dirty = True

				actor.grid_x, actor.grid_y = x, y

			actor.dirty = False

	def update_neighbours(self):
		grid_to_update = []
		for grid in self.grid_to_update:
			actor_num = len(grid.actors)
			if actor_num == 0:
				grid.leader_actor = None
				grid.dirty = False
				continue

			actor = None
			if not grid.leader_actor:
				index = random.choice(range(actor_num))
				grid.leader_actor = grid.actors[index]
				grid.leader_actor.is_leader = True
				grid.leader_actor.nearest_neighbour = None

				if actor_num > 1:
					idx = random.choice(range(actor_num - 1))
					if idx == index:
						actor = grid.actors[-1]
					else:
						actor = grid.actors[idx]

			if not actor:
				actor = grid.get_nearest_grid_actor()

			if actor:
				grid.leader_actor.nearest_neighbour = actor
				actor.followers.append(grid)
				grid.dirty = False
			else:
				grid_to_update.append(grid)

		DebugModule and DebugModule.DebugDraw.add_dirty_grid(self.grid_to_update)
		self.grid_to_update = grid_to_update

	def pick(self):
		if not Engine.instance.is_pause:
			return

		if self.picked_actor:
			self.picked_actor.unpick()
			self.picked_actor = None

		if self.picked_grid:
			self.picked_grid.unpick()
			self.picked_grid = None

		pos_x, pos_y = Engine.instance.mouse_end_pos
		for actor in self.actors:
			if actor.in_actor(pos_x, pos_y):
				actor.pick()
				self.picked_actor = actor
				break

		if self.picked_actor:
			return

		index_x, index_y = Grid.pos_to_grid(pos_x, pos_y)
		grid = self.get_grid(index_x, index_y)
		grid.pick()
		self.picked_grid = grid

	def draw(self):
		DebugModule and DebugModule.DebugDraw.show_grid(self, Grid.grid_size_w, Grid.grid_size_h)

		for actor in self.actors:
			actor.draw()

		DebugModule and DebugModule.DebugDraw.show_neighbours(self.picked_actor)
