# backend/api_key_manager.py
import os
import json
import hashlib
from typing import Dict, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class APIKeyConfig(BaseModel):
    deepseek_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    openweather_api_key: Optional[str] = None
    google_maps_api_key: Optional[str] = None
    alpha_vantage_api_key: Optional[str] = None

class APIKeyResponse(BaseModel):
    status: str
    message: str
    available_services: list

# 存储API密钥的临时字典（生产环境应使用数据库）
api_keys_storage: Dict[str, str] = {}

def get_api_key_hash(key: str) -> str:
    """生成API密钥的哈希值用于存储"""
    return hashlib.sha256(key.encode()).hexdigest()

@router.post("/api-keys/configure")
async def configure_api_keys(config: APIKeyConfig):
    """配置API密钥"""
    try:
        if config.deepseek_api_key:
            api_keys_storage["deepseek"] = config.deepseek_api_key
            os.environ["DEEPSEEK_API_KEY"] = config.deepseek_api_key
            
        if config.openai_api_key:
            api_keys_storage["openai"] = config.openai_api_key
            os.environ["OPENAI_API_KEY"] = config.openai_api_key
            
        if config.openweather_api_key:
            api_keys_storage["openweather"] = config.openweather_api_key
            os.environ["OPENWEATHER_API_KEY"] = config.openweather_api_key
            
        if config.google_maps_api_key:
            api_keys_storage["google_maps"] = config.google_maps_api_key
            os.environ["GOOGLE_MAPS_API_KEY"] = config.google_maps_api_key
            
        if config.alpha_vantage_api_key:
            api_keys_storage["alpha_vantage"] = config.alpha_vantage_api_key
            os.environ["ALPHA_VANTAGE_API_KEY"] = config.alpha_vantage_api_key
        
        return {
            "status": "success",
            "message": "API密钥配置成功",
            "configured_services": list(api_keys_storage.keys())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"配置失败: {str(e)}")

@router.get("/api-keys/status")
async def get_api_keys_status():
    """获取API密钥状态"""
    available_services = []
    
    if api_keys_storage.get("deepseek"):
        available_services.append("DeepSeek LLM")
    if api_keys_storage.get("openai"):
        available_services.append("OpenAI GPT")
    if api_keys_storage.get("openweather"):
        available_services.append("OpenWeather")
    if api_keys_storage.get("google_maps"):
        available_services.append("Google Maps")
    if api_keys_storage.get("alpha_vantage"):
        available_services.append("Alpha Vantage")
    
    return APIKeyResponse(
        status="success",
        message=f"已配置 {len(available_services)} 个服务",
        available_services=available_services
    )

@router.post("/api-keys/validate")
async def validate_api_keys():
    """验证API密钥有效性"""
    validation_results = {}
    
    # 验证DeepSeek API
    if api_keys_storage.get("deepseek"):
        try:
            from openai import OpenAI
            client = OpenAI(
                base_url='https://api.deepseek.com',
                api_key=api_keys_storage["deepseek"]
            )
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            validation_results["deepseek"] = {"status": "valid", "message": "DeepSeek API连接成功"}
        except Exception as e:
            validation_results["deepseek"] = {"status": "invalid", "message": f"DeepSeek API验证失败: {str(e)}"}
    
    # 验证OpenAI API
    if api_keys_storage.get("openai"):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_keys_storage["openai"])
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            validation_results["openai"] = {"status": "valid", "message": "OpenAI API连接成功"}
        except Exception as e:
            validation_results["openai"] = {"status": "invalid", "message": f"OpenAI API验证失败: {str(e)}"}
    
    return {
        "status": "success",
        "validation_results": validation_results
    }

@router.delete("/api-keys/clear")
async def clear_api_keys():
    """清除所有API密钥"""
    api_keys_storage.clear()
    # 清除环境变量
    for key in ["DEEPSEEK_API_KEY", "OPENAI_API_KEY", "OPENWEATHER_API_KEY", "GOOGLE_MAPS_API_KEY", "ALPHA_VANTAGE_API_KEY"]:
        if key in os.environ:
            del os.environ[key]
    
    return {
        "status": "success",
        "message": "所有API密钥已清除"
    }
