# -*- coding:utf-8 -*-

import random

from Core import Const
from Actor import Actor
from Core.Singleton import Singleton
from Core.Engine import Engine, DebugModule
from Grid import Grid
import Rule
# from RuleManager import RuleManager


class Scene(Singleton):
	def __init__(self):
		super(Scene, self).__init__()

		Const.SCENE = self

		self.map_w = Const.WIDTH
		self.map_h = Const.HEIGHT

		# 为了让格子大小是整型，多加了一行一列
		self.grid_num_w = int(Const.WIDTH / Const.GRID_SIZE) + 1
		self.grid_num_h = int(Const.HEIGHT / Const.GRID_SIZE) + 1

		self.picked_actor = None
		self.picked_grid = None

		self.grid_to_update = []

		# Grid 二维数组
		self.grids = []
		for x in range(self.grid_num_w):
			self.grids.append([])
			for y in range(self.grid_num_h):
				grid = Grid()
				grid.init_pos(x, y)
				self.grids[x].append(grid)

		for x in range(self.grid_num_w):
			for y in range(self.grid_num_h):
				grid = self.grids[x][y]
				grid.init_neighbours()
				self.grid_to_update.append(grid)

		self.actor_num = Const.ACTOR_NUM
		self.actors = []
		for i in range(self.actor_num):
			actor = Actor()
			# actor.rules.append(Rule.keep_distance)
			actor.rules.append(Rule.move_to_target)
			self.actors.append(actor)

		for actor in self.actors:
			grid_x, grid_y = Grid.pos_to_grid(actor.actor_pos.x, actor.actor_pos.y)
			grid = self.grids[grid_x][grid_y]
			grid.actors_in_grid.append(actor)
			actor.grid = grid

	def get_grid(self, index_x, index_y):
		return self.grids[index_x][index_y]

	def update(self):
		self.update_actors()
		self.update_neighbours()

	def update_actors(self):
		# 更新 actor
		for actor in self.actors:
			actor.update()
			if not actor.dirty:
				continue

			x, y = int(actor.actor_pos.x / Grid.grid_size_w), int(actor.actor_pos.y / Grid.grid_size_h)
			grid = actor.grid
			new_grid = self.grids[x][y]
			if grid != new_grid:
				grid.actors_in_grid.remove(actor)
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
					actor.become_a_leader(False)

				new_grid.actors_in_grid.append(actor)
				if not new_grid.dirty:
					self.grid_to_update.append(new_grid)
					new_grid.dirty = True

				actor.grid = new_grid

			actor.dirty = False

	def update_neighbours(self):
		grid_to_update = []
		for grid in self.grid_to_update:
			actor_num = len(grid.actors_in_grid)
			if actor_num == 0:
				grid.leader_actor = None
				grid.dirty = False
				continue

			actor = None
			if not grid.leader_actor:
				index = random.choice(range(actor_num))
				grid.leader_actor = grid.actors_in_grid[index]
				grid.leader_actor.become_a_leader(True)
				grid.leader_actor.nearest_neighbour = None

				if actor_num > 1:
					idx = random.choice(range(actor_num - 1))
					if idx == index:
						actor = grid.actors_in_grid[-1]
					else:
						actor = grid.actors_in_grid[idx]

			if not actor:
				actor = grid.get_nearest_actor()

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
		grid = self.grids[index_x][index_y]
		grid.pick()
		self.picked_grid = grid

	def draw(self):
		DebugModule and DebugModule.DebugDraw.show_grid(self, Grid.grid_size_w, Grid.grid_size_h)

		for actor in self.actors:
			actor.draw()

		if DebugModule:
			if self.picked_actor:
				DebugModule.DebugDraw.show_neighbours(self.picked_actor)
				DebugModule.DebugDraw.show_target(self.picked_actor)
