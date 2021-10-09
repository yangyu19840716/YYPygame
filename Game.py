# -*- coding:utf-8 -*-

from Engine import Singleton, Engine
from Actor import Actor
import pygame


class Game(Singleton):
    def __init__(self):
        super(Game, self).__init__()

        self.actor_num = 100
        self.actors = []
        self.pause = False

        for i in range(self.actor_num):
            self.actors.append(Actor())

        engine = Engine()
        engine.bg_color = (64, 64, 64)
        engine.tick = self.tick
        engine.frame_lock = 60
        engine.init()

        self.run = engine.loop

    def tick(self, dt):
        for event in Engine.instance.keys_up:
            if event.key == pygame.K_SPACE:
                self.pause = not self.pause

        for actor in self.actors:
            if not self.pause:
                actor.action(dt)
            actor.draw()
