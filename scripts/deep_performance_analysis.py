#!/usr/bin/env python3
"""
深度性能分析 - 找出真正的瓶颈
Deep Performance Analysis - Find Real Bottlenecks
"""

import time
import json
import sys
import os
from typing import Dict, List, Any
import tracemalloc
import psutil
import threading
from concurrent.futures import ThreadPoolExecutor
import asyncio

# 添加项目路径
sys.path.append('.')

def analyze_llm_call_performance():
    """分析LLM调用性能"""
    print("🔍 分析LLM调用性能...")
    
    # 导入LLM模块
    try:
        from core.llm import llm_callable
        print("✅ 成功导入LLM模块")
    except Exception as e:
        print(f"❌ 导入LLM模块失败: {e}")
        return
    
    # 测试LLM调用性能
    test_prompts = [
        "Calculate 1 + 1",
        "Count words in: 'Hello world'",
        "Sum of [1, 2, 3]",
        "Choose larger: 5 or 10"
    ]
    
    print("\n📊 LLM调用性能测试:")
    
    for i, prompt in enumerate(test_prompts):
        start_time = time.time()
        try:
            result = llm_callable(prompt, "default")
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"   测试 {i+1}: {execution_time*1000:.2f}ms - {prompt[:20]}...")
        except Exception as e:
            print(f"   测试 {i+1}: 失败 - {e}")

def analyze_framework_overhead():
    """分析框架开销"""
    print("\n🔍 分析框架开销...")
    
    # 测试直接执行
    def direct_execution():
        """直接执行任务"""
        start_time = time.time()
        # 模拟任务执行
        result = "Task completed"
        end_time = time.time()
        return end_time - start_time
    
    # 测试DSL执行
    def dsl_execution():
        """通过DSL执行任务"""
        try:
            from dsl.fast_dsl import FastDSL
            from core.llm import llm_callable
            
            dsl = FastDSL(workers=1)
            dsl.use_llm(llm_callable)
            
            start_time = time.time()
            task = dsl.task("test", prompt="Calculate 1 + 1", agent="default")
            scheduled_task = task.schedule()
            result = scheduled_task.wait(timeout=5)
            end_time = time.time()
            
            dsl.shutdown()
            return end_time - start_time
        except Exception as e:
            print(f"DSL执行失败: {e}")
            return None
    
    # 测试其他框架
    def langchain_execution():
        """LangChain执行"""
        try:
            from langchain.agents import initialize_agent, AgentType
            from langchain.tools import Tool
            from langchain_openai import ChatOpenAI
            
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, timeout=30)
            
            def simple_tool(input_text: str) -> str:
                return "Task completed"
            
            tools = [Tool(name="simple_tool", func=simple_tool, description="Simple tool")]
            agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)
            
            start_time = time.time()
            result = agent.run("Calculate 1 + 1")
            end_time = time.time()
            
            return end_time - start_time
        except Exception as e:
            print(f"LangChain执行失败: {e}")
            return None
    
    # 运行测试
    print("\n📊 框架开销测试:")
    
    # 直接执行
    direct_time = direct_execution()
    print(f"   直接执行: {direct_time*1000:.2f}ms")
    
    # DSL执行
    dsl_time = dsl_execution()
    if dsl_time:
        print(f"   DSL执行: {dsl_time*1000:.2f}ms")
        print(f"   DSL开销: {(dsl_time - direct_time)*1000:.2f}ms")
    
    # LangChain执行
    langchain_time = langchain_execution()
    if langchain_time:
        print(f"   LangChain执行: {langchain_time*1000:.2f}ms")
        print(f"   LangChain开销: {(langchain_time - direct_time)*1000:.2f}ms")

def analyze_memory_usage():
    """分析内存使用"""
    print("\n🔍 分析内存使用...")
    
    process = psutil.Process()
    
    # 测试不同框架的内存使用
    frameworks = {
        "Direct": lambda: "Task completed",
        "DSL": lambda: exec_dsl_task(),
        "LangChain": lambda: exec_langchain_task()
    }
    
    def exec_dsl_task():
        try:
            from dsl.fast_dsl import FastDSL
            from core.llm import llm_callable
            
            dsl = FastDSL(workers=1)
            dsl.use_llm(llm_callable)
            task = dsl.task("test", prompt="Calculate 1 + 1", agent="default")
            scheduled_task = task.schedule()
            result = scheduled_task.wait(timeout=5)
            dsl.shutdown()
            return result
        except Exception as e:
            return f"Error: {e}"
    
    def exec_langchain_task():
        try:
            from langchain.agents import initialize_agent, AgentType
            from langchain.tools import Tool
            from langchain_openai import ChatOpenAI
            
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, timeout=30)
            
            def simple_tool(input_text: str) -> str:
                return "Task completed"
            
            tools = [Tool(name="simple_tool", func=simple_tool, description="Simple tool")]
            agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)
            
            result = agent.run("Calculate 1 + 1")
            return result
        except Exception as e:
            return f"Error: {e}"
    
    print("\n📊 内存使用测试:")
    
    for name, func in frameworks.items():
        initial_memory = process.memory_info().rss / 1024 / 1024
        
        try:
            result = func()
            final_memory = process.memory_info().rss / 1024 / 1024
            memory_delta = final_memory - initial_memory
            
            print(f"   {name}: {memory_delta:.2f} MB")
        except Exception as e:
            print(f"   {name}: 失败 - {e}")

def analyze_concurrent_performance():
    """分析并发性能"""
    print("\n🔍 分析并发性能...")
    
    def test_concurrent_execution(workers: int, tasks: int):
        """测试并发执行"""
        def worker_task():
            return "Task completed"
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(worker_task) for _ in range(tasks)]
            results = [future.result() for future in futures]
        
        end_time = time.time()
        execution_time = end_time - start_time
        throughput = tasks / execution_time
        
        return execution_time, throughput
    
    print("\n📊 并发性能测试:")
    
    test_configs = [
        (1, 10),
        (5, 50),
        (10, 100)
    ]
    
    for workers, tasks in test_configs:
        execution_time, throughput = test_concurrent_execution(workers, tasks)
        print(f"   {workers} workers, {tasks} tasks: {execution_time*1000:.2f}ms, {throughput:.2f} tasks/sec")

def main():
    """主函数"""
    print("🚀 深度性能分析开始")
    print("=" * 60)
    
    # 分析LLM调用性能
    analyze_llm_call_performance()
    
    # 分析框架开销
    analyze_framework_overhead()
    
    # 分析内存使用
    analyze_memory_usage()
    
    # 分析并发性能
    analyze_concurrent_performance()
    
    print("\n" + "=" * 60)
    print("✅ 深度性能分析完成")

if __name__ == "__main__":
    main()
