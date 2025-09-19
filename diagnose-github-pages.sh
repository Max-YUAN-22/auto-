#!/bin/bash

echo "🔍 GitHub Pages 部署失败诊断"
echo "============================"

echo "📊 失败分析:"
echo "• 失败时间: 8秒 (瞬间失败)"
echo "• 失败任务: Deploy to GitHub Pages"
echo "• 可能原因: 权限配置或Pages设置问题"

echo ""
echo "🔧 常见问题和解决方案:"

echo ""
echo "1. 📋 GitHub Pages 设置检查:"
echo "   请访问: https://github.com/Max-YUAN-22/Multi-Agent_DSLframework-2025/settings/pages"
echo "   确保设置:"
echo "   • Source: GitHub Actions"
echo "   • Branch: 不设置 (使用Actions部署)"

echo ""
echo "2. 🔐 权限配置检查:"
echo "   请访问: https://github.com/Max-YUAN-22/Multi-Agent_DSLframework-2025/settings/actions"
echo "   确保设置:"
echo "   • Actions permissions: Read and write permissions"
echo "   • Workflow permissions: Read and write permissions"

echo ""
echo "3. 🏗️ 工作流简化:"
echo "   ✅ 已移除复杂的任务依赖"
echo "   ✅ 使用简化的部署流程"
echo "   ✅ 保留核心功能"

echo ""
echo "4. 📁 构建文件检查:"
echo "   确保 frontend/build 目录存在且包含文件"

# 检查本地构建文件
if [ -d "frontend/build" ]; then
    echo "   ✅ frontend/build 目录存在"
    echo "   📄 构建文件:"
    ls -la frontend/build/ | head -10
else
    echo "   ❌ frontend/build 目录不存在"
    echo "   🔧 正在构建..."
    cd frontend && npm run build && cd ..
fi

echo ""
echo "🚀 修复步骤:"
echo "1. 检查GitHub Pages设置"
echo "2. 检查仓库权限"
echo "3. 重新触发工作流"
echo "4. 监控部署状态"

echo ""
echo "🌐 访问地址:"
echo "• GitHub Pages: https://max-yuan-22.github.io/Multi-Agent_DSLframework-2025/"
echo "• Vercel: https://multi-agent-ds-lframework-2025.vercel.app"
echo "• GitHub Actions: https://github.com/Max-YUAN-22/Multi-Agent_DSLframework-2025/actions"
