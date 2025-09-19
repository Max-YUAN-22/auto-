#!/usr/bin/env python3
"""
Real Cache Performance Testing
真实缓存性能测试

This script implements real cache performance testing with actual cache implementations.
这个脚本实现真实的缓存性能测试。
"""

import asyncio
import time
import json
import random
import numpy as np
import os
from typing import Dict, List, Tuple, Any
import logging
from collections import defaultdict, deque
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RealCachePerformanceTest:
    """Real cache performance testing"""
    
    def __init__(self):
        self.results = {}
        
    def test_lru_cache(self, cache_size: int, access_pattern: str, num_operations: int = 10000):
        """Test LRU cache performance"""
        logger.info(f"Testing LRU cache (size={cache_size}, pattern={access_pattern})")
        
        # 实现真实的LRU缓存
        class LRUCache:
            def __init__(self, capacity):
                self.capacity = capacity
                self.cache = {}
                self.access_order = deque()
            
            def get(self, key):
                if key in self.cache:
                    # 移动到末尾
                    self.access_order.remove(key)
                    self.access_order.append(key)
                    return self.cache[key]
                return None
            
            def put(self, key, value):
                if key in self.cache:
                    self.cache[key] = value
                    self.access_order.remove(key)
                    self.access_order.append(key)
                else:
                    if len(self.cache) >= self.capacity:
                        # 移除最久未使用的
                        oldest = self.access_order.popleft()
                        del self.cache[oldest]
                    self.cache[key] = value
                    self.access_order.append(key)
        
        cache = LRUCache(cache_size)
        hits = 0
        misses = 0
        total_latency = 0
        
        # 生成访问模式
        if access_pattern == 'sequential':
            keys = list(range(num_operations))
        elif access_pattern == 'random':
            keys = [random.randint(0, cache_size * 2) for _ in range(num_operations)]
        elif access_pattern == 'repeated':
            keys = [random.randint(0, cache_size // 2) for _ in range(num_operations)]
        else:
            keys = list(range(num_operations))
        
        # 执行缓存操作
        for i, key in enumerate(keys):
            start_time = time.time()
            
            # 尝试获取
            result = cache.get(key)
            if result is None:
                # 缓存未命中，添加数据
                cache.put(key, f"data_{key}")
                misses += 1
            else:
                hits += 1
            
            end_time = time.time()
            total_latency += (end_time - start_time)
        
        hit_rate = hits / (hits + misses)
        avg_latency = total_latency / num_operations
        
        return {
            'cache_type': 'LRU',
            'cache_size': cache_size,
            'access_pattern': access_pattern,
            'hit_rate': hit_rate,
            'avg_latency': avg_latency,
            'hits': hits,
            'misses': misses,
            'total_operations': num_operations
        }
    
    def test_lfu_cache(self, cache_size: int, access_pattern: str, num_operations: int = 10000):
        """Test LFU cache performance"""
        logger.info(f"Testing LFU cache (size={cache_size}, pattern={access_pattern})")
        
        # 实现真实的LFU缓存
        class LFUCache:
            def __init__(self, capacity):
                self.capacity = capacity
                self.cache = {}
                self.freq = defaultdict(int)
                self.freq_keys = defaultdict(list)
                self.min_freq = 0
            
            def get(self, key):
                if key in self.cache:
                    # 更新频率
                    freq = self.freq[key]
                    self.freq[key] += 1
                    self.freq_keys[freq].remove(key)
                    self.freq_keys[freq + 1].append(key)
                    
                    if not self.freq_keys[freq] and freq == self.min_freq:
                        self.min_freq += 1
                    
                    return self.cache[key]
                return None
            
            def put(self, key, value):
                if key in self.cache:
                    self.cache[key] = value
                    self.get(key)  # 更新频率
                else:
                    if len(self.cache) >= self.capacity:
                        # 移除频率最低的
                        key_to_remove = self.freq_keys[self.min_freq].pop(0)
                        del self.cache[key_to_remove]
                        del self.freq[key_to_remove]
                    
                    self.cache[key] = value
                    self.freq[key] = 1
                    self.freq_keys[1].append(key)
                    self.min_freq = 1
        
        cache = LFUCache(cache_size)
        hits = 0
        misses = 0
        total_latency = 0
        
        # 生成访问模式
        if access_pattern == 'sequential':
            keys = list(range(num_operations))
        elif access_pattern == 'random':
            keys = [random.randint(0, cache_size * 2) for _ in range(num_operations)]
        elif access_pattern == 'repeated':
            keys = [random.randint(0, cache_size // 2) for _ in range(num_operations)]
        else:
            keys = list(range(num_operations))
        
        # 执行缓存操作
        for i, key in enumerate(keys):
            start_time = time.time()
            
            # 尝试获取
            result = cache.get(key)
            if result is None:
                # 缓存未命中，添加数据
                cache.put(key, f"data_{key}")
                misses += 1
            else:
                hits += 1
            
            end_time = time.time()
            total_latency += (end_time - start_time)
        
        hit_rate = hits / (hits + misses)
        avg_latency = total_latency / num_operations
        
        return {
            'cache_type': 'LFU',
            'cache_size': cache_size,
            'access_pattern': access_pattern,
            'hit_rate': hit_rate,
            'avg_latency': avg_latency,
            'hits': hits,
            'misses': misses,
            'total_operations': num_operations
        }
    
    def test_our_hcmpl_cache(self, cache_size: int, access_pattern: str, num_operations: int = 10000):
        """Test our HCMPL cache performance"""
        logger.info(f"Testing HCMPL cache (size={cache_size}, pattern={access_pattern})")
        
        # 实现我们的HCMPL缓存
        class HCMPLCache:
            def __init__(self, capacity):
                self.capacity = capacity
                self.cache = {}
                self.access_history = deque(maxlen=1000)  # 保存访问历史
                self.pattern_weights = defaultdict(float)
                self.min_freq = 0
                self.freq = defaultdict(int)
                self.freq_keys = defaultdict(list)
            
            def _update_pattern_weights(self, key):
                """更新模式权重"""
                if len(self.access_history) > 10:
                    # 分析访问模式
                    recent_keys = list(self.access_history)[-10:]
                    if key in recent_keys:
                        self.pattern_weights[key] += 0.1
            
            def get(self, key):
                if key in self.cache:
                    # 更新频率和模式权重
                    freq = self.freq[key]
                    self.freq[key] += 1
                    self.freq_keys[freq].remove(key)
                    self.freq_keys[freq + 1].append(key)
                    
                    if not self.freq_keys[freq] and freq == self.min_freq:
                        self.min_freq += 1
                    
                    self.access_history.append(key)
                    self._update_pattern_weights(key)
                    
                    return self.cache[key]
                return None
            
            def put(self, key, value):
                if key in self.cache:
                    self.cache[key] = value
                    self.get(key)  # 更新频率
                else:
                    if len(self.cache) >= self.capacity:
                        # 智能替换：考虑频率和模式权重
                        if self.min_freq in self.freq_keys and self.freq_keys[self.min_freq]:
                            # 选择频率最低且模式权重最低的
                            candidates = self.freq_keys[self.min_freq]
                            key_to_remove = min(candidates, key=lambda k: self.pattern_weights[k])
                            self.freq_keys[self.min_freq].remove(key_to_remove)
                        else:
                            key_to_remove = self.freq_keys[self.min_freq].pop(0)
                        
                        del self.cache[key_to_remove]
                        del self.freq[key_to_remove]
                        if key_to_remove in self.pattern_weights:
                            del self.pattern_weights[key_to_remove]
                    
                    self.cache[key] = value
                    self.freq[key] = 1
                    self.freq_keys[1].append(key)
                    self.min_freq = 1
                    self.access_history.append(key)
                    self._update_pattern_weights(key)
        
        cache = HCMPLCache(cache_size)
        hits = 0
        misses = 0
        total_latency = 0
        
        # 生成访问模式
        if access_pattern == 'sequential':
            keys = list(range(num_operations))
        elif access_pattern == 'random':
            keys = [random.randint(0, cache_size * 2) for _ in range(num_operations)]
        elif access_pattern == 'repeated':
            keys = [random.randint(0, cache_size // 2) for _ in range(num_operations)]
        else:
            keys = list(range(num_operations))
        
        # 执行缓存操作
        for i, key in enumerate(keys):
            start_time = time.time()
            
            # 尝试获取
            result = cache.get(key)
            if result is None:
                # 缓存未命中，添加数据
                cache.put(key, f"data_{key}")
                misses += 1
            else:
                hits += 1
            
            end_time = time.time()
            total_latency += (end_time - start_time)
        
        hit_rate = hits / (hits + misses)
        avg_latency = total_latency / num_operations
        
        return {
            'cache_type': 'HCMPL',
            'cache_size': cache_size,
            'access_pattern': access_pattern,
            'hit_rate': hit_rate,
            'avg_latency': avg_latency,
            'hits': hits,
            'misses': misses,
            'total_operations': num_operations
        }
    
    def run_cache_performance_test(self):
        """Run complete cache performance test"""
        logger.info("Starting real cache performance testing...")
        
        cache_sizes = [100, 500, 1000, 5000]
        access_patterns = ['sequential', 'random', 'repeated']
        cache_types = ['LRU', 'LFU', 'HCMPL']
        
        results = []
        
        for cache_size in cache_sizes:
            for pattern in access_patterns:
                for cache_type in cache_types:
                    if cache_type == 'LRU':
                        result = self.test_lru_cache(cache_size, pattern)
                    elif cache_type == 'LFU':
                        result = self.test_lfu_cache(cache_size, pattern)
                    elif cache_type == 'HCMPL':
                        result = self.test_our_hcmpl_cache(cache_size, pattern)
                    
                    results.append(result)
                    logger.info(f"Completed {cache_type} {cache_size} {pattern}: {result['hit_rate']:.3f} hit rate")
        
        # 保存结果
        self.results = {
            'cache_performance': results,
            'test_config': {
                'cache_sizes': cache_sizes,
                'access_patterns': access_patterns,
                'cache_types': cache_types,
                'timestamp': time.time()
            }
        }
        
        # 保存到文件
        os.makedirs('results', exist_ok=True)
        with open('results/real_cache_performance.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        logger.info("Real cache performance testing completed!")
        return results
    
    def generate_cache_performance_chart(self):
        """Generate cache performance comparison chart"""
        logger.info("Generating cache performance chart...")
        
        # 组织数据
        cache_data = {}
        for result in self.results['cache_performance']:
            cache_type = result['cache_type']
            pattern = result['access_pattern']
            size = result['cache_size']
            
            if cache_type not in cache_data:
                cache_data[cache_type] = {}
            if pattern not in cache_data[cache_type]:
                cache_data[cache_type][pattern] = {}
            
            cache_data[cache_type][pattern][size] = result['hit_rate']
        
        # 创建图表
        patterns = ['sequential', 'random', 'repeated']
        cache_types = ['LRU', 'LFU', 'HCMPL']
        sizes = [100, 500, 1000, 5000]
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        for i, pattern in enumerate(patterns):
            ax = axes[i]
            
            for cache_type in cache_types:
                hit_rates = []
                for size in sizes:
                    if cache_type in cache_data and pattern in cache_data[cache_type] and size in cache_data[cache_type][pattern]:
                        hit_rates.append(cache_data[cache_type][pattern][size])
                    else:
                        hit_rates.append(0)
                
                ax.plot(sizes, hit_rates, 'o-', label=cache_type, linewidth=2, markersize=6)
            
            ax.set_title(f'Cache Hit Rate - {pattern.title()} Pattern', fontsize=14, fontweight='bold')
            ax.set_xlabel('Cache Size', fontsize=12)
            ax.set_ylabel('Hit Rate', fontsize=12)
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.set_ylim(0, 1)
        
        plt.tight_layout()
        plt.savefig('figures/real_cache_performance_comparison.png', dpi=300, bbox_inches='tight')
        plt.savefig('figures/real_cache_performance_comparison.pdf', bbox_inches='tight')
        plt.close()
        
        logger.info("Cache performance chart generated!")
    
    def print_results(self):
        """Print cache performance results"""
        print("\n" + "="*60)
        print("REAL CACHE PERFORMANCE TEST RESULTS")
        print("="*60)
        
        # 按缓存类型分组显示结果
        cache_types = {}
        for result in self.results['cache_performance']:
            cache_type = result['cache_type']
            if cache_type not in cache_types:
                cache_types[cache_type] = []
            cache_types[cache_type].append(result)
        
        for cache_type, results in cache_types.items():
            print(f"\n{cache_type} Cache Performance:")
            print("-" * 40)
            
            for result in results:
                print(f"  Size: {result['cache_size']}, Pattern: {result['access_pattern']}")
                print(f"    Hit Rate: {result['hit_rate']:.3f}")
                print(f"    Avg Latency: {result['avg_latency']*1000:.3f} ms")
                print(f"    Hits: {result['hits']}, Misses: {result['misses']}")

def main():
    """Main function"""
    print("Real Cache Performance Testing")
    print("=" * 40)
    
    # 创建测试器
    tester = RealCachePerformanceTest()
    
    # 运行测试
    results = tester.run_cache_performance_test()
    
    # 生成图表
    tester.generate_cache_performance_chart()
    
    # 打印结果
    tester.print_results()
    
    print(f"\nResults saved to: results/real_cache_performance.json")
    print(f"Chart saved to: figures/real_cache_performance_comparison.png")

if __name__ == "__main__":
    main()
