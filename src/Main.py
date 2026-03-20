# -*- coding:utf-8 -*-

import time
from game import Game
from core.profiler import Profiler
from core import const


if __name__ == '__main__':
	profiler = None
	if const.PROFILE:
		profiler = Profiler(time.strftime("%Y%m%d%H%M%S", time.localtime()))

	profiler and profiler.start()

	game = Game()
	game.run()

	profiler and profiler.stop()
