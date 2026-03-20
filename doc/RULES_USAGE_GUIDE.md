# 规则系统使用指南

## 快速开始

### 1. 基本使用

```python
from rules import RuleRegistry

# 获取规则注册中心
registry = RuleRegistry()

# 执行所有规则
registry.execute_rules(actor)

# 执行指定规则
registry.execute_rules(actor, rule_names=['MyRule'])

# 按标签执行规则
registry.execute_rules(actor, tags=['MOVE'])
```

### 2. Actor集成

```python
from rules import RuleRegistry

class Actor:
	def __init__(self):
		# 使用规则名称字符串
		self.rules = ['LeaderRandomMovementRule', 'CollisionAvoidanceRule']
	
	def update(self, dt):
		registry = RuleRegistry()
		registry.execute_rules(self, rule_names=self.rules)
```

## 规则管理

### 查询规则

```python
registry = RuleRegistry()

# 获取所有规则
all_rules = registry.get_all_rules()

# 获取特定规则
rule = registry.get_rule('MyRule')

# 按标签获取规则
movement_rules = registry.get_rules_by_tag('MOVE')

# 获取统计信息
stats = registry.get_statistics()
print(f"总规则数: {stats['total_rules']}")
print(f"启用规则数: {stats['enabled_rules']}")
```

### 控制规则

```python
registry = RuleRegistry()

# 启用规则
registry.enable_rule('MyRule')

# 禁用规则
registry.disable_rule('MyRule')

# 注销规则
registry.unregister('MyRule')

# 清除所有规则
registry.clear_all()
```

## 实际应用示例

### 示例1: 为不同类型Actor分配规则

```python
class Actor:
	def __init__(self, actor_type):
		if actor_type == 'LEADER':
			self.rules = [
				'LeaderRandomMovementRule',
				'BoundaryAvoidanceRule'
			]
		elif actor_type == 'FOLLOWER':
			self.rules = [
				'FollowNearestLeaderRule',
				'CollisionAvoidanceRule',
				'BoundaryAvoidanceRule'
			]
		else:
			self.rules = ['CollisionAvoidanceRule']
```

### 示例2: 动态规则分配

```python
class Actor:
	def __init__(self):
		self.rules = ['CollisionAvoidanceRule']
		self.is_leader = False
	
	def promote_to_leader(self):
		if not self.is_leader:
			self.is_leader = True
			# 移除跟随规则
			self.rules.remove('FollowNearestLeaderRule')
			# 添加Leader规则
			self.rules.append('LeaderRandomMovementRule')
	
	def demote_to_follower(self):
		if self.is_leader:
			self.is_leader = False
			# 移除Leader规则
			self.rules.remove('LeaderRandomMovementRule')
			# 添加跟随规则
			self.rules.append('FollowNearestLeaderRule')
```

### 示例3: 条件规则执行

```python
class Scene:
	def __init__(self):
		self.emergency_mode = False
	
	def update_actors(self, actors):
		registry = RuleRegistry()
		
		for actor in actors:
			if self.emergency_mode:
				# 紧急模式只执行安全相关规则
				registry.execute_rules(actor, tags=['SAFETY'])
			else:
				# 正常模式执行所有规则
				registry.execute_rules(actor, rule_names=actor.rules)
```

### 示例4: 规则性能监控

```python
class RuleMonitor:
	def __init__(self):
		self.execution_times = {}
	
	def monitor_execution(self, actor, rule_names):
		import time
		registry = RuleRegistry()
		
		for rule_name in rule_names:
			rule = registry.get_rule(rule_name)
			if not rule or not rule.can_execute(actor):
				continue
			
			start_time = time.time()
			rule.execute(actor)
			end_time = time.time()
			
			execution_time = end_time - start_time
			if rule_name not in self.execution_times:
				self.execution_times[rule_name] = []
			self.execution_times[rule_name].append(execution_time)
	
	def get_statistics(self):
		stats = {}
		for rule_name, times in self.execution_times.items():
			stats[rule_name] = {
				'avg_time': sum(times) / len(times),
				'max_time': max(times),
				'min_time': min(times),
				'call_count': len(times)
			}
		return stats
```

## 规则开发工作流

### 开发新规则

1. **复制模板**
```bash
cp src/rules/templates/rule_template.py src/rules/movement/my_new_rule.py
```

2. **实现规则**
```python
from typing import Any
from ..core import BaseRule, register_rule

class MyNewRule(BaseRule):
	def __init__(self):
		super().__init__()
		self.set_priority(5)
	
	def execute(self, owner: Any, *args, **kwargs) -> Any:
		# 实现规则逻辑
		pass

register_rule(MyNewRule(), tags=['MOVE', 'CUSTOM'])
```

3. **测试规则**
```python
# 创建测试文件
python -m pytest src/rules/tests/test_my_new_rule.py
```

4. **集成规则**
```python
# 在Actor中使用
actor.rules.append('MyNewRule')
```

5. **无需修改其他代码！**

## 规则调试

### 启用调试模式

```python
class DebugRuleRegistry(RuleRegistry):
	def execute_rules(self, owner, rule_names=None, tags=None):
		print(f"执行规则: owner={owner}, rules={rule_names}, tags={tags}")
		super().execute_rules(owner, rule_names, tags)
```

### 规则执行追踪

```python
class RuleTracer:
	def __init__(self):
		self.execution_log = []
	
	def trace_execution(self, actor, rule_names):
		registry = RuleRegistry()
		
		for rule_name in rule_names:
			rule = registry.get_rule(rule_name)
			if not rule:
				continue
			
			can_execute = rule.can_execute(actor)
			self.execution_log.append({
				'rule': rule_name,
				'can_execute': can_execute,
				'priority': rule.priority,
				'enabled': rule.enabled
			})
			
			if can_execute:
				rule.execute(actor)
	
	def print_log(self):
		for entry in self.execution_log:
			status = "✓" if entry['can_execute'] else "✗"
			print(f"{status} {entry['rule']}: priority={entry['priority']}, enabled={entry['enabled']}")
```

## 常见使用场景

### 场景1: 游戏状态切换

```python
class GameState:
	NORMAL = 'normal'
	COMBAT = 'combat'
	STEALTH = 'stealth'

class Actor:
	def __init__(self):
		self.current_state = GameState.NORMAL
		self.rules_by_state = {
			GameState.NORMAL: ['FollowNearestLeaderRule', 'CollisionAvoidanceRule'],
			GameState.COMBAT: ['AttackRule', 'DefendRule', 'CollisionAvoidanceRule'],
			GameState.STEALTH: ['MoveQuietlyRule', 'AvoidDetectionRule']
		}
	
	def update(self, dt):
		registry = RuleRegistry()
		rules = self.rules_by_state[self.current_state]
		registry.execute_rules(self, rule_names=rules)
	
	def change_state(self, new_state):
		self.current_state = new_state
```

### 场景2: 规则组合

```python
class RuleComposer:
	def __init__(self):
		self.rule_sets = {
			'aggressive': ['AttackRule', 'ChaseRule', 'CollisionAvoidanceRule'],
			'defensive': ['DefendRule', 'RetreatRule', 'CollisionAvoidanceRule'],
			'exploratory': ['ExploreRule', 'FollowNearestLeaderRule', 'BoundaryAvoidanceRule']
		}
	
	def get_rules(self, behavior_type):
		return self.rule_sets.get(behavior_type, [])
```

### 场景3: 规则优先级调整

```python
class RulePriorityManager:
	def __init__(self):
		registry = RuleRegistry()
		self.default_priorities = {
			'CollisionAvoidanceRule': 10,
			'FollowNearestLeaderRule': 0,
			'LeaderRandomMovementRule': 0
		}
	
	def set_emergency_priorities(self):
		registry = RuleRegistry()
		# 提高安全规则优先级
		registry.get_rule('CollisionAvoidanceRule').set_priority(100)
	
	def restore_priorities(self):
		registry = RuleRegistry()
		# 恢复默认优先级
		for rule_name, priority in self.default_priorities.items():
			rule = registry.get_rule(rule_name)
			if rule:
				rule.set_priority(priority)
```

## 最佳实践

### 1. 规则命名

```python
# 好的命名
class FollowNearestLeaderRule(BaseRule):  # 清晰描述功能
class CollisionAvoidanceRule(BaseRule):      # 明确表达目的

# 不好的命名
class Rule1(BaseRule):                  # 无意义
class MovementRule(BaseRule):             # 过于泛化
```

### 2. 标签使用

```python
# 好的标签
register_rule(MyRule(), tags=['MOVE', 'SAFETY', 'HIGH_PRIORITY'])

# 不好的标签
register_rule(MyRule(), tags=['rule', 'test', 'custom'])
```

### 3. 优先级设置

```python
# 推荐的优先级范围
EMERGENCY_PRIORITY = 100      # 紧急情况
SAFETY_PRIORITY = 50         # 安全相关
BEHAVIOR_PRIORITY = 10        # 行为相关
MOVEMENT_PRIORITY = 5         # 移动相关
DEFAULT_PRIORITY = 0          # 默认优先级
```

### 4. 错误处理

```python
class RobustRule(BaseRule):
	def execute(self, owner, *args, **kwargs):
		try:
			# 规则逻辑
			if not hasattr(owner, 'required_attr'):
				return
			
			result = self._perform_action(owner)
			return result
			
		except AttributeError as e:
			print(f"规则执行错误（属性缺失）: {e}")
		except ValueError as e:
			print(f"规则执行错误（数值问题）: {e}")
		except Exception as e:
			print(f"规则执行未知错误: {e}")
```

## 性能优化

### 1. 规则缓存

```python
class CachedRule(BaseRule):
	def __init__(self):
		super().__init__()
		self._cache = {}
		self._cache_size = 100
	
	def execute(self, owner):
		cache_key = self._get_cache_key(owner)
		
		if cache_key in self._cache:
			return self._cache[cache_key]
		
		result = self._compute_result(owner)
		
		# 限制缓存大小
		if len(self._cache) >= self._cache_size:
			self._cache.popitem()
		
		self._cache[cache_key] = result
		return result
```

### 2. 条件优化

```python
class OptimizedRule(BaseRule):
	def __init__(self):
		super().__init__()
		# 添加快速失败条件
		self.add_condition(self._quick_check)
		self.add_condition(self._detailed_check)
	
	def _quick_check(self, owner):
		# 快速检查，尽早过滤
		return hasattr(owner, 'required_attr')
	
	def _detailed_check(self, owner):
		# 详细检查，只在快速检查通过后执行
		return owner.required_attr > 0
```

## 总结

新规则系统提供了：
- ✅ 简单易用的API
- ✅ 灵活的规则管理
- ✅ 强大的扩展能力
- ✅ 完善的调试工具
- ✅ 丰富的使用示例

通过遵循本指南，您可以快速掌握规则系统的使用方法，并开发出高质量的规则模块。