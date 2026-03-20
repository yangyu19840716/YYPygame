# -*- coding:utf-8 -*-

"""
规则开发模板
复制此文件来创建新的规则
"""

from typing import Any
from ..core import BaseRule, register_rule


class YourRuleName(BaseRule):
	"""
	规则描述
	简要说明这个规则的作用和适用场景
	"""
	
	# 规则常量参数
	PARAMETER_1 = 100
	PARAMETER_2 = 0.5
	
	def __init__(self):
		super().__init__()
		
		# 设置规则优先级（数值越大优先级越高）
		self.set_priority(0)
		
		# 添加执行条件（可选）
		# self.add_condition(self._your_condition_function)
	
	def _your_condition_function(self, owner: Any) -> bool:
		"""
		自定义条件函数
		
		Args:
			owner: 规则的所有者对象
		
		Returns:
			True如果条件满足，否则False
		"""
		return True
	
	def execute(self, owner: Any, *args, **kwargs) -> Any:
		"""
		执行规则逻辑
		
		Args:
			owner: 规则的所有者对象
			*args: 位置参数
			**kwargs: 关键字参数
		
		Returns:
			规则执行结果（可选）
		"""
		
		# 在这里实现你的规则逻辑
		# 示例：
		# 1. 检查前置条件
		# 2. 执行主要逻辑
		# 3. 返回结果（如果需要）
		
		pass


# 注册规则
# tags参数用于分类管理规则，建议使用有意义的标签
register_rule(YourRuleName(), tags=['CATEGORY', 'SUBCATEGORY'])