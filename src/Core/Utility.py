# -*- coding:utf-8 -*-

import random


def rand_color():
	color = [0, 0, 0]
	color_min = 100
	color_max = 180
	for i in range(3):
		color[i] = random.randint(color_min, color_max)
	return color


def sorted_dict_by_key(unsort_dict):
	if not unsort_dict:
		return unsort_dict
	return [(k, unsort_dict[k]) for k in sorted(unsort_dict.keys())]
