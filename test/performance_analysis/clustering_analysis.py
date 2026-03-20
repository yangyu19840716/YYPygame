# -*- coding:utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import time
import pygame
from Core import Const
from Scene import Scene
from Core.Engine import Engine
from clustering import ActorClustering

def detailed_clustering_analysis():
    pygame.init()
    
    engine = Engine()
    engine.bg_color = Const.GRAY
    engine.init_display()
    
    scene = Scene()
    
    print("="*60)
    print("聚类算法详细性能分析")
    print("="*60)
    print(f"Actor数量: {Const.ACTOR_NUM}")
    print(f"聚类参数: eps={scene.clustering.eps}, min_samples={scene.clustering.min_samples}")
    print(f"聚类频率: 每{scene.cluster_interval}帧执行一次")
    
    # 测试不同聚类频率的性能
    test_intervals = [5, 10, 15, 20, 30, 60]
    results = []
    
    for interval in test_intervals:
        scene.cluster_interval = interval
        scene.cluster_frame_count = 0
        
        # 运行一段时间测试
        frame_count = 0
        clustering_times = []
        total_frames = 300  # 测试300帧
        
        start_time = time.time()
        
        for frame in range(total_frames):
            # 模拟一帧的聚类操作
            scene.cluster_frame_count += 1
            if scene.cluster_frame_count >= scene.cluster_interval:
                cluster_start = time.time()
                clusters, leaders, score = scene.clustering.cluster_and_select_leaders(scene.actors)
                cluster_end = time.time()
                clustering_times.append((cluster_end - cluster_start) * 1000)  # 转换为毫秒
                
                # 重置leader标志
                for actor in scene.actors:
                    if actor.is_leader:
                        actor.is_leader = False
                
                # 设置新的leader
                for leader in leaders:
                    if leader:
                        leader.is_leader = True
                
                scene.cluster_frame_count = 0
            
            frame_count += 1
        
        avg_cluster_time = sum(clustering_times) / len(clustering_times) if clustering_times else 0
        max_cluster_time = max(clustering_times) if clustering_times else 0
        min_cluster_time = min(clustering_times) if clustering_times else 0
        
        results.append({
            'interval': interval,
            'avg_time': avg_cluster_time,
            'max_time': max_cluster_time,
            'min_time': min_cluster_time,
            'cluster_count': len(clustering_times)
        })
        
        print(f"\n聚类间隔: {interval}帧")
        print(f"  聚类次数: {len(clustering_times)}")
        print(f"  平均耗时: {avg_cluster_time:.2f}ms")
        print(f"  最大耗时: {max_cluster_time:.2f}ms")
        print(f"  最小耗时: {min_cluster_time:.2f}ms")
        print(f"  每秒聚类开销: {avg_cluster_time * (60/interval):.2f}ms")
    
    pygame.quit()
    
    # 分析结果
    print("\n" + "="*60)
    print("聚类性能分析总结")
    print("="*60)
    
    print("\n不同聚类间隔的性能影响:")
    for result in results:
        fps_impact = (result['avg_time'] / (1000/60)) * 100  # 对60FPS的影响
        print(f"间隔{result['interval']}帧: 每次聚类{result['avg_time']:.2f}ms, 对FPS影响约{fps_impact:.1f}%")
    
    # 推荐最佳配置
    best_result = min(results, key=lambda x: x['avg_time'] / x['interval'])
    print(f"\n推荐配置: 每{best_result['interval']}帧执行一次聚类")
    print(f"理由: 在保持聚类效果的同时，最小化性能开销")
    
    # 分析聚类算法复杂度
    print("\n" + "="*60)
    print("聚类算法复杂度分析")
    print("="*60)
    
    n = Const.ACTOR_NUM
    print(f"当前Actor数量: {n}")
    print(f"理论时间复杂度: O(n²) - DBSCAN算法")
    print(f"每次聚类需要计算的距离数: ~{n*(n-1)/2}")
    
    # 测试不同Actor数量的性能
    print("\n不同Actor数量的聚类性能:")
    actor_counts = [50, 100, 200, 300, 500]
    
    for count in actor_counts:
        # 创建测试场景
        test_scene = Scene.__new__(Scene)
        test_scene.map_w = Const.WIDTH
        test_scene.map_h = Const.HEIGHT
        test_scene.grid_num_w = int(Const.WIDTH / Const.GRID_SIZE) + 1
        test_scene.grid_num_h = int(Const.HEIGHT / Const.GRID_SIZE) + 1
        test_scene.clustering = ActorClustering(eps=100, min_samples=3)
        test_scene.cluster_frame_count = 0
        test_scene.cluster_interval = 15
        
        # 创建指定数量的Actor
        from Actor import Actor
        test_scene.actors = []
        for i in range(count):
            actor = Actor()
            test_scene.actors.append(actor)
        
        # 测试聚类性能
        start = time.time()
        clusters, leaders, score = test_scene.clustering.cluster_and_select_leaders(test_scene.actors)
        end = time.time()
        
        cluster_time = (end - start) * 1000
        print(f"  {count}个Actor: {cluster_time:.2f}ms")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    detailed_clustering_analysis()