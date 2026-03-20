# -*- coding:utf-8 -*-

"""
规则系统演示程序
展示如何使用新的规则系统
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from rules.rule_registry import RuleRegistry
from rules.movement import (
	LeaderRandomMovementRule,
	FollowNearestLeaderRule,
	CollisionAvoidanceRule,
	BoundaryAvoidanceRule
)


def demo_basic_usage():
	"""演示基本使用"""
	print("=" * 60)
	print("演示1: 基本使用")
	print("=" * 60)
	
	registry = RuleRegistry()
	
	# 获取统计信息
	stats = registry.get_statistics()
	print(f"已注册规则数: {stats['total_rules']}")
	print(f"可用标签: {', '.join(stats['tags'])}")
	print()


def demo_rule_management():
	"""演示规则管理"""
	print("=" * 60)
	print("演示2: 规则管理")
	print("=" * 60)
	
	registry = RuleRegistry()
	
	# 获取特定规则
	rule = registry.get_rule('CollisionAvoidanceRule')
	if rule:
		print(f"规则名称: {rule.name}")
		print(f"规则优先级: {rule.priority}")
		print(f"规则状态: {'启用' if rule.enabled else '禁用'}")
		print()
	
	# 按标签获取规则
	movement_rules = registry.get_rules_by_tag('MOVE')
	print(f"移动相关规则数: {len(movement_rules)}")
	for rule in movement_rules:
		print(f"  - {rule.name} (优先级: {rule.priority})")
	print()


def demo_rule_execution():
	"""演示规则执行"""
	print("=" * 60)
	print("演示3: 规则执行")
	print("=" * 60)
	
	# 创建模拟Actor
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
	
	registry = RuleRegistry()
	
	# Leader Actor
	leader = MockActor(is_leader=True)
	leader.rules = ['LeaderRandomMovementRule']
	print(f"Leader规则: {leader.rules}")
	
	# Follower Actor
	follower = MockActor(is_leader=False)
	follower.rules = ['FollowNearestLeaderRule', 'CollisionAvoidanceRule']
	print(f"Follower规则: {follower.rules}")
	print()


def demo_add_new_rule():
	"""演示添加新规则"""
	print("=" * 60)
	print("演示4: 添加新规则（无需修改现有代码）")
	print("=" * 60)
	
	registry = RuleRegistry()
	
	# 检查现有规则数量
	old_count = len(registry.get_all_rules())
	print(f"添加前规则数: {old_count}")
	
	# 新规则已经通过register_rule自动注册
	# BoundaryAvoidanceRule在文件末尾有：register_rule(BoundaryAvoidanceRule(), tags=['MOVE', 'BOUNDARY'])
	
	# 检查新规则数量
	new_count = len(registry.get_all_rules())
	print(f"添加后规则数: {new_count}")
	print(f"新增规则数: {new_count - old_count}")
	
	# 获取新规则
	new_rule = registry.get_rule('BoundaryAvoidanceRule')
	if new_rule:
		print(f"新规则名称: {new_rule.name}")
		print(f"新规则优先级: {new_rule.priority}")
		print(f"新规则标签: {registry.get_rules_by_tag('BOUNDARY')}")
	print()


def demo_priority_system():
	"""演示优先级系统"""
	print("=" * 60)
	print("演示5: 优先级系统")
	print("=" * 60)
	
	registry = RuleRegistry()
	
	# 获取所有规则并按优先级排序
	all_rules = registry.get_all_rules()
	sorted_rules = sorted(all_rules, key=lambda r: r.priority, reverse=True)
	
	print("规则执行顺序（按优先级从高到低）：")
	for i, rule in enumerate(sorted_rules, 1):
		print(f"{i}. {rule.name} (优先级: {rule.priority})")
	print()


def demo_condition_system():
	"""演示条件系统"""
	print("=" * 60)
	print("演示6: 条件系统")
	print("=" * 60)
	
	registry = RuleRegistry()
	
	# 获取有条件的规则
	collision_rule = registry.get_rule('CollisionAvoidanceRule')
	follow_rule = registry.get_rule('FollowNearestLeaderRule')
	
	if collision_rule:
		print(f"CollisionAvoidanceRule条件数: {len(collision_rule.conditions)}")
		print(f"CollisionAvoidanceRule优先级: {collision_rule.priority}")
	
	if follow_rule:
		print(f"FollowNearestLeaderRule条件数: {len(follow_rule.conditions)}")
		print(f"FollowNearestLeaderRule优先级: {follow_rule.priority}")
	
	print("说明: 条件系统确保规则只在满足特定条件时执行")
	print()


def main():
	"""主函数"""
	print("\n")
	print("🎮 规则系统演示程序")
	print("🎮 " + "=" * 56)
	print("\n")
	
	try:
		demo_basic_usage()
		demo_rule_management()
		demo_rule_execution()
		demo_add_new_rule()
		demo_priority_system()
		demo_condition_system()
		
		print("=" * 60)
		print("✓ 所有演示完成！")
		print("=" * 60)
		print("\n")
		print("📚 更多信息请查看：")
		print("   - 开发指南: src/rules/README.md")
		print("   - 使用指南: src/rules/USAGE_GUIDE.md")
		print("   - 重构报告: src/rules/REFACTORING_REPORT.md")
		print("   - 最终总结: src/rules/FINAL_SUMMARY.md")
		print("\n")
		
	except Exception as e:
		print(f"✗ 演示过程中发生错误: {e}")
		import traceback
		traceback.print_exc()


if __name__ == '__main__':
	main()