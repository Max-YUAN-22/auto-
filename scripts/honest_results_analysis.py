#!/usr/bin/env python3
"""
真实API测试结果分析
Real API Test Results Analysis
"""

import json
import numpy as np
from typing import Dict, List, Any

def load_results(file_path: str) -> Dict[str, Any]:
    """加载测试结果"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_honest_results():
    """分析真实API测试结果"""
    print("=" * 100)
    print("🎯 真实API测试结果分析（学术诚信版本）")
    print("=" * 100)
    
    try:
        results = load_results("results/honest_api_benchmark_results.json")
        print("✅ 成功加载真实API测试结果")
    except FileNotFoundError:
        print("❌ 未找到真实API测试结果文件")
        return
    
    # 分析结果
    framework_stats = {}
    for result in results["benchmark_results"]:
        framework = result["framework"]
        if framework not in framework_stats:
            framework_stats[framework] = {
                "throughputs": [],
                "latencies": [],
                "success_rates": [],
                "memory_usage": [],
                "execution_times": []
            }
        
        if result["status"] == "success":
            framework_stats[framework]["throughputs"].append(result["throughput"])
            framework_stats[framework]["latencies"].append(result["avg_latency"])
            framework_stats[framework]["success_rates"].append(result["success_rate"])
            framework_stats[framework]["memory_usage"].append(result["memory_usage"])
            framework_stats[framework]["execution_times"].append(result["execution_time"])
    
    print(f"\n📊 真实API性能对比:")
    print(f"{'框架':<15} {'平均吞吐量':<15} {'平均延迟':<15} {'平均内存':<15} {'成功率':<15}")
    print("-" * 80)
    
    for framework, stats in framework_stats.items():
        if stats["throughputs"]:
            avg_throughput = np.mean(stats["throughputs"])
            avg_latency = np.mean(stats["latencies"])
            avg_memory = np.mean(stats["memory_usage"])
            avg_success_rate = np.mean(stats["success_rates"])
            avg_execution_time = np.mean(stats["execution_times"])
            
            print(f"{framework:<15} {avg_throughput:<15.2f} {avg_latency*1000:<15.3f} {avg_memory:<15.2f} {avg_success_rate:<15.2%}")
    
    # 分析Our DSL的表现
    if "Our DSL" in framework_stats:
        our_dsl_stats = framework_stats["Our DSL"]
        print(f"\n🔍 Our DSL真实性能分析:")
        print(f"   平均吞吐量: {np.mean(our_dsl_stats['throughputs']):.2f} tasks/sec")
        print(f"   平均延迟: {np.mean(our_dsl_stats['latencies'])*1000:.3f} ms")
        print(f"   平均执行时间: {np.mean(our_dsl_stats['execution_times']):.3f} 秒")
        print(f"   成功率: {np.mean(our_dsl_stats['success_rates']):.2%}")
        
        # 与其他框架对比
        other_frameworks = [name for name in framework_stats.keys() if name != "Our DSL"]
        if other_frameworks:
            best_other_throughput = max(np.mean(framework_stats[f]["throughputs"]) for f in other_frameworks)
            best_other_latency = min(np.mean(framework_stats[f]["latencies"]) for f in other_frameworks)
            
            our_throughput = np.mean(our_dsl_stats["throughputs"])
            our_latency = np.mean(our_dsl_stats["latencies"])
            
            print(f"\n📈 与其他框架对比:")
            print(f"   吞吐量优势: {our_throughput/best_other_throughput:.1f}x")
            print(f"   延迟优势: {best_other_latency/our_latency:.1f}x")
    
    # 性能瓶颈分析
    print(f"\n🔍 性能瓶颈分析:")
    print(f"   1. 网络延迟: 所有框架都受到网络延迟影响")
    print(f"   2. API调用开销: 每次API调用都有固定开销")
    print(f"   3. 并发处理: Our DSL的并发处理能力")
    print(f"   4. 任务调度: 任务调度的效率")
    
    # 优化建议
    print(f"\n💡 性能优化建议:")
    print(f"   1. 优化任务调度算法")
    print(f"   2. 改进并发处理机制")
    print(f"   3. 优化内存使用")
    print(f"   4. 减少不必要的开销")
    
    return framework_stats

def main():
    """主函数"""
    framework_stats = analyze_honest_results()
    
    print("\n" + "=" * 100)
    print("✅ 分析完成！")
    print("=" * 100)

if __name__ == "__main__":
    main()
