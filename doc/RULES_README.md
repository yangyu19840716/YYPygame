# 规则系统开发指南

## 概述

本规则系统采用模块化设计，支持规则的独立开发、注册和管理。每个规则都是独立的模块，通过统一的接口进行交互。

## 系统架构

### 核心组件

1. **BaseRule** - 规则基类，所有规则必须继承此类
2. **RuleRegistry** - 规则注册中心，单例模式，负责规则的全局管理
3. **register_rule** - 装饰器函数，用于自动注册规则

### 文件结构

```
src/rules/
├── __init__.py              # 规则模块导出
├── base_rule.py            # 规则基类
├── rule_registry.py        # 规则注册中心
├── core.py                # 核心模块导出
├── movement/             # 移动相关规则
│   ├── __init__.py
│   ├── leader_random_movement.py
│   ├── follow_nearest_leader.py
│   └── collision_avoidance.py
└── templates/            # 规则开发模板
    └── rule_template.py
```

## 快速开始

### 1. 创建新规则

复制 `templates/rule_template.py` 文件，或者直接创建新的规则文件：

```python
# -*- coding:utf-8 -*-

from typing import Any
from ..core import BaseRule, register_rule


class MyCustomRule(BaseRule):
	"""
	自定义规则描述
	"""
	
	def __init__(self):
		super().__init__()
		self.set_priority(0)  # 设置优先级
	
	def execute(self, owner: Any, *args, **kwargs) -> Any:
		# 实现规则逻辑
		pass


# 注册规则
register_rule(MyCustomRule(), tags=['CUSTOM', 'MY_CATEGORY'])
```

### 2. 使用规则

在Actor中添加规则：

```python
from rules import RuleRegistry

class Actor:
	def __init__(self):
		self.rules = ['MyCustomRule']  # 使用规则名称字符串
	
	def update(self, dt):
		registry = RuleRegistry()
		registry.execute_rules(self, rule_names=self.rules)
```

## 规则开发详解

### BaseRule 基类

所有规则必须继承 `BaseRule` 基类：

```python
class BaseRule(ABC):
	def __init__(self):
		self.name = self.__class__.__name__  # 规则名称
		self.priority = 0                     # 优先级
		self.conditions: List[Callable] = []     # 执行条件
		self.enabled = True                     # 是否启用
	
	@abstractmethod
	def execute(self, owner: Any, *args, **kwargs) -> Any:
		"""执行规则逻辑（必须实现）"""
		pass
	
	def can_execute(self, owner: Any) -> bool:
		"""检查规则是否可以执行"""
		pass
```

### 规则生命周期

1. **初始化** - 规则实例化时自动设置名称和默认值
2. **注册** - 通过 `register_rule` 装饰器注册到规则中心
3. **执行** - 在Actor的update方法中被调用
4. **条件检查** - 执行前检查所有条件是否满足

### 优先级系统

规则按优先级从高到低执行，数值越大优先级越高：

```python
class HighPriorityRule(BaseRule):
	def __init__(self):
		super().__init__()
		self.set_priority(100)  # 高优先级

class LowPriorityRule(BaseRule):
	def __init__(self):
		super().__init__()
		self.set_priority(0)  # 低优先级
```

### 条件系统

规则可以添加执行条件，只有所有条件都满足时才会执行：

```python
class ConditionalRule(BaseRule):
	def __init__(self):
		super().__init__()
		self.add_condition(self._is_leader)
		self.add_condition(self._has_target)
	
	def _is_leader(self, owner: Any) -> bool:
		return owner.is_leader
	
	def _has_target(self, owner: Any) -> bool:
		return owner.target is not None
```

### 链式调用

支持方法链式调用：

```python
class MyRule(BaseRule):
	def __init__(self):
		super().__init__()
		self.set_priority(10) \
			.add_condition(self._condition1) \
			.add_condition(self._condition2) \
			.enable()
```

## RuleRegistry 规则注册中心

### 基本用法

```python
from rules import RuleRegistry

# 获取单例
registry = RuleRegistry()

# 注册规则
registry.register(MyRule(), tags=['CATEGORY'])

# 执行规则
registry.execute_rules(actor, rule_names=['MyRule'])

# 按标签执行
registry.execute_rules(actor, tags=['MOVE'])

# 执行所有规则
registry.execute_rules(actor)
```

### 规则管理

```python
# 获取规则
rule = registry.get_rule('MyRule')

# 启用/禁用规则
registry.enable_rule('MyRule')
registry.disable_rule('MyRule')

# 注销规则
registry.unregister('MyRule')

# 获取统计信息
stats = registry.get_statistics()
print(f"总规则数: {stats['total_rules']}")
print(f"启用规则数: {stats['enabled_rules']}")
```

## 规则标签系统

标签用于分类和管理规则：

```python
# 注册时指定标签
register_rule(MyRule(), tags=['MOVE', 'LEADER', 'NAVIGATION'])

# 按标签获取规则
movement_rules = registry.get_rules_by_tag('MOVE')

# 按标签执行规则
registry.execute_rules(actor, tags=['MOVE'])
```

### 常用标签建议

- `MOVE` - 移动相关规则
- `ACTION` - 动作相关规则
- `LEADER` - Leader专用规则
- `FOLLOW` - 跟随相关规则
- `COLLISION` - 碰撞相关规则
- `BEHAVIOR` - 行为相关规则

## 规则开发最佳实践

### 1. 单一职责

每个规则只负责一个具体的功能：

```python
# 好的实践
class MoveToTargetRule(BaseRule):
	def execute(self, owner):
		# 只负责移动到目标
		pass

class AvoidCollisionRule(BaseRule):
	def execute(self, owner):
		# 只负责避免碰撞
		pass

# 不好的实践
class MoveAndAvoidRule(BaseRule):
	def execute(self, owner):
		# 混合了多个职责
		pass
```

### 2. 参数化配置

使用类常量配置规则参数：

```python
class FollowLeaderRule(BaseRule):
	MIN_DISTANCE = 30
	MAX_DISTANCE = 200
	FOLLOW_SPEED = 1.0
	
	def execute(self, owner):
		# 使用配置参数
		pass
```

### 3. 错误处理

添加适当的错误处理：

```python
class SafeRule(BaseRule):
	def execute(self, owner):
		try:
			# 规则逻辑
			if not hasattr(owner, 'required_attribute'):
				return
			
			# 执行规则
			pass
		except Exception as e:
			# 记录错误但不中断系统
			print(f"Rule error: {e}")
```

### 4. 性能优化

避免在规则中进行重复计算：

```python
class OptimizedRule(BaseRule):
	def __init__(self):
		super().__init__()
		self._cache = {}
	
	def execute(self, owner):
		# 使用缓存
		cache_key = f"{owner.id}_{owner.position}"
		if cache_key in self._cache:
			return self._cache[cache_key]
		
		# 计算并缓存
		result = self._calculate(owner)
		self._cache[cache_key] = result
		return result
```

## 规则示例

### 示例1: 简单移动规则

```python
class SimpleMoveRule(BaseRule):
	def __init__(self):
		super().__init__()
		self.set_priority(0)
	
	def execute(self, owner):
		if owner.target_pos:
			vec = owner.target_pos - owner.actor_pos
			if vec.length() > 1:
				normalized = vec.normalize()
				owner.set_speed_vec(normalized * owner.actor_speed)

register_rule(SimpleMoveRule(), tags=['MOVE'])
```

### 示例2: 条件规则

```python
class LeaderOnlyRule(BaseRule):
	def __init__(self):
		super().__init__()
		self.set_priority(5)
		self.add_condition(lambda owner: owner.is_leader)
	
	def execute(self, owner):
		# 只有Leader才能执行
		owner.perform_leader_action()

register_rule(LeaderOnlyRule(), tags=['LEADER', 'ACTION'])
```

### 示例3: 高优先级规则

```python
class EmergencyStopRule(BaseRule):
	def __init__(self):
		super().__init__()
		self.set_priority(100)  # 最高优先级
		self.add_condition(self._is_emergency)
	
	def _is_emergency(self, owner):
		return owner.emergency_detected
	
	def execute(self, owner):
		owner.stop_immediately()

register_rule(EmergencyStopRule(), tags=['EMERGENCY', 'STOP'])
```

## 调试和测试

### 规则调试

```python
# 获取规则统计信息
registry = RuleRegistry()
stats = registry.get_statistics()
print(stats)

# 检查规则状态
rule = registry.get_rule('MyRule')
print(f"规则状态: {rule.enabled}")
print(f"规则优先级: {rule.priority}")
```

### 单元测试

```python
import unittest
from rules import RuleRegistry

class TestMyRule(unittest.TestCase):
	def setUp(self):
		self.registry = RuleRegistry()
		self.mock_owner = MockOwner()
	
	def test_rule_execution(self):
		rule = MyRule()
		self.registry.register(rule)
		self.registry.execute_rules(self.mock_owner, rule_names=['MyRule'])
		self.assertTrue(rule_executed)
```

## 迁移指南

### 从旧系统迁移

旧系统使用函数装饰器，新系统使用类继承：

```python
# 旧系统
@rule_def(Actor, 'MOVE', condition=[is_leader], exec=Tick)
def leader_move(actor):
	pass

# 新系统
class LeaderMoveRule(BaseRule):
	def __init__(self):
		super().__init__()
		self.set_priority(0)
		self.add_condition(lambda owner: owner.is_leader)
	
	def execute(self, owner):
		pass

register_rule(LeaderMoveRule(), tags=['MOVE', 'LEADER'])
```

### 兼容性

新系统保持与旧系统的兼容性，可以逐步迁移：

```python
# 在Actor中可以混合使用
self.rules = [
	'LeaderRandomMovementRule',  # 新系统规则
	Rule.leader_random_movement    # 旧系统规则
]
```

## 常见问题

### Q: 如何动态启用/禁用规则？

```python
registry = RuleRegistry()
registry.enable_rule('MyRule')
registry.disable_rule('MyRule')
```

### Q: 如何在运行时添加新规则？

```python
# 创建并注册新规则
new_rule = MyNewRule()
registry.register(new_rule, tags=['NEW_CATEGORY'])

# 立即使用
actor.rules.append('MyNewRule')
```

### Q: 规则之间如何通信？

规则之间应该避免直接依赖，通过owner对象进行间接通信：

```python
class Rule1(BaseRule):
	def execute(self, owner):
		owner.shared_data = {'key': 'value'}

class Rule2(BaseRule):
	def execute(self, owner):
		if hasattr(owner, 'shared_data'):
			data = owner.shared_data
```

## 性能考虑

1. **避免频繁的对象创建** - 重用规则实例
2. **使用条件过滤** - 尽早过滤不需要执行的规则
3. **合理设置优先级** - 高优先级规则应该快速执行
4. **避免复杂计算** - 在execute方法中保持逻辑简单

## 扩展性

系统设计支持以下扩展：

1. **自定义规则类型** - 继承BaseRule创建新的规则类型
2. **自定义注册机制** - 扩展RuleRegistry添加新功能
3. **自定义条件系统** - 添加新的条件类型
4. **自定义标签系统** - 使用标签进行更复杂的分类

## 总结

新规则系统提供了：
- ✅ 模块化设计，规则独立开发
- ✅ 统一的接口和标准
- ✅ 灵活的注册机制
- ✅ 集中化的规则管理
- ✅ 低耦合的规则间关系
- ✅ 完善的开发文档和模板
- ✅ 易于测试和调试

添加新规则只需三步：
1. 创建规则文件
2. 继承BaseRule并实现execute方法
3. 使用register_rule装饰器注册