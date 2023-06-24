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


def distance2(px1, py1, px2, py2):
	dx = px1 - px2
	dy = py1 - py2
	return dx * dx + dy * dy


def clamp(v, v_max, v_min):
	if v < v_min:
		v = v_min
	elif v > v_max:
		v = v_max
	return v


def clamp_repeat(v, v_max, v_min):
	d = v_max - v_min
	if v < v_min:
		v += int(v / d + 1) * d
	elif v > v_max:
		v -= int(v / d) * d
	return v
