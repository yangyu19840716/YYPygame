# -*- coding:utf-8 -*-

from typing import Any
from ..core import BaseRule, register_rule


class FollowNearestLeaderRule(BaseRule):
	"""
	跟随最近Leader规则
	让非Leader Actor移动到最近的Leader附近
	"""
	
	LEADER_MIN_DISTANCE = 30
	
	def __init__(self):
		super().__init__()
		self.set_priority(0)
		self.add_condition(self._is_not_leader)
	
	def _is_not_leader(self, owner: Any) -> bool:
		return not owner.is_leader
	
	def execute(self, owner: Any, *args, **kwargs) -> Any:
		neighbours = owner.get_neighbours_from_grid()
		leaders = [n for n in neighbours if n.is_leader and n != owner]
		
		if not leaders:
			return
		
		nearest_leader = min(leaders, key=lambda l: (l.actor_pos - owner.actor_pos).length_squared())
		owner.my_leader = nearest_leader
		
		vec = nearest_leader.actor_pos - owner.actor_pos
		distance = vec.length()
		
		if distance < self.LEADER_MIN_DISTANCE:
			return
		
		if owner.actor_speed <= 0:
			return
		
		normalized_vec = vec.normalize()
		speed_vec = normalized_vec * owner.actor_speed
		owner.set_speed_vec(speed_vec)
		return speed_vec.x, speed_vec.y


register_rule(FollowNearestLeaderRule(), tags=['MOVE', 'FOLLOW'])