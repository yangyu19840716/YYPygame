# -*- coding:utf-8 -*-

from Core.Singleton import Singleton


class RuleManager(Singleton):
	rules = {}

	@staticmethod
	def process(owner, rules={}):
		for rule in rules:
			rule_info = RuleManager.rules.get(rule, None)
			if not rule_info:
				continue

			conditions = rule_info.properties.get('condition', [])
			run_rule = True
			for condition in conditions:
				run_rule &= condition(owner)
			run_rule and rule(owner)


def rule_def(owner_type, main_tag, *tags, **properties):
	def reg_rule(rule):
		info = RuleInfo(owner_type, main_tag, tags, properties)
		RuleManager.rules[rule] = info

		# def rule_wrapper(*args, **kwargs):
		# 	rule(info, *args, **kwargs)
		return rule
	return reg_rule


class RuleInfo:
	def __init__(self, owner_type, main_tag, tags, properties):
		self.owner_type = owner_type
		self.main_tag = main_tag
		self.tags = tags
		self.properties = properties
