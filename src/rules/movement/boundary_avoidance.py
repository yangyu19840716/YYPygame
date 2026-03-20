# -*- coding:utf-8 -*-

"""
示例：添加新规则演示
展示如何在不修改任何现有代码的情况下添加新规则
"""

from typing import Any
from ..core import BaseRule, register_rule


class BoundaryAvoidanceRule(BaseRule):
	"""
	边界避免规则
	让Actor在接近屏幕边界时减速并转向
	"""
	
	BOUNDARY_MARGIN = 50
	SLOW_DOWN_FACTOR = 0.5
	TURN_AWAY_FORCE = 0.8
	
	def __init__(self):
		super().__init__()
		self.set_priority(8)  # 高优先级，仅次于碰撞避免
	
	def execute(self, owner: Any, *args, **kwargs) -> Any:
		from core import const
		
		x, y = owner.actor_pos.x, owner.actor_pos.y
		width, height = const.WIDTH, const.HEIGHT
		
		# 检查是否接近边界
		avoidance_vec = None
		
		if x < self.BOUNDARY_MARGIN:
			avoidance_vec = (1, 0)  # 向右
		elif x > width - self.BOUNDARY_MARGIN:
			avoidance_vec = (-1, 0)  # 向左
		elif y < self.BOUNDARY_MARGIN:
			avoidance_vec = (0, 1)  # 向下
		elif y > height - self.BOUNDARY_MARGIN:
			avoidance_vec = (0, -1)  # 向上
		
		if avoidance_vec:
			# 减速并转向
			owner.actor_speed *= self.SLOW_DOWN_FACTOR
			
			from core.math import Vector2
			current_dir = owner.actor_speed_dir
			new_dir = Vector2(*avoidance_vec)
			combined_dir = (current_dir + new_dir * self.TURN_AWAY_FORCE).normalize()
			owner.set_speed_vec(combined_dir * owner.actor_speed)
			
			return combined_dir.x * owner.actor_speed, combined_dir.y * owner.actor_speed


# 注册规则 - 仅需这一行即可完成注册！
register_rule(BoundaryAvoidanceRule(), tags=['MOVE', 'BOUNDARY', 'SAFETY'])