# -*- coding:utf-8 -*-

import pygame
from core import const

DRAW_LINE_TEXT_OFFSET_X = 5
DRAW_LINE_TEXT_OFFSET_Y = 2


class Graph:
	font_size = 22
	font = None
	screen = None

	@staticmethod
	def init(screen):
		Graph.screen = screen
		Graph.font = pygame.font.Font(None, Graph.font_size)

	@staticmethod
	def draw_rect_xy(x, y, w, h, color=const.WHITE):
		pygame.draw.rect(Graph.screen, color, (x, y, w, h))

	@staticmethod
	def draw_rect(pos1, pos2, color=const.WHITE):
		dis = (pos2 - pos1)
		pygame.draw.rect(Graph.screen, color, (pos1.x, pos1.y, dis.x, dis.y))

	@staticmethod
	def draw_circle_xy(pos_x, pos_y, r, w=1, color=const.WHITE):
		pygame.draw.circle(Graph.screen, color, (pos_x, pos_y), r, w)

	@staticmethod
	def draw_circle(pos, r, w=1, color=const.WHITE):
		pygame.draw.circle(Graph.screen, color, pos, r, w)

	@staticmethod
	def draw_line_xy(pos1_x, pos1_y, pos2_x, pos2_y, w=1, color=const.WHITE):
		pygame.draw.line(Graph.screen, color, (pos1_x, pos1_y), (pos2_x, pos2_y), w)

	@staticmethod
	def draw_line(pos1, pos2, w=1, color=const.WHITE):
		pygame.draw.line(Graph.screen, color, pos1, pos2, w)

	@staticmethod
	def set_font_size(size):
		Graph.font_size = size
		Graph.font = pygame.font.Font(None, size)

	@staticmethod
	def draw_text_xy(text, pos_x=0, pos_y=0, color=const.WHITE):
		image = Graph.font.render(text, True, color)
		Graph.screen.blit(image, (pos_x, pos_y))

	@staticmethod
	def draw_text(text, pos, color=const.WHITE):
		image = Graph.font.render(text, True, color)
		Graph.screen.blit(image, pos)

	@staticmethod
	def draw_line_text(text, line=0, color=const.WHITE):
		image = Graph.font.render(text, True, color)
		y = DRAW_LINE_TEXT_OFFSET_Y + line * Graph.font.get_linesize()
		Graph.screen.blit(image, (DRAW_LINE_TEXT_OFFSET_X, y))
