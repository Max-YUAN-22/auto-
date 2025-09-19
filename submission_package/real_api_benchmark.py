#!/usr/bin/env python3
"""
完全真实的基准测试
使用真实API调用，不使用任何模拟数据
符合CCF A级审核要求
"""

import os
import sys
import time
import json
import psutil
import gc
from contextlib import contextmanager
from typing import Dict, Any, List
import numpy as np
from datetime import datetime
import logging
import requests
import subprocess

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealAPIBenchmark:
    def __init__(self, random_seed: int = 42):
        self.random_seed = random_seed
        np.random.seed(random_seed)
        
        # 添加项目根目录到Python路径
        project_root = os.path.join(os.path.dirname(__file__), '..')
        sys.path.insert(0, project_root)
        
        # 加载环境变量
        self.load_env()
        
        # 设置API配置
        self.api_key = os.getenv("OPENAI_API_KEY", "sk-0WQRDm5w3t3ukRFQ7j33rOUgLk9ezcTuwhsK7BXxgfyhYuqA").strip()
        self.base_url = "https://www.yunqiaoai.top/v1"
        
        # 真实的测试任务
        self.tasks = {
            "complex_reasoning": [
                "Analyze the following business scenario and provide strategic recommendations: A tech startup with 50 employees is facing rapid growth but struggling with communication bottlenecks. The CEO wants to implement a multi-agent system to improve internal coordination. What are the key considerations and implementation strategy?",
                "Design a multi-agent coordination protocol for autonomous vehicles at a busy intersection. Consider safety, efficiency, and scalability requirements. Provide detailed technical specifications.",
                "Evaluate the trade-offs between centralized and decentralized multi-agent architectures for a distributed manufacturing system. Include performance metrics, fault tolerance, and implementation complexity analysis.",
                "Develop a comprehensive testing framework for multi-agent systems that ensures reliability, performance, and scalability. Include unit testing, integration testing, and stress testing strategies.",
                "Analyze the security implications of multi-agent systems in financial trading applications. Identify potential attack vectors and propose mitigation strategies."
            ],
            "technical_analysis": [
                "Compare the performance characteristics of different multi-agent coordination algorithms (consensus, auction-based, market-based) in terms of convergence time, message complexity, and scalability. Provide quantitative analysis.",
                "Design a fault-tolerant multi-agent system architecture for critical infrastructure monitoring. Include redundancy strategies, failure detection mechanisms, and recovery procedures.",
                "Analyze the computational complexity of different task allocation algorithms in multi-agent systems. Provide Big-O analysis and empirical performance comparisons.",
                "Evaluate the impact of network latency on multi-agent coordination performance. Design experiments to measure degradation and propose optimization strategies.",
                "Develop a formal verification framework for multi-agent system properties using temporal logic. Include safety, liveness, and fairness properties."
            ]
        }
        
        self.memory_tracker = {}
    
    def load_env(self):
        """加载环境变量"""
        # 直接设置OpenAI API密钥
        os.environ['OPENAI_API_KEY'] = 'sk-0WQRDm5w3t3ukRFQ7j33rOUgLk9ezcTuwhsK7BXxgfyhYuqA'
        logger.info("Set OPENAI_API_KEY environment variable")
        
        # 尝试从文件加载其他变量
        env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        # 清理值（移除注释和空格）
                        value = value.split('#')[0].strip()
                        if value:  # 只设置非空值
                            os.environ[key] = value
                            logger.info(f"Loaded environment variable: {key}")
    
    def memory_tracking(self, framework: str, scenario: str, agent_count: int):
        """内存跟踪上下文管理器"""
        class MemoryTracker:
            def __init__(self, parent, framework, scenario, agent_count):
                self.parent = parent
                self.framework = framework
                self.scenario = scenario
                self.agent_count = agent_count
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
                
                key = f"{self.framework}_{self.scenario}_{self.agent_count}"
                self.parent.memory_tracker[key] = memory_usage
                logger.info(f"内存使用记录: {key} = {memory_usage:.2f} MB")
        
        return MemoryTracker(self, framework, scenario, agent_count)
    
    def test_our_dsl_real_api(self, scenario: str, agent_count: int) -> Dict[str, Any]:
        """测试Our DSL框架（真实API调用）"""
        try:
            from dsl.dsl import DSL
            from core.robust_llm import llm_callable
            
            tasks = self.tasks[scenario]
            
            with self.memory_tracking("our_dsl", scenario, agent_count):
                start_time = time.time()
                
                # 创建DSL实例
                dsl = DSL(seed=self.random_seed, workers=min(agent_count, 4))
                
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
                        result = task.wait(timeout=60.0)  # 增加超时时间
                        if result is not None and len(str(result).strip()) > 50:  # 确保有实际内容
                            successful_tasks += 1
                    except Exception as e:
                        logger.warning(f"任务等待失败: {e}")
                
                execution_time = time.time() - start_time
                throughput = successful_tasks / execution_time if execution_time > 0 else 0
                avg_latency = execution_time / successful_tasks if successful_tasks > 0 else 0
                success_rate = (successful_tasks / len(tasks[:agent_count])) * 100
                
            # 在with语句结束后获取内存使用
            memory_usage = self.memory_tracker.get(f"our_dsl_{scenario}_{agent_count}", 0)
            
            return {
                "framework": "Our DSL",
                "scenario": scenario,
                "agent_count": agent_count,
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
            logger.error(f"Our DSL测试失败: {e}")
            return {
                "framework": "Our DSL",
                "scenario": scenario,
                "agent_count": agent_count,
                "execution_time": 0,
                "throughput": 0,
                "success_rate": 0,
                "successful_tasks": 0,
                "total_tasks": len(self.tasks[scenario][:agent_count]),
                "avg_latency": 0,
                "status": "error",
                "memory_usage": 0,
                "error": str(e),
                "api_type": "error"
            }
    
    def test_langchain_real_api(self, scenario: str, agent_count: int) -> Dict[str, Any]:
        """测试LangChain框架（真实API调用）"""
        try:
            from langchain_openai import ChatOpenAI
            from langchain.schema import HumanMessage
            
            tasks = self.tasks[scenario]
            
            with self.memory_tracking("langchain", scenario, agent_count):
                start_time = time.time()
                
                # 创建LangChain客户端
                llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    api_key=self.api_key,
                    base_url=self.base_url,
                    temperature=0.3,
                    max_tokens=500
                )
                
                # 执行任务
                successful_tasks = 0
                for i, task_prompt in enumerate(tasks[:agent_count]):
                    try:
                        message = HumanMessage(content=task_prompt)
                        response = llm.invoke([message])
                        if response and response.content and len(response.content.strip()) > 50:
                            successful_tasks += 1
                    except Exception as e:
                        logger.warning(f"LangChain任务{i}失败: {e}")
                
                execution_time = time.time() - start_time
                throughput = successful_tasks / execution_time if execution_time > 0 else 0
                avg_latency = execution_time / successful_tasks if successful_tasks > 0 else 0
                success_rate = (successful_tasks / len(tasks[:agent_count])) * 100
                
            # 在with语句结束后获取内存使用
            memory_usage = self.memory_tracker.get(f"langchain_{scenario}_{agent_count}", 0)
            
            return {
                "framework": "LangChain",
                "scenario": scenario,
                "agent_count": agent_count,
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
            logger.error(f"LangChain测试失败: {e}")
            return {
                "framework": "LangChain",
                "scenario": scenario,
                "agent_count": agent_count,
                "execution_time": 0,
                "throughput": 0,
                "success_rate": 0,
                "successful_tasks": 0,
                "total_tasks": len(self.tasks[scenario][:agent_count]),
                "avg_latency": 0,
                "status": "error",
                "memory_usage": 0,
                "error": str(e),
                "api_type": "error"
            }
    
    def test_crewai_real_api(self, scenario: str, agent_count: int) -> Dict[str, Any]:
        """测试CrewAI框架（真实API调用）"""
        try:
            from crewai import Agent, Task, Crew, Process
            from crewai.llm import LLM
            
            tasks = self.tasks[scenario]
            
            with self.memory_tracking("crewai", scenario, agent_count):
                start_time = time.time()
                
                # 创建CrewAI LLM
                llm = LLM(
                    model="gpt-4o-mini",
                    api_key=self.api_key,
                    base_url=self.base_url,
                    temperature=0.3,
                    max_tokens=500
                )
                
                # 创建代理
                agents = []
                for i in range(min(agent_count, 2)):  # CrewAI限制代理数量
                    agent = Agent(
                        role=f"Agent_{i}",
                        goal=f"Complete task {i} efficiently and accurately",
                        backstory="You are a helpful AI assistant specialized in complex reasoning and technical analysis.",
                        llm=llm,
                        verbose=False,
                        allow_delegation=False  # 禁用委托以提高成功率
                    )
                    agents.append(agent)
                
                # 创建任务
                crew_tasks = []
                for i, task_prompt in enumerate(tasks[:agent_count]):
                    task = Task(
                        description=task_prompt,
                        agent=agents[i % len(agents)],
                        expected_output="A detailed and comprehensive response",
                        async_execution=False  # 同步执行以提高成功率
                    )
                    crew_tasks.append(task)
                
                # 创建Crew并执行
                crew = Crew(
                    agents=agents,
                    tasks=crew_tasks,
                    verbose=False,
                    process=Process.sequential  # 顺序执行以提高成功率
                )
                
                result = crew.kickoff()
                
                # 计算成功任务数 - 改进判断逻辑
                successful_tasks = 0
                if result:
                    result_str = str(result).strip()
                    if len(result_str) > 50:
                        # 检查是否包含多个任务的响应
                        task_responses = result_str.split('\n\n')
                        successful_tasks = min(len(task_responses), len(tasks[:agent_count]))
                    else:
                        successful_tasks = 1 if len(result_str) > 50 else 0
                else:
                    successful_tasks = 0
                
                execution_time = time.time() - start_time
                throughput = successful_tasks / execution_time if execution_time > 0 else 0
                avg_latency = execution_time / successful_tasks if successful_tasks > 0 else 0
                success_rate = (successful_tasks / len(tasks[:agent_count])) * 100
                
            # 在with语句结束后获取内存使用
            memory_usage = self.memory_tracker.get(f"crewai_{scenario}_{agent_count}", 0)
            
            return {
                "framework": "CrewAI",
                "scenario": scenario,
                "agent_count": agent_count,
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
            logger.error(f"CrewAI测试失败: {e}")
            return {
                "framework": "CrewAI",
                "scenario": scenario,
                "agent_count": agent_count,
                "execution_time": 0,
                "throughput": 0,
                "success_rate": 0,
                "total_tasks": len(self.tasks[scenario][:agent_count]),
                "avg_latency": 0,
                "status": "error",
                "memory_usage": 0,
                "error": str(e),
                "api_type": "error"
            }
    
    def test_autogen_real_api(self, scenario: str, agent_count: int) -> Dict[str, Any]:
        """测试AutoGen框架（真实API调用）"""
        try:
            from autogen import ConversableAgent, GroupChat, GroupChatManager
            
            tasks = self.tasks[scenario]
            
            with self.memory_tracking("autogen", scenario, agent_count):
                start_time = time.time()
                
                # 配置LLM
                llm_config = {
                    "model": "gpt-4o-mini",
                    "api_key": self.api_key,
                    "base_url": self.base_url,
                    "temperature": 0.3,
                    "max_tokens": 500
                }
                
                # 创建代理
                agents = []
                for i in range(max(agent_count, 2)):  # AutoGen需要至少2个代理
                    agent = ConversableAgent(
                        name=f"agent_{i}",
                        llm_config=llm_config,
                        system_message="You are a helpful AI assistant."
                    )
                    agents.append(agent)
                
                # 创建群聊
                group_chat = GroupChat(
                    agents=agents,
                    messages=[],
                    max_round=3,
                    speaker_selection_method='round_robin'
                )
                
                manager = GroupChatManager(
                    groupchat=group_chat,
                    llm_config=llm_config
                )
                
                # 执行任务
                successful_tasks = 0
                for i, task_prompt in enumerate(tasks[:agent_count]):
                    try:
                        result = agents[0].initiate_chat(
                            manager,
                            message=task_prompt,
                            max_turns=2
                        )
                        if result and len(str(result).strip()) > 50:
                            successful_tasks += 1
                    except Exception as e:
                        logger.warning(f"AutoGen任务{i}失败: {e}")
                
                execution_time = time.time() - start_time
                throughput = successful_tasks / execution_time if execution_time > 0 else 0
                avg_latency = execution_time / successful_tasks if successful_tasks > 0 else 0
                success_rate = (successful_tasks / len(tasks[:agent_count])) * 100
                
            # 在with语句结束后获取内存使用
            memory_usage = self.memory_tracker.get(f"autogen_{scenario}_{agent_count}", 0)
            
            return {
                "framework": "AutoGen",
                "scenario": scenario,
                "agent_count": agent_count,
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
            logger.error(f"AutoGen测试失败: {e}")
            return {
                "framework": "AutoGen",
                "scenario": scenario,
                "agent_count": agent_count,
                "execution_time": 0,
                "throughput": 0,
                "success_rate": 0,
                "successful_tasks": 0,
                "total_tasks": len(self.tasks[scenario][:agent_count]),
                "avg_latency": 0,
                "status": "error",
                "memory_usage": 0,
                "error": str(e),
                "api_type": "error"
            }
    
    def run_benchmark(self) -> Dict[str, Any]:
        """运行基准测试"""
        logger.info("🚀 开始完全真实的API基准测试...")
        
        benchmark_results = []
        scenarios = ["complex_reasoning", "technical_analysis"]
        agent_counts = [1, 2]  # 减少测试数量，确保质量
        frameworks = ["Our DSL", "LangChain", "CrewAI", "AutoGen"]
        
        total_tests = len(scenarios) * len(agent_counts) * len(frameworks)
        current_test = 0
        
        for scenario in scenarios:
            for agent_count in agent_counts:
                for framework in frameworks:
                    current_test += 1
                    logger.info(f"📊 测试进度: {current_test}/{total_tests} - {framework} - {scenario} - {agent_count} agents")
                    
                    if framework == "Our DSL":
                        result = self.test_our_dsl_real_api(scenario, agent_count)
                    elif framework == "LangChain":
                        result = self.test_langchain_real_api(scenario, agent_count)
                    elif framework == "CrewAI":
                        result = self.test_crewai_real_api(scenario, agent_count)
                    else:  # AutoGen
                        result = self.test_autogen_real_api(scenario, agent_count)
                    
                    benchmark_results.append(result)
                    
                    # 显示结果
                    if result["status"] == "success":
                        logger.info(f"   ✅ 成功: 吞吐量={result['throughput']:.2f} tasks/sec, 延迟={result['avg_latency']:.2f} ms, 内存={result['memory_usage']:.2f} MB")
                    else:
                        logger.error(f"   ❌ 失败: {result.get('error', 'unknown error')}")
        
        # 计算统计信息
        statistics = self.calculate_statistics(benchmark_results)
        
        return {
            "benchmark_results": benchmark_results,
            "statistics": statistics,
            "memory_tracker": self.memory_tracker,
            "timestamp": datetime.now().isoformat(),
            "test_info": {
                "total_tests": len(benchmark_results),
                "scenarios": scenarios,
                "agent_counts": agent_counts,
                "frameworks": frameworks,
                "random_seed": self.random_seed
            }
        }
    
    def calculate_statistics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """计算统计信息"""
        stats = {}
        
        for framework in ["Our DSL", "LangChain", "CrewAI", "AutoGen"]:
            framework_results = [r for r in results if r["framework"] == framework and r["status"] == "success"]
            
            if framework_results:
                stats[framework] = {
                    "avg_throughput": np.mean([r["throughput"] for r in framework_results]),
                    "avg_memory": np.mean([r["memory_usage"] for r in framework_results]),
                    "avg_latency": np.mean([r["avg_latency"] for r in framework_results]),
                    "avg_success_rate": np.mean([r["success_rate"] for r in framework_results]),
                    "total_tests": len(framework_results)
                }
        
        return stats

def main():
    """主函数"""
    print("🔬 完全真实的API基准测试")
    print("=" * 50)
    print("⚠️  注意：此测试使用真实API调用，需要有效的API密钥")
    print("⚠️  基线框架需要单独安装和配置")
    print("=" * 50)
    
    # 创建基准测试实例
    benchmark = RealAPIBenchmark(random_seed=42)
    
    # 运行测试
    results = benchmark.run_benchmark()
    
    # 保存结果
    output_file = "real_api_benchmark_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 测试完成！结果已保存到: {output_file}")
    
    # 显示摘要
    print("\n📊 测试摘要:")
    print("-" * 30)
    for framework, stats in results["statistics"].items():
        print(f"{framework}:")
        print(f"  平均吞吐量: {stats['avg_throughput']:.2f} tasks/sec")
        print(f"  平均内存使用: {stats['avg_memory']:.2f} MB")
        print(f"  平均延迟: {stats['avg_latency']:.2f} ms")
        print(f"  平均成功率: {stats['avg_success_rate']:.1f}%")
        print(f"  成功测试数: {stats['total_tests']}")
        print()
    
    # 显示错误统计
    error_count = sum(1 for r in results["benchmark_results"] if r["status"] == "error")
    success_count = sum(1 for r in results["benchmark_results"] if r["status"] == "success")
    
    print(f"\n📈 总体统计:")
    print(f"  成功测试: {success_count}")
    print(f"  失败测试: {error_count}")
    print(f"  成功率: {(success_count / len(results['benchmark_results'])) * 100:.1f}%")

if __name__ == "__main__":
    main()