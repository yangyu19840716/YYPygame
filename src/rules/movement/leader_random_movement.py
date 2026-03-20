# -*- coding:utf-8 -*-

from typing import Any
from ..core import BaseRule, register_rule


class LeaderRandomMovementRule(BaseRule):
	"""
	Leader随机移动规则
	让Leader以随机方式移动，定期改变方向
	"""
	
	LEADER_DIR_CHANGE_INTERVAL = 2.0
	
	def __init__(self):
		super().__init__()
		self.set_priority(0)
	
	def execute(self, owner: Any, *args, **kwargs) -> Any:
		if not hasattr(owner, 'leader_dir_change_timer'):
			owner.leader_dir_change_timer = 0
		
		owner.leader_dir_change_timer += 1
		
		if owner.leader_dir_change_timer >= self.LEADER_DIR_CHANGE_INTERVAL * 60:
			owner.leader_dir_change_timer = 0
			owner.rand_target()
		
		if owner.target_pos:
			vec = owner.target_pos - owner.actor_pos
			if vec.length() > 1 and owner.actor_speed > 0:
				normalized_vec = vec.normalize()
				speed_vec = normalized_vec * owner.actor_speed
				owner.set_speed_vec(speed_vec)
				return speed_vec.x, speed_vec.y


def is_leader(owner: Any) -> bool:
	return owner.is_leader


register_rule(LeaderRandomMovementRule(), tags=['MOVE', 'LEADER'])