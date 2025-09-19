#!/usr/bin/env python3
"""
测试智能体交互流程
"""

import asyncio
import requests
import json
from datetime import datetime

async def test_autonomous_driving_interaction():
    """测试自动驾驶任务触发的智能体交互"""
    print("🚗 测试自动驾驶任务...")
    
    payload = {
        "start_location": "A",
        "end_location": "B", 
        "passengers": 2
    }
    
    try:
        response = requests.post(
            "http://localhost:8008/events/autonomous_driving",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ 自动驾驶任务发送成功")
            return True
        else:
            print(f"❌ 自动驾驶任务发送失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 自动驾驶任务发送异常: {e}")
        return False

async def test_weather_alert_interaction():
    """测试天气预警任务触发的智能体交互"""
    print("🌧️ 测试天气预警任务...")
    
    payload = {
        "location": "市中心",
        "alert_type": "heavy_rain",
        "severity": 8
    }
    
    try:
        response = requests.post(
            "http://localhost:8008/events/weather_alert",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ 天气预警任务发送成功")
            return True
        else:
            print(f"❌ 天气预警任务发送失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 天气预警任务发送异常: {e}")
        return False

async def test_parking_update_interaction():
    """测试停车更新任务触发的智能体交互"""
    print("🅿️ 测试停车更新任务...")
    
    payload = {
        "location": "市中心停车场",
        "available_spots": 150
    }
    
    try:
        response = requests.post(
            "http://localhost:8008/events/parking_update",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ 停车更新任务发送成功")
            return True
        else:
            print(f"❌ 停车更新任务发送失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 停车更新任务发送异常: {e}")
        return False

async def test_safety_inspection_interaction():
    """测试安全检查任务触发的智能体交互"""
    print("🔒 测试安全检查任务...")
    
    payload = {
        "location": "桥梁B",
        "require_human_intervention": True
    }
    
    try:
        response = requests.post(
            "http://localhost:8008/events/safety_inspection",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ 安全检查任务发送成功")
            return True
        else:
            print(f"❌ 安全检查任务发送失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 安全检查任务发送异常: {e}")
        return False

async def test_report_generation():
    """测试报告生成功能"""
    print("📊 测试报告生成...")
    
    # 模拟一些交互事件
    mock_events = [
        {
            "type": "agent_response",
            "payload": {
                "agent": "自动驾驶系统",
                "result": "路线规划完成，预计行驶时间15分钟"
            },
            "title": "自动驾驶系统 执行完成",
            "timestamp": datetime.now().isoformat()
        },
        {
            "type": "agent_response", 
            "payload": {
                "agent": "天气监测系统",
                "result": "检测到降雨，建议降低行驶速度"
            },
            "title": "天气监测系统 响应完成",
            "timestamp": datetime.now().isoformat()
        }
    ]
    
    try:
        response = requests.post(
            "http://localhost:8008/generate-report",
            json={"events": mock_events},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ 报告生成请求发送成功")
            return True
        else:
            print(f"❌ 报告生成请求发送失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 报告生成请求发送异常: {e}")
        return False

async def main():
    """主测试函数"""
    print("🧪 开始测试智能体交互流程...")
    print("=" * 50)
    
    # 检查后端服务是否运行
    try:
        health_response = requests.get("http://localhost:8008/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ 后端服务运行正常")
        else:
            print("❌ 后端服务异常")
            return
    except Exception as e:
        print(f"❌ 无法连接到后端服务: {e}")
        print("请确保后端服务正在运行 (python3 -m backend.main)")
        return
    
    # 测试各个智能体交互
    tests = [
        test_autonomous_driving_interaction,
        test_weather_alert_interaction, 
        test_parking_update_interaction,
        test_safety_inspection_interaction,
        test_report_generation
    ]
    
    success_count = 0
    for test_func in tests:
        try:
            result = await test_func()
            if result:
                success_count += 1
            await asyncio.sleep(2)  # 等待2秒让工作流完成
        except Exception as e:
            print(f"❌ 测试异常: {e}")
    
    print(f"\n📊 测试结果: {success_count}/{len(tests)} 成功")
    
    if success_count == len(tests):
        print("🎉 所有测试通过！智能体交互系统运行正常")
        print("\n💡 使用说明:")
        print("1. 打开浏览器访问 http://localhost:3000")
        print("2. 点击任意智能体卡片的'发送'按钮")
        print("3. 观察交互记录中的智能体协作过程")
        print("4. 点击'生成报告'按钮查看分析报告")
    else:
        print("⚠️  部分测试失败，请检查系统配置")

if __name__ == "__main__":
    asyncio.run(main())
