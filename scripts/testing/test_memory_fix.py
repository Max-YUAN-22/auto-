#!/usr/bin/env python3
"""
测试修复后的内存监控功能
"""

import sys
import os
sys.path.append('submission_package')

from comprehensive_benchmark import ComprehensiveBenchmark
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_memory_monitoring():
    """测试内存监控功能"""
    logger.info("🧪 开始测试内存监控功能")
    
    # 创建基准测试实例
    benchmark = ComprehensiveBenchmark()
    
    # 测试一个简单的场景
    logger.info("📊 测试Our DSL框架内存监控...")
    result = benchmark.test_our_dsl_real_api("business_analysis", 1, "simple")
    
    logger.info("📈 测试结果:")
    logger.info(f"  框架: {result['framework']}")
    logger.info(f"  场景: {result['scenario']}")
    logger.info(f"  智能体数量: {result['agent_count']}")
    logger.info(f"  执行时间: {result['execution_time']:.2f}s")
    logger.info(f"  吞吐量: {result['throughput']:.4f} tasks/sec")
    logger.info(f"  内存使用: {result['memory_usage']:.2f} MB")
    logger.info(f"  状态: {result['status']}")
    
    # 检查内存使用是否大于0
    if result['memory_usage'] > 0:
        logger.info("✅ 内存监控修复成功！内存使用数据正确记录")
        return True
    else:
        logger.warning("❌ 内存监控仍有问题，内存使用仍为0")
        return False

if __name__ == "__main__":
    success = test_memory_monitoring()
    if success:
        print("\n🎉 内存监控修复成功！")
    else:
        print("\n⚠️ 内存监控仍需进一步调试")
