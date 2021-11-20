# -*- coding:utf-8 -*-

from Engine.Singleton import Singleton
from Engine.Engine import Engine
from Scene import Scene


class Game(Singleton):
	def __init__(self):
		super(Game, self).__init__()

		engine = Engine()
		engine.bg_color = (64, 64, 64)
		engine.logic_tick = self.logic
		engine.draw_tick = self.draw
		# Engine.frame_lock = 120
		engine.init()
		# Engine.pause()

		self.run = engine.loop

		self.scene = Scene()

	def logic(self, dt):
		self.scene.update_actors(dt)
		self.scene.update_neighbours()

	def draw(self):
		for actor in self.scene.actors:
			actor.draw()

	def pick(self):
		pass
