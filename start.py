#!/usr/bin/env python3
"""
Render部署专用启动脚本
"""
import os
import sys
import uvicorn

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # 获取Render提供的端口
    port = int(os.environ.get("PORT", 8000))
    
    # 启动FastAPI应用
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
