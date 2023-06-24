# -*- coding:utf-8 -*-

import pygame
import time
from Core import Const
from Core.Singleton import Singleton

L_MOUSE_BUTTON = 1
M_MOUSE_BUTTON = 2
R_MOUSE_BUTTON = 3


def get_debug_module():
	try:
		import Debug
		Debug.import_all()
		return Debug
	except ImportError:
		print('DebugModule is disabled.')
		# import traceback
		# traceback.print_exc()
		return None


DebugModule = get_debug_module()


# noinspection PyUnusedLocal
def do_nothing(*args, **kwargs):
	pass


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
		self.mouse_start_pos = None
		self.mouse_end_pos = None
		self.fps_clock = None
		self.frame_lock = 0
		self.is_pause = False
		self.inited = False

		# 实际上执行的函数, Game 给出的函数, 默认空函数
		self._logic = self.logic_tick = do_nothing
		self._draw = self.draw_tick = do_nothing

		self._lock_fps = do_nothing
		self.pick = do_nothing

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

	def pause_or_resume(self):
		if self.is_pause:
			self.resume()
		else:
			self.pause()

	@staticmethod
	def cancel():
		scene = Const.SCENE
		if scene.picked_actor:
			scene.picked_actor.unpick()
			scene.picked_actor = None

		if scene.picked_grid:
			scene.picked_grid.unpick()
			scene.picked_grid = None

	def pause(self):
		self.is_pause = True
		self._logic = do_nothing

	def resume(self):
		self.is_pause = False
		self._logic = self.logic_tick

	def _input_process(self):
		keys_up = pygame.event.get(pygame.KEYUP)
		mouse_keys_down = pygame.event.get(pygame.MOUSEBUTTONDOWN)
		mouse_keys_up = pygame.event.get(pygame.MOUSEBUTTONUP)

		# 按键处理，响应up防止重复触发。
		for event in keys_up:
			if event.key == pygame.K_SPACE:
				self.pause_or_resume()
				return
			if event.key == pygame.K_ESCAPE:
				self.cancel()
				return

		# 鼠标处理
		if self.mouse_start_pos is None:
			for event in mouse_keys_down:
				if event.button == L_MOUSE_BUTTON:
					self.mouse_end_pos = None
					self.mouse_start_pos = event.pos

		if self.mouse_end_pos is None:
			for event in mouse_keys_up:
				if event.button == L_MOUSE_BUTTON:
					self.mouse_end_pos = event.pos
					self.mouse_start_pos = None
					self.pick()

	def loop(self):
		while True:
			if pygame.event.get(pygame.QUIT):
				break

			crt_t = time.time()
			self.frame_time = crt_t - self.last_time
			self.last_time = crt_t

			self._input_process()

			self._logic()

			self.screen.fill(self.bg_color)
			self._draw()
			DebugModule and DebugModule.DebugDraw.show_debug_text()
			pygame.display.flip()

			self._lock_fps(self.frame_lock)

		pygame.quit()
