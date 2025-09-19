#!/usr/bin/env python3
"""
可扩展性实验框架 - 完全真实的API调用实验
Scalability Study Framework - Fully Real API Call Experiments

测试不同框架在不同规模下的性能表现：
1. 代理数量扩展性 (1-20个代理)
2. 任务复杂度扩展性
3. 并发任务扩展性
4. 内存使用扩展性
5. 延迟扩展性
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
import concurrent.futures
import threading

# 添加项目根目录到Python路径
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ScalabilityStudy:
    """可扩展性实验类"""
    
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
        
        # 可扩展性实验配置
        self.scalability_config = {
            "frameworks": ["Our DSL", "LangChain", "CrewAI", "AutoGen"],
            "agent_scales": [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 18, 20],  # 更多代理数量
            "task_scales": [1, 2, 3, 5, 8, 10, 15, 20],  # 任务数量
            "complexity_levels": ["simple", "medium", "complex"],
            "concurrent_levels": [1, 2, 3, 4, 5],  # 并发级别
            "repetitions": 3
        }
        
        # 测试任务
        self.tasks = self._generate_scalability_tasks()
        
        logger.info(f"可扩展性实验初始化完成 - 框架数: {len(self.scalability_config['frameworks'])}, "
                   f"代理规模: {len(self.scalability_config['agent_scales'])}, "
                   f"任务规模: {len(self.scalability_config['task_scales'])}")
    
    def load_env(self):
        """加载环境变量"""
        os.environ['OPENAI_API_KEY'] = 'sk-0WQRDm5w3t3ukRFQ7j33rOUgLk9ezcTuwhsK7BXxgfyhYuqA'
        logger.info("设置OPENAI_API_KEY环境变量")
    
    def _generate_scalability_tasks(self) -> Dict[str, List[str]]:
        """生成可扩展性测试任务"""
        tasks = {
            "simple": [
                "分析一家小型咖啡店的月度销售数据，识别销售趋势并提供改进建议。",
                "评估一个在线教育平台的用户增长策略，提出优化方案。",
                "设计一个简单的RESTful API架构，包括认证、授权和数据验证机制。",
                "为移动应用设计用户认证和会话管理系统。",
                "分析气候变化对农业产量的影响，基于历史数据建立预测模型。",
                "研究社交媒体对青少年心理健康的影响，设计实验方案。",
                "优化一个Web应用的数据库查询性能，减少响应时间。",
                "优化一个移动应用的电池使用效率。",
                "评估一个创业项目的市场风险和财务风险。",
                "评估一个IT项目的技术风险和进度风险。",
                "制定一个初创公司的3年发展战略规划。",
                "制定一个传统企业的数字化转型战略。",
                "分析电商平台的用户行为数据，识别购买模式和用户偏好。",
                "分析股票市场的价格波动，建立简单的预测模型。",
                "创作一个关于人工智能与人类合作的短篇科幻故事。",
                "编写一个关于环保主题的儿童教育剧本。",
                "设计一个简单的RESTful API架构，包括认证、授权和数据验证机制。",
                "为移动应用设计用户认证和会话管理系统。",
                "分析气候变化对农业产量的影响，基于历史数据建立预测模型。",
                "研究社交媒体对青少年心理健康的影响，设计实验方案。"
            ],
            "medium": [
                "为一家中型制造企业设计数字化转型路线图，包括技术选型、实施计划和风险评估。",
                "分析电商平台的供应链管理问题，设计优化方案以提高效率和降低成本。",
                "设计一个微服务架构的电商平台，包括用户服务、商品服务、订单服务和支付服务，考虑服务间通信、数据一致性和容错机制。",
                "设计一个分布式缓存系统，支持高并发读写、数据一致性和故障恢复。",
                "设计一个基于机器学习的药物发现平台，包括分子筛选、活性预测和毒性评估，考虑数据质量和模型可解释性。",
                "研究量子计算在密码学中的应用，分析量子算法对现有加密系统的影响并提出后量子密码学方案。",
                "优化一个分布式系统的资源利用率，包括CPU、内存、网络和存储，实现动态负载均衡和资源调度。",
                "优化一个机器学习训练管道的效率，包括数据预处理、模型训练和超参数调优。",
                "评估一个跨国企业的运营风险，包括政治风险、汇率风险、供应链风险和合规风险。",
                "评估一个金融科技公司的系统性风险，包括技术风险、市场风险、操作风险和监管风险。",
                "制定一个中型企业的国际化扩张战略，包括市场选择、进入模式、资源配置和风险管控。",
                "制定一个科技公司的产品创新战略，包括技术路线图、市场定位、竞争策略和商业模式。",
                "分析城市交通数据，设计智能交通管理系统以减少拥堵和提高效率。",
                "分析医疗数据，建立疾病预测模型并评估其临床价值。",
                "创作一个多线程的悬疑小说大纲，包含多个视角和复杂的人物关系。",
                "编写一个关于未来城市生活的互动式数字叙事作品。",
                "设计一个微服务架构的电商平台，包括用户服务、商品服务、订单服务和支付服务，考虑服务间通信、数据一致性和容错机制。",
                "设计一个分布式缓存系统，支持高并发读写、数据一致性和故障恢复。",
                "设计一个基于机器学习的药物发现平台，包括分子筛选、活性预测和毒性评估，考虑数据质量和模型可解释性。",
                "研究量子计算在密码学中的应用，分析量子算法对现有加密系统的影响并提出后量子密码学方案。"
            ],
            "complex": [
                "设计一个多国企业的全球供应链风险管理框架，考虑地缘政治、自然灾害、市场波动等因素，并提供实时监控和应急响应机制。",
                "为一家大型金融机构设计基于AI的智能投顾系统架构，包括客户画像、风险评估、投资组合优化和合规管理。",
                "设计一个支持千万级用户的实时推荐系统架构，包括数据收集、特征工程、模型训练、在线推理和A/B测试框架，考虑延迟、准确性和可扩展性。",
                "设计一个多云环境下的容器编排平台，支持自动扩缩容、服务发现、负载均衡、监控告警和灾难恢复。",
                "设计一个多模态AI系统用于癌症早期诊断，整合影像学、基因组学、蛋白质组学和临床数据，建立端到端的诊断和预后预测模型。",
                "研究可控核聚变反应堆的等离子体控制算法，设计实时控制系统以维持等离子体稳定性和优化能量输出。",
                "优化一个超大规模云计算平台的整体性能，包括计算、存储、网络、安全和成本优化，实现多租户隔离和弹性扩缩容。",
                "优化一个自动驾驶系统的实时性能，包括感知、决策、控制和通信，确保安全性和效率的平衡。",
                "评估一个全球供应链网络的综合风险，包括地缘政治、自然灾害、网络安全、气候变化和宏观经济波动等多维度风险，建立动态风险评估和缓解体系。",
                "评估一个智能城市系统的网络安全风险，包括关键基础设施保护、数据隐私、AI系统安全和应急响应能力。",
                "制定一个大型集团的多元化发展战略，包括产业布局、资源配置、组织变革、文化融合和可持续发展，建立动态战略调整机制。",
                "制定一个国家的数字经济发展战略，包括基础设施建设、产业升级、人才培养、政策法规和国际合作，构建完整的数字经济生态系统。",
                "分析大规模多源异构数据（包括文本、图像、传感器数据），建立综合性的城市智慧管理系统，实现实时决策和预测性维护。",
                "分析金融市场的多维度数据，建立高频交易策略和风险管理系统，考虑市场微观结构、流动性风险和监管合规。",
                "创作一个跨媒体的科幻史诗，包括小说、游戏、影视和虚拟现实体验，构建完整的世界观和角色体系。",
                "编写一个基于历史事件的沉浸式戏剧作品，融合传统戏剧、现代技术和观众参与元素。",
                "设计一个支持千万级用户的实时推荐系统架构，包括数据收集、特征工程、模型训练、在线推理和A/B测试框架，考虑延迟、准确性和可扩展性。",
                "设计一个多云环境下的容器编排平台，支持自动扩缩容、服务发现、负载均衡、监控告警和灾难恢复。",
                "设计一个多模态AI系统用于癌症早期诊断，整合影像学、基因组学、蛋白质组学和临床数据，建立端到端的诊断和预后预测模型。",
                "研究可控核聚变反应堆的等离子体控制算法，设计实时控制系统以维持等离子体稳定性和优化能量输出。"
            ]
        }
        
        return tasks
    
    @contextmanager
    def memory_tracking(self, framework: str, scale_type: str, scale_value: int, complexity: str):
        """内存跟踪上下文管理器"""
        class MemoryTracker:
            def __init__(self, parent, framework, scale_type, scale_value, complexity):
                self.parent = parent
                self.framework = framework
                self.scale_type = scale_type
                self.scale_value = scale_value
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
                
                key = f"{self.framework}_{self.scale_type}_{self.scale_value}_{self.complexity}"
                self.parent.memory_tracker[key] = memory_usage
                logger.info(f"内存使用记录: {key} = {memory_usage:.2f} MB")
        
        tracker = MemoryTracker(self, framework, scale_type, scale_value, complexity)
        try:
            yield tracker
        finally:
            pass
    
    def test_framework_scalability(self, framework: str, scale_type: str, scale_value: int, 
                                 complexity: str, task_count: int) -> Dict[str, Any]:
        """测试框架可扩展性"""
        try:
            tasks = self.tasks[complexity][:task_count]
            
            with self.memory_tracking(framework, scale_type, scale_value, complexity):
                start_time = time.time()
                
                if framework == "Our DSL":
                    result = self._test_our_dsl_scalability(tasks, scale_value)
                elif framework == "LangChain":
                    result = self._test_langchain_scalability(tasks, scale_value)
                elif framework == "CrewAI":
                    result = self._test_crewai_scalability(tasks, scale_value)
                elif framework == "AutoGen":
                    result = self._test_autogen_scalability(tasks, scale_value)
                
                execution_time = time.time() - start_time
                throughput = result["successful_tasks"] / execution_time if execution_time > 0 else 0
                avg_latency = execution_time / result["successful_tasks"] if result["successful_tasks"] > 0 else 0
                success_rate = (result["successful_tasks"] / len(tasks)) * 100
                
            # 在with语句结束后获取内存使用
            memory_usage = self.memory_tracker.get(f"{framework}_{scale_type}_{scale_value}_{complexity}", 0)
            
            return {
                "framework": framework,
                "scale_type": scale_type,
                "scale_value": scale_value,
                "complexity": complexity,
                "task_count": task_count,
                "execution_time": execution_time,
                "throughput": throughput,
                "success_rate": success_rate,
                "successful_tasks": result["successful_tasks"],
                "total_tasks": len(tasks),
                "avg_latency": avg_latency * 1000,  # 转换为ms
                "status": "success",
                "memory_usage": memory_usage,
                "api_type": "real_api"
            }
                
        except Exception as e:
            logger.error(f"框架可扩展性测试失败 ({framework}): {e}")
            return {
                "framework": framework,
                "scale_type": scale_type,
                "scale_value": scale_value,
                "complexity": complexity,
                "task_count": task_count,
                "execution_time": 0,
                "throughput": 0,
                "success_rate": 0,
                "successful_tasks": 0,
                "total_tasks": len(self.tasks[complexity][:task_count]),
                "avg_latency": 0,
                "status": "error",
                "memory_usage": 0,
                "error": str(e),
                "api_type": "error"
            }
    
    def _test_our_dsl_scalability(self, tasks: List[str], agent_count: int) -> Dict[str, int]:
        """测试Our DSL可扩展性"""
        from dsl.dsl import DSL
        from core.robust_llm import llm_callable
        
        # 创建DSL实例
        dsl = DSL(seed=self.random_seed, workers=min(agent_count, 8))
        
        # 添加任务
        task_objects = []
        for i, task_prompt in enumerate(tasks):
            task_obj = dsl.gen(f"task_{i}", prompt=task_prompt, agent=f"agent_{i % agent_count}").schedule()
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
        
        return {"successful_tasks": successful_tasks}
    
    def _test_langchain_scalability(self, tasks: List[str], agent_count: int) -> Dict[str, int]:
        """测试LangChain可扩展性"""
        from langchain_openai import ChatOpenAI
        from langchain.schema import HumanMessage
        
        # 创建LangChain客户端
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=0.3,
            max_tokens=1000
        )
        
        # 执行任务
        successful_tasks = 0
        for i, task_prompt in enumerate(tasks):
            try:
                message = HumanMessage(content=task_prompt)
                response = llm.invoke([message])
                if response and response.content and len(response.content.strip()) > 100:
                    successful_tasks += 1
            except Exception as e:
                logger.warning(f"LangChain任务{i}失败: {e}")
        
        return {"successful_tasks": successful_tasks}
    
    def _test_crewai_scalability(self, tasks: List[str], agent_count: int) -> Dict[str, int]:
        """测试CrewAI可扩展性"""
        from crewai import Agent, Task, Crew, Process
        from crewai.llm import LLM
        
        # 创建CrewAI LLM
        llm = LLM(
            model="gpt-4o-mini",
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=0.3,
            max_tokens=1000
        )
        
        # 创建代理
        agents = []
        for i in range(min(agent_count, 3)):  # CrewAI限制代理数量
            agent = Agent(
                role=f"Specialist_{i}",
                goal=f"Complete tasks efficiently and accurately",
                backstory="You are an expert with deep domain knowledge and analytical skills.",
                llm=llm,
                verbose=False,
                allow_delegation=False
            )
            agents.append(agent)
        
        # 创建任务
        crew_tasks = []
        for i, task_prompt in enumerate(tasks):
            task = Task(
                description=task_prompt,
                agent=agents[i % len(agents)],
                expected_output="A detailed and comprehensive response with actionable insights",
                async_execution=False
            )
            crew_tasks.append(task)
        
        # 创建Crew并执行
        crew = Crew(
            agents=agents,
            tasks=crew_tasks,
            verbose=False,
            process=Process.sequential
        )
        
        result = crew.kickoff()
        
        # 计算成功任务数
        successful_tasks = 0
        if result:
            result_str = str(result).strip()
            if len(result_str) > 100:
                # 检查是否包含多个任务的响应
                task_responses = result_str.split('\n\n')
                successful_tasks = min(len(task_responses), len(tasks))
            else:
                successful_tasks = 1 if len(result_str) > 100 else 0
        
        return {"successful_tasks": successful_tasks}
    
    def _test_autogen_scalability(self, tasks: List[str], agent_count: int) -> Dict[str, int]:
        """测试AutoGen可扩展性"""
        from autogen import ConversableAgent, GroupChat, GroupChatManager
        
        # 配置LLM
        llm_config = {
            "model": "gpt-4o-mini",
            "api_key": self.api_key,
            "base_url": self.base_url,
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        # 创建代理
        agents = []
        for i in range(max(agent_count, 2)):  # AutoGen需要至少2个代理
            agent = ConversableAgent(
                name=f"agent_{i}",
                llm_config=llm_config,
                system_message="You are an expert with specialized knowledge and analytical capabilities."
            )
            agents.append(agent)
        
        # 创建群聊
        group_chat = GroupChat(
            agents=agents,
            messages=[],
            max_round=5,
            speaker_selection_method='round_robin'
        )
        
        manager = GroupChatManager(
            groupchat=group_chat,
            llm_config=llm_config
        )
        
        # 执行任务
        successful_tasks = 0
        for i, task_prompt in enumerate(tasks):
            try:
                result = agents[0].initiate_chat(
                    manager,
                    message=task_prompt,
                    max_turns=3
                )
                if result and len(str(result).strip()) > 100:
                    successful_tasks += 1
            except Exception as e:
                logger.warning(f"AutoGen任务{i}失败: {e}")
        
        return {"successful_tasks": successful_tasks}
    
    def run_scalability_study(self) -> Dict[str, Any]:
        """运行可扩展性实验"""
        logger.info("📈 开始可扩展性实验...")
        logger.info(f"实验配置: {len(self.scalability_config['frameworks'])}个框架, "
                   f"代理规模: {len(self.scalability_config['agent_scales'])}, "
                   f"任务规模: {len(self.scalability_config['task_scales'])}")
        
        scalability_results = []
        total_tests = (len(self.scalability_config['frameworks']) * 
                      len(self.scalability_config['agent_scales']) * 
                      len(self.scalability_config['task_scales']) * 
                      len(self.scalability_config['complexity_levels']) * 
                      self.scalability_config['repetitions'])
        
        current_test = 0
        
        for framework in self.scalability_config['frameworks']:
            for agent_scale in self.scalability_config['agent_scales']:
                for task_scale in self.scalability_config['task_scales']:
                    for complexity in self.scalability_config['complexity_levels']:
                        for repetition in range(self.scalability_config['repetitions']):
                            current_test += 1
                            logger.info(f"📊 测试进度: {current_test}/{total_tests} - "
                                       f"{framework} - {agent_scale} agents - {task_scale} tasks - {complexity}")
                            
                            # 运行测试
                            result = self.test_framework_scalability(
                                framework, "agent_scale", agent_scale, complexity, task_scale
                            )
                            
                            # 添加重复次数信息
                            result["repetition"] = repetition + 1
                            scalability_results.append(result)
                            
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
        results_file = "scalability_study_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                "scalability_results": scalability_results,
                "memory_tracker": self.memory_tracker,
                "timestamp": datetime.now().isoformat(),
                "scalability_config": self.scalability_config,
                "test_info": {
                    "total_tests": len(scalability_results),
                    "frameworks": self.scalability_config['frameworks'],
                    "agent_scales": self.scalability_config['agent_scales'],
                    "task_scales": self.scalability_config['task_scales'],
                    "complexity_levels": self.scalability_config['complexity_levels'],
                    "repetitions": self.scalability_config['repetitions'],
                    "random_seed": self.random_seed
                }
            }, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ 可扩展性实验完成！结果已保存到: {results_file}")
        
        # 生成可扩展性分析
        self._generate_scalability_analysis(scalability_results)
        
        return {
            "scalability_results": scalability_results,
            "memory_tracker": self.memory_tracker,
            "timestamp": datetime.now().isoformat(),
            "scalability_config": self.scalability_config
        }
    
    def _generate_scalability_analysis(self, scalability_results: List[Dict[str, Any]]):
        """生成可扩展性分析"""
        logger.info("\n📊 可扩展性分析:")
        logger.info("=" * 60)
        
        # 按框架分组统计
        framework_stats = {}
        for result in scalability_results:
            if result["status"] == "success":
                framework = result["framework"]
                scale_value = result["scale_value"]
                
                if framework not in framework_stats:
                    framework_stats[framework] = {}
                
                if scale_value not in framework_stats[framework]:
                    framework_stats[framework][scale_value] = {
                        "throughput": [],
                        "latency": [],
                        "memory": [],
                        "success_rate": []
                    }
                
                framework_stats[framework][scale_value]["throughput"].append(result["throughput"])
                framework_stats[framework][scale_value]["latency"].append(result["avg_latency"])
                framework_stats[framework][scale_value]["memory"].append(result["memory_usage"])
                framework_stats[framework][scale_value]["success_rate"].append(result["success_rate"])
        
        # 输出可扩展性分析
        for framework, scales in framework_stats.items():
            logger.info(f"\n{framework} 可扩展性分析:")
            logger.info("-" * 40)
            
            # 计算不同规模下的平均性能
            scale_performance = []
            for scale_value in sorted(scales.keys()):
                stats = scales[scale_value]
                if stats["throughput"]:
                    avg_throughput = np.mean(stats["throughput"])
                    avg_latency = np.mean(stats["latency"])
                    avg_memory = np.mean(stats["memory"])
                    avg_success_rate = np.mean(stats["success_rate"])
                    
                    scale_performance.append({
                        "scale": scale_value,
                        "throughput": avg_throughput,
                        "latency": avg_latency,
                        "memory": avg_memory,
                        "success_rate": avg_success_rate
                    })
                    
                    logger.info(f"  {scale_value}个代理: 吞吐量={avg_throughput:.3f} tasks/sec, "
                               f"延迟={avg_latency:.2f} ms, 内存={avg_memory:.2f} MB")
            
            # 分析可扩展性趋势
            if len(scale_performance) >= 3:
                # 计算吞吐量扩展性
                throughputs = [p["throughput"] for p in scale_performance]
                latency_increase = (latencies[-1] - latencies[0]) / latencies[0] * 100 if len(latencies) > 1 else 0
                memory_increase = (memories[-1] - memories[0]) / memories[0] * 100 if len(memories) > 1 else 0
                
                logger.info(f"\n  可扩展性指标:")
                logger.info(f"    吞吐量变化: {throughput_change:+.1f}%")
                logger.info(f"    延迟增加: {latency_increase:+.1f}%")
                logger.info(f"    内存增加: {memory_increase:+.1f}%")
                
                # 判断可扩展性等级
                if throughput_change > 50 and latency_increase < 100:
                    scalability_grade = "优秀"
                elif throughput_change > 20 and latency_increase < 200:
                    scalability_grade = "良好"
                elif throughput_change > 0 and latency_increase < 300:
                    scalability_grade = "一般"
                else:
                    scalability_grade = "较差"
                
                logger.info(f"    可扩展性等级: {scalability_grade}")
        
        # 总体统计
        total_tests = len(scalability_results)
        successful_tests = sum(1 for r in scalability_results if r["status"] == "success")
        overall_success_rate = (successful_tests / total_tests) * 100
        
        logger.info(f"\n📈 总体统计:")
        logger.info(f"  成功测试: {successful_tests}")
        logger.info(f"  失败测试: {total_tests - successful_tests}")
        logger.info(f"  成功率: {overall_success_rate:.1f}%")

def main():
    """主函数"""
    print("📈 可扩展性实验框架")
    print("=" * 50)
    print("⚠️  注意：此实验使用真实API调用，需要有效的API密钥")
    print("⚠️  实验规模较大，预计需要较长时间完成")
    print("=" * 50)
    
    # 创建可扩展性实验实例
    scalability = ScalabilityStudy()
    
    # 运行可扩展性实验
    results = scalability.run_scalability_study()
    
    print("\n🎉 可扩展性实验完成！")
    print(f"总测试数: {len(results['scalability_results'])}")
    print("结果已保存到 scalability_study_results.json")

if __name__ == "__main__":
    main()
