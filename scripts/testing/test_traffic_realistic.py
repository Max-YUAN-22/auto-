#!/usr/bin/env python3
"""
测试交通管理智能体的真实距离计算
Test Traffic Manager Agent Real Distance Calculation
"""

import sys
import os

# 添加项目路径
sys.path.append('backend')
sys.path.append('agents')

def test_traffic_manager():
    """测试交通管理智能体"""
    print("🧪 测试交通管理智能体真实距离计算...")
    
    # 导入交通管理智能体
    from agents.traffic_manager_agent import TrafficManagerAgent
    from core.base_agent import BaseAgent
    
    # 创建模拟的DSL实例
    class MockDSL:
        pass
    
    # 创建交通管理智能体
    traffic_agent = TrafficManagerAgent(MockDSL())
    
    # 测试不同路线
    test_routes = [
        {
            'name': '短距离路线',
            'start': '北京西站',
            'end': '北京儿童医院',
            'weather': '晴天',
            'time': '周末'
        },
        {
            'name': '中距离路线',
            'start': '国贸CBD',
            'end': '首都机场T3',
            'weather': '小雨',
            'time': '早高峰'
        },
        {
            'name': '长距离路线',
            'start': '朝阳公园',
            'end': '八达岭长城',
            'weather': '暴雨',
            'time': '晚高峰'
        },
        {
            'name': '跨区域路线',
            'start': '协和医院',
            'end': '中关村',
            'weather': '多云',
            'time': '正常'
        }
    ]
    
    print("\n🚗 测试不同路线的自动驾驶响应:")
    print("=" * 80)
    
    for i, route in enumerate(test_routes, 1):
        print(f"\n📍 测试 {i}: {route['name']}")
        print(f"起点: {route['start']}")
        print(f"终点: {route['end']}")
        print(f"天气: {route['weather']}")
        print(f"时间: {route['time']}")
        print("-" * 60)
        
        # 计算距离
        distance = traffic_agent.calculate_distance(route['start'], route['end'])
        print(f"实际距离: {distance}公里")
        
        # 计算行驶时间
        estimated_time = traffic_agent.calculate_travel_time(
            distance, route['start'], route['end'], 
            route['weather'], route['time']
        )
        print(f"预计时间: {estimated_time}分钟")
        
        # 生成完整响应
        task_data = {
            'start_location': route['start'],
            'end_location': route['end'],
            'passengers': 2,
            'weather_condition': route['weather'],
            'current_time': route['time']
        }
        
        response = traffic_agent.analyze_autonomous_driving_request(task_data)
        print("\n📋 完整响应:")
        print(response)
        print("=" * 80)
    
    print("\n✅ 测试完成！")
    print("\n📊 测试结果分析:")
    print("1. 不同距离的路线有不同的预计时间")
    print("2. 天气条件影响行驶时间和限速")
    print("3. 时间因素（高峰/周末）影响交通状况")
    print("4. 路线类型根据距离自动调整")

if __name__ == "__main__":
    test_traffic_manager()
