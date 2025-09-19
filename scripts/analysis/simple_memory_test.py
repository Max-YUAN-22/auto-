#!/usr/bin/env python3
"""
简单内存监控测试
"""

import psutil
import gc
import time

def test_memory_measurement():
    """测试内存测量功能"""
    print("🧪 开始内存测量测试")
    
    # 测试1: 基础内存测量
    gc.collect()
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    print(f"初始内存: {initial_memory:.2f} MB")
    
    # 测试2: 创建一些数据消耗内存
    data = []
    for i in range(1000):
        data.append([j for j in range(100)])
        if i % 200 == 0:
            current_memory = process.memory_info().rss / 1024 / 1024
            print(f"  创建数据中... 当前内存: {current_memory:.2f} MB")
    
    peak_memory = process.memory_info().rss / 1024 / 1024
    print(f"峰值内存: {peak_memory:.2f} MB")
    
    # 测试3: 删除数据
    del data
    gc.collect()
    final_memory = process.memory_info().rss / 1024 / 1024
    print(f"最终内存: {final_memory:.2f} MB")
    
    # 计算内存使用
    memory_usage = max(0, peak_memory - initial_memory)
    print(f"内存使用: {memory_usage:.2f} MB")
    
    if memory_usage > 0:
        print("✅ 内存测量功能正常！")
        return True
    else:
        print("❌ 内存测量可能有问题")
        return False

if __name__ == "__main__":
    test_memory_measurement()
