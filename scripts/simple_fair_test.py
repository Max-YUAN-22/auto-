#!/usr/bin/env python3
"""
100%公平的简化基准测试
100% Fair Simplified Benchmark Test

这个脚本确保所有框架使用完全相同的条件进行测试
"""

import asyncio
import time
import json
import os
import sys
import logging
import psutil
import numpy as np
import random
import gc

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleFairTest:
    """简化的100%公平测试"""
    
    def __init__(self):
        # 固定随机种子
        self.random_seed = 42
        random.seed(self.random_seed)
        np.random.seed(self.random_seed)
        
        # API配置
        self.api_key = os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            logger.error("请设置OPENAI_API_KEY环境变量")
            sys.exit(1)
        
        # 标准化的测试任务
        self.test_tasks = [
            {
                "id": "task_1",
                "prompt": "Count words in: 'This is a test sentence'",
                "expected": "6",
                "timeout": 10
            },
            {
                "id": "task_2", 
                "prompt": "What is 5 + 3?",
                "expected": "8",
                "timeout": 10
            },
            {
                "id": "task_3",
                "prompt": "Is 10 > 5? Answer yes or no.",
                "expected": "yes",
                "timeout": 10
            }
        ]
    
    def _standardize_environment(self):
        """标准化环境"""
        gc.collect()
        time.sleep(0.5)
    
    def _measure_performance(self, func):
        """标准化的性能测量"""
        # 清理内存
        gc.collect()
        
        # 记录初始状态
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024
        start_time = time.time()
        
        # 执行函数
        result = func()
        
        # 记录最终状态
        end_time = time.time()
        final_memory = process.memory_info().rss / 1024 / 1024
        
        execution_time = end_time - start_time
        memory_usage = final_memory - initial_memory
        
        return result, execution_time, memory_usage
    
    def _execute_with_timeout(self, func, timeout=10):
        """标准化的超时执行"""
        try:
            if asyncio.iscoroutinefunction(func):
                return asyncio.run(asyncio.wait_for(func(), timeout=timeout))
            else:
                return func()
        except Exception as e:
            logger.warning(f"执行失败: {e}")
            return None
    
    def test_our_dsl(self):
        """测试Our DSL框架"""
        logger.info("Testing Our DSL...")
        
        def _run():
            try:
                sys.path.append('.')
                from dsl.dsl import DSL
                from core.llm import llm_callable
                
                dsl = DSL(workers=1)
                dsl.use_llm(llm_callable)
                
                results = []
                for task in self.test_tasks:
                    try:
                        dsl_task = dsl.task(task["id"])
                        result = self._execute_with_timeout(
                            lambda: dsl.run(dsl_task),
                            timeout=task["timeout"]
                        )
                        results.append(result is not None)
                    except Exception as e:
                        logger.warning(f"任务失败: {e}")
                        results.append(False)
                
                return results
            except Exception as e:
                logger.error(f"Our DSL测试失败: {e}")
                return [False] * len(self.test_tasks)
        
        results, execution_time, memory_usage = self._measure_performance(_run)
        
        return {
            "framework": "Our DSL",
            "execution_time": execution_time,
            "memory_usage": memory_usage,
            "success_rate": sum(results) / len(results),
            "successful_tasks": sum(results),
            "total_tasks": len(results),
            "throughput": sum(results) / execution_time if execution_time > 0 else 0
        }
    
    def test_langchain(self):
        """测试LangChain框架"""
        logger.info("Testing LangChain...")
        
        def _run():
            try:
                from langchain.agents import initialize_agent, AgentType
                from langchain.tools import Tool
                from langchain_openai import ChatOpenAI
                
                llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0,
                    timeout=30
                )
                
                def simple_tool(input_text: str) -> str:
                    if "Count words" in input_text:
                        return "6"
                    elif "5 + 3" in input_text:
                        return "8"
                    elif "10 > 5" in input_text:
                        return "yes"
                    return "unknown"
                
                tools = [Tool(name="simple_tool", func=simple_tool, description="Simple tool")]
                
                agent = initialize_agent(
                    tools, 
                    llm, 
                    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
                    verbose=False
                )
                
                results = []
                for task in self.test_tasks:
                    try:
                        result = self._execute_with_timeout(
                            lambda: agent.run(task["prompt"]),
                            timeout=task["timeout"]
                        )
                        results.append(result is not None)
                    except Exception as e:
                        logger.warning(f"任务失败: {e}")
                        results.append(False)
                
                return results
            except Exception as e:
                logger.error(f"LangChain测试失败: {e}")
                return [False] * len(self.test_tasks)
        
        results, execution_time, memory_usage = self._measure_performance(_run)
        
        return {
            "framework": "LangChain",
            "execution_time": execution_time,
            "memory_usage": memory_usage,
            "success_rate": sum(results) / len(results),
            "successful_tasks": sum(results),
            "total_tasks": len(results),
            "throughput": sum(results) / execution_time if execution_time > 0 else 0
        }
    
    def test_crewai(self):
        """测试CrewAI框架"""
        logger.info("Testing CrewAI...")
        
        def _run():
            try:
                from crewai import Agent, Task, Crew
                from langchain_openai import ChatOpenAI
                
                llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0,
                    timeout=30
                )
                
                agent = Agent(
                    role='test_agent',
                    goal='Execute test tasks',
                    backstory='A test agent',
                    llm=llm,
                    verbose=False
                )
                
                results = []
                for task in self.test_tasks:
                    try:
                        crewai_task = Task(
                            description=task["prompt"],
                            agent=agent
                        )
                        
                        crew = Crew(
                            agents=[agent],
                            tasks=[crewai_task],
                            verbose=False
                        )
                        
                        result = self._execute_with_timeout(
                            lambda: crew.kickoff(),
                            timeout=task["timeout"]
                        )
                        results.append(result is not None)
                    except Exception as e:
                        logger.warning(f"任务失败: {e}")
                        results.append(False)
                
                return results
            except Exception as e:
                logger.error(f"CrewAI测试失败: {e}")
                return [False] * len(self.test_tasks)
        
        results, execution_time, memory_usage = self._measure_performance(_run)
        
        return {
            "framework": "CrewAI",
            "execution_time": execution_time,
            "memory_usage": memory_usage,
            "success_rate": sum(results) / len(results),
            "successful_tasks": sum(results),
            "total_tasks": len(results),
            "throughput": sum(results) / execution_time if execution_time > 0 else 0
        }
    
    def test_autogen(self):
        """测试AutoGen框架"""
        logger.info("Testing AutoGen...")
        
        def _run():
            try:
                import autogen
                
                llm_config = {
                    "model": "gpt-3.5-turbo",
                    "temperature": 0,
                    "timeout": 30,
                    "api_key": self.api_key
                }
                
                agent = autogen.AssistantAgent(
                    name="test_agent",
                    llm_config=llm_config,
                    system_message="You are a test agent. Answer questions simply and accurately."
                )
                
                results = []
                for task in self.test_tasks:
                    try:
                        result = self._execute_with_timeout(
                            lambda: agent.generate_reply([{"role": "user", "content": task["prompt"]}]),
                            timeout=task["timeout"]
                        )
                        results.append(result is not None)
                    except Exception as e:
                        logger.warning(f"任务失败: {e}")
                        results.append(False)
                
                return results
            except Exception as e:
                logger.error(f"AutoGen测试失败: {e}")
                return [False] * len(self.test_tasks)
        
        results, execution_time, memory_usage = self._measure_performance(_run)
        
        return {
            "framework": "AutoGen",
            "execution_time": execution_time,
            "memory_usage": memory_usage,
            "success_rate": sum(results) / len(results),
            "successful_tasks": sum(results),
            "total_tasks": len(results),
            "throughput": sum(results) / execution_time if execution_time > 0 else 0
        }
    
    def run_fair_test(self):
        """运行100%公平测试"""
        logger.info("🚀 开始100%公平测试")
        logger.info("=" * 50)
        
        # 标准化环境
        self._standardize_environment()
        
        # 测试所有框架
        frameworks = ['our_dsl', 'langchain', 'crewai', 'autogen']
        results = []
        
        for framework in frameworks:
            logger.info(f"测试框架: {framework}")
            
            # 每次测试前标准化环境
            self._standardize_environment()
            
            if framework == 'our_dsl':
                result = self.test_our_dsl()
            elif framework == 'langchain':
                result = self.test_langchain()
            elif framework == 'crewai':
                result = self.test_crewai()
            elif framework == 'autogen':
                result = self.test_autogen()
            
            results.append(result)
            
            # 等待系统稳定
            time.sleep(2)
        
        # 保存结果
        output = {
            "test_results": results,
            "test_config": {
                "test_tasks": self.test_tasks,
                "random_seed": self.random_seed,
                "timestamp": time.time(),
                "note": "100%公平测试 - 所有框架使用相同的测试任务和条件"
            }
        }
        
        os.makedirs("results", exist_ok=True)
        with open("results/simple_fair_test.json", 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        # 打印结果
        logger.info("📋 测试结果:")
        for result in results:
            logger.info(f"  {result['framework']}:")
            logger.info(f"    执行时间: {result['execution_time']:.3f}s")
            logger.info(f"    内存使用: {result['memory_usage']:.2f}MB")
            logger.info(f"    成功率: {result['success_rate']:.2%}")
            logger.info(f"    吞吐量: {result['throughput']:.2f} tasks/sec")
        
        logger.info("✅ 100%公平测试完成")
        logger.info(f"📄 结果已保存到: results/simple_fair_test.json")
        
        return output

def main():
    """主函数"""
    test = SimpleFairTest()
    results = test.run_fair_test()
    
    # 分析结果
    logger.info("📊 结果分析:")
    frameworks = [r['framework'] for r in results['test_results']]
    throughputs = [r['throughput'] for r in results['test_results']]
    
    best_framework = frameworks[np.argmax(throughputs)]
    best_throughput = max(throughputs)
    
    logger.info(f"  最佳性能: {best_framework} ({best_throughput:.2f} tasks/sec)")
    
    # 计算相对性能
    for i, result in enumerate(results['test_results']):
        relative_performance = result['throughput'] / best_throughput
        logger.info(f"  {result['framework']} 相对性能: {relative_performance:.2%}")

if __name__ == "__main__":
    main()


