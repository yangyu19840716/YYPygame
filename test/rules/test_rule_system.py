# -*- coding:utf-8 -*-

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from rules.base_rule import BaseRule
from rules.rule_registry import RuleRegistry, register_rule


class MockRule(BaseRule):
	def __init__(self):
		super().__init__()
		self.execute_count = 0
	
	def execute(self, owner, *args, **kwargs):
		self.execute_count += 1
		return "executed"


class ConditionalRule(BaseRule):
	def __init__(self):
		super().__init__()
		self.add_condition(self._should_execute)
	
	def _should_execute(self, owner):
		return hasattr(owner, 'should_execute') and owner.should_execute
	
	def execute(self, owner, *args, **kwargs):
		return "conditional_executed"


class TestBaseRule(unittest.TestCase):
	def setUp(self):
		self.rule = MockRule()
	
	def test_rule_initialization(self):
		self.assertEqual(self.rule.name, 'MockRule')
		self.assertEqual(self.rule.priority, 0)
		self.assertTrue(self.rule.enabled)
	
	def test_set_priority(self):
		self.rule.set_priority(10)
		self.assertEqual(self.rule.priority, 10)
	
	def test_enable_disable(self):
		self.rule.disable()
		self.assertFalse(self.rule.enabled)
		
		self.rule.enable()
		self.assertTrue(self.rule.enabled)
	
	def test_chain_calls(self):
		result = self.rule.set_priority(5).disable().enable()
		self.assertEqual(result, self.rule)
		self.assertEqual(self.rule.priority, 5)
		self.assertTrue(self.rule.enabled)
	
	def test_can_execute(self):
		mock_owner = type('MockOwner', (), {})()
		self.assertTrue(self.rule.can_execute(mock_owner))
	
	def test_can_execute_with_condition(self):
		conditional_rule = ConditionalRule()
		
		owner_with_condition = type('MockOwner', (), {'should_execute': True})()
		self.assertTrue(conditional_rule.can_execute(owner_with_condition))
		
		owner_without_condition = type('MockOwner', (), {})()
		self.assertFalse(conditional_rule.can_execute(owner_without_condition))
	
	def test_can_execute_disabled_rule(self):
		self.rule.disable()
		mock_owner = type('MockOwner', (), {})()
		self.assertFalse(self.rule.can_execute(mock_owner))
	
	def test_repr(self):
		self.rule.set_priority(5)
		repr_str = repr(self.rule)
		self.assertIn('MockRule', repr_str)
		self.assertIn('priority=5', repr_str)
		self.assertIn('enabled=True', repr_str)


class TestRuleRegistry(unittest.TestCase):
	def setUp(self):
		self.registry = RuleRegistry()
		self.registry.clear_all()
	
	def test_singleton_pattern(self):
		registry1 = RuleRegistry()
		registry2 = RuleRegistry()
		self.assertIs(registry1, registry2)
	
	def test_register_rule(self):
		rule = MockRule()
		self.registry.register(rule)
		
		self.assertIn('MockRule', self.registry.rules)
		self.assertEqual(self.registry.get_rule('MockRule'), rule)
	
	def test_register_duplicate_rule(self):
		rule1 = MockRule()
		rule2 = MockRule()
		
		self.registry.register(rule1)
		with self.assertRaises(ValueError):
			self.registry.register(rule2)
	
	def test_register_with_tags(self):
		rule = MockRule()
		self.registry.register(rule, tags=['TEST', 'SAMPLE'])
		
		test_rules = self.registry.get_rules_by_tag('TEST')
		self.assertEqual(len(test_rules), 1)
		self.assertEqual(test_rules[0], rule)
	
	def test_unregister_rule(self):
		rule = MockRule()
		self.registry.register(rule)
		self.registry.unregister('MockRule')
		
		self.assertNotIn('MockRule', self.registry.rules)
	
	def test_unregister_nonexistent_rule(self):
		with self.assertRaises(ValueError):
			self.registry.unregister('NonExistentRule')
	
	def test_get_rule(self):
		rule = MockRule()
		self.registry.register(rule)
		
		retrieved_rule = self.registry.get_rule('MockRule')
		self.assertEqual(retrieved_rule, rule)
	
	def test_get_nonexistent_rule(self):
		rule = self.registry.get_rule('NonExistentRule')
		self.assertIsNone(rule)
	
	def test_get_all_rules(self):
		rule1 = MockRule()
		rule2 = ConditionalRule()
		
		self.registry.register(rule1)
		self.registry.register(rule2)
		
		all_rules = self.registry.get_all_rules()
		self.assertEqual(len(all_rules), 2)
		self.assertIn(rule1, all_rules)
		self.assertIn(rule2, all_rules)
	
	def test_execute_rules(self):
		rule = MockRule()
		self.registry.register(rule)
		
		mock_owner = type('MockOwner', (), {})()
		self.registry.execute_rules(mock_owner, rule_names=['MockRule'])
		
		self.assertEqual(rule.execute_count, 1)
	
	def test_execute_rules_with_tags(self):
		rule1 = MockRule()
		rule2 = MockRule()
		
		self.registry.register(rule1, tags=['TAG1'])
		self.registry.register(rule2, tags=['TAG2'])
		
		mock_owner = type('MockOwner', (), {})()
		self.registry.execute_rules(mock_owner, tags=['TAG1'])
		
		self.assertEqual(rule1.execute_count, 1)
		self.assertEqual(rule2.execute_count, 0)
	
	def test_execute_rules_priority_order(self):
		rule1 = MockRule()
		rule2 = MockRule()
		rule3 = MockRule()
		
		rule1.set_priority(1)
		rule2.set_priority(10)
		rule3.set_priority(5)
		
		self.registry.register(rule1)
		self.registry.register(rule2)
		self.registry.register(rule3)
		
		mock_owner = type('MockOwner', (), {})()
		self.registry.execute_rules(mock_owner)
		
		self.assertEqual(rule1.execute_count, 1)
		self.assertEqual(rule2.execute_count, 1)
		self.assertEqual(rule3.execute_count, 1)
	
	def test_execute_rules_with_conditions(self):
		rule = ConditionalRule()
		self.registry.register(rule)
		
		owner_with_condition = type('MockOwner', (), {'should_execute': True})()
		self.registry.execute_rules(owner_with_condition, rule_names=['ConditionalRule'])
		
		self.assertEqual(rule.execute_count, 1)
	
	def test_execute_disabled_rules(self):
		rule = MockRule()
		rule.disable()
		self.registry.register(rule)
		
		mock_owner = type('MockOwner', (), {})()
		self.registry.execute_rules(mock_owner, rule_names=['MockRule'])
		
		self.assertEqual(rule.execute_count, 0)
	
	def test_enable_rule(self):
		rule = MockRule()
		rule.disable()
		self.registry.register(rule)
		
		self.registry.enable_rule('MockRule')
		self.assertTrue(rule.enabled)
	
	def test_disable_rule(self):
		rule = MockRule()
		self.registry.register(rule)
		
		self.registry.disable_rule('MockRule')
		self.assertFalse(rule.enabled)
	
	def test_clear_all(self):
		rule1 = MockRule()
		rule2 = ConditionalRule()
		
		self.registry.register(rule1)
		self.registry.register(rule2)
		
		self.registry.clear_all()
		
		self.assertEqual(len(self.registry.rules), 0)
		self.assertEqual(len(self.registry.rules_by_tag), 0)
	
	def test_get_statistics(self):
		rule1 = MockRule()
		rule2 = ConditionalRule()
		rule2.disable()
		
		self.registry.register(rule1, tags=['TAG1'])
		self.registry.register(rule2, tags=['TAG2'])
		
		stats = self.registry.get_statistics()
		
		self.assertEqual(stats['total_rules'], 2)
		self.assertEqual(stats['enabled_rules'], 1)
		self.assertEqual(stats['disabled_rules'], 1)
		self.assertIn('TAG1', stats['tags'])
		self.assertIn('TAG2', stats['tags'])
		self.assertIn('MockRule', stats['rule_names'])
		self.assertIn('ConditionalRule', stats['rule_names'])


class TestRegisterDecorator(unittest.TestCase):
	def setUp(self):
		self.registry = RuleRegistry()
		self.registry.clear_all()
	
	def test_register_decorator_with_instance(self):
		rule = MockRule()
		register_rule(rule, tags=['DECORATOR'])
		
		self.assertIn('MockRule', self.registry.rules)
		decorator_rules = self.registry.get_rules_by_tag('DECORATOR')
		self.assertEqual(len(decorator_rules), 1)
	
	def test_register_decorator_with_class(self):
		@register_rule(tags=['CLASS_DECORATOR'])
		class DecoratedRule(BaseRule):
			def execute(self, owner, *args, **kwargs):
				return "decorated"
		
		self.assertIn('DecoratedRule', self.registry.rules)
		decorator_rules = self.registry.get_rules_by_tag('CLASS_DECORATOR')
		self.assertEqual(len(decorator_rules), 1)


if __name__ == '__main__':
	unittest.main()