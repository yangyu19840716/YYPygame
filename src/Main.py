# -*- coding:utf-8 -*-

from Game import Game
from Engine.Profiler import Profiler

profiler = Profiler()
profiler.label = 'YY'
profiler.start()

game = Game()
game.run()

profiler.stop()
