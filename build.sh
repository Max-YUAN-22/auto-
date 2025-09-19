#!/bin/bash

# 构建脚本
echo "🚀 开始构建多智能体DSL框架..."

# 进入frontend目录
cd frontend

# 安装依赖
echo "📦 安装依赖..."
npm install

# 构建项目
echo "🔨 构建项目..."
npm run build

echo "✅ 构建完成！"
