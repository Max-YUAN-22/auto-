#!/usr/bin/env python3
"""
真正公平测试结果分析
Truly Fair Test Results Analysis
"""

import json
import numpy as np
from typing import Dict, List, Any

def load_results(file_path: str) -> Dict[str, Any]:
    """加载测试结果"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_truly_fair_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """分析真正公平的测试结果"""
    framework_stats = {}
    
    for result in results["benchmark_results"]:
        framework = result["framework"]
        if framework not in framework_stats:
            framework_stats[framework] = {
                "throughputs": [],
                "latencies": [],
                "memory_usage": [],
                "success_rates": [],
                "execution_times": [],
                "successful_tasks": []
            }
        
        if result["status"] == "success":
            framework_stats[framework]["throughputs"].append(result["throughput"])
            framework_stats[framework]["latencies"].append(result["avg_latency"])
            framework_stats[framework]["memory_usage"].append(result["memory_usage"])
            framework_stats[framework]["success_rates"].append(result["success_rate"])
            framework_stats[framework]["execution_times"].append(result["execution_time"])
            framework_stats[framework]["successful_tasks"].append(result["successful_tasks"])
    
    # 计算统计指标
    analysis = {}
    for framework, stats in framework_stats.items():
        if stats["throughputs"]:  # 确保有数据
            analysis[framework] = {
                "avg_throughput": np.mean(stats["throughputs"]),
                "max_throughput": np.max(stats["throughputs"]),
                "min_throughput": np.min(stats["throughputs"]),
                "avg_latency": np.mean(stats["latencies"]),
                "avg_memory": np.mean(stats["memory_usage"]),
                "avg_success_rate": np.mean(stats["success_rates"]),
                "total_tests": len(stats["throughputs"]),
                "total_successful_tasks": sum(stats["successful_tasks"])
            }
    
    return analysis

def print_detailed_analysis(analysis: Dict[str, Any]):
    """打印详细分析"""
    print("=" * 80)
    print("🎯 真正公平基准测试结果分析")
    print("=" * 80)
    
    print(f"\n📊 框架性能对比:")
    print(f"{'框架':<15} {'平均吞吐量':<15} {'平均延迟':<15} {'平均内存':<15} {'成功率':<15}")
    print("-" * 80)
    
    for framework, stats in analysis.items():
        print(f"{framework:<15} {stats['avg_throughput']:<15.2f} {stats['avg_latency']*1000:<15.3f} {stats['avg_memory']:<15.2f} {stats['avg_success_rate']:<15.2%}")
    
    print(f"\n🏆 性能排名:")
    
    # 吞吐量排名
    throughput_ranking = sorted(analysis.items(), key=lambda x: x[1]["avg_throughput"], reverse=True)
    print(f"\n   吞吐量排名 (tasks/sec):")
    for i, (name, stats) in enumerate(throughput_ranking, 1):
        print(f"     {i}. {name}: {stats['avg_throughput']:.2f}")
    
    # 延迟排名
    latency_ranking = sorted(analysis.items(), key=lambda x: x[1]["avg_latency"])
    print(f"\n   延迟排名 (ms):")
    for i, (name, stats) in enumerate(latency_ranking, 1):
        print(f"     {i}. {name}: {stats['avg_latency']*1000:.3f}")
    
    # 内存效率排名
    memory_ranking = sorted(analysis.items(), key=lambda x: x[1]["avg_memory"])
    print(f"\n   内存效率排名 (MB):")
    for i, (name, stats) in enumerate(memory_ranking, 1):
        print(f"     {i}. {name}: {stats['avg_memory']:.2f}")
    
    # 成功率排名
    success_ranking = sorted(analysis.items(), key=lambda x: x[1]["avg_success_rate"], reverse=True)
    print(f"\n   成功率排名:")
    for i, (name, stats) in enumerate(success_ranking, 1):
        print(f"     {i}. {name}: {stats['avg_success_rate']:.2%}")
    
    # 分析Our DSL的表现
    if "Our DSL" in analysis:
        our_dsl_stats = analysis["Our DSL"]
        print(f"\n🔍 Our DSL详细分析:")
        print(f"   平均吞吐量: {our_dsl_stats['avg_throughput']:.2f} tasks/sec")
        print(f"   平均延迟: {our_dsl_stats['avg_latency']*1000:.3f} ms")
        print(f"   平均内存使用: {our_dsl_stats['avg_memory']:.2f} MB")
        print(f"   成功率: {our_dsl_stats['avg_success_rate']:.2%}")
        print(f"   总测试数: {our_dsl_stats['total_tests']}")
        print(f"   成功任务数: {our_dsl_stats['total_successful_tasks']}")
        
        # 与其他框架对比
        other_frameworks = [name for name in analysis.keys() if name != "Our DSL"]
        if other_frameworks:
            best_throughput = max(analysis[f]["avg_throughput"] for f in other_frameworks)
            best_latency = min(analysis[f]["avg_latency"] for f in other_frameworks)
            best_memory = min(analysis[f]["avg_memory"] for f in other_frameworks)
            
            print(f"\n📈 与最佳性能对比:")
            print(f"   吞吐量差距: {our_dsl_stats['avg_throughput']/best_throughput:.2%}")
            print(f"   延迟差距: {our_dsl_stats['avg_latency']/best_latency:.2%}")
            print(f"   内存差距: {our_dsl_stats['avg_memory']/best_memory:.2%}")

def main():
    """主函数"""
    print("📊 加载真正公平基准测试结果...")
    
    try:
        results = load_results("results/truly_fair_benchmark_results.json")
        print("✅ 成功加载真正公平基准测试结果")
    except FileNotFoundError:
        print("❌ 未找到真正公平基准测试结果文件")
        return
    
    print("\n🔍 分析测试结果...")
    analysis = analyze_truly_fair_results(results)
    
    if not analysis:
        print("❌ 没有有效的测试结果")
        return
    
    print_detailed_analysis(analysis)
    
    print("\n" + "=" * 80)
    print("✅ 分析完成！")

if __name__ == "__main__":
    main()
