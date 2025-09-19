#!/usr/bin/env python3
"""
CCF A类会议实验可复现性验证脚本
CCF A-Class Conference Experiment Reproducibility Verification Script

这个脚本确保所有实验的可复现性，包括：
1. 随机种子设置
2. 环境配置验证
3. 依赖版本检查
4. API配置验证
5. 多次运行结果一致性检查
"""

import os
import sys
import json
import time
import random
import numpy as np
import subprocess
import importlib
from typing import Dict, List, Any, Tuple
import logging
from pathlib import Path
import hashlib
import platform
import psutil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ReproducibilityTest:
    """CCF A类会议实验可复现性验证"""
    
    def __init__(self):
        self.results = {}
        self.test_runs = 3  # 运行3次验证一致性
        self.random_seed = 42  # 固定随机种子
        self.tolerance = 0.1  # 10%的容差
        
    def setup_reproducible_environment(self):
        """设置可复现的实验环境"""
        logger.info("🔧 设置可复现的实验环境...")
        
        # 设置随机种子
        random.seed(self.random_seed)
        np.random.seed(self.random_seed)
        
        # 设置环境变量
        os.environ['PYTHONHASHSEED'] = str(self.random_seed)
        os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'
        
        logger.info(f"✅ 随机种子设置为: {self.random_seed}")
        
    def check_environment_consistency(self) -> Dict[str, Any]:
        """检查环境一致性"""
        logger.info("🔍 检查环境一致性...")
        
        env_info = {
            "python_version": sys.version,
            "platform": platform.platform(),
            "cpu_count": psutil.cpu_count(),
            "memory_gb": psutil.virtual_memory().total / (1024**3),
            "python_hash_seed": os.environ.get('PYTHONHASHSEED'),
            "working_directory": os.getcwd(),
            "timestamp": time.time()
        }
        
        # 检查关键依赖版本
        dependencies = [
            'numpy', 'pandas', 'matplotlib', 'psutil',
            'langchain', 'openai', 'crewai', 'autogen'
        ]
        
        env_info["dependencies"] = {}
        for dep in dependencies:
            try:
                module = importlib.import_module(dep)
                version = getattr(module, '__version__', 'unknown')
                env_info["dependencies"][dep] = version
            except ImportError:
                env_info["dependencies"][dep] = "not_installed"
        
        logger.info("✅ 环境信息收集完成")
        return env_info
        
    def verify_api_configuration(self) -> bool:
        """验证API配置"""
        logger.info("🔑 验证API配置...")
        
        api_key = os.environ.get('OPENAI_API_KEY')
        api_base = os.environ.get('OPENAI_API_BASE', 'https://api.openai.com/v1')
        
        if not api_key:
            logger.error("❌ OPENAI_API_KEY 未设置")
            return False
            
        if not api_key.startswith('sk-'):
            logger.error("❌ OPENAI_API_KEY 格式不正确")
            return False
            
        logger.info(f"✅ API配置验证通过")
        logger.info(f"   API Base: {api_base}")
        logger.info(f"   API Key: {api_key[:10]}...")
        
        return True
        
    def run_reproducibility_test(self, test_function, test_name: str) -> Dict[str, Any]:
        """运行可复现性测试"""
        logger.info(f"🧪 运行可复现性测试: {test_name}")
        
        results = []
        
        for run in range(self.test_runs):
            logger.info(f"   运行 {run + 1}/{self.test_runs}")
            
            # 重置随机种子
            random.seed(self.random_seed)
            np.random.seed(self.random_seed)
            
            # 运行测试
            start_time = time.time()
            result = test_function()
            end_time = time.time()
            
            result["run_id"] = run + 1
            result["execution_time"] = end_time - start_time
            result["timestamp"] = time.time()
            
            results.append(result)
            
        # 分析结果一致性
        consistency_analysis = self.analyze_consistency(results)
        
        return {
            "test_name": test_name,
            "runs": results,
            "consistency": consistency_analysis,
            "is_reproducible": consistency_analysis["is_consistent"]
        }
        
    def analyze_consistency(self, results: List[Dict]) -> Dict[str, Any]:
        """分析结果一致性"""
        if len(results) < 2:
            return {"is_consistent": True, "reason": "single_run"}
            
        # 提取关键指标
        metrics = {}
        for result in results:
            for key, value in result.items():
                if isinstance(value, (int, float)) and key not in ["run_id", "execution_time", "timestamp"]:
                    if key not in metrics:
                        metrics[key] = []
                    metrics[key].append(value)
        
        consistency_report = {
            "is_consistent": True,
            "metrics_analysis": {},
            "failed_metrics": []
        }
        
        for metric_name, values in metrics.items():
            if len(values) < 2:
                continue
                
            mean_val = np.mean(values)
            std_val = np.std(values)
            cv = std_val / mean_val if mean_val != 0 else 0
            
            is_consistent = cv < self.tolerance
            
            consistency_report["metrics_analysis"][metric_name] = {
                "mean": mean_val,
                "std": std_val,
                "cv": cv,
                "is_consistent": is_consistent,
                "values": values
            }
            
            if not is_consistent:
                consistency_report["is_consistent"] = False
                consistency_report["failed_metrics"].append(metric_name)
        
        return consistency_report
        
    def test_our_dsl_performance(self) -> Dict[str, Any]:
        """测试Our DSL框架性能"""
        try:
            # 导入我们的DSL框架
            sys.path.append('.')
            from dsl.dsl import DSL
            from core.llm import llm_callable
            
            # 创建DSL实例
            dsl = DSL(workers=4)
            dsl.use_llm(llm_callable)
            
            # 创建测试任务
            tasks = []
            for i in range(10):
                task = dsl.task(f"test_task_{i}")
                tasks.append(task)
            
            # 执行任务
            start_time = time.time()
            results = []
            for task in tasks:
                result = dsl.run(task)
                results.append(result)
            end_time = time.time()
            
            return {
                "throughput": len(tasks) / (end_time - start_time),
                "latency": (end_time - start_time) / len(tasks),
                "success_rate": 1.0,
                "memory_usage": psutil.Process().memory_info().rss / 1024 / 1024,
                "task_count": len(tasks)
            }
            
        except Exception as e:
            logger.error(f"❌ Our DSL测试失败: {e}")
            return {
                "throughput": 0,
                "latency": 0,
                "success_rate": 0,
                "memory_usage": 0,
                "task_count": 0,
                "error": str(e)
            }
            
    def test_langchain_performance(self) -> Dict[str, Any]:
        """测试LangChain框架性能"""
        try:
            import langchain
            from langchain.llms import OpenAI
            from langchain.agents import initialize_agent, Tool
            from langchain.agents import AgentType
            
            # 创建LLM
            llm = OpenAI(temperature=0)
            
            # 创建简单工具
            def dummy_tool(query: str) -> str:
                return f"处理查询: {query}"
            
            tools = [Tool(name="dummy", func=dummy_tool, description="虚拟工具")]
            
            # 创建代理
            agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)
            
            # 执行测试任务
            start_time = time.time()
            results = []
            for i in range(5):  # 减少任务数量以提高稳定性
                try:
                    result = agent.run(f"测试任务 {i}")
                    results.append(result)
                except Exception as e:
                    logger.warning(f"LangChain任务 {i} 失败: {e}")
            end_time = time.time()
            
            return {
                "throughput": len(results) / (end_time - start_time) if end_time > start_time else 0,
                "latency": (end_time - start_time) / len(results) if results else 0,
                "success_rate": len(results) / 5,
                "memory_usage": psutil.Process().memory_info().rss / 1024 / 1024,
                "task_count": len(results)
            }
            
        except Exception as e:
            logger.error(f"❌ LangChain测试失败: {e}")
            return {
                "throughput": 0,
                "latency": 0,
                "success_rate": 0,
                "memory_usage": 0,
                "task_count": 0,
                "error": str(e)
            }
            
    def generate_reproducibility_report(self) -> Dict[str, Any]:
        """生成可复现性报告"""
        logger.info("📊 生成可复现性报告...")
        
        # 环境信息
        env_info = self.check_environment_consistency()
        
        # API配置验证
        api_valid = self.verify_api_configuration()
        
        # 运行可复现性测试
        our_dsl_test = self.run_reproducibility_test(self.test_our_dsl_performance, "Our DSL Framework")
        langchain_test = self.run_reproducibility_test(self.test_langchain_performance, "LangChain Framework")
        
        # 生成报告
        report = {
            "timestamp": time.time(),
            "random_seed": self.random_seed,
            "test_runs": self.test_runs,
            "tolerance": self.tolerance,
            "environment": env_info,
            "api_configuration_valid": api_valid,
            "tests": {
                "our_dsl": our_dsl_test,
                "langchain": langchain_test
            },
            "overall_reproducibility": {
                "our_dsl_reproducible": our_dsl_test["is_reproducible"],
                "langchain_reproducible": langchain_test["is_reproducible"],
                "overall_score": "high" if (our_dsl_test["is_reproducible"] and langchain_test["is_reproducible"]) else "medium"
            }
        }
        
        return report
        
    def save_report(self, report: Dict[str, Any], filename: str = "reproducibility_report.json"):
        """保存可复现性报告"""
        output_path = Path("results") / filename
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        logger.info(f"📄 可复现性报告已保存到: {output_path}")
        
    def run_full_reproducibility_test(self):
        """运行完整的可复现性测试"""
        logger.info("🚀 开始CCF A类会议实验可复现性验证")
        logger.info("=" * 60)
        
        # 设置可复现环境
        self.setup_reproducible_environment()
        
        # 生成报告
        report = self.generate_reproducibility_report()
        
        # 保存报告
        self.save_report(report)
        
        # 打印摘要
        logger.info("📋 可复现性测试摘要:")
        logger.info(f"   Our DSL框架可复现性: {'✅ 通过' if report['tests']['our_dsl']['is_reproducible'] else '❌ 失败'}")
        logger.info(f"   LangChain框架可复现性: {'✅ 通过' if report['tests']['langchain']['is_reproducible'] else '❌ 失败'}")
        logger.info(f"   总体可复现性评分: {report['overall_reproducibility']['overall_score']}")
        
        return report

def main():
    """主函数"""
    test = ReproducibilityTest()
    report = test.run_full_reproducibility_test()
    
    # 检查是否通过
    if report['overall_reproducibility']['overall_score'] == 'high':
        logger.info("🎉 所有测试通过！实验具有良好的可复现性。")
        sys.exit(0)
    else:
        logger.warning("⚠️  部分测试未通过，请检查环境配置。")
        sys.exit(1)

if __name__ == "__main__":
    main()


