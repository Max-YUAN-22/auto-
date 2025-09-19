#!/usr/bin/env python3
"""
综合分析报告 - 解释性能差异
Comprehensive Analysis Report - Explaining Performance Differences
"""

import json
import numpy as np
from typing import Dict, List, Any

def load_results(file_path: str) -> Dict[str, Any]:
    """加载测试结果"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_comprehensive_results():
    """综合分析结果"""
    print("=" * 100)
    print("🔍 综合分析报告 - 解释性能差异")
    print("=" * 100)
    
    # 加载不同测试的结果
    try:
        fixed_results = load_results("results/fixed_api_benchmark_results.json")
        real_results = load_results("results/real_api_benchmark_results.json")
        print("✅ 成功加载所有测试结果")
    except FileNotFoundError as e:
        print(f"❌ 未找到测试结果文件: {e}")
        return
    
    print("\n📊 测试结果对比:")
    print("=" * 100)
    
    # 分析固定API测试结果
    print("\n1. 修复API调用问题后的测试结果:")
    print("-" * 50)
    
    fixed_stats = {}
    for result in fixed_results["benchmark_results"]:
        framework = result["framework"]
        if framework not in fixed_stats:
            fixed_stats[framework] = {"throughputs": [], "latencies": []}
        
        if result["status"] == "success":
            fixed_stats[framework]["throughputs"].append(result["throughput"])
            fixed_stats[framework]["latencies"].append(result["avg_latency"])
    
    for framework, stats in fixed_stats.items():
        if stats["throughputs"]:
            avg_throughput = np.mean(stats["throughputs"])
            avg_latency = np.mean(stats["latencies"])
            print(f"   {framework}: 吞吐量 {avg_throughput:.2f} tasks/sec, 延迟 {avg_latency*1000:.3f} ms")
    
    # 分析真实API测试结果
    print("\n2. 真实API调用测试结果:")
    print("-" * 50)
    
    real_stats = {}
    for result in real_results["benchmark_results"]:
        framework = result["framework"]
        if framework not in real_stats:
            real_stats[framework] = {"throughputs": [], "latencies": [], "api_types": []}
        
        if result["status"] == "success":
            real_stats[framework]["throughputs"].append(result["throughput"])
            real_stats[framework]["latencies"].append(result["avg_latency"])
            real_stats[framework]["api_types"].append(result.get("api_type", "unknown"))
    
    for framework, stats in real_stats.items():
        if stats["throughputs"]:
            avg_throughput = np.mean(stats["throughputs"])
            avg_latency = np.mean(stats["latencies"])
            api_type = stats["api_types"][0] if stats["api_types"] else "unknown"
            print(f"   {framework}: 吞吐量 {avg_throughput:.2f} tasks/sec, 延迟 {avg_latency*1000:.3f} ms, API类型: {api_type}")
    
    # 分析性能差异
    print("\n3. 性能差异分析:")
    print("-" * 50)
    
    if "Our DSL" in fixed_stats and "Our DSL" in real_stats:
        fixed_throughput = np.mean(fixed_stats["Our DSL"]["throughputs"])
        real_throughput = np.mean(real_stats["Our DSL"]["throughputs"])
        
        print(f"   Our DSL性能变化:")
        print(f"   修复后测试: {fixed_throughput:.2f} tasks/sec")
        print(f"   真实API测试: {real_throughput:.2f} tasks/sec")
        print(f"   性能差异: {fixed_throughput/real_throughput:.1f}x")
        
        if real_stats["Our DSL"]["api_types"][0] == "fallback":
            print("   ⚠️  真实API测试仍在使用降级策略")
    
    # 解释原因
    print("\n4. 原因分析:")
    print("-" * 50)
    print("   🔍 为什么之前没有这么高的效率？")
    print("   • 之前的测试使用了真实的API调用，有网络延迟")
    print("   • 修复后的测试使用了降级策略，没有网络延迟")
    print("   • 降级策略返回预定义的响应，执行极快")
    
    print("\n   🔍 降级策略能行吗？")
    print("   ✅ 降级策略的优点:")
    print("   • 确保系统在任何情况下都能工作")
    print("   • 提供快速的响应")
    print("   • 避免API调用失败导致的系统崩溃")
    print("   • 适合离线或API不可用的情况")
    
    print("\n   ⚠️  降级策略的局限性:")
    print("   • 不能提供真实的AI能力")
    print("   • 响应内容是预定义的，不够智能")
    print("   • 不适合需要真实AI推理的场景")
    print("   • 性能数据不能代表真实使用情况")
    
    # 真实性能评估
    print("\n5. 真实性能评估:")
    print("-" * 50)
    
    if "Our DSL" in real_stats:
        our_dsl_throughput = np.mean(real_stats["Our DSL"]["throughputs"])
        our_dsl_latency = np.mean(real_stats["Our DSL"]["latencies"])
        
        print(f"   Our DSL真实性能:")
        print(f"   • 吞吐量: {our_dsl_throughput:.2f} tasks/sec")
        print(f"   • 延迟: {our_dsl_latency*1000:.3f} ms")
        
        if real_stats["Our DSL"]["api_types"][0] == "fallback":
            print("   • 注意: 仍在使用降级策略，不是真实API调用")
        else:
            print("   • 使用真实API调用")
    
    # 与其他框架对比
    print("\n6. 与其他框架对比:")
    print("-" * 50)
    
    other_frameworks = [f for f in real_stats.keys() if f != "Our DSL"]
    if other_frameworks:
        best_other_throughput = max(np.mean(real_stats[f]["throughputs"]) for f in other_frameworks)
        best_other_latency = min(np.mean(real_stats[f]["latencies"]) for f in other_frameworks)
        
        if "Our DSL" in real_stats:
            our_throughput = np.mean(real_stats["Our DSL"]["throughputs"])
            our_latency = np.mean(real_stats["Our DSL"]["latencies"])
            
            print(f"   Our DSL vs 其他框架:")
            print(f"   • 吞吐量优势: {our_throughput/best_other_throughput:.1f}x")
            print(f"   • 延迟优势: {best_other_latency/our_latency:.1f}x")
    
    # 结论和建议
    print("\n7. 结论和建议:")
    print("-" * 50)
    print("   🎯 结论:")
    print("   • 修复API调用问题后，Our DSL确实有性能提升")
    print("   • 但高吞吐量主要来自降级策略，不是真实AI能力")
    print("   • 降级策略确保了系统稳定性，但性能数据不真实")
    print("   • 需要真实API密钥才能进行公平的性能对比")
    
    print("\n   💡 建议:")
    print("   • 设置有效的DEEPSEEK_API_KEY进行真实测试")
    print("   • 在论文中明确说明测试条件（API vs 降级策略）")
    print("   • 降级策略可以作为系统稳定性的保障")
    print("   • 真实性能测试需要包含网络延迟")

def main():
    """主函数"""
    analyze_comprehensive_results()
    
    print("\n" + "=" * 100)
    print("✅ 分析完成！")
    print("=" * 100)

if __name__ == "__main__":
    main()
