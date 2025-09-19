#!/bin/bash

# Multi-Agent DSL Framework 启动脚本
# 确保后端服务正常运行

echo "🚀 启动 Multi-Agent DSL Framework..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 检查Node.js环境
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装Node.js"
    exit 1
fi

# 检查依赖
echo "📦 检查依赖..."

# 检查Python依赖
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt 文件不存在"
    exit 1
fi

# 检查Node.js依赖
if [ ! -f "frontend/package.json" ]; then
    echo "❌ frontend/package.json 文件不存在"
    exit 1
fi

# 安装Python依赖
echo "📦 安装Python依赖..."
pip3 install -r requirements.txt

# 安装Node.js依赖
echo "📦 安装Node.js依赖..."
cd frontend
npm install
cd ..

# 检查端口是否被占用
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  端口 $1 已被占用，尝试停止现有服务..."
        lsof -ti:$1 | xargs kill -9 2>/dev/null || true
        sleep 2
    fi
}

# 检查后端端口
check_port 8008

# 启动后端服务
echo "🔧 启动后端服务..."
cd backend
python3 main.py &
BACKEND_PID=$!
cd ..

# 等待后端启动
echo "⏳ 等待后端服务启动..."
sleep 5

# 检查后端是否启动成功
if ! curl -s http://localhost:8008/health > /dev/null 2>&1; then
    echo "❌ 后端服务启动失败"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

echo "✅ 后端服务启动成功"

# 启动前端服务
echo "🌐 启动前端服务..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo "🎉 Multi-Agent DSL Framework 启动完成！"
echo "📱 前端地址: http://localhost:3001"
echo "🔧 后端地址: http://localhost:8008"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
trap 'echo "🛑 正在停止服务..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0' INT

# 保持脚本运行
wait
