# core/llm.py
import os
import json
import logging
from functools import lru_cache
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()

def get_llm():
    """
    Returns a configured OpenAI client for DeepSeek.
    """
    if not DEEPSEEK_API_KEY:
        return None
    return OpenAI(
        base_url='https://api.deepseek.com',
        api_key=DEEPSEEK_API_KEY
    )

def llm_callable(prompt: str, role: str = None) -> str:
    """
    A callable function for DSL to use for LLM calls.
    Returns a mock response if no API key is available.
    """
    if not DEEPSEEK_API_KEY:
        # Return a mock response based on the prompt
        if "自动驾驶" in prompt:
            return "自动驾驶系统已启动，路线规划完成，预计到达时间15分钟。系统检测到交通状况良好，将采用最优路径。"
        elif "天气" in prompt:
            return "天气监测系统检测到当前天气状况稳定，无异常天气预警。建议继续正常运营。"
        elif "停车" in prompt:
            return "停车管理系统更新完成，当前可用车位充足。建议引导车辆到指定区域停车。"
        elif "安全" in prompt:
            return "安全检查完成，所有系统运行正常。未发现安全隐患，建议继续监控。"
        elif "报告" in prompt:
            return "基于最近的交互记录，城市运行状况良好。各系统协调工作正常，建议继续保持当前运营状态。"
        else:
            return f"[模拟响应] 已处理任务: {prompt[:50]}..."
    
    try:
        client = get_llm()
        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个智能城市管理助手，负责处理各种城市运营任务。请用中文简洁地回应用户的请求。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"LLM调用失败: {e}")
        return f"[API错误] 无法处理请求: {prompt[:50]}..."


async def generate_report_with_deepseek(report_data: str, language: str = "zh") -> str:
    """
    Generates a report using the DeepSeek API with caching.
    The report_data is a JSON string containing a list of recent events.
    Returns a local placeholder if the API key is not set.
    """
    if not DEEPSEEK_API_KEY:
        logger.info("DEEPSEEK_API_KEY not set, returning local placeholder.")
        try:
            events = json.loads(report_data)
            event_summary = "\n".join([f"- {event.get('prompt', 'Unknown')}: {event.get('result', 'No details')}" for event in events])
            return (
                f"[本地报告] 智能城市事件分析\n"
                f"分析的事件:\n{event_summary}\n"
                f"总结: 基于最近的交互记录，城市各系统运行正常，智能体间协作良好。\n"
                f"建议: 继续保持当前运营状态，定期进行系统检查。\n"
                f"提示: 设置DEEPSEEK_API_KEY环境变量以使用真实的LLM。"
            )
        except:
            return (
                f"[本地报告] 智能城市事件分析\n"
                f"基于最近的交互记录，城市各系统运行正常，智能体间协作良好。\n"
                f"建议: 继续保持当前运营状态，定期进行系统检查。"
            )

    system_prompt = (
        "你是一个智能城市分析助手，负责分析最近的智能城市事件并生成有洞察力的报告。 "
        "基于提供的事件历史:\n"
        "1. 总结事件序列及其关系\n"
        "2. 识别事件间的模式或关联\n"
        "3. 评估整体城市状态和潜在影响\n"
        "4. 提供可操作的建议\n"
        f"用{language}写报告，包含清晰的章节和要点。"
    )

    try:
        logger.info(f"Generating report for: {report_data}")
        client = get_llm()
        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"基于以下数据生成城市分析报告: {report_data}"}
            ],
            temperature=0.3
        )
        report = completion.choices[0].message.content
        if not report:
            logger.error("Empty response from API")
            return "[API错误] 空响应"
        return report
    except Exception as e:
        logger.exception("报告生成过程中发生意外错误。")
        return f"[意外错误] 发生意外错误: {e}"