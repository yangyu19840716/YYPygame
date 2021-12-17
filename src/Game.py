# -*- coding:utf-8 -*-

from Core import Const
from Core.Singleton import Singleton
from Core.Engine import Engine
from Scene import Scene

BG_COLOR = (64, 64, 64)
FPS = 60.0


class Game(Singleton):
	def __init__(self):
		super(Game, self).__init__()

		Const.GAME = self
		engine = Engine()
		engine.bg_color = BG_COLOR

		self.scene = Scene()

		engine.logic_tick = self.scene.update
		engine.draw_tick = self.scene.draw
		engine.pick = self.scene.pick
		engine.frame_lock = FPS
		engine.init()
		# engine.pause()

		self.run = engine.loop
