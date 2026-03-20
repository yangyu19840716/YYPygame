# -*- coding:utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import time
import pygame
import gc
import tracemalloc
from Core import Const
from Scene import Scene
from Core.Engine import Engine

def memory_analysis():
    pygame.init()
    
    print("="*60)
    print("内存使用和泄漏分析")
    print("="*60)
    
    # 开始内存跟踪
    tracemalloc.start()
    
    # 创建场景
    engine = Engine()
    engine.bg_color = Const.GRAY
    engine.init_display()
    
    scene = Scene()
    
    # 获取初始内存使用情况
    snapshot1 = tracemalloc.take_snapshot()
    
    print(f"\n初始内存使用:")
    print(f"  Actor数量: {Const.ACTOR_NUM}")
    print(f"  Grid数量: {scene.grid_num_w * scene.grid_num_h}")
    
    # 运行一段时间检查内存增长
    print("\n运行内存增长测试（1000帧）:")
    
    memory_samples = []
    frame_count = 0
    
    for frame in range(1000):
        # 模拟一帧的逻辑
        scene.update(0.016)  # 假设60FPS
        
        # 每100帧记录一次内存
        if frame % 100 == 0:
            current, peak = tracemalloc.get_traced_memory()
            memory_samples.append({
                'frame': frame,
                'current': current / 1024 / 1024,  # MB
                'peak': peak / 1024 / 1024  # MB
            })
            print(f"  帧{frame}: 当前{current/1024/1024:.2f}MB, 峰值{peak/1024/1024:.2f}MB")
        
        frame_count += 1
    
    # 获取最终内存快照
    snapshot2 = tracemalloc.take_snapshot()
    
    # 比较内存变化
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')
    
    print("\n内存增长分析:")
    print(f"  初始内存: {memory_samples[0]['current']:.2f}MB")
    print(f"  最终内存: {memory_samples[-1]['current']:.2f}MB")
    print(f"  内存增长: {memory_samples[-1]['current'] - memory_samples[0]['current']:.2f}MB")
    print(f"  峰值内存: {memory_samples[-1]['peak']:.2f}MB")
    
    # 检查是否有明显的内存泄漏
    memory_growth = memory_samples[-1]['current'] - memory_samples[0]['current']
    if memory_growth > 1.0:  # 增长超过1MB
        print(f"\n⚠️  警告: 检测到可能的内存泄漏，增长了{memory_growth:.2f}MB")
    else:
        print(f"\n✓ 内存使用稳定，无明显泄漏")
    
    # 分析内存分配热点
    print("\n内存分配热点（前10）:")
    for stat in top_stats[:10]:
        print(f"  {stat}")
    
    # 分析对象生命周期
    print("\n对象生命周期分析:")
    
    # 测试Actor对象创建和销毁
    print("\nActor对象创建/销毁测试:")
    
    gc.collect()  # 强制垃圾回收
    
    # 测试创建大量Actor
    start_mem = tracemalloc.get_traced_memory()[0]
    test_actors = []
    from Actor import Actor
    
    for i in range(1000):
        actor = Actor()
        test_actors.append(actor)
    
    after_create_mem = tracemalloc.get_traced_memory()[0]
    create_mem = (after_create_mem - start_mem) / 1024  # KB
    
    print(f"  创建1000个Actor: {create_mem:.2f}KB")
    print(f"  平均每个Actor: {create_mem/1000:.2f}KB")
    
    # 测试删除Actor
    del test_actors
    gc.collect()
    
    after_delete_mem = tracemalloc.get_traced_memory()[0]
    delete_mem = (after_create_mem - after_delete_mem) / 1024  # KB
    
    print(f"  删除1000个Actor: {delete_mem:.2f}KB")
    print(f"  内存回收率: {delete_mem/create_mem*100:.1f}%")
    
    # 分析Grid对象内存
    print("\nGrid对象内存分析:")
    
    start_mem = tracemalloc.get_traced_memory()[0]
    
    # 创建网格
    test_grids = []
    from Grid import Grid
    for x in range(30):
        for y in range(20):
            grid = Grid()
            grid.init_pos(x, y)
            test_grids.append(grid)
    
    after_grid_mem = tracemalloc.get_traced_memory()[0]
    grid_mem = (after_grid_mem - start_mem) / 1024  # KB
    
    print(f"  创建600个Grid: {grid_mem:.2f}KB")
    print(f"  平均每个Grid: {grid_mem/600:.2f}KB")
    
    # 分析聚类对象内存
    print("\n聚类对象内存分析:")
    
    start_mem = tracemalloc.get_traced_memory()[0]
    
    # 执行一次聚类
    clusters, leaders, score = scene.clustering.cluster_and_select_leaders(scene.actors)
    
    after_cluster_mem = tracemalloc.get_traced_memory()[0]
    cluster_mem = (after_cluster_mem - start_mem) / 1024  # KB
    
    print(f"  执行一次聚类: {cluster_mem:.2f}KB")
    print(f"  临时对象数量: {len(clusters)}个簇")
    
    # 内存优化建议
    print("\n" + "="*60)
    print("内存优化建议")
    print("="*60)
    
    print("\n1. 对象池优化:")
    print(f"   - Actor对象平均大小: {create_mem/1000:.2f}KB")
    print(f"   - Grid对象平均大小: {grid_mem/600:.2f}KB")
    print(f"   - 建议: 使用对象池减少频繁创建/销毁开销")
    
    print("\n2. 内存泄漏预防:")
    if memory_growth > 1.0:
        print(f"   - 检测到{memory_growth:.2f}MB内存增长")
        print(f"   - 建议: 检查事件监听器、回调函数的引用")
    else:
        print(f"   - 当前内存使用稳定")
        print(f"   - 建议: 继续监控长期运行的内存增长")
    
    print("\n3. 聚类算法内存优化:")
    print(f"   - 每次聚类临时内存: {cluster_mem:.2f}KB")
    print(f"   - 建议: 优化距离矩阵存储，考虑使用稀疏矩阵")
    
    print("\n4. 数据结构优化:")
    print(f"   - 当前使用列表存储Actor和Grid")
    print(f"   - 建议: 考虑使用更高效的数据结构如numpy数组")
    
    tracemalloc.stop()
    pygame.quit()
    
    print("\n" + "="*60)

if __name__ == '__main__':
    memory_analysis()