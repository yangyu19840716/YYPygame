# 性能分析文件夹

本文件夹包含 YYPygame 应用程序的所有性能分析相关文件，按功能分类整理。

---

## 📁 文件夹结构

```
performance_analysis/
├── test_scripts/          # 性能测试脚本
├── reports/              # 分析报告
├── data/                 # 原始数据
└── docs/                 # 文档和说明
```

---

## 📂 子文件夹说明

### test_scripts/ - 测试脚本
包含所有性能分析测试脚本，可用于重新执行性能测试。

### reports/ - 分析报告
包含性能分析的完整报告和结果总结。

### data/ - 原始数据
包含性能分析过程中产生的原始数据文件。

### docs/ - 文档说明
包含任务状态记录、使用说明和相关文档。

---

## 🚀 快速开始

### 运行所有测试
```bash
cd e:\YYPygame\performance_analysis\test_scripts

# 整体性能测试
python performance_test.py

# 聚类算法分析
python clustering_analysis.py

# 渲染性能分析
python rendering_analysis.py

# 内存使用分析
python memory_analysis.py
```

### 查看分析报告
```bash
# 打开性能分析报告
start e:\YYPygame\performance_analysis\reports\性能分析报告.md
```

---

## 📊 主要发现

根据性能分析结果，主要性能瓶颈为：

1. **聚类算法** - 占用约160%的帧时间
2. **Actor更新** - 占用约30%的帧时间
3. **渲染操作** - 性能良好，不是瓶颈

详细分析请查看 `reports/性能分析报告.md`

---

## 📝 使用说明

1. **重新测试**: 修改代码后，运行相应测试脚本验证优化效果
2. **数据对比**: 比较不同版本的性能数据
3. **报告更新**: 根据新的测试结果更新分析报告

---

## 📞 联系信息

如有问题或需要进一步分析，请参考 `docs/` 目录下的文档。

---

**最后更新**: 2026-03-16
**版本**: 1.0