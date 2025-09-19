#!/usr/bin/env python3
"""
Multi-Agent DSL Framework: Distributed Experiment Platform
多智能体DSL框架：分布式实验平台

This module implements a distributed experiment platform for large-scale testing:
1. Multi-machine deployment using Docker containers
2. Distributed task scheduling and load balancing
3. Network latency and bandwidth testing
4. Distributed caching and learning mechanisms
"""

import asyncio
import time
import json
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Any
import requests
import threading
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor
import psutil
import os
import subprocess
import yaml
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class NodeConfig:
    """Configuration for a distributed node"""
    node_id: str
    host: str
    port: int
    cpu_cores: int
    memory_gb: int
    network_latency_ms: float
    bandwidth_mbps: float
    capabilities: List[str]

@dataclass
class DistributedTask:
    """Task for distributed execution"""
    task_id: str
    complexity: str
    required_capabilities: List[str]
    estimated_duration: float
    priority: int
    deadline: Optional[float] = None
    dependencies: List[str] = None

@dataclass
class DistributedResult:
    """Result from distributed execution"""
    task_id: str
    node_id: str
    result: Any
    execution_time: float
    network_latency: float
    success: bool
    timestamp: float

class DistributedNode:
    """Represents a distributed node in the system"""
    
    def __init__(self, config: NodeConfig):
        self.config = config
        self.current_load = 0.0
        self.max_capacity = 1.0
        self.task_queue = []
        self.completed_tasks = []
        self.performance_history = []
        self.is_active = True
        
    async def execute_task(self, task: DistributedTask) -> DistributedResult:
        """Execute a task on this node"""
        start_time = time.time()
        
        try:
            # Simulate task execution based on complexity
            execution_time = task.estimated_duration
            
            # Add network latency simulation
            network_latency = self.config.network_latency_ms / 1000.0
            await asyncio.sleep(execution_time + network_latency)
            
            # Generate result
            result = {
                'task_id': task.task_id,
                'node_id': self.config.node_id,
                'complexity': task.complexity,
                'execution_time': execution_time,
                'network_latency': network_latency
            }
            
            # Update node state
            self.current_load += execution_time
            self.completed_tasks.append(task.task_id)
            self.performance_history.append(execution_time)
            
            return DistributedResult(
                task_id=task.task_id,
                node_id=self.config.node_id,
                result=result,
                execution_time=execution_time,
                network_latency=network_latency,
                success=True,
                timestamp=time.time()
            )
            
        except Exception as e:
            logger.error(f"Task execution failed on node {self.config.node_id}: {e}")
            return DistributedResult(
                task_id=task.task_id,
                node_id=self.config.node_id,
                result=None,
                execution_time=0.0,
                network_latency=0.0,
                success=False,
                timestamp=time.time()
            )

class DistributedScheduler:
    """Distributed task scheduler with load balancing"""
    
    def __init__(self, nodes: List[DistributedNode]):
        self.nodes = nodes
        self.task_history = []
        self.load_balancing_strategy = "adaptive"
        
    def select_node(self, task: DistributedTask) -> Optional[DistributedNode]:
        """Select the best node for a task"""
        # Filter nodes by capabilities
        capable_nodes = [node for node in self.nodes 
                        if any(cap in node.config.capabilities for cap in task.required_capabilities)]
        
        if not capable_nodes:
            return None
        
        # Select node based on load balancing strategy
        if self.load_balancing_strategy == "round_robin":
            return self._round_robin_selection(capable_nodes)
        elif self.load_balancing_strategy == "least_loaded":
            return self._least_loaded_selection(capable_nodes)
        elif self.load_balancing_strategy == "adaptive":
            return self._adaptive_selection(capable_nodes, task)
        else:
            return capable_nodes[0]
    
    def _round_robin_selection(self, nodes: List[DistributedNode]) -> DistributedNode:
        """Round-robin node selection"""
        # Simple round-robin based on node ID
        node_ids = sorted([node.config.node_id for node in nodes])
        current_index = len(self.task_history) % len(node_ids)
        selected_id = node_ids[current_index]
        return next(node for node in nodes if node.config.node_id == selected_id)
    
    def _least_loaded_selection(self, nodes: List[DistributedNode]) -> DistributedNode:
        """Select the least loaded node"""
        return min(nodes, key=lambda node: node.current_load)
    
    def _adaptive_selection(self, nodes: List[DistributedNode], task: DistributedTask) -> DistributedNode:
        """Adaptive node selection based on multiple factors"""
        best_node = None
        best_score = float('inf')
        
        for node in nodes:
            # Calculate score based on multiple factors
            load_score = node.current_load / node.max_capacity
            capability_score = len(set(task.required_capabilities).intersection(set(node.config.capabilities)))
            performance_score = np.mean(node.performance_history[-10:]) if node.performance_history else 1.0
            network_score = node.config.network_latency_ms / 100.0  # Normalize latency
            
            # Weighted combination
            total_score = (load_score * 0.4 + 
                          (1.0 - capability_score / len(task.required_capabilities)) * 0.3 +
                          performance_score * 0.2 +
                          network_score * 0.1)
            
            if total_score < best_score:
                best_score = total_score
                best_node = node
        
        return best_node
    
    async def schedule_task(self, task: DistributedTask) -> DistributedResult:
        """Schedule a task to the best available node"""
        selected_node = self.select_node(task)
        
        if not selected_node:
            return DistributedResult(
                task_id=task.task_id,
                node_id="none",
                result=None,
                execution_time=0.0,
                network_latency=0.0,
                success=False,
                timestamp=time.time()
            )
        
        # Execute task on selected node
        result = await selected_node.execute_task(task)
        
        # Record task history
        self.task_history.append({
            'task_id': task.task_id,
            'node_id': selected_node.config.node_id,
            'execution_time': result.execution_time,
            'success': result.success,
            'timestamp': result.timestamp
        })
        
        return result

class DistributedCache:
    """Distributed cache with consistency mechanisms"""
    
    def __init__(self, nodes: List[DistributedNode]):
        self.nodes = nodes
        self.cache_data = {}
        self.cache_metadata = {}
        self.consistency_strategy = "eventual"
        
    def get(self, key: str, node_id: str) -> Optional[Any]:
        """Get value from distributed cache"""
        # Check local cache first
        if key in self.cache_data:
            return self.cache_data[key]
        
        # Check other nodes' caches
        for node in self.nodes:
            if node.config.node_id != node_id:
                # Simulate network request to other node
                if key in self.cache_data:  # Simplified for demo
                    return self.cache_data[key]
        
        return None
    
    def put(self, key: str, value: Any, node_id: str):
        """Put value into distributed cache"""
        self.cache_data[key] = value
        self.cache_metadata[key] = {
            'created_by': node_id,
            'timestamp': time.time(),
            'version': 1
        }
        
        # Replicate to other nodes (simplified)
        for node in self.nodes:
            if node.config.node_id != node_id:
                # Simulate replication
                pass
    
    def invalidate(self, key: str):
        """Invalidate cache entry across all nodes"""
        if key in self.cache_data:
            del self.cache_data[key]
        if key in self.cache_metadata:
            del self.cache_metadata[key]

class DistributedLearning:
    """Distributed learning with knowledge sharing"""
    
    def __init__(self, nodes: List[DistributedNode]):
        self.nodes = nodes
        self.knowledge_base = {}
        self.learning_history = {}
        
    def update_knowledge(self, node_id: str, key: str, value: float):
        """Update knowledge base for a node"""
        if node_id not in self.knowledge_base:
            self.knowledge_base[node_id] = {}
        
        self.knowledge_base[node_id][key] = value
        
        # Record learning history
        if key not in self.learning_history:
            self.learning_history[key] = []
        
        self.learning_history[key].append({
            'node_id': node_id,
            'value': value,
            'timestamp': time.time()
        })
    
    def share_knowledge(self, source_node_id: str, target_node_id: str, key: str):
        """Share knowledge between nodes"""
        if (source_node_id in self.knowledge_base and 
            key in self.knowledge_base[source_node_id]):
            
            source_value = self.knowledge_base[source_node_id][key]
            
            if target_node_id not in self.knowledge_base:
                self.knowledge_base[target_node_id] = {}
            
            # Transfer knowledge with learning rate
            learning_rate = 0.1
            if key in self.knowledge_base[target_node_id]:
                current_value = self.knowledge_base[target_node_id][key]
                new_value = (1 - learning_rate) * current_value + learning_rate * source_value
            else:
                new_value = learning_rate * source_value
            
            self.knowledge_base[target_node_id][key] = new_value
    
    def get_knowledge(self, node_id: str, key: str) -> float:
        """Get knowledge value for a node"""
        if node_id in self.knowledge_base and key in self.knowledge_base[node_id]:
            return self.knowledge_base[node_id][key]
        return 0.0

class DistributedExperimentPlatform:
    """Main distributed experiment platform"""
    
    def __init__(self, nodes: List[DistributedNode]):
        self.nodes = nodes
        self.scheduler = DistributedScheduler(nodes)
        self.cache = DistributedCache(nodes)
        self.learning = DistributedLearning(nodes)
        
        # Performance metrics
        self.metrics = {
            'total_tasks': 0,
            'completed_tasks': 0,
            'failed_tasks': 0,
            'average_execution_time': 0.0,
            'average_network_latency': 0.0,
            'cache_hit_rate': 0.0,
            'load_balance_variance': 0.0
        }
    
    async def run_distributed_experiment(self, tasks: List[DistributedTask]) -> List[DistributedResult]:
        """Run a distributed experiment with multiple tasks"""
        logger.info(f"Starting distributed experiment with {len(tasks)} tasks across {len(self.nodes)} nodes")
        
        results = []
        
        # Process tasks concurrently
        semaphore = asyncio.Semaphore(len(self.nodes))  # Limit concurrent tasks
        
        async def process_task(task: DistributedTask):
            async with semaphore:
                # Check cache first
                cache_key = f"task_{task.task_id}_{task.complexity}"
                cached_result = self.cache.get(cache_key, "scheduler")
                
                if cached_result:
                    self.metrics['cache_hit_rate'] += 1
                    return DistributedResult(
                        task_id=task.task_id,
                        node_id="cache",
                        result=cached_result,
                        execution_time=0.001,
                        network_latency=0.0,
                        success=True,
                        timestamp=time.time()
                    )
                
                # Schedule and execute task
                result = await self.scheduler.schedule_task(task)
                
                # Cache result
                if result.success:
                    self.cache.put(cache_key, result.result, result.node_id)
                
                # Update learning
                if result.success:
                    knowledge_key = f"{task.complexity}_{len(task.required_capabilities)}"
                    performance = 1.0 / result.execution_time if result.execution_time > 0 else 1.0
                    self.learning.update_knowledge(result.node_id, knowledge_key, performance)
                
                return result
        
        # Execute all tasks
        tasks_coroutines = [process_task(task) for task in tasks]
        results = await asyncio.gather(*tasks_coroutines)
        
        # Update metrics
        self.update_metrics(results)
        
        return results
    
    def update_metrics(self, results: List[DistributedResult]):
        """Update performance metrics"""
        self.metrics['total_tasks'] = len(results)
        self.metrics['completed_tasks'] = sum(1 for r in results if r.success)
        self.metrics['failed_tasks'] = sum(1 for r in results if not r.success)
        
        if results:
            self.metrics['average_execution_time'] = np.mean([r.execution_time for r in results])
            self.metrics['average_network_latency'] = np.mean([r.network_latency for r in results])
        
        # Calculate load balance variance
        node_loads = [node.current_load for node in self.nodes]
        if node_loads:
            self.metrics['load_balance_variance'] = np.var(node_loads)
        
        # Calculate cache hit rate
        if self.metrics['total_tasks'] > 0:
            self.metrics['cache_hit_rate'] = self.metrics['cache_hit_rate'] / self.metrics['total_tasks']
    
    def get_system_performance(self) -> Dict[str, Any]:
        """Get comprehensive system performance metrics"""
        return {
            'metrics': self.metrics,
            'node_status': [
                {
                    'node_id': node.config.node_id,
                    'current_load': node.current_load,
                    'completed_tasks': len(node.completed_tasks),
                    'average_performance': np.mean(node.performance_history) if node.performance_history else 0.0
                }
                for node in self.nodes
            ],
            'cache_status': {
                'total_entries': len(self.cache.cache_data),
                'hit_rate': self.metrics['cache_hit_rate']
            },
            'learning_status': {
                'total_knowledge_entries': sum(len(kb) for kb in self.learning.knowledge_base.values()),
                'learning_events': len(self.learning.learning_history)
            }
        }

def create_docker_compose_config(nodes: List[NodeConfig]) -> str:
    """Create Docker Compose configuration for distributed deployment"""
    services = {}
    
    for node in nodes:
        services[f"node_{node.node_id}"] = {
            'image': 'python:3.9-slim',
            'container_name': f"dsl_node_{node.node_id}",
            'ports': [f"{node.port}:{node.port}"],
            'environment': [
                f"NODE_ID={node.node_id}",
                f"NODE_HOST={node.host}",
                f"NODE_PORT={node.port}",
                f"CPU_CORES={node.cpu_cores}",
                f"MEMORY_GB={node.memory_gb}",
                f"NETWORK_LATENCY_MS={node.network_latency_ms}",
                f"BANDWIDTH_MBPS={node.bandwidth_mbps}",
                f"CAPABILITIES={','.join(node.capabilities)}"
            ],
            'volumes': [
                './:/app'
            ],
            'working_dir': '/app',
            'command': f'python3 scripts/distributed_node.py --node-id {node.node_id} --port {node.port}',
            'networks': ['dsl_network']
        }
    
    config = {
        'version': '3.8',
        'services': services,
        'networks': {
            'dsl_network': {
                'driver': 'bridge'
            }
        }
    }
    
    return yaml.dump(config, default_flow_style=False)

def generate_test_tasks(count: int, complexities: List[str]) -> List[DistributedTask]:
    """Generate test tasks for distributed experiments"""
    tasks = []
    capabilities_pool = [
        ["traffic", "safety"],
        ["weather", "parking"],
        ["traffic", "weather"],
        ["safety", "parking"],
        ["traffic", "safety", "weather"],
        ["weather", "parking", "safety"]
    ]
    
    for i in range(count):
        complexity = np.random.choice(complexities)
        capabilities = np.random.choice(capabilities_pool)
        
        # Estimate duration based on complexity
        duration_map = {
            'simple': 0.1,
            'medium': 0.2,
            'complex': 0.3,
            'very_complex': 0.5
        }
        
        task = DistributedTask(
            task_id=f"task_{i}",
            complexity=complexity,
            required_capabilities=capabilities,
            estimated_duration=duration_map[complexity],
            priority=np.random.randint(1, 5),
            deadline=time.time() + 3600  # 1 hour deadline
        )
        tasks.append(task)
    
    return tasks

async def main():
    """Main function to run distributed experiments"""
    logger.info("Starting distributed experiment platform")
    
    # Create distributed nodes
    nodes_config = [
        NodeConfig(
            node_id="node_1",
            host="localhost",
            port=8001,
            cpu_cores=4,
            memory_gb=8,
            network_latency_ms=10.0,
            bandwidth_mbps=1000.0,
            capabilities=["traffic", "safety"]
        ),
        NodeConfig(
            node_id="node_2",
            host="localhost",
            port=8002,
            cpu_cores=4,
            memory_gb=8,
            network_latency_ms=15.0,
            bandwidth_mbps=800.0,
            capabilities=["weather", "parking"]
        ),
        NodeConfig(
            node_id="node_3",
            host="localhost",
            port=8003,
            cpu_cores=4,
            memory_gb=8,
            network_latency_ms=20.0,
            bandwidth_mbps=600.0,
            capabilities=["traffic", "weather"]
        ),
        NodeConfig(
            node_id="node_4",
            host="localhost",
            port=8004,
            cpu_cores=4,
            memory_gb=8,
            network_latency_ms=25.0,
            bandwidth_mbps=400.0,
            capabilities=["safety", "parking"]
        )
    ]
    
    # Create distributed nodes
    nodes = [DistributedNode(config) for config in nodes_config]
    
    # Create distributed platform
    platform = DistributedExperimentPlatform(nodes)
    
    # Generate test tasks
    tasks = generate_test_tasks(100, ['simple', 'medium', 'complex', 'very_complex'])
    
    # Run distributed experiment
    results = await platform.run_distributed_experiment(tasks)
    
    # Get performance metrics
    performance = platform.get_system_performance()
    
    # Save results
    os.makedirs("results/distributed", exist_ok=True)
    
    with open("results/distributed/distributed_experiment_results.json", "w") as f:
        json.dump({
            'results': [asdict(r) for r in results],
            'performance': performance
        }, f, indent=2, default=str)
    
    # Create Docker Compose configuration
    docker_config = create_docker_compose_config(nodes_config)
    with open("docker-compose.distributed.yml", "w") as f:
        f.write(docker_config)
    
    logger.info("Distributed experiment completed!")
    logger.info(f"Results saved to results/distributed/")
    logger.info(f"Docker Compose config saved to docker-compose.distributed.yml")
    
    return results

if __name__ == "__main__":
    asyncio.run(main())
