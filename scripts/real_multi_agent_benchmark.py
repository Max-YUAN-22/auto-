#!/usr/bin/env python3
"""
Real Multi-Agent System Benchmarking Framework
真实多智能体系统基准测试框架

This script implements real benchmarking of multi-agent systems including:
- Our DSL framework
- LangChain multi-agent
- CrewAI
- AutoGen

All tests use real implementations and measure actual performance.
这个脚本实现真实的多智能体系统基准测试，包括我们的DSL框架、LangChain、CrewAI、AutoGen。
所有测试都使用真实实现并测量实际性能。
"""

import asyncio
import time
import json
import os
import sys
import subprocess
import importlib
from typing import Dict, List, Any, Optional
import logging
import psutil
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import threading

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RealMultiAgentBenchmark:
    """Real multi-agent system benchmarking"""
    
    def __init__(self):
        self.results = {}
        self.test_scenarios = [
            "traffic_management",
            "healthcare_coordination", 
            "financial_services",
            "smart_city_management"
        ]
        
    def check_dependencies(self):
        """Check if required frameworks are installed"""
        frameworks = {
            'langchain': 'langchain',
            'crewai': 'crewai', 
            'autogen': 'pyautogen',
            'our_dsl': 'dsl'
        }
        
        available = {}
        for name, module in frameworks.items():
            try:
                if name == 'our_dsl':
                    # Check our DSL framework
                    sys.path.append('.')
                    import dsl.dsl
                    available[name] = True
                    logger.info(f"✓ Our DSL framework available")
                else:
                    importlib.import_module(module)
                    available[name] = True
                    logger.info(f"✓ {name} framework available")
            except ImportError:
                available[name] = False
                logger.warning(f"✗ {name} framework not available")
        
        return available
    
    def install_frameworks(self):
        """Install required frameworks"""
        logger.info("Installing required frameworks...")
        
        frameworks = [
            'langchain',
            'crewai',
            'pyautogen'
        ]
        
        for framework in frameworks:
            try:
                logger.info(f"Installing {framework}...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', framework], 
                             check=True, capture_output=True)
                logger.info(f"✓ {framework} installed successfully")
            except subprocess.CalledProcessError as e:
                logger.error(f"✗ Failed to install {framework}: {e}")
    
    async def test_our_dsl_framework(self, scenario: str, agent_count: int):
        """Test our DSL framework with real implementation"""
        logger.info(f"Testing our DSL framework - {scenario} with {agent_count} agents")
        
        try:
            # Import our DSL framework
            sys.path.append('.')
            from dsl.dsl import DSL
            from core.llm import llm_callable
            
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            # Create DSL instance
            dsl = DSL(workers=min(agent_count, 8))
            dsl.use_llm(llm_callable)
            
            # Create tasks based on scenario
            tasks = []
            for i in range(agent_count):
                if scenario == "traffic_management":
                    task = dsl.gen(f"traffic_task_{i}", 
                                 prompt=f"Analyze traffic conditions at intersection {i}",
                                 agent="traffic_manager")
                elif scenario == "healthcare_coordination":
                    task = dsl.gen(f"healthcare_task_{i}",
                                 prompt=f"Coordinate patient care for patient {i}",
                                 agent="healthcare_coordinator")
                elif scenario == "financial_services":
                    task = dsl.gen(f"financial_task_{i}",
                                 prompt=f"Process financial transaction {i}",
                                 agent="financial_analyst")
                else:  # smart_city_management
                    task = dsl.gen(f"city_task_{i}",
                                 prompt=f"Manage city service {i}",
                                 agent="city_manager")
                
                tasks.append(task)
            
            # Execute tasks
            results = []
            for task in tasks:
                try:
                    result = await asyncio.to_thread(task.schedule)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Task execution failed: {e}")
                    results.append(None)
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            execution_time = end_time - start_time
            throughput = agent_count / execution_time
            memory_usage = end_memory - start_memory
            successful_tasks = sum(1 for r in results if r is not None)
            success_rate = successful_tasks / agent_count
            
            return {
                'framework': 'Our DSL',
                'scenario': scenario,
                'agent_count': agent_count,
                'execution_time': execution_time,
                'throughput': throughput,
                'memory_usage': memory_usage,
                'success_rate': success_rate,
                'successful_tasks': successful_tasks,
                'avg_latency': execution_time / agent_count,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Our DSL test failed: {e}")
            return {
                'framework': 'Our DSL',
                'scenario': scenario,
                'agent_count': agent_count,
                'status': 'error',
                'error': str(e)
            }
    
    async def test_langchain_framework(self, scenario: str, agent_count: int):
        """Test LangChain multi-agent framework"""
        logger.info(f"Testing LangChain framework - {scenario} with {agent_count} agents")
        
        try:
            from langchain.agents import initialize_agent, AgentType
            from langchain.llms import OpenAI
            from langchain.tools import Tool
            
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            # Create LangChain agents
            def dummy_tool(input_text: str) -> str:
                """Dummy tool for testing"""
                time.sleep(0.001)  # Simulate work
                return f"Processed: {input_text}"
            
            tools = [Tool(name="dummy_tool", func=dummy_tool, description="A dummy tool")]
            
            # Create multiple agents
            agents = []
            for i in range(agent_count):
                agent = initialize_agent(
                    tools=tools,
                    llm=OpenAI(temperature=0),
                    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                    verbose=False
                )
                agents.append(agent)
            
            # Execute tasks
            results = []
            for i, agent in enumerate(agents):
                try:
                    if scenario == "traffic_management":
                        prompt = f"Analyze traffic conditions at intersection {i}"
                    elif scenario == "healthcare_coordination":
                        prompt = f"Coordinate patient care for patient {i}"
                    elif scenario == "financial_services":
                        prompt = f"Process financial transaction {i}"
                    else:
                        prompt = f"Manage city service {i}"
                    
                    result = await asyncio.to_thread(agent.run, prompt)
                    results.append(result)
                except Exception as e:
                    logger.error(f"LangChain agent execution failed: {e}")
                    results.append(None)
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            execution_time = end_time - start_time
            throughput = agent_count / execution_time
            memory_usage = end_memory - start_memory
            successful_tasks = sum(1 for r in results if r is not None)
            success_rate = successful_tasks / agent_count
            
            return {
                'framework': 'LangChain',
                'scenario': scenario,
                'agent_count': agent_count,
                'execution_time': execution_time,
                'throughput': throughput,
                'memory_usage': memory_usage,
                'success_rate': success_rate,
                'successful_tasks': successful_tasks,
                'avg_latency': execution_time / agent_count,
                'status': 'success'
            }
            
        except ImportError:
            logger.warning("LangChain not installed, skipping test")
            return {
                'framework': 'LangChain',
                'scenario': scenario,
                'agent_count': agent_count,
                'status': 'not_available',
                'note': 'LangChain not installed'
            }
        except Exception as e:
            logger.error(f"LangChain test failed: {e}")
            return {
                'framework': 'LangChain',
                'scenario': scenario,
                'agent_count': agent_count,
                'status': 'error',
                'error': str(e)
            }
    
    async def test_crewai_framework(self, scenario: str, agent_count: int):
        """Test CrewAI framework"""
        logger.info(f"Testing CrewAI framework - {scenario} with {agent_count} agents")
        
        try:
            from crewai import Agent, Task, Crew
            
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            # Create CrewAI agents and tasks
            agents = []
            tasks = []
            
            for i in range(agent_count):
                if scenario == "traffic_management":
                    agent = Agent(
                        role='Traffic Manager',
                        goal=f'Analyze traffic conditions at intersection {i}',
                        backstory='You are a traffic management expert.',
                        verbose=False
                    )
                    task = Task(
                        description=f'Analyze traffic conditions at intersection {i}',
                        agent=agent
                    )
                elif scenario == "healthcare_coordination":
                    agent = Agent(
                        role='Healthcare Coordinator',
                        goal=f'Coordinate patient care for patient {i}',
                        backstory='You are a healthcare coordination expert.',
                        verbose=False
                    )
                    task = Task(
                        description=f'Coordinate patient care for patient {i}',
                        agent=agent
                    )
                elif scenario == "financial_services":
                    agent = Agent(
                        role='Financial Analyst',
                        goal=f'Process financial transaction {i}',
                        backstory='You are a financial analysis expert.',
                        verbose=False
                    )
                    task = Task(
                        description=f'Process financial transaction {i}',
                        agent=agent
                    )
                else:  # smart_city_management
                    agent = Agent(
                        role='City Manager',
                        goal=f'Manage city service {i}',
                        backstory='You are a smart city management expert.',
                        verbose=False
                    )
                    task = Task(
                        description=f'Manage city service {i}',
                        agent=agent
                    )
                
                agents.append(agent)
                tasks.append(task)
            
            # Create crew and execute
            crew = Crew(agents=agents, tasks=tasks, verbose=False)
            
            # Execute tasks
            results = []
            for task in tasks:
                try:
                    result = await asyncio.to_thread(crew.kickoff)
                    results.append(result)
                except Exception as e:
                    logger.error(f"CrewAI task execution failed: {e}")
                    results.append(None)
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            execution_time = end_time - start_time
            throughput = agent_count / execution_time
            memory_usage = end_memory - start_memory
            successful_tasks = sum(1 for r in results if r is not None)
            success_rate = successful_tasks / agent_count
            
            return {
                'framework': 'CrewAI',
                'scenario': scenario,
                'agent_count': agent_count,
                'execution_time': execution_time,
                'throughput': throughput,
                'memory_usage': memory_usage,
                'success_rate': success_rate,
                'successful_tasks': successful_tasks,
                'avg_latency': execution_time / agent_count,
                'status': 'success'
            }
            
        except ImportError:
            logger.warning("CrewAI not installed, skipping test")
            return {
                'framework': 'CrewAI',
                'scenario': scenario,
                'agent_count': agent_count,
                'status': 'not_available',
                'note': 'CrewAI not installed'
            }
        except Exception as e:
            logger.error(f"CrewAI test failed: {e}")
            return {
                'framework': 'CrewAI',
                'scenario': scenario,
                'agent_count': agent_count,
                'status': 'error',
                'error': str(e)
            }
    
    async def test_autogen_framework(self, scenario: str, agent_count: int):
        """Test AutoGen framework"""
        logger.info(f"Testing AutoGen framework - {scenario} with {agent_count} agents")
        
        try:
            import autogen
            
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            # Create AutoGen agents
            agents = []
            for i in range(agent_count):
                if scenario == "traffic_management":
                    agent = autogen.AssistantAgent(
                        name=f"traffic_manager_{i}",
                        system_message=f"You are a traffic management expert analyzing intersection {i}."
                    )
                elif scenario == "healthcare_coordination":
                    agent = autogen.AssistantAgent(
                        name=f"healthcare_coordinator_{i}",
                        system_message=f"You are a healthcare coordinator managing patient {i}."
                    )
                elif scenario == "financial_services":
                    agent = autogen.AssistantAgent(
                        name=f"financial_analyst_{i}",
                        system_message=f"You are a financial analyst processing transaction {i}."
                    )
                else:  # smart_city_management
                    agent = autogen.AssistantAgent(
                        name=f"city_manager_{i}",
                        system_message=f"You are a city manager handling service {i}."
                    )
                
                agents.append(agent)
            
            # Execute tasks
            results = []
            for i, agent in enumerate(agents):
                try:
                    if scenario == "traffic_management":
                        message = f"Analyze traffic conditions at intersection {i}"
                    elif scenario == "healthcare_coordination":
                        message = f"Coordinate patient care for patient {i}"
                    elif scenario == "financial_services":
                        message = f"Process financial transaction {i}"
                    else:
                        message = f"Manage city service {i}"
                    
                    result = await asyncio.to_thread(agent.generate_reply, [{"role": "user", "content": message}])
                    results.append(result)
                except Exception as e:
                    logger.error(f"AutoGen agent execution failed: {e}")
                    results.append(None)
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            execution_time = end_time - start_time
            throughput = agent_count / execution_time
            memory_usage = end_memory - start_memory
            successful_tasks = sum(1 for r in results if r is not None)
            success_rate = successful_tasks / agent_count
            
            return {
                'framework': 'AutoGen',
                'scenario': scenario,
                'agent_count': agent_count,
                'execution_time': execution_time,
                'throughput': throughput,
                'memory_usage': memory_usage,
                'success_rate': success_rate,
                'successful_tasks': successful_tasks,
                'avg_latency': execution_time / agent_count,
                'status': 'success'
            }
            
        except ImportError:
            logger.warning("AutoGen not installed, skipping test")
            return {
                'framework': 'AutoGen',
                'scenario': scenario,
                'agent_count': agent_count,
                'status': 'not_available',
                'note': 'AutoGen not installed'
            }
        except Exception as e:
            logger.error(f"AutoGen test failed: {e}")
            return {
                'framework': 'AutoGen',
                'scenario': scenario,
                'agent_count': agent_count,
                'status': 'error',
                'error': str(e)
            }
    
    async def run_comprehensive_benchmark(self):
        """Run comprehensive benchmark across all frameworks and scenarios"""
        logger.info("Starting comprehensive multi-agent system benchmark...")
        
        # Check dependencies
        available_frameworks = self.check_dependencies()
        
        # Install missing frameworks if needed
        if not all(available_frameworks.values()):
            logger.info("Some frameworks are missing. Installing...")
            self.install_frameworks()
            available_frameworks = self.check_dependencies()
        
        # Test configurations
        agent_counts = [1, 5, 10, 20, 50]
        frameworks_to_test = ['our_dsl', 'langchain', 'crewai', 'autogen']
        
        all_results = []
        
        for scenario in self.test_scenarios:
            logger.info(f"\n=== Testing Scenario: {scenario} ===")
            
            for agent_count in agent_counts:
                logger.info(f"\n--- Testing with {agent_count} agents ---")
                
                for framework in frameworks_to_test:
                    if not available_frameworks.get(framework, False):
                        logger.warning(f"Skipping {framework} - not available")
                        continue
                    
                    if framework == 'our_dsl':
                        result = await self.test_our_dsl_framework(scenario, agent_count)
                    elif framework == 'langchain':
                        result = await self.test_langchain_framework(scenario, agent_count)
                    elif framework == 'crewai':
                        result = await self.test_crewai_framework(scenario, agent_count)
                    elif framework == 'autogen':
                        result = await self.test_autogen_framework(scenario, agent_count)
                    
                    all_results.append(result)
                    
                    if result['status'] == 'success':
                        logger.info(f"{framework}: {result['throughput']:.2f} tasks/sec, "
                                  f"{result['memory_usage']:.2f} MB, "
                                  f"{result['success_rate']:.3f} success rate")
                    else:
                        logger.warning(f"{framework}: {result['status']}")
        
        # Save results
        self.results = {
            'benchmark_results': all_results,
            'test_config': {
                'scenarios': self.test_scenarios,
                'agent_counts': agent_counts,
                'frameworks': frameworks_to_test,
                'timestamp': time.time()
            }
        }
        
        os.makedirs('results', exist_ok=True)
        with open('results/real_multi_agent_benchmark.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        logger.info("Comprehensive benchmark completed!")
        return all_results
    
    def print_results(self):
        """Print benchmark results"""
        print("\n" + "="*80)
        print("REAL MULTI-AGENT SYSTEM BENCHMARK RESULTS")
        print("="*80)
        
        # Group results by framework
        framework_results = {}
        for result in self.results.get('benchmark_results', []):
            framework = result['framework']
            if framework not in framework_results:
                framework_results[framework] = []
            framework_results[framework].append(result)
        
        for framework, results in framework_results.items():
            print(f"\n{framework} Framework:")
            print("-" * 50)
            
            # Group by scenario
            scenario_results = {}
            for result in results:
                scenario = result['scenario']
                if scenario not in scenario_results:
                    scenario_results[scenario] = []
                scenario_results[scenario].append(result)
            
            for scenario, scenario_data in scenario_results.items():
                print(f"\n  {scenario}:")
                for result in scenario_data:
                    if result['status'] == 'success':
                        print(f"    {result['agent_count']} agents: "
                              f"{result['throughput']:,.2f} tasks/sec, "
                              f"{result['memory_usage']:.2f} MB, "
                              f"{result['success_rate']:.3f} success rate")
                    else:
                        print(f"    {result['agent_count']} agents: {result['status']}")

async def main():
    """Main function"""
    print("Real Multi-Agent System Benchmarking Framework")
    print("=" * 60)
    
    # Create benchmarker
    benchmarker = RealMultiAgentBenchmark()
    
    # Run comprehensive benchmark
    results = await benchmarker.run_comprehensive_benchmark()
    
    # Print results
    benchmarker.print_results()
    
    print(f"\nResults saved to: results/real_multi_agent_benchmark.json")

if __name__ == "__main__":
    asyncio.run(main())

