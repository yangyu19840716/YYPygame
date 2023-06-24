# -*- coding:utf-8 -*-

import time
from Game import Game
from Core.Profiler import Profiler
from Core import Const


if __name__ == '__main__':
	profiler = None
	if Const.PROFILE:
		profiler = Profiler(time.strftime("%Y%m%d%H%M%S", time.localtime()))

	profiler and profiler.start()

	game = Game()
	game.run()

	profiler and profiler.stop()
