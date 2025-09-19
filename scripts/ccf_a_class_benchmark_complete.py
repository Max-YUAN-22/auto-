#!/usr/bin/env python3
"""
CCF A-Class Conference Standard Multi-Agent Framework Benchmark (Complete Real API)
CCF A类会议标准多智能体框架基准测试 (完整真实API版本)

This script runs complete CCF A-class experiments with real API calls.
这个脚本使用真实API调用运行完整的CCF A类实验。
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
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CCFAClassBenchmarkComplete:
    """CCF A-class conference standard multi-agent framework benchmarking (Complete Real API)"""
    
    def __init__(self):
        self.results = {}
        self.test_scenarios = [
            "traffic_management",
            "healthcare_coordination", 
            "financial_services",
            "smart_city_management"
        ]
        self.agent_counts = [1, 5, 10, 20, 50, 100]  # 包含100个智能体
        self.frameworks = ['our_dsl', 'langchain', 'crewai', 'autogen']  # 完整4个框架
        
        # Set up API configuration
        self.api_key = os.environ.get('OPENAI_API_KEY')
        self.base_url = os.environ.get('OPENAI_API_BASE', 'https://api.openai.com/v1')
        
        if not self.api_key:
            logger.error("请设置OPENAI_API_KEY环境变量")
            sys.exit(1)
        
        os.environ['OPENAI_API_KEY'] = self.api_key
        os.environ['OPENAI_API_BASE'] = self.base_url
        
        logger.info(f"API Key: {self.api_key[:10]}...")
        logger.info(f"API Base: {self.base_url}")
        
    def setup_environment(self):
        """Setup environment for all frameworks"""
        logger.info("Setting up environment for CCF A-class benchmarking with Complete Real API...")
        
        # Install missing packages
        packages_to_install = [
            'langchain',
            'langchain-openai', 
            'langchain-community',
            'openai',
            'crewai',
            'autogen'
        ]
        
        for package in packages_to_install:
            try:
                logger.info(f"Installing {package}...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                             check=True, capture_output=True, timeout=60)
                logger.info(f"✓ {package} installed successfully")
            except subprocess.TimeoutExpired:
                logger.warning(f"Timeout installing {package}")
            except subprocess.CalledProcessError as e:
                logger.warning(f"Failed to install {package}: {e}")
    
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
        """Test LangChain multi-agent framework with OpenAI API"""
        logger.info(f"Testing LangChain framework - {scenario} with {agent_count} agents")
        
        try:
            # Import LangChain components
            from langchain.agents import initialize_agent, AgentType
            from langchain.tools import Tool
            from langchain_openai import ChatOpenAI
            from langchain.schema import HumanMessage
            
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            # Create a simple tool for testing
            def dummy_tool(input_text: str) -> str:
                """Dummy tool for testing"""
                time.sleep(0.001)  # Simulate work
                return f"Processed: {input_text}"
            
            tools = [Tool(name="dummy_tool", func=dummy_tool, description="A dummy tool")]
            
            # Create LLM with OpenAI API
            llm = ChatOpenAI(
                temperature=0, 
                max_tokens=50, 
                model="gpt-4o-mini",
                api_key=self.api_key,
                base_url=self.base_url
            )
            
            # Create multiple agents
            agents = []
            for i in range(agent_count):
                try:
                    agent = initialize_agent(
                        tools=tools,
                        llm=llm,
                        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                        verbose=False,
                        handle_parsing_errors=True,
                        max_iterations=1
                    )
                    agents.append(agent)
                except Exception as e:
                    logger.warning(f"Failed to create LangChain agent {i}: {e}")
                    continue
            
            if not agents:
                return {
                    'framework': 'LangChain',
                    'scenario': scenario,
                    'agent_count': agent_count,
                    'status': 'error',
                    'error': 'No agents created successfully'
                }
            
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
            throughput = len(agents) / execution_time
            memory_usage = end_memory - start_memory
            successful_tasks = sum(1 for r in results if r is not None)
            success_rate = successful_tasks / len(agents)
            
            return {
                'framework': 'LangChain',
                'scenario': scenario,
                'agent_count': len(agents),
                'execution_time': execution_time,
                'throughput': throughput,
                'memory_usage': memory_usage,
                'success_rate': success_rate,
                'successful_tasks': successful_tasks,
                'avg_latency': execution_time / len(agents),
                'status': 'success'
            }
            
        except ImportError as e:
            logger.warning(f"LangChain not available: {e}")
            return {
                'framework': 'LangChain',
                'scenario': scenario,
                'agent_count': agent_count,
                'status': 'not_available',
                'note': f'LangChain not available: {e}'
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
        """Test CrewAI framework with OpenAI API"""
        logger.info(f"Testing CrewAI framework - {scenario} with {agent_count} agents")
        
        try:
            # Import CrewAI components
            from crewai import Agent, Task, Crew
            from langchain_openai import ChatOpenAI
            
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            # Create LLM with OpenAI API
            llm = ChatOpenAI(
                model="gpt-4o-mini",
                api_key=self.api_key,
                base_url=self.base_url,
                temperature=0
            )
            
            # Create agents
            agents = []
            for i in range(agent_count):
                try:
                    if scenario == "traffic_management":
                        agent = Agent(
                            role='traffic_analyst',
                            goal=f'Analyze traffic conditions at intersection {i}',
                            backstory=f'You are an expert traffic analyst for intersection {i}',
                            llm=llm,
                            verbose=False
                        )
                    elif scenario == "healthcare_coordination":
                        agent = Agent(
                            role='healthcare_coordinator',
                            goal=f'Coordinate patient care for patient {i}',
                            backstory=f'You are a healthcare coordinator for patient {i}',
                            llm=llm,
                            verbose=False
                        )
                    elif scenario == "financial_services":
                        agent = Agent(
                            role='financial_analyst',
                            goal=f'Process financial transaction {i}',
                            backstory=f'You are a financial analyst for transaction {i}',
                            llm=llm,
                            verbose=False
                        )
                    else:  # smart_city_management
                        agent = Agent(
                            role='city_manager',
                            goal=f'Manage city service {i}',
                            backstory=f'You are a city manager for service {i}',
                            llm=llm,
                            verbose=False
                        )
                    
                    agents.append(agent)
                except Exception as e:
                    logger.warning(f"Failed to create CrewAI agent {i}: {e}")
                    continue
            
            if not agents:
                return {
                    'framework': 'CrewAI',
                    'scenario': scenario,
                    'agent_count': agent_count,
                    'status': 'error',
                    'error': 'No agents created successfully'
                }
            
            # Create tasks and execute
            results = []
            for i, agent in enumerate(agents):
                try:
                    if scenario == "traffic_management":
                        task = Task(
                            description=f"Analyze traffic conditions at intersection {i}",
                            agent=agent,
                            expected_output=f"Traffic analysis report for intersection {i}"
                        )
                    elif scenario == "healthcare_coordination":
                        task = Task(
                            description=f"Coordinate patient care for patient {i}",
                            agent=agent,
                            expected_output=f"Patient care coordination plan for patient {i}"
                        )
                    elif scenario == "financial_services":
                        task = Task(
                            description=f"Process financial transaction {i}",
                            agent=agent,
                            expected_output=f"Financial transaction analysis for transaction {i}"
                        )
                    else:
                        task = Task(
                            description=f"Manage city service {i}",
                            agent=agent,
                            expected_output=f"City service management plan for service {i}"
                        )
                    
                    # Create crew and execute
                    crew = Crew(
                        agents=[agent],
                        tasks=[task],
                        verbose=False
                    )
                    
                    result = await asyncio.to_thread(crew.kickoff)
                    results.append(result)
                except Exception as e:
                    logger.error(f"CrewAI task execution failed: {e}")
                    results.append(None)
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            execution_time = end_time - start_time
            throughput = len(agents) / execution_time
            memory_usage = end_memory - start_memory
            successful_tasks = sum(1 for r in results if r is not None)
            success_rate = successful_tasks / len(agents)
            
            return {
                'framework': 'CrewAI',
                'scenario': scenario,
                'agent_count': len(agents),
                'execution_time': execution_time,
                'throughput': throughput,
                'memory_usage': memory_usage,
                'success_rate': success_rate,
                'successful_tasks': successful_tasks,
                'avg_latency': execution_time / len(agents),
                'status': 'success'
            }
            
        except ImportError as e:
            logger.warning(f"CrewAI not available: {e}")
            return {
                'framework': 'CrewAI',
                'scenario': scenario,
                'agent_count': agent_count,
                'status': 'not_available',
                'note': f'CrewAI not available: {e}'
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
        """Test AutoGen framework with OpenAI API"""
        logger.info(f"Testing AutoGen framework - {scenario} with {agent_count} agents")
        
        try:
            # Import AutoGen components
            import autogen
            from autogen import ConversableAgent, GroupChat, GroupChatManager
            
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            # Configure AutoGen
            config_list = [{
                "model": "gpt-4o-mini",
                "api_key": self.api_key,
                "base_url": self.base_url,
            }]
            
            # Create agents
            agents = []
            for i in range(agent_count):
                try:
                    agent = ConversableAgent(
                        name=f"agent_{i}",
                        system_message=f"You are an expert in {scenario}",
                        llm_config={"config_list": config_list},
                        human_input_mode="NEVER"
                    )
                    agents.append(agent)
                except Exception as e:
                    logger.warning(f"Failed to create AutoGen agent {i}: {e}")
                    continue
            
            if not agents:
                return {
                    'framework': 'AutoGen',
                    'scenario': scenario,
                    'agent_count': agent_count,
                    'status': 'error',
                    'error': 'No agents created successfully'
                }
            
            # Create group chat
            group_chat = GroupChat(
                agents=agents,
                messages=[],
                max_round=1
            )
            
            manager = GroupChatManager(
                groupchat=group_chat,
                llm_config={"config_list": config_list}
            )
            
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
                    
                    result = await asyncio.to_thread(
                        agent.initiate_chat, 
                        manager, 
                        message=message
                    )
                    results.append(result)
                except Exception as e:
                    logger.error(f"AutoGen agent execution failed: {e}")
                    results.append(None)
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            execution_time = end_time - start_time
            throughput = len(agents) / execution_time
            memory_usage = end_memory - start_memory
            successful_tasks = sum(1 for r in results if r is not None)
            success_rate = successful_tasks / len(agents)
            
            return {
                'framework': 'AutoGen',
                'scenario': scenario,
                'agent_count': len(agents),
                'execution_time': execution_time,
                'throughput': throughput,
                'memory_usage': memory_usage,
                'success_rate': success_rate,
                'successful_tasks': successful_tasks,
                'avg_latency': execution_time / len(agents),
                'status': 'success'
            }
            
        except ImportError as e:
            logger.warning(f"AutoGen not available: {e}")
            return {
                'framework': 'AutoGen',
                'scenario': scenario,
                'agent_count': agent_count,
                'status': 'not_available',
                'note': f'AutoGen not available: {e}'
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
    
    async def run_ccf_a_class_benchmark(self):
        """Run CCF A-class conference standard benchmark"""
        logger.info("Starting CCF A-class conference standard multi-agent system benchmark with Complete Real API...")
        
        # Setup environment
        self.setup_environment()
        
        all_results = []
        
        for scenario in self.test_scenarios:
            logger.info(f"\n=== Testing Scenario: {scenario} ===")
            
            for agent_count in self.agent_counts:
                logger.info(f"\n--- Testing with {agent_count} agents ---")
                
                for framework in self.frameworks:
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
                'agent_counts': self.agent_counts,
                'frameworks': self.frameworks,
                'timestamp': time.time(),
                'api_provider': 'OpenAI Complete',
                'api_key': self.api_key[:10] + '...',
                'note': 'Complete CCF A-class benchmark with all frameworks using real API'
            }
        }
        
        os.makedirs('results', exist_ok=True)
        with open('results/ccf_a_class_benchmark_complete.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        logger.info("CCF A-class benchmark completed!")
        return all_results
    
    def print_results(self):
        """Print CCF A-class benchmark results"""
        print("\n" + "="*80)
        print("CCF A-CLASS CONFERENCE STANDARD MULTI-AGENT SYSTEM BENCHMARK RESULTS (COMPLETE)")
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
    print("CCF A-Class Conference Standard Multi-Agent Framework Benchmarking (Complete Real API)")
    print("=" * 80)
    
    # Check API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("错误: 请设置OPENAI_API_KEY环境变量")
        print("例如: export OPENAI_API_KEY='your-api-key-here'")
        print("例如: export OPENAI_API_BASE='https://www.yunqiaoai.top/v1'")
        sys.exit(1)
    
    # Create benchmarker
    benchmarker = CCFAClassBenchmarkComplete()
    
    # Run CCF A-class benchmark
    results = await benchmarker.run_ccf_a_class_benchmark()
    
    # Print results
    benchmarker.print_results()
    
    print(f"\nResults saved to: results/ccf_a_class_benchmark_complete.json")
    print(f"Total tests completed: {len(results)}")
    print(f"API Provider: OpenAI Complete")
    print(f"API Key: {os.environ['OPENAI_API_KEY'][:10]}...")
    print(f"\nNote: Complete CCF A-class benchmark with all frameworks using real API")

if __name__ == "__main__":
    asyncio.run(main())

