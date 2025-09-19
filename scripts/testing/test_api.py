#!/usr/bin/env python3
"""
测试代理API是否正常工作
"""

import os
from openai import OpenAI

def test_api():
    """测试API连接"""
    try:
        client = OpenAI(
            base_url="https://www.yunqiaoai.top/v1",
            api_key="sk-wqJXkfEYHrJNnEJhQ9OLoZ5dP4FqwCKLLdxqMM7LP2wZXnAY"
        )
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hello, please respond with 'API test successful'"},
            ],
            max_tokens=50
        )
        
        print("✅ API测试成功!")
        print(f"响应: {response.choices[0].message.content}")
        print(f"模型: {response.model}")
        print(f"使用tokens: {response.usage.total_tokens}")
        
        return True
        
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False

if __name__ == "__main__":
    print("测试代理API连接...")
    test_api()

