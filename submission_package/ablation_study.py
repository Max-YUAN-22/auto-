#!/usr/bin/env python3
"""
消融实验框架 - 完全真实的API调用实验
Ablation Study Framework - Fully Real API Call Experiments

分析Our DSL框架各个组件的贡献：
1. 缓存机制的影响
2. 调度策略的影响  
3. 负载均衡的影响
4. 重试机制的影响
5. 内存优化的影响
"""

import os
import sys
import json
import time
import logging
import numpy as np
import psutil
import gc
from datetime import datetime
from typing import Dict, List, Any, Tuple
from contextlib import contextmanager

# 添加项目根目录到Python路径
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AblationStudy:
    """消融实验类"""
    
    def __init__(self, random_seed: int = 42):
        self.random_seed = random_seed
        np.random.seed(random_seed)
        
        # 加载环境变量
        self.load_env()
        
        # 设置API配置
        self.api_key = os.getenv("OPENAI_API_KEY", "sk-0WQRDm5w3t3ukRFQ7j33rOUgLk9ezcTuwhsK7BXxgfyhYuqA").strip()
        self.base_url = "https://www.yunqiaoai.top/v1"
        
        # 内存跟踪器
        self.memory_tracker = {}
        
        # 消融实验配置
        self.ablation_config = {
            "scenarios": ["business_analysis", "technical_design", "scientific_research"],
            "agent_counts": [1, 2, 3, 4, 5],
            "complexities": ["simple", "medium", "complex"],
            "repetitions": 3,
            "ablation_components": [
                "baseline",           # 基线版本（完整功能）
                "no_cache",          # 无缓存
                "no_scheduler",      # 无智能调度
                "no_load_balance",   # 无负载均衡
                "no_retry",          # 无重试机制
                "no_memory_opt"      # 无内存优化
            ]
        }
        
        # 测试任务
        self.tasks = self._generate_ablation_tasks()
        
        logger.info(f"消融实验初始化完成 - 组件数: {len(self.ablation_config['ablation_components'])}, "
                   f"场景数: {len(self.ablation_config['scenarios'])}, "
                   f"代理数量: {len(self.ablation_config['agent_counts'])}")
    
    def load_env(self):
        """加载环境变量"""
        os.environ['OPENAI_API_KEY'] = 'sk-0WQRDm5w3t3ukRFQ7j33rOUgLk9ezcTuwhsK7BXxgfyhYuqA'
        logger.info("设置OPENAI_API_KEY环境变量")
    
    def _generate_ablation_tasks(self) -> Dict[str, Dict[str, List[str]]]:
        """生成消融实验测试任务"""
        tasks = {}
        
        # 商业分析场景
        tasks["business_analysis"] = {
            "simple": [
                "分析一家小型咖啡店的月度销售数据，识别销售趋势并提供改进建议。",
                "评估一个在线教育平台的用户增长策略，提出优化方案。"
            ],
            "medium": [
                "为一家中型制造企业设计数字化转型路线图，包括技术选型、实施计划和风险评估。",
                "分析电商平台的供应链管理问题，设计优化方案以提高效率和降低成本。"
            ],
            "complex": [
                "设计一个多国企业的全球供应链风险管理框架，考虑地缘政治、自然灾害、市场波动等因素，并提供实时监控和应急响应机制。",
                "为一家大型金融机构设计基于AI的智能投顾系统架构，包括客户画像、风险评估、投资组合优化和合规管理。"
            ]
        }
        
        # 技术设计场景
        tasks["technical_design"] = {
            "simple": [
                "设计一个简单的RESTful API架构，包括认证、授权和数据验证机制。",
                "为移动应用设计用户认证和会话管理系统。"
            ],
            "medium": [
                "设计一个微服务架构的电商平台，包括用户服务、商品服务、订单服务和支付服务，考虑服务间通信、数据一致性和容错机制。",
                "设计一个分布式缓存系统，支持高并发读写、数据一致性和故障恢复。"
            ],
            "complex": [
                "设计一个支持千万级用户的实时推荐系统架构，包括数据收集、特征工程、模型训练、在线推理和A/B测试框架，考虑延迟、准确性和可扩展性。",
                "设计一个多云环境下的容器编排平台，支持自动扩缩容、服务发现、负载均衡、监控告警和灾难恢复。"
            ]
        }
        
        # 科学研究场景
        tasks["scientific_research"] = {
            "simple": [
                "分析气候变化对农业产量的影响，基于历史数据建立预测模型。",
                "研究社交媒体对青少年心理健康的影响，设计实验方案。"
            ],
            "medium": [
                "设计一个基于机器学习的药物发现平台，包括分子筛选、活性预测和毒性评估，考虑数据质量和模型可解释性。",
                "研究量子计算在密码学中的应用，分析量子算法对现有加密系统的影响并提出后量子密码学方案。"
            ],
            "complex": [
                "设计一个多模态AI系统用于癌症早期诊断，整合影像学、基因组学、蛋白质组学和临床数据，建立端到端的诊断和预后预测模型。",
                "研究可控核聚变反应堆的等离子体控制算法，设计实时控制系统以维持等离子体稳定性和优化能量输出。"
            ]
        }
        
        return tasks
    
    @contextmanager
    def memory_tracking(self, component: str, scenario: str, agent_count: int, complexity: str):
        """内存跟踪上下文管理器"""
        class MemoryTracker:
            def __init__(self, parent, component, scenario, agent_count, complexity):
                self.parent = parent
                self.component = component
                self.scenario = scenario
                self.agent_count = agent_count
                self.complexity = complexity
                self.initial_memory = None
                
            def __enter__(self):
                gc.collect()
                process = psutil.Process()
                self.initial_memory = process.memory_info().rss / 1024 / 1024  # MB
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                process = psutil.Process()
                final_memory = process.memory_info().rss / 1024 / 1024  # MB
                memory_usage = max(0, final_memory - self.initial_memory)
                
                key = f"{self.component}_{self.scenario}_{self.agent_count}_{self.complexity}"
                self.parent.memory_tracker[key] = memory_usage
                logger.info(f"内存使用记录: {key} = {memory_usage:.2f} MB")
        
        tracker = MemoryTracker(self, component, scenario, agent_count, complexity)
        try:
            yield tracker
        finally:
            pass
    
    def test_dsl_component(self, component: str, scenario: str, agent_count: int, complexity: str) -> Dict[str, Any]:
        """测试DSL特定组件"""
        try:
            from dsl.dsl import DSL
            from core.robust_llm import llm_callable
            
            tasks = self.tasks[scenario][complexity]
            
            with self.memory_tracking(component, scenario, agent_count, complexity):
                start_time = time.time()
                
                # 根据组件类型创建不同的DSL配置
                if component == "baseline":
                    # 基线版本 - 完整功能
                    dsl = DSL(seed=self.random_seed, workers=min(agent_count, 8))
                elif component == "no_cache":
                    # 无缓存版本
                    dsl = DSL(seed=self.random_seed, workers=min(agent_count, 8), enable_cache=False)
                elif component == "no_scheduler":
                    # 无智能调度版本
                    dsl = DSL(seed=self.random_seed, workers=min(agent_count, 8), enable_scheduler=False)
                elif component == "no_load_balance":
                    # 无负载均衡版本
                    dsl = DSL(seed=self.random_seed, workers=min(agent_count, 8), enable_load_balance=False)
                elif component == "no_retry":
                    # 无重试机制版本
                    dsl = DSL(seed=self.random_seed, workers=min(agent_count, 8), enable_retry=False)
                elif component == "no_memory_opt":
                    # 无内存优化版本
                    dsl = DSL(seed=self.random_seed, workers=min(agent_count, 8), enable_memory_opt=False)
                else:
                    # 默认基线版本
                    dsl = DSL(seed=self.random_seed, workers=min(agent_count, 8))
                
                # 添加任务
                task_objects = []
                for i, task_prompt in enumerate(tasks[:agent_count]):
                    task_obj = dsl.gen(f"task_{i}", prompt=task_prompt, agent=f"agent_{i}").schedule()
                    task_objects.append(task_obj)
                
                # 运行DSL
                dsl.run(llm_callable)
                
                # 等待任务完成
                successful_tasks = 0
                for task in task_objects:
                    try:
                        result = task.wait(timeout=120.0)
                        if result is not None and len(str(result).strip()) > 100:
                            successful_tasks += 1
                    except Exception as e:
                        logger.warning(f"任务等待失败: {e}")
                
                execution_time = time.time() - start_time
                throughput = successful_tasks / execution_time if execution_time > 0 else 0
                avg_latency = execution_time / successful_tasks if successful_tasks > 0 else 0
                success_rate = (successful_tasks / len(tasks[:agent_count])) * 100
                
            # 在with语句结束后获取内存使用
            memory_usage = self.memory_tracker.get(f"{component}_{scenario}_{agent_count}_{complexity}", 0)
            
            return {
                "component": component,
                "scenario": scenario,
                "agent_count": agent_count,
                "complexity": complexity,
                "execution_time": execution_time,
                "throughput": throughput,
                "success_rate": success_rate,
                "successful_tasks": successful_tasks,
                "total_tasks": len(tasks[:agent_count]),
                "avg_latency": avg_latency * 1000,  # 转换为ms
                "status": "success",
                "memory_usage": memory_usage,
                "api_type": "real_api"
            }
                
        except Exception as e:
            logger.error(f"DSL组件测试失败 ({component}): {e}")
            return {
                "component": component,
                "scenario": scenario,
                "agent_count": agent_count,
                "complexity": complexity,
                "execution_time": 0,
                "throughput": 0,
                "success_rate": 0,
                "successful_tasks": 0,
                "total_tasks": len(self.tasks[scenario][complexity][:agent_count]),
                "avg_latency": 0,
                "status": "error",
                "memory_usage": 0,
                "error": str(e),
                "api_type": "error"
            }
    
    def run_ablation_study(self) -> Dict[str, Any]:
        """运行消融实验"""
        logger.info("🔬 开始消融实验...")
        logger.info(f"实验配置: {len(self.ablation_config['ablation_components'])}个组件, "
                   f"{len(self.ablation_config['scenarios'])}个场景, "
                   f"{len(self.ablation_config['agent_counts'])}个代理数量")
        
        ablation_results = []
        total_tests = (len(self.ablation_config['ablation_components']) * 
                      len(self.ablation_config['scenarios']) * 
                      len(self.ablation_config['agent_counts']) * 
                      len(self.ablation_config['complexities']) * 
                      self.ablation_config['repetitions'])
        
        current_test = 0
        
        for component in self.ablation_config['ablation_components']:
            for scenario in self.ablation_config['scenarios']:
                for agent_count in self.ablation_config['agent_counts']:
                    for complexity in self.ablation_config['complexities']:
                        for repetition in range(self.ablation_config['repetitions']):
                            current_test += 1
                            logger.info(f"📊 测试进度: {current_test}/{total_tests} - "
                                       f"{component} - {scenario} - {agent_count} agents - {complexity}")
                            
                            # 运行测试
                            result = self.test_dsl_component(component, scenario, agent_count, complexity)
                            
                            # 添加重复次数信息
                            result["repetition"] = repetition + 1
                            ablation_results.append(result)
                            
                            # 记录结果
                            if result["status"] == "success":
                                logger.info(f"   ✅ 成功: 吞吐量={result['throughput']:.3f} tasks/sec, "
                                           f"延迟={result['avg_latency']:.2f} ms, "
                                           f"内存={result['memory_usage']:.2f} MB")
                            else:
                                logger.error(f"   ❌ 失败: {result.get('error', 'Unknown error')}")
                            
                            # 短暂休息以避免API限制
                            time.sleep(1)
        
        # 保存结果
        results_file = "ablation_study_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                "ablation_results": ablation_results,
                "memory_tracker": self.memory_tracker,
                "timestamp": datetime.now().isoformat(),
                "ablation_config": self.ablation_config,
                "test_info": {
                    "total_tests": len(ablation_results),
                    "components": self.ablation_config['ablation_components'],
                    "scenarios": self.ablation_config['scenarios'],
                    "agent_counts": self.ablation_config['agent_counts'],
                    "complexities": self.ablation_config['complexities'],
                    "repetitions": self.ablation_config['repetitions'],
                    "random_seed": self.random_seed
                }
            }, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ 消融实验完成！结果已保存到: {results_file}")
        
        # 生成消融分析
        self._generate_ablation_analysis(ablation_results)
        
        return {
            "ablation_results": ablation_results,
            "memory_tracker": self.memory_tracker,
            "timestamp": datetime.now().isoformat(),
            "ablation_config": self.ablation_config
        }
    
    def _generate_ablation_analysis(self, ablation_results: List[Dict[str, Any]]):
        """生成消融分析"""
        logger.info("\n📊 消融实验分析:")
        logger.info("=" * 60)
        
        # 按组件分组统计
        component_stats = {}
        for result in ablation_results:
            if result["status"] == "success":
                component = result["component"]
                if component not in component_stats:
                    component_stats[component] = {
                        "throughput": [],
                        "latency": [],
                        "memory": [],
                        "success_rate": [],
                        "total_tests": 0,
                        "successful_tests": 0
                    }
                
                component_stats[component]["throughput"].append(result["throughput"])
                component_stats[component]["latency"].append(result["avg_latency"])
                component_stats[component]["memory"].append(result["memory_usage"])
                component_stats[component]["success_rate"].append(result["success_rate"])
                component_stats[component]["total_tests"] += 1
                if result["success_rate"] > 0:
                    component_stats[component]["successful_tests"] += 1
        
        # 输出统计结果
        baseline_stats = component_stats.get("baseline", {})
        if baseline_stats and baseline_stats["throughput"]:
            baseline_throughput = np.mean(baseline_stats["throughput"])
            baseline_latency = np.mean(baseline_stats["latency"])
            baseline_memory = np.mean(baseline_stats["memory"])
            
            logger.info(f"\n基线版本 (完整功能):")
            logger.info(f"  平均吞吐量: {baseline_throughput:.3f} tasks/sec")
            logger.info(f"  平均延迟: {baseline_latency:.2f} ms")
            logger.info(f"  平均内存使用: {baseline_memory:.2f} MB")
            
            # 计算各组件的性能影响
            logger.info(f"\n组件性能影响分析:")
            logger.info("-" * 40)
            
            for component, stats in component_stats.items():
                if component != "baseline" and stats["throughput"]:
                    avg_throughput = np.mean(stats["throughput"])
                    avg_latency = np.mean(stats["latency"])
                    avg_memory = np.mean(stats["memory"])
                    
                    throughput_change = ((avg_throughput - baseline_throughput) / baseline_throughput) * 100
                    latency_change = ((avg_latency - baseline_latency) / baseline_latency) * 100
                    memory_change = ((avg_memory - baseline_memory) / baseline_memory) * 100
                    
                    logger.info(f"\n{component}:")
                    logger.info(f"  吞吐量变化: {throughput_change:+.1f}% ({avg_throughput:.3f} tasks/sec)")
                    logger.info(f"  延迟变化: {latency_change:+.1f}% ({avg_latency:.2f} ms)")
                    logger.info(f"  内存变化: {memory_change:+.1f}% ({avg_memory:.2f} MB)")
                    
                    # 判断组件重要性
                    if abs(throughput_change) > 10:
                        importance = "高"
                    elif abs(throughput_change) > 5:
                        importance = "中"
                    else:
                        importance = "低"
                    
                    logger.info(f"  组件重要性: {importance}")
        
        # 总体统计
        total_tests = len(ablation_results)
        successful_tests = sum(1 for r in ablation_results if r["status"] == "success")
        overall_success_rate = (successful_tests / total_tests) * 100
        
        logger.info(f"\n📈 总体统计:")
        logger.info(f"  成功测试: {successful_tests}")
        logger.info(f"  失败测试: {total_tests - successful_tests}")
        logger.info(f"  成功率: {overall_success_rate:.1f}%")

def main():
    """主函数"""
    print("🔬 消融实验框架")
    print("=" * 50)
    print("⚠️  注意：此实验使用真实API调用，需要有效的API密钥")
    print("⚠️  实验规模较大，预计需要较长时间完成")
    print("=" * 50)
    
    # 创建消融实验实例
    ablation = AblationStudy()
    
    # 运行消融实验
    results = ablation.run_ablation_study()
    
    print("\n🎉 消融实验完成！")
    print(f"总测试数: {len(results['ablation_results'])}")
    print("结果已保存到 ablation_study_results.json")

if __name__ == "__main__":
    main()
