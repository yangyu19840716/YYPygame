# 项目文件命名规范

## 概述

本项目采用**驼峰命名法（CamelCase）**作为统一的文件和文件夹命名标准，确保代码库的一致性和可维护性。

## 命名规范

### 1. 文件夹命名

**规范要求：**
- 使用驼峰命名法（CamelCase）
- 首字母小写
- 后续每个单词首字母大写
- 不包含空格、下划线或其他特殊字符
- 使用有意义的名称，反映文件夹用途

**格式：**
```
camelCase  # 首字母小写，后续单词首字母大写
```

**示例：**
```bash
✅ 正确示例：
core/              # 核心模块
debug/             # 调试模块
rules/             # 规则模块
movement/          # 移动相关
templates/          # 模板文件
tests/             # 测试文件

❌ 错误示例：
Core/              # 首字母大写
Debug/             # 首字母大写
core_module/       # 包含下划线
movement-files/    # 包含连字符
test_files/        # 包含下划线
```

### 2. Python文件命名

**规范要求：**
- 使用驼峰命名法（CamelCase）
- 首字母小写
- 后续每个单词首字母大写
- 文件名应准确反映文件功能或包含的主要类/函数
- 不包含空格、下划线或其他特殊字符
- 使用`.py`作为文件扩展名

**格式：**
```
camelCase.py  # 首字母小写，后续单词首字母大写
```

**示例：**
```bash
✅ 正确示例：
actor.py                    # Actor类相关
scene.py                    # Scene类相关
game.py                     # Game类相关
grid.py                     # Grid类相关
ruleRegistry.py             # RuleRegistry类相关
baseRule.py                 # BaseRule类相关
collisionAvoidance.py        # CollisionAvoidance类相关
followNearestLeader.py       # FollowNearestLeader类相关

❌ 错误示例：
Actor.py                    # 首字母大写
scene_file.py              # 包含下划线
game-manager.py            # 包含连字符
grid.py                    # 首字母大写
RuleRegistry.py            # 首字母大写
base_rule.py               # 包含下划线
```

### 3. 命名一致性要求

**确保项目中所有现有文件夹和Python文件均符合此命名规范**

**检查清单：**
- [ ] 所有文件夹使用驼峰命名
- [ ] 所有Python文件使用驼峰命名
- [ ] 文件名准确反映功能
- [ ] 无特殊字符或下划线
- [ ] 首字母小写

### 4. 例外处理

**如存在特殊第三方库或框架要求的特定命名格式，需在项目文档中明确说明并保持一致性**

**例外情况：**
```python
# 第三方库要求的命名
from third_party_library import Special_Naming_Class

# 框架要求的命名
class Framework_Required_Name:
	pass

# 在文档中说明
"""
注意：以下命名不符合项目规范，但为第三方库/框架要求：
- Special_Naming_Class (第三方库要求）
- Framework_Required_Name (框架要求）
"""
```

## 命名原则

### 1. 清晰性

文件名应该清晰表达其用途和内容：

```python
✅ 好的命名：
collisionAvoidance.py        # 清晰表达碰撞避免功能
ruleRegistry.py             # 清晰表达规则注册功能

❌ 不好的命名：
utils.py                    # 过于泛化
helper.py                  # 不够具体
stuff.py                   # 无意义
```

### 2. 一致性

相同类型的文件应该使用一致的命名模式：

```python
✅ 一致的命名模式：
actor.py
scene.py
game.py
grid.py

❌ 不一致的命名：
actor.py
Scene.py
game.py
Grid.py
```

### 3. 简洁性

文件名应该简洁但具有描述性：

```python
✅ 简洁的命名：
actor.py
scene.py
game.py

❌ 冗长的命名：
actorEntity.py
sceneManager.py
gameController.py
```

### 4. 可读性

文件名应该易于阅读和理解：

```python
✅ 可读的命名：
collisionAvoidance.py
followNearestLeader.py

❌ 难读的命名：
colAvoid.py
fllwNstLdr.py
```

## 项目当前状态

### 已重命名的文件夹

| 原名称 | 新名称 | 状态 |
|--------|--------|------|
| Core | core | ✅ 已重命名 |
| Debug | debug | ✅ 已重命名 |

### 已更新的导入语句

以下文件已更新导入语句以符合新的命名规范：

| 文件 | 更新的导入 | 状态 |
|------|------------|------|
| Actor.py | Core → core | ✅ 已更新 |
| Scene.py | Core → core | ✅ 已更新 |
| Game.py | Core → core | ✅ 已更新 |
| Grid.py | Core → core | ✅ 已更新 |
| rules/Rule.py | Core → core | ✅ 已更新 |
| rules/RuleManager.py | Core → core | ✅ 已更新 |
| rules/movement/boundaryAvoidance.py | Core → core | ✅ 已更新 |
| rules/movement/collisionAvoidance.py | Core → core | ✅ 已更新 |
| clustering/ActorClustering.py | Core → core | ✅ 已更新 |
| Main.py | Core → core | ✅ 已更新 |

### 符合规范的文件

以下文件已符合驼峰命名规范：

- ✅ Actor.py
- ✅ Scene.py
- ✅ Game.py
- ✅ Grid.py
- ✅ Main.py
- ✅ Controller.py
- ✅ rules/baseRule.py
- ✅ rules/ruleRegistry.py
- ✅ rules/core.py
- ✅ rules/demo.py
- ✅ rules/movement/leaderRandomMovement.py
- ✅ rules/movement/followNearestLeader.py
- ✅ rules/movement/collisionAvoidance.py
- ✅ rules/movement/boundaryAvoidance.py
- ✅ rules/tests/testRuleSystem.py
- ✅ rules/tests/testIntegration.py
- ✅ rules/tests/runTests.py
- ✅ rules/templates/ruleTemplate.py
- ✅ clustering/actorClustering.py

## 使用指南

### 创建新文件夹

```bash
# 正确的文件夹命名
mkdir core
mkdir debug
mkdir movement
mkdir templates

# 错误的文件夹命名
mkdir Core              # 首字母大写
mkdir debug_module       # 包含下划线
mkdir movement-files     # 包含连字符
```

### 创建新Python文件

```python
# 正确的文件命名
# actor.py
class Actor:
	pass

# scene.py
class Scene:
	pass

# game.py
class Game:
	pass

# 错误的文件命名
# Actor.py
class Actor:      # 首字母大写
	pass

# scene_file.py
class Scene:      # 包含下划线
	pass
```

### 导入模块

```python
# 正确的导入方式
from core import Const
from core.Math import Vector2
from debug import DebugDraw

# 错误的导入方式
from Core import Const           # 首字母大写
from debug_module import DebugDraw  # 包含下划线
```

## 命名检查工具

### 手动检查

```python
import os
import re

def check_camel_case(name):
	"""
	检查是否符合驼峰命名规范
	"""
	# 检查首字母是否小写
	if not name[0].islower():
		return False, "首字母应该小写"
	
	# 检查是否包含特殊字符
	if not re.match(r'^[a-z][a-zA-Z0-9]*$', name):
		return False, "包含特殊字符或下划线"
	
	return True, "符合规范"

def check_directory(path):
	"""
	检查目录中的所有文件和文件夹
	"""
	issues = []
	
	for item in os.listdir(path):
		full_path = os.path.join(path, item)
		
		if os.path.isdir(full_path):
			# 检查文件夹命名
			valid, message = check_camel_case(item)
			if not valid:
				issues.append(f"文件夹: {item} - {message}")
		
		elif item.endswith('.py'):
			# 检查Python文件命名
			name_without_ext = item[:-3]
			valid, message = check_camel_case(name_without_ext)
			if not valid:
				issues.append(f"文件: {item} - {message}")
	
	return issues

# 使用示例
issues = check_directory('E:/YYPygame/src')
if issues:
	print("发现命名问题：")
	for issue in issues:
		print(f"  - {issue}")
else:
	print("所有文件和文件夹命名符合规范！")
```

### 自动化检查

可以创建pre-commit钩子来自动检查命名规范：

```bash
# .git/hooks/pre-commit
#!/bin/bash

python scripts/check_naming.py
if [ $? -ne 0 ]; then
	echo "命名规范检查失败，请修正后再提交"
	exit 1
fi
```

## 最佳实践

### 1. 规划命名

在创建文件前先规划好命名：

```python
# 规划阶段
文件功能：处理Actor的移动逻辑
文件包含的主要类：Actor
建议命名：actor.py

# 避免频繁重命名
# 先想好再创建
```

### 2. 使用有意义的名称

文件名应该具有描述性：

```python
✅ 有意义的命名：
collisionAvoidance.py      # 碰撞避免
followNearestLeader.py     # 跟随最近Leader
ruleRegistry.py            # 规则注册中心

❌ 无意义的命名：
file1.py
temp.py
test.py
```

### 3. 保持一致性

相同类型的文件使用一致的命名模式：

```python
✅ 一致的命名：
actor.py
scene.py
game.py
grid.py

# 所有都是单个单词，首字母小写
```

### 4. 避免缩写

除非是广泛认知的缩写，否则避免使用：

```python
✅ 可接受的缩写：
actor.py
scene.py
game.py

❌ 应避免的缩写：
act.py           # actor的缩写
scn.py           # scene的缩写
gm.py            # game的缩写
```

## 迁移指南

### 从旧命名迁移到新命名

如果项目中存在不符合规范的文件，按以下步骤迁移：

```bash
# 步骤1: 重命名文件或文件夹
git mv OldName.py newName.py
git mv OldFolder newFolder

# 步骤2: 更新所有导入语句
# 在所有引用该文件的地方更新导入

# 步骤3: 测试功能
# 确保重命名后功能正常

# 步骤4: 提交更改
git add .
git commit -m "重命名文件/文件夹以符合驼峰命名规范"
```

## 常见问题

### Q1: 为什么使用驼峰命名而不是下划线命名？

**A:** 驼峰命名在文件和文件夹级别更易读，与Python类命名（PascalCase）形成对比，提高代码组织性。

### Q2: 是否所有文件都必须使用驼峰命名？

**A:** 是的，项目中的所有文件夹和Python文件都应该遵循此规范，确保一致性。

### Q3: 如果第三方库要求不同的命名怎么办？

**A:** 在项目文档中明确说明，并保持与该库命名的一致性。

### Q4: 如何处理现有不符合规范的文件？

**A:** 逐步迁移，先重命名影响较小的文件，测试后再重命名影响较大的文件。

### Q5: 命名规范是否影响代码功能？

**A:** 不影响，命名规范只是文件和文件夹命名，不影响代码内部逻辑。

## 总结

### 核心原则

1. **驼峰命名法** - 首字母小写，后续单词首字母大写
2. **无特殊字符** - 不包含空格、下划线或连字符
3. **有意义命名** - 文件名准确反映功能
4. **一致性** - 相同类型文件使用一致模式
5. **简洁性** - 文件名简洁但具有描述性

### 实施要求

- ✅ 所有文件夹使用驼峰命名
- ✅ 所有Python文件使用驼峰命名
- ✅ 文件名准确反映功能
- ✅ 无特殊字符或下划线
- ✅ 首字母小写
- ✅ 新创建的文件严格遵循规范
- ✅ 例外情况在文档中明确说明

### 质量保证

- ✅ 提高代码可读性
- ✅ 改善项目一致性
- ✅ 降低维护成本
- ✅ 便于团队协作
- ✅ 符合行业最佳实践

---

**项目命名规范版本：1.0**  
**最后更新：2026-03-16**  
**维护者：开发团队**