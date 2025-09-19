"""
Environment Configuration
环境配置文件
"""

import os
from typing import Optional

class Config:
    """应用配置类"""
    
    # 基础配置
    APP_NAME: str = "Multi-Agent DSL Framework"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # 服务器配置
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8008"))
    
    # 数据库配置
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    # Redis配置（用于缓存）
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # WebSocket配置
    WS_HOST: str = os.getenv("WS_HOST", "localhost")
    WS_PORT: int = int(os.getenv("WS_PORT", "8008"))
    
    # 前端配置
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3001")
    
    # 性能配置
    MAX_CONCURRENT_EVENTS: int = int(os.getenv("MAX_CONCURRENT_EVENTS", "1000"))
    EVENT_TIMEOUT: int = int(os.getenv("EVENT_TIMEOUT", "30"))  # seconds
    
    # 缓存配置
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "300"))  # 5 minutes
    CACHE_MAX_SIZE: int = int(os.getenv("CACHE_MAX_SIZE", "10000"))
    
    # 日志配置
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE")
    
    # 监控配置
    ENABLE_METRICS: bool = os.getenv("ENABLE_METRICS", "true").lower() == "true"
    METRICS_PORT: int = int(os.getenv("METRICS_PORT", "9090"))
    
    # 安全配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3001").split(",")
    
    # 智能体配置
    AGENT_TIMEOUT: int = int(os.getenv("AGENT_TIMEOUT", "60"))  # seconds
    MAX_AGENTS: int = int(os.getenv("MAX_AGENTS", "50"))
    
    @classmethod
    def validate(cls) -> bool:
        """验证配置"""
        required_vars = [
            "HOST", "PORT", "DATABASE_URL", "FRONTEND_URL"
        ]
        
        for var in required_vars:
            if not getattr(cls, var):
                raise ValueError(f"Required configuration {var} is not set")
        
        return True
    
    @classmethod
    def get_database_config(cls) -> dict:
        """获取数据库配置"""
        return {
            "url": cls.DATABASE_URL,
            "echo": cls.DEBUG,
            "pool_size": 10,
            "max_overflow": 20
        }
    
    @classmethod
    def get_redis_config(cls) -> dict:
        """获取Redis配置"""
        return {
            "url": cls.REDIS_URL,
            "decode_responses": True,
            "socket_timeout": 5,
            "socket_connect_timeout": 5
        }

# 开发环境配置
class DevelopmentConfig(Config):
    ENVIRONMENT = "development"
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    CACHE_TTL = 60  # 1 minute for dev

# 生产环境配置
class ProductionConfig(Config):
    ENVIRONMENT = "production"
    DEBUG = False
    LOG_LEVEL = "WARNING"
    CACHE_TTL = 3600  # 1 hour for prod

# 测试环境配置
class TestingConfig(Config):
    ENVIRONMENT = "testing"
    DEBUG = True
    DATABASE_URL = "sqlite:///./test.db"
    CACHE_TTL = 1  # 1 second for testing
    MAX_CONCURRENT_EVENTS = 100

# 配置工厂
def get_config() -> Config:
    """根据环境变量获取配置"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()

# 导出配置实例
config = get_config()
