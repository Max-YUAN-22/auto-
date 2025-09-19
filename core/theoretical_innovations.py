#!/usr/bin/env python3
"""
Multi-Agent DSL Framework: Theoretical Innovations Implementation
多智能体DSL框架：理论创新实现

This module implements the novel algorithms proposed in our theoretical innovations:
1. Adaptive Weighted Round-Robin (AW-RR) for dynamic load balancing
2. Pattern-Aware Adaptive Caching (PAAC) for intelligent caching
3. Collaborative Reinforcement Learning (CRL) for agent learning
"""

import asyncio
import time
import numpy as np
import heapq
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict, deque
import logging
from dataclasses import dataclass
from enum import Enum
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TaskComplexity(Enum):
    SIMPLE = 1
    MEDIUM = 2
    COMPLEX = 3
    VERY_COMPLEX = 4

@dataclass
class Task:
    id: str
    complexity: TaskComplexity
    estimated_duration: float
    required_capabilities: List[str]
    priority: int = 1

@dataclass
class Agent:
    id: str
    capabilities: List[str]
    current_load: float = 0.0
    max_capacity: float = 1.0
    performance_history: List[float] = None
    
    def __post_init__(self):
        if self.performance_history is None:
            self.performance_history = []

@dataclass
class CacheItem:
    key: str
    value: Any
    access_count: int = 0
    last_access: float = 0.0
    pattern_score: float = 0.0

class AdaptiveWeightedRoundRobin:
    """
    Novel Algorithm 1: Adaptive Weighted Round-Robin (AW-RR)
    Implements dynamic load balancing with adaptive weights
    """
    
    def __init__(self, agents: List[Agent]):
        self.agents = agents
        self.weights = {agent.id: 1.0 for agent in agents}
        self.load_history = defaultdict(list)
        self.performance_window = 10  # Consider last 10 tasks
        
    def update_weights(self, agent_id: str, performance: float):
        """Update agent weights based on recent performance"""
        # Exponential moving average for weight updates
        alpha = 0.1
        current_weight = self.weights[agent_id]
        self.weights[agent_id] = (1 - alpha) * current_weight + alpha * performance
        
        # Normalize weights to prevent drift
        total_weight = sum(self.weights.values())
        for aid in self.weights:
            self.weights[aid] /= total_weight
    
    def get_current_load(self, agent: Agent) -> float:
        """Get current load of an agent"""
        return agent.current_load / agent.max_capacity
    
    def weighted_selection(self, task: Task) -> Agent:
        """Select agent using weighted round-robin with load consideration"""
        # Filter agents by capabilities
        capable_agents = [a for a in self.agents 
                         if any(cap in a.capabilities for cap in task.required_capabilities)]
        
        if not capable_agents:
            raise ValueError(f"No agent capable of handling task {task.id}")
        
        # Calculate selection scores considering both weight and load
        scores = {}
        for agent in capable_agents:
            load_factor = 1.0 - self.get_current_load(agent)
            weight_factor = self.weights[agent.id]
            scores[agent.id] = weight_factor * load_factor
        
        # Select agent with highest score
        selected_agent_id = max(scores.keys(), key=lambda a: scores[a])
        selected_agent = next(a for a in capable_agents if a.id == selected_agent_id)
        
        # Update agent load
        selected_agent.current_load += task.estimated_duration
        
        return selected_agent
    
    def assign_tasks(self, tasks: List[Task]) -> Dict[str, str]:
        """Assign tasks to agents using AW-RR algorithm"""
        assignments = {}
        
        for task in tasks:
            try:
                selected_agent = self.weighted_selection(task)
                assignments[task.id] = selected_agent.id
                
                # Record assignment for performance tracking
                self.load_history[selected_agent.id].append({
                    'task_id': task.id,
                    'complexity': task.complexity.value,
                    'timestamp': time.time()
                })
                
            except ValueError as e:
                logger.error(f"Failed to assign task {task.id}: {e}")
                continue
        
        return assignments
    
    def update_performance(self, agent_id: str, task_id: str, completion_time: float):
        """Update agent performance based on task completion"""
        # Find the task in history
        task_history = self.load_history[agent_id]
        for record in task_history:
            if record['task_id'] == task_id:
                # Calculate performance score (lower completion time = higher performance)
                expected_time = record['complexity'] * 0.1  # Base time per complexity
                performance = expected_time / completion_time if completion_time > 0 else 0
                
                # Update performance history
                agent = next(a for a in self.agents if a.id == agent_id)
                agent.performance_history.append(performance)
                
                # Keep only recent performance history
                if len(agent.performance_history) > self.performance_window:
                    agent.performance_history.pop(0)
                
                # Update weights based on recent performance
                if agent.performance_history:
                    avg_performance = np.mean(agent.performance_history)
                    self.update_weights(agent_id, avg_performance)
                
                break

class PatternAwareAdaptiveCaching:
    """
    Novel Algorithm 2: Pattern-Aware Adaptive Caching (PAAC)
    Implements intelligent caching with pattern recognition
    """
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.access_patterns = defaultdict(int)
        self.pattern_correlations = defaultdict(dict)
        self.access_history = deque(maxlen=1000)
        
    def analyze_patterns(self) -> Dict[str, float]:
        """Analyze access patterns to identify frequent patterns"""
        pattern_frequency = {}
        
        # Count pattern occurrences
        for pattern in self.access_history:
            pattern_frequency[pattern] = pattern_frequency.get(pattern, 0) + 1
        
        # Normalize frequencies
        total_accesses = len(self.access_history)
        if total_accesses > 0:
            for pattern in pattern_frequency:
                pattern_frequency[pattern] /= total_accesses
        
        return pattern_frequency
    
    def compute_correlations(self) -> Dict[str, Dict[str, float]]:
        """Compute correlations between access patterns"""
        correlations = defaultdict(dict)
        
        # Analyze sequential patterns
        for i in range(len(self.access_history) - 1):
            current = self.access_history[i]
            next_pattern = self.access_history[i + 1]
            
            if current not in correlations:
                correlations[current] = {}
            
            correlations[current][next_pattern] = correlations[current].get(next_pattern, 0) + 1
        
        # Normalize correlations
        for pattern in correlations:
            total = sum(correlations[pattern].values())
            if total > 0:
                for next_pattern in correlations[pattern]:
                    correlations[pattern][next_pattern] /= total
        
        return dict(correlations)
    
    def compute_adaptive_score(self, item: CacheItem, pattern_frequency: Dict[str, float], 
                             pattern_correlations: Dict[str, Dict[str, float]]) -> float:
        """Compute adaptive score for cache eviction"""
        # Base score from access frequency
        frequency_score = pattern_frequency.get(item.key, 0)
        
        # Correlation score from pattern relationships
        correlation_score = 0.0
        if item.key in pattern_correlations:
            correlation_score = sum(pattern_correlations[item.key].values())
        
        # Recency score
        current_time = time.time()
        recency_score = 1.0 / (current_time - item.last_access + 1)
        
        # Combined adaptive score
        adaptive_score = (0.4 * frequency_score + 
                         0.3 * correlation_score + 
                         0.3 * recency_score)
        
        return adaptive_score
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache with pattern tracking"""
        if key in self.cache:
            item = self.cache[key]
            item.access_count += 1
            item.last_access = time.time()
            
            # Record access pattern
            self.access_history.append(key)
            
            return item.value
        
        return None
    
    def put(self, key: str, value: Any) -> None:
        """Put item in cache with adaptive eviction"""
        current_time = time.time()
        
        # If cache is full, evict item with lowest adaptive score
        if len(self.cache) >= self.capacity:
            pattern_frequency = self.analyze_patterns()
            pattern_correlations = self.compute_correlations()
            
            # Find item with lowest adaptive score
            min_score = float('inf')
            evict_key = None
            
            for cache_key, item in self.cache.items():
                score = self.compute_adaptive_score(item, pattern_frequency, pattern_correlations)
                if score < min_score:
                    min_score = score
                    evict_key = cache_key
            
            if evict_key:
                del self.cache[evict_key]
        
        # Add new item
        self.cache[key] = CacheItem(
            key=key,
            value=value,
            access_count=1,
            last_access=current_time,
            pattern_score=0.0
        )
    
    def get_hit_rate(self) -> float:
        """Calculate cache hit rate"""
        if not self.access_history:
            return 0.0
        
        hits = sum(1 for key in self.access_history if key in self.cache)
        return hits / len(self.access_history)

class CollaborativeReinforcementLearning:
    """
    Novel Algorithm 3: Collaborative Reinforcement Learning (CRL)
    Implements collaborative learning between agents
    """
    
    def __init__(self, agents: List[Agent], learning_rate: float = 0.1, 
                 discount_factor: float = 0.9, epsilon: float = 0.1):
        self.agents = agents
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        
        # Initialize Q-tables for each agent
        self.q_tables = {agent.id: defaultdict(float) for agent in agents}
        
        # Knowledge sharing parameters
        self.similarity_threshold = 0.7
        self.knowledge_transfer_rate = 0.1
        
    def compute_similarity(self, agent1: Agent, agent2: Agent) -> float:
        """Compute similarity between two agents based on capabilities"""
        capabilities1 = set(agent1.capabilities)
        capabilities2 = set(agent2.capabilities)
        
        if not capabilities1 or not capabilities2:
            return 0.0
        
        intersection = len(capabilities1.intersection(capabilities2))
        union = len(capabilities1.union(capabilities2))
        
        return intersection / union if union > 0 else 0.0
    
    def get_neighbors(self, agent: Agent) -> List[Agent]:
        """Get neighboring agents for knowledge sharing"""
        neighbors = []
        for other_agent in self.agents:
            if other_agent.id != agent.id:
                similarity = self.compute_similarity(agent, other_agent)
                if similarity >= self.similarity_threshold:
                    neighbors.append(other_agent)
        
        return neighbors
    
    def transfer_knowledge(self, source_agent: Agent, target_agent: Agent, 
                         similarity: float) -> None:
        """Transfer knowledge between agents"""
        source_q = self.q_tables[source_agent.id]
        target_q = self.q_tables[target_agent.id]
        
        # Transfer knowledge based on similarity
        transfer_rate = self.knowledge_transfer_rate * similarity
        
        for state_action, q_value in source_q.items():
            if state_action in target_q:
                # Weighted update
                target_q[state_action] = ((1 - transfer_rate) * target_q[state_action] + 
                                         transfer_rate * q_value)
            else:
                # Direct transfer for new state-action pairs
                target_q[state_action] = transfer_rate * q_value
    
    def update_q_table(self, agent: Agent, state: str, action: str, 
                      reward: float, next_state: str) -> None:
        """Update Q-table for an agent"""
        q_table = self.q_tables[agent.id]
        state_action = (state, action)
        
        # Current Q-value
        current_q = q_table[state_action]
        
        # Next state max Q-value
        next_max_q = 0.0
        if next_state:
            next_actions = self.get_possible_actions(agent, next_state)
            if next_actions:
                next_max_q = max(q_table[(next_state, action)] for action in next_actions)
        
        # Q-learning update
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)
        q_table[state_action] = new_q
        
        # Collaborative learning: share knowledge with neighbors
        neighbors = self.get_neighbors(agent)
        for neighbor in neighbors:
            similarity = self.compute_similarity(agent, neighbor)
            self.transfer_knowledge(agent, neighbor, similarity)
    
    def get_possible_actions(self, agent: Agent, state: str) -> List[str]:
        """Get possible actions for an agent in a given state"""
        # This would be implemented based on the specific domain
        # For now, return basic actions
        return ['execute', 'wait', 'collaborate']
    
    def select_action(self, agent: Agent, state: str) -> str:
        """Select action using epsilon-greedy policy"""
        possible_actions = self.get_possible_actions(agent, state)
        
        if np.random.random() < self.epsilon:
            # Exploration: random action
            return np.random.choice(possible_actions)
        else:
            # Exploitation: best action
            q_table = self.q_tables[agent.id]
            action_values = {action: q_table[(state, action)] for action in possible_actions}
            return max(action_values.keys(), key=lambda a: action_values[a])
    
    def get_performance_improvement(self, agent: Agent) -> float:
        """Calculate performance improvement for an agent"""
        if len(agent.performance_history) < 2:
            return 0.0
        
        recent_performance = np.mean(agent.performance_history[-5:])
        initial_performance = np.mean(agent.performance_history[:5])
        
        if initial_performance > 0:
            return (recent_performance - initial_performance) / initial_performance
        
        return 0.0

class IntegratedSystem:
    """
    Integrated system combining all three novel algorithms
    """
    
    def __init__(self, agents: List[Agent], cache_capacity: int = 1000):
        self.agents = agents
        self.load_balancer = AdaptiveWeightedRoundRobin(agents)
        self.cache = PatternAwareAdaptiveCaching(cache_capacity)
        self.learning_system = CollaborativeReinforcementLearning(agents)
        
        # Performance metrics
        self.metrics = {
            'total_tasks': 0,
            'completed_tasks': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'load_balance_variance': 0.0,
            'average_completion_time': 0.0
        }
    
    async def process_task(self, task: Task) -> Dict[str, Any]:
        """Process a task using the integrated system"""
        self.metrics['total_tasks'] += 1
        
        # Check cache first
        cache_key = f"task_{task.id}_{task.complexity.value}"
        cached_result = self.cache.get(cache_key)
        
        if cached_result:
            self.metrics['cache_hits'] += 1
            return {
                'task_id': task.id,
                'result': cached_result,
                'from_cache': True,
                'completion_time': 0.001  # Minimal time for cache hit
            }
        
        self.metrics['cache_misses'] += 1
        
        # Assign task using load balancer
        assignments = self.load_balancer.assign_tasks([task])
        assigned_agent_id = assignments[task.id]
        assigned_agent = next(a for a in self.agents if a.id == assigned_agent_id)
        
        # Execute task with learning
        start_time = time.time()
        
        # Simulate task execution
        await asyncio.sleep(task.estimated_duration)
        
        completion_time = time.time() - start_time
        
        # Generate result
        result = {
            'task_id': task.id,
            'agent_id': assigned_agent_id,
            'completion_time': completion_time,
            'complexity': task.complexity.value
        }
        
        # Cache the result
        self.cache.put(cache_key, result)
        
        # Update learning system
        reward = 1.0 / completion_time if completion_time > 0 else 1.0
        self.learning_system.update_q_table(
            assigned_agent, 
            f"state_{task.complexity.value}", 
            "execute", 
            reward, 
            "completed"
        )
        
        # Update performance metrics
        self.metrics['completed_tasks'] += 1
        self.update_metrics()
        
        return result
    
    def update_metrics(self):
        """Update system performance metrics"""
        # Calculate load balance variance
        loads = [self.load_balancer.get_current_load(agent) for agent in self.agents]
        if loads:
            self.metrics['load_balance_variance'] = np.var(loads)
        
        # Calculate average completion time
        if self.metrics['completed_tasks'] > 0:
            total_time = sum(agent.performance_history for agent in self.agents if agent.performance_history)
            if total_time:
                self.metrics['average_completion_time'] = np.mean(total_time)
    
    def get_system_performance(self) -> Dict[str, Any]:
        """Get comprehensive system performance metrics"""
        cache_hit_rate = self.cache.get_hit_rate()
        
        # Calculate performance improvements
        performance_improvements = {}
        for agent in self.agents:
            improvement = self.learning_system.get_performance_improvement(agent)
            performance_improvements[agent.id] = improvement
        
        return {
            'cache_hit_rate': cache_hit_rate,
            'load_balance_variance': self.metrics['load_balance_variance'],
            'average_completion_time': self.metrics['average_completion_time'],
            'performance_improvements': performance_improvements,
            'total_tasks': self.metrics['total_tasks'],
            'completed_tasks': self.metrics['completed_tasks']
        }

# Example usage and testing
async def main():
    """Example usage of the integrated system"""
    # Create agents
    agents = [
        Agent(id="agent_1", capabilities=["traffic", "safety"], max_capacity=1.0),
        Agent(id="agent_2", capabilities=["weather", "parking"], max_capacity=1.0),
        Agent(id="agent_3", capabilities=["traffic", "weather"], max_capacity=1.0),
        Agent(id="agent_4", capabilities=["safety", "parking"], max_capacity=1.0)
    ]
    
    # Create integrated system
    system = IntegratedSystem(agents, cache_capacity=100)
    
    # Create test tasks
    tasks = [
        Task(id="task_1", complexity=TaskComplexity.SIMPLE, estimated_duration=0.1, required_capabilities=["traffic"]),
        Task(id="task_2", complexity=TaskComplexity.MEDIUM, estimated_duration=0.2, required_capabilities=["weather"]),
        Task(id="task_3", complexity=TaskComplexity.COMPLEX, estimated_duration=0.3, required_capabilities=["safety"]),
        Task(id="task_4", complexity=TaskComplexity.VERY_COMPLEX, estimated_duration=0.4, required_capabilities=["parking"])
    ]
    
    # Process tasks
    results = []
    for task in tasks:
        result = await system.process_task(task)
        results.append(result)
    
    # Get performance metrics
    performance = system.get_system_performance()
    
    print("System Performance Metrics:")
    print(json.dumps(performance, indent=2))
    
    return results

if __name__ == "__main__":
    asyncio.run(main())
