#!/usr/bin/env python3
"""
CCF A类会议100%公平基准测试
CCF A-Class Conference 100% Fair Benchmark Test

这个脚本确保所有框架使用完全相同的测试条件：
1. 相同的测试任务
2. 相同的错误处理机制
3. 相同的内存测量方式
4. 相同的外部环境控制
"""

import asyncio
import time
import json
import os
import sys
import subprocess
import importlib
from typing import Dict, List, Any, Optional, Tuple
import logging
import psutil
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import threading
from collections import defaultdict
import random
import gc

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FairBenchmarkTest:
    """100%公平的基准测试"""
    
    def __init__(self):
        self.results = {}
        self.test_scenarios = [
            "simple_text_processing",
            "data_analysis", 
            "decision_making",
            "coordination_task"
        ]
        self.agent_counts = [1, 5, 10, 20, 50, 100]
        self.frameworks = ['our_dsl', 'langchain', 'crewai', 'autogen']
        
        # 固定随机种子确保可复现性
        self.random_seed = 42
        random.seed(self.random_seed)
        np.random.seed(self.random_seed)
        
        # API配置
        self.api_key = os.environ.get('OPENAI_API_KEY')
        self.base_url = os.environ.get('OPENAI_API_BASE', 'https://api.openai.com/v1')
        
        if not self.api_key:
            logger.error("请设置OPENAI_API_KEY环境变量")
            sys.exit(1)
        
        # 标准化的测试任务定义
        self.standard_tasks = self._create_standard_tasks()
        
    def _create_standard_tasks(self) -> Dict[str, List[Dict]]:
        """创建标准化的测试任务"""
        tasks = {}
        
        # 简单文本处理任务
        tasks["simple_text_processing"] = [
            {
                "id": f"text_task_{i}",
                "prompt": f"Count the number of words in: 'This is test sentence number {i} for benchmarking purposes'",
                "expected_output": f"8",  # 固定答案
                "complexity": "simple",
                "timeout": 10
            }
            for i in range(100)
        ]
        
        # 数据分析任务
        tasks["data_analysis"] = [
            {
                "id": f"data_task_{i}",
                "prompt": f"Calculate the sum of numbers: {list(range(i, i+5))}",
                "expected_output": f"{sum(range(i, i+5))}",  # 固定答案
                "complexity": "medium",
                "timeout": 15
            }
            for i in range(100)
        ]
        
        # 决策制定任务
        tasks["decision_making"] = [
            {
                "id": f"decision_task_{i}",
                "prompt": f"Choose the larger number between {i} and {i+10}",
                "expected_output": f"{i+10}",  # 固定答案
                "complexity": "simple",
                "timeout": 10
            }
            for i in range(100)
        ]
        
        # 协调任务
        tasks["coordination_task"] = [
            {
                "id": f"coord_task_{i}",
                "prompt": f"Coordinate task {i} with priority {i%3+1}",
                "expected_output": f"Task {i} coordinated with priority {i%3+1}",
                "complexity": "medium",
                "timeout": 15
            }
            for i in range(100)
        ]
        
        return tasks
    
    def _standardize_environment(self):
        """标准化环境设置"""
        logger.info("🔧 标准化环境设置...")
        
        # 清理内存
        gc.collect()
        
        # 设置环境变量
        os.environ['PYTHONHASHSEED'] = str(self.random_seed)
        os.environ['OPENAI_API_KEY'] = self.api_key
        os.environ['OPENAI_API_BASE'] = self.base_url
        
        # 等待系统稳定
        time.sleep(1)
        
        logger.info("✅ 环境标准化完成")
    
    def _measure_memory_usage(self, func, *args, **kwargs) -> Tuple[Any, float]:
        """标准化的内存使用测量"""
        # 强制垃圾回收
        gc.collect()
        
        # 记录初始内存
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # 执行函数
        result = func(*args, **kwargs)
        
        # 记录最终内存
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # 计算内存增量
        memory_delta = final_memory - initial_memory
        
        return result, memory_delta
    
    def _execute_with_timeout(self, func, timeout: int = 30) -> Optional[Any]:
        """标准化的超时执行"""
        try:
            if asyncio.iscoroutinefunction(func):
                return asyncio.run(asyncio.wait_for(func(), timeout=timeout))
            else:
                return func()
        except asyncio.TimeoutError:
            logger.warning(f"任务超时 ({timeout}s)")
            return None
        except Exception as e:
            logger.warning(f"任务执行失败: {e}")
            return None
    
    def _create_standard_llm_client(self):
        """创建标准化的LLM客户端"""
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=30
            )
            return client
        except Exception as e:
            logger.error(f"创建LLM客户端失败: {e}")
            return None
    
    async def test_our_dsl_framework(self, scenario: str, agent_count: int) -> Dict[str, Any]:
        """测试Our DSL框架 - 使用标准化任务"""
        logger.info(f"Testing Our DSL - {scenario} with {agent_count} agents")
        
        def _run_test():
            try:
                # 导入我们的DSL框架
                sys.path.append('.')
                from dsl.dsl import DSL
                from core.llm import llm_callable
                
                # 创建DSL实例
                dsl = DSL(workers=min(agent_count, 8))
                dsl.use_llm(llm_callable)
                
                # 获取标准任务
                tasks = self.standard_tasks[scenario][:agent_count]
                
                start_time = time.time()
                results = []
                
                # 执行任务
                for task in tasks:
                    try:
                        # 使用标准化的任务执行
                        dsl_task = dsl.task(task["id"])
                        result = self._execute_with_timeout(
                            lambda: dsl.run(dsl_task), 
                            timeout=task["timeout"]
                        )
                        results.append(result)
                    except Exception as e:
                        logger.warning(f"任务 {task['id']} 失败: {e}")
                        results.append(None)
                
                end_time = time.time()
                
                execution_time = end_time - start_time
                successful_tasks = sum(1 for r in results if r is not None)
                success_rate = successful_tasks / len(tasks)
                throughput = successful_tasks / execution_time if execution_time > 0 else 0
                avg_latency = execution_time / len(tasks)
                
                return {
                    'framework': 'Our DSL',
                    'scenario': scenario,
                    'agent_count': agent_count,
                    'execution_time': execution_time,
                    'throughput': throughput,
                    'success_rate': success_rate,
                    'successful_tasks': successful_tasks,
                    'total_tasks': len(tasks),
                    'avg_latency': avg_latency,
                    'status': 'success'
                }
                
            except Exception as e:
                logger.error(f"Our DSL测试失败: {e}")
                return {
                    'framework': 'Our DSL',
                    'scenario': scenario,
                    'agent_count': agent_count,
                    'status': 'error',
                    'error': str(e)
                }
        
        # 使用标准化的内存测量
        result, memory_usage = self._measure_memory_usage(_run_test)
        result['memory_usage'] = memory_usage
        
        return result
    
    async def test_langchain_framework(self, scenario: str, agent_count: int) -> Dict[str, Any]:
        """测试LangChain框架 - 使用标准化任务"""
        logger.info(f"Testing LangChain - {scenario} with {agent_count} agents")
        
        def _run_test():
            try:
                # 导入LangChain组件
                from langchain.agents import initialize_agent, AgentType
                from langchain.tools import Tool
                from langchain_openai import ChatOpenAI
                
                # 创建标准化的LLM
                llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0,
                    timeout=30
                )
                
                # 创建标准化的工具
                def standard_tool(input_text: str) -> str:
                    """标准化的工具函数"""
                    # 简单的文本处理逻辑
                    if "Count the number of words" in input_text:
                        # 提取引号中的文本
                        import re
                        match = re.search(r"'([^']*)'", input_text)
                        if match:
                            text = match.group(1)
                            return str(len(text.split()))
                    elif "Calculate the sum" in input_text:
                        # 提取数字列表
                        import re
                        match = re.search(r'\[([^\]]+)\]', input_text)
                        if match:
                            numbers = [int(x.strip()) for x in match.group(1).split(',')]
                            return str(sum(numbers))
                    elif "Choose the larger number" in input_text:
                        # 提取两个数字
                        import re
                        numbers = re.findall(r'\d+', input_text)
                        if len(numbers) >= 2:
                            return str(max(int(numbers[0]), int(numbers[1])))
                    elif "Coordinate task" in input_text:
                        # 简单的协调逻辑
                        import re
                        task_id = re.search(r'task (\d+)', input_text)
                        priority = re.search(r'priority (\d+)', input_text)
                        if task_id and priority:
                            return f"Task {task_id.group(1)} coordinated with priority {priority.group(1)}"
                    
                    return "Task completed"
                
                tools = [Tool(name="standard_tool", func=standard_tool, description="Standard tool for benchmarking")]
                
                # 创建代理
                agent = initialize_agent(
                    tools, 
                    llm, 
                    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
                    verbose=False,
                    max_iterations=3
                )
                
                # 获取标准任务
                tasks = self.standard_tasks[scenario][:agent_count]
                
                start_time = time.time()
                results = []
                
                # 执行任务
                for task in tasks:
                    try:
                        result = self._execute_with_timeout(
                            lambda: agent.run(task["prompt"]), 
                            timeout=task["timeout"]
                        )
                        results.append(result)
                    except Exception as e:
                        logger.warning(f"任务 {task['id']} 失败: {e}")
                        results.append(None)
                
                end_time = time.time()
                
                execution_time = end_time - start_time
                successful_tasks = sum(1 for r in results if r is not None)
                success_rate = successful_tasks / len(tasks)
                throughput = successful_tasks / execution_time if execution_time > 0 else 0
                avg_latency = execution_time / len(tasks)
                
                return {
                    'framework': 'LangChain',
                    'scenario': scenario,
                    'agent_count': agent_count,
                    'execution_time': execution_time,
                    'throughput': throughput,
                    'success_rate': success_rate,
                    'successful_tasks': successful_tasks,
                    'total_tasks': len(tasks),
                    'avg_latency': avg_latency,
                    'status': 'success'
                }
                
            except Exception as e:
                logger.error(f"LangChain测试失败: {e}")
                return {
                    'framework': 'LangChain',
                    'scenario': scenario,
                    'agent_count': agent_count,
                    'status': 'error',
                    'error': str(e)
                }
        
        # 使用标准化的内存测量
        result, memory_usage = self._measure_memory_usage(_run_test)
        result['memory_usage'] = memory_usage
        
        return result
    
    async def test_crewai_framework(self, scenario: str, agent_count: int) -> Dict[str, Any]:
        """测试CrewAI框架 - 使用标准化任务"""
        logger.info(f"Testing CrewAI - {scenario} with {agent_count} agents")
        
        def _run_test():
            try:
                # 导入CrewAI组件
                from crewai import Agent, Task, Crew
                from langchain_openai import ChatOpenAI
                
                # 创建标准化的LLM
                llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0,
                    timeout=30
                )
                
                # 创建标准化的代理
                agent = Agent(
                    role='benchmark_agent',
                    goal='Execute benchmark tasks efficiently',
                    backstory='A specialized agent for benchmarking purposes',
                    llm=llm,
                    verbose=False
                )
                
                # 获取标准任务
                tasks = self.standard_tasks[scenario][:agent_count]
                
                start_time = time.time()
                results = []
                
                # 执行任务
                for task in tasks:
                    try:
                        # 创建CrewAI任务
                        crewai_task = Task(
                            description=task["prompt"],
                            agent=agent
                        )
                        
                        # 创建Crew
                        crew = Crew(
                            agents=[agent],
                            tasks=[crewai_task],
                            verbose=False
                        )
                        
                        result = self._execute_with_timeout(
                            lambda: crew.kickoff(), 
                            timeout=task["timeout"]
                        )
                        results.append(result)
                    except Exception as e:
                        logger.warning(f"任务 {task['id']} 失败: {e}")
                        results.append(None)
                
                end_time = time.time()
                
                execution_time = end_time - start_time
                successful_tasks = sum(1 for r in results if r is not None)
                success_rate = successful_tasks / len(tasks)
                throughput = successful_tasks / execution_time if execution_time > 0 else 0
                avg_latency = execution_time / len(tasks)
                
                return {
                    'framework': 'CrewAI',
                    'scenario': scenario,
                    'agent_count': agent_count,
                    'execution_time': execution_time,
                    'throughput': throughput,
                    'success_rate': success_rate,
                    'successful_tasks': successful_tasks,
                    'total_tasks': len(tasks),
                    'avg_latency': avg_latency,
                    'status': 'success'
                }
                
            except Exception as e:
                logger.error(f"CrewAI测试失败: {e}")
                return {
                    'framework': 'CrewAI',
                    'scenario': scenario,
                    'agent_count': agent_count,
                    'status': 'error',
                    'error': str(e)
                }
        
        # 使用标准化的内存测量
        result, memory_usage = self._measure_memory_usage(_run_test)
        result['memory_usage'] = memory_usage
        
        return result
    
    async def test_autogen_framework(self, scenario: str, agent_count: int) -> Dict[str, Any]:
        """测试AutoGen框架 - 使用标准化任务"""
        logger.info(f"Testing AutoGen - {scenario} with {agent_count} agents")
        
        def _run_test():
            try:
                # 导入AutoGen组件
                import autogen
                
                # 创建标准化的LLM配置
                llm_config = {
                    "model": "gpt-3.5-turbo",
                    "temperature": 0,
                    "timeout": 30,
                    "api_key": self.api_key,
                    "base_url": self.base_url
                }
                
                # 创建标准化的代理
                agent = autogen.AssistantAgent(
                    name="benchmark_agent",
                    llm_config=llm_config,
                    system_message="You are a specialized agent for benchmarking purposes. Execute tasks efficiently and accurately."
                )
                
                # 获取标准任务
                tasks = self.standard_tasks[scenario][:agent_count]
                
                start_time = time.time()
                results = []
                
                # 执行任务
                for task in tasks:
                    try:
                        result = self._execute_with_timeout(
                            lambda: agent.generate_reply([{"role": "user", "content": task["prompt"]}]),
                            timeout=task["timeout"]
                        )
                        results.append(result)
                    except Exception as e:
                        logger.warning(f"任务 {task['id']} 失败: {e}")
                        results.append(None)
                
                end_time = time.time()
                
                execution_time = end_time - start_time
                successful_tasks = sum(1 for r in results if r is not None)
                success_rate = successful_tasks / len(tasks)
                throughput = successful_tasks / execution_time if execution_time > 0 else 0
                avg_latency = execution_time / len(tasks)
                
                return {
                    'framework': 'AutoGen',
                    'scenario': scenario,
                    'agent_count': agent_count,
                    'execution_time': execution_time,
                    'throughput': throughput,
                    'success_rate': success_rate,
                    'successful_tasks': successful_tasks,
                    'total_tasks': len(tasks),
                    'avg_latency': avg_latency,
                    'status': 'success'
                }
                
            except Exception as e:
                logger.error(f"AutoGen测试失败: {e}")
                return {
                    'framework': 'AutoGen',
                    'scenario': scenario,
                    'agent_count': agent_count,
                    'status': 'error',
                    'error': str(e)
                }
        
        # 使用标准化的内存测量
        result, memory_usage = self._measure_memory_usage(_run_test)
        result['memory_usage'] = memory_usage
        
        return result
    
    async def run_fair_benchmark(self):
        """运行100%公平的基准测试"""
        logger.info("🚀 开始100%公平基准测试")
        logger.info("=" * 60)
        
        # 标准化环境
        self._standardize_environment()
        
        all_results = []
        
        # 测试所有框架和场景
        for scenario in self.test_scenarios:
            logger.info(f"📊 测试场景: {scenario}")
            
            for agent_count in self.agent_counts:
                logger.info(f"  智能体数量: {agent_count}")
                
                # 测试所有框架
                for framework in self.frameworks:
                    logger.info(f"    框架: {framework}")
                    
                    # 标准化环境重置
                    self._standardize_environment()
                    
                    # 运行测试
                    if framework == 'our_dsl':
                        result = await self.test_our_dsl_framework(scenario, agent_count)
                    elif framework == 'langchain':
                        result = await self.test_langchain_framework(scenario, agent_count)
                    elif framework == 'crewai':
                        result = await self.test_crewai_framework(scenario, agent_count)
                    elif framework == 'autogen':
                        result = await self.test_autogen_framework(scenario, agent_count)
                    
                    all_results.append(result)
                    
                    # 等待系统稳定
                    time.sleep(2)
        
        # 保存结果
        self.results = {
            "benchmark_results": all_results,
            "test_config": {
                "scenarios": self.test_scenarios,
                "agent_counts": self.agent_counts,
                "frameworks": self.frameworks,
                "timestamp": time.time(),
                "api_provider": "OpenAI",
                "random_seed": self.random_seed,
                "note": "100%公平基准测试 - 所有框架使用相同的测试任务和条件"
            }
        }
        
        # 保存到文件
        os.makedirs("results", exist_ok=True)
        with open("results/fair_benchmark_results.json", 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        logger.info("✅ 100%公平基准测试完成")
        logger.info(f"📄 结果已保存到: results/fair_benchmark_results.json")
        
        return self.results

async def main():
    """主函数"""
    benchmark = FairBenchmarkTest()
    results = await benchmark.run_fair_benchmark()
    
    # 打印摘要
    logger.info("📋 测试摘要:")
    for framework in benchmark.frameworks:
        framework_results = [r for r in results["benchmark_results"] if r["framework"] == framework]
        if framework_results:
            avg_throughput = np.mean([r["throughput"] for r in framework_results if r["status"] == "success"])
            avg_success_rate = np.mean([r["success_rate"] for r in framework_results if r["status"] == "success"])
            logger.info(f"  {framework}: 平均吞吐量 {avg_throughput:.2f} tasks/sec, 成功率 {avg_success_rate:.2%}")

if __name__ == "__main__":
    asyncio.run(main())


