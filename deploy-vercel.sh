#!/bin/bash

# Vercel部署脚本
echo "🚀 开始部署到Vercel..."

# 检查是否安装了Vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "📦 安装Vercel CLI..."
    npm install -g vercel
fi

# 进入前端目录
cd frontend

# 构建应用
echo "🔨 构建应用..."
npm run build

# 检查构建是否成功
if [ $? -eq 0 ]; then
    echo "✅ 构建成功！"
    
    # 部署到Vercel
    echo "🌐 部署到Vercel..."
    vercel --prod
    
    echo "🎉 部署完成！"
    echo "访问地址: https://multi-agent-ds-lframework-2025.vercel.app"
else
    echo "❌ 构建失败，请检查错误信息"
    exit 1
fi
