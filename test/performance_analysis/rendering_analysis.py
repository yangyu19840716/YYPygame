# -*- coding:utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import time
import pygame
from Core import Const
from Scene import Scene
from Core.Engine import Engine

def rendering_analysis():
    pygame.init()
    
    engine = Engine()
    engine.bg_color = Const.GRAY
    engine.init_display()
    
    scene = Scene()
    
    print("="*60)
    print("渲染性能详细分析")
    print("="*60)
    print(f"屏幕分辨率: {Const.SCREEN_W}x{Const.SCREEN_H}")
    print(f"Actor数量: {Const.ACTOR_NUM}")
    print(f"网格数量: {scene.grid_num_w * scene.grid_num_h}")
    
    # 分析绘制操作的性能
    print("\n绘制操作分析:")
    
    # 测试单个Actor绘制性能
    from Actor import Actor
    test_actor = Actor()
    test_actor.draw_pos.x = 400
    test_actor.draw_pos.y = 300
    
    draw_times = []
    for i in range(1000):
        start = time.time()
        test_actor.draw()
        pygame.display.flip()
        end = time.time()
        draw_times.append((end - start) * 1000)
    
    avg_single_draw = sum(draw_times) / len(draw_times)
    print(f"单个Actor绘制平均耗时: {avg_single_draw:.4f}ms")
    print(f"200个Actor绘制理论耗时: {avg_single_draw * 200:.2f}ms")
    
    # 测试批量绘制性能
    print("\n批量绘制性能测试:")
    
    batch_sizes = [50, 100, 200, 300, 500]
    
    for batch_size in batch_sizes:
        # 创建测试Actor
        test_actors = []
        for i in range(batch_size):
            actor = Actor()
            actor.draw_pos.x = 100 + (i % 20) * 30
            actor.draw_pos.y = 100 + (i // 20) * 30
            test_actors.append(actor)
        
        # 测试绘制时间
        draw_times = []
        for _ in range(100):
            start = time.time()
            engine.screen.fill(engine.bg_color)
            for actor in test_actors:
                actor.draw()
            pygame.display.flip()
            end = time.time()
            draw_times.append((end - start) * 1000)
        
        avg_batch_time = sum(draw_times) / len(draw_times)
        print(f"{batch_size}个Actor批量绘制: {avg_batch_time:.2f}ms (平均每个: {avg_batch_time/batch_size:.4f}ms)")
    
    # 分析不同绘制方法的性能
    print("\n不同绘制方法性能对比:")
    
    # 方法1: 直接绘制
    def direct_draw(actors):
        engine.screen.fill(engine.bg_color)
        for actor in actors:
            pygame.draw.circle(engine.screen, 
                              Const.RED if actor.is_leader else actor.draw_color, 
                              actor.draw_pos, 
                              actor.draw_size, 
                              4 if actor.is_leader else 2)
        pygame.display.flip()
    
    # 方法2: 使用Graph包装
    def graph_draw(actors):
        engine.screen.fill(engine.bg_color)
        for actor in actors:
            from Core.Graph import Graph
            Graph.draw_circle(actor.draw_pos, actor.draw_size, 
                            4 if actor.is_leader else 2, 
                            Const.RED if actor.is_leader else actor.draw_color)
        pygame.display.flip()
    
    test_actors = scene.actors[:100]  # 使用100个Actor测试
    
    # 测试直接绘制
    direct_times = []
    for _ in range(100):
        start = time.time()
        direct_draw(test_actors)
        end = time.time()
        direct_times.append((end - start) * 1000)
    
    avg_direct = sum(direct_times) / len(direct_times)
    print(f"直接pygame绘制: {avg_direct:.2f}ms")
    
    # 测试Graph包装绘制
    graph_times = []
    for _ in range(100):
        start = time.time()
        graph_draw(test_actors)
        end = time.time()
        graph_times.append((end - start) * 1000)
    
    avg_graph = sum(graph_times) / len(graph_times)
    print(f"Graph包装绘制: {avg_graph:.2f}ms (开销: {(avg_graph-avg_direct)/avg_direct*100:.1f}%)")
    
    # 分析显示翻转性能
    print("\n显示翻转性能分析:")
    
    flip_times = []
    for _ in range(1000):
        start = time.time()
        pygame.display.flip()
        end = time.time()
        flip_times.append((end - start) * 1000)
    
    avg_flip = sum(flip_times) / len(flip_times)
    print(f"显示翻转平均耗时: {avg_flip:.4f}ms")
    print(f"60FPS下翻转开销占比: {avg_flip/(1000/60)*100:.1f}%")
    
    # 分析屏幕清除性能
    print("\n屏幕清除性能分析:")
    
    clear_times = []
    for _ in range(1000):
        start = time.time()
        engine.screen.fill(engine.bg_color)
        end = time.time()
        clear_times.append((end - start) * 1000)
    
    avg_clear = sum(clear_times) / len(clear_times)
    print(f"屏幕清除平均耗时: {avg_clear:.4f}ms")
    print(f"60FPS下清除开销占比: {avg_clear/(1000/60)*100:.1f}%")
    
    pygame.quit()
    
    # 渲染优化建议
    print("\n" + "="*60)
    print("渲染优化建议")
    print("="*60)
    
    print("\n1. 绘制操作优化:")
    print(f"   - 当前每帧绘制{Const.ACTOR_NUM}个Actor")
    print(f"   - 单个Actor绘制耗时约{avg_single_draw:.4f}ms")
    print(f"   - 总绘制耗时约{avg_single_draw * Const.ACTOR_NUM:.2f}ms")
    print(f"   - 建议: 考虑批量绘制或使用Surface缓存")
    
    print("\n2. 显示优化:")
    print(f"   - 显示翻转耗时: {avg_flip:.4f}ms")
    print(f"   - 屏幕清除耗时: {avg_clear:.4f}ms")
    print(f"   - 建议: 只在必要时更新显示区域")
    
    print("\n3. 绘制方法选择:")
    print(f"   - 直接绘制比Graph包装快{(avg_graph-avg_direct)/avg_direct*100:.1f}%")
    print(f"   - 建议: 在性能关键路径使用直接绘制")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    rendering_analysis()