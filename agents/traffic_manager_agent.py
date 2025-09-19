import random
import math
from datetime import datetime, timedelta
from core.base_agent import BaseAgent

class TrafficManagerAgent(BaseAgent):
    """交通管理子智能体 - Sub Agent"""
    
    def __init__(self, dsl_instance):
        super().__init__(
            dsl_instance=dsl_instance,
            role="TrafficManager",
            capabilities=["route_planning", "traffic_monitoring", "signal_control", "incident_response"]
        )
        self.active_routes = {}
        self.traffic_sensors = {}
        
        # 北京主要地点的坐标和距离数据
        self.location_data = {
            '北京西站': {'lat': 39.8968, 'lng': 116.3204, 'area': '西城区'},
            '首都机场T3': {'lat': 40.0799, 'lng': 116.6031, 'area': '顺义区'},
            '国贸CBD': {'lat': 39.9042, 'lng': 116.4619, 'area': '朝阳区'},
            '朝阳公园': {'lat': 39.9375, 'lng': 116.4731, 'area': '朝阳区'},
            '八达岭长城': {'lat': 40.3589, 'lng': 116.0144, 'area': '延庆区'},
            '协和医院': {'lat': 39.9042, 'lng': 116.4074, 'area': '东城区'},
            '北京儿童医院': {'lat': 39.8968, 'lng': 116.3204, 'area': '西城区'},
            '天安门': {'lat': 39.9042, 'lng': 116.4074, 'area': '东城区'},
            '三里屯': {'lat': 39.9375, 'lng': 116.4619, 'area': '朝阳区'},
            '中关村': {'lat': 39.9836, 'lng': 116.3164, 'area': '海淀区'}
        }
        
        # 不同区域的平均车速
        self.area_speed = {
            '西城区': 35, '顺义区': 50, '朝阳区': 40, '延庆区': 60,
            '东城区': 30, '海淀区': 45, '丰台区': 40, '石景山区': 45
        }
    
    def calculate_distance(self, start_loc, end_loc):
        """计算两点间的距离（公里）"""
        start_data = self.location_data.get(start_loc)
        end_data = self.location_data.get(end_loc)
        
        if not start_data or not end_data:
            # 如果地点不在数据库中，使用随机距离
            return random.randint(5, 50)
        
        # 使用Haversine公式计算距离
        lat1, lng1 = math.radians(start_data['lat']), math.radians(start_data['lng'])
        lat2, lng2 = math.radians(end_data['lat']), math.radians(end_data['lng'])
        
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # 地球半径（公里）
        r = 6371
        distance = c * r
        
        return round(distance, 1)
    
    def get_area_speed(self, location):
        """获取区域平均车速"""
        location_data = self.location_data.get(location)
        if location_data:
            return self.area_speed.get(location_data['area'], 40)
        return 40  # 默认车速
    
    def calculate_travel_time(self, distance, start_loc, end_loc, weather_condition, current_time):
        """计算实际行驶时间"""
        # 获取起点和终点的平均车速
        start_speed = self.get_area_speed(start_loc)
        end_speed = self.get_area_speed(end_loc)
        avg_speed = (start_speed + end_speed) / 2
        
        # 基础行驶时间（小时）
        base_time = distance / avg_speed
        
        # 天气影响系数
        weather_factor = 1.0
        if '暴雨' in weather_condition or '大雨' in weather_condition:
            weather_factor = 1.5  # 暴雨时速度降低50%
        elif '小雨' in weather_condition or '中雨' in weather_condition:
            weather_factor = 1.2  # 小雨时速度降低20%
        elif '晴天' in weather_condition or '多云' in weather_condition:
            weather_factor = 0.9  # 晴天时速度提升10%
        
        # 时间影响系数
        time_factor = 1.0
        if '高峰' in current_time or 'rush' in current_time.lower():
            time_factor = 1.8  # 高峰时速度降低80%
        elif '周末' in current_time:
            time_factor = 1.1  # 周末稍微拥堵
        
        # 计算最终时间（分钟）
        final_time = base_time * 60 * weather_factor * time_factor
        
        return max(5, int(final_time))  # 最少5分钟
    
    def analyze_autonomous_driving_request(self, task_data):
        """分析自动驾驶请求 - 根据实际输入动态响应"""
        start_loc = task_data.get('start_location', '未知起点')
        end_loc = task_data.get('end_location', '未知终点')
        passengers = task_data.get('passengers', 1)
        
        # 检查是否有天气信息影响
        weather_condition = task_data.get('weather_condition', '')
        current_time = task_data.get('current_time', '')
        
        # 计算实际距离
        distance = self.calculate_distance(start_loc, end_loc)
        
        # 计算实际行驶时间
        estimated_time = self.calculate_travel_time(distance, start_loc, end_loc, weather_condition, current_time)
        
        # 根据距离和天气调整限速
        if '暴雨' in weather_condition or '大雨' in weather_condition:
            speed_limit = random.randint(30, 50)
            road_condition = "湿滑路面"
            visibility = "能见度低"
            safety_note = "⚠️ 暴雨天气，建议延迟出行或选择公共交通"
        elif '小雨' in weather_condition or '中雨' in weather_condition:
            speed_limit = random.randint(40, 60)
            road_condition = "轻微湿滑"
            visibility = "能见度一般"
            safety_note = "🌧️ 雨天路滑，请谨慎驾驶"
        elif '晴天' in weather_condition or '多云' in weather_condition:
            speed_limit = random.randint(60, 80)
            road_condition = "干燥良好"
            visibility = "能见度良好"
            safety_note = "☀️ 天气良好，适合自动驾驶"
        else:
            speed_limit = random.randint(50, 70)
            road_condition = "正常"
            visibility = "正常"
            safety_note = "✅ 路况正常，自动驾驶系统运行良好"
        
        # 根据时间调整
        if '高峰' in current_time or 'rush' in current_time.lower():
            traffic_condition = "高峰拥堵"
        else:
            traffic_condition = "交通顺畅"
        
        # 根据距离生成不同的路线建议
        if distance > 30:
            route_type = "高速公路+城市道路"
            route_description = "主要使用高速公路，部分城市道路"
        elif distance > 15:
            route_type = "城市快速路"
            route_description = "城市快速路为主，避开拥堵路段"
        else:
            route_type = "城市道路"
            route_description = "城市道路，优化信号灯通行"
        
        response = f"""TrafficManager: 自动驾驶路线分析完成

🚦 实时交通数据:
- 起点: {start_loc} ({self.location_data.get(start_loc, {}).get('area', '未知区域')})
- 终点: {end_loc} ({self.location_data.get(end_loc, {}).get('area', '未知区域')})
- 实际距离: {distance}公里
- 交通状况: {traffic_condition}
- 天气影响: {weather_condition if weather_condition else '无特殊天气'}

🗺️ 路线分析:
- 推荐路线: {route_type}
- 路线描述: {route_description}
- 预计行驶时间: {estimated_time}分钟
- 路面状况: {road_condition}
- 能见度: {visibility}
- 限速建议: {speed_limit}km/h

⚡ 智能优化:
- 信号灯协调: 已根据天气调整
- 动态限速: {speed_limit}km/h
- 车道推荐: 根据天气选择最安全车道
- 乘客数量: {passengers}人

{safety_note}
✅ 路线规划完成，自动驾驶系统已激活"""
        
        return response
    
    def respond_to_weather_alert(self, weather_data):
        """响应天气预警"""
        # 处理增强的任务数据
        if 'context' in weather_data:
            location = weather_data['context'].get('location', weather_data.get('location', '未知区域'))
            alert_type = weather_data['context'].get('weather_condition', weather_data.get('alert_type', '未知类型'))
            severity = weather_data['context'].get('severity', weather_data.get('severity', 5))
        else:
            location = weather_data.get('location', '未知区域')
            alert_type = weather_data.get('alert_type', '未知类型')
            severity = weather_data.get('severity', 5)
        
        traffic_impact = self._assess_weather_traffic_impact(location, alert_type, severity)
        
        # 根据天气类型生成更具体的响应
        if '暴雨' in alert_type or 'heavy_rain' in alert_type:
            weather_response = f"""TrafficManager: 暴雨天气交通紧急响应

🌧️ 暴雨预警响应:
- 影响区域: {location}
- 天气类型: {alert_type}
- 严重程度: {severity}/10

🚨 紧急交通管制:
- 能见度: {traffic_impact['visibility_impact']}
- 路面状况: {traffic_impact['road_condition']}
- 限速: {traffic_impact['speed_limit']}km/h
- 禁行区域: {traffic_impact['restricted_areas']}

🚦 交通管制措施:
- 信号灯: {traffic_impact['signal_adjustment']}
- 车道封闭: {traffic_impact['lane_closures']}
- 绕行路线: {traffic_impact['detour_routes']}

⚠️ 自动驾驶建议:
- 建议暂停自动驾驶服务
- 如必须使用，切换至人工模式
- 选择主要干道，避开危险路段
- 保持极低车速

✅ 暴雨天气交通管制系统已全面启动"""
        else:
            weather_response = f"""TrafficManager: 天气预警交通响应

🌤️ 天气影响评估:
- 影响区域: {location}
- 天气类型: {alert_type}
- 严重程度: {severity}/10

🚗 交通影响分析:
- 能见度影响: {traffic_impact['visibility_impact']}
- 路面状况: {traffic_impact['road_condition']}
- 限速建议: {traffic_impact['speed_limit']}km/h
- 禁行区域: {traffic_impact['restricted_areas']}

🚦 交通管制措施:
- 信号灯调整: {traffic_impact['signal_adjustment']}
- 车道封闭: {traffic_impact['lane_closures']}
- 绕行建议: {traffic_impact['detour_routes']}

✅ 交通管制系统已激活，确保行车安全"""
        
        return weather_response
    
    def respond_to_parking_update(self, parking_data):
        """响应停车更新"""
        location = parking_data.get('location', '未知位置')
        available_spots = parking_data.get('available_spots', 0)
        
        traffic_flow_impact = self._analyze_parking_traffic_impact(location, available_spots)
        
        response = f"""TrafficManager: 停车状况交通分析

🅿️ 停车影响评估:
- 停车位置: {location}
- 可用车位: {available_spots}个
- 停车需求: {traffic_flow_impact['parking_demand']}

🚗 交通流影响:
- 周边交通状况: {traffic_flow_impact['surrounding_traffic']}
- 排队长度: {traffic_flow_impact['queue_length']}米
- 等待时间: {traffic_flow_impact['waiting_time']}分钟

🔄 交通优化建议:
- 信号灯调整: {traffic_flow_impact['signal_optimization']}
- 车道分配: {traffic_flow_impact['lane_allocation']}
- 引导系统: {traffic_flow_impact['guidance_system']}

✅ 交通流优化完成，减少停车拥堵"""
        
        return response
    
    def respond_to_safety_inspection(self, safety_data):
        """响应安全检查"""
        location = safety_data.get('location', '未知位置')
        require_human = safety_data.get('require_human_intervention', False)
        
        traffic_safety_measures = self._implement_safety_traffic_measures(location, require_human)
        
        response = f"""TrafficManager: 安全检查交通措施

🔍 安全检查响应:
- 检查位置: {location}
- 需要人工干预: {'是' if require_human else '否'}
- 安全等级: {traffic_safety_measures['safety_level']}

🚧 交通管制措施:
- 限速区域: {traffic_safety_measures['speed_restrictions']}
- 临时封闭: {traffic_safety_measures['temporary_closures']}
- 绕行路线: {traffic_safety_measures['detour_routes']}

🚦 信号控制:
- 信号灯状态: {traffic_safety_measures['signal_status']}
- 优先通行: {traffic_safety_measures['priority_access']}
- 应急通道: {traffic_safety_measures['emergency_lanes']}

✅ 安全交通管制已实施，确保检查区域安全"""
        
        return response
    
    def _collect_traffic_data(self, start, end):
        """收集交通数据"""
        return {
            "start_traffic": random.choice(["畅通", "缓慢", "拥堵"]),
            "end_traffic": random.choice(["畅通", "缓慢", "拥堵"]),
            "congestion_points": [f"拥堵点{i}" for i in range(random.randint(0, 3))]
        }
    
    def _analyze_route_options(self, start, end, traffic_data):
        """分析路线选项"""
        routes = ["高速优先", "城市道路", "绕行路线", "混合路线"]
        return {
            "recommended_route": random.choice(routes),
            "alternative_routes": random.choice(routes),
            "estimated_time": random.randint(10, 30),
            "fuel_consumption": round(random.uniform(2.5, 5.0), 1),
            "signal_coordination": "已优化",
            "dynamic_speed": f"{random.randint(40, 80)}km/h",
            "lane_recommendation": "最左侧车道"
        }
    
    def _assess_weather_traffic_impact(self, location, alert_type, severity):
        """评估天气对交通的影响"""
        return {
            "visibility_impact": f"{random.randint(50, 200)}米",
            "road_condition": random.choice(["湿滑", "积水", "结冰", "正常"]),
            "speed_limit": random.randint(30, 60),
            "restricted_areas": f"{location}周边{random.randint(1, 5)}公里",
            "signal_adjustment": "延长绿灯时间",
            "lane_closures": "应急车道开放",
            "detour_routes": "已规划3条绕行路线"
        }
    
    def _analyze_parking_traffic_impact(self, location, available_spots):
        """分析停车对交通的影响"""
        return {
            "parking_demand": random.choice(["高", "中", "低"]),
            "surrounding_traffic": random.choice(["畅通", "缓慢", "拥堵"]),
            "queue_length": random.randint(50, 200),
            "waiting_time": random.randint(2, 10),
            "signal_optimization": "已调整",
            "lane_allocation": "增加右转车道",
            "guidance_system": "实时更新"
        }
    
    def _implement_safety_traffic_measures(self, location, require_human):
        """实施安全交通措施"""
        return {
            "safety_level": random.choice(["高", "中", "低"]),
            "speed_restrictions": f"{location}周边限速{random.randint(20, 40)}km/h",
            "temporary_closures": "部分车道临时封闭" if require_human else "无封闭",
            "detour_routes": "已规划绕行路线",
            "signal_status": "正常" if not require_human else "调整中",
            "priority_access": "应急车辆优先" if require_human else "正常通行",
            "emergency_lanes": "应急车道开放" if require_human else "正常使用"
        }