#!/usr/bin/env python3
"""
快速内存监控测试 - 小规模试验
"""

import sys
import os
import time
import psutil
import gc
import threading
from contextlib import contextmanager

# 设置日志
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QuickMemoryTracker:
    """快速内存跟踪器"""
    
    def __init__(self):
        self.memory_tracker = {}
    
    @contextmanager
    def memory_tracking(self, test_name: str):
        """内存跟踪上下文管理器"""
        class MemoryTracker:
            def __init__(self, parent, test_name):
                self.parent = parent
                self.test_name = test_name
                self.initial_memory = None
                self.peak_memory = 0
                self.monitoring_active = False
                
            def __enter__(self):
                # 强制垃圾回收
                gc.collect()
                process = psutil.Process()
                self.initial_memory = process.memory_info().rss / 1024 / 1024  # MB
                self.peak_memory = self.initial_memory
                self.monitoring_active = True
                
                # 启动内存监控线程
                self.monitor_thread = threading.Thread(target=self._monitor_memory)
                self.monitor_thread.daemon = True
                self.monitor_thread.start()
                
                logger.info(f"🧪 {self.test_name} - 初始内存: {self.initial_memory:.2f} MB")
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                # 停止内存监控
                self.monitoring_active = False
                if hasattr(self, 'monitor_thread'):
                    self.monitor_thread.join(timeout=1.0)
                
                process = psutil.Process()
                final_memory = process.memory_info().rss / 1024 / 1024  # MB
                
                # 计算内存使用
                memory_usage = max(0, self.peak_memory - self.initial_memory)
                
                # 记录结果
                self.parent.memory_tracker[self.test_name] = memory_usage
                
                logger.info(f"📊 {self.test_name} 结果:")
                logger.info(f"  初始内存: {self.initial_memory:.2f} MB")
                logger.info(f"  峰值内存: {self.peak_memory:.2f} MB") 
                logger.info(f"  最终内存: {final_memory:.2f} MB")
                logger.info(f"  内存使用: {memory_usage:.2f} MB")
            
            def _monitor_memory(self):
                """内存监控线程"""
                process = psutil.Process()
                while self.monitoring_active:
                    try:
                        current_memory = process.memory_info().rss / 1024 / 1024  # MB
                        if current_memory > self.peak_memory:
                            self.peak_memory = current_memory
                        time.sleep(0.1)  # 每100ms检查一次
                    except:
                        break
        
        tracker = MemoryTracker(self, test_name)
        try:
            yield tracker
        finally:
            pass

def simulate_memory_usage():
    """模拟内存使用"""
    # 创建一些数据来消耗内存
    data = []
    for i in range(1000):
        data.append([j for j in range(100)])  # 每个元素约400字节
        if i % 100 == 0:
            time.sleep(0.01)  # 模拟处理时间
    return data

def test_memory_tracking():
    """测试内存跟踪功能"""
    logger.info("🚀 开始快速内存监控测试")
    
    tracker = QuickMemoryTracker()
    
    # 测试1: 无内存使用
    logger.info("\n📝 测试1: 无内存使用")
    with tracker.memory_tracking("无内存使用"):
        time.sleep(0.5)
    
    # 测试2: 少量内存使用
    logger.info("\n📝 测试2: 少量内存使用")
    with tracker.memory_tracking("少量内存使用"):
        data1 = simulate_memory_usage()
        time.sleep(0.5)
        del data1
    
    # 测试3: 大量内存使用
    logger.info("\n📝 测试3: 大量内存使用")
    with tracker.memory_tracking("大量内存使用"):
        data2 = []
        for i in range(5000):  # 更大的数据集
            data2.append([j for j in range(200)])
            if i % 500 == 0:
                time.sleep(0.01)
        time.sleep(0.5)
        del data2
    
    # 显示结果
    logger.info("\n📈 测试结果总结:")
    for test_name, memory_usage in tracker.memory_tracker.items():
        status = "✅" if memory_usage > 0 else "❌"
        logger.info(f"  {status} {test_name}: {memory_usage:.2f} MB")
    
    # 检查是否有任何测试显示内存使用
    has_memory_usage = any(usage > 0 for usage in tracker.memory_tracker.values())
    
    if has_memory_usage:
        logger.info("\n🎉 内存监控修复成功！能够正确检测到内存使用")
        return True
    else:
        logger.warning("\n⚠️ 内存监控仍有问题，所有测试都显示0 MB")
        return False

if __name__ == "__main__":
    success = test_memory_tracking()
    if success:
        print("\n✅ 内存监控修复验证成功！")
    else:
        print("\n❌ 内存监控修复验证失败，需要进一步调试")
