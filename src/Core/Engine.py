# -*- coding:utf-8 -*-

import pygame
import time
from Core import Const
from Core.Graph import Graph
from Core.Singleton import Singleton

L_MOUSE_BUTTON = 1
M_MOUSE_BUTTON = 2
R_MOUSE_BUTTON = 3


DebugModule = None

def ensure_debug_module():
	global DebugModule
	if DebugModule is None:
		try:
			import Debug
			Debug.import_all()
			DebugModule = Debug
		except (ImportError, AttributeError) as e:
			print(f'DebugModule is disabled: {e}')
			DebugModule = None


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
		self.cancel_callback = do_nothing

	def init_display(self):
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
		Graph.init(self.screen)

	def init_ticks(self):
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

	def pause(self):
		self.is_pause = True
		self._logic = do_nothing

	def resume(self):
		self.is_pause = False
		self._logic = self.logic_tick

	def _input_process(self):
		# Unified event processing to keep queue healthy at high FPS
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					self.pause_or_resume()
					return
				elif event.key == pygame.K_ESCAPE:
					self.cancel_callback()
					return
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == L_MOUSE_BUTTON:
					self.mouse_end_pos = None
					self.mouse_start_pos = event.pos
			elif event.type == pygame.MOUSEBUTTONUP:
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
			# Clamp dt to avoid extreme spikes/underflows at uncapped FPS
			if self.frame_time < 1e-6:
				self.frame_time = 1e-6
			elif self.frame_time > 0.05:
				self.frame_time = 0.05

			self._input_process()

			self._logic(self.frame_time)

			self.screen.fill(self.bg_color)
			self._draw()
			ensure_debug_module()
			DebugModule and DebugModule.DebugDraw.show_debug_text()
			pygame.display.flip()

			self._lock_fps(self.frame_lock)

		pygame.quit()
