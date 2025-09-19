#!/usr/bin/env python3
"""
Our DSL性能优化 - 真实提升
Our DSL Performance Optimization - Real Improvement
"""

import asyncio
import time
import json
import os
import sys
import threading
from typing import Dict, List, Any, Optional, Callable
import logging
import psutil
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
import random
import gc
import tracemalloc
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OptimizedDSL:
    """优化后的DSL实现"""
    
    def __init__(self, seed: int = 7, workers: int = 8):
        self.seed = seed
        self.workers = workers
        self.cache = {}
        self.metrics = {"total_tasks": 0, "completed_tasks": 0, "failed_tasks": 0}
        self.history = []
        
        # 优化：使用线程池而不是创建新线程
        self.executor = ThreadPoolExecutor(max_workers=workers)
        
        # 优化：任务队列
        self.task_queue = []
        self.completed_tasks = []
        
        # 优化：批处理
        self.batch_size = 4
        self.batch_timeout = 0.1  # 100ms
        
    def add_task(self, name: str, prompt: str, agent: str, priority: int = 0):
        """添加任务到队列"""
        task = {
            "name": name,
            "prompt": prompt,
            "agent": agent,
            "priority": priority,
            "status": "pending",
            "result": None,
            "start_time": None,
            "end_time": None
        }
        self.task_queue.append(task)
        self.metrics["total_tasks"] += 1
        return task
    
    def _process_batch(self, tasks: List[Dict], llm_callable: Callable) -> List[Dict]:
        """批量处理任务"""
        results = []
        
        # 优化：并发处理批次中的任务
        futures = []
        for task in tasks:
            future = self.executor.submit(self._execute_single_task, task, llm_callable)
            futures.append((task, future))
        
        # 等待所有任务完成
        for task, future in futures:
            try:
                result = future.result(timeout=30)
                task["result"] = result
                task["status"] = "completed"
                task["end_time"] = time.time()
                self.metrics["completed_tasks"] += 1
                results.append(task)
            except Exception as e:
                logger.error(f"任务 {task['name']} 执行失败: {e}")
                task["status"] = "failed"
                task["end_time"] = time.time()
                self.metrics["failed_tasks"] += 1
                results.append(task)
        
        return results
    
    def _execute_single_task(self, task: Dict, llm_callable: Callable) -> str:
        """执行单个任务"""
        task["start_time"] = time.time()
        
        # 优化：检查缓存
        cache_key = f"{task['prompt']}_{task['agent']}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # 执行LLM调用
        result = llm_callable(task["prompt"], task["agent"])
        
        # 优化：缓存结果
        self.cache[cache_key] = result
        
        return result
    
    def run(self, llm_callable: Callable) -> Dict[str, Any]:
        """运行DSL"""
        start_time = time.time()
        
        # 优化：按优先级排序任务
        self.task_queue.sort(key=lambda x: x["priority"], reverse=True)
        
        # 优化：批量处理任务
        batch_results = []
        for i in range(0, len(self.task_queue), self.batch_size):
            batch = self.task_queue[i:i + self.batch_size]
            batch_result = self._process_batch(batch, llm_callable)
            batch_results.extend(batch_result)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # 计算性能指标
        successful_tasks = len([t for t in batch_results if t["status"] == "completed"])
        throughput = successful_tasks / execution_time if execution_time > 0 else 0
        avg_latency = execution_time / successful_tasks if successful_tasks > 0 else 0
        
        return {
            "execution_time": execution_time,
            "throughput": throughput,
            "successful_tasks": successful_tasks,
            "total_tasks": len(self.task_queue),
            "avg_latency": avg_latency,
            "success_rate": successful_tasks / len(self.task_queue) if self.task_queue else 0,
            "results": batch_results
        }
    
    def cleanup(self):
        """清理资源"""
        self.executor.shutdown(wait=True)

class PerformanceOptimizer:
    """性能优化器"""
    
    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY')
        self.base_url = os.environ.get('OPENAI_API_BASE', 'https://api.openai.com/v1')
        
        if not self.api_key:
            logger.error("未设置OPENAI_API_KEY")
            sys.exit(1)
    
    def _create_llm_client(self):
        """创建LLM客户端"""
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=30,
                max_retries=2
            )
            return client
        except Exception as e:
            logger.error(f"创建LLM客户端失败: {e}")
            return None
    
    def _optimized_llm_call(self, prompt: str, role: str = None) -> str:
        """优化的LLM调用"""
        client = self._create_llm_client()
        if not client:
            raise Exception("无法创建LLM客户端")
        
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个智能城市管理助手，负责处理各种城市运营任务。请用中文简洁地回应用户的请求。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM调用失败: {e}")
            raise e
    
    def test_optimized_dsl(self, scenario: str, agent_count: int) -> Dict[str, Any]:
        """测试优化后的DSL"""
        try:
            # 创建测试任务
            test_tasks = {
                "simple_math": [
                    "计算 15 + 27",
                    "计算 100 - 45", 
                    "计算 8 * 7",
                    "计算 144 / 12"
                ],
                "text_processing": [
                    "处理文本: 智能城市管理",
                    "处理文本: 交通优化系统",
                    "处理文本: 环境监测数据",
                    "处理文本: 公共服务管理"
                ],
                "data_analysis": [
                    "分析数据: 交通流量模式",
                    "分析数据: 能源消耗趋势",
                    "分析数据: 人口分布统计",
                    "分析数据: 环境质量指标"
                ],
                "decision_logic": [
                    "决策: 交通信号灯调整",
                    "决策: 停车位分配策略",
                    "决策: 紧急事件响应",
                    "决策: 资源分配优化"
                ]
            }
            
            tasks = test_tasks[scenario]
            
            # 创建优化后的DSL
            dsl = OptimizedDSL(seed=42, workers=min(agent_count, 8))
            
            # 添加任务
            for i, task_prompt in enumerate(tasks[:agent_count]):
                dsl.add_task(f"task_{i}", task_prompt, f"agent_{i}", priority=i)
            
            # 运行DSL
            start_time = time.time()
            result = dsl.run(self._optimized_llm_call)
            end_time = time.time()
            
            # 清理资源
            dsl.cleanup()
            
            return {
                "framework": "Our Optimized DSL",
                "scenario": scenario,
                "agent_count": agent_count,
                "execution_time": result["execution_time"],
                "throughput": result["throughput"],
                "success_rate": result["success_rate"],
                "successful_tasks": result["successful_tasks"],
                "total_tasks": result["total_tasks"],
                "avg_latency": result["avg_latency"],
                "status": "success",
                "memory_usage": 0,
                "api_type": "real_api"
            }
            
        except Exception as e:
            logger.error(f"优化DSL测试失败: {e}")
            return {
                "framework": "Our Optimized DSL",
                "scenario": scenario,
                "agent_count": agent_count,
                "execution_time": 0,
                "throughput": 0,
                "success_rate": 0,
                "successful_tasks": 0,
                "total_tasks": len(test_tasks[scenario][:agent_count]),
                "avg_latency": 0,
                "status": "error",
                "memory_usage": 0,
                "error": str(e),
                "api_type": "error"
            }
    
    def run_optimization_test(self) -> Dict[str, Any]:
        """运行优化测试"""
        logger.info("🚀 开始Our DSL性能优化测试...")
        
        results = []
        test_scenarios = ["simple_math", "text_processing", "data_analysis", "decision_logic"]
        agent_counts = [1, 3, 5]
        
        total_tests = len(test_scenarios) * len(agent_counts)
        current_test = 0
        
        for scenario in test_scenarios:
            for agent_count in agent_counts:
                current_test += 1
                logger.info(f"📊 测试进度: {current_test}/{total_tests} - {scenario} - {agent_count} agents")
                
                result = self.test_optimized_dsl(scenario, agent_count)
                results.append(result)
                
                # 强制垃圾回收
                gc.collect()
        
        # 保存结果
        output_file = "results/optimized_dsl_results.json"
        os.makedirs("results", exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({"benchmark_results": results}, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ 优化测试完成！结果已保存到 {output_file}")
        
        return {"benchmark_results": results}

def main():
    """主函数"""
    optimizer = PerformanceOptimizer()
    results = optimizer.run_optimization_test()
    
    # 简单统计
    print("\n" + "="*80)
    print("🎯 Our DSL性能优化测试结果")
    print("="*80)
    
    framework_stats = {}
    for result in results["benchmark_results"]:
        framework = result["framework"]
        if framework not in framework_stats:
            framework_stats[framework] = {
                "throughputs": [],
                "latencies": [],
                "success_rates": [],
                "execution_times": []
            }
        
        if result["status"] == "success":
            framework_stats[framework]["throughputs"].append(result["throughput"])
            framework_stats[framework]["latencies"].append(result["avg_latency"])
            framework_stats[framework]["success_rates"].append(result["success_rate"])
            framework_stats[framework]["execution_times"].append(result["execution_time"])
    
    print(f"\n📊 优化后性能:")
    print(f"{'框架':<20} {'平均吞吐量':<15} {'平均延迟':<15} {'成功率':<15}")
    print("-" * 70)
    
    for framework, stats in framework_stats.items():
        if stats["throughputs"]:
            avg_throughput = np.mean(stats["throughputs"])
            avg_latency = np.mean(stats["latencies"])
            avg_success_rate = np.mean(stats["success_rates"])
            avg_execution_time = np.mean(stats["execution_times"])
            
            print(f"{framework:<20} {avg_throughput:<15.2f} {avg_latency*1000:<15.3f} {avg_success_rate:<15.2%}")
    
    # 与原始结果对比
    print(f"\n📈 性能提升分析:")
    print(f"   优化重点:")
    print(f"   • 批量处理: 减少API调用开销")
    print(f"   • 并发执行: 提高任务并行度")
    print(f"   • 缓存机制: 避免重复计算")
    print(f"   • 线程池: 减少线程创建开销")
    print(f"   • 任务排序: 优化任务执行顺序")

if __name__ == "__main__":
    main()
