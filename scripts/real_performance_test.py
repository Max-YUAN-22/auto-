#!/usr/bin/env python3
"""
真实性能验证测试
Real Performance Verification Test
"""

import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dsl.dsl import DSL
from core.robust_llm import llm_callable, test_api_connection

def test_real_performance():
    """测试真实性能"""
    print("🔍 真实性能验证测试")
    print("=" * 60)
    
    # 1. 测试API连接
    print("1. 测试API连接状态:")
    api_result = test_api_connection()
    print(f"   API密钥设置: {api_result['api_key_set']}")
    print(f"   客户端可用: {api_result['client_available']}")
    print(f"   响应: {api_result['response']}")
    print(f"   延迟: {api_result['latency']:.3f}秒")
    
    # 2. 测试单个任务
    print("\n2. 测试单个任务执行:")
    dsl = DSL(seed=42, workers=1)
    
    start_time = time.time()
    task = dsl.gen("test_task", prompt="计算 1+1", agent="test_agent").schedule()
    dsl.run(llm_callable)
    end_time = time.time()
    
    print(f"   执行时间: {end_time - start_time:.6f}秒")
    print(f"   任务状态: {task._event.is_set()}")
    if task._event.is_set():
        result = task.wait(timeout=0)
        print(f"   任务结果: {result}")
    
    # 3. 测试多个任务
    print("\n3. 测试多个任务执行:")
    dsl = DSL(seed=42, workers=4)
    
    tasks = []
    for i in range(5):
        task = dsl.gen(f"task_{i}", prompt=f"计算 {i}+{i}", agent=f"agent_{i}").schedule()
        tasks.append(task)
    
    start_time = time.time()
    dsl.run(llm_callable)
    end_time = time.time()
    
    execution_time = end_time - start_time
    successful_tasks = sum(1 for t in tasks if t._event.is_set())
    
    print(f"   执行时间: {execution_time:.6f}秒")
    print(f"   成功任务数: {successful_tasks}/{len(tasks)}")
    print(f"   吞吐量: {successful_tasks/execution_time:.2f} tasks/sec")
    print(f"   平均延迟: {execution_time/successful_tasks:.6f}秒" if successful_tasks > 0 else "   平均延迟: N/A")
    
    # 4. 分析结果
    print("\n4. 结果分析:")
    if api_result['api_key_set']:
        print("   ✅ 使用真实API调用")
    else:
        print("   ⚠️  使用降级策略（模拟响应）")
        print("   ⚠️  高吞吐量是因为没有真实的网络延迟")
    
    print(f"   实际吞吐量: {successful_tasks/execution_time:.2f} tasks/sec")
    print(f"   这个数字是否合理: {'是' if execution_time > 0.001 else '否（太快了）'}")

def test_with_real_api():
    """使用真实API测试"""
    print("\n" + "=" * 60)
    print("🌐 使用真实API测试")
    print("=" * 60)
    
    # 设置一个测试用的API密钥（如果用户提供）
    test_api_key = input("请输入DeepSeek API密钥进行真实测试（或按Enter跳过）: ").strip()
    
    if test_api_key:
        os.environ['DEEPSEEK_API_KEY'] = test_api_key
        
        # 重新测试
        print("\n使用真实API重新测试...")
        api_result = test_api_connection()
        print(f"API连接结果: {api_result}")
        
        if api_result['success']:
            print("✅ 真实API测试成功")
            # 运行真实性能测试
            dsl = DSL(seed=42, workers=1)
            start_time = time.time()
            task = dsl.gen("real_test", prompt="请计算 15+27 的结果", agent="real_agent").schedule()
            dsl.run(llm_callable)
            end_time = time.time()
            
            print(f"真实API执行时间: {end_time - start_time:.3f}秒")
            if task._event.is_set():
                result = task.wait(timeout=0)
                print(f"真实API结果: {result}")
        else:
            print("❌ 真实API测试失败")
    else:
        print("跳过真实API测试")

def main():
    """主函数"""
    test_real_performance()
    test_with_real_api()
    
    print("\n" + "=" * 60)
    print("🎯 结论:")
    print("=" * 60)
    print("1. 如果使用降级策略，高吞吐量是正常的（没有网络延迟）")
    print("2. 真实API调用会有网络延迟，吞吐量会显著降低")
    print("3. 需要设置有效的DEEPSEEK_API_KEY才能进行真实测试")
    print("4. 降级策略确保了系统的稳定性，但性能数据不是真实的")

if __name__ == "__main__":
    main()
