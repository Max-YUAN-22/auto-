#!/usr/bin/env python3
"""
Multi-Agent DSL Framework: Novel Algorithms for A-Class Publication
多智能体DSL框架：A类发表的新颖算法

This module implements novel algorithms that address key problems in existing multi-agent frameworks:
1. Adaptive Task Scheduling with Load Prediction (ATSLP)
2. Hierarchical Cache Management with Pattern Learning (HCMPL)
3. Collaborative Agent Learning with Knowledge Transfer (CALK)
"""

import asyncio
import time
import numpy as np
import heapq
from typing import Dict, List, Tuple, Optional, Any, Set
from collections import defaultdict, deque
import logging
from dataclasses import dataclass
from enum import Enum
import json
import math
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pickle

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
    deadline: Optional[float] = None
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

@dataclass
class Agent:
    id: str
    capabilities: List[str]
    current_load: float = 0.0
    max_capacity: float = 1.0
    performance_history: List[float] = None
    specialization_score: Dict[str, float] = None
    
    def __post_init__(self):
        if self.performance_history is None:
            self.performance_history = []
        if self.specialization_score is None:
            self.specialization_score = {}

class AdaptiveTaskSchedulingWithLoadPrediction:
    """
    Novel Algorithm 1: Adaptive Task Scheduling with Load Prediction (ATSLP)
    
    This algorithm addresses the key problem of load balancing in multi-agent systems by:
    1. Predicting future load based on historical patterns
    2. Adaptively adjusting scheduling decisions
    3. Considering agent specialization and current workload
    """
    
    def __init__(self, agents: List[Agent], prediction_window: int = 10):
        self.agents = agents
        self.prediction_window = prediction_window
        self.load_history = defaultdict(deque)
        self.task_patterns = defaultdict(list)
        self.agent_specialization = {agent.id: {} for agent in agents}
        
        # Load prediction model parameters
        self.prediction_weights = np.random.random(3)  # [historical, pattern, specialization]
        self.prediction_weights = self.prediction_weights / np.sum(self.prediction_weights)
        
    def update_load_history(self, agent_id: str, load: float):
        """Update load history for an agent"""
        self.load_history[agent_id].append(load)
        if len(self.load_history[agent_id]) > self.prediction_window:
            self.load_history[agent_id].popleft()
    
    def predict_future_load(self, agent_id: str, task: Task) -> float:
        """Predict future load for an agent given a task"""
        # Historical load trend
        historical_loads = list(self.load_history[agent_id])
        if len(historical_loads) >= 3:
            trend = np.polyfit(range(len(historical_loads)), historical_loads, 1)[0]
            historical_prediction = historical_loads[-1] + trend
        else:
            historical_prediction = historical_loads[-1] if historical_loads else 0.0
        
        # Pattern-based prediction
        pattern_key = f"{task.complexity.value}_{len(task.required_capabilities)}"
        if pattern_key in self.task_patterns:
            pattern_loads = self.task_patterns[pattern_key]
            pattern_prediction = np.mean(pattern_loads[-5:]) if pattern_loads else 0.0
        else:
            pattern_prediction = 0.0
        
        # Specialization-based prediction
        agent = next(a for a in self.agents if a.id == agent_id)
        specialization_score = 0.0
        for cap in task.required_capabilities:
            if cap in agent.specialization_score:
                specialization_score += agent.specialization_score[cap]
        specialization_prediction = 1.0 - (specialization_score / len(task.required_capabilities))
        
        # Weighted combination
        predicted_load = (self.prediction_weights[0] * historical_prediction +
                         self.prediction_weights[1] * pattern_prediction +
                         self.prediction_weights[2] * specialization_prediction)
        
        return max(0.0, min(1.0, predicted_load))
    
    def select_optimal_agent(self, task: Task) -> Agent:
        """Select the optimal agent for a task using load prediction"""
        capable_agents = [a for a in self.agents 
                         if any(cap in a.capabilities for cap in task.required_capabilities)]
        
        if not capable_agents:
            raise ValueError(f"No agent capable of handling task {task.id}")
        
        best_agent = None
        best_score = float('inf')
        
        for agent in capable_agents:
            # Predict future load
            predicted_load = self.predict_future_load(agent.id, task)
            
            # Calculate score considering current load, predicted load, and specialization
            specialization_score = 0.0
            for cap in task.required_capabilities:
                if cap in agent.specialization_score:
                    specialization_score += agent.specialization_score[cap]
            
            # Score combines load prediction, specialization, and deadline urgency
            urgency_factor = 1.0
            if task.deadline:
                time_remaining = task.deadline - time.time()
                if time_remaining > 0:
                    urgency_factor = 1.0 / (1.0 + time_remaining / 3600)  # Urgency increases as deadline approaches
            
            score = (predicted_load * 0.4 + 
                    (1.0 - specialization_score / len(task.required_capabilities)) * 0.3 +
                    urgency_factor * 0.3)
            
            if score < best_score:
                best_score = score
                best_agent = agent
        
        return best_agent
    
    def schedule_task(self, task: Task) -> Tuple[Agent, float]:
        """Schedule a task and return the assigned agent and predicted completion time"""
        selected_agent = self.select_optimal_agent(task)
        
        # Update agent load
        selected_agent.current_load += task.estimated_duration
        
        # Update load history
        self.update_load_history(selected_agent.id, selected_agent.current_load)
        
        # Update task patterns
        pattern_key = f"{task.complexity.value}_{len(task.required_capabilities)}"
        self.task_patterns[pattern_key].append(task.estimated_duration)
        if len(self.task_patterns[pattern_key]) > 20:
            self.task_patterns[pattern_key].pop(0)
        
        # Predict completion time
        predicted_completion = task.estimated_duration * (1.0 + selected_agent.current_load)
        
        return selected_agent, predicted_completion
    
    def update_specialization(self, agent_id: str, task: Task, performance: float):
        """Update agent specialization based on task performance"""
        agent = next(a for a in self.agents if a.id == agent_id)
        
        for cap in task.required_capabilities:
            if cap not in agent.specialization_score:
                agent.specialization_score[cap] = 0.5  # Initialize with neutral score
            
            # Update specialization score based on performance
            learning_rate = 0.1
            agent.specialization_score[cap] = (
                (1 - learning_rate) * agent.specialization_score[cap] +
                learning_rate * performance
            )

class HierarchicalCacheManagementWithPatternLearning:
    """
    Novel Algorithm 2: Hierarchical Cache Management with Pattern Learning (HCMPL)
    
    This algorithm addresses the key problem of cache efficiency in multi-agent systems by:
    1. Learning access patterns at multiple levels
    2. Implementing hierarchical cache management
    3. Adaptively adjusting cache policies based on patterns
    """
    
    def __init__(self, capacity: int, hierarchy_levels: int = 3):
        self.capacity = capacity
        self.hierarchy_levels = hierarchy_levels
        self.cache_levels = [{} for _ in range(hierarchy_levels)]
        self.access_patterns = defaultdict(list)
        self.pattern_clusters = {}
        self.cluster_centers = {}
        
        # Pattern learning parameters
        self.pattern_window = 100
        self.cluster_update_frequency = 50
        self.access_count = 0
        
    def extract_pattern_features(self, key: str, context: Dict[str, Any]) -> np.ndarray:
        """Extract features for pattern analysis"""
        features = []
        
        # Key-based features
        features.append(len(key))
        features.append(key.count('_'))
        features.append(hash(key) % 100)  # Normalized hash
        
        # Context-based features
        features.append(context.get('agent_id', 0))
        features.append(context.get('task_complexity', 0))
        features.append(context.get('time_of_day', 0))
        features.append(context.get('day_of_week', 0))
        
        return np.array(features)
    
    def update_pattern_clusters(self):
        """Update pattern clusters using K-means"""
        if len(self.access_patterns) < 10:
            return
        
        # Prepare features for clustering
        features = []
        pattern_keys = []
        
        for pattern_key, accesses in self.access_patterns.items():
            if len(accesses) >= 5:  # Only consider patterns with sufficient data
                # Use recent accesses for clustering
                recent_accesses = accesses[-10:]
                for access in recent_accesses:
                    features.append(self.extract_pattern_features(pattern_key, access))
                    pattern_keys.append(pattern_key)
        
        if len(features) < 10:
            return
        
        # Perform clustering
        features = np.array(features)
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        n_clusters = min(5, len(set(pattern_keys)))
        if n_clusters < 2:
            return
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(features_scaled)
        
        # Update cluster information
        self.cluster_centers = kmeans.cluster_centers_
        self.pattern_clusters = dict(zip(pattern_keys, clusters))
    
    def get_cache_level(self, key: str, context: Dict[str, Any]) -> int:
        """Determine appropriate cache level for a key"""
        if key in self.pattern_clusters:
            cluster_id = self.pattern_clusters[key]
            # Higher levels for more frequently accessed patterns
            return min(self.hierarchy_levels - 1, cluster_id + 1)
        else:
            return 0  # Default to lowest level
    
    def get(self, key: str, context: Dict[str, Any] = None) -> Optional[Any]:
        """Get item from hierarchical cache"""
        if context is None:
            context = {}
        
        # Record access pattern
        self.access_patterns[key].append(context)
        if len(self.access_patterns[key]) > self.pattern_window:
            self.access_patterns[key].pop(0)
        
        self.access_count += 1
        
        # Update clusters periodically
        if self.access_count % self.cluster_update_frequency == 0:
            self.update_pattern_clusters()
        
        # Search through cache levels
        for level in range(self.hierarchy_levels):
            if key in self.cache_levels[level]:
                # Move to higher level if appropriate
                target_level = self.get_cache_level(key, context)
                if target_level > level:
                    value = self.cache_levels[level].pop(key)
                    self.cache_levels[target_level][key] = value
                
                return self.cache_levels[target_level if target_level > level else level][key]
        
        return None
    
    def put(self, key: str, value: Any, context: Dict[str, Any] = None):
        """Put item in hierarchical cache"""
        if context is None:
            context = {}
        
        # Determine appropriate level
        level = self.get_cache_level(key, context)
        
        # Check if we need to evict
        total_items = sum(len(cache) for cache in self.cache_levels)
        if total_items >= self.capacity:
            self.evict_items()
        
        # Store in appropriate level
        self.cache_levels[level][key] = value
    
    def evict_items(self):
        """Evict items from cache using hierarchical policy"""
        # Evict from lowest level first
        for level in range(self.hierarchy_levels):
            if self.cache_levels[level]:
                # Evict least recently used item
                key_to_evict = next(iter(self.cache_levels[level]))
                del self.cache_levels[level][key_to_evict]
                break
    
    def get_hit_rate(self) -> float:
        """Calculate overall cache hit rate"""
        total_accesses = sum(len(accesses) for accesses in self.access_patterns.values())
        if total_accesses == 0:
            return 0.0
        
        hits = 0
        for level in self.cache_levels:
            hits += len(level)
        
        return hits / total_accesses if total_accesses > 0 else 0.0

class CollaborativeAgentLearningWithKnowledgeTransfer:
    """
    Novel Algorithm 3: Collaborative Agent Learning with Knowledge Transfer (CALK)
    
    This algorithm addresses the key problem of agent learning efficiency by:
    1. Enabling knowledge transfer between similar agents
    2. Implementing collaborative learning mechanisms
    3. Adaptively adjusting knowledge transfer based on agent similarity
    """
    
    def __init__(self, agents: List[Agent], learning_rate: float = 0.1, 
                 transfer_threshold: float = 0.7):
        self.agents = agents
        self.learning_rate = learning_rate
        self.transfer_threshold = transfer_threshold
        
        # Knowledge bases for each agent
        self.knowledge_bases = {agent.id: defaultdict(float) for agent in agents}
        
        # Transfer history and success rates
        self.transfer_history = defaultdict(list)
        self.transfer_success_rates = defaultdict(float)
        
        # Similarity matrix
        self.similarity_matrix = self._compute_similarity_matrix()
        
    def _compute_similarity_matrix(self) -> Dict[Tuple[str, str], float]:
        """Compute similarity matrix between agents"""
        similarity_matrix = {}
        
        for i, agent1 in enumerate(self.agents):
            for j, agent2 in enumerate(self.agents):
                if i != j:
                    similarity = self._compute_agent_similarity(agent1, agent2)
                    similarity_matrix[(agent1.id, agent2.id)] = similarity
        
        return similarity_matrix
    
    def _compute_agent_similarity(self, agent1: Agent, agent2: Agent) -> float:
        """Compute similarity between two agents"""
        # Capability similarity
        capabilities1 = set(agent1.capabilities)
        capabilities2 = set(agent2.capabilities)
        
        if not capabilities1 or not capabilities2:
            return 0.0
        
        capability_similarity = len(capabilities1.intersection(capabilities2)) / len(capabilities1.union(capabilities2))
        
        # Performance similarity
        if len(agent1.performance_history) > 0 and len(agent2.performance_history) > 0:
            perf1 = np.mean(agent1.performance_history[-10:])
            perf2 = np.mean(agent2.performance_history[-10:])
            performance_similarity = 1.0 - abs(perf1 - perf2) / max(perf1, perf2, 1.0)
        else:
            performance_similarity = 0.5
        
        # Specialization similarity
        spec1 = agent1.specialization_score
        spec2 = agent2.specialization_score
        
        if spec1 and spec2:
            common_specs = set(spec1.keys()).intersection(set(spec2.keys()))
            if common_specs:
                spec_similarities = [1.0 - abs(spec1[k] - spec2[k]) for k in common_specs]
                specialization_similarity = np.mean(spec_similarities)
            else:
                specialization_similarity = 0.0
        else:
            specialization_similarity = 0.5
        
        # Weighted combination
        total_similarity = (capability_similarity * 0.4 + 
                           performance_similarity * 0.3 + 
                           specialization_similarity * 0.3)
        
        return total_similarity
    
    def get_similar_agents(self, agent_id: str) -> List[Agent]:
        """Get agents similar to the given agent"""
        similar_agents = []
        
        for other_agent in self.agents:
            if other_agent.id != agent_id:
                similarity = self.similarity_matrix.get((agent_id, other_agent.id), 0.0)
                if similarity >= self.transfer_threshold:
                    similar_agents.append(other_agent)
        
        return similar_agents
    
    def transfer_knowledge(self, source_agent_id: str, target_agent_id: str, 
                          knowledge_key: str, transfer_rate: float = 0.1):
        """Transfer knowledge from source to target agent"""
        source_kb = self.knowledge_bases[source_agent_id]
        target_kb = self.knowledge_bases[target_agent_id]
        
        if knowledge_key in source_kb:
            source_value = source_kb[knowledge_key]
            
            if knowledge_key in target_kb:
                # Weighted update
                target_kb[knowledge_key] = ((1 - transfer_rate) * target_kb[knowledge_key] + 
                                           transfer_rate * source_value)
            else:
                # Direct transfer
                target_kb[knowledge_key] = transfer_rate * source_value
            
            # Record transfer
            transfer_key = f"{source_agent_id}->{target_agent_id}:{knowledge_key}"
            self.transfer_history[transfer_key].append({
                'timestamp': time.time(),
                'transfer_rate': transfer_rate,
                'source_value': source_value,
                'target_value': target_kb[knowledge_key]
            })
    
    def update_knowledge(self, agent_id: str, knowledge_key: str, 
                        reward: float, context: Dict[str, Any] = None):
        """Update agent knowledge based on experience"""
        knowledge_base = self.knowledge_bases[agent_id]
        
        # Update own knowledge
        if knowledge_key in knowledge_base:
            knowledge_base[knowledge_key] = ((1 - self.learning_rate) * knowledge_base[knowledge_key] + 
                                           self.learning_rate * reward)
        else:
            knowledge_base[knowledge_key] = reward
        
        # Transfer knowledge to similar agents
        similar_agents = self.get_similar_agents(agent_id)
        for similar_agent in similar_agents:
            similarity = self.similarity_matrix[(agent_id, similar_agent.id)]
            transfer_rate = self.learning_rate * similarity * 0.5  # Reduced transfer rate
            
            self.transfer_knowledge(agent_id, similar_agent.id, knowledge_key, transfer_rate)
    
    def get_knowledge(self, agent_id: str, knowledge_key: str) -> float:
        """Get knowledge value for an agent"""
        return self.knowledge_bases[agent_id].get(knowledge_key, 0.0)
    
    def get_transfer_success_rate(self, source_agent_id: str, target_agent_id: str) -> float:
        """Get success rate of knowledge transfer between agents"""
        transfer_key = f"{source_agent_id}->{target_agent_id}"
        if transfer_key in self.transfer_history:
            transfers = self.transfer_history[transfer_key]
            if len(transfers) > 0:
                # Calculate success rate based on transfer effectiveness
                recent_transfers = transfers[-10:]  # Last 10 transfers
                success_count = sum(1 for t in recent_transfers if t['transfer_rate'] > 0.1)
                return success_count / len(recent_transfers)
        
        return 0.0

class IntegratedNovelSystem:
    """
    Integrated system combining all three novel algorithms
    """
    
    def __init__(self, agents: List[Agent], cache_capacity: int = 1000):
        self.agents = agents
        self.scheduler = AdaptiveTaskSchedulingWithLoadPrediction(agents)
        self.cache = HierarchicalCacheManagementWithPatternLearning(cache_capacity)
        self.learning_system = CollaborativeAgentLearningWithKnowledgeTransfer(agents)
        
        # Performance metrics
        self.metrics = {
            'total_tasks': 0,
            'completed_tasks': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'load_balance_variance': 0.0,
            'average_completion_time': 0.0,
            'knowledge_transfers': 0,
            'prediction_accuracy': 0.0
        }
    
    async def process_task(self, task: Task) -> Dict[str, Any]:
        """Process a task using the integrated novel system"""
        self.metrics['total_tasks'] += 1
        
        # Check cache first
        cache_key = f"task_{task.id}_{task.complexity.value}"
        context = {
            'agent_id': 'unknown',
            'task_complexity': task.complexity.value,
            'time_of_day': time.time() % 86400,
            'day_of_week': int(time.time() // 86400) % 7
        }
        
        cached_result = self.cache.get(cache_key, context)
        
        if cached_result:
            self.metrics['cache_hits'] += 1
            return {
                'task_id': task.id,
                'result': cached_result,
                'from_cache': True,
                'completion_time': 0.001
            }
        
        self.metrics['cache_misses'] += 1
        
        # Schedule task using novel scheduler
        assigned_agent, predicted_completion = self.scheduler.schedule_task(task)
        
        # Execute task with learning
        start_time = time.time()
        
        # Simulate task execution
        await asyncio.sleep(task.estimated_duration)
        
        completion_time = time.time() - start_time
        
        # Calculate performance metrics
        performance = 1.0 / completion_time if completion_time > 0 else 1.0
        
        # Update learning system
        knowledge_key = f"{task.complexity.value}_{len(task.required_capabilities)}"
        self.learning_system.update_knowledge(assigned_agent.id, knowledge_key, performance)
        
        # Update scheduler specialization
        self.scheduler.update_specialization(assigned_agent.id, task, performance)
        
        # Generate result
        result = {
            'task_id': task.id,
            'agent_id': assigned_agent.id,
            'completion_time': completion_time,
            'predicted_completion': predicted_completion,
            'complexity': task.complexity.value,
            'performance': performance
        }
        
        # Cache the result
        self.cache.put(cache_key, result, context)
        
        # Update performance metrics
        self.metrics['completed_tasks'] += 1
        self.update_metrics()
        
        return result
    
    def update_metrics(self):
        """Update system performance metrics"""
        # Calculate load balance variance
        loads = [agent.current_load for agent in self.agents]
        if loads:
            self.metrics['load_balance_variance'] = np.var(loads)
        
        # Calculate average completion time
        if self.metrics['completed_tasks'] > 0:
            total_time = sum(agent.performance_history for agent in self.agents if agent.performance_history)
            if total_time:
                self.metrics['average_completion_time'] = np.mean(total_time)
        
        # Calculate cache hit rate
        self.metrics['cache_hit_rate'] = self.cache.get_hit_rate()
        
        # Count knowledge transfers
        self.metrics['knowledge_transfers'] = sum(len(transfers) for transfers in self.learning_system.transfer_history.values())
    
    def get_system_performance(self) -> Dict[str, Any]:
        """Get comprehensive system performance metrics"""
        return {
            'cache_hit_rate': self.metrics['cache_hit_rate'],
            'load_balance_variance': self.metrics['load_balance_variance'],
            'average_completion_time': self.metrics['average_completion_time'],
            'knowledge_transfers': self.metrics['knowledge_transfers'],
            'total_tasks': self.metrics['total_tasks'],
            'completed_tasks': self.metrics['completed_tasks'],
            'prediction_accuracy': self.metrics['prediction_accuracy']
        }

# Example usage and testing
async def main():
    """Example usage of the integrated novel system"""
    # Create agents
    agents = [
        Agent(id="agent_1", capabilities=["traffic", "safety"], max_capacity=1.0),
        Agent(id="agent_2", capabilities=["weather", "parking"], max_capacity=1.0),
        Agent(id="agent_3", capabilities=["traffic", "weather"], max_capacity=1.0),
        Agent(id="agent_4", capabilities=["safety", "parking"], max_capacity=1.0)
    ]
    
    # Create integrated novel system
    system = IntegratedNovelSystem(agents, cache_capacity=100)
    
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
    
    print("Novel System Performance Metrics:")
    print(json.dumps(performance, indent=2))
    
    return results

if __name__ == "__main__":
    asyncio.run(main())



