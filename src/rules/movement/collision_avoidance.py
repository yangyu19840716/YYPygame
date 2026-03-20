# -*- coding:utf-8 -*-

from typing import Any
from ..core import BaseRule, register_rule
from core.math import Vector2


class CollisionAvoidanceRule(BaseRule):
	"""
	碰撞避免规则
	让Actor避免与其他Actor发生碰撞
	"""
	
	COLLISION_AVOIDANCE_DISTANCE = 15
	COLLISION_AVOIDANCE_FORCE = 0.8
	
	def __init__(self):
		super().__init__()
		self.set_priority(10)
		self.add_condition(self._is_not_leader)
	
	def _is_not_leader(self, owner: Any) -> bool:
		return not owner.is_leader
	
	def execute(self, owner: Any, *args, **kwargs) -> Any:
		neighbours = owner.get_neighbours_from_grid()
		avoidance_vec = Vector2(0, 0)
		
		for other in neighbours:
			if other == owner:
				continue
			
			vec = owner.actor_pos - other.actor_pos
			distance = vec.length()
			
			if distance < self.COLLISION_AVOIDANCE_DISTANCE and distance > 0:
				avoidance_force = (self.COLLISION_AVOIDANCE_DISTANCE - distance) / self.COLLISION_AVOIDANCE_DISTANCE
				avoidance_vec += vec.normalize() * avoidance_force * self.COLLISION_AVOIDANCE_FORCE
		
		if avoidance_vec.length_squared() > 0.01 and owner.actor_speed > 0:
			normalized_vec = avoidance_vec.normalize()
			owner.set_speed_vec(normalized_vec * owner.actor_speed)
			return normalized_vec.x * owner.actor_speed, normalized_vec.y * owner.actor_speed


register_rule(CollisionAvoidanceRule(), tags=['MOVE', 'COLLISION'])