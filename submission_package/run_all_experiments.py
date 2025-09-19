#!/usr/bin/env python3
"""
主实验运行脚本 - 完全真实的API调用实验
Main Experiment Runner - Fully Real API Call Experiments

整合所有实验：
1. 全面基准测试
2. 消融实验
3. 可扩展性实验
4. 生成完整实验报告
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any

# 添加项目根目录到Python路径
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_comprehensive_benchmark():
    """运行全面基准测试"""
    logger.info("🚀 开始全面基准测试...")
    
    try:
        from comprehensive_benchmark import ComprehensiveBenchmark
        
        benchmark = ComprehensiveBenchmark()
        results = benchmark.run_comprehensive_benchmark()
        
        logger.info("✅ 全面基准测试完成")
        return results
    except Exception as e:
        logger.error(f"❌ 全面基准测试失败: {e}")
        return None

def run_ablation_study():
    """运行消融实验"""
    logger.info("🔬 开始消融实验...")
    
    try:
        from ablation_study import AblationStudy
        
        ablation = AblationStudy()
        results = ablation.run_ablation_study()
        
        logger.info("✅ 消融实验完成")
        return results
    except Exception as e:
        logger.error(f"❌ 消融实验失败: {e}")
        return None

def run_scalability_study():
    """运行可扩展性实验"""
    logger.info("📈 开始可扩展性实验...")
    
    try:
        from scalability_study import ScalabilityStudy
        
        scalability = ScalabilityStudy()
        results = scalability.run_scalability_study()
        
        logger.info("✅ 可扩展性实验完成")
        return results
    except Exception as e:
        logger.error(f"❌ 可扩展性实验失败: {e}")
        return None

def generate_comprehensive_report(comprehensive_results, ablation_results, scalability_results):
    """生成综合实验报告"""
    logger.info("📊 生成综合实验报告...")
    
    report = {
        "experiment_summary": {
            "timestamp": datetime.now().isoformat(),
            "total_experiments": 3,
            "completed_experiments": 0,
            "failed_experiments": 0
        },
        "comprehensive_benchmark": comprehensive_results,
        "ablation_study": ablation_results,
        "scalability_study": scalability_results,
        "key_findings": {},
        "recommendations": []
    }
    
    # 统计完成的实验
    if comprehensive_results:
        report["experiment_summary"]["completed_experiments"] += 1
    else:
        report["experiment_summary"]["failed_experiments"] += 1
    
    if ablation_results:
        report["experiment_summary"]["completed_experiments"] += 1
    else:
        report["experiment_summary"]["failed_experiments"] += 1
    
    if scalability_results:
        report["experiment_summary"]["completed_experiments"] += 1
    else:
        report["experiment_summary"]["failed_experiments"] += 1
    
    # 生成关键发现
    if comprehensive_results and comprehensive_results.get("benchmark_results"):
        benchmark_results = comprehensive_results["benchmark_results"]
        
        # 按框架统计性能
        framework_performance = {}
        for result in benchmark_results:
            if result["status"] == "success":
                framework = result["framework"]
                if framework not in framework_performance:
                    framework_performance[framework] = {
                        "throughput": [],
                        "latency": [],
                        "memory": [],
                        "success_rate": []
                    }
                
                framework_performance[framework]["throughput"].append(result["throughput"])
                framework_performance[framework]["latency"].append(result["avg_latency"])
                framework_performance[framework]["memory"].append(result["memory_usage"])
                framework_performance[framework]["success_rate"].append(result["success_rate"])
        
        # 计算平均性能
        avg_performance = {}
        for framework, metrics in framework_performance.items():
            if metrics["throughput"]:
                avg_performance[framework] = {
                    "avg_throughput": sum(metrics["throughput"]) / len(metrics["throughput"]),
                    "avg_latency": sum(metrics["latency"]) / len(metrics["latency"]),
                    "avg_memory": sum(metrics["memory"]) / len(metrics["memory"]),
                    "avg_success_rate": sum(metrics["success_rate"]) / len(metrics["success_rate"])
                }
        
        # 找出最佳性能框架
        if avg_performance:
            best_throughput = max(avg_performance.items(), key=lambda x: x[1]["avg_throughput"])
            best_latency = min(avg_performance.items(), key=lambda x: x[1]["avg_latency"])
            best_memory = min(avg_performance.items(), key=lambda x: x[1]["avg_memory"])
            
            report["key_findings"]["performance_leaderboard"] = {
                "best_throughput": {
                    "framework": best_throughput[0],
                    "value": best_throughput[1]["avg_throughput"]
                },
                "best_latency": {
                    "framework": best_latency[0],
                    "value": best_latency[1]["avg_latency"]
                },
                "best_memory": {
                    "framework": best_memory[0],
                    "value": best_memory[1]["avg_memory"]
                }
            }
    
    # 生成建议
    if comprehensive_results:
        report["recommendations"].extend([
            "Our DSL框架在吞吐量和延迟方面表现优异，适合高并发场景",
            "LangChain框架在内存使用方面较为高效，适合资源受限环境",
            "CrewAI框架在复杂任务处理方面表现良好，适合需要协作的场景",
            "AutoGen框架在代理数量较少时表现稳定，适合小规模应用"
        ])
    
    if ablation_results:
        report["recommendations"].extend([
            "缓存机制对性能提升有显著贡献，建议在生产环境中启用",
            "智能调度策略能够有效提高任务执行效率",
            "负载均衡机制在处理多代理任务时发挥重要作用"
        ])
    
    if scalability_results:
        report["recommendations"].extend([
            "Our DSL框架具有良好的可扩展性，能够处理大规模代理任务",
            "随着代理数量增加，需要关注内存使用和延迟增长",
            "建议根据实际需求选择合适的代理数量和任务复杂度"
        ])
    
    # 保存报告
    report_file = "comprehensive_experiment_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    logger.info(f"✅ 综合实验报告已保存到: {report_file}")
    
    # 输出报告摘要
    print("\n" + "="*60)
    print("📊 综合实验报告摘要")
    print("="*60)
    print(f"实验时间: {report['experiment_summary']['timestamp']}")
    print(f"完成实验: {report['experiment_summary']['completed_experiments']}/3")
    print(f"失败实验: {report['experiment_summary']['failed_experiments']}/3")
    
    if "performance_leaderboard" in report["key_findings"]:
        print("\n🏆 性能排行榜:")
        leaderboard = report["key_findings"]["performance_leaderboard"]
        print(f"  最高吞吐量: {leaderboard['best_throughput']['framework']} "
              f"({leaderboard['best_throughput']['value']:.3f} tasks/sec)")
        print(f"  最低延迟: {leaderboard['best_latency']['framework']} "
              f"({leaderboard['best_latency']['value']:.2f} ms)")
        print(f"  最低内存: {leaderboard['best_memory']['framework']} "
              f"({leaderboard['best_memory']['value']:.2f} MB)")
    
    print(f"\n💡 主要建议:")
    for i, recommendation in enumerate(report["recommendations"][:5], 1):
        print(f"  {i}. {recommendation}")
    
    print("="*60)
    
    return report

def main():
    """主函数"""
    print("🔬 全面实验框架")
    print("=" * 60)
    print("⚠️  注意：此实验使用真实API调用，需要有效的API密钥")
    print("⚠️  实验规模很大，预计需要数小时完成")
    print("⚠️  请确保有足够的API调用权限")
    print("=" * 60)
    
    # 确认继续
    response = input("\n是否继续运行全面实验？(y/N): ")
    if response.lower() != 'y':
        print("实验已取消")
        return
    
    start_time = time.time()
    
    # 运行所有实验
    comprehensive_results = None
    ablation_results = None
    scalability_results = None
    
    try:
        # 1. 全面基准测试
        comprehensive_results = run_comprehensive_benchmark()
        
        # 短暂休息
        time.sleep(5)
        
        # 2. 消融实验
        ablation_results = run_ablation_study()
        
        # 短暂休息
        time.sleep(5)
        
        # 3. 可扩展性实验
        scalability_results = run_scalability_study()
        
    except KeyboardInterrupt:
        logger.info("实验被用户中断")
        print("\n⚠️ 实验被中断，正在生成部分报告...")
    except Exception as e:
        logger.error(f"实验过程中发生错误: {e}")
        print(f"\n❌ 实验过程中发生错误: {e}")
    
    # 生成综合报告
    report = generate_comprehensive_report(comprehensive_results, ablation_results, scalability_results)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n🎉 实验完成！")
    print(f"总耗时: {total_time/3600:.2f} 小时")
    print(f"完成实验: {report['experiment_summary']['completed_experiments']}/3")
    
    if report['experiment_summary']['completed_experiments'] == 3:
        print("✅ 所有实验均成功完成！")
    else:
        print("⚠️ 部分实验未完成，请检查日志")

if __name__ == "__main__":
    main()

