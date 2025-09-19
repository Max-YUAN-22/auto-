#!/usr/bin/env python3
"""
简单性能验证测试
Simple Performance Verification Test
"""

import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dsl.dsl import DSL
from core.robust_llm import llm_callable

def simple_test():
    """简单测试"""
    print("🔍 简单性能验证测试")
    print("=" * 50)
    
    # 测试单个任务
    print("1. 测试单个任务:")
    dsl = DSL(seed=42, workers=1)
    
    # 创建任务
    task = dsl.gen("test_task", prompt="计算 1+1", agent="test_agent").schedule()
    
    # 运行DSL
    start_time = time.time()
    dsl.run(llm_callable)
    end_time = time.time()
    
    execution_time = end_time - start_time
    print(f"   执行时间: {execution_time:.6f}秒")
    
    # 等待任务完成
    print("   等待任务完成...")
    time.sleep(0.1)  # 给调度器时间执行
    
    if task._event.is_set():
        result = task.wait(timeout=0)
        print(f"   任务完成: {result}")
        print(f"   吞吐量: {1/execution_time:.2f} tasks/sec")
    else:
        print("   任务未完成")
    
    # 测试多个任务
    print("\n2. 测试多个任务:")
    dsl = DSL(seed=42, workers=4)
    
    tasks = []
    for i in range(5):
        task = dsl.gen(f"task_{i}", prompt=f"计算 {i}+{i}", agent=f"agent_{i}").schedule()
        tasks.append(task)
    
    start_time = time.time()
    dsl.run(llm_callable)
    end_time = time.time()
    
    execution_time = end_time - start_time
    print(f"   执行时间: {execution_time:.6f}秒")
    
    # 等待任务完成
    print("   等待任务完成...")
    time.sleep(0.2)  # 给调度器时间执行
    
    successful_tasks = sum(1 for t in tasks if t._event.is_set())
    print(f"   成功任务数: {successful_tasks}/{len(tasks)}")
    
    if successful_tasks > 0:
        print(f"   吞吐量: {successful_tasks/execution_time:.2f} tasks/sec")
        print(f"   平均延迟: {execution_time/successful_tasks:.6f}秒")
    else:
        print("   没有任务完成")
    
    # 分析结果
    print("\n3. 结果分析:")
    print("   ⚠️  注意：这个测试使用的是降级策略（模拟响应）")
    print("   ⚠️  高吞吐量是因为没有真实的网络延迟")
    print("   ⚠️  真实API调用会有显著的网络延迟")
    
    if execution_time < 0.001:
        print("   ❌ 执行时间太短，不真实")
    else:
        print("   ✅ 执行时间合理")

def test_with_wait():
    """使用等待机制测试"""
    print("\n" + "=" * 50)
    print("⏳ 使用等待机制测试")
    print("=" * 50)
    
    dsl = DSL(seed=42, workers=2)
    
    # 创建任务
    task = dsl.gen("wait_test", prompt="计算 10+20", agent="wait_agent").schedule()
    
    start_time = time.time()
    dsl.run(llm_callable)
    
    # 等待任务完成
    print("等待任务完成...")
    result = task.wait(timeout=5.0)  # 等待最多5秒
    end_time = time.time()
    
    execution_time = end_time - start_time
    print(f"总执行时间: {execution_time:.6f}秒")
    print(f"任务结果: {result}")
    
    if result is not None:
        print(f"吞吐量: {1/execution_time:.2f} tasks/sec")
        print("✅ 任务成功完成")
    else:
        print("❌ 任务超时或失败")

def main():
    """主函数"""
    simple_test()
    test_with_wait()
    
    print("\n" + "=" * 50)
    print("🎯 结论:")
    print("=" * 50)
    print("1. 降级策略确实能工作，但性能数据不真实")
    print("2. 高吞吐量是因为没有网络延迟")
    print("3. 需要真实API密钥才能进行真实测试")
    print("4. 之前的基准测试结果需要重新评估")

if __name__ == "__main__":
    main()
