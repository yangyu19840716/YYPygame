# -*- coding:utf-8 -*-

import random


def rand_color():
	color = [0, 0, 0]
	color_min = 100
	color_max = 180
	for i in range(3):
		color[i] = random.randint(color_min, color_max)
	return color
