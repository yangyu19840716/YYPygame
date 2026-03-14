# -*- coding:utf-8 -*-

import random

from Core import Const
from Actor import Actor
from Core.Singleton import Singleton
from Core.Engine import Engine
from Grid import Grid
from rules import Rule
# from rules.RuleManager import RuleManager


class Scene(Singleton):
	def __init__(self):
		super(Scene, self).__init__()

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
				grid.init_neighbours(self.grids, self.grid_num_w, self.grid_num_h)
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

	def update(self, dt):
		self.update_actors(dt)
		self.update_grids()

	def update_actors(self, dt):
		# 更新 actor
		for actor in self.actors:
			actor.update(dt)
			if not actor.actor_dirty:
				continue

			grid = actor.grid
			# Fast check: skip if still within current grid (using pre-calculated boundaries)
			if grid and grid.left < actor.actor_pos.x < grid.right and \
			   grid.top < actor.actor_pos.y < grid.bottom:
				# Even if within grid, we keep dirty=True so that draw_pos updates are respected
				continue

			# Calculate new grid index only when boundary is crossed
			x, y = Grid.pos_to_grid(actor.actor_pos.x, actor.actor_pos.y)
			new_grid = self.grids[x][y]
			
			if grid != new_grid:
				if grid:
					grid.actors_in_grid.remove(actor)
					if not grid.grid_dirty:
						self.grid_to_update.append(grid)
						grid.grid_dirty = True

				if actor.is_leader:
					grid.leader_actor = None
					actor.is_leader = False

				if actor.is_assistant:
					grid.assistant_actor = None
					actor.is_assistant = False

				new_grid.actors_in_grid.append(actor)
				if not new_grid.grid_dirty:
					self.grid_to_update.append(new_grid)
					new_grid.grid_dirty = True

				actor.grid = new_grid

			# Reset dirty flag after processing all logic for this frame
			actor.actor_dirty = False

	def update_grids(self):
		for grid in self.grid_to_update:
			grid.grid_dirty = False
			actor_num = len(grid.actors_in_grid)
			if actor_num == 0:
				grid.leader_actor = None
				grid.assistant_actor = None
				continue

			# Deterministic leader/assistant selection by proximity to grid center
			center = grid.grid_pos
			sorted_actors = sorted(grid.actors_in_grid, key=lambda a: (a.actor_pos - center).length_squared())
			# reset previous flags
			if grid.leader_actor:
				grid.leader_actor.is_leader = False
			if grid.assistant_actor:
				grid.assistant_actor.is_assistant = False
			grid.leader_actor = sorted_actors[0]
			grid.leader_actor.is_leader = True
			if actor_num > 1:
				grid.assistant_actor = sorted_actors[1]
				grid.assistant_actor.is_assistant = True
			else:
				grid.assistant_actor = None

		from Core.Engine import DebugModule
		DebugModule and DebugModule.DebugDraw.add_dirty_grid(self.grid_to_update)
		self.grid_to_update = []

	def cancel(self):
		if self.picked_actor:
			self.picked_actor.unpick()
			self.picked_actor = None

		if self.picked_grid:
			self.picked_grid.unpick()
			self.picked_grid = None

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
		from Core.Engine import DebugModule
		DebugModule and DebugModule.DebugDraw.show_grid(self, Grid.grid_size_w, Grid.grid_size_h)

		for actor in self.actors:
			actor.draw()

		if DebugModule:
			if self.picked_actor:
				DebugModule.DebugDraw.show_neighbours(self.picked_actor)
				DebugModule.DebugDraw.show_target(self.picked_actor)
