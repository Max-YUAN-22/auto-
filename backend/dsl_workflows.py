import asyncio
import json
from datetime import datetime
from typing import Dict, Any
from .dependencies import get_dsl_instance, get_websocket_manager
from dsl.dsl import DSL

dsl = get_dsl_instance()

async def broadcast_message_task(dsl: DSL, message: Any):
    """Broadcasts a message to all connected Socket.IO clients."""
    from socket_app import sio
    from datetime import datetime
    try:
        if isinstance(message, str):
            # Wrap raw strings in a structured JSON object
            await sio.emit('broadcast', {
                "type": "simulation_log",
                "title": "Simulation Log",
                "payload": {"details": message},
                "timestamp": datetime.now().isoformat()
            }, room='default_room')
        elif isinstance(message, dict):
            # Ensure timestamp is present and in ISO format
            if 'timestamp' not in message:
                message['timestamp'] = datetime.now().isoformat()
            elif isinstance(message['timestamp'], (int, float)):
                # Convert Unix timestamp to ISO format
                message['timestamp'] = datetime.fromtimestamp(message['timestamp']).isoformat()
            # Send dictionaries as-is
            await sio.emit('broadcast', message, room='default_room')
        else:
            # Log an error for unhandled types
            print(f"Cannot broadcast message of unknown type: {type(message)}")
    except Exception as e:
        print(f"Error broadcasting message: {e}")
        import traceback
        traceback.print_exc()

async def fire_alert_workflow_task(dsl: DSL, event_data: dict):
    """Workflow for handling fire alerts."""
    dsl.gen(
        name="broadcast_fire_alert",
        prompt=f"Broadcasting fire alert: {event_data}",
        agent="broadcast_agent"
    ).schedule()
    
    safety_check_task = dsl.gen(
        name="safety_protocol_check",
        prompt="Confirm all safety protocols are active for a fire emergency.",
        agent="safety_agent"
    ).schedule()

    report_task = dsl.gen(
        name="generate_fire_report",
        prompt=f"Generate a detailed report for the fire event: {event_data}",
        agent="reporting_agent"
    ).schedule()

    await broadcast_message_task(dsl, {
        "type": "fire_alert",
        "title": "Fire Alert",
        "payload": event_data
    })
    
    await asyncio.to_thread(dsl.join, [safety_check_task, report_task], mode="all")

async def traffic_incident_workflow_task(dsl: DSL, event_data: dict):
    """Workflow for handling traffic incidents."""
    dsl.gen(
        name="broadcast_traffic_incident",
        prompt=f"Broadcasting traffic incident: {event_data}",
        agent="broadcast_agent"
    ).schedule()

    reroute_task = dsl.gen(
        name="calculate_optimal_reroute",
        prompt=f"Calculate optimal rerouting for traffic incident at {event_data['location']}",
        agent="traffic_agent"
    ).schedule()

    await broadcast_message_task(dsl, {
        "type": "traffic_incident",
        "title": "Traffic Incident",
        "payload": event_data
    })
    
    await asyncio.to_thread(dsl.join, [reroute_task])

async def master_workflow_chain_task(dsl: DSL, event_data: dict):
    """Workflow for handling weather alerts, which may trigger other workflows."""
    dsl.gen(
        name="broadcast_weather_alert",
        prompt=f"Broadcasting weather alert: {event_data}",
        agent="broadcast_agent"
    ).schedule()

    await broadcast_message_task(dsl, {
        "type": "weather_alert",
        "title": "Weather Alert",
        "payload": event_data
    })
    
    if "fire" in event_data.get("secondary_risks", []):
        fire_event = {
            "location": event_data["area"],
            "details": "Secondary fire risk due to weather conditions."
        }
        await fire_alert_workflow_task(dsl, fire_event)


async def city_analysis_workflow_task(dsl: DSL, city: str):
    """Workflow for city analysis using multiple agents."""
    await broadcast_message_task(dsl, {
        "type": "agent_message",
        "payload": f"Starting analysis for {city}...",
        "title": "City Analysis Workflow"
    })

    planning_task = dsl.gen(
        name="create_analysis_plan",
        prompt=f"Create a plan to analyze the city of {city}.",
        agent="planning_agent"
    ).schedule()
    await asyncio.to_thread(dsl.join, [planning_task])

    await broadcast_message_task(dsl, {
        "type": "agent_message",
        "payload": f"Plan created. Collecting data for {city}...",
        "title": "City Analysis Workflow"
    })

    data_collection_task = dsl.gen(
        name="collect_city_data",
        prompt=f"Collect relevant data for the city of {city}.",
        agent="data_collection_agent"
    ).schedule()
    await asyncio.to_thread(dsl.join, [data_collection_task])

    await broadcast_message_task(dsl, {
        "type": "agent_message",
        "payload": f"Data collected. Generating report for {city}...",
        "title": "City Analysis Workflow"
    })

    report_task = dsl.gen(
        name="generate_city_report",
        prompt=f"Generate a comprehensive analysis report for {city} based on the collected data.",
        agent="reporting_agent"
    ).schedule()
    join_results = await asyncio.to_thread(dsl.join, [report_task])

    report_result = join_results.get(report_task.name)
    report_content = report_result.get("report", "Failed to generate report.") if isinstance(report_result, dict) else str(report_result)

    await broadcast_message_task(dsl, {
        "type": "analysis_report",
        "payload": {"report": report_content},
        "title": "City Analysis Report"
    })


async def smart_city_simulation_workflow(dsl: DSL, entry_point: str, task_data: Dict[str, Any]):
    """
    A dynamic workflow that simulates a smart city environment, allowing for a flexible entry point.
    The workflow is initiated by a starting task and then triggers other agents to react to it.
    """
    print(f"Starting smart city simulation workflow with entry_point: {entry_point}")
    
    # 导入主智能体和子智能体实例
    from dependencies import (
        city_manager_agent, traffic_manager_agent, weather_agent, parking_agent, safety_agent
    )
    
    # 发送初始触发事件
    event_type_map = {
        "autonomous_driving_task": "autonomous_driving",
        "weather_alert_task": "weather_alert", 
        "parking_update_task": "parking_update",
        "safety_inspection_task": "safety_inspection"
    }
    
    initial_event_type = event_type_map.get(entry_point, entry_point)
    # 不重复发送初始事件，因为API已经发送了
    # await broadcast_message_task(dsl, {
    #     "type": initial_event_type,
    #     "payload": task_data,
    #     "title": f"{initial_event_type.replace('_', ' ').title()} Event"
    # })
    
    # 发送工作流启动消息
    await broadcast_message_task(dsl, {
        "type": "workflow_start", 
        "payload": f"启动 {entry_point} 工作流，主智能体开始协调", 
        "title": "智能体协调启动"
    })

    # 使用主智能体协调所有任务
    main_task_execution = dsl.gen(
        name=f"{entry_point}_coordination",
        prompt=f"协调 {entry_point} 任务，分析任务数据并制定执行策略",
        agent=city_manager_agent
    ).schedule()
    
    join_results = await asyncio.to_thread(dsl.join, [main_task_execution])
    main_result = join_results.get(main_task_execution.name)
    main_result_str = str(main_result.get("result", main_result) if isinstance(main_result, dict) else main_result)

    # 发送主智能体的协调结果
    await broadcast_message_task(dsl, {
        "type": "main_coordination",
        "payload": {
            "agent": "城市管理主智能体",
            "result": main_result_str,
            "task": entry_point,
            "step": "1/4"
        },
        "title": "主智能体协调完成"
    })

    # 定义智能的子智能体配置 - 根据任务类型选择相关智能体
    sub_agent_configs = {
        "autonomous_driving_task": {
            "primary_agent": {"agent": traffic_manager_agent, "title": "交通管理子智能体", "method": "analyze_autonomous_driving_request"},
            "related_agents": [
                {"agent": weather_agent, "title": "天气监测子智能体", "method": "respond_to_autonomous_driving", "condition": "weather_condition"}
            ]
        },
        "weather_alert_task": {
            "primary_agent": {"agent": weather_agent, "title": "天气监测子智能体", "method": "trigger_weather_alert"},
            "related_agents": [
                {"agent": traffic_manager_agent, "title": "交通管理子智能体", "method": "respond_to_weather_alert", "condition": "traffic_impact"},
                {"agent": safety_agent, "title": "安全监测子智能体", "method": "respond_to_weather_alert", "condition": "safety_risk"}
            ]
        },
        "parking_update_task": {
            "primary_agent": {"agent": parking_agent, "title": "停车管理子智能体", "method": "update_parking_status"},
            "related_agents": [
                {"agent": traffic_manager_agent, "title": "交通管理子智能体", "method": "respond_to_parking_update", "condition": "traffic_impact"}
            ]
        },
        "safety_inspection_task": {
            "primary_agent": {"agent": safety_agent, "title": "安全监测子智能体", "method": "monitor_safety"},
            "related_agents": [
                {"agent": traffic_manager_agent, "title": "交通管理子智能体", "method": "respond_to_safety_inspection", "condition": "traffic_impact"}
            ]
        },
    }

    if entry_point not in sub_agent_configs:
        error_message = f"无效的入口任务: {entry_point}"
        await broadcast_message_task(dsl, {"type": "error", "payload": error_message, "title": "错误"})
        print(error_message)
        return

    # 获取子智能体配置
    sub_agents_config = sub_agent_configs[entry_point]
    
    # 智能选择需要响应的智能体
    selected_agents = []
    
    # 总是包含主要智能体
    selected_agents.append(sub_agents_config["primary_agent"])
    
    # 根据条件选择相关智能体
    for related_agent in sub_agents_config["related_agents"]:
        condition = related_agent.get("condition", "")
        should_include = True  # 默认包含所有相关智能体
        
        if condition == "weather_condition":
            # 如果有天气条件，包含天气智能体
            weather_condition = task_data.get('weather_condition', '')
            should_include = bool(weather_condition and weather_condition.strip())
        elif condition == "traffic_impact":
            # 如果任务可能影响交通，包含交通智能体
            should_include = True  # 大部分任务都会影响交通
        elif condition == "safety_risk":
            # 如果任务涉及安全风险，包含安全智能体
            should_include = True  # 大部分任务都涉及安全
        
        if should_include:
            selected_agents.append(related_agent)
    
    # 发送子智能体协调开始消息
    await broadcast_message_task(dsl, {
        "type": "sub_agent_coordination",
        "payload": f"主智能体分发任务给 {len(selected_agents)} 个子智能体",
        "title": "子智能体协调开始",
        "step": "2/4"
    })

    # 执行子智能体任务 - 分步执行
    sub_agent_tasks = []
    for i, agent_config in enumerate(selected_agents):
        agent_instance = agent_config['agent']
        agent_title = agent_config['title']
        method_name = agent_config['method']
        
        # 为智能体准备增强的任务数据，包含上下文信息
        enhanced_task_data = {
            **task_data,  # 原始任务数据
            'trigger_event': entry_point,  # 触发事件类型
            'trigger_time': datetime.now().isoformat(),  # 触发时间
            'context': {
                'weather_condition': task_data.get('alert_type', '') if entry_point == 'weather_alert_task' else '',
                'location': task_data.get('area', task_data.get('location', '')),
                'severity': task_data.get('severity', 5),
                'original_task': entry_point
            }
        }
        
        # 发送子智能体开始处理消息
        await broadcast_message_task(dsl, {
            "type": "sub_agent_processing",
            "payload": {
                "agent": agent_title,
                "method": method_name,
                "step": f"2.{i+1}/4"
            },
            "title": f"{agent_title} 开始处理"
        })
        
        # 直接调用智能体方法并传递增强的任务数据
        try:
            if hasattr(agent_instance, method_name):
                method = getattr(agent_instance, method_name)
                # 检查方法是否为异步方法
                if asyncio.iscoroutinefunction(method):
                    result = await method(enhanced_task_data)
                else:
                    result = method(enhanced_task_data)
                sub_agent_tasks.append((agent_title, result))
                
                # 发送子智能体处理完成消息
                await broadcast_message_task(dsl, {
                    "type": "sub_agent_completed",
                    "payload": {
                        "agent": agent_title,
                        "result": str(result)[:100] + "..." if len(str(result)) > 100 else str(result),
                        "step": f"2.{i+1}/4"
                    },
                    "title": f"{agent_title} 处理完成"
                })
            else:
                # 如果方法不存在，使用默认的DSL任务
                task = dsl.gen(
                    name=f"{entry_point}_{agent_title.replace('子智能体', '').replace(' ', '_')}",
                    prompt=f"执行 {method_name} 方法，处理 {entry_point} 任务数据: {enhanced_task_data}",
                    agent=agent_instance
                ).schedule()
                sub_agent_tasks.append((agent_title, task))
        except Exception as e:
            error_result = f"智能体 {agent_title} 执行出错: {str(e)}"
            sub_agent_tasks.append((agent_title, error_result))
            
            # 发送错误消息
            await broadcast_message_task(dsl, {
                "type": "sub_agent_error",
                "payload": {
                    "agent": agent_title,
                    "error": str(e),
                    "step": f"2.{i+1}/4"
                },
                "title": f"{agent_title} 处理出错"
            })

    # 只对DSL任务进行join操作
    dsl_tasks = [task for _, task in sub_agent_tasks if not isinstance(task, str)]
    if dsl_tasks:
        join_results = await asyncio.to_thread(dsl.join, dsl_tasks, mode="all")
    else:
        join_results = {}

    # 收集所有子智能体响应结果
    responses = []
    for title, result in sub_agent_tasks:
        if isinstance(result, str):
            # 直接的方法调用结果
            result_str = result
        else:
            # DSL任务结果
            result_str = str(result.get("result", result) if isinstance(result, dict) else result)
        
        responses.append({
            "agent": title,
            "result": result_str[:200] + "..." if len(result_str) > 200 else result_str  # 增加显示长度
        })

    # 发送结果汇总消息
    await broadcast_message_task(dsl, {
        "type": "result_summary",
        "payload": {
            "total_agents": len(responses),
            "successful_agents": len([r for r in responses if "出错" not in r["result"]]),
            "step": "3/4"
        },
        "title": "结果汇总"
    })

    # 发送汇总的响应结果 - 合并所有事件为一个
    await broadcast_message_task(dsl, {
        "type": "coordination_result",
        "payload": {
            "triggered_by": "城市管理主智能体",
            "responses": responses,
            "total_agents": len(responses),
            "workflow_status": "completed",
            "task_type": entry_point,
            "summary": f"主智能体成功协调了 {len(responses)} 个子智能体完成 {entry_point} 任务",
            "step": "4/4"
        },
        "title": "智能体协同完成"
    })


async def generate_report_workflow(dsl: DSL, events_data: list = None):
    """
    Workflow to generate a report of the last 5 interactions.
    """
    await broadcast_message_task(dsl, {
        "type": "agent_message",
        "payload": "正在生成基于近五次交互的城市分析报告...",
        "title": "报告生成器",
        "timestamp": asyncio.get_event_loop().time()
    })

    # 使用传入的事件数据或从历史记录获取
    if events_data:
        last_5_interactions = events_data[-5:]
    else:
        history = dsl.get_history() 
        last_5_interactions = history[-5:]

    if not last_5_interactions:
        await broadcast_message_task(dsl, {
            "type": "analysis_report",
            "payload": {"report": "暂无交互记录，无法生成报告。"},
            "title": "城市分析报告",
            "timestamp": asyncio.get_event_loop().time()
        })
        return

    # 构建报告提示
    report_prompt = "基于以下智能城市交互记录，生成一份简洁的城市分析报告，包括主要发现、趋势分析和建议：\n\n"
    for i, interaction in enumerate(last_5_interactions, 1):
        if isinstance(interaction, dict):
            if 'type' in interaction and 'payload' in interaction:
                # 处理WebSocket事件格式
                event_type = interaction.get('type', '未知事件')
                payload = interaction.get('payload', {})
                title = interaction.get('title', '未知标题')
                
                if event_type == 'agent_response':
                    agent = payload.get('agent', '未知智能体')
                    result = payload.get('result', '无结果')
                    report_prompt += f"{i}. {agent} 响应: {result}\n"
                elif event_type == 'agent_message':
                    message = payload if isinstance(payload, str) else str(payload)
                    report_prompt += f"{i}. {title}: {message}\n"
                else:
                    report_prompt += f"{i}. {title}: {str(payload)}\n"
            else:
                # 处理历史记录格式
                prompt = interaction.get("prompt", "未知提示")
                result = interaction.get("result", "无结果")
                report_prompt += f"{i}. {prompt}: {result}\n"
        else:
            report_prompt += f"{i}. {str(interaction)}\n"

    # 导入智能体实例
    from dependencies import weather_agent
    
    report_task = dsl.gen(
        name="generate_city_analysis_report",
        prompt=report_prompt,
        agent=weather_agent
    ).schedule()
    join_results = await asyncio.to_thread(dsl.join, [report_task])

    report_result = join_results.get(report_task.name)
    report_content = report_result.get("report", "报告生成失败。") if isinstance(report_result, dict) else str(report_result)

    await broadcast_message_task(dsl, {
        "type": "analysis_report",
        "payload": {"report": report_content},
        "title": "城市分析报告",
        "timestamp": datetime.now().isoformat()
    })