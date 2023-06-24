# -*- coding:utf-8 -*-

import random
from RuleManager import rule_def
from Actor import Actor


Tick = 1
AllStages = 2


# ========================= Conditions for Rules ==========================
# 每个condition 需要带一个 owner 参数。
def is_not_a_leader(owner):
	return not owner.is_leader


# ========================= Rules for actors ==============================
# 每条rule 需要带一个 actor 参数。

SPEED_ACC = 1.0
RAD_ACC = 0.1
MIN_ACTOR_DIS = 20


@rule_def(Actor, 'MOVE', property=1)
def random_move(actor):
	speed = actor.actor_speed + random.uniform(-SPEED_ACC, SPEED_ACC)
	speed_rad = actor.speed_rad + random.uniform(-RAD_ACC, RAD_ACC)
	return speed, speed_rad


@rule_def(Actor, 'MOVE', property=1)
def move_to_target(actor):
	return


@rule_def(Actor, 'MOVE', condition=[is_not_a_leader], exec=Tick)
def keep_distance(actor):
	if not actor.nearest_neighbour:
		return

	vec = actor.grid_pos - actor.nearest_neighbour.grid_pos
	dis = vec.length()
	new_speed_vec = vec.normalize()
	speed = MIN_ACTOR_DIS - dis
	new_speed_vec.x *= speed
	new_speed_vec.y *= speed
	actor.set_speed_vec(new_speed_vec)


@rule_def(Actor, 'ACTION', property=2)
def find_target(actor):
	pass
