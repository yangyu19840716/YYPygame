# -*- coding:utf-8 -*-

from Core import Const
from Core.Singleton import Singleton
from Core.Engine import Engine
from Scene import Scene

BG_COLOR = (64, 64, 64)
FPS = 0


class Game(Singleton):
	def __init__(self):
		super(Game, self).__init__()

		engine = Engine()
		engine.bg_color = BG_COLOR
		engine.init_display()

		self.scene = Scene()

		engine.logic_tick = self.scene.update
		engine.draw_tick = self.scene.draw
		engine.pick = self.scene.pick
		engine.cancel_callback = self.scene.cancel
		engine.frame_lock = FPS
		engine.init_ticks()
		# engine.pause()

		self.run = engine.loop
