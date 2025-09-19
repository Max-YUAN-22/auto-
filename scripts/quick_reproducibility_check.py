#!/usr/bin/env python3
"""
快速可复现性检查脚本
Quick Reproducibility Check Script

这个脚本快速验证实验的可复现性，确保CCF A类会议标准。
"""

import os
import sys
import json
import time
import random
import numpy as np
import subprocess
import importlib
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_reproducible_environment():
    """设置可复现环境"""
    logger.info("🔧 设置可复现环境...")
    
    # 设置固定随机种子
    RANDOM_SEED = 42
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    os.environ['PYTHONHASHSEED'] = str(RANDOM_SEED)
    
    logger.info(f"✅ 随机种子设置为: {RANDOM_SEED}")
    return RANDOM_SEED

def check_environment():
    """检查环境配置"""
    logger.info("🔍 检查环境配置...")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        logger.error(f"❌ Python版本过低: {python_version.major}.{python_version.minor}")
        return False
    
    # 检查API密钥
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        logger.error("❌ OPENAI_API_KEY 未设置")
        return False
    
    if not api_key.startswith('sk-'):
        logger.error("❌ OPENAI_API_KEY 格式不正确")
        return False
    
    # 检查关键依赖
    required_packages = ['numpy', 'pandas', 'matplotlib', 'psutil']
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"❌ 缺少依赖包: {missing_packages}")
        return False
    
    logger.info("✅ 环境配置检查通过")
    return True

def run_simple_performance_test():
    """运行简单性能测试"""
    logger.info("🧪 运行简单性能测试...")
    
    try:
        # 导入我们的DSL框架
        sys.path.append('.')
        from dsl.dsl import DSL
        from core.llm import llm_callable
        
        # 创建DSL实例
        dsl = DSL(workers=2)
        dsl.use_llm(llm_callable)
        
        # 创建简单任务
        tasks = []
        for i in range(5):
            task = dsl.task(f"test_task_{i}")
            tasks.append(task)
        
        # 执行任务
        start_time = time.time()
        results = []
        for task in tasks:
            try:
                result = dsl.run(task)
                results.append(result)
            except Exception as e:
                logger.warning(f"任务执行失败: {e}")
        
        end_time = time.time()
        
        performance = {
            "throughput": len(results) / (end_time - start_time) if end_time > start_time else 0,
            "latency": (end_time - start_time) / len(results) if results else 0,
            "success_rate": len(results) / len(tasks),
            "task_count": len(results)
        }
        
        logger.info(f"✅ 性能测试完成: {performance}")
        return performance
        
    except Exception as e:
        logger.error(f"❌ 性能测试失败: {e}")
        return {
            "throughput": 0,
            "latency": 0,
            "success_rate": 0,
            "task_count": 0,
            "error": str(e)
        }

def verify_reproducibility():
    """验证可复现性"""
    logger.info("🔄 验证可复现性...")
    
    # 运行两次测试
    results = []
    for i in range(2):
        logger.info(f"   运行第 {i+1} 次测试...")
        
        # 重置随机种子
        random.seed(42)
        np.random.seed(42)
        
        result = run_simple_performance_test()
        results.append(result)
    
    # 检查一致性
    if len(results) < 2:
        return {"reproducible": False, "reason": "insufficient_runs"}
    
    # 比较关键指标
    throughput_diff = abs(results[0]["throughput"] - results[1]["throughput"])
    throughput_avg = (results[0]["throughput"] + results[1]["throughput"]) / 2
    
    if throughput_avg > 0:
        throughput_cv = throughput_diff / throughput_avg
    else:
        throughput_cv = 1.0
    
    # 10%的容差
    is_reproducible = throughput_cv < 0.1
    
    logger.info(f"   吞吐量差异: {throughput_cv:.2%}")
    logger.info(f"   可复现性: {'✅ 通过' if is_reproducible else '❌ 失败'}")
    
    return {
        "reproducible": is_reproducible,
        "throughput_cv": throughput_cv,
        "results": results
    }

def main():
    """主函数"""
    logger.info("🚀 开始快速可复现性检查")
    logger.info("=" * 50)
    
    # 设置可复现环境
    seed = setup_reproducible_environment()
    
    # 检查环境
    if not check_environment():
        logger.error("❌ 环境检查失败")
        sys.exit(1)
    
    # 验证可复现性
    reproducibility_result = verify_reproducibility()
    
    # 生成报告
    report = {
        "timestamp": time.time(),
        "random_seed": seed,
        "environment_check": True,
        "reproducibility": reproducibility_result,
        "status": "PASS" if reproducibility_result["reproducible"] else "FAIL"
    }
    
    # 保存报告
    os.makedirs("results", exist_ok=True)
    with open("results/quick_reproducibility_report.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    # 打印结果
    logger.info("📋 检查结果:")
    logger.info(f"   环境检查: ✅ 通过")
    logger.info(f"   可复现性: {'✅ 通过' if reproducibility_result['reproducible'] else '❌ 失败'}")
    logger.info(f"   总体状态: {report['status']}")
    
    if report['status'] == 'PASS':
        logger.info("🎉 可复现性检查通过！实验具有良好的可复现性。")
        sys.exit(0)
    else:
        logger.warning("⚠️  可复现性检查未通过，请检查环境配置。")
        sys.exit(1)

if __name__ == "__main__":
    main()


