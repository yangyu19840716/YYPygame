# -*- coding:utf-8 -*-

from abc import ABC, abstractmethod
from typing import List, Callable, Any, Optional


class BaseRule(ABC):
	"""
	规则基类，所有规则必须继承此类
	"""
	
	def __init__(self):
		self.name = self.__class__.__name__
		self.priority = 0
		self.conditions: List[Callable[[Any], bool]] = []
		self.enabled = True
	
	@abstractmethod
	def execute(self, owner: Any, *args, **kwargs) -> Any:
		"""
		执行规则逻辑
		
		Args:
			owner: 规则的所有者对象
			*args: 位置参数
			**kwargs: 关键字参数
		
		Returns:
			规则执行结果
		"""
		pass
	
	def can_execute(self, owner: Any) -> bool:
		"""
		检查规则是否可以执行
		
		Args:
			owner: 规则的所有者对象
		
		Returns:
			True如果规则可以执行，否则False
		"""
		if not self.enabled:
			return False
		
		for condition in self.conditions:
			if not condition(owner):
				return False
		
		return True
	
	def add_condition(self, condition: Callable[[Any], bool]) -> 'BaseRule':
		"""
		添加执行条件
		
		Args:
			condition: 条件函数
		
		Returns:
			规则实例本身，支持链式调用
		"""
		self.conditions.append(condition)
		return self
	
	def set_priority(self, priority: int) -> 'BaseRule':
		"""
		设置规则优先级
		
		Args:
			priority: 优先级数值，越大优先级越高
		
		Returns:
			规则实例本身，支持链式调用
		"""
		self.priority = priority
		return self
	
	def enable(self) -> 'BaseRule':
		"""
		启用规则
		
		Returns:
			规则实例本身，支持链式调用
		"""
		self.enabled = True
		return self
	
	def disable(self) -> 'BaseRule':
		"""
		禁用规则
		
		Returns:
			规则实例本身，支持链式调用
		"""
		self.enabled = False
		return self
	
	def __repr__(self) -> str:
		return f"{self.__class__.__name__}(priority={self.priority}, enabled={self.enabled})"