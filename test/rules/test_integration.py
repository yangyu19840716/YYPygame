# -*- coding:utf-8 -*-

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from rules import RuleRegistry
from rules.movement import (
	LeaderRandomMovementRule,
	FollowNearestLeaderRule,
	CollisionAvoidanceRule
)


class MockActor:
	def __init__(self, is_leader=False):
		self.is_leader = is_leader
		self.is_persistent_leader = is_leader
		self.actor_pos = type('Vector2', (), {'x': 100, 'y': 100})()
		self.actor_speed = 20
		self.actor_speed_dir = type('Vector2', (), {'x': 1, 'y': 0})()
		self.target_pos = type('Vector2', (), {'x': 200, 'y': 200})()
		self.my_leader = None
		self.leader_dir_change_timer = 0
		self.rules = []
	
	def set_speed_vec(self, speed_vec):
		self.actor_speed_dir = speed_vec
	
	def rand_target(self):
		self.target_pos = type('Vector2', (), {
			'x': self.actor_pos.x + 50,
			'y': self.actor_pos.y + 50
		})()
	
	def get_neighbours_from_grid(self):
		return []


class TestMovementRulesIntegration(unittest.TestCase):
	def setUp(self):
		self.registry = RuleRegistry()
		self.registry.clear_all()
		
		leader_rule = LeaderRandomMovementRule()
		follow_rule = FollowNearestLeaderRule()
		collision_rule = CollisionAvoidanceRule()
		
		self.registry.register(leader_rule, tags=['MOVE', 'LEADER'])
		self.registry.register(follow_rule, tags=['MOVE', 'FOLLOW'])
		self.registry.register(collision_rule, tags=['MOVE', 'COLLISION'])
	
	def test_leader_random_movement(self):
		leader = MockActor(is_leader=True)
		leader.rules = ['LeaderRandomMovementRule']
		
		self.registry.execute_rules(leader, rule_names=leader.rules)
		
		self.assertEqual(leader.leader_dir_change_timer, 1)
	
	def test_leader_direction_change(self):
		leader = MockActor(is_leader=True)
		leader.leader_dir_change_timer = 120
		leader.rules = ['LeaderRandomMovementRule']
		
		self.registry.execute_rules(leader, rule_names=leader.rules)
		
		self.assertEqual(leader.leader_dir_change_timer, 0)
	
	def test_follower_nearest_leader(self):
		follower = MockActor(is_leader=False)
		leader = MockActor(is_leader=True)
		
		follower.get_neighbours_from_grid = lambda: [leader]
		follower.rules = ['FollowNearestLeaderRule']
		
		self.registry.execute_rules(follower, rule_names=follower.rules)
		
		self.assertEqual(follower.my_leader, leader)
	
	def test_follower_maintains_distance(self):
		follower = MockActor(is_leader=False)
		leader = MockActor(is_leader=True)
		leader.actor_pos = type('Vector2', (), {'x': 100, 'y': 100})()
		follower.actor_pos = type('Vector2', (), {'x': 90, 'y': 90})()
		
		follower.get_neighbours_from_grid = lambda: [leader]
		follower.rules = ['FollowNearestLeaderRule']
		
		self.registry.execute_rules(follower, rule_names=follower.rules)
		
		self.assertEqual(follower.my_leader, leader)
	
	def test_collision_avoidance(self):
		actor1 = MockActor(is_leader=False)
		actor2 = MockActor(is_leader=False)
		
		actor1.actor_pos = type('Vector2', (), {'x': 100, 'y': 100})()
		actor2.actor_pos = type('Vector2', (), {'x': 105, 'y': 100})()
		
		actor1.get_neighbours_from_grid = lambda: [actor2]
		actor1.rules = ['CollisionAvoidanceRule']
		
		self.registry.execute_rules(actor1, rule_names=actor1.rules)
		
		self.assertIsNotNone(actor1.actor_speed_dir)
	
	def test_multiple_rules_execution(self):
		actor = MockActor(is_leader=False)
		actor.rules = ['FollowNearestLeaderRule', 'CollisionAvoidanceRule']
		
		leader = MockActor(is_leader=True)
		actor.get_neighbours_from_grid = lambda: [leader]
		
		self.registry.execute_rules(actor, rule_names=actor.rules)
		
		self.assertEqual(actor.my_leader, leader)
	
	def test_rule_priority_order(self):
		actor = MockActor(is_leader=False)
		
		actor.rules = ['FollowNearestLeaderRule', 'CollisionAvoidanceRule']
		
		leader = MockActor(is_leader=True)
		actor.get_neighbours_from_grid = lambda: [leader]
		
		self.registry.execute_rules(actor, rule_names=actor.rules)
		
		collision_rule = self.registry.get_rule('CollisionAvoidanceRule')
		follow_rule = self.registry.get_rule('FollowNearestLeaderRule')
		
		self.assertGreater(collision_rule.priority, follow_rule.priority)
	
	def test_disabled_rule_not_executed(self):
		actor = MockActor(is_leader=True)
		actor.rules = ['LeaderRandomMovementRule']
		
		self.registry.disable_rule('LeaderRandomMovementRule')
		
		initial_timer = actor.leader_dir_change_timer
		self.registry.execute_rules(actor, rule_names=actor.rules)
		
		self.assertEqual(actor.leader_dir_change_timer, initial_timer)
	
	def test_enable_rule_execution(self):
		actor = MockActor(is_leader=True)
		actor.rules = ['LeaderRandomMovementRule']
		
		self.registry.disable_rule('LeaderRandomMovementRule')
		self.registry.enable_rule('LeaderRandomMovementRule')
		
		self.registry.execute_rules(actor, rule_names=actor.rules)
		
		self.assertEqual(actor.leader_dir_change_timer, 1)


class TestRuleSystemScalability(unittest.TestCase):
	def setUp(self):
		self.registry = RuleRegistry()
		self.registry.clear_all()
	
	def test_multiple_actors_with_different_rules(self):
		leader = MockActor(is_leader=True)
		follower1 = MockActor(is_leader=False)
		follower2 = MockActor(is_leader=False)
		
		leader.rules = ['LeaderRandomMovementRule']
		follower1.rules = ['FollowNearestLeaderRule', 'CollisionAvoidanceRule']
		follower2.rules = ['FollowNearestLeaderRule', 'CollisionAvoidanceRule']
		
		leader.get_neighbours_from_grid = lambda: []
		follower1.get_neighbours_from_grid = lambda: [leader]
		follower2.get_neighbours_from_grid = lambda: [leader]
		
		self.registry.execute_rules(leader, rule_names=leader.rules)
		self.registry.execute_rules(follower1, rule_names=follower1.rules)
		self.registry.execute_rules(follower2, rule_names=follower2.rules)
		
		self.assertEqual(leader.leader_dir_change_timer, 1)
		self.assertEqual(follower1.my_leader, leader)
		self.assertEqual(follower2.my_leader, leader)
	
	def test_dynamic_rule_addition(self):
		actor = MockActor(is_leader=False)
		actor.rules = ['FollowNearestLeaderRule']
		
		leader = MockActor(is_leader=True)
		actor.get_neighbours_from_grid = lambda: [leader]
		
		self.registry.execute_rules(actor, rule_names=actor.rules)
		
		actor.rules.append('CollisionAvoidanceRule')
		self.registry.execute_rules(actor, rule_names=actor.rules)
		
		self.assertEqual(actor.my_leader, leader)
	
	def test_rule_removal(self):
		actor = MockActor(is_leader=True)
		actor.rules = ['LeaderRandomMovementRule']
		
		self.registry.execute_rules(actor, rule_names=actor.rules)
		self.assertEqual(actor.leader_dir_change_timer, 1)
		
		self.registry.unregister('LeaderRandomMovementRule')
		
		with self.assertRaises(KeyError):
			self.registry.execute_rules(actor, rule_names=actor.rules)


class TestRuleSystemStability(unittest.TestCase):
	def setUp(self):
		self.registry = RuleRegistry()
		self.registry.clear_all()
	
	def test_concurrent_rule_execution(self):
		actors = [MockActor(is_leader=(i == 0)) for i in range(10)]
		
		for actor in actors:
			if actor.is_leader:
				actor.rules = ['LeaderRandomMovementRule']
			else:
				actor.rules = ['FollowNearestLeaderRule', 'CollisionAvoidanceRule']
		
		leader = actors[0]
		for actor in actors[1:]:
			actor.get_neighbours_from_grid = lambda: [leader]
		
		for actor in actors:
			self.registry.execute_rules(actor, rule_names=actor.rules)
		
		self.assertEqual(leader.leader_dir_change_timer, 1)
		for actor in actors[1:]:
			self.assertEqual(actor.my_leader, leader)
	
	def test_error_handling_in_rules(self):
		class ErrorRule(BaseRule):
			def execute(self, owner, *args, **kwargs):
				raise ValueError("Test error")
		
		from rules.base_rule import BaseRule
		error_rule = ErrorRule()
		self.registry.register(error_rule)
		
		actor = MockActor(is_leader=False)
		actor.rules = ['ErrorRule']
		
		try:
			self.registry.execute_rules(actor, rule_names=actor.rules)
		except ValueError:
			pass
	
	def test_rule_statistics_accuracy(self):
		leader_rule = LeaderRandomMovementRule()
		follow_rule = FollowNearestLeaderRule()
		collision_rule = CollisionAvoidanceRule()
		
		self.registry.register(leader_rule, tags=['MOVE', 'LEADER'])
		self.registry.register(follow_rule, tags=['MOVE', 'FOLLOW'])
		self.registry.register(collision_rule, tags=['MOVE', 'COLLISION'])
		
		stats = self.registry.get_statistics()
		
		self.assertEqual(stats['total_rules'], 3)
		self.assertEqual(stats['enabled_rules'], 3)
		self.assertEqual(stats['disabled_rules'], 0)
		self.assertIn('MOVE', stats['tags'])
		self.assertIn('LEADER', stats['tags'])
		self.assertIn('FOLLOW', stats['tags'])
		self.assertIn('COLLISION', stats['tags'])


if __name__ == '__main__':
	unittest.main()