# 项目文件命名规范

## Python源代码文件命名规则

所有Python源代码文件（.py扩展名）必须严格遵循**snake_case命名规范**。

### 具体要求

1. 文件名全部使用小写字母
2. 单词之间通过下划线（_）连接
3. 不得包含空格、连字符或其他特殊字符
4. 文件名应准确反映文件内容或功能

### 命名格式

```
snake_case.py  # 全部小写，单词间用下划线连接
```

### 示例

**✅ 正确：** actor.py, scene.py, game.py, rule_manager.py, base_rule.py

**❌ 错误：** Actor.py, Scene.py, game-manager.py, RuleManager.py, baseRule.py

### 适用范围

此规则适用于项目中所有新建和现有的Python文件，包括src、performance_analysis目录及所有子目录中的.py文件。

### 实施要求

1. 新建文件时必须严格遵循snake_case命名规范
2. 现有不符合规范的文件需进行重命名调整
3. 重命名文件后，必须更新所有相关的导入语句
4. 重命名后必须进行功能测试，确保无破坏性影响
