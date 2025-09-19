#!/usr/bin/env python3
"""
性能对比分析 - 展示真实性能提升
Performance Comparison Analysis - Show Real Performance Improvements
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, List, Any

def load_benchmark_results(file_path: str) -> Dict[str, Any]:
    """加载基准测试结果"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_performance(results: Dict[str, Any]) -> Dict[str, Any]:
    """分析性能数据"""
    framework_stats = {}
    
    for result in results["benchmark_results"]:
        framework = result["framework"]
        if framework not in framework_stats:
            framework_stats[framework] = {
                "throughputs": [],
                "latencies": [],
                "memory_usage": [],
                "success_rates": [],
                "execution_times": []
            }
        
        if result["status"] == "success":
            framework_stats[framework]["throughputs"].append(result["throughput"])
            framework_stats[framework]["latencies"].append(result["avg_latency"])
            framework_stats[framework]["memory_usage"].append(result["memory_usage"])
            framework_stats[framework]["success_rates"].append(result["success_rate"])
            framework_stats[framework]["execution_times"].append(result["execution_time"])
    
    # 计算统计指标
    analysis = {}
    for framework, stats in framework_stats.items():
        analysis[framework] = {
            "avg_throughput": np.mean(stats["throughputs"]),
            "max_throughput": np.max(stats["throughputs"]),
            "min_throughput": np.min(stats["throughputs"]),
            "std_throughput": np.std(stats["throughputs"]),
            "avg_latency": np.mean(stats["latencies"]),
            "avg_memory": np.mean(stats["memory_usage"]),
            "avg_success_rate": np.mean(stats["success_rates"]),
            "total_tests": len(stats["throughputs"])
        }
    
    return analysis

def compare_performance(old_results: Dict[str, Any], new_results: Dict[str, Any]) -> Dict[str, Any]:
    """对比新旧性能"""
    old_analysis = analyze_performance(old_results)
    new_analysis = analyze_performance(new_results)
    
    comparison = {}
    
    # 对比Our DSL的性能提升
    if "Our DSL" in old_analysis and "Our Fast DSL" in new_analysis:
        old_dsl = old_analysis["Our DSL"]
        new_dsl = new_analysis["Our Fast DSL"]
        
        comparison["Our DSL Performance Improvement"] = {
            "throughput_improvement": (new_dsl["avg_throughput"] - old_dsl["avg_throughput"]) / old_dsl["avg_throughput"] * 100,
            "latency_reduction": (old_dsl["avg_latency"] - new_dsl["avg_latency"]) / old_dsl["avg_latency"] * 100,
            "memory_efficiency": (old_dsl["avg_memory"] - new_dsl["avg_memory"]) / old_dsl["avg_memory"] * 100,
            "old_throughput": old_dsl["avg_throughput"],
            "new_throughput": new_dsl["avg_throughput"],
            "old_latency": old_dsl["avg_latency"],
            "new_latency": new_dsl["avg_latency"]
        }
    
    # 对比所有框架
    comparison["Framework Rankings"] = {}
    
    # 吞吐量排名
    throughput_ranking = sorted(new_analysis.items(), key=lambda x: x[1]["avg_throughput"], reverse=True)
    comparison["Framework Rankings"]["Throughput"] = [(name, stats["avg_throughput"]) for name, stats in throughput_ranking]
    
    # 延迟排名
    latency_ranking = sorted(new_analysis.items(), key=lambda x: x[1]["avg_latency"])
    comparison["Framework Rankings"]["Latency"] = [(name, stats["avg_latency"]) for name, stats in latency_ranking]
    
    # 内存效率排名
    memory_ranking = sorted(new_analysis.items(), key=lambda x: x[1]["avg_memory"])
    comparison["Framework Rankings"]["Memory Efficiency"] = [(name, stats["avg_memory"]) for name, stats in memory_ranking]
    
    return comparison

def print_performance_report(comparison: Dict[str, Any]):
    """打印性能报告"""
    print("=" * 80)
    print("🚀 高性能DSL基准测试结果分析")
    print("=" * 80)
    
    if "Our DSL Performance Improvement" in comparison:
        improvement = comparison["Our DSL Performance Improvement"]
        print(f"\n📈 Our DSL性能提升:")
        print(f"   吞吐量提升: {improvement['throughput_improvement']:.1f}%")
        print(f"   延迟减少: {improvement['latency_reduction']:.1f}%")
        print(f"   内存效率提升: {improvement['memory_efficiency']:.1f}%")
        print(f"   旧吞吐量: {improvement['old_throughput']:.2f} tasks/sec")
        print(f"   新吞吐量: {improvement['new_throughput']:.2f} tasks/sec")
        print(f"   旧延迟: {improvement['old_latency']*1000:.3f} ms")
        print(f"   新延迟: {improvement['new_latency']*1000:.3f} ms")
    
    print(f"\n🏆 框架性能排名:")
    
    if "Framework Rankings" in comparison:
        rankings = comparison["Framework Rankings"]
        
        print(f"\n   吞吐量排名 (tasks/sec):")
        for i, (name, throughput) in enumerate(rankings["Throughput"], 1):
            print(f"     {i}. {name}: {throughput:.2f}")
        
        print(f"\n   延迟排名 (秒):")
        for i, (name, latency) in enumerate(rankings["Latency"], 1):
            print(f"     {i}. {name}: {latency*1000:.3f} ms")
        
        print(f"\n   内存效率排名 (MB):")
        for i, (name, memory) in enumerate(rankings["Memory Efficiency"], 1):
            print(f"     {i}. {name}: {memory:.2f}")

def main():
    """主函数"""
    print("📊 加载基准测试结果...")
    
    # 加载旧版本结果
    try:
        old_results = load_benchmark_results("results/perfectly_fair_benchmark_results.json")
        print("✅ 已加载原始DSL基准测试结果")
    except FileNotFoundError:
        print("❌ 未找到原始DSL基准测试结果")
        old_results = None
    
    # 加载新版本结果
    try:
        new_results = load_benchmark_results("results/high_performance_benchmark_results.json")
        print("✅ 已加载高性能DSL基准测试结果")
    except FileNotFoundError:
        print("❌ 未找到高性能DSL基准测试结果")
        return
    
    # 分析性能
    print("\n🔍 分析性能数据...")
    new_analysis = analyze_performance(new_results)
    
    # 对比性能
    if old_results:
        print("📈 对比性能提升...")
        comparison = compare_performance(old_results, new_results)
        print_performance_report(comparison)
    else:
        print("\n📊 当前性能分析:")
        for framework, stats in new_analysis.items():
            print(f"\n   {framework}:")
            print(f"     平均吞吐量: {stats['avg_throughput']:.2f} tasks/sec")
            print(f"     平均延迟: {stats['avg_latency']*1000:.3f} ms")
            print(f"     平均内存使用: {stats['avg_memory']:.2f} MB")
            print(f"     成功率: {stats['avg_success_rate']:.2%}")
    
    print("\n" + "=" * 80)
    print("✅ 性能分析完成！")

if __name__ == "__main__":
    main()
