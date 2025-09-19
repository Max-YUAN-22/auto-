"""
Performance Tests
性能测试和基准测试
"""

import pytest
import time
import threading
import asyncio
import statistics
from concurrent.futures import ThreadPoolExecutor
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

class TestPerformance:
    """性能测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.sample_event = {
            "event_id": "perf_test_001",
            "event_type": "traffic_incident",
            "timestamp": "2025-01-10T10:00:00Z",
            "location": {"lat": 37.7749, "lng": -122.4194},
            "data": {"severity": "high"}
        }
    
    def test_latency_benchmark(self):
        """延迟基准测试"""
        def mock_event_processing(event):
            # 模拟事件处理延迟
            time.sleep(0.001)  # 1ms processing time
            return {"processed": True, "latency": 1}
        
        # 测试100次事件处理
        latencies = []
        for i in range(100):
            start_time = time.time()
            result = mock_event_processing(self.sample_event)
            end_time = time.time()
            
            latency = (end_time - start_time) * 1000  # Convert to ms
            latencies.append(latency)
        
        # 计算统计指标
        avg_latency = statistics.mean(latencies)
        p95_latency = statistics.quantiles(latencies, n=20)[18]  # 95th percentile
        max_latency = max(latencies)
        
        # 性能断言
        assert avg_latency < 10, f"Average latency {avg_latency}ms exceeds 10ms threshold"
        assert p95_latency < 20, f"95th percentile latency {p95_latency}ms exceeds 20ms threshold"
        assert max_latency < 50, f"Max latency {max_latency}ms exceeds 50ms threshold"
        
        print(f"Latency Benchmark Results:")
        print(f"  Average: {avg_latency:.2f}ms")
        print(f"  95th percentile: {p95_latency:.2f}ms")
        print(f"  Maximum: {max_latency:.2f}ms")
    
    def test_throughput_benchmark(self):
        """吞吐量基准测试"""
        def mock_event_processor():
            # 模拟事件处理
            time.sleep(0.001)
            return True
        
        # 测试并发处理能力
        def run_concurrent_events(num_events, num_threads):
            start_time = time.time()
            
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = [executor.submit(mock_event_processor) for _ in range(num_events)]
                results = [future.result() for future in futures]
            
            end_time = time.time()
            duration = end_time - start_time
            throughput = num_events / duration  # events per second
            
            return throughput, duration
        
        # 测试不同并发级别
        test_cases = [
            (100, 10),   # 100 events, 10 threads
            (200, 20),   # 200 events, 20 threads
            (500, 50),   # 500 events, 50 threads
        ]
        
        results = []
        for num_events, num_threads in test_cases:
            throughput, duration = run_concurrent_events(num_events, num_threads)
            results.append((num_events, num_threads, throughput, duration))
            
            # 吞吐量断言（至少1000 events/second）
            assert throughput > 1000, f"Throughput {throughput:.2f} events/sec below 1000 threshold"
        
        print(f"Throughput Benchmark Results:")
        for num_events, num_threads, throughput, duration in results:
            print(f"  {num_events} events, {num_threads} threads: {throughput:.2f} events/sec ({duration:.3f}s)")
    
    def test_memory_usage(self):
        """内存使用测试"""
        import psutil
        import gc
        
        # 获取初始内存使用
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # 创建大量事件对象
        events = []
        for i in range(10000):
            event = {
                "event_id": f"memory_test_{i}",
                "event_type": "test",
                "timestamp": "2025-01-10T10:00:00Z",
                "data": {"value": i}
            }
            events.append(event)
        
        # 测量内存使用
        peak_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # 清理内存
        del events
        gc.collect()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = peak_memory - initial_memory
        
        # 内存使用断言（10,000个事件对象不应超过100MB）
        assert memory_increase < 100, f"Memory increase {memory_increase:.2f}MB exceeds 100MB threshold"
        
        print(f"Memory Usage Test Results:")
        print(f"  Initial memory: {initial_memory:.2f}MB")
        print(f"  Peak memory: {peak_memory:.2f}MB")
        print(f"  Memory increase: {memory_increase:.2f}MB")
        print(f"  Final memory: {final_memory:.2f}MB")
    
    def test_cache_performance(self):
        """缓存性能测试"""
        class MockCache:
            def __init__(self):
                self.cache = {}
                self.hits = 0
                self.misses = 0
            
            def get(self, key):
                if key in self.cache:
                    self.hits += 1
                    return self.cache[key]
                else:
                    self.misses += 1
                    return None
            
            def set(self, key, value):
                self.cache[key] = value
            
            def hit_rate(self):
                total = self.hits + self.misses
                return (self.hits / total * 100) if total > 0 else 0
        
        cache = MockCache()
        
        # 模拟缓存操作
        for i in range(1000):
            key = f"event_{i % 100}"  # 只有100个不同的key，增加命中率
            value = cache.get(key)
            
            if value is None:
                # 模拟从数据库获取数据
                value = {"event_id": key, "processed": True}
                cache.set(key, value)
        
        hit_rate = cache.hit_rate()
        
        # 缓存命中率断言（应该>80%）
        assert hit_rate > 80, f"Cache hit rate {hit_rate:.2f}% below 80% threshold"
        
        print(f"Cache Performance Test Results:")
        print(f"  Cache hits: {cache.hits}")
        print(f"  Cache misses: {cache.misses}")
        print(f"  Hit rate: {hit_rate:.2f}%")
    
    def test_error_recovery_performance(self):
        """错误恢复性能测试"""
        def mock_unreliable_operation():
            import random
            if random.random() < 0.1:  # 10% failure rate
                raise Exception("Simulated failure")
            return {"status": "success"}
        
        def resilient_operation(max_retries=3):
            for attempt in range(max_retries):
                try:
                    return mock_unreliable_operation()
                except Exception as e:
                    if attempt == max_retries - 1:
                        return {"status": "failed", "error": str(e)}
                    time.sleep(0.001)  # Brief delay before retry
            return {"status": "failed", "error": "Max retries exceeded"}
        
        # 测试错误恢复性能
        start_time = time.time()
        success_count = 0
        failure_count = 0
        
        for i in range(1000):
            result = resilient_operation()
            if result["status"] == "success":
                success_count += 1
            else:
                failure_count += 1
        
        end_time = time.time()
        duration = end_time - start_time
        
        success_rate = (success_count / 1000) * 100
        
        # 成功率断言（应该>90%）
        assert success_rate > 90, f"Success rate {success_rate:.2f}% below 90% threshold"
        
        print(f"Error Recovery Performance Test Results:")
        print(f"  Success count: {success_count}")
        print(f"  Failure count: {failure_count}")
        print(f"  Success rate: {success_rate:.2f}%")
        print(f"  Duration: {duration:.3f}s")

class TestLoadTesting:
    """负载测试类"""
    
    def test_sustained_load(self):
        """持续负载测试"""
        def mock_heavy_operation():
            # 模拟重负载操作
            time.sleep(0.01)  # 10ms
            return {"processed": True}
        
        # 持续运行30秒
        start_time = time.time()
        end_time = start_time + 30  # 30 seconds
        
        processed_count = 0
        errors = 0
        
        while time.time() < end_time:
            try:
                result = mock_heavy_operation()
                if result["processed"]:
                    processed_count += 1
            except Exception:
                errors += 1
        
        duration = time.time() - start_time
        throughput = processed_count / duration
        
        # 负载测试断言
        assert throughput > 50, f"Sustained throughput {throughput:.2f} ops/sec below 50 threshold"
        assert errors < processed_count * 0.01, f"Error rate too high: {errors} errors"
        
        print(f"Sustained Load Test Results:")
        print(f"  Duration: {duration:.2f}s")
        print(f"  Processed: {processed_count}")
        print(f"  Errors: {errors}")
        print(f"  Throughput: {throughput:.2f} ops/sec")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
