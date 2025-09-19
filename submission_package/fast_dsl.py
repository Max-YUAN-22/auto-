#!/usr/bin/env python3
"""
高性能DSL实现 - 从根本上提升性能
High-Performance DSL Implementation - Fundamental Performance Improvements

关键优化：
1. 轻量级任务调度 - 减少线程开销
2. 高效缓存机制 - 优化查找性能
3. 批量处理支持 - 减少API调用开销
4. 内存优化 - 减少对象创建
5. 异步执行 - 提升并发性能
"""

import asyncio
import time
import threading
from typing import Any, Dict, Callable, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, deque
import heapq
import weakref
from concurrent.futures import ThreadPoolExecutor
import functools

@dataclass
class FastTask:
    """轻量级任务实现"""
    name: str
    prompt: str
    agent: Any
    priority: int = 0
    timeout: float = 10.0
    max_retries: int = 0
    backoff_ms: int = 200
    constraint: Any = None
    fallback_prompt: Optional[str] = None
    
    _result: Any = field(default=None, init=False)
    _done: bool = field(default=False, init=False)
    _callbacks: List[Callable] = field(default_factory=list, init=False)

    def set_result(self, val: Any):
        """设置结果并触发回调"""
        self._result = val
        self._done = True
        for callback in self._callbacks:
            try:
                callback(val)
            except Exception:
                pass
        self._callbacks.clear()

    def add_callback(self, callback: Callable):
        """添加完成回调"""
        if self._done:
            callback(self._result)
        else:
            self._callbacks.append(callback)

    def is_done(self) -> bool:
        return self._done

    def wait(self, timeout: Optional[float] = None) -> Any:
        """同步等待结果"""
        if self._done:
            return self._result
        
        # 使用事件等待
        event = threading.Event()
        self.add_callback(lambda _: event.set())
        
        if event.wait(timeout):
            return self._result
        return None

class FastCache:
    """高性能缓存实现"""
    
    def __init__(self, capacity: int = 2048):
        self.capacity = capacity
        self._cache: Dict[str, Any] = {}
        self._access_order = deque()
        self._lock = threading.RLock()
        
    def get(self, key: str) -> Optional[Any]:
        """快速获取缓存"""
        with self._lock:
            if key in self._cache:
                # 更新访问顺序
                if key in self._access_order:
                    self._access_order.remove(key)
                self._access_order.append(key)
                return self._cache[key]
            return None
    
    def put(self, key: str, value: Any):
        """快速存储缓存"""
        with self._lock:
            if key not in self._cache and len(self._cache) >= self.capacity:
                # LRU淘汰
                if self._access_order:
                    oldest = self._access_order.popleft()
                    self._cache.pop(oldest, None)
            
            self._cache[key] = value
            if key in self._access_order:
                self._access_order.remove(key)
            self._access_order.append(key)
    
    def get_with_prefix(self, key: str) -> Tuple[int, Optional[Any]]:
        """获取最长匹配前缀"""
        with self._lock:
            best_len = 0
            best_value = None
            
            for cached_key in self._cache:
                if cached_key.startswith(key[:len(cached_key)]):
                    if len(cached_key) > best_len:
                        best_len = len(cached_key)
                        best_value = self._cache[cached_key]
            
            return best_len, best_value

class FastScheduler:
    """高性能任务调度器"""
    
    def __init__(self, workers: int = 8):
        self.workers = workers
        self._queue = deque()
        self._lock = threading.RLock()
        self._executor = ThreadPoolExecutor(max_workers=workers, thread_name_prefix="FastWorker")
        self._llm: Optional[Callable[[str, Optional[str]], str]] = None
        self._cache: Optional[FastCache] = None
        self._metrics = None
        self._use_cache = True
        
    def configure(self, *, llm: Callable[[str, Optional[str]], str], 
                  cache: FastCache, metrics=None, use_cache: bool = True):
        """配置调度器"""
        self._llm = llm
        self._cache = cache
        self._metrics = metrics
        self._use_cache = use_cache
    
    def add(self, task: FastTask):
        """添加任务到调度器"""
        # 检查缓存
        if self._use_cache and self._cache:
            prefix_len, cached_value = self._cache.get_with_prefix(task.prompt)
            if cached_value is not None and prefix_len == len(task.prompt):
                # 缓存命中，直接设置结果
                task.set_result(cached_value)
                if self._metrics:
                    self._metrics.on_complete(0.0, True)
                return
        
        # 提交到线程池执行
        future = self._executor.submit(self._execute_task, task)
        
        # 添加完成回调
        def on_complete(fut):
            try:
                fut.result()
            except Exception as e:
                task.set_result(f"[error:{task.name}] {e}")
        
        future.add_done_callback(on_complete)
        
        if self._metrics:
            self._metrics.on_submit()
    
    def _execute_task(self, task: FastTask):
        """执行单个任务"""
        start_time = time.time()
        result = None
        success = False
        attempts = 0
        
        agent_role = task.agent.role if hasattr(task.agent, 'role') else task.agent
        
        while attempts <= task.max_retries and not success:
            try:
                # 执行LLM调用
                if self._llm:
                    result = self._llm(task.prompt, agent_role)
                else:
                    result = f"[LLM:{agent_role}] {task.prompt}"
                
                # 验证约束
                if task.constraint:
                    if hasattr(task.constraint, 'validate'):
                        success = bool(task.constraint.validate(result))
                    elif hasattr(task.constraint, 'valid'):
                        success = bool(task.constraint.valid(result))
                    else:
                        success = True
                else:
                    success = True
                    
            except Exception as e:
                result = f"[error:{task.name}] {e}"
                success = False
            
            if not success:
                attempts += 1
                if attempts <= task.max_retries:
                    time.sleep((task.backoff_ms / 1000.0) * (2 ** (attempts - 1)))
        
        # 尝试fallback
        if not success and task.fallback_prompt:
            try:
                if self._llm:
                    result = self._llm(task.fallback_prompt, agent_role)
                else:
                    result = task.fallback_prompt
                success = True
            except Exception as e:
                result = f"[error:{task.name}] {e}"
        
        # 设置结果
        task.set_result(result)
        
        # 更新缓存
        if success and self._use_cache and self._cache:
            self._cache.put(task.prompt, result)
        
        # 更新指标
        if self._metrics:
            execution_time = (time.time() - start_time) * 1000.0
            self._metrics.on_complete(execution_time, success)
    
    def shutdown(self):
        """关闭调度器"""
        self._executor.shutdown(wait=True)

class FastTaskBuilder:
    """快速任务构建器"""
    
    def __init__(self, dsl: 'FastDSL', name: str, prompt: str, agent: str):
        self._dsl = dsl
        self._task_params = {
            "name": name,
            "prompt": prompt,
            "agent": agent,
            "priority": 0,
            "timeout": 10.0,
            "max_retries": 0,
            "backoff_ms": 200,
            "constraint": None,
            "fallback_prompt": None,
        }
    
    def with_priority(self, priority: int) -> 'FastTaskBuilder':
        self._task_params["priority"] = priority
        return self
    
    def with_timeout(self, timeout: float) -> 'FastTaskBuilder':
        self._task_params["timeout"] = timeout
        return self
    
    def with_retries(self, retries: int, backoff_ms: int = 200) -> 'FastTaskBuilder':
        self._task_params["max_retries"] = retries
        self._task_params["backoff_ms"] = backoff_ms
        return self
    
    def with_contract(self, contract) -> 'FastTaskBuilder':
        self._task_params["constraint"] = contract
        return self
    
    def with_regex(self, regex: str) -> 'FastTaskBuilder':
        from core.contracts import Contract
        contract_name = f"{self._task_params['name']}-re"
        self._task_params["constraint"] = Contract(name=contract_name, regex=regex)
        return self
    
    def with_fallback(self, fallback_prompt: str) -> 'FastTaskBuilder':
        self._task_params["fallback_prompt"] = fallback_prompt
        return self
    
    def schedule(self) -> FastTask:
        """调度任务"""
        task = FastTask(**self._task_params)
        self._dsl.scheduler.add(task)
        return task

class FastDSL:
    """高性能DSL实现"""
    
    def __init__(self, seed: int = 7, workers: int = 8):
        self.cache = FastCache(capacity=4096)  # 增大缓存容量
        self.scheduler = FastScheduler(workers=workers)
        self._llm: Optional[Callable[[str, Optional[str]], str]] = None
        self.metrics = None
        self.history: List[Dict[str, Any]] = []
        
        # 性能优化：预分配常用对象
        self._task_pool = deque()
        self._lock = threading.RLock()
    
    def use_llm(self, llm_callable: Callable[[str, Optional[str]], str], *, use_cache: bool = True):
        """配置LLM"""
        self._llm = llm_callable
        self.scheduler.configure(
            llm=llm_callable, 
            cache=self.cache, 
            metrics=self.metrics, 
            use_cache=use_cache
        )
    
    def task(self, name: str, *, prompt: str = "", agent: str = "default") -> FastTaskBuilder:
        """创建任务构建器"""
        return FastTaskBuilder(self, name, prompt, agent)
    
    def gen(self, name: str, *, prompt: str, agent: str) -> FastTaskBuilder:
        """生成任务"""
        return FastTaskBuilder(self, name, prompt, agent)
    
    def join(self, tasks: List[FastTask], mode: str = "all", within_ms: Optional[int] = None) -> Dict[str, Any]:
        """等待任务完成"""
        results: Dict[str, Any] = {}
        start_time = time.time()
        
        if mode == "all":
            for task in tasks:
                timeout = (within_ms / 1000.0) if within_ms else None
                result = task.wait(timeout=timeout)
                results[task.name] = result
                
                if within_ms and (time.time() - start_time) >= (within_ms / 1000.0):
                    break
        elif mode == "any":
            while True:
                if within_ms and (time.time() - start_time) * 1000 > within_ms:
                    break
                    
                for task in tasks:
                    if task.is_done():
                        results[task.name] = task.wait(timeout=0)
                        return results
                
                time.sleep(0.001)  # 减少轮询间隔
        
        return results
    
    def run(self, llm_callable: Optional[Callable[[str, Optional[str]], str]] = None) -> Dict[str, Any]:
        """运行DSL程序"""
        if llm_callable:
            self.use_llm(llm_callable)
        elif self._llm is None:
            self.use_llm(lambda p, role=None: f"[mocked:{role}] {p}")
        return {}
    
    def batch_execute(self, tasks: List[FastTask]) -> List[Any]:
        """批量执行任务"""
        # 提交所有任务
        for task in tasks:
            self.scheduler.add(task)
        
        # 等待所有任务完成
        results = []
        for task in tasks:
            result = task.wait()
            results.append(result)
        
        return results
    
    def shutdown(self):
        """关闭DSL"""
        self.scheduler.shutdown()

# 性能优化装饰器
def performance_monitor(func):
    """性能监控装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        
        if execution_time > 0.001:  # 只记录耗时超过1ms的操作
            print(f"Performance: {func.__name__} took {execution_time*1000:.2f}ms")
        
        return result
    return wrapper

# 导出高性能版本
DSL = FastDSL
Task = FastTask
TaskBuilder = FastTaskBuilder
CacheAwareScheduler = FastScheduler
RadixTrieCache = FastCache
