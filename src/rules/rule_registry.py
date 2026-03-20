# -*- coding:utf-8 -*-

from typing import Dict, List, Type, Any, Optional
from .base_rule import BaseRule


class RuleRegistry:
	"""
	规则注册中心，负责规则的注册、管理和调用
	"""
	
	_instance = None
	_initialized = False
	
	def __new__(cls):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance
	
	def __init__(self):
		if RuleRegistry._initialized:
			return
		
		self.rules: Dict[str, BaseRule] = {}
		self.rules_by_type: Dict[Type, List[str]] = {}
		self.rules_by_tag: Dict[str, List[str]] = {}
		RuleRegistry._initialized = True
	
	def register(self, rule: BaseRule, tags: Optional[List[str]] = None) -> None:
		"""
		注册规则
		
		Args:
			rule: 规则实例
			tags: 规则标签列表，用于分类管理
		"""
		if rule.name in self.rules:
			raise ValueError(f"Rule '{rule.name}' is already registered")
		
		self.rules[rule.name] = rule
		
		if tags:
			for tag in tags:
				if tag not in self.rules_by_tag:
					self.rules_by_tag[tag] = []
				self.rules_by_tag[tag].append(rule.name)
	
	def unregister(self, rule_name: str) -> None:
		"""
		注销规则
		
		Args:
			rule_name: 规则名称
		"""
		if rule_name not in self.rules:
			raise ValueError(f"Rule '{rule_name}' is not registered")
		
		del self.rules[rule_name]
		
		for tag, rule_names in self.rules_by_tag.items():
			if rule_name in rule_names:
				rule_names.remove(rule_name)
	
	def get_rule(self, rule_name: str) -> Optional[BaseRule]:
		"""
		获取规则
		
		Args:
			rule_name: 规则名称
		
		Returns:
			规则实例，如果不存在返回None
		"""
		return self.rules.get(rule_name)
	
	def get_rules_by_tag(self, tag: str) -> List[BaseRule]:
		"""
		根据标签获取规则列表
		
		Args:
			tag: 规则标签
		
		Returns:
			规则实例列表
		"""
		rule_names = self.rules_by_tag.get(tag, [])
		return [self.rules[name] for name in rule_names if name in self.rules]
	
	def get_all_rules(self) -> List[BaseRule]:
		"""
		获取所有已注册的规则
		
		Returns:
			规则实例列表
		"""
		return list(self.rules.values())
	
	def execute_rules(self, owner: Any, rule_names: Optional[List[str]] = None, 
	                 tags: Optional[List[str]] = None) -> None:
		"""
		执行规则
		
		Args:
			owner: 规则的所有者对象
			rule_names: 要执行的规则名称列表，如果为None则执行所有规则
			tags: 要执行的规则标签列表，如果为None则不按标签过滤
		"""
		rules_to_execute = []
		
		if rule_names:
			rules_to_execute = [self.rules[name] for name in rule_names if name in self.rules]
		elif tags:
			for tag in tags:
				rules_to_execute.extend(self.get_rules_by_tag(tag))
		else:
			rules_to_execute = self.get_all_rules()
		
		sorted_rules = sorted(rules_to_execute, key=lambda r: r.priority, reverse=True)
		
		for rule in sorted_rules:
			if rule.can_execute(owner):
				rule.execute(owner)
	
	def enable_rule(self, rule_name: str) -> None:
		"""
		启用规则
		
		Args:
			rule_name: 规则名称
		"""
		rule = self.get_rule(rule_name)
		if rule:
			rule.enable()
	
	def disable_rule(self, rule_name: str) -> None:
		"""
		禁用规则
		
		Args:
			rule_name: 规则名称
		"""
		rule = self.get_rule(rule_name)
		if rule:
			rule.disable()
	
	def clear_all(self) -> None:
		"""
		清除所有已注册的规则
		"""
		self.rules.clear()
		self.rules_by_type.clear()
		self.rules_by_tag.clear()
	
	def get_statistics(self) -> Dict[str, Any]:
		"""
		获取规则统计信息
		
		Returns:
			包含统计信息的字典
		"""
		enabled_count = sum(1 for rule in self.rules.values() if rule.enabled)
		disabled_count = len(self.rules) - enabled_count
		
		return {
			'total_rules': len(self.rules),
			'enabled_rules': enabled_count,
			'disabled_rules': disabled_count,
			'tags': list(self.rules_by_tag.keys()),
			'rule_names': list(self.rules.keys())
		}


def register_rule(rule: BaseRule, tags: Optional[List[str]] = None) -> BaseRule:
	"""
	装饰器函数，用于自动注册规则
	
	Args:
		rule: 规则类
		tags: 规则标签列表
	
	Returns:
		规则类本身
	"""
	def decorator(rule_class: Type[BaseRule]) -> Type[BaseRule]:
		rule_instance = rule_class()
		registry = RuleRegistry()
		registry.register(rule_instance, tags)
		return rule_class
	
	if isinstance(rule, type):
		return decorator(rule)
	else:
		registry = RuleRegistry()
		registry.register(rule, tags)
		return rule