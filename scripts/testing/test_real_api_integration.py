#!/usr/bin/env python3
"""
测试真实API集成
Test Real API Integration
"""

import asyncio
import os
import sys
import logging

# 添加项目路径
sys.path.append('backend')
sys.path.append('agents')

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_real_weather_api():
    """测试真实天气API集成"""
    print("🧪 测试真实天气API集成...")
    
    # 设置API密钥（如果没有设置，会使用模拟数据）
    os.environ.setdefault("OPENWEATHER_API_KEY", "")
    
    # 导入天气智能体
    from agents.weather_agent import WeatherAgent
    from core.base_agent import BaseAgent
    
    # 创建模拟的DSL实例
    class MockDSL:
        pass
    
    # 创建天气智能体
    weather_agent = WeatherAgent(MockDSL())
    
    print(f"📊 API状态: {'✅ 已配置' if weather_agent.use_real_api else '❌ 未配置，使用模拟数据'}")
    
    # 测试获取天气数据
    print("\n🌤️ 测试获取天气数据...")
    weather_data = await weather_agent.get_real_weather_data("San Francisco")
    
    print(f"📍 城市: {weather_data['city']}")
    print(f"🌡️ 温度: {weather_data['temperature']}°C")
    print(f"💧 湿度: {weather_data['humidity']}%")
    print(f"👁️ 能见度: {weather_data['visibility']}km")
    print(f"📝 描述: {weather_data['description']}")
    print(f"📊 数据来源: {weather_data['source']}")
    print(f"✅ 真实数据: {'是' if weather_data['is_real'] else '否'}")
    
    # 测试天气预警
    print("\n🚨 测试天气预警...")
    alert_data = {
        'alert_type': 'rain',
        'area': 'San Francisco',
        'severity': 5
    }
    
    alert_response = await weather_agent.trigger_weather_alert(alert_data)
    print("预警响应:")
    print(alert_response[:200] + "..." if len(alert_response) > 200 else alert_response)
    
    # 测试自动驾驶天气分析
    print("\n🚗 测试自动驾驶天气分析...")
    driving_data = {
        'start_location': 'San Francisco',
        'weather_condition': 'rain'
    }
    
    driving_response = await weather_agent.respond_to_autonomous_driving(driving_data)
    print("自动驾驶分析:")
    print(driving_response[:200] + "..." if len(driving_response) > 200 else driving_response)

async def test_api_key_setup():
    """测试API密钥设置"""
    print("\n🔑 API密钥设置指南:")
    print("1. 申请OpenWeatherMap API密钥:")
    print("   https://openweathermap.org/api")
    print("2. 设置环境变量:")
    print("   export OPENWEATHER_API_KEY='your_api_key_here'")
    print("3. 或者创建.env文件:")
    print("   OPENWEATHER_API_KEY=your_api_key_here")
    print("\n💡 免费额度: 1000次/天")

async def main():
    """主测试函数"""
    print("🚀 开始测试真实API集成...")
    
    await test_real_weather_api()
    await test_api_key_setup()
    
    print("\n✅ 测试完成！")
    print("\n📋 下一步:")
    print("1. 申请OpenWeatherMap API密钥")
    print("2. 设置环境变量")
    print("3. 重新运行测试验证真实数据")

if __name__ == "__main__":
    asyncio.run(main())
