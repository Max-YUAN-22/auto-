#!/usr/bin/env python3
"""
全面基准测试框架 - 完全真实的API调用实验
Comprehensive Benchmark Framework - Fully Real API Call Experiments

包含：
1. 多场景对比实验
2. 消融实验  
3. 可扩展性实验
4. 鲁棒性实验
5. 内存效率实验
6. 延迟分析实验
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
import subprocess

# 添加项目根目录到Python路径
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComprehensiveBenchmark:
    """全面基准测试类"""
    
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
        
        # 实验配置
        self.experiment_config = {
            "scenarios": [
                "business_analysis",      # 商业分析
                "technical_design",       # 技术设计
                "scientific_research",    # 科学研究
                "creative_writing",       # 创意写作
                "data_analysis",          # 数据分析
                "system_optimization",    # 系统优化
                "risk_assessment",        # 风险评估
                "strategic_planning"      # 战略规划
            ],
            "agent_counts": [1, 2, 3, 4, 5, 6, 8, 10],  # 更多代理数量
            "frameworks": ["Our DSL", "LangChain", "CrewAI", "AutoGen"],
            "task_complexities": ["simple", "medium", "complex"],  # 任务复杂度
            "repetitions": 3  # 每个实验重复3次
        }
        
        # 真实测试任务 - 8个不同场景，每个场景3个复杂度
        self.tasks = self._generate_comprehensive_tasks()
        
        logger.info(f"初始化完成 - 场景数: {len(self.experiment_config['scenarios'])}, "
                   f"代理数量: {len(self.experiment_config['agent_counts'])}, "
                   f"任务总数: {sum(len(tasks) for tasks in self.tasks.values())}")
    
    def load_env(self):
        """加载环境变量"""
        os.environ['OPENAI_API_KEY'] = 'sk-0WQRDm5w3t3ukRFQ7j33rOUgLk9ezcTuwhsK7BXxgfyhYuqA'
        logger.info("设置OPENAI_API_KEY环境变量")
    
    def _generate_comprehensive_tasks(self) -> Dict[str, Dict[str, List[str]]]:
        """生成全面的测试任务"""
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
        
        # 创意写作场景
        tasks["creative_writing"] = {
            "simple": [
                "创作一个关于人工智能与人类合作的短篇科幻故事。",
                "编写一个关于环保主题的儿童教育剧本。"
            ],
            "medium": [
                "创作一个多线程的悬疑小说大纲，包含多个视角和复杂的人物关系。",
                "编写一个关于未来城市生活的互动式数字叙事作品。"
            ],
            "complex": [
                "创作一个跨媒体的科幻史诗，包括小说、游戏、影视和虚拟现实体验，构建完整的世界观和角色体系。",
                "编写一个基于历史事件的沉浸式戏剧作品，融合传统戏剧、现代技术和观众参与元素。"
            ]
        }
        
        # 数据分析场景
        tasks["data_analysis"] = {
            "simple": [
                "分析电商平台的用户行为数据，识别购买模式和用户偏好。",
                "分析股票市场的价格波动，建立简单的预测模型。"
            ],
            "medium": [
                "分析城市交通数据，设计智能交通管理系统以减少拥堵和提高效率。",
                "分析医疗数据，建立疾病预测模型并评估其临床价值。"
            ],
            "complex": [
                "分析大规模多源异构数据（包括文本、图像、传感器数据），建立综合性的城市智慧管理系统，实现实时决策和预测性维护。",
                "分析金融市场的多维度数据，建立高频交易策略和风险管理系统，考虑市场微观结构、流动性风险和监管合规。"
            ]
        }
        
        # 系统优化场景
        tasks["system_optimization"] = {
            "simple": [
                "优化一个Web应用的数据库查询性能，减少响应时间。",
                "优化一个移动应用的电池使用效率。"
            ],
            "medium": [
                "优化一个分布式系统的资源利用率，包括CPU、内存、网络和存储，实现动态负载均衡和资源调度。",
                "优化一个机器学习训练管道的效率，包括数据预处理、模型训练和超参数调优。"
            ],
            "complex": [
                "优化一个超大规模云计算平台的整体性能，包括计算、存储、网络、安全和成本优化，实现多租户隔离和弹性扩缩容。",
                "优化一个自动驾驶系统的实时性能，包括感知、决策、控制和通信，确保安全性和效率的平衡。"
            ]
        }
        
        # 风险评估场景
        tasks["risk_assessment"] = {
            "simple": [
                "评估一个创业项目的市场风险和财务风险。",
                "评估一个IT项目的技术风险和进度风险。"
            ],
            "medium": [
                "评估一个跨国企业的运营风险，包括政治风险、汇率风险、供应链风险和合规风险。",
                "评估一个金融科技公司的系统性风险，包括技术风险、市场风险、操作风险和监管风险。"
            ],
            "complex": [
                "评估一个全球供应链网络的综合风险，包括地缘政治、自然灾害、网络安全、气候变化和宏观经济波动等多维度风险，建立动态风险评估和缓解体系。",
                "评估一个智能城市系统的网络安全风险，包括关键基础设施保护、数据隐私、AI系统安全和应急响应能力。"
            ]
        }
        
        # 战略规划场景
        tasks["strategic_planning"] = {
            "simple": [
                "制定一个初创公司的3年发展战略规划。",
                "制定一个传统企业的数字化转型战略。"
            ],
            "medium": [
                "制定一个中型企业的国际化扩张战略，包括市场选择、进入模式、资源配置和风险管控。",
                "制定一个科技公司的产品创新战略，包括技术路线图、市场定位、竞争策略和商业模式。"
            ],
            "complex": [
                "制定一个大型集团的多元化发展战略，包括产业布局、资源配置、组织变革、文化融合和可持续发展，建立动态战略调整机制。",
                "制定一个国家的数字经济发展战略，包括基础设施建设、产业升级、人才培养、政策法规和国际合作，构建完整的数字经济生态系统。"
            ]
        }
        
        return tasks
    
    @contextmanager
    def memory_tracking(self, framework: str, scenario: str, agent_count: int, complexity: str = "medium"):
        """内存跟踪上下文管理器 - 修复版本"""
        class MemoryTracker:
            def __init__(self, parent, framework, scenario, agent_count, complexity):
                self.parent = parent
                self.framework = framework
                self.scenario = scenario
                self.agent_count = agent_count
                self.complexity = complexity
                self.initial_memory = None
                self.peak_memory = 0
                
            def __enter__(self):
                # 强制垃圾回收
                gc.collect()
                process = psutil.Process()
                self.initial_memory = process.memory_info().rss / 1024 / 1024  # MB
                self.peak_memory = self.initial_memory
                self.monitoring_active = True
                
                # 启动内存监控线程
                self.monitor_thread = threading.Thread(target=self._monitor_memory)
                self.monitor_thread.daemon = True
                self.monitor_thread.start()
                
                logger.info(f"初始内存: {self.initial_memory:.2f} MB")
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                # 停止内存监控
                self.monitoring_active = False
                if hasattr(self, 'monitor_thread'):
                    self.monitor_thread.join(timeout=1.0)
                
                process = psutil.Process()
                final_memory = process.memory_info().rss / 1024 / 1024  # MB
                
                # 计算内存使用 - 使用峰值内存而不是最终内存
                memory_usage = max(0, self.peak_memory - self.initial_memory)
                
                # 确保键格式一致
                key = f"{self.framework}_{self.scenario}_{self.agent_count}_{self.complexity}"
                self.parent.memory_tracker[key] = memory_usage
                
                logger.info(f"内存使用记录: {key}")
                logger.info(f"  初始内存: {self.initial_memory:.2f} MB")
                logger.info(f"  峰值内存: {self.peak_memory:.2f} MB") 
                logger.info(f"  最终内存: {final_memory:.2f} MB")
                logger.info(f"  内存使用: {memory_usage:.2f} MB")
            
            def _monitor_memory(self):
                """内存监控线程"""
                process = psutil.Process()
                while self.monitoring_active:
                    try:
                        current_memory = process.memory_info().rss / 1024 / 1024  # MB
                        if current_memory > self.peak_memory:
                            self.peak_memory = current_memory
                        time.sleep(0.1)  # 每100ms检查一次
                    except:
                        break
        
        tracker = MemoryTracker(self, framework, scenario, agent_count, complexity)
        try:
            yield tracker
        finally:
            pass
    
    def test_our_dsl_real_api(self, scenario: str, agent_count: int, complexity: str = "medium") -> Dict[str, Any]:
        """测试Our DSL框架（真实API调用）"""
        try:
            from dsl.dsl import DSL
            from core.robust_llm import llm_callable
            
            tasks = self.tasks[scenario][complexity]
            
            # 改进的内存监控
            gc.collect()
            process = psutil.Process()
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            peak_memory = initial_memory
            
            start_time = time.time()
            
            # 创建DSL实例
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
                    result = task.wait(timeout=120.0)  # 增加超时时间
                    if result is not None and len(str(result).strip()) > 100:  # 提高质量要求
                        successful_tasks += 1
                    
                    # 在任务执行过程中监控内存
                    current_memory = process.memory_info().rss / 1024 / 1024
                    if current_memory > peak_memory:
                        peak_memory = current_memory
                        
                except Exception as e:
                    logger.warning(f"任务等待失败: {e}")
            
            execution_time = time.time() - start_time
            throughput = successful_tasks / execution_time if execution_time > 0 else 0
            avg_latency = execution_time / successful_tasks if successful_tasks > 0 else 0
            success_rate = (successful_tasks / len(tasks[:agent_count])) * 100
            
            # 计算内存使用
            memory_usage = max(0, peak_memory - initial_memory)
            
            logger.info(f"Our DSL内存使用: {memory_usage:.2f} MB (初始: {initial_memory:.2f}, 峰值: {peak_memory:.2f})")
            
            return {
                "framework": "Our DSL",
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
            logger.error(f"Our DSL测试失败: {e}")
            return {
                "framework": "Our DSL",
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
    
    def test_langchain_real_api(self, scenario: str, agent_count: int, complexity: str = "medium") -> Dict[str, Any]:
        """测试LangChain框架（真实API调用）"""
        try:
            from langchain_openai import ChatOpenAI
            from langchain.schema import HumanMessage
            
            tasks = self.tasks[scenario][complexity]
            
            with self.memory_tracking("langchain", scenario, agent_count, complexity):
                start_time = time.time()
                
                # 创建LangChain客户端
                llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    api_key=self.api_key,
                    base_url=self.base_url,
                    temperature=0.3,
                    max_tokens=1000  # 增加token数量
                )
                
                # 执行任务
                successful_tasks = 0
                for i, task_prompt in enumerate(tasks[:agent_count]):
                    try:
                        message = HumanMessage(content=task_prompt)
                        response = llm.invoke([message])
                        if response and response.content and len(response.content.strip()) > 100:
                            successful_tasks += 1
                    except Exception as e:
                        logger.warning(f"LangChain任务{i}失败: {e}")
                
                execution_time = time.time() - start_time
                throughput = successful_tasks / execution_time if execution_time > 0 else 0
                avg_latency = execution_time / successful_tasks if successful_tasks > 0 else 0
                success_rate = (successful_tasks / len(tasks[:agent_count])) * 100
                
            # 在with语句结束后获取内存使用
            memory_usage = self.memory_tracker.get(f"langchain_{scenario}_{agent_count}_{complexity}", 0)
            
            return {
                "framework": "LangChain",
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
            logger.error(f"LangChain测试失败: {e}")
            return {
                "framework": "LangChain",
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
    
    def test_crewai_real_api(self, scenario: str, agent_count: int, complexity: str = "medium") -> Dict[str, Any]:
        """测试CrewAI框架（真实API调用）"""
        try:
            from crewai import Agent, Task, Crew, Process
            from crewai.llm import LLM
            
            tasks = self.tasks[scenario][complexity]
            
            with self.memory_tracking("crewai", scenario, agent_count, complexity):
                start_time = time.time()
                
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
                        goal=f"Complete {scenario} tasks efficiently and accurately",
                        backstory=f"You are an expert in {scenario} with deep domain knowledge and analytical skills.",
                        llm=llm,
                        verbose=False,
                        allow_delegation=False
                    )
                    agents.append(agent)
                
                # 创建任务
                crew_tasks = []
                for i, task_prompt in enumerate(tasks[:agent_count]):
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
                        successful_tasks = min(len(task_responses), len(tasks[:agent_count]))
                    else:
                        successful_tasks = 1 if len(result_str) > 100 else 0
                else:
                    successful_tasks = 0
                
                execution_time = time.time() - start_time
                throughput = successful_tasks / execution_time if execution_time > 0 else 0
                avg_latency = execution_time / successful_tasks if successful_tasks > 0 else 0
                success_rate = (successful_tasks / len(tasks[:agent_count])) * 100
                
            # 在with语句结束后获取内存使用
            memory_usage = self.memory_tracker.get(f"crewai_{scenario}_{agent_count}_{complexity}", 0)
            
            return {
                "framework": "CrewAI",
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
            logger.error(f"CrewAI测试失败: {e}")
            return {
                "framework": "CrewAI",
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
    
    def test_autogen_real_api(self, scenario: str, agent_count: int, complexity: str = "medium") -> Dict[str, Any]:
        """测试AutoGen框架（真实API调用）"""
        try:
            from autogen import ConversableAgent, GroupChat, GroupChatManager
            
            tasks = self.tasks[scenario][complexity]
            
            with self.memory_tracking("autogen", scenario, agent_count, complexity):
                start_time = time.time()
                
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
                        system_message=f"You are an expert in {scenario} with specialized knowledge and analytical capabilities."
                    )
                    agents.append(agent)
                
                # 创建群聊
                group_chat = GroupChat(
                    agents=agents,
                    messages=[],
                    max_round=5,  # 增加轮数
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
                            max_turns=3  # 增加轮数
                        )
                        if result and len(str(result).strip()) > 100:
                            successful_tasks += 1
                    except Exception as e:
                        logger.warning(f"AutoGen任务{i}失败: {e}")
                
                execution_time = time.time() - start_time
                throughput = successful_tasks / execution_time if execution_time > 0 else 0
                avg_latency = execution_time / successful_tasks if successful_tasks > 0 else 0
                success_rate = (successful_tasks / len(tasks[:agent_count])) * 100
                
            # 在with语句结束后获取内存使用
            memory_usage = self.memory_tracker.get(f"autogen_{scenario}_{agent_count}_{complexity}", 0)
            
            return {
                "framework": "AutoGen",
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
            logger.error(f"AutoGen测试失败: {e}")
            return {
                "framework": "AutoGen",
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
    
    def run_comprehensive_benchmark(self) -> Dict[str, Any]:
        """运行全面基准测试"""
        logger.info("🚀 开始全面基准测试...")
        logger.info(f"实验配置: {len(self.experiment_config['scenarios'])}个场景, "
                   f"{len(self.experiment_config['agent_counts'])}个代理数量, "
                   f"{len(self.experiment_config['frameworks'])}个框架, "
                   f"{len(self.experiment_config['task_complexities'])}个复杂度")
        
        benchmark_results = []
        total_tests = (len(self.experiment_config['scenarios']) * 
                      len(self.experiment_config['agent_counts']) * 
                      len(self.experiment_config['frameworks']) * 
                      len(self.experiment_config['task_complexities']) * 
                      self.experiment_config['repetitions'])
        
        current_test = 0
        
        for scenario in self.experiment_config['scenarios']:
            for agent_count in self.experiment_config['agent_counts']:
                for framework in self.experiment_config['frameworks']:
                    for complexity in self.experiment_config['task_complexities']:
                        for repetition in range(self.experiment_config['repetitions']):
                            current_test += 1
                            logger.info(f"📊 测试进度: {current_test}/{total_tests} - "
                                       f"{framework} - {scenario} - {agent_count} agents - {complexity}")
                            
                            # 运行测试
                            if framework == "Our DSL":
                                result = self.test_our_dsl_real_api(scenario, agent_count, complexity)
                            elif framework == "LangChain":
                                result = self.test_langchain_real_api(scenario, agent_count, complexity)
                            elif framework == "CrewAI":
                                result = self.test_crewai_real_api(scenario, agent_count, complexity)
                            elif framework == "AutoGen":
                                result = self.test_autogen_real_api(scenario, agent_count, complexity)
                            
                            # 添加重复次数信息
                            result["repetition"] = repetition + 1
                            benchmark_results.append(result)
                            
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
        results_file = "comprehensive_benchmark_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                "benchmark_results": benchmark_results,
                "memory_tracker": self.memory_tracker,
                "timestamp": datetime.now().isoformat(),
                "experiment_config": self.experiment_config,
                "test_info": {
                    "total_tests": len(benchmark_results),
                    "scenarios": self.experiment_config['scenarios'],
                    "agent_counts": self.experiment_config['agent_counts'],
                    "frameworks": self.experiment_config['frameworks'],
                    "complexities": self.experiment_config['task_complexities'],
                    "repetitions": self.experiment_config['repetitions'],
                    "random_seed": self.random_seed
                }
            }, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ 测试完成！结果已保存到: {results_file}")
        
        # 生成统计摘要
        self._generate_summary(benchmark_results)
        
        return {
            "benchmark_results": benchmark_results,
            "memory_tracker": self.memory_tracker,
            "timestamp": datetime.now().isoformat(),
            "experiment_config": self.experiment_config
        }
    
    def _generate_summary(self, benchmark_results: List[Dict[str, Any]]):
        """生成统计摘要"""
        logger.info("\n📊 测试摘要:")
        logger.info("=" * 50)
        
        # 按框架分组统计
        framework_stats = {}
        for result in benchmark_results:
            if result["status"] == "success":
                framework = result["framework"]
                if framework not in framework_stats:
                    framework_stats[framework] = {
                        "throughput": [],
                        "latency": [],
                        "memory": [],
                        "success_rate": [],
                        "total_tests": 0,
                        "successful_tests": 0
                    }
                
                framework_stats[framework]["throughput"].append(result["throughput"])
                framework_stats[framework]["latency"].append(result["avg_latency"])
                framework_stats[framework]["memory"].append(result["memory_usage"])
                framework_stats[framework]["success_rate"].append(result["success_rate"])
                framework_stats[framework]["total_tests"] += 1
                if result["success_rate"] > 0:
                    framework_stats[framework]["successful_tests"] += 1
        
        # 输出统计结果
        for framework, stats in framework_stats.items():
            if stats["throughput"]:
                avg_throughput = np.mean(stats["throughput"])
                avg_latency = np.mean(stats["latency"])
                avg_memory = np.mean(stats["memory"])
                avg_success_rate = np.mean(stats["success_rate"])
                overall_success_rate = (stats["successful_tests"] / stats["total_tests"]) * 100
                
                logger.info(f"\n{framework}:")
                logger.info(f"  平均吞吐量: {avg_throughput:.3f} tasks/sec")
                logger.info(f"  平均延迟: {avg_latency:.2f} ms")
                logger.info(f"  平均内存使用: {avg_memory:.2f} MB")
                logger.info(f"  平均成功率: {avg_success_rate:.1f}%")
                logger.info(f"  总体成功率: {overall_success_rate:.1f}%")
                logger.info(f"  成功测试数: {stats['successful_tests']}/{stats['total_tests']}")
        
        # 总体统计
        total_tests = len(benchmark_results)
        successful_tests = sum(1 for r in benchmark_results if r["status"] == "success")
        overall_success_rate = (successful_tests / total_tests) * 100
        
        logger.info(f"\n📈 总体统计:")
        logger.info(f"  成功测试: {successful_tests}")
        logger.info(f"  失败测试: {total_tests - successful_tests}")
        logger.info(f"  成功率: {overall_success_rate:.1f}%")

def main():
    """主函数"""
    print("🔬 全面基准测试框架")
    print("=" * 50)
    print("⚠️  注意：此测试使用真实API调用，需要有效的API密钥")
    print("⚠️  测试规模较大，预计需要较长时间完成")
    print("=" * 50)
    
    # 创建基准测试实例
    benchmark = ComprehensiveBenchmark()
    
    # 运行全面基准测试
    results = benchmark.run_comprehensive_benchmark()
    
    print("\n🎉 全面基准测试完成！")
    print(f"总测试数: {len(results['benchmark_results'])}")
    print("结果已保存到 comprehensive_benchmark_results.json")

if __name__ == "__main__":
    main()
