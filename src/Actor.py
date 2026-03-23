# -*- coding:utf-8 -*-

import random
from core import const, utility
from core.graph import Graph
from core.math import *
from config.actor_config import ActorConfig, ActorType


SIZE = 4
PICK_SIZE_EXTEND = 2
MAX_SPEED = 30
SPEED_ACC_RATE = 15


class Actor:
    ACTOR_ID = 0

    def __init__(self, actor_type: ActorType = ActorType.NORMAL):
        self.name = Actor.ACTOR_ID
        Actor.ACTOR_ID += 1
        
        self.actor_type = actor_type
        self.actor_pos = Vector2()
        self.actor_pos.x, self.actor_pos.y = random.randint(0, const.WIDTH), random.randint(0, const.HEIGHT)
        self.grid_x = self.grid_y = 0
        self.grid_pos = Vector2()
        self.update_grid_pos()
        
        self.actor_color = const.GREEN
        self.actor_dir_rad = 0
        self.actor_speed = 0
        self.actor_speed_dir = Vector2()
        self.target = None
        self.target_pos = None
        self.rand_target()

        self.rules = []
        self.actor_neighbours = []
        self.my_leader = None
        self.is_leader = (actor_type == ActorType.LEADER)
        self.is_assistant = False
        self.grid = None
        self.actor_dirty = True
        self.picked = False
        self.draw_pos = Vector2()
        self.draw_pos.x, self.draw_pos.y = self.actor_pos.x, self.actor_pos.y
        self.draw_color = self.actor_color
        self.draw_size = SIZE
        
        if self.is_leader:
            self.rules = ActorConfig.get_rules_for_type(ActorType.LEADER)
        else:
            self.rules = ActorConfig.get_rules_for_type(ActorType.NORMAL)

    def update_grid_pos(self):
        self.grid_pos.x, self.grid_pos.y = self.actor_pos.x, self.actor_pos.y

    def set_speed_vec(self, speed_vec):
        self.actor_speed_dir = speed_vec.normalize()
        self.actor_speed = speed_vec.length()

    def rand_target(self):
        self.target_pos = Vector2()
        self.target_pos.x, self.target_pos.y = random.randint(0, const.WIDTH), random.randint(0, const.HEIGHT)
        self.actor_speed_dir = (self.target_pos - self.actor_pos).normalize()

    def update(self, dt):
        if self.target_pos is None:
            return

        from rules import RuleRegistry
        registry = RuleRegistry()
        registry.execute_rules(self, rule_names=self.rules)

        move_vec = self.actor_speed_dir * (self.actor_speed * dt)
        
        self.actor_pos += move_vec
        
        self.actor_pos.x %= const.WIDTH
        self.actor_pos.y %= const.HEIGHT

        self.update_grid_pos()

        target_dir = self.target_pos - self.actor_pos
        dis2 = target_dir.length_squared()

        if move_vec.length_squared() > dis2:
            self.actor_pos = Vector2(self.target_pos)
            self.draw_pos = Vector2(self.target_pos)
            self.actor_speed_dir = Vector2(0, 0)
            self.actor_speed = 0
            self.target_pos = None
            self.actor_dirty = True
            self.rand_target()
            return

        if (self.actor_pos - self.draw_pos).length_squared() > 0.04:
            self.draw_pos = Vector2(self.actor_pos)
            self.actor_dirty = True

        if dis2 > 0:
            self.update_speed(dis2, dt)

    def update_speed(self, length_squared, dt):
        if self.actor_speed > 0 and length_squared < 0.04 * (self.actor_speed * self.actor_speed):
            self.actor_speed *= 0.5
        else:
            self.actor_speed += SPEED_ACC_RATE * dt

        if self.actor_speed > MAX_SPEED:
            self.actor_speed = MAX_SPEED

    def in_actor(self, x, y):
        size = SIZE + PICK_SIZE_EXTEND
        if self.actor_pos.x - size < x < self.actor_pos.x + size and self.actor_pos.y - size < y < self.actor_pos.y + size:
            return True
        else:
            return False

    def pick(self):
        self.picked = True

    def unpick(self):
        self.picked = False

    def draw(self):
        width = 4 if self.is_leader else 2
        color = const.RED if self.is_leader else self.draw_color
        pygame.draw.circle(Graph.screen, color, self.draw_pos, self.draw_size, width)

    def get_neighbours_from_grid(self):
        neighbours = list(self.grid.actors_in_grid)
        main_grid_actor_num = len(neighbours)
        has_assistant = main_grid_actor_num > 1
        assistant_range = 0
        assistant_dis = None
        if len(self.grid.grid_neighbours):
            assistant_dis = self.grid.grid_neighbours[0]
        for neighbour_grids in self.grid.grid_neighbours:
            if assistant_dis == neighbour_grids[0]:
                assistant_range += len(neighbour_grids[1])
            for neighbour_grid in neighbour_grids[1]:
                neighbours.extend(neighbour_grid.actors_in_grid)

        return neighbours