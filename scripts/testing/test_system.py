#!/usr/bin/env python3
"""
测试智能城市多智能体系统
"""

import asyncio
import json
import requests
import time
from datetime import datetime

# 测试数据
test_data = {
    "autonomous_driving": {
        "start_location": "A",
        "end_location": "B", 
        "passengers": 2
    },
    "weather_alert": {
        "location": "市中心",
        "alert_type": "heavy_rain",
        "severity": 8
    },
    "parking_update": {
        "location": "市中心停车场",
        "available_spots": 150
    },
    "safety_inspection": {
        "location": "桥梁B",
        "require_human_intervention": True
    }
}

def test_api_endpoint(endpoint, data):
    """测试API端点"""
    url = f"http://localhost:8000/events/{endpoint}"
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"✅ {endpoint}: {response.status_code} - {response.json()}")
        return True
    except Exception as e:
        print(f"❌ {endpoint}: {e}")
        return False

def test_health():
    """测试健康检查"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ 后端服务健康")
            return True
        else:
            print(f"❌ 后端服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到后端: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 开始测试智能城市多智能体系统...")
    print("=" * 50)
    
    # 测试健康检查
    if not test_health():
        print("❌ 后端服务未启动，请先运行 start_system.sh")
        return
    
    print("\n📡 测试API端点...")
    success_count = 0
    total_tests = len(test_data)
    
    for endpoint, data in test_data.items():
        if test_api_endpoint(endpoint, data):
            success_count += 1
        time.sleep(1)  # 避免请求过快
    
    print(f"\n📊 测试结果: {success_count}/{total_tests} 成功")
    
    if success_count == total_tests:
        print("🎉 所有测试通过！系统运行正常")
        print("\n💡 提示:")
        print("- 点击各个模块的'发送'按钮测试智能体交互")
        print("- 查看'交互记录'了解智能体之间的协作")
        print("- 点击'生成报告'按钮获取城市分析报告")
    else:
        print("⚠️  部分测试失败，请检查系统配置")

if __name__ == "__main__":
    main()
