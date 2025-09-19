#!/bin/bash

echo "🚀 启动智能城市多智能体系统（简化版）..."

# 清理现有进程
echo "🧹 清理现有进程..."
pkill -f "uvicorn" 2>/dev/null
pkill -f "react-scripts" 2>/dev/null
pkill -f "proxyServer" 2>/dev/null
sleep 2

# 启动后端服务
echo "🔧 启动后端服务 (端口 8008)..."
cd backend
python3 -c "
import sys
sys.path.append('..')
from backend.main import app
import uvicorn
print('后端服务启动中...')
uvicorn.run(app, host='0.0.0.0', port=8008)
" &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 5

# 测试后端
echo "🔍 测试后端服务..."
if curl -s http://localhost:8008/health > /dev/null; then
    echo "✅ 后端服务启动成功"
else
    echo "❌ 后端服务启动失败"
    exit 1
fi

# 启动前端服务
echo "🎨 启动前端服务 (端口 3000)..."
cd frontend
PORT=3000 npm start &
FRONTEND_PID=$!
cd ..

# 等待前端启动
sleep 10

echo ""
echo "🎉 系统启动完成！"
echo ""
echo "📱 前端地址: http://localhost:3000"
echo "🔧 后端地址: http://localhost:8008"
echo "📡 WebSocket: ws://localhost:8008/socket.io"
echo ""
echo "💡 使用说明:"
echo "   1. 打开浏览器访问 http://localhost:3000"
echo "   2. 点击任意智能体卡片的'发送'按钮"
echo "   3. 观察交互记录中的智能体协作过程"
echo "   4. 点击'生成报告'按钮查看分析报告"
echo ""
echo "🛑 停止服务: 按 Ctrl+C"

# 等待用户中断
trap "echo ''; echo '🛑 正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo '✅ 服务已停止'; exit 0" INT

# 保持脚本运行
wait
