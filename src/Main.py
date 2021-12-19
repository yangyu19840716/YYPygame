# -*- coding:utf-8 -*-

import time
from Game import Game
from Core.Profiler import Profiler

profiler = Profiler()
profiler.label = time.strftime("%Y%m%d%H%M%S", time.localtime())
profiler.start()

game = Game()
game.run()

profiler.stop()
