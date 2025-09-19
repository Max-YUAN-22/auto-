"""
Backend API Tests
测试后端API的功能和性能
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from main import app
from data_models import Event, AgentStatus, SystemMetrics

class TestBackendAPI:
    """Backend API测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.client = TestClient(app)
        self.sample_event = {
            "event_id": "test_001",
            "event_type": "traffic_incident",
            "timestamp": "2025-01-10T10:00:00Z",
            "location": {"lat": 37.7749, "lng": -122.4194},
            "data": {"severity": "high", "description": "accident"}
        }
    
    def test_health_check(self):
        """测试健康检查端点"""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_event_submission(self):
        """测试事件提交"""
        response = self.client.post("/events", json=self.sample_event)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "accepted"
        assert data["event_id"] == "test_001"
    
    def test_invalid_event_format(self):
        """测试无效事件格式"""
        invalid_event = {"invalid": "data"}
        response = self.client.post("/events", json=invalid_event)
        assert response.status_code == 422  # Validation error
    
    def test_agent_status_endpoint(self):
        """测试智能体状态端点"""
        response = self.client.get("/agents/status")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # 验证智能体状态结构
        if data:
            agent = data[0]
            assert "agent_id" in agent
            assert "status" in agent
            assert "last_activity" in agent
    
    def test_system_metrics_endpoint(self):
        """测试系统指标端点"""
        response = self.client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "latency" in data
        assert "throughput" in data
        assert "cache_hit_rate" in data
        assert isinstance(data["latency"], (int, float))
        assert isinstance(data["throughput"], (int, float))
        assert 0 <= data["cache_hit_rate"] <= 100
    
    def test_websocket_connection(self):
        """测试WebSocket连接"""
        with self.client.websocket_connect("/ws") as websocket:
            # 发送测试消息
            websocket.send_text(json.dumps({
                "type": "ping",
                "data": "test"
            }))
            # 接收响应
            data = websocket.receive_text()
            response = json.loads(data)
            assert response["type"] == "pong"
    
    def test_event_processing_performance(self):
        """测试事件处理性能"""
        import time
        
        start_time = time.time()
        response = self.client.post("/events", json=self.sample_event)
        end_time = time.time()
        
        assert response.status_code == 200
        # 确保响应时间在合理范围内（<100ms）
        assert (end_time - start_time) < 0.1
    
    def test_concurrent_events(self):
        """测试并发事件处理"""
        import threading
        import time
        
        results = []
        errors = []
        
        def send_event(event_id):
            try:
                event = self.sample_event.copy()
                event["event_id"] = f"concurrent_{event_id}"
                response = self.client.post("/events", json=event)
                results.append(response.status_code)
            except Exception as e:
                errors.append(str(e))
        
        # 创建多个线程同时发送事件
        threads = []
        for i in range(10):
            thread = threading.Thread(target=send_event, args=(i,))
            threads.append(thread)
            thread.start()
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
        
        # 验证所有请求都成功
        assert len(errors) == 0
        assert all(status == 200 for status in results)
        assert len(results) == 10

class TestDataModels:
    """数据模型测试类"""
    
    def test_event_model_validation(self):
        """测试事件模型验证"""
        valid_event = Event(
            event_id="test_001",
            event_type="traffic_incident",
            timestamp="2025-01-10T10:00:00Z",
            location={"lat": 37.7749, "lng": -122.4194},
            data={"severity": "high"}
        )
        assert valid_event.event_id == "test_001"
        assert valid_event.event_type == "traffic_incident"
    
    def test_agent_status_model(self):
        """测试智能体状态模型"""
        status = AgentStatus(
            agent_id="traffic_manager",
            status="active",
            last_activity="2025-01-10T10:00:00Z",
            metrics={"processed_events": 100}
        )
        assert status.agent_id == "traffic_manager"
        assert status.status == "active"
    
    def test_system_metrics_model(self):
        """测试系统指标模型"""
        metrics = SystemMetrics(
            latency=67.5,
            throughput=1247,
            cache_hit_rate=85.2,
            active_agents=5
        )
        assert metrics.latency == 67.5
        assert metrics.throughput == 1247
        assert metrics.cache_hit_rate == 85.2

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
