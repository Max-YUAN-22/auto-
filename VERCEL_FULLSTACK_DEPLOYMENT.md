# Vercel全栈部署方案

## 方案概述
将后端API作为Vercel Serverless Functions部署，前端和后端都在Vercel上。

## 部署步骤

### 1. 修改Vercel配置
在Vercel项目根目录创建 `vercel.json`：

```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    },
    {
      "src": "backend/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/backend/main.py"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/build/$1"
    }
  ]
}
```

### 2. 创建Vercel API路由
在 `api/` 目录下创建API路由文件。

### 3. 重新部署
推送代码后Vercel会自动部署全栈应用。

## 优势
- 完全免费
- 前后端同域
- 自动扩缩容
- 全球CDN
- 无需额外配置
