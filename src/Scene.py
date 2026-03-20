# -*- coding:utf-8 -*-

import random

from core import const
from actor import Actor
from core.singleton import Singleton
from core.engine import Engine
from grid import Grid


class Scene(Singleton):
	def __init__(self):
		super(Scene, self).__init__()

		self.map_w = const.WIDTH
		self.map_h = const.HEIGHT

		# 为了让格子大小是整型，多加了一行一列
		self.grid_num_w = int(const.WIDTH / const.GRID_SIZE) + 1
		self.grid_num_h = int(const.HEIGHT / const.GRID_SIZE) + 1

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

		self.actor_num = const.ACTOR_NUM
		self.actors = []
		for i in range(self.actor_num):
			actor = Actor()
			if actor.is_leader:
				actor.rules.append('LeaderRandomMovementRule')
			else:
				actor.rules.append('FollowNearestLeaderRule')
				actor.rules.append('CollisionAvoidanceRule')
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

			if grid.assistant_actor:
				grid.assistant_actor.is_assistant = False

			leader_in_grid = None
			for actor in grid.actors_in_grid:
				if actor.is_leader:
					leader_in_grid = actor
					break
			
			if leader_in_grid:
				grid.leader_actor = leader_in_grid
			else:
				grid.leader_actor = None

			if actor_num > 1:
				non_leader_actors = [actor for actor in grid.actors_in_grid if actor != grid.leader_actor]
				if non_leader_actors:
					center = grid.grid_pos
					sorted_non_leaders = sorted(non_leader_actors, key=lambda a: (a.actor_pos - center).length_squared())
					grid.assistant_actor = sorted_non_leaders[0]
					grid.assistant_actor.is_assistant = True
				else:
					grid.assistant_actor = None
			else:
				grid.assistant_actor = None

		from core.engine import DebugModule
		DebugModule and DebugModule.DebugDraw.add_dirty_grid(self.grid_to_update)
		self.grid_to_update = []

	def cancel(self):
		if self.picked_actor:
			self.picked_actor.unpick()

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
		from core.engine import DebugModule
		DebugModule and DebugModule.DebugDraw.show_grid(self, Grid.grid_size_w, Grid.grid_size_h)

		for actor in self.actors:
			actor.draw()

		if DebugModule:
			if self.picked_actor:
				DebugModule.DebugDraw.show_neighbours(self.picked_actor)
				DebugModule.DebugDraw.show_target(self.picked_actor)
