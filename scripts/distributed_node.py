#!/usr/bin/env python3
"""
Multi-Agent DSL Framework: Distributed Node
多智能体DSL框架：分布式节点

This script runs a single distributed node in the system.
"""

import asyncio
import argparse
import json
import logging
import os
import time
from typing import Dict, List, Any
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import psycopg2
from psycopg2.extras import RealDictCursor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Node configuration
NODE_ID = os.getenv('NODE_ID', 'default_node')
NODE_HOST = os.getenv('NODE_HOST', 'localhost')
NODE_PORT = int(os.getenv('NODE_PORT', '8000'))
CPU_CORES = int(os.getenv('CPU_CORES', '4'))
MEMORY_GB = int(os.getenv('MEMORY_GB', '8'))
NETWORK_LATENCY_MS = float(os.getenv('NETWORK_LATENCY_MS', '10.0'))
BANDWIDTH_MBPS = float(os.getenv('BANDWIDTH_MBPS', '1000.0'))
CAPABILITIES = os.getenv('CAPABILITIES', 'traffic,safety').split(',')

# FastAPI app
app = FastAPI(title=f"DSL Node {NODE_ID}", version="1.0.0")

# Redis connection
redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

# PostgreSQL connection
def get_db_connection():
    return psycopg2.connect(
        host='postgres',
        port=5432,
        database='dsl_framework',
        user='dsl_user',
        password='dsl_password'
    )

# Pydantic models
class TaskRequest(BaseModel):
    task_id: str
    complexity: str
    required_capabilities: List[str]
    estimated_duration: float
    priority: int
    deadline: float = None
    dependencies: List[str] = []

class TaskResponse(BaseModel):
    task_id: str
    node_id: str
    result: Any
    execution_time: float
    network_latency: float
    success: bool
    timestamp: float

class NodeStatus(BaseModel):
    node_id: str
    status: str
    current_load: float
    max_capacity: float
    capabilities: List[str]
    completed_tasks: int
    failed_tasks: int
    average_performance: float
    uptime: float

# Node state
node_state = {
    'current_load': 0.0,
    'max_capacity': 1.0,
    'completed_tasks': 0,
    'failed_tasks': 0,
    'performance_history': [],
    'start_time': time.time(),
    'is_active': True
}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "node_id": NODE_ID,
        "timestamp": time.time()
    }

@app.get("/status", response_model=NodeStatus)
async def get_node_status():
    """Get current node status"""
    uptime = time.time() - node_state['start_time']
    avg_performance = sum(node_state['performance_history']) / len(node_state['performance_history']) if node_state['performance_history'] else 0.0
    
    return NodeStatus(
        node_id=NODE_ID,
        status="active" if node_state['is_active'] else "inactive",
        current_load=node_state['current_load'],
        max_capacity=node_state['max_capacity'],
        capabilities=CAPABILITIES,
        completed_tasks=node_state['completed_tasks'],
        failed_tasks=node_state['failed_tasks'],
        average_performance=avg_performance,
        uptime=uptime
    )

@app.post("/execute", response_model=TaskResponse)
async def execute_task(task_request: TaskRequest):
    """Execute a task on this node"""
    try:
        # Check if node can handle this task
        if not any(cap in CAPABILITIES for cap in task_request.required_capabilities):
            raise HTTPException(
                status_code=400, 
                detail=f"Node {NODE_ID} cannot handle capabilities: {task_request.required_capabilities}"
            )
        
        # Check if node has capacity
        if node_state['current_load'] >= node_state['max_capacity']:
            raise HTTPException(
                status_code=503,
                detail=f"Node {NODE_ID} is at capacity"
            )
        
        # Execute task
        start_time = time.time()
        
        # Simulate task execution
        execution_time = task_request.estimated_duration
        
        # Add network latency simulation
        network_latency = NETWORK_LATENCY_MS / 1000.0
        await asyncio.sleep(execution_time + network_latency)
        
        # Generate result
        result = {
            'task_id': task_request.task_id,
            'node_id': NODE_ID,
            'complexity': task_request.complexity,
            'execution_time': execution_time,
            'network_latency': network_latency,
            'capabilities_used': task_request.required_capabilities
        }
        
        # Update node state
        node_state['current_load'] += execution_time
        node_state['completed_tasks'] += 1
        node_state['performance_history'].append(execution_time)
        
        # Keep only recent performance history
        if len(node_state['performance_history']) > 100:
            node_state['performance_history'].pop(0)
        
        # Store result in Redis
        redis_client.setex(
            f"task_result:{task_request.task_id}",
            3600,  # 1 hour TTL
            json.dumps(result)
        )
        
        # Store result in PostgreSQL
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO task_results 
                    (task_id, node_id, result, execution_time, network_latency, success, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    task_request.task_id,
                    NODE_ID,
                    json.dumps(result),
                    execution_time,
                    network_latency,
                    True,
                    time.time()
                ))
                conn.commit()
        
        return TaskResponse(
            task_id=task_request.task_id,
            node_id=NODE_ID,
            result=result,
            execution_time=execution_time,
            network_latency=network_latency,
            success=True,
            timestamp=time.time()
        )
        
    except Exception as e:
        logger.error(f"Task execution failed: {e}")
        node_state['failed_tasks'] += 1
        
        # Store failure in PostgreSQL
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO task_results 
                    (task_id, node_id, result, execution_time, network_latency, success, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    task_request.task_id,
                    NODE_ID,
                    None,
                    0.0,
                    0.0,
                    False,
                    time.time()
                ))
                conn.commit()
        
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    metrics = []
    
    # Node metrics
    metrics.append(f"dsl_node_current_load{{node_id=\"{NODE_ID}\"}} {node_state['current_load']}")
    metrics.append(f"dsl_node_max_capacity{{node_id=\"{NODE_ID}\"}} {node_state['max_capacity']}")
    metrics.append(f"dsl_node_completed_tasks{{node_id=\"{NODE_ID}\"}} {node_state['completed_tasks']}")
    metrics.append(f"dsl_node_failed_tasks{{node_id=\"{NODE_ID}\"}} {node_state['failed_tasks']}")
    
    # Performance metrics
    if node_state['performance_history']:
        avg_performance = sum(node_state['performance_history']) / len(node_state['performance_history'])
        metrics.append(f"dsl_node_average_performance{{node_id=\"{NODE_ID}\"}} {avg_performance}")
    
    # System metrics
    metrics.append(f"dsl_node_cpu_cores{{node_id=\"{NODE_ID}\"}} {CPU_CORES}")
    metrics.append(f"dsl_node_memory_gb{{node_id=\"{NODE_ID}\"}} {MEMORY_GB}")
    metrics.append(f"dsl_node_network_latency_ms{{node_id=\"{NODE_ID}\"}} {NETWORK_LATENCY_MS}")
    metrics.append(f"dsl_node_bandwidth_mbps{{node_id=\"{NODE_ID}\"}} {BANDWIDTH_MBPS}")
    
    # Uptime
    uptime = time.time() - node_state['start_time']
    metrics.append(f"dsl_node_uptime_seconds{{node_id=\"{NODE_ID}\"}} {uptime}")
    
    return "\n".join(metrics)

@app.post("/cache/get")
async def get_from_cache(key: str):
    """Get value from distributed cache"""
    try:
        value = redis_client.get(key)
        if value:
            return {"key": key, "value": json.loads(value), "found": True}
        else:
            return {"key": key, "value": None, "found": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cache/put")
async def put_to_cache(key: str, value: Any):
    """Put value to distributed cache"""
    try:
        redis_client.setex(key, 3600, json.dumps(value))  # 1 hour TTL
        return {"key": key, "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cache/invalidate")
async def invalidate_cache(key: str):
    """Invalidate cache entry"""
    try:
        redis_client.delete(key)
        return {"key": key, "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("startup")
async def startup_event():
    """Initialize node on startup"""
    logger.info(f"Starting DSL Node {NODE_ID}")
    logger.info(f"Capabilities: {CAPABILITIES}")
    logger.info(f"Network latency: {NETWORK_LATENCY_MS}ms")
    logger.info(f"Bandwidth: {BANDWIDTH_MBPS}Mbps")
    
    # Initialize database tables
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS task_results (
                        id SERIAL PRIMARY KEY,
                        task_id VARCHAR(255) NOT NULL,
                        node_id VARCHAR(255) NOT NULL,
                        result JSONB,
                        execution_time FLOAT,
                        network_latency FLOAT,
                        success BOOLEAN,
                        timestamp FLOAT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
        logger.info("Database tables initialized")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info(f"Shutting down DSL Node {NODE_ID}")
    node_state['is_active'] = False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='DSL Distributed Node')
    parser.add_argument('--node-id', default=NODE_ID, help='Node ID')
    parser.add_argument('--port', type=int, default=NODE_PORT, help='Port number')
    parser.add_argument('--host', default='0.0.0.0', help='Host address')
    
    args = parser.parse_args()
    
    logger.info(f"Starting DSL Node {args.node_id} on {args.host}:{args.port}")
    
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        log_level="info"
    )

if __name__ == "__main__":
    main()



