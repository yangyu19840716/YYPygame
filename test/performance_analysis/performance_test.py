# -*- coding:utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import time
import pygame
from Core import Const
from Scene import Scene
from Core.Engine import Engine
from Core.Profiler import Profiler

def performance_test():
    pygame.init()
    
    engine = Engine()
    engine.bg_color = Const.GRAY
    engine.init_display()
    
    scene = Scene()
    
    engine.logic_tick = scene.update
    engine.draw_tick = scene.draw
    engine.pick = scene.pick
    engine.cancel_callback = scene.cancel
    engine.frame_lock = 0  # 不限制帧率以测试最大性能
    engine.init_ticks()
    
    frame_count = 0
    total_time = 0
    fps_samples = []
    logic_times = []
    draw_times = []
    
    print("开始性能测试，运行10秒...")
    print(f"Actor数量: {Const.ACTOR_NUM}")
    print(f"网格大小: {Const.GRID_SIZE}")
    print(f"聚类间隔: {scene.cluster_interval}帧")
    
    start_time = time.time()
    test_duration = 10  # 测试10秒
    
    while True:
        frame_start = time.time()
        
        if pygame.event.get(pygame.QUIT):
            break
        
        # 处理输入
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
        
        # 测量逻辑更新时间
        logic_start = time.time()
        crt_t = time.time()
        engine.frame_time = crt_t - engine.last_time
        engine.last_time = crt_t
        if engine.frame_time < 1e-6:
            engine.frame_time = 1e-6
        elif engine.frame_time > 0.05:
            engine.frame_time = 0.05
        
        engine._input_process()
        engine._logic(engine.frame_time)
        logic_end = time.time()
        logic_times.append(logic_end - logic_start)
        
        # 测量绘制时间
        draw_start = time.time()
        engine.screen.fill(engine.bg_color)
        engine._draw()
        pygame.display.flip()
        draw_end = time.time()
        draw_times.append(draw_end - draw_start)
        
        frame_end = time.time()
        frame_time = frame_end - frame_start
        fps = 1.0 / frame_time if frame_time > 0 else 0
        fps_samples.append(fps)
        
        frame_count += 1
        total_time = time.time() - start_time
        
        if total_time >= test_duration:
            break
    
    pygame.quit()
    
    # 计算统计数据
    avg_fps = sum(fps_samples) / len(fps_samples)
    min_fps = min(fps_samples)
    max_fps = max(fps_samples)
    avg_logic_time = sum(logic_times) / len(logic_times) * 1000  # 转换为毫秒
    avg_draw_time = sum(draw_times) / len(draw_times) * 1000
    
    print("\n" + "="*60)
    print("性能分析报告")
    print("="*60)
    print(f"测试时长: {total_time:.2f}秒")
    print(f"总帧数: {frame_count}")
    print(f"平均FPS: {avg_fps:.2f}")
    print(f"最低FPS: {min_fps:.2f}")
    print(f"最高FPS: {max_fps:.2f}")
    print(f"平均帧时间: {1000/avg_fps:.2f}ms")
    print(f"逻辑更新平均耗时: {avg_logic_time:.2f}ms ({avg_logic_time/(1000/avg_fps)*100:.1f}%)")
    print(f"绘制平均耗时: {avg_draw_time:.2f}ms ({avg_draw_time/(1000/avg_fps)*100:.1f}%)")
    print(f"其他开销: {(1000/avg_fps - avg_logic_time - avg_draw_time):.2f}ms ({(100 - avg_logic_time/(1000/avg_fps)*100 - avg_draw_time/(1000/avg_fps)*100):.1f}%)")
    
    # 性能瓶颈分析
    print("\n" + "="*60)
    print("性能瓶颈分析")
    print("="*60)
    
    if avg_fps < 30:
        print("严重性能问题：FPS低于30，存在明显卡顿")
    elif avg_fps < 60:
        print("性能问题：FPS低于60，存在轻微卡顿")
    else:
        print("性能良好：FPS达到60以上")
    
    print(f"\n主要性能瓶颈:")
    if avg_logic_time > avg_draw_time:
        print(f"- 逻辑更新是主要瓶颈，占用{avg_logic_time/(1000/avg_fps)*100:.1f}%的帧时间")
        print(f"  建议优化聚类算法频率（当前每{scene.cluster_interval}帧执行一次）")
        print(f"  建议优化Actor更新逻辑")
    else:
        print(f"- 绘制是主要瓶颈，占用{avg_draw_time/(1000/avg_fps)*100:.1f}%的帧时间")
        print(f"  建议优化绘制调用次数（当前{Const.ACTOR_NUM}个Actor每帧绘制）")
        print(f"  建议考虑批量绘制或使用更高效的绘制方法")
    
    print(f"\n内存使用情况:")
    print(f"- Actor对象数量: {Const.ACTOR_NUM}")
    print(f"- Grid对象数量: {scene.grid_num_w * scene.grid_num_h}")
    print(f"- 聚类分析频率: 每{scene.cluster_interval}帧执行一次")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    performance_test()