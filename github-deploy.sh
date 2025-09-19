#!/bin/bash

# GitHub云部署脚本
echo "🚀 开始GitHub云部署..."

# 检查Git状态
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 检测到未提交的更改，正在提交..."
    git add .
    git commit -m "feat: 更新多智能体DSL框架功能 - $(date '+%Y-%m-%d %H:%M:%S')"
else
    echo "📝 没有检测到更改，创建空提交触发部署..."
    git commit --allow-empty -m "trigger: 触发GitHub Actions部署 - $(date '+%Y-%m-%d %H:%M:%S')"
fi

# 推送到GitHub
echo "📤 推送到GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ 代码推送成功！"
    echo ""
    echo "🔄 GitHub Actions正在自动部署..."
    echo "⏱️  预计部署时间：3-5分钟"
    echo ""
    echo "🌐 部署完成后可通过以下地址访问："
    echo "   📱 GitHub Pages: https://max-yuan-22.github.io/Multi-Agent_DSLframework-2025/"
    echo "   🚀 Vercel: https://multi-agent-ds-lframework-2025.vercel.app"
    echo ""
    echo "📊 监控部署状态："
    echo "   🔗 https://github.com/Max-YUAN-22/Multi-Agent_DSLframework-2025/actions"
    echo ""
    echo "🎯 应用功能："
    echo "   🏠 首页 - 项目介绍和性能指标"
    echo "   💻 DSL演示 - ATSLP、HCMPL、CALK算法演示"
    echo "   🤖 智能体管理 - 12个智能体管理界面"
    echo "   📊 交互记录 - 智能体协作历史"
    echo "   📚 学术论文 - 研究成果展示"
    echo "   📈 企业仪表板 - 实时系统监控"
    echo ""
    echo "🎉 部署已启动，请稍候访问应用！"
else
    echo "❌ 推送失败，请检查网络连接和GitHub权限"
    exit 1
fi
