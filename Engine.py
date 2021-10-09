# -*- coding:utf-8 -*-

import pygame

# 确保一开始就被调用
pygame.init()

import time
import Const
from Graph import Graph


class Singleton(object):
    instance = None

    def __init__(self):
        Singleton.instance = self


class Engine(Singleton):
    AVG_FRAME_NUM = 100

    def __init__(self):
        super(Engine, self).__init__()

        self.screen = None
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (0, 0, 0)
        self.crt_frame = 0
        self.crt_time = self.last_time = time.time()
        self.frame_time = 0.0
        self.tick = None
        self.keys_up = None
        self.clock = None
        self.frame_lock = 0
        self.inited = False

    def init(self):
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.clock = pygame.time.Clock()

        # self.screen.fill(self.bg_color)

        Const.ENGINE = self
        Const.SCREEN = self.screen
        Const.WIDTH, Const.HEIGHT = self.screen_width, self.screen_height
        Const.CENTER_X, Const.CENTER_Y = self.screen_width * 0.5, self.screen_height * 0.5

        self.inited = True

    def loop(self):
        while True:
            if pygame.event.get(pygame.QUIT):
                break

            self.keys_up = pygame.event.get(pygame.KEYUP)
            crt_t = time.time()
            frame_time = crt_t - self.last_time
            self.last_time = crt_t
            crt_frame = self.crt_frame % Engine.AVG_FRAME_NUM
            if crt_frame == 0:
                crt_time = crt_t
                self.frame_time = crt_time - self.crt_time
                self.crt_time = crt_time
            self.crt_frame += 1

            self.screen.fill(self.bg_color)

            self.tick(frame_time)

            Graph.draw_text("AVG FPS: %.2f" % (Engine.AVG_FRAME_NUM / self.frame_time))
            pygame.display.flip()

            if self.frame_lock:
                self.clock.tick(self.frame_lock)

        pygame.quit()

