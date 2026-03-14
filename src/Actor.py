# -*- coding:utf-8 -*-

import random

from Core import Const, Utility
from Core.Graph import Graph
from Core.Math import *

SIZE = 4  							# 单位：pixel
PICK_SIZE_EXTEND = 2				# 单位：pixel
MAX_SPEED = 100						# 单位：pixel / s
SPEED_ACC_RATE = 50  				# 单位：pixel / s2
# RAD_ACC_RATE = 0.1  				# 单位：rad / s
# MAX_SPEED_ACC = MAX_SPEED  		# 单位：pixel / s2


class Actor:
	ACTOR_ID = 0
	# RAND_SPEED_DIR = False

	def __init__(self):
		self.name = Actor.ACTOR_ID
		Actor.ACTOR_ID += 1
		
		self.actor_pos = Vector2()
		self.actor_pos.x, self.actor_pos.y = random.randint(0, Const.WIDTH), random.randint(0, Const.HEIGHT)
		self.grid_x = self.grid_y = 0
		self.grid_pos = Vector2()
		self.update_grid_pos()
		
		self.actor_color = Const.GREEN  # 绿色
		self.actor_dir_rad = 0  			# random.uniform(0.0, Const.DOUBLE_PI)
		self.actor_speed = 0  				# random.uniform(0.0, self.max_speed)
		self.actor_speed_dir = Vector2()  	# self.speed * math.cos(self.dir_rad), self.speed * math.sin(self.dir_rad)
		# self.speed_dir_n = Vector2()		# speed_dir 垂直方向，为了添加随机波动
		self.target = None
		self.target_pos = None
		self.rand_target()

		self.rules = []
		self.actor_neighbours = []
		self.my_leader = None				# 通常为
		# self.grid_followers = []  		# grid list, 被 leader 指定为 nearest_neighbour, 改变 grid 的时候重置
		self.is_leader = False  			# 被 grid 指定为 leader_actor, 改变 grid 的时候重置
		self.is_assistant = False			# 被 grid 指定为 assistant_actor, 改变 grid 的时候重置
		self.grid = None
		self.actor_dirty = True  			# 位置改变会 dirty
		self.picked = False
		self.draw_pos = Vector2()
		self.draw_pos.x, self.draw_pos.y = self.actor_pos.x, self.actor_pos.y
		self.draw_color = self.actor_color
		self.draw_size = SIZE

	def update_grid_pos(self):
		self.grid_pos.x, self.grid_pos.y = self.actor_pos.x, self.actor_pos.y

	def set_speed_vec(self, speed_vec):
		self.actor_speed_dir = speed_vec.normalize()
		self.actor_speed = speed_vec.length()

	def rand_target(self):
		self.target_pos = Vector2()
		self.target_pos.x, self.target_pos.y = random.randint(0, Const.WIDTH), random.randint(0, Const.HEIGHT)
		self.actor_speed_dir = (self.target_pos - self.actor_pos).normalize()
		# self.speed_dir_n.x, self.speed_dir_n.y = self.speed_dir.y, self.speed_dir.x
		# self.speed = MAX_SPEED

	# def update_speed(self, dt):
	# 	if self.target_pos is None:
	# 		return
	#
	# 	if (self.target_pos - self.pos).length_squared() < MIN_VALUE:
	# 		self.target_pos.x, self.target_pos.y = random.randint(0, Const.WIDTH), random.randint(0, Const.HEIGHT)
	# 		return
	#
	# 	dspeed = MAX_SPEED_ACC * dt
	# 	target_dir = self.target_pos - self.pos
	# 	target_dir_n = target_dir.normalize()
	#
	# 	if self.speed > 0:
	# 		cos_a = target_dir_n.dot(self.speed_dir)
	# 	else:
	# 		cos_a = 1
	#
	# 	dis = target_dir.length()
	# 	if dis > self.dec_dis:
	# 		speed_dx = min(MAX_SPEED - cos_a * self.speed, dspeed)
	# 	else:
	# 		speed_dx = -min(cos_a * self.speed, dspeed)
	#
	# 	self.speed = cos_a * self.speed + speed_dx
	# 	self.speed_dir = target_dir_n
	#
	# 	if cos_a < 1:
	# 		sin_a = Math.sqrt(1 - cos_a * cos_a)
	# 		speed_dy = max(sin_a * self.speed - dspeed, 0)
	# 		if speed_dy > 0:
	# 			dv = Vector2()
	# 			dv.x = -target_dir_n.y
	# 			dv.y = target_dir_n.x
	# 			speed_dir = self.speed_dir + dv * speed_dy
	# 			self.speed = speed_dir.length()
	#  			self.speed_dir = speed_dir.normalize()
	#
	# 	self.speed += random.uniform(-SPEED_ACC_RATE, SPEED_ACC_RATE)
	# 	if self.speed > MAX_SPEED:
	# 		self.speed = MAX_SPEED
	# 	elif self.speed < 0:
	# 		self.speed = 0
	#
	# 	self.dir_rad += random.uniform(-RAD_ACC_RATE, RAD_ACC_RATE)
	# 	if self.dir_rad > Const.DOUBLE_PI:
	# 		self.dir_rad -= Const.DOUBLE_PI
	# 	elif self.dir_rad < 0:
	# 		self.dir_rad += Const.DOUBLE_PI
	#
	# 	self.speed_dir.x, self.speed_dir.y = Math.cos(self.dir_rad), Math.sin(self.dir_rad)

	def rand_speed(self, target_dir):
		# 添加速度随机波动
		self.actor_speed_dir = target_dir.normalize()
		rand_s = 1
		ds = random.uniform(-rand_s, rand_s)
		self.actor_speed_dir.x += ds * self.actor_speed_dir.y
		self.actor_speed_dir.y += ds * self.actor_speed_dir.x
		self.actor_speed_dir.normalize()

	# 根据目标距离更新速度，目标远加速，直到速度上限，距离近减速
	def update_speed(self, length_squared, dt):
		if self.actor_speed > 0 and length_squared < 0.04 * (self.actor_speed * self.actor_speed):
			self.actor_speed *= 0.5
		else:
			self.actor_speed += SPEED_ACC_RATE * dt

		if self.actor_speed > MAX_SPEED:
			self.actor_speed = MAX_SPEED

	def update(self, dt):
		if self.target_pos is None:
			return

		# Process rules
		from rules import RuleManager
		RuleManager.process(self, self.rules)

		# Calculate potential movement
		move_vec = self.actor_speed_dir * (self.actor_speed * dt)
		
		# Apply movement
		self.actor_pos += move_vec
		
		# Boundary wrap
		self.actor_pos.x %= Const.WIDTH
		self.actor_pos.y %= Const.HEIGHT

		# Update grid position
		self.update_grid_pos()

		# Target direction and distance
		target_dir = self.target_pos - self.actor_pos
		dis2 = target_dir.length_squared()

		# Check if reached target
		if move_vec.length_squared() > dis2:
			self.actor_pos = Vector2(self.target_pos)
			self.draw_pos = Vector2(self.target_pos)
			self.actor_speed_dir = Vector2(0, 0)
			self.actor_speed = 0
			self.target_pos = None
			self.actor_dirty = True
			self.rand_target()
			return

		# Fix: Use cumulative distance from last draw position instead of single-frame delta
		# This ensures movement is visible even at very high FPS where single-frame delta is tiny
		if (self.actor_pos - self.draw_pos).length_squared() > 0.04:
			self.draw_pos = Vector2(self.actor_pos)
			self.actor_dirty = True

		if dis2 > 0:
			self.update_speed(dis2, dt)

	def in_actor(self, x, y):
		size = SIZE + PICK_SIZE_EXTEND
		if self.actor_pos.x - size < x < self.actor_pos.x + size and self.actor_pos.y - size < y < self.actor_pos.y + size:
			return True
		else:
			return False

	def pick(self):
		self.picked = True

	def unpick(self):
		self.picked = False

	def draw(self):
		width = 4 if self.is_leader else 2
		color = Const.RED if self.is_leader else self.draw_color
		pygame.draw.circle(Graph.screen, color, self.draw_pos, self.draw_size, width)

	def get_neighbours_from_grid(self):
		neighbours = list(self.grid.actors_in_grid)
		main_grid_actor_num = len(neighbours)
		has_assistant = main_grid_actor_num > 1
		assistant_range = 0
		assistant_dis = None
		if len(self.grid.grid_neighbours):
			assistant_dis = self.grid.grid_neighbours[0]
		for neighbour_grids in self.grid.grid_neighbours:
			if assistant_dis == neighbour_grids[0]:
				assistant_range += len(neighbour_grids[1])
			for neighbour_grid in neighbour_grids[1]:
				neighbours.extend(neighbour_grid.actors_in_grid)

		return neighbours
