# -*- coding:utf-8 -*-

import os
import math

PROFILE = False

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (64, 64, 64)

DOUBLE_PI = 2 * math.pi

SCREEN_W, SCREEN_H = 800, 600
CENTER_X, CENTER_Y = SCREEN_W * 0.5, SCREEN_H * 0.5
WIDTH, HEIGHT = SCREEN_W, SCREEN_H
GRID_SIZE = 30
VISION_SIZE = 120

# Path configuration
ROOT_PATH = os.getcwd() + '/'
RES_PATH = os.path.join(ROOT_PATH, 'res')
TMP_PATH = os.path.join(ROOT_PATH, 'tmp')
