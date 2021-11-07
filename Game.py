# -*- coding:utf-8 -*-

from Engine import Engine
from Singleton import Singleton
from Scene import Scene


class Game(Singleton):
    def __init__(self):
        super(Game, self).__init__()

        engine = Engine()
        engine.bg_color = (64, 64, 64)
        engine.logic_tick = self.logic
        engine.draw_tick = self.draw
        # engine.frame_lock = 120
        engine.init()
        # engine.pause()

        self.run = engine.loop

        self.scene = Scene()

    def logic(self, dt):
        self.scene.update_actors(dt)
        self.scene.update_neighbours()

    def draw(self, dt):
        for actor in self.scene.actors:
            actor.draw()

    def pick(self):
        pass
