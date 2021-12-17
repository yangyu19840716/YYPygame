# -*- coding:utf-8 -*-

import pygame
from Core import Const

DRAW_LINE_TEXT_OFFSET_X = 5
DRAW_LINE_TEXT_OFFSET_Y = 2


class Graph(object):
	font_size = 22
	font = pygame.font.Font(None, font_size)

	@staticmethod
	def draw_rect(x, y, w, h, color=Const.WHITE):
		pygame.draw.rect(Const.SCREEN, color, (x, y, w, h))

	@staticmethod
	def draw_circle(pos_x, pos_y, r, w=1, color=Const.WHITE):
		pygame.draw.circle(Const.SCREEN, color, (pos_x, pos_y), r, w)

	@staticmethod
	def draw_line(pos1_x, pos1_y, pos2_x, pos2_y, w=1, color=Const.WHITE):
		pygame.draw.line(Const.SCREEN, color, (pos1_x, pos1_y), (pos2_x, pos2_y), w)

	@staticmethod
	def set_font_size(size):
		Graph.font_size = size
		Graph.font = pygame.font.Font(None, size)

	@staticmethod
	def draw_text(text, pos_x=0, pos_y=0, color=Const.WHITE):
		image = Graph.font.render(text, True, color)
		Const.SCREEN.blit(image, (pos_x, pos_y))

	@staticmethod
	def draw_line_text(text, line=0, color=Const.WHITE):
		image = Graph.font.render(text, True, color)
		y = DRAW_LINE_TEXT_OFFSET_Y + line * Graph.font.get_linesize()
		Const.SCREEN.blit(image, (DRAW_LINE_TEXT_OFFSET_X, y))
