#!/usr/bin/env python3
"""
测试真实交互响应
Test Real Interaction Response
"""

import asyncio
import json
from backend.dsl_workflows import smart_city_simulation_workflow

async def test_weather_aware_response():
    """测试天气感知的响应"""
    print("🧪 测试天气感知的自动驾驶响应...")
    
    # 测试暴雨天气
    print("\n🌧️ 测试暴雨天气场景:")
    task_data = {
        "start_location": "国贸CBD",
        "end_location": "首都机场T3", 
        "passengers": 1,
        "weather_condition": "暴雨",
        "current_time": "早高峰"
    }
    
    await smart_city_simulation_workflow("autonomous_driving_task", task_data)
    
    print("\n" + "="*50)
    
    # 测试晴天天气
    print("\n☀️ 测试晴天天气场景:")
    task_data = {
        "start_location": "朝阳公园",
        "end_location": "八达岭长城",
        "passengers": 4,
        "weather_condition": "晴天",
        "current_time": "周末"
    }
    
    await smart_city_simulation_workflow("autonomous_driving_task", task_data)

if __name__ == "__main__":
    print("🚀 开始测试真实交互响应...")
    asyncio.run(test_weather_aware_response())
    print("\n✅ 测试完成！")
