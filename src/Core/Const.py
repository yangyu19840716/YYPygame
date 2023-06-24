# -*- coding:utf-8 -*-

import os
import math

PROFILE = False

WHITE = (255, 255, 255)

DOUBLE_PI = 2 * math.pi

SCREEN_W, SCREEN_H = 800, 600
CENTER_X, CENTER_Y = SCREEN_W * 0.5, SCREEN_H * 0.5
WIDTH, HEIGHT = SCREEN_W, SCREEN_H
GRID_SIZE = 25
VISION_SIZE = 60  # 单位: pixel
ACTOR_NUM = 100

ENGINE = None
SCREEN = None
SCENE = None
GAME = None

ROOT_PATH = os.getcwd() + '/'
RES_PATH = ROOT_PATH + 'res'
TMP_PATH = ROOT_PATH + 'tmp'
