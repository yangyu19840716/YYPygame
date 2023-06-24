# -*- coding:utf-8 -*-

import time
from Core import Const
from Core.Graph import Graph

# ======================================= show_fps ==========================================
FPS_AVG_FRAME_NUM = 10  # FPS 多少帧刷新一次。 取均值。
FPS_LINE = 0
MSG_LINE = 1

_crt_frame = 0
_last_frame_time = 0
_frames_time = 0


def show_fps():
	global _crt_frame, _last_frame_time, _frames_time
	_crt_frame += 1
	crt_frame = _crt_frame % FPS_AVG_FRAME_NUM
	if crt_frame == 1:
		t = time.time()
		_frames_time = t - _last_frame_time
		_last_frame_time = t

	Graph.draw_line_text("AVG FPS: %.2f" % (FPS_AVG_FRAME_NUM / float(_frames_time)), FPS_LINE)


def show_msg():
	global DIRTY_GRID_FRAME, FLUSHING_GRID
	Graph.draw_line_text("Debug: DIRTY GRID %d" % FLUSHING_GRID, MSG_LINE)


def show_debug_text():
	show_fps()
	show_msg()


# ======================================= show_neighbours ==========================================
NEIGHBOURS_COLOR = (222, 222, 222)
NEAREST_NEIGHBOUR_COLOR = (222, 22, 22)
VISION_SIZE_COLOR = (22, 222, 22)
TARGET_COLOR = (22, 22, 222)


def show_neighbours(actor):
	Graph.draw_circle(actor.actor_pos, Const.VISION_SIZE, color=VISION_SIZE_COLOR)

	neighbours = actor.get_neighbours_from_grid()
	if neighbours:
		for neighbour in neighbours[1:]:
			Graph.draw_line(actor.actor_pos, neighbour.actor_pos, 2, NEIGHBOURS_COLOR)

		# 最后画这个防止被覆盖
		Graph.draw_line(actor.actor_pos, neighbours[0].actor_pos, 2, NEAREST_NEIGHBOUR_COLOR)


def show_target(actor):
	if actor.target_pos:
		Graph.draw_line(actor.actor_pos, actor.target_pos, 2, TARGET_COLOR)


# ======================================= show_grid ==========================================
GRID_LINE_COLOR = (44, 44, 188)
NEIGHBOUR_GRID_COLOR = (111, 111, 11)
DIRTY_GRID_COLOR = (111, 22, 22)
DIRTY_GRID_FRAME = []
FLUSH_TIME = 30
FLUSHING_GRID = 0


def add_dirty_grid(grid_list):
	global DIRTY_GRID_FRAME, FLUSH_TIME, FLUSHING_GRID
	FLUSHING_GRID = len(grid_list)
	DIRTY_GRID_FRAME.append(list(grid_list))
	if len(DIRTY_GRID_FRAME) > FLUSH_TIME:
		DIRTY_GRID_FRAME.pop(0)


def show_grid_line(scene, grid_size_w, grid_size_h):
	for i in range(scene.grid_num_w):
		pos_x = i * grid_size_w
		Graph.draw_line_xy(pos_x, 0, pos_x, scene.map_h, color=GRID_LINE_COLOR)
	for j in range(scene.grid_num_h):
		pos_y = j * grid_size_h
		Graph.draw_line_xy(0, pos_y, scene.map_w, pos_y, color=GRID_LINE_COLOR)


def show_vision_grid(scene):
	actor = scene.picked_actor
	grid = scene.picked_grid
	if actor:
		grid = actor.grid

	if grid:
		Graph.draw_rect_xy(
			grid.left_top.x, grid.left_top.y, grid.grid_size_h, grid.grid_size_w, color=NEIGHBOUR_GRID_COLOR)

		i = total = len(grid.grid_neighbours)
		for neighbours in grid.grid_neighbours:
			i -= 1.0
			color = (NEIGHBOUR_GRID_COLOR[0] * (i / total), NEIGHBOUR_GRID_COLOR[1] * (i / total), NEIGHBOUR_GRID_COLOR[2])
			for neighbour in neighbours[1]:
				Graph.draw_rect_xy(
					neighbour.left_top.x, neighbour.left_top.y, neighbour.grid_size_h, neighbour.grid_size_w,
					color=color)


def show_dirty_grid():
	global DIRTY_GRID_FRAME, DIRTY_GRID_COLOR
	for index, grid_frame in enumerate(DIRTY_GRID_FRAME):
		color = (DIRTY_GRID_COLOR[0] * index / FLUSH_TIME, DIRTY_GRID_COLOR[1], DIRTY_GRID_COLOR[2])
		for grid in grid_frame:
			Graph.draw_rect_xy(
				grid.left_top.x, grid.left_top.y, grid.grid_size_h, grid.grid_size_w,
				color=color)


def show_grid(scene, grid_size_w, grid_size_h):
	if not Const.ENGINE.is_pause:
		return

	show_grid_line(scene, grid_size_w, grid_size_h)
	show_vision_grid(scene)
	# show_dirty_grid()
