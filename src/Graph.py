# -*- coding:utf-8 -*-

import pygame
import Const


class Graph(object):
    font_size = 22
    font = pygame.font.Font(None, font_size)

    @staticmethod
    def draw_circle(r, pos=(0, 0),  w=1, color=(255, 255, 255)):
        pygame.draw.circle(Const.SCREEN, color, pos, r, w)

    @staticmethod
    def set_font_size(size):
        Graph.font_size = size
        Graph.font = pygame.font.Font(None, size)

    @staticmethod
    def draw_text(text, pos=(0, 0), color=(255, 255, 255)):
        image = Graph.font.render(text, True, color)
        Const.SCREEN.blit(image, pos)
