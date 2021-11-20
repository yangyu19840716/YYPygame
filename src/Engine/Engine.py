# -*- coding:utf-8 -*-

import time
import pygame
from Engine import Const
from Engine.Singleton import Singleton
from Engine.Graph import Graph


class Engine(Singleton):
	def __init__(self):
		super(Engine, self).__init__()

		self.screen = None
		self.screen_width = Const.SCREEN_W
		self.screen_height = Const.SCREEN_H
		self.bg_color = (0, 0, 0)
		self.crt_frame = 0
		self.crt_time = self.last_time = time.time()
		self.frame_time = 0.0
		self.keys_up = None
		self.mouse_keys_up = None
		self.fps_clock = None
		self.frame_lock = 0
		self.is_pause = False
		self.pick = None
		self.inited = False

		# 实际上执行的函数, Game 给出的函数, 默认空函数
		self._logic = self.logic_tick = self.logic
		self._draw = self.draw_tick = self.draw

		self._lock_fps = self.fps_clock_tick

	def init(self):
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

		# self.screen.fill(self.bg_color)

		Const.ENGINE = self
		Const.SCREEN = self.screen

		self._logic = self.logic_tick
		self._draw = self.draw_tick
		if self.frame_lock:
			self.fps_clock = pygame.time.Clock()
			self._lock_fps = self.fps_clock.tick

		self.inited = True

	def logic(self, dt):
		pass

	def draw(self, dt):
		pass

	def fps_clock_tick(self, fps):
		pass

	def pause_or_resume_game(self):
		if self.is_pause:
			self.resume()
		else:
			self.pause()

	def pause(self):
		self.is_pause = True
		self._logic = self.logic  # 空函数

	def resume(self):
		self.is_pause = False
		self._logic = self.logic_tick

	def loop(self):
		while True:
			crt_t = time.time()
			frame_time = crt_t - self.last_time
			self.last_time = crt_t
			crt_frame = self.crt_frame % Const.FPS_AVG_FRAME_NUM
			self.crt_frame += 1

			if crt_frame == 0:
				crt_time = crt_t
				self.frame_time = crt_time - self.crt_time
				self.crt_time = crt_time

			if pygame.event.get(pygame.QUIT):
				break

			self.keys_up = pygame.event.get(pygame.KEYUP)
			self.mouse_keys_up = pygame.event.get(pygame.MOUSEBUTTONUP)

			# 按键处理，响应up防止重复触发。
			for event in Engine.instance.keys_up:
				if event.key == pygame.K_SPACE:
					self.pause_or_resume_game()

			# 鼠标处理
			self.pick = None
			for event in Engine.instance.mouse_keys_up:
				if event.button == Const.L_MOUSE_BUTTON:
					self.pick = event.pos

			self._logic(frame_time)

			self.screen.fill(self.bg_color)
			self._draw()
			Graph.draw_text("AVG FPS: %.2f" % (Const.FPS_AVG_FRAME_NUM / self.frame_time))
			pygame.display.flip()

			self._lock_fps(self.frame_lock)

		pygame.quit()
