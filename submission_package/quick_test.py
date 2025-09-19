#!/usr/bin/env python3
"""
快速测试脚本 - 验证实验框架是否正常工作
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from comprehensive_benchmark import ComprehensiveBenchmark

def main():
    print('🔬 运行快速测试确保系统正常...')
    
    # 创建基准测试实例
    benchmark = ComprehensiveBenchmark()
    
    # 修改配置为小规模测试
    benchmark.experiment_config = {
        'scenarios': ['business_analysis'],  # 1个场景
        'agent_counts': [1],  # 1个代理数量
        'frameworks': ['LangChain'],  # 1个框架
        'task_complexities': ['simple'],  # 1个复杂度
        'repetitions': 1  # 运行1次
    }
    
    total_tests = (len(benchmark.experiment_config['scenarios']) * 
                  len(benchmark.experiment_config['agent_counts']) * 
                  len(benchmark.experiment_config['frameworks']) * 
                  len(benchmark.experiment_config['task_complexities']) * 
                  benchmark.experiment_config['repetitions'])
    
    print(f'测试配置: {len(benchmark.experiment_config["scenarios"])}个场景, '
          f'{len(benchmark.experiment_config["agent_counts"])}个代理数量, '
          f'{len(benchmark.experiment_config["frameworks"])}个框架')
    print(f'总测试数: {total_tests}')
    print('预计耗时: 约2-5分钟')
    
    # 运行测试
    results = benchmark.run_comprehensive_benchmark()
    
    print('\n🎉 快速测试完成！')
    print(f'总测试数: {len(results["benchmark_results"])}')
    
    # 统计结果
    successful_tests = sum(1 for r in results['benchmark_results'] if r['status'] == 'success')
    failed_tests = len(results['benchmark_results']) - successful_tests
    success_rate = (successful_tests / len(results['benchmark_results'])) * 100
    
    print(f'成功测试: {successful_tests}')
    print(f'失败测试: {failed_tests}')
    print(f'成功率: {success_rate:.1f}%')
    
    # 显示详细结果
    for result in results['benchmark_results']:
        if result['status'] == 'success':
            print(f'✅ {result["framework"]}: 吞吐量={result["throughput"]:.3f} tasks/sec, '
                  f'延迟={result["avg_latency"]:.2f} ms, 内存={result["memory_usage"]:.2f} MB')
        else:
            print(f'❌ {result["framework"]}: 失败 - {result.get("error", "Unknown error")}')

if __name__ == "__main__":
    main()

