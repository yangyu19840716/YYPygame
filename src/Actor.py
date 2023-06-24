# -*- coding:utf-8 -*-

import random

from Core import Const, Utility
from Core.Graph import Graph
from Core.Math import *
# from RuleManager import RuleManager

SIZE = 4  							# 单位：pixel
PICK_SIZE_EXTEND = 2				# 单位：pixel
MAX_SPEED = 100						# 单位：pixel / s
SPEED_ACC_RATE = 50  				# 单位：pixel / s2
# RAD_ACC_RATE = 0.1  				# 单位：rad / s
# MAX_SPEED_ACC = MAX_SPEED  		# 单位：pixel / s2


class Actor:
	ACTOR_ID = 0
	RAND_SPEED_DIR = False

	def __init__(self):
		self.name = Actor.ACTOR_ID
		Actor.ACTOR_ID += 1
		
		self.actor_pos = Vector2()
		self.actor_pos.x, self.actor_pos.y = random.randint(0, Const.WIDTH), random.randint(0, Const.HEIGHT)
		self.grid_x = self.grid_y = 0
		
		self.actor_color = Utility.rand_color()
		self.actor_dir_rad = 0  			# random.uniform(0.0, Const.DOUBLE_PI)
		self.actor_speed = 0  				# random.uniform(0.0, self.max_speed)
		self.actor_speed_dir = Vector2()  	# self.speed * math.cos(self.dir_rad), self.speed * math.sin(self.dir_rad)
		# self.speed_dir_n = Vector2()		# speed_dir 垂直方向，为了添加随机波动
		self.target_pos = None
		self.rand_target()

		self.rules = []
		self.actor_neighbours = []
		self.nearest_neighbour = None
		self.followers = []  		# grid list, 被 leader 指定为 nearest_neighbour, 改变 grid 的时候重置
		self.is_leader = False  	# 被 grid 指定为 leader_actor, 改变 grid 的时候重置
		self.grid = None
		self.dirty = True  			# 位置改变会 dirty
		self.picked = False
		self.draw_pos = Vector2()
		self.draw_pos.x, self.draw_pos.y = self.actor_pos.x, self.actor_pos.y
		self.draw_color = self.actor_color
		self.draw_size = SIZE

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
	def update_speed(self, length_squared):
		dis2_f = 0.04
		speed_f = 0.5

		if self.actor_speed > 0 and length_squared / (self.actor_speed * self.actor_speed) < dis2_f:
			self.actor_speed *= speed_f
		else:
			self.actor_speed += SPEED_ACC_RATE * Const.ENGINE.frame_time

		# self.speed += random.uniform(0, SPEED_ACC_RATE * dt)
		if self.actor_speed > MAX_SPEED:
			self.actor_speed = MAX_SPEED

	def update(self):
		dt = Const.ENGINE.frame_time

		self.actor_pos.x = self.actor_pos.x + self.actor_speed_dir.x * self.actor_speed * dt
		self.actor_pos.y = self.actor_pos.y + self.actor_speed_dir.y * self.actor_speed * dt
		dx = self.actor_pos.x - self.draw_pos.x
		dy = self.actor_pos.y - self.draw_pos.y
		d2 = dx * dx + dy * dy

		target_dir = self.target_pos - self.actor_pos
		dis2 = target_dir.length_squared()

		if d2 > dis2:
			self.draw_pos.x, self.draw_pos.y = self.actor_pos.x, self.actor_pos.y = self.target_pos.x, self.target_pos.y
			self.actor_speed_dir.x = self.actor_speed_dir.y = 0
			# self.speed_dir_n.x = self.speed_dir_n.y = 0
			self.actor_speed = 0
			self.target_pos = None
			self.dirty = True

			self.rand_target()
			return

		if self.actor_pos.x > Const.WIDTH:
			self.actor_pos.x -= int(self.actor_pos.x / Const.WIDTH) * Const.WIDTH
		elif self.actor_pos.x < 0:
			self.actor_pos.x += (int(-self.actor_pos.x / Const.WIDTH) + 1) * Const.WIDTH
		if self.actor_pos.y > Const.HEIGHT:
			self.actor_pos.y -= int(self.actor_pos.y / Const.HEIGHT) * Const.HEIGHT
		elif self.actor_pos.y < 0:
			self.actor_pos.y += (int(-self.actor_pos.y / Const.HEIGHT) + 1) * Const.HEIGHT

		if d2 > 0.5:
			# 小于一个像素不移动
			self.dirty = True
			self.draw_pos.x, self.draw_pos.y = self.actor_pos.x, self.actor_pos.y

		if dis2 > 0:
			if Actor.RAND_SPEED_DIR:
				self.rand_speed(target_dir)
			self.update_speed(dis2)

	def in_actor(self, x, y):
		size = SIZE + PICK_SIZE_EXTEND
		if self.actor_pos.x - size < x < self.actor_pos.x + size and self.actor_pos.y - size < y < self.actor_pos.y + size:
			return True
		else:
			return False

	def become_a_leader(self, is_leader):
		self.is_leader = is_leader

	def pick(self):
		self.picked = True

	def unpick(self):
		self.picked = False

	def draw(self):
		w = 2
		if self.is_leader:
			w = 4
		Graph.draw_circle(self.draw_pos, self.draw_size, w, self.draw_color)

	def get_neighbours_from_grid(self):
		neighbours = list(self.grid.actors_in_grid)
		for neighbour_grids in self.grid.grid_neighbours:
			for neighbour_grid in neighbour_grids[1]:
				neighbours.extend(neighbour_grid.actors_in_grid)

		return neighbours, self.get_nearest_from_grid()

	def get_nearest_from_grid(self):
		if self.is_leader:
			nearest = self.nearest_neighbour
		else:
			nearest = self.grid.leader_actor
		return nearest
