import random
from core.base_agent import BaseAgent

class SafetyAgent(BaseAgent):
    def __init__(self, dsl_instance):
        super().__init__(
            dsl_instance=dsl_instance,
            role="Safety Supervisor",
            capabilities=["monitor_safety", "trigger_alert", "respond_to_autonomous_driving", "respond_to_weather_alert", "respond_to_parking_update", "respond_to_safety_inspection"]
        )

    def monitor_safety(self, data):
        """监控城市安全状态"""
        location = data.get('location', '未知位置')
        safety_status = data.get('safety_status', 'normal')
        weather_condition = data.get('weather_condition', '')
        
        # 根据天气调整安全等级
        if '暴雨' in weather_condition:
            safety_level = "高风险"
            safety_measures = "加强监控，启动应急预案"
            risk_factors = "能见度低，路面湿滑，山体滑坡风险"
        elif '小雨' in weather_condition:
            safety_level = "中等风险"
            safety_measures = "加强路面监控，提醒注意安全"
            risk_factors = "路面湿滑，能见度一般"
        else:
            safety_level = "低风险"
            safety_measures = "正常监控，标准安全措施"
            risk_factors = "无明显风险因素"
        
        response = f"""SafetyAgent: 安全状态监控

🔍 安全监控信息:
- 监控位置: {location}
- 安全状态: {safety_status}
- 安全等级: {safety_level}
- 天气条件: {weather_condition if weather_condition else '正常'}

⚠️ 风险因素:
- {risk_factors}

🚧 安全措施:
- {safety_measures}
- 监控系统: 正常运行
- 应急响应: 待命状态
- 安全设备: 检查完成

✅ 安全监控系统运行正常"""
        
        print(f"Monitoring safety at {location} with status {safety_status}")
        if safety_status == 'danger':
            self.trigger_alert(location)
        
        return response

    def respond_to_autonomous_driving(self, task_data):
        """响应自动驾驶请求的安全分析"""
        location = task_data.get('start_location', '未知位置')
        weather_condition = task_data.get('weather_condition', '')
        
        if '暴雨' in weather_condition:
            response = f"""SafetyAgent: 自动驾驶安全分析

🌧️ 天气条件: 暴雨
📍 行驶区域: {location}

⚠️ 安全风险评估:
- 能见度风险: 极高
- 路面风险: 极高
- 制动风险: 极高
- 整体风险: 极高

🚧 安全建议:
- 建议暂停自动驾驶服务
- 如必须使用，请切换至人工模式
- 选择主要干道，避开危险路段
- 保持极低车速

🚨 应急准备:
- 应急响应系统已激活
- 救援队伍待命
- 安全监控加强
- 危险路段标记

✅ 安全系统已为恶劣天气做好准备"""
        else:
            response = f"""SafetyAgent: 自动驾驶安全分析

☀️ 天气条件: 良好
📍 行驶区域: {location}

✅ 安全风险评估:
- 能见度风险: 低
- 路面风险: 低
- 制动风险: 低
- 整体风险: 低

🚧 安全建议:
- 自动驾驶模式安全可用
- 正常行驶速度
- 标准安全距离
- 常规监控即可

🚨 应急准备:
- 应急响应系统正常
- 救援队伍待命
- 安全监控正常
- 系统运行最佳

✅ 安全系统运行正常"""
        
        return response

    def respond_to_weather_alert(self, weather_data):
        """响应天气预警的安全管理"""
        # 处理增强的任务数据
        if 'context' in weather_data:
            location = weather_data['context'].get('location', weather_data.get('location', '未知区域'))
            alert_type = weather_data['context'].get('weather_condition', weather_data.get('alert_type', '未知'))
            severity = weather_data['context'].get('severity', weather_data.get('severity', 5))
        else:
            location = weather_data.get('location', '未知区域')
            alert_type = weather_data.get('alert_type', '未知')
            severity = weather_data.get('severity', 5)
        
        if '暴雨' in alert_type or 'heavy_rain' in alert_type:
            response = f"""SafetyAgent: 暴雨天气安全紧急响应

🌧️ 暴雨预警: {alert_type}
📍 影响区域: {location}
⚠️ 严重程度: {severity}/10

🚨 安全风险:
- 能见度: 严重受限 (<50米)
- 路面状况: 极度危险
- 山体滑坡: 高风险
- 积水风险: 极高
- 交通事故风险: 极高

🚧 紧急安全措施:
- 危险路段立即封闭
- 应急通道全面开放
- 救援队伍紧急部署
- 安全监控24小时加强
- 危险区域设置警戒线

🚨 应急预案:
- 一级应急响应启动
- 24小时不间断监控
- 实时风险评估系统
- 快速响应机制激活
- 应急通讯系统畅通

⚠️ 自动驾驶安全建议:
- 立即暂停自动驾驶服务
- 强制切换至人工驾驶模式
- 禁止在危险区域使用自动驾驶
- 加强安全监控和预警

✅ 暴雨天气安全管理系统已全面启动，确保城市安全"""
        else:
            response = f"""SafetyAgent: 天气预警安全管理

🌤️ 天气预警: {alert_type}
📍 影响区域: {location}
⚠️ 严重程度: {severity}/10

✅ 安全风险:
- 能见度: 正常
- 路面状况: 良好
- 环境风险: 低
- 整体安全: 良好

🚧 安全措施:
- 正常监控
- 标准安全措施
- 常规检查
- 预防性维护

🚨 应急预案:
- 正常应急响应
- 标准监控
- 常规检查
- 预防措施

✅ 安全管理系统运行正常"""
        
        return response

    def respond_to_parking_update(self, parking_data):
        """响应停车更新的安全分析"""
        location = parking_data.get('location', '未知位置')
        
        response = f"""SafetyAgent: 停车区域安全分析

🅿️ 停车区域: {location}

🔍 安全检查:
- 停车位安全: 检查完成
- 监控设备: 正常运行
- 照明系统: 正常
- 应急通道: 畅通

🚧 安全措施:
- 安全监控加强
- 定期安全检查
- 应急设备检查
- 安全标识更新

✅ 停车区域安全检查完成"""
        
        return response

    def respond_to_safety_inspection(self, safety_data):
        """响应安全检查"""
        location = safety_data.get('location', '未知位置')
        require_human = safety_data.get('require_human_intervention', False)
        
        if require_human:
            response = f"""SafetyAgent: 安全检查响应

🔍 安全检查区域: {location}
⚠️ 需要人工干预: 是

🚧 安全措施:
- 区域临时封闭
- 安全警戒线设置
- 专业人员介入
- 应急通道开放

🚨 应急准备:
- 救援队伍待命
- 安全设备检查
- 应急通讯畅通
- 危险区域标记

✅ 安全检查安全措施已全面实施"""
        else:
            response = f"""SafetyAgent: 安全检查响应

🔍 安全检查区域: {location}
✅ 需要人工干预: 否

🚧 安全措施:
- 区域正常开放
- 安全监控正常
- 常规检查完成
- 安全设备正常

🚨 应急准备:
- 应急响应正常
- 安全监控正常
- 通讯系统正常
- 设备运行正常

✅ 安全检查安全措施已实施"""
        
        return response

    def trigger_alert(self, location):
        """触发安全警报"""
        print(f"Safety alert triggered at {location}.")
        return f"安全警报已在 {location} 触发"

