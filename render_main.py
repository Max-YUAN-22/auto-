"""
Render部署专用后端启动文件
简化版本，避免复杂的相对导入
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 创建FastAPI应用
app = FastAPI(title="Multi-Agent DSL Framework API")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Multi-Agent DSL Framework API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "multi-agent-dsl-backend"}

@app.get("/api/status")
async def api_status():
    return {
        "status": "active",
        "version": "1.0.0",
        "services": ["deepseek", "openai", "openweather", "google_maps", "alpha_vantage"]
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
